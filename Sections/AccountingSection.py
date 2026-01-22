from Sections.Components.Row import Row
from Sections.SectionBase import *
from Common.DefaultPriceEnum import DefaultPriceEnum
from Common.ModeEnum import ModeEnum

class AccountingSection(SectionBase):
    """
    defines a section for the accounting widgets
    """
    def __init__(self, master, app: "PriceCalc") -> None:
        self.frame = FrameBase(master=master)

        self.total = DoubleVar(value=0.0)
        self.total.trace_add("write", app.calculate_total)

        #wall of bools
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
        self.subtotals = []

        self.checkboxes = (CheckBoxBase(master=self.frame,
                                        text="Evidence",
                                        variable=self.evidence_bool,
                                        command=lambda: self.base_checkbox_tick(ModeEnum.EVIDENCE)),
                           CheckBoxBase(master=self.frame,
                                        text="Účto",
                                        variable=self.ucto_bool,
                                        command=lambda: self.base_checkbox_tick(ModeEnum.UCTO)))

        self.dph_pay = (CheckBoxBase(master=self.frame,
                                     text="Plátce DPH",
                                     variable=self.dph_pay_bool,
                                     command=lambda: self.toggle_dph()),
                        LabelBase(master=self.frame,
                                  text=""))

        self.import_only_var=DoubleVar(value=0.0)
        self.import_only_var.trace_add("write", self.get_total)

        self.import_only = (CheckBoxBase(master=self.frame,
                                         text="Import vystavených faktur",
                                         variable=self.import_only_bool,
                                         command=self.get_total),
                            ComboBoxBase(master=self.frame,
                                         values=[str(800), str(1000), str(1200), str(1400), str(1600)],
                                         variable=self.import_only_var))

        self.headers = (LabelBase(master=self.frame,
                                  text="Položka"),
                        LabelBase(master=self.frame,
                                  text="Počet"),
                        LabelBase(master=self.frame,
                                  text="Cena")
                        )

        self.centers = (CheckBoxBase(master=self.frame,
                                     text="Střediska",
                                     variable=self.centers_bool,
                                     command=self.get_total),
                        LabelBase(master=self.frame,
                                  text="x1,1"))

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

        self.define_row(text="Počet položek na bance",
                        evidence_price=DefaultPriceEnum.BANK,
                        ucto_price=DefaultPriceEnum.BANK,
                        dph_price=DefaultPriceEnum.BANK,
                        no_dph_price=DefaultPriceEnum.BANK)
        self.define_row(text="Počet zaúčtovaných vystavených faktur",
                        price=DefaultPriceEnum.BY_HAND_EVIDENCE if self.evidence_bool.get() else DefaultPriceEnum.BY_HAND_UCTO if self.ucto_bool.get() else DefaultPriceEnum.BY_HAND_NO_DPH)
        self.define_row(text="Počet pokladních dokladů",
                        price=DefaultPriceEnum.REGISTER_EVIDENCE if self.evidence_bool.get() else DefaultPriceEnum.REGISTER_UCTO if self.ucto_bool.get() else DefaultPriceEnum.REGISTER_NO_DPH)
        self.define_row(text="Počet operací provedených platební kartou",
                        price=DefaultPriceEnum.CREDIT_CARD_EVIDENCE if self.evidence_bool.get() else DefaultPriceEnum.CREDIT_CARD_UCTO if self.ucto_bool.get() else DefaultPriceEnum.CREDIT_CARD_NO_DPH)
        self.define_row(text="Počet přijatých faktur",
                        price=DefaultPriceEnum.CREATE_PFA_UCTO if self.ucto_bool.get() else DefaultPriceEnum.CREATE_PFA_EVIDENCE if self.evidence_bool.get() else 0.0)
        self.define_row(text="Počet vystavovaných faktur za klienta",
                        price=DefaultPriceEnum.CREATE_VFA_DPH if self.dph_pay_bool.get() else DefaultPriceEnum.CREATE_VFA_NO_DPH)

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
        self.widgets.append(self.centers)
        self.widgets.append(self.orders)
        self.widgets.append(self.analysis)
        self.widgets.append(self.warehouses)
        self.dph_widgets.append(self.tax_check)
        self.dph_widgets.append(self.send_docs)
        self.no_dph_widgets.append(self.create_dppodpfo)
        self.widgets.append(self.headers)

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
        total = 0.0
        try:
            for subtotal in self.subtotals:
                total += subtotal.get()

            if self.centers_bool.get():
                total *= 1.1
            if self.orders_bool.get():
                total *= 1.1
            if self.analysis_bool.get():
                total *= 1.1
            if self.warehouses_bool.get():
                total *= 1.2

        except ValueError as e:
            total = 0.0
            print(e)

        except TypeError as e:
            total = 0.0
            print(e)

        self.total.set(total)

    def base_checkbox_tick(self, kind: ModeEnum) -> None:
        """
        tracks the 2 base checkboxes and ensures that only one can ever be selected, making them mutually exclusive
        :param kind: which checkbox has been ticked
        :return: None
        """
        match kind:
            case ModeEnum.EVIDENCE:
                self.checkboxes[1].deselect()

            case ModeEnum.UCTO:
                self.checkboxes[0].deselect()

            case _:
                pass

        self.get_total()

    def define_row(self, text : str, evidence_price: Union[DefaultPriceEnum, float], ucto_price: Union[DefaultPriceEnum, float], dph_price: Union[DefaultPriceEnum, float], no_dph_price: Union[DefaultPriceEnum, float]) -> None:
        row = Row(master=self.frame,
                  text=text,
                  ucto_price=ucto_price,
                  evidence_price=evidence_price,
                  dph_price=dph_price,
                  no_dph_price=no_dph_price,
                  evidence_bool=self.evidence_bool,
                  dph_bool=self.dph_pay_bool,
                  ucto_bool=self.ucto_bool)

        row.subtotal_var.trace_add("write", self.get_total)
        self.widgets.append(row)
        self.subtotals.append(row.subtotal_var)