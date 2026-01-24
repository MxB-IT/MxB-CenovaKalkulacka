from tkinter import StringVar, IntVar, DoubleVar, BooleanVar
from customtkinter import CTkFrame
from Common.PlaceholderTexts import PlaceholderTexts
from Widgets.CTkSpinbox import CTkSpinbox
from Widgets.TextBoxBase import TextBoxBase
from Widgets.Tooltip import Tooltip


class Row(CTkFrame):
    """
    class used to define every single interactible row with amounts and prices
    """
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
                 amt_var = None,
                 is_ghost = False,
                 *args,
                 **kwargs):
        """
        initialization method for Rows
        :param master: master widget that will contain this row
        :param text: description to display on this row (optional, defaults to some default text)
        :param ucto_price: ucto price (optional, defaults to 0)
        :param evidence_price: evidence price (optional, defaults to 0)
        :param dph_price: price for dph payers (optional, defaults to 0)
        :param no_dph_price: price for dph non payers (optional, defaults to 0)
        :param ucto_bool: BoolVar indicating whether ucto is active (optional, defaults to nothing)
        :param evidence_bool: BoolVar indicating whether evidence is active (optional, defaults to constantnly false bool)
        :param dph_bool: BoolVar indicating whether dph is active (optional, defaults to constantnly false bool)
        :param fg_color: fg_color for this row
        :param amt_var: amt_var that this row will save its amount into (optional, creates its own var by default)
        :param args: any other args
        :param kwargs: any other kwargs
        """
        super().__init__(master, fg_color = fg_color, *args, **kwargs)

        self.is_ghost = is_ghost

        Tooltip(widget=self.close_button,
                text="Odstraní řádek, tato akce je nevratná")


        self.description_var = StringVar(value=text)
        self.amount_var = amt_var if amt_var is not None else IntVar(value=0)
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

        self.ucto_bool.trace_add("write", self.set_price)
        self.evidence_bool.trace_add("write", self.set_price)
        self.dph_bool.trace_add("write", self.set_price)

        self.amount_var.trace_add("write", self.get_subtotal)
        self.price_var.trace_add("write", self.get_subtotal)

        self.grid_columnconfigure((0, 1, 2), weight = 1)

        self.textbox = TextBoxBase(master = self, height = 30, text = text)
        self.textbox.grid(row=0, column=0, padx=5, pady=5, sticky = "ew")

        Tooltip(widget=self.textbox,
                text="Editujte dvojklikem levého tlačítka myši")

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
        """
        method used for recalculating the total for this row by multiplying amt with its price
        :param args: any args passed
        :param kwargs: any kwargs passed
        :return: None, sets an internal variable
        """
        try:
            self.subtotal_var.set(round(self.amount_var.get() * self.price_var.get(), 0))
        except Exception:
            self.subtotal_var.set(0.0)

    def set_price(self, *args) -> None:
        if self.ucto_bool.get() and self.ucto_price != 0.0:
            self.price_var.set(self.ucto_price)
        elif self.evidence_bool.get() and self.evidence_price != 0.0:
            self.price_var.set(self.evidence_price)
        elif self.dph_bool.get() and self.dph_price != 0.0:
            self.price_var.set(self.dph_price)
        elif self.no_dph_price != 0.0:
            self.price_var.set(self.no_dph_price)