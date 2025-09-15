from pydbus import SessionBus
from gi.repository import GLib

# Connect to the session bus
print("Connecting to D-Bus session bus...")
bus = SessionBus()
print("Connected to D-Bus session bus.")
# Get the squeekboard object
osk = bus.get("sm.puri.OSK0", "/sm/puri/OSK0")
print("Obtained OSK object.")
# Show the keyboard
osk.SetVisible(True)
print("On-screen keyboard should now be visible.")
# Wait a bit so you can see it
import time
time.sleep(3)

# Hide the keyboard
osk.SetVisible(False)