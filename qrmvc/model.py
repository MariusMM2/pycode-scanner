import json


class QRGenerator:
    def __init__(self):
        with open('.config.json') as config_file:
            config = json.load(config_file)
            self.title = config['title']
            self.code_types = config['code_types']
