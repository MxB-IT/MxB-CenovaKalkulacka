from tkinter import StringVar, IntVar, DoubleVar
from customtkinter import CTkFrame
from Common.PlaceholderTexts import PlaceholderTexts
from Widgets.CTkSpinbox import CTkSpinbox
from Widgets.LabelBase import LabelBase
from Widgets.TextBoxBase import TextBoxBase


class Row(CTkFrame):
    def __init__(self,
                 master,
                 *args,
                 **kwargs):
        super().__init__(master, *args, **kwargs)

        self.description_var = StringVar(value = PlaceholderTexts.DESCRIPTION)
        self.amount_var = IntVar(value=0)
        self.price_var = DoubleVar(value=0.0)

        self.description_var.trace_add("write", self.updateTextBox)
        self.amount_var.trace_add("write", self.updateAmount)
        self.price_var.trace_add("write", self.updatePrice)

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

    def get_subtotal(self) -> float:
        try:
            return self.amount_var.get() * self.price_var.get()
        except Exception:
            return 0.00