import time
import sys
import logging
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import undetected_chromedriver as uc
from colorama import Fore, Style, init

# Initialize colorama
init()

def log_setup():
    """Setup logging configuration"""
    logging.basicConfig(
        filename='booking_bot.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

def precise_wait_until(target_time):
    """Wait until the exact target time with sub-second precision"""
    while True:
        now = datetime.now()
        if now >= target_time:
            break
        # Calculate time to wait
        wait_seconds = (target_time - now).total_seconds()
        if wait_seconds > 0.1:  # If more than 100ms, sleep normally
            time.sleep(wait_seconds - 0.1)
        else:  # For the last 100ms, busy wait for precision
            while datetime.now() < target_time:
                pass
    logging.info(f"Target time reached: {target_time.strftime('%H:%M:%S.%f')}")

def get_user_input():
    """Get and validate user input for URL and target time"""
    while True:
        url = input("Enter Ticketlink event URL: ").strip()
        if url.startswith(('http://', 'https://')):
            break
        print(Fore.RED + "Please enter a valid URL starting with http:// or https://" + Style.RESET_ALL)

    while True:
        time_str = input("Enter target time (HH:MM:SS, 24h): ").strip()
        try:
            today = datetime.now().date()
            target_time = datetime.strptime(f"{today} {time_str}", "%Y-%m-%d %H:%M:%S")
            if target_time > datetime.now():
                break
            print(Fore.RED + "Please enter a future time" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Please enter time in HH:MM:SS format" + Style.RESET_ALL)

    return url, target_time

def wait_for_book_now_button(driver, wait_time=30):
    """Wait for the Book Now button to appear and return it"""
    wait = WebDriverWait(driver, wait_time)
    try:
        book_btn = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'scheduleId') and contains(text(), 'Book Now')]"))
        )
        return book_btn
    except TimeoutException:
        logging.error("Book Now button not found within timeout period")
        return None

def main():
    log_setup()
    print(Fore.CYAN + "\n=== Ticketlink Booking Bot ===" + Style.RESET_ALL)
    url, target_time = get_user_input()
    
    print(f"\nBot will start at: {target_time.strftime('%H:%M:%S')}")
    print("Preparing browser...")
    
    try:
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-notifications")
        driver = uc.Chrome(options=options)
        driver.set_window_size(1920, 1080)  # Set a standard window size
        
        # Open the page slightly before target time
        print(f"\nOpening page at: {(target_time - timedelta(seconds=5)).strftime('%H:%M:%S')}")
        driver.get(url)
        logging.info(f"Opened event page: {url}")

        # Wait until exact target time
        precise_wait_until(target_time)
        
        # Start monitoring for the Book Now button
        print("\nMonitoring for Book Now button...")
        max_attempts = 30  # Maximum number of attempts to find the button
        attempt = 0
        
        while attempt < max_attempts:
            book_btn = wait_for_book_now_button(driver, wait_time=1)
            if book_btn:
                try:
                    booking_url = book_btn.get_attribute("href")
                    print(Fore.GREEN + f"\nBooking URL found: {booking_url}" + Style.RESET_ALL)
                    logging.info(f"Found booking URL: {booking_url}")

                    # Save backup
                    with open("booking_url.txt", "w") as f:
                        f.write(f"{booking_url}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    
                    # Optionally click
                    auto_click = input("\nClick 'Book Now' automatically? (y/n): ").strip().lower()
                    if auto_click == 'y':
                        try:
                            # Re-find the button to avoid stale element
                            book_btn = wait_for_book_now_button(driver)
                            if book_btn:
                                book_btn.click()
                                logging.info("Clicked 'Book Now' button")
                                print(Fore.YELLOW + "Clicked 'Book Now'! Proceed manually if needed." + Style.RESET_ALL)
                        except Exception as e:
                            logging.error(f"Error clicking button: {e}")
                            print(Fore.RED + f"Error clicking button: {e}" + Style.RESET_ALL)
                    break
                except StaleElementReferenceException:
                    logging.warning("Stale element encountered, retrying...")
                    continue
            attempt += 1
            time.sleep(0.1)  # Small delay between attempts
        
        if attempt >= max_attempts:
            print(Fore.RED + "\nBook Now button not found after maximum attempts" + Style.RESET_ALL)
            logging.error("Book Now button not found after maximum attempts")

        # Check for CAPTCHA
        if "captcha" in driver.page_source.lower():
            print(Fore.RED + "\nCAPTCHA detected! Manual intervention required." + Style.RESET_ALL)
            logging.warning("CAPTCHA detected on page")

    except Exception as e:
        logging.error(f"Error: {e}")
        print(Fore.RED + f"\nError: {e}" + Style.RESET_ALL)
    finally:
        input("\nPress Enter to exit and close browser...")
        driver.quit()

if __name__ == "__main__":
    main() 