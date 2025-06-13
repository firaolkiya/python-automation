# Ticketlink Booking Bot

A lightweight automation tool built with Python and Selenium to automate ticket booking on Ticketlink.

## Features

- Opens a specific Ticketlink event page at a user-defined time.
- Detects when the "Book Now" button appears and extracts the booking URL.
- Optionally clicks the "Book Now" button automatically.
- Logs all actions and errors to a log file.
- Saves the booking URL as a backup.

## Requirements

- Python 3.6 or higher
- Chrome browser installed
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone this repository or download the files.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```
   python main.py
   ```
2. Enter the Ticketlink event URL when prompted.
3. Enter the target time in 24-hour format (HH:MM:SS).
4. The bot will wait until the specified time, open the event page, and attempt to find the "Book Now" button.
5. If the button is found, the booking URL will be displayed and saved to `booking_url.txt`.
6. Optionally, the bot can click the "Book Now" button automatically.

## Packaging for Windows

To create a standalone executable for Windows, use PyInstaller:

```
pip install pyinstaller
pyinstaller --onefile --add-data "booking_url.txt;." main.py
```

The executable will be created in the `dist` folder.

## Notes

- Adjust the XPath selector for the "Book Now" button if needed.
- The bot uses undetected-chromedriver to avoid detection, but consider using Playwright for more advanced anti-bot evasion.
- CAPTCHA detection is simple and will prompt for manual intervention if detected.

## License

This project is open-source and available under the MIT License. 