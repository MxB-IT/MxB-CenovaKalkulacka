from Sections.BaseSection import *
from Sections.AccountingSection import *
from Sections.PayrollSection import *
from Sections.TotalSection import *

NUMBER_FORMAT = "%.0f"
MXB_RED = "#703230"

class PriceCalc(CTk):
    """
    price calculator app class
    handles the entire app operations
    """
    def __init__(self):
        super().__init__()
        self.geometry("400x600")
        self.title("Cenová kalkulačka")
        self.scrollable_frame = CTkScrollableFrame(master=self,
                                                   border_width = 2,
                                                   border_color = "white")
        self.scrollable_frame.grid(row=0,
                                   column=0,
                                   padx=10,
                                   pady=10,
                                   sticky="nsew")

        self.grid_rowconfigure(index=0,
                               weight=1)
        self.grid_columnconfigure(index=0,
                                  weight=1)

        self.base_section = BaseSection(self.scrollable_frame, self)
        self.total_section = TotalSection(self.scrollable_frame)
        self.payrolls_section = PayrollSection(self.scrollable_frame, self)
        self.accounting_section = AccountingSection(self.scrollable_frame, self)

        self._setup_sections()
        self.calculate_total()

    def _setup_sections(self) -> None:
        """
        sets up all the sections into default positions
        :return: None
        """

        self.base_section.frame.grid(row = 0,
                                     column = 0,
                                     columnspan = 3,
                                     sticky = "ew")
        self.total_section.frame.grid(row = 3,
                                      column = 0,
                                      columnspan = 3,
                                      sticky = "ew")
        self.update()
        self.scrollable_frame.configure(width = self.winfo_width() - 40,
                                        height = self.winfo_height() - 40)
        self.scrollable_frame.rowconfigure((0,4), weight = 1)
        self.scrollable_frame.columnconfigure(0, weight = 1)

    def calculate_total(self, *args) -> None:
        """
        calculates the totals based on all the input data, calls itself every 100ms (subject to change)
        :return: None
        """
        try:
            self.total_section.payrolls_total[1].configure(text = NUMBER_FORMAT % self.payrolls_section.total.get())
            self.total_section.accounting_total[1].configure(text = NUMBER_FORMAT % self.accounting_section.total.get())
            self.total_section.total_price[1].configure(text = NUMBER_FORMAT % (self.payrolls_section.total.get() + self.accounting_section.total.get()))
        except AttributeError:
            print("AttributeError on init FIX ASAP")

    @staticmethod
    def toggle_relevant(toggle_bool, section, offset) -> None:
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