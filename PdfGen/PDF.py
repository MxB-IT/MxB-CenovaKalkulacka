from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.image('../Assets/Images/mxbLogo.png', 10, 8, 33)
        self.set_font('helvetica', 'B', 15)
        self.cell(80)
        self.cell(w=0,
                  h=10,
                  text="Souhrn ceny služeb",
                  border=False,
                  align='C')

    def construct_table(self, data: list, total_price: float) -> None:
        with self.table(col_widths=(3, 1), text_align=("LEFT", "RIGHT")) as table:
            row = table.row()
            row.cell('Služba')
            row.cell('Cena(CZK)')

            for item in data:
                row = table.row()
                row.cell(item['name'])
                row.cell(f"${item['price']:,.2f}")

        row = table.row()
        row.cell('CENA CELKEM', align='R')
        row.cell(f"${total_price:,.2f}")