import tkinter as tk
from PdfUtils.PdfGen import PdfGen
from Sections.BaseSection import *
from Sections.AccountingSection import *
from Sections.PayrollSection import *
from Sections.TotalSection import *
from PIL import Image
import os

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

        self._resize_timer = None

        self.grid_rowconfigure(0,
                               weight=1)
        self.grid_columnconfigure(0,
                                  weight=1)

        self.canvas = tk.Canvas(self,
                                borderwidth=0,
                                highlightthickness=0,
                                bg="white")
        self.canvas.grid(row=0,
                         column=0,
                         sticky="nsew")

        self.scrollbar = CTkScrollbar(self,
                                      orientation="vertical",
                                      command=self.canvas.yview)
        self.scrollbar.grid(row=0,
                            column=1,
                            sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = FrameBase(master=self.canvas,
                                          border_width = 2,
                                          border_color = "white")

        self.canvas_window = self.canvas.create_window((0, 0),
                                                       window=self.scrollable_frame,
                                                       anchor="nw")

        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind("<Enter>", self._bind_mouse_scroll)
        self.bind("<Leave>", self._unbind_mouse_scroll)

        self.base_section = BaseSection(self.scrollable_frame, self)
        self.total_section = TotalSection(self.scrollable_frame)
        self.payrolls_section = PayrollSection(self.scrollable_frame, self)
        self.accounting_section = AccountingSection(self.scrollable_frame, self)

        self._setup_sections()
        self.calculate_total()

        self.topbar = CTkFrame(master=self.scrollable_frame,
                               height=60,
                               corner_radius=0,
                               fg_color="#dddddd")

        self.app_title = LabelBase(master=self.topbar,
                                   text="Cenová kalkulačka",
                                   font=("Arial", 20, "bold"))

        self.app_title.pack(side=LEFT)

        self.topbar.grid(row=0,
                         column=0,
                         padx=0,
                         pady=0,
                         columnspan=self.scrollable_frame.grid_size()[0],
                         sticky="ew")

        icon_path = PriceCalc.resource_path("Assets/Images/PDF_file_icon.png")
        pdf_image = Image.open(icon_path)

        pdf_icon = CTkImage(light_image=pdf_image,
                            dark_image=pdf_image,
                            size=(15,20))

        self.export_to_pdf_button = ButtonBase(master=self.topbar,
                                               command=self.export_pdf,
                                               text="",
                                               image=pdf_icon,
                                               bg_color="white",
                                               hover_color="#4d2422",
                                               border_width=0,
                                               corner_radius=0)

        Tooltip(widget=self.export_to_pdf_button,
                text="Export do PDF")

        self.export_to_pdf_button.configure(width=30,
                                            height=30)

        self.export_to_pdf_button.pack(side=RIGHT)

    def _setup_sections(self) -> None:
        """
        sets up all the sections into default positions
        :return: None
        """

        self.base_section.frame.grid(row = 1,
                                     column = 0,
                                     columnspan = 3,
                                     sticky = "ew")
        self.total_section.frame.grid(row = 4,
                                      column = 0,
                                      columnspan = 3,
                                      sticky = "ew")
        self.scrollable_frame.configure(width = self.winfo_width() - 40,
                                        height = self.winfo_height() - 40)
        self.scrollable_frame.rowconfigure((0,4), weight = 1)
        self.scrollable_frame.columnconfigure(0, weight = 1)

    def _bind_mouse_scroll(self, event) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mouse_scroll(self, event) -> None:
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):

        if self._resize_timer:
            self.after_cancel(self._resize_timer)

        self._resize_timer = self.after(150, self._perform_resize, event.width)

    def _perform_resize(self, new_width: int) -> None:
        self.canvas.itemconfig(self.canvas_window,
                               width=new_width)

        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self._resize_timer = None

    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def calculate_total(self, *args) -> None:
        """
        calculates the totals based on all the input data, called upon changes in totals
        :return: None
        """
        try:
            payrolls_total = self.payrolls_section.total.get()
            accounting_total = self.accounting_section.total.get()
            combined_total = payrolls_total + accounting_total

            self.total_section.payrolls_total[1].configure(text = NUMBER_FORMAT % payrolls_total)
            self.total_section.accounting_total[1].configure(text = NUMBER_FORMAT % accounting_total)
            self.total_section.total_price[1].configure(text = NUMBER_FORMAT % combined_total)
        except AttributeError:
            pass

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

    @staticmethod
    def resource_path(relative_path : str) -> str:
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)

    def export_pdf(self):
        rows = []

        for widget in self.accounting_section.widgets:
            if isinstance(widget, Row):
                rows.append(widget)

        for widget in self.payrolls_section.widgets:
            if isinstance(widget, Row):
                rows.append(widget)

        PdfGen.create_pdf(rows, self.accounting_section.export_non_row_items_for_pdf(), float(self.total_section.total_price[1].cget("text")))

if __name__ == "__main__":
    app = PriceCalc()
    app.mainloop()