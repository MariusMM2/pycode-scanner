import json


class QRGenerator:
    def __init__(self):
        with open('.config.json') as config_file:
            config = json.load(config_file)
            self.title = config['title']
            self.form_types = config['form_types']
            self.input_forms = config['input_forms']
        with open('sample.json') as sample_form_file:
            self.sample_form = json.load(sample_form_file)

    def get_form(self):
        return self.sample_form["form"], self.sample_form["type"]

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
