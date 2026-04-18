from src.Sections.SectionBase import *


class TotalSection(SectionBase):
    """
    section defining space for all widgets containing calculated totals
    """
    def __init__(self, master):
        self.frame = FrameBase(master=master)

        self.widgets = []

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
        """
        sets up all the widgets with their default values
        :return: None
        """
        self.widgets.append(self.payrolls_total)
        self.widgets.append(self.accounting_total)
        self.widgets.append(self.total_price)