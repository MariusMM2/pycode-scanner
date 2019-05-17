import tkinter as tk

from qrmvc.VerticalScrolledFrame import VerticalScrolledFrame


class QRGeneratorView:
    def __init__(self, controller):
        self.controller = controller

        self.window = tk.Tk()
        self.window.title(self.controller.title)

        self.type_ctrl = tk.StringVar(self.window)
        self.type_ctrl.set(self.controller.code_types[0])

        self.select_type_menu = tk.OptionMenu(self.window, self.type_ctrl, *self.controller.code_types, command=print)
        self.select_type_menu.grid(column=0, row=0, sticky='nesw')

        self.scroll_frame = VerticalScrolledFrame(self.window)
        self.scroll_frame.grid(column=0, columnspan=2, row=1, sticky='nesw')

        for i in range(0, 20):
            field_label = tk.Label(self.scroll_frame.interior, anchor='w', text='Field ' + str(i))
            field_label.pack()
            field = tk.Entry(self.scroll_frame.interior)
            field.insert(tk.END, 'Field ' + str(i))
            field.config(highlightbackground='black', highlightthickness=1)
            field.pack()
            blank_label = tk.Label(self.scroll_frame.interior)
            blank_label.pack()

        self.load_button = tk.Button(self.window, text="Load from file", command=lambda: print("Load from file"))
        self.load_button.grid(column=0, row=2, sticky='nesw')

        self.save_button = tk.Button(self.window, text="Save to file", command=lambda: print("Save to file"))
        self.save_button.grid(column=1, row=2, sticky='nesw')

        self.clear_button = tk.Button(self.window, text="Clear", command=lambda: print("Clear"))
        self.clear_button.grid(column=2, row=2, sticky='nesw')

        self.generate_button = tk.Button(self.window, text="Generate", command=lambda: print("Generate"))
        self.generate_button.grid(column=3, row=2, sticky='nesw')

        self.code_canvas = tk.Canvas(self.window, bg="red")
        self.code_canvas.grid(column=2, columnspan=2, row=0, rowspan=2, sticky='nesw')
