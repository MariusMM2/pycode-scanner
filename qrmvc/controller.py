from tkinter import filedialog

import pyqrcode
from PIL import Image
import qrmvc.model
import qrmvc.view


# noinspection PyArgumentList
class QRGenerator:
    def __init__(self):
        self.model = qrmvc.model.QRGenerator()

        # config related
        self.title = self.model.title
        self.form_types = self.model.form_types
        self.input_forms = self.model.input_forms
        self.default_picture = self.model.default_picture
        self.temp_picture = self.model.temp_picture
        self.picture_size = self.model.picture_size

        self.view = qrmvc.view.QRGeneratorView(self)
        self.select_type(self.form_types[0])
        self.view.window.mainloop()

    def select_type(self, form_type):
        self.clear()
        self.view.set_form({k: '' for k in self.input_forms[form_type]}, form_type)

    def load_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("json files", "*.json"), ("all files", "*.*")))

        self.set_form(*self.model.load_form(filename))

    def save_file(self, form, form_type):

        filename = filedialog.asksaveasfilename(initialdir="/", title="Select location", filetypes=(
            ("json files", "*.json"), ("all files", "*.*")))

        print(f"Saving {form} to {filename}")

        self.model.save_form(filename, {"type": form_type, "form": form})

    def save_code_file(self):
         try:
            filename = filedialog.asksaveasfile(initialdir="/", defaultextension=".png", title="Select location",
            filetypes=[("JPEG", "*.jpg"),("All files", "*")])
            print(filename)
            image = Image.open(self.temp_picture)
            image.save(filename)

         except FileNotFoundError:
            print("attempted to save nonexistent QR Code")
            return
    def clear(self):
        self.view.delete_picture()

    def set_form(self, form, form_type):
        self.clear()
        self.view.set_form(form, form_type)

    def generate(self, form, form_type):
        global content_value
        if form_type not in self.form_types:
            raise AssertionError(f"Invalid form type: {form_type}")

        print(f"form: {form}")

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
            print(f"content: {content_value}")
            url = pyqrcode.create(content_value, error='L')
            url.png(self.temp_picture)
            self.view.set_picture(self.temp_picture)
