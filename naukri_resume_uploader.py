from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

USERNAME = os.getenv("NAUKRI_USERNAME")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = "Sunil_kumar_Python_Automation_Tester.pdf"

options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
    driver.get("https://www.naukri.com/")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'input[placeholder="Enter your active Email ID / Username"]'))
    ).send_keys(USERNAME)

    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter your password"]').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "mnjuser/profile")]')))
    driver.get("https://www.naukri.com/mnjuser/profile")

    try:
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'i[data-title="delete-resume"]'))
        )
        delete_button.click()
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='lightbox model_open flipOpen']//button[@class='btn-dark-ot']"))
        )
        confirm_button.click()
        print("✅ Old resume deleted.")
        time.sleep(2)
        driver.refresh()
    except TimeoutException:
        print("🔸 No existing resume found.")

    upload_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="attachCV"]'))
    )
    upload_element.send_keys(os.path.abspath(RESUME_PATH))
    print("✅ Resume uploaded successfully!")

except Exception as e:
    print("❌ Error occurred:", e)
finally:
    time.sleep(3)
    driver.quit()
