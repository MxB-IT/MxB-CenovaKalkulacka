"""Defines the Row class, used to define all interactive rows in the app."""
from collections.abc import Callable
from tkinter import BooleanVar, DoubleVar, IntVar, StringVar
from typing import Any

from customtkinter import CTkButton, CTkFrame

from src.common.enums.colour_enum import ColourEnum
from src.common.enums.placeholder_texts import PlaceholderTexts
from src.widgets.ctk_spinbox import CTkSpinbox
from src.widgets.textbox_base import TextBoxBase
from src.widgets.tooltip import Tooltip


class Row(CTkFrame):
    """Class used to define every single interactible row with amounts and prices."""

    def __init__(self,  # noqa: PLR0913
                 *args: tuple[Any, ...],
                 master: CTkFrame,
                 on_delete_callback: Callable | None = None,
                 text: PlaceholderTexts | str= PlaceholderTexts.DESCRIPTION,
                 ucto_price: float = 0.0,
                 evidence_price: float = 0.0,
                 dph_price: float = 0.0,
                 no_dph_price: float = 0.0,
                 ucto_bool: BooleanVar | None = None,
                 evidence_bool: BooleanVar | None = None,
                 dph_bool: BooleanVar | None = None,
                 fg_color: ColourEnum = ColourEnum.WHITE,
                 amt_var: IntVar | None = None,
                 **kwargs: Any) -> None:
        """Initialise a Row instance.

        Initialises a Row instance.
        :param args: Any positional args for the master class.
        :param master: Master widget that will contain this row.
        :param text: Description to display on this row (optional, defaults to some default text).
        :param ucto_price: Ucto price (optional, defaults to 0).
        :param evidence_price: Evidence price (optional, defaults to 0).
        :param dph_price: Price for dph payers (optional, defaults to 0).
        :param no_dph_price: Price for dph non payers (optional, defaults to 0).
        :param ucto_bool: BoolVar indicating whether ucto is active (optional, defaults to nothing).
        :param evidence_bool: BoolVar indicating whether evidence is active (optional, defaults to
        constantnly false bool).
        :param dph_bool: BoolVar indicating whether dph is active (optional, defaults to constantnly
        false bool).
        :param fg_color: Fg_color for this row.
        :param amt_var: Amt_var that this row will save its amount into (optional, creates its own
        var by default).
        :param on_delete_callback: Callback for when row is deleted.
        :param kwargs: Any keyword args for the master class.
        """
        super().__init__(*args,
                         master,
                         fg_color = fg_color,
                         **kwargs)

        self.on_delete_callback = on_delete_callback

        self.close_button = CTkButton(
            self,
            text="X",
            width=28,
            height=28,
            corner_radius=14,
            fg_color="#FF6F56",
            hover_color="#FF4040",
            text_color="white",
            font=("Arial", 14, "bold"),
            command=self.delete_row,
        )

        Tooltip(widget=self.close_button,
                text="Odstraní řádek, tato akce je nevratná")

        self.close_button.grid(row=0,
                               column=4,
                               padx=10,
                               pady=10)

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

        self.ucto_bool.trace_add("write",
                                 self.set_price)
        self.evidence_bool.trace_add("write",
                                     self.set_price)
        self.dph_bool.trace_add("write",
                                self.set_price)

        self.amount_var.trace_add("write",
                                  self.get_subtotal)
        self.price_var.trace_add("write",
                                 self.get_subtotal)

        self.grid_columnconfigure((0, 1, 2),
                                  weight=1)

        self.textbox = TextBoxBase(master=self,
                                   height=30,
                                   text=text)
        self.textbox.grid(row=0,
                          column=0,
                          padx=5,
                          pady=5,
                          sticky = "ew")

        Tooltip(widget=self.textbox,
                text="Editujte dvojklikem levého tlačítka myši")

        self.amount_spinbox = CTkSpinbox(
            master=self,
            width=100,
            variable=self.amount_var,
        )
        self.amount_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.price_spinbox = CTkSpinbox(
            master=self,
            width=100,
            variable=self.price_var,
        )
        self.price_spinbox.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    def get_subtotal(self,
                     name: str | None = None,
                     index: str | None = None,
                     value: str | None = None) -> None:
        """Get subtotal from this Row.

        Method used for recalculating the total for this row by multiplying amt with its price.
        :param name: Arg shoehorned in, so Ruff doesn't scream at me.
        :param index: Arg shoehorned in, so Ruff doesn't scream at me.
        :param value: Arg shoehorned in, so Ruff doesn't scream at me.
        :return: None, sets an internal variable
        """
        try:
            self.subtotal_var.set(round(self.amount_var.get() * self.price_var.get(), 0))
        except Exception:
            self.subtotal_var.set(0.0)

    def set_price(self,
                  name: str | None = None,
                  index: str | None = None,
                  value: str | None = None) -> None:
        """Set price for this Row.

        Method used to set the price of a row's item.
        :param name: Arg shoehorned in, so Ruff doesn't scream at me.
        :param index: Arg shoehorned in, so Ruff doesn't scream at me.
        :param value: Arg shoehorned in, so Ruff doesn't scream at me.
        :return: None
        """
        if self.ucto_bool.get() and self.ucto_price != 0.0:
            self.price_var.set(self.ucto_price)
        elif self.evidence_bool.get() and self.evidence_price != 0.0:
            self.price_var.set(self.evidence_price)
        elif self.dph_bool.get() and self.dph_price != 0.0:
            self.price_var.set(self.dph_price)
        elif self.no_dph_price != 0.0:
            self.price_var.set(self.no_dph_price)

    def delete_row(self) -> None:
        """Delete a rpw upon user's request during runtime.

        Method used to safely delete a row, calling a callback function in its parent to ensure safe
        deletion before self.destroying.
        :return: None
        """
        if self.on_delete_callback:
            self.on_delete_callback(self)

        self.destroy()
