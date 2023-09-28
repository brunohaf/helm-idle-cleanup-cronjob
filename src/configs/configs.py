from .seq_configs import SeqConfigs
from .prometheus_configs import PrometheusConfigs
from .cronjob_configs import CronjobConfigs
from .azure_fileshare_configs import AzureFileShareConfigs
from json import load

class Configs():
    def __init__(self):
        with open('./src/configs/configs.json', 'r') as configs:
            configs = load(configs)
            self.azure_fileshare = AzureFileShareConfigs(configs['azure_fileshare'])
            self.prometheus = PrometheusConfigs(configs['prometheus'])
            self.cronjob = CronjobConfigs(configs['cronjob'])
            self.seq = SeqConfigs(configs['seq'])
