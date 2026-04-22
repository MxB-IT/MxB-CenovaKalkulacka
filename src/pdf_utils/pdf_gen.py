"""Defines the class used for generating PDF files."""
import webbrowser
from pathlib import Path

from src.pdf_utils.mappers.row_to_pdf_mapper import PDFDataClass, RowToPdfMapper
from src.pdf_utils.pdf import PDF
from src.sections.components.row import Row


class PdfGen:
    """Class used as a wrapper for generating PDFs, contains all the necessary methods."""

    @staticmethod
    def create_pdf(rows: list[Row],
                   client_name: str,
                   non_row_items: list[PDFDataClass],
                   total_price: float,
                   output_path: Path) -> None:
        """Create a new pdf file with data passed as args.

        Method used to create a PDF file.
        :param rows: List of all the Row objects to be taken into account and the data of which
        should be exported.
        :param client_name: Name of the client the PDF is for.
        :param non_row_items: List of all the items that are taken into account, but are not Row
        objects, need to be converted into PDFDataClass objects beforehand.
        :param total_price: Total price calculated for the customer.
        :param output_path: Where to save the file.
        :return: None
        """
        pdf: PDF = PDF(client_name)
        pdf.add_page()

        table_data: list[PDFDataClass] = non_row_items
        table_data.extend(RowToPdfMapper.rows_to_dict(rows))

        pdf.construct_table(table_data, total_price)

        pdf.output(f"{output_path}/output.pdf")
        webbrowser.open(f"{output_path}/output.pdf")
