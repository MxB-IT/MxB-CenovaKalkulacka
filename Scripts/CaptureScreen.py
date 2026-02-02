import sys
from PIL import ImageGrab
import time

time.sleep(15)

try:
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.jpg", "JPEG")
    print("Screenshot captured successfully.")
except Exception as e:
    print(f"Failed to capture screenshot: {e}")
    sys.exit(1)