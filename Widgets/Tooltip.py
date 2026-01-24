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

        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<ButtonPress>", self.hide_tooltip)

    def schedule_tooltip(self, event=None):
        self.id = self.widget.after(self.delay, self.show_tooltip)

    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tooltip_window = CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        self.tooltip_window.attributes("-topmost", True)

        label = CTkLabel(
            master=self.tooltip_window,
            text=self.text,
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

        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None