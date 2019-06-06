from tkinter import filedialog

import pyqrcode
from PIL import Image
import qrmvc.QRModel
import qrmvc.QRView


# noinspection PyArgumentList
class QRController:
    def __init__(self):
        self.model = qrmvc.QRModel.QRModel()

        # config stuff
        self.title = self.model.title
        self.form_types = self.model.form_types
        self.input_forms = self.model.input_forms
        self.default_picture = self.model.default_picture
        self.temp_picture = self.model.temp_picture
        self.picture_size = self.model.picture_size

        # create the view
        self.view = qrmvc.QRView.QRView(self)
        # set default code type to URL
        self.select_type(self.form_types[0])
        # start the main tkinter loop
        self.view.window.mainloop()

    def select_type(self, form_type):
        """ Selects the type of the form shown in the UI.

        :param form_type: The type of the form
        """

        self.clear()
        self.view.set_form({k: '' for k in self.input_forms[form_type]['fields']}, form_type)

    def load_file(self):
        """ Shows the dialog for selecting a form file and loads the file. """

        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("JSON files", "*.json"), ("All files", "*.*")))

        self.set_form(*self.model.load_form(filename))

    def save_file(self, form, form_type):
        """ Saves the current form to a file.

        :param form: The dictionary of the form.
        :param form_type: The type of the form.
        """

        filename = filedialog.asksaveasfilename(initialdir="/", defaultextension=".json", title="Select location",
                                                filetypes=(
                                                    ("JSON files", "*.json"), ("All files", "*.*")))

        print(f"Saving {form} to {filename}")

        self.model.save_form(filename, {"type": form_type, "form": form})

    def save_code_file(self):
        """ Saves the current QR Code to a .jpg file. """

        try:
            filename = filedialog.asksaveasfile(initialdir="/", defaultextension=".jpg", title="Select location",
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
        code_format = self.input_forms[form_type]["code_format"]
        content_value = code_format.format(*form.values())

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
