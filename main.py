import tkinter as tk
from tkinter import ttk

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

    print("Calculating...")
    total = 0

    try:
        if payrolls_bool.get():
            total += int(payrolls_amt_tuple[1].get()) * int(payrolls_price_tuple[1].get())
            total += int(signups_signoffs_tuple[1].get()) * 300
            total += int(executions_tuple[1].get()) * 880

        if accounting_bool.get():
            if evidence_bool.get():
                pass
            else:
                pass
    except ValueError:
        pass

    total_price_tuple[1].config(text=str(total))

    root.after(100, calculate_total)

if __name__ == '__main__':

    root = tk.Tk()
    root.title("Cenová kalkulačka")

    VFA_header = ttk.Label(master=root, text="VFA"), ttk.Label(master=root, text="VFA")
    PFA_header = ttk.Label(master=root, text="PFA"), ttk.Label(master=root, text="PFA")
    total_price_tuple = ttk.Label(master=root, text="Cena celkem:"), ttk.Label(master=root, text="")

    payrolls_bool = tk.BooleanVar()
    payrolls_checkbox = ttk.Checkbutton(master = root, text = "Mzdy", variable = payrolls_bool, command = lambda : toggle_relevant(payrolls_bool, payrolls_widgets))
    accounting_bool = tk.BooleanVar()
    accounting_checkbox = ttk.Checkbutton(master = root, text = "Účetnictví", variable = accounting_bool, command = lambda : toggle_relevant(accounting_bool, accounting_widgets))

    payrolls_widgets = []

    payrolls_amt_tuple = ttk.Label(master = root, text = "Počet mezd"), ttk.Spinbox(master = root)
    payrolls_widgets.append(payrolls_amt_tuple)
    payrolls_price_tuple = ttk.Label(master = root, text = "Cena za zpracování jedné"), ttk.Spinbox(master = root)
    payrolls_price_tuple[1].set(275)
    payrolls_widgets.append(payrolls_price_tuple)
    signups_signoffs_tuple = ttk.Label(master = root, text = "Počet přihlášek/odhlášek"), ttk.Spinbox(master = root)
    payrolls_widgets.append(signups_signoffs_tuple)
    executions_tuple = ttk.Label(master = root, text = "Exekuce"), ttk.Combobox(master = root)
    payrolls_widgets.append(executions_tuple)

    payrolls_widgets.append(total_price_tuple)


    accounting_widgets = []

    evidence_bool = tk.BooleanVar()
    ucto_bool = tk.BooleanVar()

    accounting_checkboxes = (ttk.Checkbutton(master = root, text = "Evidence", variable = evidence_bool),
                             ttk.Checkbutton(master = root, text = "Účto", variable = ucto_bool))
    accounting_widgets.append(accounting_checkboxes)
    accounting_widgets.append(VFA_header)
    import_only = ttk.Checkbutton(master = root, text = "1x import"), ttk.Combobox(master = root)
    import_only[1].set(1000)
    accounting_widgets.append(import_only)
    by_hand = ttk.Label(master = root, text = "Počet ručně"), ttk.Spinbox(master = root)
    accounting_widgets.append(by_hand)
    create_VFA = ttk.Label(master = root, text = "Počet VFA k vystavení"), ttk.Spinbox(master = root)
    accounting_widgets.append(create_VFA)
    accounting_widgets.append(PFA_header)
    PFA_amt = ttk.Label(master = root, text = "Počet PFA k vystavení"), ttk.Spinbox(master = root)
    accounting_widgets.append(PFA_amt)
    view_amt = ttk.Label(master = root, text = "Počet pohledů(?) k vystavení"), ttk.Spinbox(master = root)
    accounting_widgets.append(view_amt)
    package_amt = ttk.Label(master = root, text = "Baulici(?)"), ttk.Spinbox(master = root)
    accounting_widgets.append(package_amt)
    tax_check = ttk.Checkbutton(master = root, text = "Kontrola DPH"), ttk.Label(master = root, text = "")
    accounting_widgets.append(tax_check)
    send_docs = ttk.Checkbutton(master = root, text = "Odeslání DPH, KH"), ttk.Label(master = root, text = "")
    accounting_widgets.append(send_docs)

    accounting_widgets.append(total_price_tuple)

    payrolls_checkbox.grid(row = 0, column = 0)
    accounting_checkbox.grid(row = 0, column = 1)

    calculate_total()

    root.mainloop()
