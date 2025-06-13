from Widgets.WidgetsBase import *

class CTkSpinbox(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 variable: Optional[Union[DoubleVar, IntVar]] = None,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.variable = variable or DoubleVar(value=0)
        self.variable.trace_add("write",
                                self._on_var_change)

        self.configure(fg_color=MXB_RED)
        self.grid_columnconfigure((0, 2),
                                  weight=0)
        self.grid_columnconfigure(1,
                                  weight=1)

        self.subtract_button = CTkButton(self, text="-",
                                         width=height-6,
                                         height=height-6,
                                         command=self.subtract_button_callback,
                                         fg_color="white",
                                         hover_color="#ffbfbf",
                                         text_color=MXB_RED)
        self.subtract_button.grid(row=0,
                                  column=0,
                                  padx=(3, 0),
                                  pady=3)

        self.entry = CTkEntry(self,
                              width=width - 2 * height,
                              height=height - 6,
                              border_width=0,
                              textvariable=self.variable)
        self.entry.grid(row=0,
                        column=1,
                        padx=3,
                        pady=3,
                        sticky="ew")

        self.add_button = CTkButton(self,
                                    text="+",
                                    width=height-6,
                                    height=height-6,
                                    command=self.add_button_callback,
                                    fg_color="white",
                                    hover_color="#bfffcc",
                                    text_color=MXB_RED)
        self.add_button.grid(row=0,
                             column=2,
                             padx=(0, 3),
                             pady=3)

    def _on_var_change(self, *args):
        if self.command:
            self.command()

    def add_button_callback(self):
        try:
            self.variable.set(self.variable.get() + self.step_size)
        except Exception:
            self.variable.set(0)

    def subtract_button_callback(self):
        try:
            self.variable.set(self.variable.get() - self.step_size)
        except Exception:
            self.variable.set(0)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

    def base_checkbox_tick(self, checkbox_kind : str) -> None:
        if checkbox_kind == "Evidence":
            self.checkboxes[1].deselect()
        else:
            self.checkboxes[0].deselect()
        self.get_total()