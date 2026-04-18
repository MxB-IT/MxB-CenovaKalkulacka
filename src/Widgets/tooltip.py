"""The tooltip module defines a Tooltip class used for displaying tooltips to the user."""
from typing import Any

from customtkinter import CTkLabel, CTkToplevel

from Errors.gui_error import GUIError


class Tooltip:
    """Class used for displaying tooltips to the user.

    This class is utilised for displaying tooltips to the user whenever they hover over an element
    of the GUI.
    """

    def __init__(self,
                 widget: Any,
                 text: str,
                 delay: int =500) -> None:
        """Initialise the tooltip.

        :param widget: widget for which the tooltip will be shown
        :param text: text the tooltip will display
        :param delay: delay after which the tooltip will appear (in ms)
        """
        self._widget = widget
        self._text: str = text
        self._delay: int = delay
        self._tooltip_window: CTkToplevel | None = None
        self._id = None

        self._widget.bind("<Enter>", self._schedule_tooltip)
        self._widget.bind("<Leave>", self._hide_tooltip)
        self._widget.bind("<ButtonPress>", self._hide_tooltip)

    def _schedule_tooltip(self, event: Any = None) -> None:
        """Schedule tooltip appearance.

        shedules tooltip appearance in the GUI.
        :param event: shoehorned arg, so GUI does not complain about invalid args
        :return: None
        """
        self._id = self._widget.after(self._delay, self._show_tooltip)

    def _show_tooltip(self, event: Any = None) -> None:
        """Show tooltip to the user.

        Calculates the size of the tooltip and its position relative to the parent
        widget
        :return: None
        """
        x = self._widget.winfo_rootx() + 20
        y = self._widget.winfo_rooty() + self._widget.winfo_height() + 5

        self._tooltip_window = CTkToplevel(master=self._widget)
        if not self._tooltip_window:
            raise GUIError(error_code=,
                           error_message="Tooltip window failed to initialise.")

        self._tooltip_window.wm_overrideredirect(boolean=True)
        self._tooltip_window.geometry(f"+{x}+{y}")
        self._tooltip_window.attributes("-topmost", True)

        label = CTkLabel(
            master=self._tooltip_window,
            text=self._text,
            fg_color="#333333",
            text_color="#FFFFFF",
            corner_radius=6,
            font=("Arial", 12),
            padx=10,
            pady=5,
        )
        label.pack()

    def _hide_tooltip(self, event = None) -> None:
        """Hide the tooltip after it is not needed.

        Hides the tooltip, called after user action or timeout.
        :return: None
        """
        if self._id:
            self._widget.after_cancel(self._id)
            self._id = None

        if self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None
