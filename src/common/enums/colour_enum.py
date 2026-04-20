"""Defines the ColourEnum class, containing an enumeration of all colours used in the project."""
from enum import StrEnum


class ColourEnum(StrEnum):
    """Enum containing all colours used within the project."""

    MXB_RED = "#703230"
    DARK_MXB_RED = "#401c1b"
    WHITE = "#FFFFFF"
    LIGHT_MXB_RED = "#ffb3b3"

    def to_hex(self) -> int:
        """Convert enum value to hex code.

        Converts the enum value held in the enum to a hex code of the colour.
        :return: Hex representation of the colour.
        """
        return int(self.value.lstrip("#"), 16)
