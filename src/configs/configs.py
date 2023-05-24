from .seq_configs import SeqConfigs
from .prometheus_configs import PrometheusConfigs
from .cronjob_configs import CronjobConfigs
from json import load

class Configs():
    def __init__(self):
        with open('./src/configs/configs.json', 'r') as configs:
            configs = load(configs)
            self.prometheus = PrometheusConfigs(configs['prometheus'])
            self.cronjob = CronjobConfigs(configs['cronjob'])
            self.seq = SeqConfigs(configs['seq'])