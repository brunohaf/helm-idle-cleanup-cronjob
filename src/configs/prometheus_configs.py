class PrometheusConfigs:
    def __init__(self, json_config: dict) -> None:
        self.server_url = json_config['prometheus_server_url']
        self.requests_query = json_config['requests_query']
