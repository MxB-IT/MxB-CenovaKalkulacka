"""Defines the base class for all textboxes within the project."""
from typing import Any

from customtkinter import CTkFrame, CTkTextbox

from src.common.enums.colour_enum import ColourEnum
from src.common.enums.placeholder_texts import PlaceholderTexts
from src.common.enums.scrollbar_activation import ScrollbarActivation


class TextBoxBase(CTkTextbox):
    """Base class for all textboxes within the project."""

    def __init__(self,  # noqa: PLR0913
                 master: CTkFrame,
                 border_color: ColourEnum = ColourEnum.DARK_MXB_RED,
                 fg_color: str = "transparent",
                 text_color: ColourEnum = ColourEnum.MXB_RED,
                 wrap: str = "word",
                 height: int = 35,
                 activate_scrollbars: ScrollbarActivation = ScrollbarActivation.ACTIVE,
                 border_width: int = 0,
                 text: PlaceholderTexts | str = PlaceholderTexts.DESCRIPTION,
                 *args: tuple[Any, ...],
                 **kwargs: Any) -> None:
        """Initialise the textbox widget.

        Initialises a textbox widget with the passed arguments forming its behaviour.
        :param master: Master widget.
        :param border_color: Border colour for the textbox, defaults to "401c1b".
        :param fg_color: Colour for the background of the textbox when it is in focus,
        defaults to transparent.
        :param text_color: Colour for the text held by the textbox widget, defaults to
        MXB_RED.
        :param wrap: Wrap mode, defining how the textbox should wrap text that is too
        long to be displayed on a single line, defaults to word.
        :param height: Height of the textbox in px, defaults to 35.
        :param activate_scrollbars: Indicates whether scrollbars should be present in
        the textbox, defaults to False.
        :param border_width: Border width for the textbox in px, defaults to 0.
        :param text: Text to display in the textbox, defaults to PlaceholderTexts.DESCRIPTION.
        :return: None
        """
        super().__init__(*args,
                         master,
                         border_color=border_color,
                         fg_color=fg_color,
                         text_color=text_color,
                         wrap=wrap,
                         height=height,
                         activate_scrollbars=bool(activate_scrollbars),
                         border_width=border_width,
                         **kwargs)
        self.colour: ColourEnum | str = fg_color

        self._resize_timer = None

        self.insert(0.0, text)

        self.after(100, self.update_height)

        self.configure(state = "disabled")
        self.editing = False

        self.bind("<Double-Button-1>", self.start_edit)
        self.bind("<Return>", self.stop_edit)
        self.bind("<FocusOut>", self.stop_edit)
        self.bind("<Shift-Return>", self.add_newline)
        self.bind("<Configure>", self.on_resize)

    def start_edit(self, event: Any = None) -> None:
        """Set the textbox into editable mode.

        Switches the textbox from behaving like a label to behaving like an editable textbox
        :param event: Arg shoehorned in, so customtkinter doesn't complain.
        :return: None
        """
        self.configure(state="normal",
                       border_color=ColourEnum.MXB_RED,
                       border_width=2,
                       fg_color="#b39998")
        self.focus_set()

    def stop_edit(self, event: Any = None) -> None:
        """Set the text for the textbox and switch it into non-editable mode.

        Saves the current text held within the textbox and switches its behaviour from being
        editable into behaving like a static label.
        :param event: Arg shoehorned in, so customtkinter doesn't complain.
        :return: None
        """
        self.configure(state="disabled",
                       border_width=0,
                       fg_color=self.colour)

    def add_newline(self, event: Any = None) -> None:
        #TODO
        pass

    def update_height(self) -> None:
        """Update height of the widget based on text within.

        Updates the height of the widget based on how many lines of text are contained within it.
        """
        num_lines = self._textbox.count("1.0", "end", "displaylines")[0]

        new_height = num_lines

        if self.cget("height") != new_height:
            self.configure(height=new_height)

    def on_resize(self, event: Any) -> None:
        """Set up a timer for resizing the widget.

        Sets up a timer for resizing the widget after the text within has been edited.
        :param event: Param shoehorned in, so customtkinter doesn't complain.
        :return: None
        """
        if self._resize_timer:
            self.after_cancel(self._resize_timer)

        self._resize_timer = self.after(200, self.update_height)
