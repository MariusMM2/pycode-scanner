from tkinter import filedialog
import pyqrcode

import qrmvc.model
import qrmvc.view


# noinspection PyArgumentList
class QRGenerator:
    def __init__(self):
        self.model = qrmvc.model.QRGenerator()
        self.title = self.model.title
        self.form_types = self.model.form_types
        self.input_forms = self.model.input_forms

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

    def clear(self):
        self.view.delete_picture()

    def test(self):
        self.set_form(*self.model.get_form())

    def set_form(self, form, form_type):
        self.clear()
        self.view.set_form(form, form_type)

    def generate(self, form, form_type):
        if form_type not in self.form_types:
            raise AssertionError(f"Invalid form type: {form_type}")

        if form_type == self.form_types[0] or form_type == self.form_types[2]:  # URL or Text
            print(f"form: {form}")
            content_key = self.input_forms[form_type][0]
            content_value = form[content_key]
            print(content_value)
            url = pyqrcode.create(content_value, error='L')
            filename = 'code.png'
            url.png(filename, scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff])
            self.view.set_picture(filename)
            print(str(url))