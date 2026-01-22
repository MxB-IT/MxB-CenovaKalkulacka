from tkinter import StringVar, IntVar, DoubleVar, BooleanVar
from customtkinter import CTkFrame
from Common.PlaceholderTexts import PlaceholderTexts
from Widgets.CTkSpinbox import CTkSpinbox
from Widgets.TextBoxBase import TextBoxBase


class Row(CTkFrame):
    def __init__(self,
                 master,
                 text = PlaceholderTexts.DESCRIPTION,
                 ucto_price = 0.0,
                 evidence_price = 0.0,
                 dph_price = 0.0,
                 no_dph_price = 0.0,
                 ucto_bool = None,
                 evidence_bool = None,
                 dph_bool = None,
                 fg_color = "white",
                 *args,
                 **kwargs):
        super().__init__(master, fg_color = fg_color, *args, **kwargs)

        self.description_var = StringVar(value=text)
        self.amount_var = IntVar(value=0)
        self.price_var = DoubleVar(value=0.0)
        self.subtotal_var = DoubleVar(value=0.0)

        self.dph_price = dph_price
        self.no_dph_price = no_dph_price
        self.evidence_price = evidence_price
        self.ucto_price = ucto_price

        self.ucto_bool = ucto_bool if ucto_bool is not None else BooleanVar(value=False)
        self.evidence_bool = evidence_bool if evidence_bool is not None else BooleanVar(value=False)
        self.dph_bool = dph_bool if dph_bool is not None else BooleanVar(value=False)

        if self.ucto_bool.get():
            self.price_var.set(ucto_price)
        elif self.evidence_bool.get():
            self.price_var.set(evidence_price)
        elif self.dph_bool.get():
            self.price_var.set(dph_price)
        else:
            self.price_var.set(no_dph_price)

        ucto_bool.trace_add("write", self.set_price)
        evidence_bool.trace_add("write", self.set_price)
        dph_bool.trace_add("write", self.set_price)

        self.amount_var.trace_add("write", self.get_subtotal)
        self.price_var.trace_add("write", self.get_subtotal)

        self.grid_columnconfigure((0, 1, 2), weight = 1)

        self.textbox = TextBoxBase(master = self, height = 30, text = text)
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

    def set_price(self, *args) -> None:
        if self.ucto_bool.get():
            self.price_var.set(self.ucto_price)
        elif self.evidence_bool.get():
            self.price_var.set(self.evidence_price)
        elif self.dph_bool.get():
            self.price_var.set(self.dph_price)
        else:
            self.price_var.set(self.no_dph_price)