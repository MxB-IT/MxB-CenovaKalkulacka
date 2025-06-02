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

def toggle_relevant(boolean_var : tk.BooleanVar, widgets : list) -> None:
    """
    toggles the relevant widgets depending on what button has been clicked
    :param boolean_var: represents the state of the button pressed
    :param widgets: all the widgets to either show or hide
    :return: None
    """
    if boolean_var.get():
        for widget in widgets:
            widget[0].grid(row = root.grid_size()[1], column = 0)
            widget[1].grid(row = root.grid_size()[1] - 1, column = 1)
    else:
        for widget in widgets:
            widget[0].grid_forget()
            widget[1].grid_forget()

def calculate_total() -> None:
    """
    calculates and displays the total price for the client based on data filled into the GUI
    :return: None, updates a label
    """
    total = 0

    try:
        if payrolls_bool.get():
            total += int(payrolls_amt_tuple[1].get()) * int(payrolls_price_tuple[1].get())
            total += int(signups_signoffs_tuple[1].get()) * 300
            total += int(executions_tuple[1].get()) * 880

        if accounting_bool.get():

            total += int(create_VFA[1].get()) * 50
            total += int(bank_amt[1].get()) * 10

            if import_only_bool.get():
                total += int(import_only[1].get())

            if evidence_bool.get():
                total += int(by_hand[1].get()) * 25
                total += int(PFA_amt[1].get()) * 25
                total += int(credit_card_amt[1].get()) * 35
                total += int(view_amt[1].get()) * 25

            if ucto_bool.get():
                total += int(by_hand[1].get()) * 35
                total += int(PFA_amt[1].get()) * 35
                total += int(credit_card_amt[1].get()) * 35
                total += int(view_amt[1].get()) * 35

            if tax_check_bool.get():

                if int(create_VFA[1].get()) + int(PFA_amt[1].get()) + int(view_amt[1].get()) + int(
                        bank_amt[1].get()) < 300:
                    total += 500
                elif 300 <= int(create_VFA[1].get()) + int(PFA_amt[1].get()) + int(view_amt[1].get()) + int(
                        bank_amt[1].get()) < 500:
                    total += 700
                elif 500 <= int(create_VFA[1].get()) + int(PFA_amt[1].get()) + int(view_amt[1].get()) + int(
                        bank_amt[1].get()) < 1000:
                    total += 1000
                else:
                    total += 2000

            if send_docs_bool.get():
                total += 300

        total = total * 7 / 6

    except ValueError:
        pass

    total_price_tuple[1].configure(text=str(total))

    root.after(100, calculate_total)

if __name__ == '__main__':

    root = CTk()
    root.title("Cenová kalkulačka")

    VFA_header = CTkLabel(master=root, text="Vydané faktury"), CTkLabel(master=root, text="Vydané faktury")
    PFA_header = CTkLabel(master=root, text="Přijaté faktury"), CTkLabel(master=root, text="Přijaté faktury")
    total_price_tuple = CTkLabel(master=root, text="Cena celkem:"), CTkLabel(master=root, text="")

    payrolls_bool = tk.BooleanVar()
    payrolls_checkbox = CTkCheckBox(master = root, text = "Mzdy", variable = payrolls_bool,
                                    command = lambda : toggle_relevant(payrolls_bool, payrolls_widgets))
    accounting_bool = tk.BooleanVar()
    accounting_checkbox = CTkCheckBox(master = root, text = "Účetnictví", variable = accounting_bool,
                                      command = lambda : toggle_relevant(accounting_bool, accounting_widgets))


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

    accounting_widgets = list()

    DPH_pay_bool = tk.BooleanVar()
    evidence_bool = tk.BooleanVar()
    ucto_bool = tk.BooleanVar()

    DPH_pay = (CTkCheckBox(master=root, text="Plátce DPH", variable=DPH_pay_bool),
               CTkLabel(master=root, text=""))
    accounting_widgets.append(DPH_pay)

    accounting_checkboxes = (CTkCheckBox(master = root, text = "Evidence", variable = evidence_bool),
                             CTkCheckBox(master = root, text = "Účto", variable = ucto_bool))
    accounting_widgets.append(accounting_checkboxes)
    accounting_widgets.append(VFA_header)

    import_only_bool = tk.BooleanVar()
    import_only = (CTkCheckBox(master = root, text = "1x import", variable = import_only_bool),
                   CTkComboBox(master = root, values = sorted([str(1200), str(1400), str(1600), str(800)])))
    import_only[1].set(str(1000))
    accounting_widgets.append(import_only)

    by_hand = (CTkLabel(master = root, text = "Počet ručně"),
               Spinbox(master = root, width = 150))
    by_hand[1].set(0)
    accounting_widgets.append(by_hand)

    create_VFA = (CTkLabel(master = root, text = "Počet vydaných faktur k vystavení"),
                  Spinbox(master = root, width = 150))
    create_VFA[1].set(0)
    accounting_widgets.append(create_VFA)

    accounting_widgets.append(PFA_header)
    PFA_amt = (CTkLabel(master = root, text = "Počet přijatých faktur k vystavení"),
               Spinbox(master = root, width = 150))
    PFA_amt[1].set(0)
    accounting_widgets.append(PFA_amt)

    credit_card_amt = (CTkLabel(master = root, text = "Počet operací provedených platební kartou"),
                       Spinbox(master = root, width = 150))
    credit_card_amt[1].set(0)
    accounting_widgets.append(credit_card_amt)

    view_amt = (CTkLabel(master = root, text = "Počet pokladen"),
                Spinbox(master = root, width = 150))
    view_amt[1].set(0)
    accounting_widgets.append(view_amt)

    bank_amt = (CTkLabel(master = root, text ="Počet bankovních výpisů"),
                Spinbox(master = root, width = 150))
    bank_amt[1].set(0)
    accounting_widgets.append(bank_amt)

    tax_check_bool = tk.BooleanVar()
    tax_check = (CTkCheckBox(master = root, text = "Kontrola DPH", variable = tax_check_bool),
                 CTkLabel(master = root, text = ""))
    accounting_widgets.append(tax_check)

    send_docs_bool = tk.BooleanVar()
    send_docs = (CTkCheckBox(master = root, text = "Odeslání DPH, KH", variable = send_docs_bool),
                 CTkLabel(master = root, text = ""))
    accounting_widgets.append(send_docs)



    total_price_tuple[0].grid(row = 0, column = 0)
    total_price_tuple[1].grid(row = 0, column = 1)
    payrolls_checkbox.grid(row = 1, column = 0)
    accounting_checkbox.grid(row = 1, column = 1)

    calculate_total()

    root.mainloop()
