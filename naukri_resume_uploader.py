import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

USERNAME = os.environ.get("NAUKRI_USERNAME")
PASSWORD = os.environ.get("NAUKRI_PASSWORD")
RESUME_PATH = os.path.abspath("Sunil_kumar_Python_Automation_Tester.pdf")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.naukri.com/")
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
driver.save_screenshot("home_page.png")

try:
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
except TimeoutException:
    print("❌ Login button not found!")
    driver.save_screenshot("login_fail.png")
    driver.quit()
    raise

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter your active Email ID / Username"]'))
).send_keys(USERNAME)

driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter your password"]').send_keys(PASSWORD)
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "mnjuser/profile")]')))

driver.get("https://www.naukri.com/mnjuser/profile")

try:
    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'i[data-title="delete-resume"]'))
    )
    delete_button.click()
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='lightbox model_open flipOpen']//button[@class='btn-dark-ot']"))
    )
    confirm_button.click()
    time.sleep(2)
    driver.refresh()
except TimeoutException:
    print("🔸 No existing resume to delete.")

try:
    upload_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="attachCV"]'))
    )
    upload_element.send_keys(RESUME_PATH)
    print("✅ Resume uploaded.")
except Exception as e:
    print("❌ Upload failed:", e)
    driver.save_screenshot("upload_fail.png")

time.sleep(3)
driver.quit()
