import pyautogui
import time

print("Move your mouse to the desired position...")
time.sleep(3)

try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})", end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped.")
