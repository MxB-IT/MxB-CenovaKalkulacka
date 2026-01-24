from customtkinter import *
from typing import *
from tkinter import *
from Widgets.LabelBase import *
from Widgets.FrameBase import *
from Widgets.CTkSpinbox import *
from Widgets.CheckBoxBase import *
from Widgets.ComboBoxBase import *

class SectionBase:
    """
    server as a base for all sections, containing common methods
    """
    @staticmethod
    def arrange_widgets(master : CTkFrame, widgets : List[Tuple[Widget, Widget]]) -> None:
        """
        arranges widgets into a grid layout within the master parameter
        :param master: the master widget within which to arrange all the child widgets
        :param widgets: list of all child widgets, expected to be arranged into a list of tuples, where each list item
                        represents a row and each tuple item represents a column within the grid
        :return: None
        """
        for i, row in enumerate(widgets):

            # if row does not contain multiple elements, make it a list in order to not break the rest of the logic
            if not isinstance(row, (list, tuple)):
                row = [row]

            span_width = 4 if len(row) == 1 else 1

            for j, widget in enumerate(row):
                widget.grid(row=i,
                            column=j,
                            padx = 10,
                            pady = 10,
                            columnspan=span_width,
                            sticky="ew")
                master.columnconfigure(j, weight=1)
            master.rowconfigure(i, weight=1)