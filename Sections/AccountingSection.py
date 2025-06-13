from Sections.SectionBase import *

class AccountingSection(SectionBase):
    """
    defines a section for the accounting widgets
    """
    def __init__(self, master, on_total_change: Callable) -> None:
        self.frame = FrameBase(master=master)

        self.total = DoubleVar(value=0.0)
        self.total.trace_add("write", lambda *args: on_total_change())
        self.import_only_bool = BooleanVar(value = False)
        self.dph_pay_bool = BooleanVar(value = False)
        self.evidence_bool = BooleanVar(value = False)
        self.ucto_bool = BooleanVar(value = False)
        self.centers_bool = BooleanVar(value = False)
        self.orders_bool = BooleanVar(value = False)
        self.analysis_bool = BooleanVar(value = False)
        self.warehouses_bool = BooleanVar(value = False)
        self.send_docs_bool = BooleanVar(value = False)
        self.dppodpfo_bool = BooleanVar(value = False)
        self.tax_check_bool = BooleanVar(value = False)

        self.widgets = []
        self.dph_widgets = []
        self.no_dph_widgets = []

        self.checkboxes = (CheckBoxBase(master=self.frame,
                                        text="Evidence",
                                        variable=self.evidence_bool,
                                        command=lambda: self.base_checkbox_tick("Evidence")),
                           CheckBoxBase(master=self.frame,
                                        text="Účto",
                                        variable=self.ucto_bool,
                                        command=lambda: self.base_checkbox_tick("Účto")))
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
                        CTkSpinbox(master=self.frame,
                                   width=150,
                                   variable=self.by_hand_var))
        self.create_vfa_var = DoubleVar()
        self.create_vfa_var.trace_add("write", self.get_total)
        self.create_vfa = (LabelBase(master=self.frame,
                                     text="Počet vystavovaných faktur za klienta"),
                           CTkSpinbox(master=self.frame,
                                      width=150,
                                      variable=self.create_vfa_var))
        self.pfa_amt_var = DoubleVar()
        self.pfa_amt_var.trace_add("write", self.get_total)
        self.pfa_amt = (LabelBase(master=self.frame,
                                  text="Počet přijatých faktur"),
                        CTkSpinbox(master=self.frame,
                                   width=150,
                                   variable=self.pfa_amt_var))
        self.credit_card_amt_var = DoubleVar()
        self.credit_card_amt_var.trace_add("write", self.get_total)
        self.credit_card_amt = (LabelBase(master=self.frame,
                                          text="Počet operací provedených platební kartou"),
                                CTkSpinbox(master=self.frame,
                                           width=150,
                                           variable=self.credit_card_amt_var))
        self.register_amt_var = DoubleVar()
        self.register_amt_var.trace_add("write", self.get_total)
        self.register_amt = (LabelBase(master=self.frame,
                                       text="Počet pokladních dokladů"),
                             CTkSpinbox(master=self.frame,
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
                         CTkSpinbox(master=self.frame,
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

        self.get_total()

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

    def base_checkbox_tick(self, kind):
        match kind:
            case"Evidence":
                self.checkboxes[1].deselect()

            case "Účto":
                self.checkboxes[0].deselect()

        self.get_total()