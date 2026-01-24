from Common.PlaceholderTexts import PlaceholderTexts
from Widgets.WidgetsBase import *

class ButtonBase(CTkButton):
    def __init__(self,
                 master: CTkFrame,
                 fg_color=MXB_RED,
                 border_color=MXB_RED,
                 text_color="white",
                 text=PlaceholderTexts.BUTTON_TEXT,
                 *args,
                 **kwargs):
        super().__init__(*args,
                         master=master,
                         fg_color=fg_color,
                         border_color=border_color,
                         text_color=text_color,
                         text=text,
                         **kwargs)