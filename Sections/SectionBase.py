from customtkinter import *
from typing import *
from tkinter import *
from Widgets.Label import *
from Widgets.Frame import *
from Widgets.CTkSpinbox import *
from Widgets.CheckBox import *
from Widgets.ComboBox import *

class SectionBase:
    """
    server as a base for all sections, containing common methods
    """
    def arrange_widgets(self, master : CTkFrame, widgets : List[Tuple[Widget, Widget]]) -> None:
        """
        arranges widgets into a grid layout within the master parameter
        :param master: the master widget within which to arrange all the child widgets
        :param widgets: list of all child widgets, expected to be arranged into a list of tuples, where each list item
                        represents a row and each tuple item represents a column within the grid
        :return: None
        """
        for i, row in enumerate(widgets):
            for j, widget in enumerate(row):
                widget.grid(row=i,
                            column=j,
                            padx = 10,
                            pady = 10)
                master.columnconfigure(j, weight=1)
            master.rowconfigure(i, weight=1)