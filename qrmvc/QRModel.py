import json
import os


class QRModel:
    def __init__(self):
        with open('.config.json') as config_file:
            # load the json config file to variables
            config = json.load(config_file)
            self.title = config['title']
            #
            self.code_folder = config['code_folder']

            self.input_forms = self.load_codes()
            self.form_types = [code_title for code_title in self.input_forms.keys()]

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

    def get_code_files(self):
        return [code_name for code_name in
                list(filter(lambda file: ".json" in file, os.listdir(self.code_folder)))]

    def load_codes(self):
        codes = {}
        for code_file_handle in self.get_code_files():
            with open(os.path.join(self.code_folder, code_file_handle)) as code_file:
                code_json = json.load(code_file)
                code_name = code_json['title']
                codes[code_name] = code_json

        return codes
