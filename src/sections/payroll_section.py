"""Defines a class for the payroll section of the app."""
from __future__ import annotations

from tkinter import DoubleVar
from typing import TYPE_CHECKING, Any

from customtkinter import CTkFrame

from src.common.enums.colour_enum import ColourEnum
from src.common.enums.default_price_enum import DefaultPriceEnum
from src.sections.components.row import Row
from src.sections.section_base import SectionBase
from src.widgets.button_base import ButtonBase
from src.widgets.label_base import LabelBase

if TYPE_CHECKING:
    from src.price_calc import PriceCalc

class PayrollSection(SectionBase):
    """Defines a section for widgets pertaining to the payroll prices."""

    def __init__(self,
                 master,
                 app: PriceCalc) -> None:
        """Initialise the PayrollSection class.

        Initialises the PayrollSection class, setting up widgets and variables.
        :param master: Mater widgets for the PayrollSection.
        :param app: PriceCalc app instance.
        """
        self.frame = CTkFrame(master = master,
                              fg_color = ColourEnum.WHITE,
                              border_color = ColourEnum.MXB_RED,
                              border_width = 2)
        self.widgets: list[tuple[Any, ...] | Row] = []
        self.total = DoubleVar()
        self.total.trace_add("write", app.calculate_total)
        self.subtotals: list[DoubleVar] = []

        self.headers = (LabelBase(master=self.frame,
                                  text="Položka"),
                        LabelBase(master=self.frame,
                                  text="Počet"),
                        LabelBase(master=self.frame,
                                  text="Cena"))

        self.setup_widgets()

        self.define_row(text="Počet přihlášek/odhlášek",
                        price=DefaultPriceEnum.SIGNUPS_SIGNOFFS)

        self.define_row(text="Mzdy",
                        price=DefaultPriceEnum.PAYROLL_PRICE)

        self.define_row(text="Exekuce",
                        price=DefaultPriceEnum.EXECUTIONS)

        self.arrange_widgets(self.frame, self.widgets)

        self.add_row_button = ButtonBase(master=self.frame,
                                         text="+",
                                         command=self.add_row)

        self.add_row_button.grid(row=self.frame.grid_size()[1] + 1,
                                 column=0,
                                 columnspan=self.frame.grid_size()[0],
                                 sticky="ew",
                                 padx=10,
                                 pady=10)

    def setup_widgets(self) -> None:
        """Sst up widgets used in the payroll section.

        Sets up all widgets into default locations with default values.
        :return: None
        """
        self.widgets.append(self.headers)

    def get_total(self,
                  name: str | None = None,
                  index: str | None = None,
                  value: str | None = None) -> None:
        """Get all totals in this section and add them up into a grand total.

        Gets the total of all the widgets within the section.
        :return: float representing the total
        """
        total = 0.0
        try:
            for subtotal in self.subtotals:
                total += subtotal.get()

            total *= 7/6

        except ValueError:
            total = 0.0

        except TypeError:
            total = 0.0

        self.total.set(total)

    def define_row(self,
                   text : str,
                   price: DefaultPriceEnum | float) -> None:
        """Define a new row during setup, before the program is ran.

        Method used to define each row with an interactible price and amount of items to be
        calculated.
        :param text: Text to be displayed in the textbox, describing what this row represents.
        :param price: Default price to be displayed next to the widget before being edited in any
        way by the user.
        :return: None
        """
        row = Row(master=self.frame,
                  text=text,
                  evidence_price=price,
                  ucto_price=price,
                  dph_price=price,
                  no_dph_price=price,
                  on_delete_callback=self.row_delete_callback)

        row.subtotal_var.trace_add("write", self.get_total)
        self.widgets.append(row)
        self.subtotals.append(row.subtotal_var)

    def add_row(self) -> None:
        """Add a new row at the user's request during runtime.

        Method used for creating new rows during runtime when the user wants to add them.
        :return: None
        """
        self.add_row_button.grid_forget()

        row = Row(master=self.frame,
                  on_delete_callback=self.row_delete_callback)

        row.subtotal_var.trace_add("write", self.get_total)
        self.widgets.append(row)
        self.subtotals.append(row.subtotal_var)

        row.grid(row=self.frame.grid_size()[1] + 1,
                 column=0,
                 columnspan=self.frame.grid_size()[0],
                 sticky="ew",
                 padx=10,
                 pady=10)

        self.add_row_button.grid(row=self.frame.grid_size()[1] + 1,
                                 column=0,
                                 columnspan=self.frame.grid_size()[0],
                                 sticky="ew",
                                 padx=10,
                                 pady=10)

    def row_delete_callback(self, deleted_row: Row) -> None:
        """Delete a row upon user's request during runtime.

        Callback used when the user deletes a row, ensuring frame forgetting the row and the button
        for adding a new row.
        :param deleted_row: An instance of the row class that is about to be deleted.
        :return: None
        """
        self.subtotals.remove(deleted_row.subtotal_var)
        self.get_total()
        self.widgets.remove(deleted_row)
