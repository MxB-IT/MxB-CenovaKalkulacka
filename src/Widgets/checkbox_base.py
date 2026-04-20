"""Defines the base class for all checkboxes in this project."""
from typing import Any

from customtkinter import CTkCheckBox, CTkFrame

from src.Common.Enums.colour_enum import ColourEnum


class CheckBoxBase(CTkCheckBox):
    """Serves as the base class for all checkboxes in this project."""

    def __init__(self,
                 *args: tuple[Any, ...],
                 master: CTkFrame,
                 fg_color: ColourEnum = ColourEnum.MXB_RED,
                 border_color: ColourEnum = ColourEnum.MXB_RED,
                 text_color: ColourEnum = ColourEnum.MXB_RED,
                 hover_color: ColourEnum = ColourEnum.MXB_RED,
                 **kwargs: Any) -> None:
        """Initialise the Checkbox with the passed arguments.

        Initialises the Checkbox and modifies its appearance based on the arguments passed.
        :param master: Master widget for the checkbox.
        :param fg_color: Colour for the checkbox, defaults to MXB_RED.
        :param border_color: Colour for the border of the checkbox, defaults to MXB_RED.
        :param text_color: Colour for the text displayed with the checkbox, defaults to MXB_RED.
        :param hover_color: Colour for the checkbox when hovered over, defaults to MXB_RED.
        :return: None
        """
        super().__init__(*args,
                         master,
                         hover_color = hover_color,
                         fg_color = fg_color,
                         border_color = border_color,
                         text_color = text_color,
                         **kwargs)
