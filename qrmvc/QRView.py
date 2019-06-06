import tkinter as tk

from PIL import Image, ImageTk

from qrmvc.TextWithVar import TextWithVar
from qrmvc.VerticalScrolledFrame import VerticalScrolledFrame


class QRView:
    def __init__(self, controller):
        self.controller = controller

        # main window
        self.window = tk.Tk()
        self.window.title(self.controller.title)

        # variable storing the current form type
        self.type_ctrl = tk.StringVar(self.window)
        # sets the default form type (URL)
        self.type_ctrl.set(self.controller.form_types[0])

        # options menu dropdown for selecting the form type
        self.select_type_menu = tk.OptionMenu(self.window, self.type_ctrl, *self.controller.form_types,
                                              command=self.controller.select_type)
        self.select_type_menu.grid(column=0, row=0, sticky='nesw')

        # scroll frame containing the form fields
        self.scroll_frame = VerticalScrolledFrame(self.window)
        self.scroll_frame.grid(column=0, columnspan=2, row=1, sticky='nesw')

        # button to load a form from a file
        self.load_button = tk.Button(self.window, text="Load from file", command=self.controller.load_file)
        self.load_button.grid(column=0, row=2, sticky='nesw')

        # button to save a form to a file
        self.save_button = tk.Button(self.window, text="Save to file",
                                     command=lambda: self.controller.save_file(self.get_form(), self.type_ctrl.get()))
        self.save_button.grid(column=1, row=2, sticky='nesw')

        # button to clear the current form
        self.clear_button = tk.Button(self.window, text="Clear",
                                      command=lambda: self.controller.select_type(self.type_ctrl.get()))
        self.clear_button.grid(column=2, row=2, sticky='nesw')

        # button to save the generated QR Code to a file
        # the button is disabled at start and until a code is generated
        self.save_code_button = tk.Button(self.window, text="Save code to file", state=tk.DISABLED,
                                          command=self.controller.save_code_file)
        self.save_code_button.grid(column=3, row=2, sticky='nesw')

        # button to generate the qr code
        self.generate_button = tk.Button(self.window, text="Generate",
                                         command=lambda: self.controller.generate(self.get_form(),
                                                                                  self.type_ctrl.get()))
        self.generate_button.grid(column=4, row=2, sticky='nesw')

        # the dictionary holding the current form
        self.form_dict = {}

    def set_form(self, form, form_type):
        """ Sets the current form of the UI

        :param form: The contents of the form
        :param form_type: The type of the form
        """

        # set the type of the form in the dropdown
        self.type_ctrl.set(form_type)

        # delete the contents of the previous form
        previous_form_fields = self.scroll_frame.interior.pack_slaves()
        for field in previous_form_fields:
            field.destroy()

        # store the titles of the fields
        form_fields = form.keys()

        # generate a dictionary containing StringVars for each field, with each StringVar holding a field value
        # from the parameter
        self.form_dict = {str(field): QRView.new_string_var(form[field]) for field in form_fields}
        print({k: v.get() for k, v in self.form_dict.items()})

        # generate the UI widgets for the fields
        for field_name in form_fields:
            # check if the name contains the '#big'
            is_big = '#big' in field_name

            # if applicable, remove the '#big' tag from the title of the field when displaying
            field_name_display = field_name[:field_name.find('#big')] if is_big else field_name

            print(field_name_display)

            # put the title of the field in a label
            field_label = tk.Label(self.scroll_frame.interior, anchor='w', text=field_name_display)
            field_label.pack()

            if is_big:
                # create a custom TextWithVar widget
                field = TextWithVar(self.scroll_frame.interior, textvariable=self.form_dict[field_name],
                                    borderwidth=1, relief="sunken", height=10, width=23, )
            else:
                # create a normal Entry widget
                field = tk.Entry(self.scroll_frame.interior, textvariable=self.form_dict[field_name])

            field.config(highlightbackground='black', highlightthickness=1)
            field.pack()

    def get_form(self):
        """ Returns the form as a str: str dictionary.
        :return: a str:str dictionary of the form.
        """

        return {k: v.get() for k, v in self.form_dict.items()}

    def set_picture(self, file_name):
        """ Loads a picture file and displays it.
        :param file_name: The location of the file to load.
        """

        # load the image file
        load = Image.open(file_name)
        # resize to fit the window
        load = load.resize((self.controller.picture_size, self.controller.picture_size), Image.ANTIALIAS)
        # load the image in a widget
        render = ImageTk.PhotoImage(load)

        # remove the old image, if applicable
        if hasattr(self, 'image_label'):
            self.image_label.grid_forget()

        # noinspection PyAttributeOutsideInit
        # create a new widget for the picture
        self.image_label = tk.Label(self.window, image=render)
        self.image_label.image = render
        self.image_label.grid(column=2, columnspan=3, row=0, rowspan=2)
        # enable the save code button
        self.save_code_button.config(state='normal')

    def delete_picture(self):
        """ Deletes the current picture. """

        # set the current picture to a fully white picture
        self.set_picture(self.controller.default_picture)
        # disable the save code button
        self.save_code_button.config(state='disabled')

    @staticmethod
    def new_string_var(value):
        """ Creates and returns a StringVar with the given value.
        :param value: The value to store.
        :return: a StringVar with the value
        """
        string_var = tk.StringVar()
        string_var.set(value)
        return string_var
