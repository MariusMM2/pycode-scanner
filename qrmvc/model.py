import json
import os


class QRGenerator:
    def __init__(self):
        with open('.config.json') as config_file:
            # load the json config file to variables
            config = json.load(config_file)
            self.title = config['title']
            self.input_forms = config['input_forms']
            self.form_types = list(self.input_forms.keys())
            self.default_picture = config['default_picture']
            self.temp_picture = config['temp_picture']
            self.picture_size = config['picture_size']

    @staticmethod
    def load_form(filename):
        """ Loads a json based form into a dict.

        :param filename: The string of the file location.
        :return:
            form: Dictionary containing the fields of the file.
            form_type: The type of the form.
        """

        with open(filename) as form_file:
            form_loaded = json.load(form_file)
            form = form_loaded["form"]
            form_type = form_loaded["type"]

        return form, form_type

    @staticmethod
    def save_form(filename, form):
        """ Saves the current form input as json

        :param filename: The string of the file location.
        :param form: The dictionary containing the input form.
        """

        with open(filename, "w+") as form_file:
            json.dump(form, form_file)

    def delete_temp(self):
        """ Delete the temporary picture files used for displaying. Called when the program closes """

        try:
            print("removing temp picture")
            os.remove(self.temp_picture)
        except FileNotFoundError:
            print("temp picture not found")
            pass
