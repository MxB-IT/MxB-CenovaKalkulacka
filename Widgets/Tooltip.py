from customtkinter import CTkToplevel, CTkLabel

class Tooltip:
    def __init__(self,
                 widget,
                 text,
                 delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.id = None
        self._widget = widget
        self._text = text
        self._delay = delay
        self._tooltip_window = None
        self._id = None

        self._widget.bind("<Enter>", self._schedule_tooltip)
        self._widget.bind("<Leave>", self._hide_tooltip)
        self._widget.bind("<ButtonPress>", self._hide_tooltip)

    def schedule_tooltip(self, event=None):
        self.id = self.widget.after(self.delay, self.show_tooltip)
    def _schedule_tooltip(self) -> None:
        self._id = self._widget.after(self._delay, self._show_tooltip)

    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
    def _show_tooltip(self) -> None:
        x = self._widget.winfo_rootx() + 20
        y = self._widget.winfo_rooty() + self._widget.winfo_height() + 5

        self._tooltip_window = CTkToplevel(master=self._widget)
        self._tooltip_window.wm_overrideredirect(True)
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
            pady=5
        )
        label.pack()

    def hide_tooltip(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
    def _hide_tooltip(self) -> None:
        if self._id:
            self._widget.after_cancel(self._id)
            self._id = None

        if self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None