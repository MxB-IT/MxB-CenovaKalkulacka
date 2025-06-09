import tkinter as tk
from typing import *
from customtkinter import *
from customtkinter import CTkCheckBox, CTkLabel

class Spinbox(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))

class SectionBase:
    def arrange_widgets(self, master : CTkFrame, widgets : List[Tuple[tk.Widget, tk.Widget]]):
        for i, row in enumerate(widgets):
            for j, widget in enumerate(row):
                widget.grid(row=i,
                            column=j,
                            padx = 10,
                            pady = 10)
                master.columnconfigure(j, weight=1)
            master.rowconfigure(i, weight=1)

class PayrollSection(SectionBase):
    def __init__(self, master):
        self.frame = CTkFrame(master = master,
                              fg_color = "#b34f4c",
                              border_color = "white",
                              border_width = 2)
        self.widgets = []
        self.setup_widgets()
        self.arrange_widgets(self.frame, self.widgets)

    def setup_widgets(self):
        self.payrolls_amt = (CTkLabel(master = self.frame,
                                      text = "Počet mezd"),
                             Spinbox(master = self.frame,
                                     width = 150))
        self.payrolls_amt[1].set(0)
        self.widgets.append(self.payrolls_amt)

        self.payrolls_price = (CTkLabel(master = self.frame,
                                         text = "Cena za zpracování jedné"),
                               Spinbox(master = self.frame,
                                       width = 150))
        self.payrolls_price[1].set(0)
        self.widgets.append(self.payrolls_price)

        self.signups_signoffs = (CTkLabel(master = self.frame,
                                       text = "Počet přihlášek/odhlášek"),
                                 Spinbox(master = self.frame,
                                         width=150))
        self.signups_signoffs[1].set(0)
        self.widgets.append(self.signups_signoffs)

        self.executions = (CTkLabel(master = self.frame,
                                 text = "Exekuce"),
                        CTkComboBox(master = self.frame))
        self.executions[1].set(str(0))
        self.widgets.append(self.executions)

    def get_total(self) -> float:
        try:
            total = int(self.payrolls_amt[1].get()) * int(self.payrolls_price[1].get())
            total += int(self.signups_signoffs[1].get()) * 300
            total += int(self.executions[1].get()) * 880
            total *= 7/6

        except ValueError:
            return 0.0
        except TypeError:
            return 0.0

        return total

class AccountingSection(SectionBase):
    def __init__(self, master):
        self.frame = CTkFrame(master=master,
                              fg_color = "#b34f4c",
                              border_color = "white",
                              border_width = 2)

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
        self.setup_widgets()

        self.arrange_widgets(self.frame, self.widgets[:2] + self.no_dph_widgets + self.widgets[2:])

        self.total = 0

    def setup_widgets(self):
        self.checkboxes = (CTkCheckBox(master = self.frame,
                                       text = "Evidence",
                                       variable = self.evidence_bool),
                            CTkCheckBox(master = self.frame,
                                        text = "Účto",
                                        variable = self.ucto_bool))
        self.widgets.append(self.checkboxes)

        self.dph_pay = (CTkCheckBox(master = self.frame,
                                    text = "Plátce DPH",
                                    variable = self.dph_pay_bool,
                                    command = lambda: self.toggle_dph()),
                   CTkLabel(master = self.frame,
                            text = ""))
        self.widgets.append(self.dph_pay)

        self.import_only = (CTkCheckBox(master = self.frame,
                                        text = "import",
                                        variable = self.import_only_bool),
                            CTkComboBox(master=self.frame,
                                        values=[str(800), str(1000), str(1200), str(1400), str(1600)]))
        self.import_only[1].set(str(1000))
        self.widgets.append(self.import_only)

        self.by_hand = (CTkLabel(master = self.frame,
                                 text = "Počet vystavených faktur pro ruční zpracování"),
                        Spinbox(master = self.frame,
                                width = 150))
        self.by_hand[1].set(0)
        self.widgets.append(self.by_hand)

        self.create_vfa = (CTkLabel(master = self.frame,
                                    text = "Počet vydaných faktur k vystavení"),
                           Spinbox(master = self.frame,
                                    width = 150))
        self.create_vfa[1].set(0)
        self.widgets.append(self.create_vfa)

        self.pfa_amt = (CTkLabel(master = self.frame,
                                 text = "Počet přijatých faktur k vystavení"),
                        Spinbox(master = self.frame,
                                width = 150))
        self.pfa_amt[1].set(0)
        self.widgets.append(self.pfa_amt)

        self.credit_card_amt = (CTkLabel(master = self.frame,
                                         text = "Počet operací provedených platební kartou"),
                                Spinbox(master = self.frame,
                                        width = 150))
        self.credit_card_amt[1].set(0)
        self.widgets.append(self.credit_card_amt)

        self.register_amt = (CTkLabel(master = self.frame,
                                      text ="Počet pokladen"),
                             Spinbox(master = self.frame,
                                     width = 150))
        self.register_amt[1].set(0)
        self.widgets.append(self.register_amt)

        self.bank_amt = (CTkLabel(master = self.frame,
                                  text ="Počet bankovních výpisů"),
                         Spinbox(master = self.frame,
                                 width = 150))
        self.bank_amt[1].set(0)
        self.widgets.append(self.bank_amt)

        self.centers = (CTkCheckBox(master = self.frame,
                                    text = "Střediska",
                                    variable = self.centers_bool),
                        CTkLabel(master = self.frame,
                                 text="x1,1"))
        self.widgets.append(self.centers)

        self.orders = (CTkCheckBox(master = self.frame,
                                   text = "Zakázky",
                                   variable = self.orders_bool),
                       CTkLabel(master = self.frame,
                                text = "x1,1"))
        self.widgets.append(self.orders)

        self.analysis = (CTkCheckBox(master = self.frame,
                                     text = "Analytické služby",
                                     variable = self.analysis_bool),
                         CTkLabel(master = self.frame,
                                  text = "x1,1"))
        self.widgets.append(self.analysis)

        self.warehouses = (CTkCheckBox(master = self.frame,
                                       text = "Sklady",
                                       variable = self.warehouses_bool),
                           CTkLabel(master = self.frame,
                                    text = "x1,2"))
        self.widgets.append(self.warehouses)

        self.tax_check = (CTkCheckBox(master=self.frame,
                                      text="Kontrola DPH",
                                      variable=self.tax_check_bool),
                          CTkLabel(master=self.frame,
                                   text=""))
        self.dph_widgets.append(self.tax_check)

        self.send_docs = (CTkCheckBox(master=self.frame,
                                      text="Odeslání DPH, KH",
                                      variable=self.send_docs_bool),
                          CTkLabel(master=self.frame,
                                   text=""))
        self.dph_widgets.append(self.send_docs)

        self.create_dppodpfo = (CTkCheckBox(master=self.frame,
                                            text="Zpracování DPPO/DPFO",
                                            variable=self.dppodpfo_bool),
                                CTkLabel(master=self.frame,
                                         text=""))
        self.no_dph_widgets.append(self.create_dppodpfo)

    def toggle_dph(self):
        for widget in self.frame.grid_slaves():
            widget.grid_forget()
        if self.dph_pay_bool.get():
            self.arrange_widgets(self.frame, self.widgets[:2] + self.dph_widgets + self.widgets[2:])
        else:
            self.arrange_widgets(self.frame, self.widgets[:2] + self.no_dph_widgets + self.widgets[2:])

    def get_total(self) -> float:
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
            return 0.0
        except TypeError:
            return 0.0

        return total



class TotalSection(SectionBase):
    def __init__(self, master):
        self.frame = CTkFrame(master=master,
                              fg_color = "#b34f4c",
                              border_color = "white",
                              border_width = 2)

        self.widgets = []

        self.setup_widgets()
        self.arrange_widgets(self.frame, self.widgets)

    def setup_widgets(self):
        self.payrolls_total = (CTkLabel(master = self.frame,
                                               text = "Cena za mzdy"),
                                      CTkLabel(master = self.frame,
                                               text = ""))
        self.widgets.append(self.payrolls_total)

        self.accounting_total = (CTkLabel(master = self.frame,
                                           text = "Cena za účto"),
                                  CTkLabel(master = self.frame,
                                           text = ""))
        self.widgets.append(self.accounting_total)

        self.total_price = (CTkLabel(master = self.frame,
                                      text = "Cena celkem:"),
                             CTkLabel(master = self.frame,
                                      text = ""))
        self.widgets.append(self.total_price)

class BaseSection(SectionBase):
    def __init__(self, master):
        self.frame = CTkFrame(master=master,
                              fg_color="#b34f4c",
                              border_color="white",
                              border_width=2)

        self.accounting_bool = tk.BooleanVar(value = False)
        self.payrolls_bool = tk.BooleanVar(value = False)

        self.widgets = []

        self.setup_widgets()
        self.arrange_widgets(self.frame, self.widgets)

    def setup_widgets(self):
        self.checkboxes = (CTkCheckBox(master = self.frame,
                                       text = "Mzdy",
                                       variable = self.payrolls_bool,
                                       command = lambda: app.toggle_relevant(self.payrolls_bool.get(), app.payrolls_section, 1)),
                           CTkCheckBox(master = self.frame,
                                       text = "Účetnictví",
                                       variable = self.accounting_bool,
                                       command = lambda: app.toggle_relevant(self.accounting_bool.get(), app.accounting_section, 2)))

        self.widgets.append(self.checkboxes)

class PriceCalc(CTk):
    def __init__(self):
        super().__init__()
        self.title("Cenová kalkulačka")
        self.scrollable_frame = CTkScrollableFrame(master = self)
        self.scrollable_frame.pack(fill = "both",
                                   expand = True,
                                   padx = 10,
                                   pady = 10)

        self.base_section = BaseSection(self.scrollable_frame)
        self.total_section = TotalSection(self.scrollable_frame)
        self.payrolls_section = PayrollSection(self.scrollable_frame)
        self.accounting_section = AccountingSection(self.scrollable_frame)

        self.setup_sections()
        self.calculate_total()

    def setup_sections(self):

        self.base_section.frame.grid(row = 0,
                                     column = 0,
                                     padx = 10,
                                     pady = 10,
                                     columnspan = 2)
        self.total_section.frame.grid(row = 3,
                                      column = 0,
                                      padx = 10,
                                      pady = 10,
                                      columnspan = 2)

    def calculate_total(self):
        payrolls_total = PayrollSection.get_total(self.payrolls_section)
        accounting_total = AccountingSection.get_total(self.accounting_section)
        self.total_section.payrolls_total[1].configure(text = "%.3f" % payrolls_total)
        self.total_section.accounting_total[1].configure(text = "%.3f" % accounting_total)
        self.total_section.total_price[1].configure(text = "%.3f" % (payrolls_total + accounting_total))

        self.after(100, self.calculate_total)

    def toggle_relevant(self, toggle_bool, section, offset):
        if toggle_bool:
            section.frame.grid(row = offset,
                               column = 0,
                               padx = 10,
                               pady = 10,
                               columnspan = 2)
        else:
            section.frame.grid_forget()

if __name__ == "__main__":
    app = PriceCalc()
    app.mainloop()