from Common.DefaultPriceEnum import DefaultPriceEnum
from Sections.Components.Row import Row
from Sections.SectionBase import *

class PayrollSection(SectionBase):
    """
    defines a section for the payrolls widgets
    """
    def __init__(self, master, app: "PriceCalc"):
        self.frame = CTkFrame(master = master,
                              fg_color = "white",
                              border_color = MXB_RED,
                              border_width = 2)
        self.widgets = []
        self.total = DoubleVar()
        self.total.trace_add("write", app.calculate_total)
        self.subtotals = []

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

    def setup_widgets(self) -> None:
        """
        sets up all widgets into default locations with default values
        :return: None
        """
        self.widgets.append(self.headers)

    def get_total(self, *args) -> None:
        """
        gets the total of all the widgets within the section
        :return: float representing the total
        """
        total = 0.0
        try:
            for subtotal in self.subtotals:
                total += subtotal.get()

            total *= 7/6

        except ValueError as e:
            total = 0.0
            print(e)

        except TypeError as e:
            total = 0.0
            print(e)

        self.total.set(total)

    def define_row(self, text : str, price: Union[DefaultPriceEnum, float]) -> None:
        row = Row(master=self.frame,
                  text=text,
                  ucto_price=price)

        row.subtotal_var.trace_add("write", self.get_total)
        self.widgets.append(row)
        self.subtotals.append(row.subtotal_var)