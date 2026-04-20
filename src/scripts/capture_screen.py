"""Used to capture a screenshot, used in GitHub builds to ensure the app built successfully."""
import sys
import time

from PIL import ImageGrab

time.sleep(15)

try:
    screenshot = ImageGrab.grab()

    if screenshot.mode in ["RGBA", "P"]:
        screenshot = screenshot.convert("RGB")

    screenshot.save("screenshot.jpg", "JPEG")
except Exception:
    sys.exit(1)
