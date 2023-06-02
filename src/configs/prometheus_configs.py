class PrometheusConfigs:
    def __init__(self, json_config: dict) -> None:
        self.server_url = json_config['prometheus_server_url']
        self.query = QueryConfigs(json_config['query'])

class QueryConfigs:
    def __init__(self, json_config: dict) -> None:
        self.time_range = json_config['time_range']
        self.component = json_config['component']
        self.template = json_config['template']
        self.metric = json_config['metric']
