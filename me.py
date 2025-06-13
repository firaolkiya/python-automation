import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pyautogui
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def open_and_run_android_emulator():
    url = "https://www.myandroid.org/playonline/androidemulator.php"

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        logging.info("✅ Opened initial emulator page")

        wait = WebDriverWait(driver, 30)

        # Step 1: Click emulator image in box id=1
        box = wait.until(EC.presence_of_element_located((By.ID, "1")))
        first_emulator_link = box.find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].scrollIntoView(true);", first_emulator_link)
        time.sleep(1)
        first_emulator_link.click()
        logging.info("✅ Clicked first emulator button")

        # Step 2: Wait for and click Enter button that links to /run/start.php
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/run/start.php']")))
        second_emulator_link = driver.find_element(By.CSS_SELECTOR, "a[href='/run/start.php']")
        driver.execute_script("arguments[0].scrollIntoView(true);", second_emulator_link)
        time.sleep(1)
        second_emulator_link.click()
        logging.info("✅ Clicked Enter image button")

        # Step 3: Wait 12 seconds for splash screen to load
        logging.info("⏳ Waiting 12 seconds for 'Start emulator' to appear...")
        time.sleep(12)

        # Step 4: Click 'Start emulator' button
        start_button = wait.until(EC.element_to_be_clickable((By.ID, "talpa-splash-button")))
        if start_button.text.strip().lower() == "start emulator":
            start_button.click()
            logging.info("✅ Clicked 'Start emulator' button")
        else:
            logging.warning("⚠️ 'Start emulator' button not found, got different label")

        # Step 5: Wait 20 seconds for loading
        logging.info("⏳ Waiting 20 seconds for 'Enter' button to appear...")
        time.sleep(40)

        # Step 6: Click 'Enter' button
        enter_button = wait.until(EC.element_to_be_clickable((By.ID, "talpa-splash-button")))
        if enter_button.text.strip().lower() == "enter":
            enter_button.click()
            logging.info("✅ Clicked final 'Enter' button")
        else:
            logging.warning("⚠️ Final 'Enter' button not found, got different label")

        # Done
        logging.info("✅ Emulator should now be running")
        time.sleep(50)
        pyautogui.click(x=900, y=370)  # Click somewhere on emulator (Play Store icon)
        print("already clicked")
        # Simulate typing email
        pyautogui.write('fraolbulo20@@gmail.com', interval=0.1)
        print("password entered")
        pyautogui.press('Next')
        time.sleep(15)

        # Simulate typing password
        pyautogui.write('Fir12@#80', interval=0.1)
        pyautogui.press('Next')
        input("Press Enter to exit...")

    except Exception as e:
        logging.error(f"❌ Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    open_and_run_android_emulator()
