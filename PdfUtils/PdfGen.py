from PdfUtils.PDF import PDF
from Sections.Components.Row import Row
from PdfUtils.Mappers.RowToPdfMapper import RowToPdfMapper, PDFDataClass


class PdfGen:
    @staticmethod
    def create_pdf(rows: list[Row], non_row_items: list[PDFDataClass], total_price: float) -> None:
        pdf = PDF()
        pdf.add_page()

        table_data = non_row_items
        table_data += RowToPdfMapper.rows_to_dict(rows)

        pdf.construct_table(table_data, total_price)

        pdf.output("output.pdf")