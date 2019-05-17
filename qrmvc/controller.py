from tkinter import filedialog

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

    def save_file(self, form):

        filename = filedialog.asksaveasfilename(initialdir="/", title="Select location", filetypes=(
            ("json files", "*.json"), ("all files", "*.*")))

        print(f"Saving {form} to {filename}")

        self.model.save_form(filename, form)

    def clear(self):
        self.view.delete_picture()

    def generate(self):
        form = self.view.get_form()
        print(form)

    def test(self):
        self.set_form(*self.model.get_form())

    def set_form(self, form, form_type):
        self.clear()
        self.view.set_form(form, form_type)
