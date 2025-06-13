from Widgets.WidgetsBase import *

class CheckBoxBase(CTkCheckBox):
    def __init__(self,
                 *args,
                 master: CTkFrame,
                 fg_color = MXB_RED,
                 border_color = MXB_RED,
                 text_color = MXB_RED,
                 hover_color = MXB_RED,
                 **kwargs):
        super().__init__(*args,
                         master,
                         hover_color = hover_color,
                         fg_color = fg_color,
                         border_color = border_color,
                         text_color = text_color,
                         **kwargs)