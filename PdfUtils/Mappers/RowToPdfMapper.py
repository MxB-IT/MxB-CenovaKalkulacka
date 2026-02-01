from dataclasses import dataclass
from Sections.Components.Row import Row

@dataclass
class PDFDataClass:
    name: str
    price: float

class RowToPdfMapper:
    @staticmethod
    def rows_to_dict(rows : list[Row]) -> list[PDFDataClass]:
        output = []
        for row in rows:
            row_data = PDFDataClass(name=row.textbox.get("0.0", "end"),
                                    price=round(row.subtotal_var.get(), 2))
            output.append(row_data)

        return output