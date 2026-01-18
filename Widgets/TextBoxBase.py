from Common.PlaceholderTexts import PlaceholderTexts
from Widgets.WidgetsBase import *

class TextBoxBase(CTkTextbox):
    def __init__(self,
                 master: CTkFrame,
                 border_color = "401c1b",
                 fg_color = "transparent",
                 text = PlaceholderTexts.DESCRIPTION,
                 text_color = MXB_RED,
                 wrap = "word",
                 height = 35,
                 activate_scrollbars = False,
                 border_width = 0,
                 *args,
                 **kwargs):
        super().__init__(master,
                         border_color=border_color,
                         fg_color=fg_color,
                         text_color=text_color,
                         wrap=wrap,
                         height=height,
                         activate_scrollbars=activate_scrollbars,
                         border_width=border_width,
                         *args,
                         **kwargs)
        self.insert(0.0, text)

        self.configure(state = "disabled")
        self.editing = False

        self.bind("<Button-1>", self.start_edit)
        self.bind("<Return>", self.stop_edit)
        self.bind("<FocusOut>", self.stop_edit)
        self.bind("<Shift-Return>", self.add_newline)

    def start_edit(self, event = None) -> None:
        self.configure(state = "normal")
        self.focus_set()

    def stop_edit(self, event = None):
        self.configure(state = "disabled")
        return "break"

    def add_newline(self, event = None) -> None:
        pass