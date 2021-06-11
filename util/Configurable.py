import json

class Configurable():
    def __init__(self):
        self._file = self._get_config_file()
    
    def _get_config_file(self):
        CFG_FILENAME = './config.json'
        with open(CFG_FILENAME) as cfg:
            CFG = json.load(cfg)
        return CFG
    