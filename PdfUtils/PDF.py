from fpdf import FPDF
from fpdf.fonts import FontFace
from PdfUtils.Mappers.RowToPdfMapper import PDFDataClass
from pathlib import Path

from Widgets.WidgetsBase import MXB_RED


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        try:
            self.add_font('DejaVuSans', '', './Assets/fonts/DejaVuSans.ttf', uni=True)
            self.add_font('DejaVuSans', 'B', './Assets/fonts/DejaVuSans-Bold.ttf', uni=True)
        except:
            self.add_font('DejaVuSans', '', './Assets/fonts/DejaVuSans.ttf')
            self.add_font('DejaVuSans', 'B', './Assets/fonts/DejaVuSans-Bold.ttf')

    def header(self):
        self.image('./Assets/Images/mxbLogo.png', 10, 8, 33)
        self.set_font('DejaVuSans', 'B', 25)
        self.cell(w=0,
                  h=33,
                  text="Souhrn ceny služeb",
                  border=False,
                  align='C')

        self.set_y(50)

    def construct_table(self, data: list[PDFDataClass], total_price: float) -> None:

        self.set_line_width(0.6)
        # ignore editor warn about self.set_draw_color, false flag
        self.set_draw_color(MXB_RED)
        self.set_font('DejaVuSans', '', 15)

        # ignore editor warn about self.set_draw_color, false flag
        header_style = FontFace(emphasis="BOLD",
                                color=(255, 255, 255),
                                fill_color=MXB_RED)

        with (self.table(col_widths=(3, 1),
                         text_align=("LEFT", "RIGHT"),
                         headings_style=header_style,
                         cell_fill_color=(245, 245, 245))
              as table):

            row = table.row()
            row.cell(text='Služba')
            row.cell(text='Cena(CZK)')

            for item in data:
                row = table.row()
                row.cell(text=item.name)
                row.cell(text=f"{item.price:,.2f}")

            self.set_font('DejaVuSans', 'B', 15)
            row = table.row()
            row.cell(text='CENA CELKEM',
                     style=header_style)
            row.cell(text=f"{total_price:,.2f}",
                      style=header_style)