"""Defines a class used to hold the PDF definition."""
from fpdf import FPDF
from fpdf.fonts import FontFace

from src.common.enums.colour_enum import ColourEnum
from src.pdf_utils.mappers.row_to_pdf_mapper import PDFDataClass
from src.scripts.resource_pather import ResourcePather


class PDF(FPDF):
    """Container for the PDF file, contains styling and data layout definitions."""

    def __init__(self, client_name: str) -> None:
        """Initialise the PDF class.

        Initialises the PDF class, defining its fonts and the header.
        """
        super().__init__()
        font_path: str = ResourcePather.resource_path("./assets/fonts/DejaVuSans.ttf")
        bold_font_path: str = ResourcePather.resource_path("./assets/fonts/DejaVuSans-Bold.ttf")
        self.client_name: str = client_name
        try:
            self.add_font("DejaVuSans", "", font_path, uni=True)
            self.add_font("DejaVuSans", "B", bold_font_path, uni=True)
        except Exception:
            self.add_font("DejaVuSans", "", font_path)
            self.add_font("DejaVuSans", "B", bold_font_path)

    def header(self) -> None:
        """Define the header of a PDF page, overriding definition in FPDF.

        Defines the header of the PDF pages.
        :return: None
        """
        img_path = ResourcePather.resource_path("./assets/Images/mxbLogo.png")
        self.image(img_path, 10, 8, 33)
        self.set_font("DejaVuSans", "B", 25)
        self.cell(w=0,
                  h=33,
                  text=self.client_name,
                  border=False,
                  align="C")

        self.set_y(50)

    def construct_table(self,
                        data: list[PDFDataClass],
                        total_price: float) -> None:
        """Construct a table of the data provided as an argument.

        Method used to construct a table of all the data to be exported from the calculator (rows
        with names and prices).
        :param data: List of PDFDataClass objects with all the relevant data.
        :param total_price: Total price of all services.
        :return: None
        """
        self.set_line_width(0.6)
        self.set_draw_color(ColourEnum.MXB_RED.to_hex())
        self.set_font("DejaVuSans", "", 15)

        header_style = FontFace(emphasis="BOLD",
                                color=(255, 255, 255),
                                fill_color=ColourEnum.MXB_RED.to_hex())

        with (self.table(col_widths=(3, 1),
                         text_align=("LEFT", "RIGHT"),
                         headings_style=header_style,
                         cell_fill_color=(245, 245, 245))
              as table):

            row = table.row()
            row.cell(text="Služba")
            row.cell(text="Cena(CZK)")

            for item in data:
                row = table.row()
                row.cell(text=item.name)
                row.cell(text=f"{item.price:,.2f}")

            self.set_font("DejaVuSans", "B", 15)
            row = table.row()
            row.cell(text="CENA CELKEM",
                     style=header_style)
            row.cell(text=f"{total_price:,.2f}",
                      style=header_style)
