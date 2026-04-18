"""Defines the base class for all the labels within the project."""
from typing import Any

from customtkinter import CTkFrame, CTkLabel, CTkToplevel

from src.Widgets.widgets_base import MXB_RED


class LabelBase(CTkLabel):
    """Base class for all labels within the project."""

    def __init__(
            self,
            *args: tuple[Any, ...],
            master: CTkFrame | CTkToplevel,
            text_color: str = MXB_RED,
            **kwargs: dict[str, Any],
    ) -> None:
        """Initialise the Label.

        Initialises the label with the passed arguments.
        :param args: Positional arguments for the parent CTkLabel class.
        :param master: Master widget.
        :param text_color: Colour for the text held by the label.
        :param kwargs: Keyword arguments for the parent CTkLabel class.
        """
        super().__init__(
            *args,
            master,
            text_color=text_color,
            **kwargs)
