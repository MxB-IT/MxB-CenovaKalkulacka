
import tkinter as tk
from pathlib import Path
from tkinter import LEFT, RIGHT, Event
from typing import Any

from customtkinter import CTk, CTkFrame, CTkImage, CTkScrollbar
from future.moves.tkinter import filedialog
from PIL import Image

from src.pdf_utils.pdf_gen import PdfGen
from src.scripts.resource_pather import ResourcePather
from src.sections.accounting_section import AccountingSection
from src.sections.base_section import BaseSection
from src.sections.components.row import Row
from src.sections.payroll_section import PayrollSection
from src.sections.total_section import TotalSection
from src.widgets.button_base import ButtonBase
from src.widgets.frame_base import FrameBase
from src.widgets.label_base import LabelBase
from src.widgets.tooltip import Tooltip

NUMBER_FORMAT = "%.0f"

class PriceCalc(CTk):
    """Price calculator app class, handles mainly GUI operations."""

    def __init__(self) -> None:
        """Initialise the PriceCalc class.

        Initialises the PriceCalc class, which includes setting up all the sections and pdf
        generation.
        """
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

        icon_path = ResourcePather.resource_path("assets/Images/PDF_file_icon.png")
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
        """Set up all sections.

        Sets up all the sections into default positions.
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

    def _bind_mouse_scroll(self,
                           event: Event) -> None:
        """Bind mouse scroll to scrolling in the app.

        Method used to bind the mouse scrollwheel to scrolling through the app.
        :param event: Unused.
        :return: None
        """
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mouse_scroll(self,
                             event: Event) -> None:
        """Unbind mouse scroll from scrolling in the app.

        method used to unbind the mouse scrollwheel from scrolling through the app, used when the
        user's mouse pointer exits the app.
        :param event: Unused.
        :return: None
        """
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_frame_configure(self,
                            event: Event) -> None:
        """Respond to the resize of the app window.

        Method used to redefine the scrollregion whenever the app is resized to have it actually
        correspond with where the app is visually.
        :param event: Unused.
        :return: None
        """
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def _on_canvas_configure(self,
                             event: Event) -> None:
        """Respon to resuze of the app window.

        Method used to delay recalculating the widget and GUI elements sizes and parameters
        until the user has stopped resizing the app, helps with lag significantly.
        :param event: Event descriptor, containing information about the user's action.
        :return: None
        """
        if self._resize_timer:
            self.after_cancel(self._resize_timer)

        self._resize_timer = self.after(150, self._perform_resize, event.width)

    def _perform_resize(self, new_width: int) -> None:
        """Resize app.

        Method used to manually resize the app, after the user is done modifying the window size.
        :param new_width: new width of the app
        :return: None
        """
        self.canvas.itemconfig(self.canvas_window,
                               width=new_width)

        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self._resize_timer = None

    def _on_mousewheel(self,
                       event: Event) -> None:
        """Respond to scrolling the mousewheel.

        Method used to catch the movement of the mousewheel and react accordingly.
        :param event: Event descriptor, containing information about the user's action.
        :return: None
        """
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def calculate_total(self,
                        *args: tuple[Any, ...]) -> None:
        """Calculate the grand total for the service prices.

        Calculates the totals based on all the input data, called upon changes in totals.
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
    def toggle_relevant(toggle_bool: bool,
                        section: AccountingSection | PayrollSection | TotalSection | BaseSection,
                        offset: int) -> None:
        """Toggle the relevant section.

        Toggles relevant sections of the app based on user input (clicking base checkboxes).
        :param toggle_bool: Toggle deciding whether to turn a widget on or off.
        :param section: Section to toggle.
        :param offset: Offset at which to toggle said section.
        :return: None
        """
        if toggle_bool:
            section.frame.grid(row = offset,
                               column = 0,
                               columnspan = 2,
                               sticky = "ew")
        else:
            section.frame.grid_forget()

    def export_pdf(self) -> None:
        """Export data in the app into a PDF file.

        Method used to export all the data within the calculator app into a PDF format.
        :return: None
        """
        rows = [w for w in self.payrolls_section.widgets if isinstance(w, Row)]
        rows.extend([w for w in self.accounting_section.widgets if isinstance(w, Row)])

        output_folder: Path = Path(filedialog.askdirectory(initialdir=Path.cwd()))

        if output_folder == "":
            output_folder = Path.cwd()

        PdfGen.create_pdf(rows,
                          self.accounting_section.export_non_row_items_for_pdf(),
                          float(self.total_section.total_price[1].cget("text")),
                          output_folder)
