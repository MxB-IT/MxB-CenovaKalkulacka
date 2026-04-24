"""Class for the base section in the app."""
from __future__ import annotations

from tkinter import BooleanVar
from typing import TYPE_CHECKING, Any

from src.sections.section_base import SectionBase
from src.widgets.checkbox_base import CheckBoxBase
from src.widgets.frame_base import FrameBase

if TYPE_CHECKING:
    from src.price_calc import PriceCalc

class BaseSection(SectionBase):
    """Define the base section in the app, containing basic checks.

    Section defining space for all the base widgets (base decisions visible on startup)
    """

    def __init__(self,
                 master,
                 app: PriceCalc) -> None:
        """Initialise BaseSection class.

        Initialises the BaseSection class with all its widgets prepped and variables set.
        :param master: Master widget for the BaseSection class.
        :param app: The PriceCalc app wrapper.
        :return: None
        """
        self.frame = FrameBase(master=master)

        self.accounting_bool = BooleanVar(value = False)
        self.payrolls_bool = BooleanVar(value = False)

        self.widgets: list[tuple[Any, Any]] = []

        self.checkboxes = (CheckBoxBase(master=self.frame,
                                        text="Mzdy",
                                        variable=self.payrolls_bool,
                                        command=lambda: app.toggle_relevant(self.payrolls_bool.get(),
                                                                            app.payrolls_section, 2)),
                           CheckBoxBase(master=self.frame,
                                        text="Účetnictví",
                                        variable=self.accounting_bool,
                                        command=lambda: app.toggle_relevant(self.accounting_bool.get(),
                                                                            app.accounting_section, 3)))

        self.setup_widgets()
        self.arrange_widgets(self.frame, self.widgets)

    def setup_widgets(self) -> None:
        """Set up all the widgets in the base section.

        Sets up widgets into default states with their default values
        :return: None
        """
        self.widgets.append(self.checkboxes)
