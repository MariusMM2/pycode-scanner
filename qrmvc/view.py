import tkinter as tk

from PIL import Image, ImageTk

from qrmvc.TextWithVar import TextWithVar
from qrmvc.VerticalScrolledFrame import VerticalScrolledFrame

PICTURE_SIZE = 300


class QRGeneratorView:
    def __init__(self, controller):
        self.controller = controller

        self.window = tk.Tk()
        self.window.title(self.controller.title)

        self.type_ctrl = tk.StringVar(self.window)
        self.type_ctrl.set(self.controller.form_types[0])

        self.select_type_menu = tk.OptionMenu(self.window, self.type_ctrl, *self.controller.form_types,
                                              command=self.controller.select_type)
        self.select_type_menu.grid(column=0, row=0, sticky='nesw')

        self.scroll_frame = VerticalScrolledFrame(self.window)
        self.scroll_frame.grid(column=0, columnspan=2, row=1, sticky='nesw')

        self.load_button = tk.Button(self.window, text="Load from file", command=self.controller.load_file)
        self.load_button.grid(column=0, row=2, sticky='nesw')

        self.save_button = tk.Button(self.window, text="Save to file",
                                     command=lambda: self.controller.save_file(self.get_form(), self.type_ctrl.get()))
        self.save_button.grid(column=1, row=2, sticky='nesw')

        self.clear_button = tk.Button(self.window, text="Clear",
                                      command=lambda: self.controller.select_type(self.type_ctrl.get()))
        self.clear_button.grid(column=2, row=2, sticky='nesw')

        self.generate_button = tk.Button(self.window, text="Generate",
                                         command=lambda: self.controller.generate(self.get_form(),
                                                                                  self.type_ctrl.get()))
        self.generate_button.grid(column=3, row=2, sticky='nesw')

        self.set_picture('sample.png')

        self.form_dict = {}

    def set_form(self, form, form_type):
        self.type_ctrl.set(form_type)

        previous_forms = self.scroll_frame.interior.pack_slaves()
        for l in previous_forms:
            l.destroy()

        form_fields = form.keys()

        self.form_dict = {str(field): QRGeneratorView.new_string_var(form[field]) for field in form_fields}
        print(self.form_dict)

        for field_name in form_fields:
            is_big = '#big' in field_name
            field_name_display = field_name[:field_name.find('#big')] if is_big else field_name

            print(field_name_display)

            field_label = tk.Label(self.scroll_frame.interior, anchor='w', text=field_name_display)
            field_label.pack()

            if is_big:
                field = TextWithVar(self.scroll_frame.interior, textvariable=self.form_dict[field_name],
                                    borderwidth=1, relief="sunken", height=10, width=23, )
                pass
            else:
                field = tk.Entry(self.scroll_frame.interior, textvariable=self.form_dict[field_name])
            field.config(highlightbackground='black', highlightthickness=1)
            field.pack()

    def get_form(self):

        return {k: v.get() for k, v in self.form_dict.items()}

    def set_picture(self, file_name):
        load = Image.open(file_name)
        load = load.resize((PICTURE_SIZE, PICTURE_SIZE), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        if hasattr(self, 'image_label'):
            self.image_label.grid_forget()

        # noinspection PyAttributeOutsideInit
        self.image_label = tk.Label(self.window, image=render)
        self.image_label.image = render
        self.image_label.grid(column=2, columnspan=2, row=0, rowspan=2)

    def delete_picture(self):
        self.set_picture('blank.png')

    @staticmethod
    def new_string_var(value):
        asd = tk.StringVar()
        asd.set(value)
        return asd
