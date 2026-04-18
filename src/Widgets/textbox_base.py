from src.Common.Enums.placeholder_texts import PlaceholderTexts
from customtkinter import CTkTextbox, CTkFrame
from widgets_base import MXB_RED

class TextBoxBase(CTkTextbox):
    def __init__(self,
                 master: CTkFrame,
                 border_color = "401c1b",
                 fg_color = "transparent",
                 text_color = MXB_RED,
                 wrap = "word",
                 height = 35,
                 activate_scrollbars = False,
                 border_width = 0,
                 text = PlaceholderTexts.DESCRIPTION,
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

    def start_edit(self, event = None) -> None:
        self.configure(state="normal",
                       border_color=MXB_RED,
                       border_width=2,
                       fg_color="#b39998")
        self.focus_set()

    def stop_edit(self, event = None):
        self.configure(state="disabled",
                       border_width=0,
                       fg_color="white")
        return "break"

    def add_newline(self, event = None) -> None:
        pass

    def update_height(self):
        num_lines = self._textbox.count("1.0", "end", "displaylines")[0]

        new_height = num_lines

        if self.cget("height") != new_height:
            self.configure(height=new_height)

    def on_resize(self, event):
        if self._resize_timer:
            self.after_cancel(self._resize_timer)

        self._resize_timer = self.after(200, self.update_height)