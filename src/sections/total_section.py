"""Defines a class for the section of the app containing totals."""
from typing import Any

from src.sections.section_base import SectionBase
from src.widgets.frame_base import FrameBase
from src.widgets.label_base import LabelBase


class TotalSection(SectionBase):
    """Section defining space for all widgets containing calculated totals."""

    def __init__(self,
                 master) -> None:
        """Initialise the total section class.

        Initialises the TotalSection class, defining and arranging the widgets within the section.
        :param master: Master widget for the totals section.
        :return: None
        """
        self.frame = FrameBase(master=master)

        self.widgets: list[tuple[Any, Any]] = []

        self.payrolls_total = (LabelBase(master=self.frame,
                                         text="Cena za mzdy"),
                               LabelBase(master=self.frame,
                                         text=""))
        self.accounting_total = (LabelBase(master=self.frame,
                                           text="Cena za účto"),
                                 LabelBase(master=self.frame,
                                           text=""))
        self.total_price = (LabelBase(master=self.frame,
                                      text="Cena celkem:"),
                            LabelBase(master=self.frame,
                                      text=""))

        self.setup_widgets()
        self.arrange_widgets(self.frame, self.widgets)

    def setup_widgets(self) -> None:
        """Set up all widgets for the totals section.

        Sets up all the widgets with their default values.
        :return: None
        """
        self.widgets.append(self.payrolls_total)
        self.widgets.append(self.accounting_total)
        self.widgets.append(self.total_price)
