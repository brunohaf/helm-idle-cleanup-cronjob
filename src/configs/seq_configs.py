class SeqConfigs:
    def __init__(self, json_config: dict) -> None:
        self.batch_size = json_config['batch_size']
        self.server_url = json_config['server_url']
        self.api_key = json_config['api_key']
