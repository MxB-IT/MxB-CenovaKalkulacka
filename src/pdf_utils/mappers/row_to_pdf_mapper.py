from dataclasses import dataclass

from src.sections.components.row import Row


@dataclass
class PDFDataClass:
    """Class serving as a data holder for exported PDF file."""

    name: str
    price: float

class RowToPdfMapper:
    """Class serving as a mapper of Row objects to PDFDataClasses."""

    @staticmethod
    def rows_to_dict(rows : list[Row]) -> list[PDFDataClass]:
        """Convert a list of Row objects into a list of PDFDataClasses.

        Static method used to convert a list of rows into a list o PDFDataClasses.
        :param rows: List of Row objects to be converted.
        :return: List of PDFDataClasses containing the Row's description text and the calculated
        price for the row.
        """
        output = []
        for row in rows:
            row_data = PDFDataClass(name=row.textbox.get("0.0", "end"),
                                    price=round(row.subtotal_var.get(), 2))
            output.append(row_data)

        return output
