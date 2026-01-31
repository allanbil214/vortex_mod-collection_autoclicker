import os
import pyautogui
import pytesseract
from PIL import Image
import time
import sys

# ============================================
# TESSERACT PATH CONFIGURATION (Windows)
# ============================================
# If you get "tesseract is not installed" error, uncomment and update this path:
pytesseract.pytesseract.tesseract_cmd = r'C:\Applications\Tesseract-OCR\tesseract.exe'

# Common alternative paths:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
# ============================================

print("=== Vortex Auto Mod Downloader ===")
print(f"Working directory: {os.getcwd()}\n")

# Disable PyAutoGUI failsafe (move mouse to corner to stop)
# Set to True if you want the failsafe feature
pyautogui.FAILSAFE = False

# Configuration
DOWNLOAD_BUTTON_IMAGE = "download_manually.PNG"  # You'll need to create this screenshot
CONFIDENCE_THRESHOLD = 0.85
MAX_RETRIES_NO_BUTTON = 5  # How many times to retry if button not found
RETRY_INTERVAL = 3  # Seconds between retries
POLL_INTERVAL = 2  # Seconds between checking if button reappeared
BROWSER_DELAY = 5  # Seconds to wait for browser JS to work
MOD_NAME_TIMEOUT = 60  # Max seconds to wait for mod name to change
AUTO_RETRY_TIMEOUT = 30  # Seconds to auto-retry before prompting user (when Vortex is downloading multiple mods)

# You'll need to adjust these coordinates based on your screen
# This is the region where the mod name appears (x, y, width, height)
# To find this, run the script once and it will help you identify the region
MOD_NAME_REGION = None  # Will be set to (left, top, width, height) or None for manual setup


def capture_mod_name(region=None):
    """
    Captures the mod name from the screen using OCR.
    If region is None, captures a larger area (you should refine this).
    """
    try:
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            # Default: capture area around where mod name typically appears
            # You may need to adjust this based on your screen resolution
            screenshot = pyautogui.screenshot(region=(641, 96, 634, 57))
        
        # Use OCR to extract text
        mod_name = pytesseract.image_to_string(screenshot).strip()
        return mod_name
    except Exception as e:
        print(f"Error capturing mod name: {e}")
        return None


def find_download_button(max_attempts=1):
    """
    Searches for the 'Download manually' button on screen.
    Returns the location if found, None otherwise.
    """
    for attempt in range(max_attempts):
        try:
            location = pyautogui.locateOnScreen(DOWNLOAD_BUTTON_IMAGE, confidence=CONFIDENCE_THRESHOLD)
            if location is not None:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        
        if attempt < max_attempts - 1:
            time.sleep(RETRY_INTERVAL)
    
    return None


def click_button(location):
    """
    Clicks the button at the given location and restores mouse position.
    """
    # Save current mouse position
    original_x, original_y = pyautogui.position()
    
    # Click the button (offset slightly from top-left corner)
    click_x = location.left + location.width // 2
    click_y = location.top + location.height // 2
    
    pyautogui.click(click_x, click_y)
    print(f"✓ Clicked button at ({click_x}, {click_y})")
    
    # Restore mouse position
    pyautogui.moveTo(original_x, original_y)


def wait_for_button_reappear(timeout=30):
    """
    Polls for the download button to reappear after browser activity.
    Returns True if button found, False if timeout.
    """
    print("⏳ Waiting for button to reappear...", end="", flush=True)
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        location = find_download_button(max_attempts=1)
        if location is not None:
            print(" Found!")
            return True
        print(".", end="", flush=True)
        time.sleep(POLL_INTERVAL)
    
    print(" Timeout!")
    return False


def wait_for_mod_name_change(previous_name, timeout=MOD_NAME_TIMEOUT):
    """
    Waits until the mod name changes from the previous one.
    Returns the new mod name if changed, None if timeout.
    """
    print(f"⏳ Waiting for mod name to change from: '{previous_name}'")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        current_name = capture_mod_name(MOD_NAME_REGION)
        
        if current_name and current_name != previous_name:
            print(f"✓ New mod detected: '{current_name}'")
            return current_name
        
        time.sleep(2)
    
    print("⚠ Timeout waiting for mod name change")
    return None


def auto_retry_find_button(timeout=AUTO_RETRY_TIMEOUT):
    """
    Auto-retries finding the button for a specified duration.
    This is useful when Vortex is downloading multiple mods and button doesn't appear.
    Returns button location if found, None if timeout reached.
    """
    print(f"\n⏳ Auto-retrying for {timeout} seconds (Vortex may be downloading multiple mods)...")
    print("   Scanning for button", end="", flush=True)
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        location = find_download_button(max_attempts=1)
        if location is not None:
            print(" Found!")
            return location
        
        print(".", end="", flush=True)
        time.sleep(POLL_INTERVAL)
    
    print(f" Timeout after {timeout}s!")
    return None


def prompt_user_on_no_button():
    """
    Prompts user when button is not found after multiple retries.
    Returns True to continue, False to quit.
    """
    print("\n" + "="*60)
    print("❌ 'Download manually' button not found after multiple attempts.")
    print("="*60)
    print("\nOptions:")
    print("  [ENTER] - Retry looking for the button")
    print("  [q]     - Quit the script")
    print()
    
    user_input = input("Your choice: ").strip().lower()
    
    return user_input != 'q'


def setup_mod_name_region():
    """
    Helper function to help user identify the mod name region.
    """
    print("\n" + "="*60)
    print("SETUP: Identifying mod name region")
    print("="*60)
    print("\nYou need to define the screen region where the mod name appears.")
    print("Please follow these steps:")
    print("1. Take a screenshot of the Vortex window with a mod visible")
    print("2. Note the coordinates (x, y, width, height) of the mod name area")
    print("3. Update MOD_NAME_REGION in the script")
    print("\nFor now, using default region. OCR might not work accurately.")
    print("="*60 + "\n")
    input("Press ENTER to continue...")


def main():
    """
    Main loop for the auto-downloader.
    """
    print("\n🚀 Starting Vortex Auto Mod Downloader...")
    print(f"📁 Make sure '{DOWNLOAD_BUTTON_IMAGE}' exists in: {os.getcwd()}\n")
    
    # Check if button image exists
    if not os.path.exists(DOWNLOAD_BUTTON_IMAGE):
        print(f"❌ ERROR: Image file '{DOWNLOAD_BUTTON_IMAGE}' not found!")
        print("Please create a screenshot of the 'Download manually' button.")
        return
    
    # Setup mod name region if needed
    if MOD_NAME_REGION is None:
        setup_mod_name_region()
    
    print("Starting in 3 seconds... (Move mouse to corner to abort if FAILSAFE is True)")
    time.sleep(3)
    
    download_count = 0
    current_mod_name = capture_mod_name(MOD_NAME_REGION)
    
    print(f"Initial mod: '{current_mod_name}'\n")
    print("-" * 60)
    
    while True:
        # Step 1: Find and click the "Download manually" button
        print(f"\n[Cycle {download_count + 1}] Looking for 'Download manually' button...")
        
        button_location = find_download_button(max_attempts=1)
        
        if button_location is None:
            print("⚠ Button not found on first attempt. Retrying...")
            button_location = find_download_button(max_attempts=MAX_RETRIES_NO_BUTTON)
            
            if button_location is None:
                # Button still not found after quick retries
                # Try auto-retry with longer timeout (Vortex might be downloading multiple mods)
                button_location = auto_retry_find_button(timeout=AUTO_RETRY_TIMEOUT)
                
                if button_location is None:
                    # Still not found after auto-retry timeout - prompt user
                    should_continue = prompt_user_on_no_button()
                    
                    if not should_continue:
                        print("\n👋 Exiting script. Goodbye!")
                        break
                    else:
                        print("\n🔄 Retrying...\n")
                        continue
        
        # Step 2: Click the button
        click_button(button_location)
        download_count += 1
        
        # Step 3: Wait for browser JavaScript to handle the download
        print(f"⏳ Waiting {BROWSER_DELAY}s for browser to process...")
        time.sleep(BROWSER_DELAY)
        
        # Step 4: Wait for button to reappear (indicates we're back in Vortex)
        if not wait_for_button_reappear(timeout=30):
            print("⚠ Button didn't reappear. Continuing anyway...")
        
        # Step 5: Wait for mod name to change before clicking again
        new_mod_name = wait_for_mod_name_change(current_mod_name, timeout=MOD_NAME_TIMEOUT)
        
        if new_mod_name:
            current_mod_name = new_mod_name
        else:
            print("⚠ Mod name didn't change. Proceeding anyway...")
            # Update mod name even if we're not sure it changed
            current_mod_name = capture_mod_name(MOD_NAME_REGION)
        
        print(f"✅ Downloads completed: {download_count}")
        print("-" * 60)
    
    print(f"\n📊 Final stats: {download_count} downloads initiated")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Script interrupted by user (Ctrl+C)")
        print("👋 Exiting gracefully...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()