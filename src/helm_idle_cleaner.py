from configs import Configs
from services import PrometheusClient, AzureShareFileService
from kubernetes import client, config
from datetime import datetime
from pygelf import GelfHttpHandler
import logging

# Configuration.
configs = Configs()

# Kubernetes Settings (use config.load_kube_config() locally).
config.load_incluster_config()
k8s_client_instance = client.AppsV1Api()

# Prometheus Settings.
query_configs = configs.prometheus.query
prometheus = PrometheusClient(url=configs.prometheus.server_url)

#Seq Settings.
logging_configs = configs.seq
logging_templates = logging_configs.templates
logger = logging.getLogger()
logger.addHandler(GelfHttpHandler(
    host=logging_configs.server_url,
    port=logging_configs.port))

# Azure File Share Settings.
file_share_configs = configs.azure_fileshare
today = datetime.now().strftime(file_share_configs.filename_date_format)
file_path = file_share_configs.filename_template.format(file_name=today)
nodes_snapshot_file_path = file_share_configs.nodes_snapshot_filename_template.format(file_name=today)

# List elegible deployments.
allowed_list_resp = k8s_client_instance.list_namespaced_deployment(
    namespace=configs.cronjob.namespace,
    label_selector=f'team in ({",".join(configs.cronjob.teams)})')

allowed_list = list(map(
    lambda deployment: {
        "release": deployment.metadata.name,
        "team": deployment.metadata.labels.get("team")
        }, allowed_list_resp.items))

# Get from Prometheus the list of ingress with requests in the last 2 weeks.
requests_query = query_configs.template.format(
    metric=query_configs.metric,
    component=query_configs.component,
    time_range=query_configs.time_range)

query_result = prometheus.custom_query(requests_query)
to_be_purged = []

# List releases to be purged.
for ingress in query_result:
    try:
        metric = ingress.get('metric', None)
        request_rate = ingress.get('value', None)
        subject_name = metric.get('ingress', '')
        subject_data = next((e for e in allowed_list if e['release'] == subject_name), None)

        is_idle = request_rate is not None and request_rate[1] == "0"
        is_elegible = subject_data is not None

        if(is_idle and is_elegible):
            to_be_purged.append(subject_data)
            logger.warning(logging_templates.purging_message.format(subject=subject_name, team=subject_data["team"]))

    except Exception as ex:
        logger.error(logging_templates.purging_message.format(ingress=subject_name, ex_message=str(ex)))
    finally:
        continue


# Uploads releases list to be purged on Azure File Share.
azure_file_client = AzureShareFileService(
    conn_str=file_share_configs.conn_str,
    share_name=file_share_configs.share_name)

azure_file_client.upload_json_file(
    file_path=file_path,
    file=to_be_purged)

# Uploads nodes allocated/capacity snapshot to Azure File Share.
nodes = client.CoreV1Api().list_node().items
nodes_snapshot = []

for node in nodes:
    nodes_snapshot.append({
        'NodeName': node.metadata.name,
        'Allocated': {
            'cpu': node.status.allocatable['cpu'],
            'memory':  node.status.allocatable['memory']
        },
        'Capacity': {
            'cpu': node.status.capacity['cpu'],
            'memory':  node.status.capacity['memory']
        }
    })

azure_file_client.upload_json_file(
    file_path=nodes_snapshot_file_path,
    file=nodes_snapshot)
