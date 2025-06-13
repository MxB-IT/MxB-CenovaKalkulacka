from Sections.SectionBase import *

class PayrollSection(SectionBase):
    """
    defines a section for the payrolls widgets
    """
    def __init__(self, master, on_total_change: Callable):
        self.frame = CTkFrame(master = master,
                              fg_color = "white",
                              border_color = MXB_RED,
                              border_width = 2)
        self.widgets = []
        self.total = DoubleVar()
        self.total.trace_add("write", lambda *args: on_total_change())

        self.payrolls_amt_var = DoubleVar()
        self.payrolls_amt_var.trace_add("write", self.get_total)
        self.payrolls_amt = (LabelBase(master=self.frame,
                                       text="Počet mezd"),
                             CTkSpinbox(master=self.frame,
                                        width=150,
                                        variable=self.payrolls_amt_var))
        self.payrolls_price_var = DoubleVar(value=250.0)
        self.payrolls_price_var.trace_add("write",self.get_total)
        self.payrolls_price = (LabelBase(master=self.frame,
                                         text="Cena za zpracování jedné"),
                               CTkSpinbox(master=self.frame,
                                          width=150,
                                          variable=self.payrolls_price_var))
        self.signups_signoffs_var = DoubleVar()
        self.signups_signoffs_var.trace_add("write", self.get_total)
        self.signups_signoffs = (LabelBase(master=self.frame,
                                           text="Počet přihlášek/odhlášek"),
                                 CTkSpinbox(master=self.frame,
                                            width=150,
                                            variable=self.signups_signoffs_var))

        self.executions_var = DoubleVar()
        self.executions_var.trace_add("write", self.get_total)

        self.executions = (LabelBase(master=self.frame,
                                     text="Exekuce"),
                           ComboBoxBase(master=self.frame,
                                        variable = self.executions_var))

        self.setup_widgets()
        self.arrange_widgets(self.frame, self.widgets)

    def setup_widgets(self) -> None:
        """
        sets up all widgets into default locations with default values
        :return: None
        """
        self.payrolls_amt[1].set(0)
        self.widgets.append(self.payrolls_amt)
        self.payrolls_price[1].set(0)
        self.widgets.append(self.payrolls_price)
        self.signups_signoffs[1].set(0)
        self.widgets.append(self.signups_signoffs)
        self.executions[1].set(str(0))
        self.widgets.append(self.executions)

    def get_total(self, *args) -> None:
        """
        gets the total of all the widgets within the section
        :return: float representing the total
        """
        try:
            total = int(self.payrolls_amt[1].get()) * int(self.payrolls_price[1].get())
            total += int(self.signups_signoffs[1].get()) * 300
            total += int(self.executions[1].get()) * 880
            total *= 7/6

        except ValueError:
            total = 0.0
        except TypeError:
            total = 0.0
        self.total.set(total)