from pydbus import SessionBus
from gi.repository import GLib

# Connect to the session bus
bus = SessionBus()

# Get the squeekboard object
osk = bus.get("sm.puri.OSK0", "/sm/puri/OSK0")

# Show the keyboard
osk.SetVisible(True)

# Wait a bit so you can see it
import time
time.sleep(3)

# Hide the keyboard
osk.SetVisible(False)