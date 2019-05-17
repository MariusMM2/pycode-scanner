import qrmvc.model
import qrmvc.view


class QRGenerator:
    def __init__(self):
        self.model = qrmvc.model.QRGenerator()
        self.title = self.model.title
        self.code_types = self.model.code_types
        self.view = qrmvc.view.QRGeneratorView(self)
        self.view.window.mainloop()

    def select_type(self, form_type):
        pass

    def load_file(self):
        pass

    def save_file(self):
        pass

    def clear_input(self):
        pass

    def generate_code(self):
        pass
