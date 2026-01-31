from PdfUtils.PDF import PDF
from Sections.Components.Row import Row
from PdfUtils.Mappers.RowToPdfMapper import RowToPdfMapper

class PdfGen:
    @staticmethod
    def create_pdf(rows: list[Row], total_price: float) -> None:
        pdf = PDF()
        pdf.add_page()

        row_data = RowToPdfMapper.rows_to_dict(rows)

        pdf.construct_table(row_data, total_price)

        pdf.output("output.pdf")