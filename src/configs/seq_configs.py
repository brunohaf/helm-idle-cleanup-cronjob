class SeqConfigs:
    def __init__(self, json_config: dict) -> None:
        self.templates = LogTemplates(json_config['log_templates'])
        self.server_url = json_config['server_url']
        self.api_key = json_config['api_key']
        self.port = json_config['port']

class LogTemplates:
    def __init__(self, json_config: dict) -> None:
        self.purging_message = json_config['purging_message']
        self.error_message = json_config['error_message']
