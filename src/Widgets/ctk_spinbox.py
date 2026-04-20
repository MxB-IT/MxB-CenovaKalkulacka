"""Defines the spinbox base class for all spinboxes in this project."""
from collections.abc import Callable
from tkinter import DoubleVar, IntVar, StringVar
from typing import Any

from customtkinter import CTkButton, CTkEntry, CTkFrame
from src.Common.Enums. colour_enum import ColourEnum


class CTkSpinbox(CTkFrame):
    """Base class for al the spinboxes in this project."""

    def __init__(
        self,
        *args: tuple[Any, ...],
        width: int = 100,
        height: int = 32,
        step_size: float = 1,
        variable: DoubleVar | IntVar | None = None,
        command: Callable | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        """Initialise the spinbox base class.

        Initialises the spinbox based on the passed arguments, since there is no CTkSpinbox at the
        time of making this app, this class inherits from CTkFrame.
        :param args: Any positional arguments applicable to CTkFrame.
        :param width: Desired width of the spinbox in px, defaults to 100.
        :param height: Desired height of the spinbox in px, defaults to 32.
        :param step_size: Step size for how much the value within the spinbox should change when a
        + or - button is pressed.
        :param variable: Variable held inside the spinbox, defaults to None if no var is passed in.
        :param command: Callback command for when a button is pressed.
        :param kwargs: Any keyword arguments applicable to CTkFrame.
        :return: None
        """
        super().__init__(*args, width=width, height=height, **kwargs)

        self.display_var = StringVar()

        if variable is not None and variable.get() != 0:
            self.display_var.set(str(int(round(variable.get(), 0))))

        self.display_var.trace_add("write", self._on_display_var_change)

        self.step_size = step_size
        self.command = command

        self.variable = variable or DoubleVar(value=0)
        self.variable.trace_add("write", self._on_var_change)

        self.configure(fg_color=ColourEnum.MXB_RED)
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.subtract_button = CTkButton(
            self,
            text="-",
            width=height - 6,
            height=height - 6,
            command=self.subtract_button_callback,
            fg_color="white",
            hover_color="#ffbfbf",
            text_color=ColourEnum.MXB_RED,
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = CTkEntry(
            self,
            width=width - 2 * height,
            height=height - 6,
            border_width=0,
            textvariable=self.display_var,
        )
        self.entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTkButton(
            self,
            text="+",
            width=height - 6,
            height=height - 6,
            command=self.add_button_callback,
            fg_color="white",
            hover_color="#bfffcc",
            text_color=ColourEnum.MXB_RED,
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

    def _on_var_change(self, name: str, index: str, mode: str) -> None:
        """React to internal variable change.

        Callback method reacting to a change in the value of the variable held by the spinbox.
        :param name: Name of the variable being changed.
        :param index: Index of the variable being changed in case it is a list-like.
        :param mode: What happened to the variable (e.g. write).
        :return: None
        """
        if self.variable.get() <= 0:
            self.display_var.set("")
            self.variable.set(0)

        else:
            self.display_var.set(str(int(round(self.variable.get(), 0))))

        if self.command:
            self.command()

    def _on_display_var_change(self, name: str, index: str, mode: str) -> None:
        """React to display variable change.

        Callback method reacting to the changes made to the variable displayed by the spinbox.
        :param name: Name of the variable being changed.
        :param index: Index of the variable being changed in case it is a list-like.
        :param mode: What happened to the variable (e.g. write).
        :return: None
        """
        if not self.display_var.get().isnumeric():
            self.variable.set(0)
        elif isinstance(self.variable, IntVar):
            self.variable.set(int(self.display_var.get()))
        elif isinstance(self.variable, DoubleVar):
            self.variable.set(float(self.display_var.get()))

    def add_button_callback(self) -> None:
        """React to the + button.

        Callback method reacting to the user clicking the + button by incrementing the internal
        variable held by the spinbox.
        """
        try:
            if isinstance(self.variable, IntVar):
                self.variable.set(int(self.variable.get() + self.step_size))
            elif isinstance(self.variable, DoubleVar):
                self.variable.set(float(self.variable.get() + self.step_size))
        except Exception:
            self.variable.set(0)

    def subtract_button_callback(self) -> None:
        """React to the - button.

        Callback method reacting to the user clicking the - button by decrementing the internal
        variable held by the spinbox.
        :return: None
        """
        try:
            if isinstance(self.variable, IntVar):
                self.variable.set(int(self.variable.get() - self.step_size))
            elif isinstance(self.variable, DoubleVar):
                self.variable.set(float(self.variable.get() - self.step_size))
        except Exception:
            self.variable.set(0)

    def get(self) -> int | float:
        """Get the variable held by the spinbox."""
        return self.variable.get()

    def set(self, value: float) -> None:
        """Set the internal variable held by the spinbox to a certain value."""
        if isinstance(self.variable, IntVar):
            self.variable.set(int(value))
        elif isinstance(self.variable, DoubleVar):
            self.variable.set(float(value))

    def base_checkbox_tick(self, checkbox_kind: str) -> None:
        """React to the tick of a specific checkbox.

        Reacts to a checkbox for selecting a general category getting unticked, meaning other
        checkboxes should get unticked in reaction to hide a category.
        :param checkbox_kind: The kind of checkbox that has been ticked, this method should only
        react to a certain one.
        """
        if checkbox_kind == "Evidence":
            self.checkboxes[1].deselect()
        else:
            self.checkboxes[0].deselect()
        self.get_total()
