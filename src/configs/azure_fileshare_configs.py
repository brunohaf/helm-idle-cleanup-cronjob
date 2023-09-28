class AzureFileShareConfigs:
    def __init__(self, json_config: dict) -> None:
        self.conn_str = json_config['connection_string']
        self.share_name = json_config['share_name']
        self.filename_template = json_config['filename_template']
        self.filename_date_format = json_config['filename_date_format']
        self.nodes_snapshot_filename_template = json_config['nodes_snapshot_filename_template']
