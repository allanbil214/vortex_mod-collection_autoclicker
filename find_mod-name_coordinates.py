import pyautogui
import time

print("="*60)
print("MOD NAME REGION FINDER")
print("="*60)
print("\nThis tool helps you find the coordinates for the mod name region.")
print("Follow the instructions carefully.\n")

input("Press ENTER when ready to start...")

print("\n[Step 1/2] Finding TOP-LEFT corner")
print("Move your mouse to the TOP-LEFT corner of the mod name text")
print("(Where the mod name starts)")

for i in range(5, 0, -1):
    print(f"  Starting in {i}...", end="\r")
    time.sleep(1)

x1, y1 = pyautogui.position()
print(f"\n✓ Top-left corner: ({x1}, {y1})")

print("\n[Step 2/2] Finding BOTTOM-RIGHT corner")
print("Move your mouse to the BOTTOM-RIGHT corner of the mod name text")
print("(Where the mod name ends)")

for i in range(5, 0, -1):
    print(f"  Starting in {i}...", end="\r")
    time.sleep(1)

x2, y2 = pyautogui.position()
print(f"\n✓ Bottom-right corner: ({x2}, {y2})")

# Calculate width and height
width = x2 - x1
height = y2 - y1

print("\n" + "="*60)
print("RESULTS")
print("="*60)
print(f"\nTop-left:     ({x1}, {y1})")
print(f"Bottom-right: ({x2}, {y2})")
print(f"Width:        {width}")
print(f"Height:       {height}")
print(f"\n📋 Copy this line into your script:")
print(f"\nMOD_NAME_REGION = ({x1}, {y1}, {width}, {height})")
print("\n" + "="*60)

input("\nPress ENTER to exit...")