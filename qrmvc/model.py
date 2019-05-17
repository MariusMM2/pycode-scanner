import json


class QRGenerator:
    def __init__(self):
        with open('.config.json') as config_file:
            config = json.load(config_file)
            self.title = config['title']
            self.input_forms = config['input_forms']
            self.form_types = list(self.input_forms)
            self.default_picture = config['default_picture']
            self.temp_picture = config['temp_picture']
            self.picture_size = config['picture_size']

    @staticmethod
    def load_form(filename):
        with open(filename) as form_file:
            form_loaded = json.load(form_file)
            form = form_loaded["form"]
            form_type = form_loaded["type"]

        return form, form_type

    @staticmethod
    def save_form(filename, form):
        with open(filename, "w+") as form_file:
            json.dump(form, form_file)
