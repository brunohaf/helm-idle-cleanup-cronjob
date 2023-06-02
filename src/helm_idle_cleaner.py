from configs import Configs
from services import PrometheusClient
from subprocess import run
from pygelf import GelfUdpHandler
import logging
import json

# Configuration
configs = Configs()

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
allowed_list_command = ["kubectl", "get", "deployments","--no-headers" ,"-l", f'team in ({",".join(configs.cronjob.teams)})', "-o", "custom-columns=:metadata.name,:metadata.labels.team"]
allowed_list_command_output = run(allowed_list_command, capture_output=True, text=True)
allowed_list_raw = [e for e in allowed_list_command_output.stdout.split("\n") if e.strip()]
allowed_list = list(map(lambda item: {"release": item.split()[0], "team": item.split()[1]}, allowed_list_raw))

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