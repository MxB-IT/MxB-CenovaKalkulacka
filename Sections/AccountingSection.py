import _tkinter
from PdfUtils.Mappers.RowToPdfMapper import PDFDataClass
from Sections.Components.Row import Row
from Sections.SectionBase import *
from Common.DefaultPriceEnum import DefaultPriceEnum
from Common.ModeEnum import ModeEnum
from Widgets.ButtonBase import ButtonBase
from Widgets.Tooltip import Tooltip

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
        self.import_only_bool.trace_add("write", self.get_total)
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
        self.tax_check_amts = []

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
                                         variable=self.import_only_bool),
                            ComboBoxBase(master=self.frame,
                                         values=[str(800), str(1000), str(1200), str(1400), str(1600)],
                                         variable=self.import_only_var))

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

        self.headers = (LabelBase(master=self.frame,
                                  text="Položka"),
                        LabelBase(master=self.frame,
                                  text="Počet"),
                        LabelBase(master=self.frame,
                                  text="Cena")
                        )

        self.setup_widgets()

        bank_amt = IntVar(value=0)
        self.tax_check_amts.append(bank_amt)
        self._define_row(text="Počet položek na bance", evidence_price=DefaultPriceEnum.BANK,
                         ucto_price=DefaultPriceEnum.BANK, dph_price=DefaultPriceEnum.BANK,
                         no_dph_price=DefaultPriceEnum.BANK, amt_var=bank_amt)

        by_hand_amt = IntVar(value=0)
        self.tax_check_amts.append(by_hand_amt)
        self._define_row(text="Počet zaúčtovaných vystavených faktur", evidence_price=DefaultPriceEnum.BY_HAND_EVIDENCE,
                         ucto_price=DefaultPriceEnum.BY_HAND_UCTO, dph_price=0.0,
                         no_dph_price=DefaultPriceEnum.BY_HAND_NO_DPH, amt_var=by_hand_amt)

        register_amt = IntVar(value=0)
        self.tax_check_amts.append(register_amt)
        self._define_row(text="Počet pokladních dokladů", evidence_price=DefaultPriceEnum.REGISTER_EVIDENCE,
                         ucto_price=DefaultPriceEnum.REGISTER_UCTO, dph_price=0.0,
                         no_dph_price=DefaultPriceEnum.REGISTER_NO_DPH, amt_var=register_amt)

        self._define_row(text="Počet operací provedených platební kartou",
                         evidence_price=DefaultPriceEnum.CREDIT_CARD_EVIDENCE,
                         ucto_price=DefaultPriceEnum.CREDIT_CARD_UCTO, dph_price=0.0,
                         no_dph_price=DefaultPriceEnum.CREDIT_CARD_NO_DPH)

        self._define_row(text="Počet přijatých faktur", evidence_price=DefaultPriceEnum.CREATE_PFA_EVIDENCE,
                         ucto_price=DefaultPriceEnum.CREATE_PFA_UCTO, dph_price=0.0, no_dph_price=0.0)

        vfa_amt = IntVar(value=0)
        self.tax_check_amts.append(vfa_amt)
        self._define_row(text="Počet vystavovaných faktur za klienta", evidence_price=0.0, ucto_price=0.0,
                         dph_price=DefaultPriceEnum.CREATE_VFA_DPH, no_dph_price=DefaultPriceEnum.CREATE_VFA_NO_DPH,
                         amt_var=vfa_amt)

        self.arrange_widgets(self.frame, self.widgets[:2] + self.no_dph_widgets + self.widgets[2:])

        self.add_row_button=ButtonBase(master=self.frame,
                                       text="+",
                                       command=self._add_row)

        Tooltip(widget=self.add_row_button,
                text="Přidá další řádek s položkou, která bude do finálního výpočtu připočítána")

        self.add_row_button.grid(row=self.frame.grid_size()[1] + 1,
                                 column=0,
                                 columnspan=self.frame.grid_size()[0],
                                 sticky="ew",
                                 padx=10,
                                 pady=10)

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
        self.add_row_button.grid_forget()

        for widget in self.frame.grid_slaves():
            widget.grid_forget()

        if self.dph_pay_bool.get():
            #disgusting hack
            self.arrange_widgets(self.frame, self.widgets[:2] + self.dph_widgets + self.widgets[2:])
        else:
            #disgusting hack
            self.arrange_widgets(self.frame, self.widgets[:2] + self.no_dph_widgets + self.widgets[2:])

        self.add_row_button.grid(row=self.frame.grid_size()[1] + 1,
                                 column=0,
                                 columnspan=self.frame.grid_size()[0],
                                 sticky="ew",
                                 padx=10,
                                 pady=10)

        self.get_total()

    def get_total(self, *args) -> None:
        """
        gets the total of all the widgets within the section
        :return: None, updates an internal section total
        """
        total = 0.0
        try:
            for subtotal in self.subtotals:
                try:
                    total += subtotal.get()
                except _tkinter.TclError:
                    total += 0.0

            if self.import_only_bool.get():
                try:
                    total += self.import_only_var.get()
                except _tkinter.TclError:
                    total += 0.0

            if self.dph_pay_bool.get():
                if self.send_docs_bool.get():
                    total += DefaultPriceEnum.SEND_DOCS

                if self.tax_check_bool.get():
                    total_amts = sum(var.get() for var in self.tax_check_amts)

                    if total_amts < 300:
                        total+= 500
                    elif 300 <= total_amts < 500:
                        total += 700
                    elif 500 <= total_amts < 1000:
                        total += 1000
                    else:
                        total += 2000

                if self.dph_pay_bool.get():
                    total *= 7/6

            else:
                if self.dppodpfo_bool.get():
                    total += DefaultPriceEnum.DPPO_DPFO

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

    def _define_row(self, text : str, evidence_price: Union[DefaultPriceEnum, float], ucto_price: Union[DefaultPriceEnum, float], dph_price: Union[DefaultPriceEnum, float], no_dph_price: Union[DefaultPriceEnum, float], amt_var: IntVar = None) -> None:
        """
        method used to define each row with an interactible price and amount of items to be calculated
        :param text: text to be displayed in the textbox next to the row
        :param evidence_price: price for evidence (optional, if left out, defaults to 0)
        :param ucto_price: price for ucto (optional, if left out, defaults to 0)
        :param dph_price: price for dph payers (optional, if left out, defaults to 0)
        :param no_dph_price: price for no pay of dph (optional, if left out, defaults to 0)
        :param amt_var: optional variable to let the section track the amount in this row (optional, if left out, defaults to 0)
        :return: None
        """
        row = Row(master=self.frame,
                  text=text,
                  ucto_price=ucto_price,
                  evidence_price=evidence_price,
                  dph_price=dph_price,
                  no_dph_price=no_dph_price,
                  evidence_bool=self.evidence_bool,
                  dph_bool=self.dph_pay_bool,
                  ucto_bool=self.ucto_bool,
                  amt_var = amt_var,
                  on_delete_callback=self.row_delete_callback)

        row.subtotal_var.trace_add("write", self.get_total)
        self.widgets.append(row)
        self.subtotals.append(row.subtotal_var)

    def _add_row(self) -> None:
        """
        method used for creating new rows during runtime when the user wants to add them
        :return: None
        """
        self.add_row_button.grid_forget()

        row = Row(master=self.frame,
                  on_delete_callback=self.row_delete_callback)

        row.subtotal_var.trace_add("write", self.get_total)
        self.widgets.append(row)
        self.subtotals.append(row.subtotal_var)

        row.grid(row=self.frame.grid_size()[1] + 1,
                 column=0,
                 columnspan=self.frame.grid_size()[0],
                 sticky="ew",
                 padx=10,
                 pady=10)

        self.add_row_button.grid(row=self.frame.grid_size()[1] + 1,
                                 column=0,
                                 columnspan=self.frame.grid_size()[0],
                                 sticky="ew",
                                 padx=10,
                                 pady=10)

    def row_delete_callback(self, deleted_row: Row) -> None:
        """
        callback used when the user deletes a row, ensuring frame forgetting the row and the button for adding a new row
        :param deleted_row: an instance of the row class that is about to be deleted
        :return: None
        """

        if deleted_row.subtotal_var in self.subtotals:
            self.subtotals.remove(deleted_row.subtotal_var)

        self.get_total()

        try:
            deleted_row_index = int(deleted_row.grid_info()["row"])
        except _tkinter.TclError:
            deleted_row_index = 9999

        if deleted_row in self.widgets:
            self.widgets.remove(deleted_row)

        for widget in self.widgets:
            if isinstance(widget, (list, tuple)):
                continue

            try:
                current_row = int(widget.grid_info()["row"])
            except _tkinter.TclError:
                continue

            if current_row > deleted_row_index:
                widget.grid(row=current_row - 1,
                            column=0,
                            columnspan=self.frame.grid_size()[0],
                            sticky="ew",
                            padx=10,
                            pady=10)

    def export_non_row_items_for_pdf(self) -> list[PDFDataClass]:
        for widget in self.widgets:
            if not isinstance(widget, Row):
