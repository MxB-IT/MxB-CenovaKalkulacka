"""Defines the base class for all buttons in the project."""
from typing import Any

from customtkinter import CTkButton, CTkFrame

from src.Common.Enums.placeholder_texts import PlaceholderTexts
from src.Widgets.widgets_base import MXB_RED


class ButtonBase(CTkButton):
    """Base class for all the buttons in this project."""

    def __init__(self,
                 master: CTkFrame,
                 fg_color: str=MXB_RED,
                 border_color: str=MXB_RED,
                 text_color: str="white",
                 text: str=PlaceholderTexts.BUTTON_TEXT,
                 *args: tuple[Any, ...],
                 **kwargs: dict[str, Any]) -> None:
        """Initialise the button.

        Initialises the button with the given arguments modifying its initial appearance
        :param master: master widget
        :param fg_color: colour this should have, defaults to MXB_RED
        :param border_color: colour this button's border should have, defaults to MXB_RED
        :param text_color: colour this button's text should have, defaults to "white"
        :param text: text for the button, defaults to PlaceholderTexts.BUTTON_TEXT
        """
        super().__init__(*args,
                         master=master,
                         fg_color=fg_color,
                         border_color=border_color,
                         text_color=text_color,
                         text=text,
                         **kwargs)
