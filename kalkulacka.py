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

def toggle_relevant(boolean_var : bool, widgets : list, offset : int) -> None:
    """
    toggles the relevant widgets depending on what button has been clicked
    :param boolean_var: represents the state of the button pressed
    :param widgets: all the widgets to either show or hide
    :param offset: offset of the widgets, makes sure all the widgets always render in the same predetermined place
    :return: None
    """
    if boolean_var:
        for index in range(0, len(widgets)):
            for portion in range(0, len(widgets[index])):
                widgets[index][portion].grid(row = offset + 4 + index, column = portion)
                root.rowconfigure(offset, weight=1)
    else:
        for widget in widgets:
            for portion in range(0, len(widget)):
                widget[portion].grid_forget()

def calculate_total() -> None:
    """
    calculates and displays the total price for the client based on data filled into the GUI
    :return: None, updates a label
    """
    payrolls_total = 0
    accounting_total = 0

    try:
        if payrolls_bool.get():
            payrolls_total += int(payrolls_amt_tuple[1].get()) * int(payrolls_price_tuple[1].get())
            payrolls_total += int(signups_signoffs_tuple[1].get()) * 300
            payrolls_total += int(executions_tuple[1].get()) * 880

            payrolls_total = payrolls_total * 7 / 6

        if accounting_bool.get():

            if not DPH_pay_bool.get():

                if import_only_bool.get():
                    accounting_total += int(import_only[1].get())

                accounting_total += int(by_hand[1].get()) * 20
                accounting_total += int(create_VFA[1].get()) * 20
                accounting_total += int(credit_card_amt[1].get()) * 20
                accounting_total += int(register_amt[1].get()) * 20
                accounting_total += int(bank_amt[1].get()) * 10

                if DPPODPFO_bool.get():
                    accounting_total += 1500

            else:

                accounting_total += int(create_VFA[1].get()) * 50
                accounting_total += int(bank_amt[1].get()) * 10

                if import_only_bool.get():
                    accounting_total += int(import_only[1].get())

                if evidence_bool.get():
                    accounting_total += int(by_hand[1].get()) * 25
                    accounting_total += int(PFA_amt[1].get()) * 25
                    accounting_total += int(credit_card_amt[1].get()) * 35
                    accounting_total += int(register_amt[1].get()) * 25

                if ucto_bool.get():
                    accounting_total += int(by_hand[1].get()) * 35
                    accounting_total += int(PFA_amt[1].get()) * 35
                    accounting_total += int(credit_card_amt[1].get()) * 35
                    accounting_total += int(register_amt[1].get()) * 35

                if tax_check_bool.get():

                    if int(create_VFA[1].get()) + int(PFA_amt[1].get()) + int(register_amt[1].get()) + int(
                            bank_amt[1].get()) + int(by_hand[1].get()) < 300:
                        accounting_total += 500
                    elif 300 <= int(create_VFA[1].get()) + int(PFA_amt[1].get()) + int(register_amt[1].get()) + int(
                            bank_amt[1].get()) + int(by_hand[1].get()) < 500:
                        accounting_total += 700
                    elif 500 <= int(create_VFA[1].get()) + int(PFA_amt[1].get()) + int(register_amt[1].get()) + int(
                            bank_amt[1].get()) + int(by_hand[1].get()) < 1000:
                        accounting_total += 1000
                    else:
                        accounting_total += 2000

                if send_docs_bool.get():
                    accounting_total += 300

                accounting_total = accounting_total * 7 / 6

        if centers_bool.get():
            accounting_total = accounting_total * 1.1
        if analytics_bool.get():
            accounting_total = accounting_total * 1.1
        if orders_bool.get():
            accounting_total = accounting_total * 1.1
        if warehouses_bool.get():
            accounting_total = accounting_total * 1.2

    except ValueError:
        pass

    finally:

        total = "%.3f" % (accounting_total + payrolls_total)
        accounting_total = "%.3f" % accounting_total
        payrolls_total = "%.3f" % payrolls_total

        accounting_price_tuple[1].configure(text = accounting_total)
        payrolls_total_price_tuple[1].configure(text = payrolls_total)
        total_price_tuple[1].configure(text = total)

        #kind of inefficiently done every 100ms, should change to only be done whenever there is a change in parms
        root.after(100, calculate_total)

def toggle_dph(dph_boolean : bool, dph_widgets : list, no_dph_widgets : list, dph_offset : int) -> None:
    if dph_boolean:
        toggle_relevant(False, no_dph_widgets, dph_offset)
        toggle_relevant(True, dph_widgets, dph_offset)
    else:
        toggle_relevant(False, dph_widgets, dph_offset)
        toggle_relevant(True, no_dph_widgets, dph_offset)

def accounting_wrapper(dph_boolean : bool, accounting_boolean : bool, widgets : list, dph_widgets : list, no_dph_widgets : list, accounting_offset : int, dph_offset : int) -> None:
    """
    serves as a wrapper function for accounting toggle to turn dph widgets on or off along with accounting, since that's
    what needs these widgets
    :param dph_boolean: toggle for deciding whether dph widgets are on or off
    :param accounting_boolean: toggle for turning accounting widgets on or off
    :param widgets: widgets to either show or hide
    :param dph_widgets: dph relevant widgets, to be shown when DPH is to be accounted for
    :param no_dph_widgets: dph relevant widgets, to be shown when DPH is not to be accounted for
    :param accounting_offset: offset for accounting widgets
    :param dph_offset: offset for dph widgets
    :return: None
    """
    toggle_relevant(accounting_boolean, widgets, accounting_offset)
    if accounting_boolean:
        toggle_dph(dph_boolean, dph_widgets, no_dph_widgets, dph_offset)
    else:
        toggle_relevant(False, no_dph_widgets, dph_offset)
        toggle_relevant(False, dph_widgets, dph_offset)

if __name__ == '__main__':

    #windows managed by customtkinter, looks nicer
    root = CTk()
    root.title("Cenová kalkulačka")

    #all widgets are stored in tuples, philosophy being that loading can be made easier through this

    #widgets for price display
    accounting_price_tuple = CTkLabel(master = root, text = "Cena za účto"), CTkLabel(master = root, text = "")
    payrolls_total_price_tuple = CTkLabel(master=root, text="Cena za mzdy"), CTkLabel(master = root, text = "")
    total_price_tuple = CTkLabel(master=root, text="Cena celkem:"), CTkLabel(master = root, text = "")

    #base checkboxes for determining the kind of widgets to display to the user
    payrolls_bool = tk.BooleanVar(value = False)
    payrolls_checkbox = CTkCheckBox(master = root, text = "Mzdy", variable = payrolls_bool,
                                    command = lambda : toggle_relevant(payrolls_bool.get(), payrolls_widgets, 0))
    accounting_bool = tk.BooleanVar(value = False)
    accounting_checkbox = CTkCheckBox(master = root, text = "Účetnictví", variable = accounting_bool,
                                      command = lambda : accounting_wrapper(DPH_pay_bool.get(), accounting_bool.get(), accounting_widgets, DPH_widgets, DPPO_widgets, len(payrolls_widgets) + len(DPH_widgets), 4 + len(payrolls_widgets) + len(accounting_widgets)))

    #payroll widgets
    payrolls_widgets = []

    payrolls_amt_tuple = (CTkLabel(master = root, text = "Počet mezd"),
                          Spinbox(master = root, width = 150))
    payrolls_amt_tuple[1].set(0)
    payrolls_widgets.append(payrolls_amt_tuple)

    payrolls_price_tuple = (CTkLabel(master = root, text = "Cena za zpracování jedné"),
                            Spinbox(master = root, width = 150))
    payrolls_price_tuple[1].set(275)
    payrolls_widgets.append(payrolls_price_tuple)

    signups_signoffs_tuple = (CTkLabel(master = root, text = "Počet přihlášek/odhlášek"),
                              Spinbox(master = root, width = 150))
    signups_signoffs_tuple[1].set(0)
    payrolls_widgets.append(signups_signoffs_tuple)

    executions_tuple = (CTkLabel(master = root, text = "Exekuce"),
                        CTkComboBox(master = root))
    executions_tuple[1].set(str(0))
    payrolls_widgets.append(executions_tuple)

    #accounting widgets
    DPH_widgets = list()
    DPPO_widgets = list()
    accounting_widgets = list()

    DPH_pay_bool = tk.BooleanVar(value = False)
    evidence_bool = tk.BooleanVar(value = False)
    ucto_bool = tk.BooleanVar(value = False)

    accounting_checkboxes = (CTkCheckBox(master = root, text = "Evidence", variable = evidence_bool),
                             CTkCheckBox(master = root, text = "Účto", variable = ucto_bool))
    DPH_widgets.append(accounting_checkboxes)

    import_only_bool = tk.BooleanVar()
    import_only = (CTkCheckBox(master = root, text = "import", variable = import_only_bool),
                   CTkComboBox(master = root, values = [str(800), str(1000), str(1200), str(1400), str(1600)]))
    import_only[1].set(str(1000))
    accounting_widgets.append(import_only)

    by_hand = (CTkLabel(master = root, text = "Počet vystavených faktur pro ruční zpracování"),
               Spinbox(master = root, width = 150))
    by_hand[1].set(0)
    accounting_widgets.append(by_hand)

    create_VFA = (CTkLabel(master = root, text = "Počet vydaných faktur k vystavení"),
                  Spinbox(master = root, width = 150))
    create_VFA[1].set(0)
    accounting_widgets.append(create_VFA)

    PFA_amt = (CTkLabel(master = root, text = "Počet přijatých faktur k vystavení"),
               Spinbox(master = root, width = 150))
    PFA_amt[1].set(0)
    accounting_widgets.append(PFA_amt)

    credit_card_amt = (CTkLabel(master = root, text = "Počet operací provedených platební kartou"),
                       Spinbox(master = root, width = 150))
    credit_card_amt[1].set(0)
    accounting_widgets.append(credit_card_amt)

    register_amt = (CTkLabel(master = root, text ="Počet pokladen"),
                    Spinbox(master = root, width = 150))
    register_amt[1].set(0)
    accounting_widgets.append(register_amt)

    bank_amt = (CTkLabel(master = root, text ="Počet bankovních výpisů"),
                Spinbox(master = root, width = 150))
    bank_amt[1].set(0)
    accounting_widgets.append(bank_amt)

    centers_bool = tk.BooleanVar(value = False)
    centers_tuple = (CTkCheckBox(master = root, text = "Střediska", variable = centers_bool),
                     CTkLabel(master=root, text="x1,1"))
    accounting_widgets.append(centers_tuple)
    orders_bool = tk.BooleanVar(value = False)
    orders_tuple = (CTkCheckBox(master = root, text = "Zakázky", variable = orders_bool),
                     CTkLabel(master = root, text = "x1,1"))
    accounting_widgets.append(orders_tuple)
    analytics_bool = tk.BooleanVar(value = False)
    analytics_tuple = (CTkCheckBox(master = root, text = "Analytické služby", variable = analytics_bool),
                     CTkLabel(master = root, text = "x1,1"))
    accounting_widgets.append(analytics_tuple)
    warehouses_bool = tk.BooleanVar(value = False)
    warehouses_tuple = (CTkCheckBox(master = root, text = "Sklady", variable = warehouses_bool),
                     CTkLabel(master = root, text = "x1,2"))
    accounting_widgets.append(warehouses_tuple)

    DPH_pay = (CTkCheckBox(master=root, text="Plátce DPH", variable=DPH_pay_bool,
                           command=lambda: toggle_dph(DPH_pay_bool.get(), DPH_widgets, DPPO_widgets,
                                                      4 + len(accounting_widgets) + len(payrolls_widgets))),
               CTkLabel(master=root, text=""))
    accounting_widgets.append(DPH_pay)

    tax_check_bool = tk.BooleanVar(value = False)
    tax_check = (CTkCheckBox(master = root, text = "Kontrola DPH", variable = tax_check_bool),
                 CTkLabel(master = root, text = ""))
    DPH_widgets.append(tax_check)

    send_docs_bool = tk.BooleanVar(value = False)
    send_docs = (CTkCheckBox(master = root, text = "Odeslání DPH, KH", variable = send_docs_bool),
                 CTkLabel(master = root, text = ""))
    DPH_widgets.append(send_docs)

    DPPODPFO_bool = tk.BooleanVar(value = False)
    create_DPPODPFO = (CTkCheckBox(master = root, text = "Zpracování DPPO/DPFO", variable = DPPODPFO_bool),
                       CTkLabel(master = root, text = ""))
    DPPO_widgets.append(create_DPPODPFO)

    #base widget rendering
    payrolls_total_price_tuple[0].grid(row=0, column=0)
    payrolls_total_price_tuple[1].grid(row=0, column=1)
    accounting_price_tuple[0].grid(row=1, column=0)
    accounting_price_tuple[1].grid(row=1, column=1)
    total_price_tuple[0].grid(row = 2, column = 0)
    total_price_tuple[1].grid(row = 2, column = 1)
    payrolls_checkbox.grid(row = 3, column = 0)
    accounting_checkbox.grid(row = 3, column = 1)

    #column configures for base widgets
    for i in range(0, root.grid_size()[1]):
        root.rowconfigure(i, weight = 1)
    for i in range(0, root.grid_size()[0]):
        root.columnconfigure(i, weight = 1)

    calculate_total()

    root.mainloop()
