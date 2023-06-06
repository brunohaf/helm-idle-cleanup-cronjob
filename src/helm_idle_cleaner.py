from configs import Configs
from services import PrometheusClient
from kubernetes import client, config as k8s_config
from pygelf import GelfUdpHandler
import logging

# Configuration
configs = Configs()

# Kubernetes Settings
k8s_config.load_kube_config() # k8s_config.load_incluster_config()
k8s_client_instance = client.AppsV1Api(k8s_config.new_client_from_config())

# Prometheus Settings
query_configs = configs.prometheus.query
prometheus = PrometheusClient(url=configs.prometheus.server_url)

#Seq Settings
logging_configs = configs.seq
logging_templates = logging_configs.templates
logger = logging.getLogger()
logger.addHandler(GelfUdpHandler(
    host=logging_configs.server_url,
    port=logging_configs.port))

# List elegible deployments
allowed_list_resp = k8s_client_instance.list_namespaced_deployment(
    namespace=configs.cronjob.namespace,
    label_selector=f'team in ({",".join(configs.cronjob.teams)})')

allowed_list = list(map(
    lambda deployment: {
        "release": deployment.metadata.name,
        "team": deployment.metadata.labels.get("team")
        }, allowed_list_resp.items))

# Get from Prometheus the list of ingress with requests in the last 2 weeks
requests_query = query_configs.template.format(
    metric=query_configs.metric,
    component=query_configs.component,
    time_range=query_configs.time_range)

query_result = prometheus.custom_query(requests_query)
to_be_purged = []

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
            logger.warning(logging_templates.purging_message.format(subject=subject_name))

    except Exception as ex:
        logger.error(logging_templates.purging_message.format(ingress=subject_name, ex_message=str(ex)))
    finally:
        continue

go = f"save_on_blob_storage({to_be_purged})"