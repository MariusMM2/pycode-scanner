from tkinter import filedialog

import pyqrcode
from PIL import Image
import qrmvc.model
import qrmvc.view


# noinspection PyArgumentList
class QRGenerator:
    def __init__(self):
        self.model = qrmvc.model.QRGenerator()

        # config stuff
        self.title = self.model.title
        self.form_types = self.model.form_types
        self.input_forms = self.model.input_forms
        self.default_picture = self.model.default_picture
        self.temp_picture = self.model.temp_picture
        self.picture_size = self.model.picture_size

        # create the view
        self.view = qrmvc.view.QRGeneratorView(self)
        # set default code type to URL
        self.select_type(self.form_types[0])
        # start the main tkinter loop
        self.view.window.mainloop()

    def select_type(self, form_type):
        """ Selects the type of the form shown in the UI.

        :param form_type: The type of the form
        """

        self.clear()
        self.view.set_form({k: '' for k in self.input_forms[form_type]}, form_type)

    def load_file(self):
        """ Shows the dialog for selecting a form file and loads the file. """

        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("json files", "*.json"), ("all files", "*.*")))

        self.set_form(*self.model.load_form(filename))

    def save_file(self, form, form_type):
        """ Saves the current form to a file.

        :param form: The dictionary of the form.
        :param form_type: The type of the form.
        """

        filename = filedialog.asksaveasfilename(initialdir="/", defaultextension=".json", title="Select location",
                                                filetypes=(
                                                    ("json files", "*.json"), ("all files", "*.*")))

        print(f"Saving {form} to {filename}")

        self.model.save_form(filename, {"type": form_type, "form": form})

    def save_code_file(self):
        """ Saves the current QR Code to a .jpg file. """

        try:
            filename = filedialog.asksaveasfile(initialdir="/", defaultextension=".png", title="Select location",
                                                filetypes=[("JPEG", "*.jpg"), ("All files", "*")])
            print(filename)
            image = Image.open(self.temp_picture)
            image.save(filename)

        except FileNotFoundError:
            print("attempted to save nonexistent QR Code")

    def clear(self):
        """ Removes the current shown QR Code."""

        self.view.delete_picture()

    def set_form(self, form, form_type):
        """ Clears the current QR Code and loads the passed form.

        :param form: The form to be shown.
        :param form_type: The type of the form to be shown.
        """

        self.clear()
        self.view.set_form(form, form_type)

    def generate(self, form, form_type):
        """ Generates a QR Code from the given form and shows it.

        :param form: The form used to populate the QR Code.
        :param form_type: The type of the form used to structure the QR Code.
        """

        print(f"form: {form}")

        # the contents of the QR Code
        global content_value

        if form_type == self.form_types[0] or form_type == self.form_types[2]:  # URL or Text
            content_key = self.input_forms[form_type][0]
            content_value = form[content_key]
            print(f"URL: {content_value}")

        elif form_type == self.form_types[1]:  # SMS
            content_keys = self.input_forms[form_type]
            content_number = form[content_keys[0]]
            content_message = form[content_keys[1]]
            print(f"number: {content_number}, message: {content_message}")

            content_value = f"SMSTO: {content_number}: {content_message}"

        elif form_type == self.form_types[3]:  # Email
            content_keys = self.input_forms[form_type]
            content_recipient = form[content_keys[0]]
            content_subject = form[content_keys[1]]
            content_body = form[content_keys[2]]
            print(f"recipient: {content_recipient}, subject: {content_subject}, body: {content_body}")

            content_value = f"MATMSG:TO:{content_recipient};SUB:{content_subject};BODY:{content_body};;"

        if content_value is not None:
            print(f"contents: {content_value}")
            # generate the QR Code
            url = pyqrcode.create(content_value, error='L')
            # save the code to a temporary file
            url.png(self.temp_picture)
            # present the generated code
            self.view.set_picture(self.temp_picture)

        if form_type not in self.form_types:
            raise AssertionError(f"Unknown form type: {form_type}")

    def stop(self):
        """ Callback called when the program closes. """

        self.model.delete_temp()
