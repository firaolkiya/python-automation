import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


def open_browser():
     url = "https://www.betika.com/et/aviator?utm_medium=ppc&utm_source=google&campaign=Eth_PMAX_Aviator_Welcome_Bonus_2025&adgroup=&keyword=&matchtype=&gclsrc=aw.ds&gad_source=1&gad_campaignid=22139570812&gbraid=0AAAAABUaFqYrGYBKKxD8XFUylf0qwaim2&gclid=Cj0KCQjwmK_CBhCEARIsAMKwcD5oX3Xo8V7mDcRZWRdm8HLiStxSN_Ut7qMpeMrccZKYKNc4GEaZ0AEaApJNEALw_wcB"

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        logging.info("✅ The web is opening.....")

        wait = WebDriverWait(driver, 30)

        # Step 1: Click emulator image in box id=1
        box = wait.until(EC.presence_of_element_located((By.ID, "1")))
        first_emulator_link = box.find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].scrollIntoView(true);", first_emulator_link)
        time.sleep(1)
        first_emulator_link.click()
        logging.info("✅ Clicked first emulator button")
    except Exception as e:
        logging.error(f"❌ Error occurred: {e}")