import sys
import tkinter as tk

from src.price_calc import PriceCalc
from src.scripts.resource_pather import ResourcePather

if __name__ == "__main__":
    app = PriceCalc()
    if sys.platform.startswith("win"):
        app.iconbitmap(ResourcePather.resource_path("assets/Icon/calculatorICO.ico"))
    else:
        img = tk.PhotoImage(file=ResourcePather.resource_path("assets/Icon/calculatorICNS.icns"))
        app.iconphoto(True, img)
    app.mainloop()
