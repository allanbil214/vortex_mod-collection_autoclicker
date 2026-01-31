# Vortex Mod Collection Auto Downloader

An automated script for downloading mod collections in Vortex Mod Manager without a premium NexusMods subscription. This tool automatically clicks the "Download manually" button and waits for each mod to complete before moving to the next one.

## 🎯 Purpose

This script is designed for **free NexusMods users** who want to download mod collections through Vortex Mod Manager. Instead of manually clicking "Download manually" for each mod in a collection, this script automates the process while you do something else.

## 🔗 Works In Conjunction With

This script **must be used together** with the [nexus-no-wait-pp](https://github.com/torkelicious/nexus-no-wait-pp) browser extension, which automatically handles the "Slow Download" button in your browser.

**Combined workflow:**
1. Vortex opens → This script clicks "Download manually"
2. Browser opens → nexus-no-wait-pp clicks "Slow Download"
3. Download starts → Script waits for next mod
4. Repeat until all mods are downloaded

## ✨ Features

- 🖱️ **Auto-clicks** "Download manually" button in Vortex
- ⏱️ **Intelligent waiting** - Uses OCR to detect when mod name changes before clicking next
- 🔄 **Retry mechanism** - Attempts 5 times before prompting user
- 📊 **Progress tracking** - Console output shows download count and status
- 🛡️ **Safe operation** - Restores mouse position, handles interrupts gracefully
- 💬 **User control** - Prompts user when button not found (retry or quit)

## 📋 Prerequisites

### Required Software

1. **Python 3.7+**
   - Download from [python.org](https://www.python.org/downloads/)

2. **Tesseract OCR**
   - **Windows:** [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Linux:** `sudo apt-get install tesseract-ocr`
   - **Mac:** `brew install tesseract`

3. **Python Packages**
   ```bash
   pip install pyautogui pytesseract pillow opencv-python 
   ```

4. **Browser Extension**
   - Install [nexus-no-wait-pp](https://github.com/torkelicious/nexus-no-wait-pp) for your browser

## 🚀 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/vortex-auto-downloader.git
   cd vortex-auto-downloader
   ```

2. **Install dependencies**
   ```bash
   pip install pyautogui pytesseract pillow opencv-python
   ```

3. **Install Tesseract OCR** (see Prerequisites above)

4. **Configure Tesseract path** (Windows only)
   
   Open `vortex_auto_downloader.py` and update this line with your Tesseract installation path:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

## 📸 Setup

### 1. Create Button Screenshot

1. Open Vortex Mod Manager
2. Navigate to a mod collection download screen
3. Take a screenshot of **ONLY** the "Download manually" button
4. Save it as `download_manually.PNG` in the script folder

**Tips for good screenshot:**
- Capture only the button, no extra borders
- Use high quality/resolution
- Ensure button text is clear and readable

### 2. Configure Mod Name Region (Optional but Recommended)

The script uses OCR to detect when the mod name changes. For best results:

1. Run the helper script:
   ```bash
   python find_mod_region.py
   ```

2. Follow the on-screen instructions to identify the mod name coordinates

3. Copy the output and update `MOD_NAME_REGION` in the main script:
   ```python
   MOD_NAME_REGION = (100, 100, 600, 50)  # Your coordinates
   ```

## 🎮 Usage

1. **Setup your environment:**
   - Open Vortex Mod Manager
   - Navigate to your mod collection
   - Start the download process (you'll see the first "Download manually" button)
   - Make sure nexus-no-wait-pp extension is enabled in your browser

2. **Run the script:**
   ```bash
   python vortex_auto_downloader.py
   ```

3. **Let it work:**
   - The script will automatically click "Download manually"
   - Your browser will open (nexus-no-wait-pp handles the "Slow Download" button)
   - The script waits for the download to complete and mod name to change
   - Process repeats for all mods

4. **When complete:**
   - Script will notify you when no more buttons are found
   - You can choose to retry or quit

## ⚙️ Configuration

Edit these variables in `vortex_auto_downloader.py`:

```python
CONFIDENCE_THRESHOLD = 0.85     # Image matching accuracy (0.0-1.0)
MAX_RETRIES_NO_BUTTON = 5       # Quick retry attempts before auto-retry
RETRY_INTERVAL = 3              # Seconds between quick retries
POLL_INTERVAL = 2               # How often to check for button
BROWSER_DELAY = 5               # Wait time for browser to process
MOD_NAME_TIMEOUT = 60           # Max wait for mod name change
AUTO_RETRY_TIMEOUT = 30         # Seconds to auto-scan before asking user (for when Vortex is downloading multiple mods)
```

**Important Note on `AUTO_RETRY_TIMEOUT`:**
When Vortex downloads multiple mods simultaneously, the "Download manually" button won't appear until those downloads finish. This setting makes the script automatically keep scanning for the button for the specified duration before prompting you to quit or retry. Set it higher (e.g., 60-120 seconds) if you're downloading large collections.

## 🐛 Troubleshooting

### "Tesseract not found" error
- Install Tesseract OCR (see Prerequisites)
- Update the `tesseract_cmd` path in the script

### "Image not found" errors
- Ensure `download_manually.PNG` is in the script folder
- Try lowering `CONFIDENCE_THRESHOLD` to 0.80 or 0.75
- Recreate the screenshot with better quality

### Script clicks wrong location
- Ensure screenshot only contains the button
- Check your screen resolution matches when screenshot was taken
- Try capturing a slightly larger area around the button

### OCR not detecting mod names
- Run `find_mod_region.py` to set proper coordinates
- Verify Tesseract is installed correctly
- The script will still work but may not wait for mod changes

### Browser doesn't auto-click
- Make sure nexus-no-wait-pp extension is installed and enabled
- Check extension permissions for nexusmods.com

## 🔒 Safety & Best Practices

- ✅ Test with 2-3 mods first before running on large collections
- ✅ Keep Vortex window in the same position during operation
- ✅ Don't minimize or move windows while script is running
- ✅ Monitor the first few downloads to ensure proper operation
- ✅ Press `Ctrl+C` to stop the script gracefully at any time

## 📝 How It Works

1. **Image Recognition**: Uses PyAutoGUI to find the "Download manually" button on screen
2. **Click Automation**: Clicks the button and returns mouse to original position
3. **Browser Handling**: Waits for nexus-no-wait-pp to handle the browser download
4. **OCR Detection**: Uses Tesseract to read mod name and detect when it changes
5. **Smart Waiting**: Only clicks next button when a new mod appears
6. **Auto-Retry**: If button not found, automatically scans for 30 seconds (configurable) before prompting
7. **Error Handling**: After auto-retry timeout, prompts user to quit or retry manually

## ⚠️ Disclaimer

This tool is for educational purposes and to improve user experience for free NexusMods users. It does not bypass any premium features or violate terms of service - it simply automates the manual clicking process that free users must perform anyway.

**Please support NexusMods by:**
- Considering a premium subscription if you frequently download mods
- Donating to mod authors
- Endorsing mods you enjoy

## 📄 License

No License - feel free to use and modify as needed.

## 🙏 Credits

- Built for use with [nexus-no-wait-pp](https://github.com/torkelicious/nexus-no-wait-pp) by torkelicious
- Uses PyAutoGUI for automation
- Uses Tesseract OCR for text recognition

---

**Enjoy your automated mod downloads! 🎮**
