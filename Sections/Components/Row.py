from tkinter import StringVar, IntVar, DoubleVar
from customtkinter import CTkFrame
from Common.PlaceholderTexts import PlaceholderTexts
from Widgets.CTkSpinbox import CTkSpinbox
from Widgets.TextBoxBase import TextBoxBase


class Row(CTkFrame):
    def __init__(self,
                 master,
                 text = PlaceholderTexts.DESCRIPTION,
                 price = 0.0,
                 *args,
                 **kwargs):
        super().__init__(master, *args, **kwargs)

        self.description_var = StringVar(value=text)
        self.amount_var = IntVar(value=0)
        self.price_var = DoubleVar(value=price)
        self.subtotal_var = DoubleVar(value=0.0)

        self.amount_var.trace_add("write", self.get_subtotal)
        self.price_var.trace_add("write", self.get_subtotal)

        self.grid_columnconfigure((0, 1, 2), weight = 1)

        self.textbox = TextBoxBase(master = self, height = 30)
        self.textbox.grid(row=0, column=0, padx=5, pady=5, sticky = "ew")

        self.amount_spinbox = CTkSpinbox(
            master=self,
            width=100,
            variable=self.amount_var
        )
        self.amount_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.price_spinbox = CTkSpinbox(
            master=self,
            width=100,
            variable=self.price_var
        )
        self.price_spinbox.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    def get_subtotal(self, *args, **kwargs) -> None:
        try:
            self.subtotal_var.set(round(self.amount_var.get() * self.price_var.get(), 0))
        except Exception:
            self.subtotal_var.set(0.00)