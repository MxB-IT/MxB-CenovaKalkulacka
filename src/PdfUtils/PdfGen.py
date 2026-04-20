from src.PdfUtils.PDF import PDF
from src.Sections.Components.row import Row
from src.PdfUtils.Mappers.RowToPdfMapper import RowToPdfMapper, PDFDataClass
import webbrowser

class PdfGen:
    """
    class used as a wrapper for generating PDFs, contains all the necessary methods
    """
    @staticmethod
    def create_pdf(rows: list[Row], non_row_items: list[PDFDataClass], total_price: float, output_path: str) -> None:
        """
        method used to create a PDF file
        :param rows: list of all the Row objects to be taken into account and the data of which should be exported
        :param non_row_items: list of all the items that are taken into account, but are not Row objects, need to be converted into PDFDataClass objects beforehand
        :param total_price: total price calculated for the customer
        :param output_path: where to save the file
        :return: None
        """
        pdf = PDF()
        pdf.add_page()

        table_data = non_row_items
        table_data += RowToPdfMapper.rows_to_dict(rows)

        pdf.construct_table(table_data, total_price)

        pdf.output(f"{output_path}/output.pdf")
        webbrowser.open(f"{output_path}/output.pdf")