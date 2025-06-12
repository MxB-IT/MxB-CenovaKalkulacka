import tkinter as tk
from typing import *
from customtkinter import *

FontManager.load_font('./DMSans-Regular.ttf')

NUMBER_FORMAT = "%.3f"
MXB_RED = "#703230"

class ComboBoxBase(CTkComboBox):
    def __init__(self,
                 *args,
                 master: CTkFrame,
                 border_color = "#401c1b",
                 fg_color = "white",
                 dropdown_fg_color = "white",
                 button_color = "#401c1b",
                 text_color = MXB_RED,
                 dropdown_text_color = MXB_RED,
                 border_width = 2,
                 **kwargs):
        super().__init__(*args,
                         master,
                         border_color = border_color,
                         fg_color = fg_color,
                         dropdown_fg_color = dropdown_fg_color,
                         button_color = button_color,
                         text_color = text_color,
                         dropdown_text_color = dropdown_text_color,
                         border_width = border_width,
                         **kwargs)

class CheckBoxBase(CTkCheckBox):
    def __init__(self,
                 *args,
                 master: CTkFrame,
                 fg_color = MXB_RED,
                 border_color = MXB_RED,
                 text_color = MXB_RED,
                 hover_color = MXB_RED,
                 **kwargs):
        super().__init__(*args,
                         master,
                         hover_color = hover_color,
                         fg_color = fg_color,
                         border_color = border_color,
                         text_color = text_color,
                         **kwargs)

class FrameBase(CTkFrame):
    def __init__(self,
                 *args,
                 master: CTkFrame,
                 fg_color = "white",
                 border_color = MXB_RED,
                 border_width = 2,
                 **kwargs):
        super().__init__(*args,
                         master,
                         fg_color = fg_color,
                         border_color = border_color,
                         border_width = border_width,
                         **kwargs)

class LabelBase(CTkLabel):
    def __init__(self,
                 *args,
                 master: CTkFrame,
                 text_color = MXB_RED,
                 **kwargs):
        super().__init__(*args,
                         master,
                         text_color = text_color,
                         **kwargs)

class Spinbox(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 variable: Optional[tk.Variable] = None,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.variable = variable or tk.DoubleVar(value=0)
        self.variable.trace_add("write",
                                self._on_var_change)

        self.configure(fg_color=MXB_RED)
        self.grid_columnconfigure((0, 2),
                                  weight=0)
        self.grid_columnconfigure(1,
                                  weight=1)

        self.subtract_button = CTkButton(self, text="-",
                                         width=height-6,
                                         height=height-6,
                                         command=self.subtract_button_callback,
                                         fg_color="white",
                                         text_color=MXB_RED)
        self.subtract_button.grid(row=0,
                                  column=0,
                                  padx=(3, 0),
                                  pady=3)

        self.entry = CTkEntry(self,
                              width=width - 2 * height,
                              height=height - 6,
                              border_width=0,
                              textvariable=self.variable)
        self.entry.grid(row=0,
                        column=1,
                        padx=3,
                        pady=3,
                        sticky="ew")

        self.add_button = CTkButton(self,
                                    text="+",
                                    width=height-6,
                                    height=height-6,
                                    command=self.add_button_callback,
                                    fg_color="white",
                                    text_color=MXB_RED)
        self.add_button.grid(row=0,
                             column=2,
                             padx=(0, 3),
                             pady=3)

    def _on_var_change(self, *args):
        if self.command:
            self.command()

    def add_button_callback(self):
        try:
            self.variable.set(self.variable.get() + self.step_size)
        except Exception:
            self.variable.set(0)

    def subtract_button_callback(self):
        try:
            self.variable.set(self.variable.get() - self.step_size)
        except Exception:
            self.variable.set(0)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)


class SectionBase:
    """
    server as a base for all sections, containing common methods
    """
    def arrange_widgets(self, master : CTkFrame, widgets : List[Tuple[tk.Widget, tk.Widget]]) -> None:
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
                             Spinbox(master=self.frame,
                                     width=150,
                                     variable=self.payrolls_amt_var))
        self.payrolls_price_var = DoubleVar(value=250.0)
        self.payrolls_price_var.trace_add("write",self.get_total)
        self.payrolls_price = (LabelBase(master=self.frame,
                                         text="Cena za zpracování jedné"),
                               Spinbox(master=self.frame,
                                       width=150,
                                       variable=self.payrolls_price_var))
        self.signups_signoffs_var = DoubleVar()
        self.signups_signoffs_var.trace_add("write", self.get_total)
        self.signups_signoffs = (LabelBase(master=self.frame,
                                           text="Počet přihlášek/odhlášek"),
                                 Spinbox(master=self.frame,
                                         width=150,
                                         variable=self.signups_signoffs_var))

        self.executions_var = tk.DoubleVar()
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

class AccountingSection(SectionBase):
    """
    defines a section for the accounting widgets
    """
    def __init__(self, master, on_total_change: Callable) -> None:
        self.frame = FrameBase(master=master)

        self.total = DoubleVar(value=0.0)
        self.total.trace_add("write", lambda *args: on_total_change())
        self.import_only_bool = tk.BooleanVar(value = False)
        self.dph_pay_bool = tk.BooleanVar(value = False)
        self.evidence_bool = tk.BooleanVar(value = False)
        self.ucto_bool = tk.BooleanVar(value = False)
        self.centers_bool = tk.BooleanVar(value = False)
        self.orders_bool = tk.BooleanVar(value = False)
        self.analysis_bool = tk.BooleanVar(value = False)
        self.warehouses_bool = tk.BooleanVar(value = False)
        self.send_docs_bool = tk.BooleanVar(value = False)
        self.dppodpfo_bool = tk.BooleanVar(value = False)
        self.tax_check_bool = tk.BooleanVar(value = False)

        self.widgets = []
        self.dph_widgets = []
        self.no_dph_widgets = []

        self.checkboxes = (CheckBoxBase(master=self.frame,
                                        text="Evidence",
                                        variable=self.evidence_bool,
                                        command=lambda: self.checkboxes[1].deselect()),
                           CheckBoxBase(master=self.frame,
                                        text="Účto",
                                        variable=self.ucto_bool,
                                        command=lambda: self.checkboxes[0].deselect()))
        self.dph_pay = (CheckBoxBase(master=self.frame,
                                     text="Plátce DPH",
                                     variable=self.dph_pay_bool,
                                     command=lambda: self.toggle_dph()),
                        LabelBase(master=self.frame,
                                  text=""))
        self.import_only_var=DoubleVar()
        self.import_only_var.trace_add("write", self.get_total)
        self.import_only = (CheckBoxBase(master=self.frame,
                                         text="Import vystavených faktur",
                                         variable=self.import_only_bool,
                                         command=self.get_total),
                            ComboBoxBase(master=self.frame,
                                         values=[str(800), str(1000), str(1200), str(1400), str(1600)],
                                         variable=self.import_only_var))
        self.by_hand_var = DoubleVar()
        self.by_hand_var.trace_add("write", self.get_total)
        self.by_hand = (LabelBase(master=self.frame,
                                  text="Počet zaúčtovaných vystavených faktur"),
                        Spinbox(master=self.frame,
                                width=150,
                                variable=self.by_hand_var))
        self.create_vfa_var = DoubleVar()
        self.create_vfa_var.trace_add("write", self.get_total)
        self.create_vfa = (LabelBase(master=self.frame,
                                     text="Počet vystavovaných faktur za klienta"),
                           Spinbox(master=self.frame,
                                   width=150,
                                   variable=self.create_vfa_var))
        self.pfa_amt_var = DoubleVar()
        self.pfa_amt_var.trace_add("write", self.get_total)
        self.pfa_amt = (LabelBase(master=self.frame,
                                  text="Počet přijatých faktur"),
                        Spinbox(master=self.frame,
                                width=150,
                                variable=self.pfa_amt_var))
        self.credit_card_amt_var = DoubleVar()
        self.credit_card_amt_var.trace_add("write", self.get_total)
        self.credit_card_amt = (LabelBase(master=self.frame,
                                          text="Počet operací provedených platební kartou"),
                                Spinbox(master=self.frame,
                                        width=150,
                                        variable=self.credit_card_amt_var))
        self.register_amt_var = DoubleVar()
        self.register_amt_var.trace_add("write", self.get_total)
        self.register_amt = (LabelBase(master=self.frame,
                                       text="Počet pokladních dokladů"),
                             Spinbox(master=self.frame,
                                     width=150,
                                     variable=self.register_amt_var))
        self.centers = (CheckBoxBase(master=self.frame,
                                     text="Střediska",
                                     variable=self.centers_bool,
                                     command=self.get_total),
                        LabelBase(master=self.frame,
                                  text="x1,1"))
        self.bank_amt_var = DoubleVar()
        self.bank_amt_var.trace_add("write", self.get_total)
        self.bank_amt = (LabelBase(master=self.frame,
                                   text="Počet položek na bance"),
                         Spinbox(master=self.frame,
                                 width=150,
                                 variable=self.bank_amt_var))
        self.orders = (CheckBoxBase(master=self.frame,
                                    text="Zakázky",
                                    variable=self.orders_bool,
                                    command=self.get_total),
                       LabelBase(master=self.frame,
                                 text="x1,1"))
        self.analysis = (CheckBoxBase(master=self.frame,
                                      text="Analytické služby",
                                      variable=self.analysis_bool,
                                      command=self.get_total),
                         LabelBase(master=self.frame,
                                   text="x1,1"))
        self.warehouses = (CheckBoxBase(master=self.frame,
                                        text="Sklady",
                                        variable=self.warehouses_bool,
                                        command=self.get_total),
                           LabelBase(master=self.frame,
                                     text="x1,2"))
        self.tax_check = (CheckBoxBase(master=self.frame,
                                       text="Kontrola DPH",
                                       variable=self.tax_check_bool,
                                       command=self.get_total),
                          LabelBase(master=self.frame,
                                    text=""))
        self.send_docs = (CheckBoxBase(master=self.frame,
                                       text="Odeslání DPH, KH",
                                       variable=self.send_docs_bool,
                                       command=self.get_total),
                          LabelBase(master=self.frame,
                                    text=""))
        self.create_dppodpfo = (CheckBoxBase(master=self.frame,
                                             text="Zpracování DPPO/DPFO",
                                             variable=self.dppodpfo_bool,
                                             command=self.get_total),
                                LabelBase(master=self.frame,
                                          text=""))

        self.setup_widgets()

        self.arrange_widgets(self.frame, self.widgets[:2] + self.no_dph_widgets + self.widgets[2:])

    def setup_widgets(self) -> None:
        """
        sets up all widgets into default states with default values
        :return: None
        """
        self.widgets.append(self.checkboxes)
        self.widgets.append(self.dph_pay)
        self.import_only[1].set(str(1000))
        self.widgets.append(self.import_only)
        self.by_hand[1].set(0)
        self.widgets.append(self.by_hand)
        self.create_vfa[1].set(0)
        self.widgets.append(self.create_vfa)
        self.pfa_amt[1].set(0)
        self.widgets.append(self.pfa_amt)
        self.credit_card_amt[1].set(0)
        self.widgets.append(self.credit_card_amt)
        self.register_amt[1].set(0)
        self.widgets.append(self.register_amt)
        self.bank_amt[1].set(0)
        self.widgets.append(self.bank_amt)
        self.widgets.append(self.centers)
        self.widgets.append(self.orders)
        self.widgets.append(self.analysis)
        self.widgets.append(self.warehouses)
        self.dph_widgets.append(self.tax_check)
        self.dph_widgets.append(self.send_docs)
        self.no_dph_widgets.append(self.create_dppodpfo)

    def toggle_dph(self) -> None:
        """
        toggles all widgets to do with dph
        :return: None
        """
        for widget in self.frame.grid_slaves():
            widget.grid_forget()
        if self.dph_pay_bool.get():
            #disgusting hack
            self.arrange_widgets(self.frame, self.widgets[:2] + self.dph_widgets + self.widgets[2:])
        else:
            #disgusting hack
            self.arrange_widgets(self.frame, self.widgets[:2] + self.no_dph_widgets + self.widgets[2:])

    def get_total(self, *args) -> None:
        """
        gets the total of all the widgets within the section
        :return: float representing the total
        """
        try:
            if self.dph_pay_bool.get():

                total = int(self.create_vfa[1].get()) * 50
                total += int(self.bank_amt[1].get()) * 10

                if self.import_only_bool.get():
                    total += int(self.import_only[1].get())

                if self.evidence_bool.get():
                    total += int(self.by_hand[1].get()) * 25
                    total += int(self.pfa_amt[1].get()) * 25
                    total += int(self.credit_card_amt[1].get()) * 35
                    total += int(self.register_amt[1].get()) * 25

                if self.ucto_bool.get():
                    total += int(self.by_hand[1].get()) * 35
                    total += int(self.pfa_amt[1].get()) * 35
                    total += int(self.credit_card_amt[1].get()) * 35
                    total += int(self.register_amt[1].get()) * 35

                if self.tax_check_bool.get():

                    if int(self.create_vfa[1].get()) + int(self.pfa_amt[1].get()) + int(self.register_amt[1].get()) + int(
                            self.bank_amt[1].get()) + int(self.by_hand[1].get()) < 300:
                        total += 500
                    elif 300 <= int(self.create_vfa[1].get()) + int(self.pfa_amt[1].get()) + int(self.register_amt[1].get()) + int(
                            self.bank_amt[1].get()) + int(self.by_hand[1].get()) < 500:
                        total += 700
                    elif 500 <= int(self.create_vfa[1].get()) + int(self.pfa_amt[1].get()) + int(self.register_amt[1].get()) + int(
                            self.bank_amt[1].get()) + int(self.by_hand[1].get()) < 1000:
                        total += 1000
                    else:
                        total += 2000

                if self.send_docs_bool.get():
                    total += 300

                total *= 7/6

            else:
                total = int(self.by_hand[1].get()) * 20
                total += int(self.create_vfa[1].get()) * 20
                total += int(self.credit_card_amt[1].get()) * 20
                total += int(self.register_amt[1].get()) * 20
                total += int(self.bank_amt[1].get()) * 10

                if self.import_only_bool.get():
                    total += int(self.import_only[1].get())

                if self.dppodpfo_bool.get():
                    total += 1500

            if self.centers_bool.get():
                total *= 1.1
            if self.orders_bool.get():
                total *= 1.1
            if self.analysis_bool.get():
                total *= 1.1
            if self.warehouses_bool.get():
                total *= 1.2

        except ValueError:
            total = 0.0
        except TypeError:
            total = 0.0

        self.total.set(total)



class TotalSection(SectionBase):
    """
    section defining space for all widgets containing calculated totals
    """
    def __init__(self, master):
        self.frame = FrameBase(master=master)

        self.widgets = []

        self.payrolls_total = (LabelBase(master=self.frame,
                                         text="Cena za mzdy",
                                         font=CTkFont("DMSans-Regular")),
                               LabelBase(master=self.frame,
                                         text="",
                                         font=CTkFont("DMSans-Regular")))
        self.accounting_total = (LabelBase(master=self.frame,
                                           text="Cena za účto",
                                           font=CTkFont("DMSans-Regular")),
                                 LabelBase(master=self.frame,
                                           text="",
                                           font=CTkFont("DMSans-Regular")))
        self.total_price = (LabelBase(master=self.frame,
                                      text="Cena celkem:",
                                      font=CTkFont("DM Sans")),
                            LabelBase(master=self.frame,
                                      text="",
                                      font=CTkFont("DM Sans")))

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

class BaseSection(SectionBase):
    """
    section defining space for all the base widgets (base decisions visible on startup)
    """
    def __init__(self, master):
        self.frame = FrameBase(master=master)

        self.accounting_bool = tk.BooleanVar(value = False)
        self.payrolls_bool = tk.BooleanVar(value = False)

        self.widgets = []

        self.checkboxes = (CheckBoxBase(master=self.frame,
                                        text="Mzdy",
                                        variable=self.payrolls_bool,
                                        command=lambda: app.toggle_relevant(self.payrolls_bool.get(),
                                                                            app.payrolls_section, 1),
                                        font=CTkFont("DMSans-Regular")),
                           CheckBoxBase(master=self.frame,
                                        text="Účetnictví",
                                        variable=self.accounting_bool,
                                        command=lambda: app.toggle_relevant(self.accounting_bool.get(),
                                                                            app.accounting_section, 2),
                                        font=CTkFont('DMSans-Regular')))

        self.setup_widgets()
        self.arrange_widgets(self.frame, self.widgets)

    def setup_widgets(self) -> None:
        """
        sets up widgets into default states with their default values
        :return: None
        """
        self.widgets.append(self.checkboxes)

class PriceCalc(CTk):
    """
    price calculator app class
    handles the entire app operations
    """
    def __init__(self):
        super().__init__()
        self.geometry("400x600")
        self.title("Cenová kalkulačka")
        self.scrollable_frame = CTkScrollableFrame(master = self,
                                                   border_width = 2,
                                                   border_color = "white")
        self.scrollable_frame.grid(row = 0,
                                   column = 0,
                                   padx = 10,
                                   pady = 10,
                                   sticky = "ew")

        self.base_section = BaseSection(self.scrollable_frame)
        self.total_section = TotalSection(self.scrollable_frame)
        self.payrolls_section = PayrollSection(self.scrollable_frame, self.calculate_total)
        self.accounting_section = AccountingSection(self.scrollable_frame, self.calculate_total)

        self.setup_sections()
        self.calculate_total()
        self.bind("<Configure>", self.resize)

    def setup_sections(self) -> None:
        """
        sets up all the sections into default positions
        :return: None
        """

        self.base_section.frame.grid(row = 0,
                                     column = 0,
                                     columnspan = 2,
                                     sticky = "ew")
        self.total_section.frame.grid(row = 3,
                                      column = 0,
                                      columnspan = 2,
                                      sticky = "ew")
        self.update()
        self.scrollable_frame.configure(width = self.winfo_width(),
                                        height = self.winfo_height())
        self.scrollable_frame.rowconfigure((0,4), weight = 1)
        self.scrollable_frame.columnconfigure(0, weight = 1)

    def resize(self, event) -> None:
        """
        handles resizing of the internal widgets along with the window, since widgets are contained within a scrollable
        frame which would not resize on its own
        :param event: describes an event that occured on the app level
        :return: None
        """
        if event.widget == self:
            if self.scrollable_frame.winfo_width() != event.widget.winfo_width() or self.scrollable_frame.winfo_height() != event.widget.winfo_height():
                self.scrollable_frame.configure(width = event.width - 40,
                                                height = event.height - 40)
                self.scrollable_frame.update()

    def calculate_total(self, *args) -> None:
        """
        calculates the totals based on all the input data, calls itself every 100ms (subject to change)
        :return: None
        """
        self.total_section.payrolls_total[1].configure(text = NUMBER_FORMAT % self.payrolls_section.total.get())
        self.total_section.accounting_total[1].configure(text = NUMBER_FORMAT % self.accounting_section.total.get())
        self.total_section.total_price[1].configure(text = NUMBER_FORMAT % (self.payrolls_section.total.get() + self.accounting_section.total.get()))

    def toggle_relevant(self, toggle_bool, section, offset) -> None:
        """
        toggles relevant sections of the app based on user input
        :param toggle_bool: toggle deciding whether to turn a widget on or off
        :param section: section to toggle
        :param offset: offset at which to toggle said section
        :return: None
        """
        if toggle_bool:
            section.frame.grid(row = offset,
                               column = 0,
                               columnspan = 2,
                               sticky = "ew")
        else:
            section.frame.grid_forget()

if __name__ == "__main__":
    app = PriceCalc()
    app.mainloop()