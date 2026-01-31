from dataclasses import dataclass
from Sections.Components.Row import Row

@dataclass
class RowClass:
    name: str
    price: float

class RowToPdfMapper:
    @staticmethod
    def rows_to_dict(rows : list[Row]) -> list[RowClass]:
        output = []
        for row in rows:
            row_data = RowClass(row.textbox.get("0.0", "end"), round(row.subtotal_var.get(), 2))
            output.append(row_data)

        return output