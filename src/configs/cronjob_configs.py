class CronjobConfigs:
    def __init__(self, json_config: dict) -> None:
        self.teams = json_config['team_label_targets']
