"""Defines the base class for all Frames within the project."""
from tkinter import Canvas
from typing import Any

from customtkinter import CTkFrame

from src.Common.Enums.colour_enum import ColourEnum


class FrameBase(CTkFrame):
    """Base class for all Frames within the project."""

    def __init__(
        self,
        *args: tuple[Any, ...],
        master: CTkFrame | Canvas,
        fg_color: ColourEnum = ColourEnum.WHITE,
        border_color: str = ColourEnum.MXB_RED,
        border_width: int = 2,
        **kwargs: dict[str, Any],
    ) -> None:
        """Initialise the Frame.

        Initialises the Frame with passed arguments.
        :param args: Positional arguments for the CTkFrame parent class.
        :param master: Master widget.
        :param fg_color: Colour of the Frame.
        :param border_color: Border colour of the Frame.
        :param border_width: Border width of the Frame.
        :param kwargs: Keyword arguments for the CTkFrame parent class.
        :return: None
        """
        super().__init__(
            *args,
            master,
            fg_color=fg_color,
            border_color=border_color,
            border_width=border_width,
            **kwargs,
        )
