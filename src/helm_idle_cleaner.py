from configs import Configs
from services import PrometheusClient
from subprocess import run
from pygelf import GelfUdpHandler
import logging
import json

# Configuration
configs = Configs()

# Cronjob Settings
allowed_teams = configs.cronjob.teams

# Prometheus Settings
prometheus_configs = configs.prometheus
prometheus = PrometheusClient(url=prometheus_configs.server_url)

#Seq Settings
logger = logging.getLogger()
logger.addHandler(GelfUdpHandler(host=configs.seq.server_url, port=12201))

# Fetches Helm releases
helm_releases = run(["helm", "list", "--short"], capture_output=True, text=True).stdout.strip().split("\n")

for release in helm_releases:
    try:
        # Checks if the release is from a target team
        release_values = json.loads(run(["helm", "get", "values", release, "-o", "json"], capture_output=True, text=True).stdout)
        if not("team" in release_values and release_values["team"] in allowed_teams):
            continue

        # Checks if there have been requests in the last 2 weeks
        requests_query = prometheus_configs.requests_query.format(release=release)
        requests_result = prometheus.custom_query(requests_query)

        if len(requests_result) != 0 and requests_result[0]["value"][1] == "0":
            # Deletes Helm release
            # run(["helm", "delete", release])
            
            # Logs purge event on Seq
            logger.warning(f"[Helm Idle Cleanup Cronjob] The Helm release {release} was purged due to application inativity (lack of requests in the last 2 weeks).")
    except Exception as ex:
        logger.error(f"[Helm Idle Cleanup Cronjob] An error occurred while processing the release [{release}], error message:  {str(ex)}).")
    finally:
        continue
