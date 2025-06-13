from Widgets.WidgetsBase import *

class ComboBoxBase(CTkComboBox):
    def __init__(self,
                 *args,
                 master: CTkFrame,
                 border_color = "#401c1b",
                 fg_color = "white",
                 dropdown_fg_color = "white",
                 button_color = "#401c1b",
                 text_color = MXB_RED,
                 dropdown_text_color = MXB_RED,
                 dropdown_hover_color = "#ffb3b3",
                 border_width = 2,
                 button_hover_color="#ffb3b3",
                 **kwargs):
        super().__init__(*args,
                         master,
                         border_color=border_color,
                         fg_color=fg_color,
                         dropdown_fg_color=dropdown_fg_color,
                         button_color=button_color,
                         text_color=text_color,
                         dropdown_text_color=dropdown_text_color,
                         border_width=border_width,
                         dropdown_hover_color=dropdown_hover_color,
                         button_hover_color=button_hover_color,
                         **kwargs)