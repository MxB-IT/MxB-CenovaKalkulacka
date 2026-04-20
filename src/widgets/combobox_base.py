"""Defines the base class for all comboboxes in this project."""
from typing import Any

from customtkinter import CTkComboBox, CTkFrame

from src.common.enums.colour_enum import ColourEnum


class ComboBoxBase(CTkComboBox):
    """The base class for all comboboxes in this project."""

    def __init__(self,  # noqa: PLR0913
                 *args: tuple[Any, ...],
                 master: CTkFrame,
                 border_color: ColourEnum = ColourEnum.DARK_MXB_RED,
                 fg_color: ColourEnum = ColourEnum.WHITE,
                 dropdown_fg_color: ColourEnum = ColourEnum.WHITE,
                 button_color: ColourEnum = ColourEnum.DARK_MXB_RED,
                 text_color: ColourEnum = ColourEnum.MXB_RED,
                 dropdown_text_color: ColourEnum = ColourEnum.MXB_RED,
                 dropdown_hover_color: ColourEnum = ColourEnum.LIGHT_MXB_RED,
                 border_width: int = 2,
                 button_hover_color: ColourEnum = ColourEnum.LIGHT_MXB_RED,
                 **kwargs: Any) -> None:
        """Initialise the Combobox.

        Initialises the combobox based on the given parameters.
        :param args: Any positional arguments applicable to CTkComboBox.
        :param master: Master widget.
        :param border_color: Colour for the combobox border, defaults to "#401c1b".
        :param fg_color: Colour for the combobox, defaults to white.
        :param dropdown_fg_color: Colour for the combobox dropdown menu, defaults to white.
        :param button_color: Colour for the combobox buttons, defaults to "#401c1b".
        :param text_color: Colour for the text displayed with the combobox, defaults to MXB_RED.
        :param dropdown_text_color: Colour for the text displayed in the dropdown menu, defaults to
        MXB_RED.
        :param dropdown_hover_color: Colour for a dropdown menu item when hovered over, defaults to
        "#ffb3b3".
        :param border_width: Width of the combobox border in px, defaults to 2.
        :param button_hover_color: Colour for the combobox buttons when hovered over, defaults to
        "ffb3b3".
        :param kwargs: Any additional keyword arguments applicable to CTkCombobox.
        :return None
        """
        super().__init__(*args,
                         master,
                         border_color=border_color,
                         fg_color=fg_color,
                         dropdown_fg_color=dropdown_fg_color,
                         button_color=button_color,
                         text_color=text_color,
                         dropdown_text_color=dropdown_text_color,
                         border_width=border_width,
                         dropdown_hover_color=dropdown_hover_color,
                         button_hover_color=button_hover_color,
                         **kwargs)
