from dataclasses import dataclass
from src.Sections.Components.row import Row

@dataclass
class PDFDataClass:
    """
    class serving as a data holder for exported PDF file
    """
    name: str
    price: float

class RowToPdfMapper:
    """
    class serving as a mapper of Row objects to PDFDataClasses, taking text from the Row object's textbox and price from its subtotal
    """
    @staticmethod
    def rows_to_dict(rows : list[Row]) -> list[PDFDataClass]:
        """
        static method used to convert a list of rows into a list o PDFDataClasses
        :param rows: list of Row objects to be converted
        :return: list of PDFDataClasses containing the Row's description text and the calculated price for the row
        """
        output = []
        for row in rows:
            row_data = PDFDataClass(name=row.textbox.get("0.0", "end"),
                                    price=round(row.subtotal_var.get(), 2))
            output.append(row_data)

        return output