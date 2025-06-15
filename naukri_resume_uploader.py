import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Credentials from GitHub Secrets
USERNAME = os.getenv("NAUKRI_USERNAME")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = os.path.abspath("Sunil_Kumar_PythonAutomationTester.pdf")

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless=new')  # headless mode for CI

driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Open Naukri website
driver.get("https://www.naukri.com/")

# Login
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Enter your active Email ID / Username"]'))
).send_keys(USERNAME)
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter your password"]').send_keys(PASSWORD)
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

# Wait for login
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "mnjuser/profile")]')))

# Go to profile page
driver.get("https://www.naukri.com/mnjuser/profile")

try:
    # Delete existing resume
    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'i[data-title="delete-resume"]'))
    )
    print("🔹 Old resume found. Deleting...")
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

# Upload new resume
try:
    upload_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="attachCV"]'))
    )
    upload_element.send_keys(RESUME_PATH)
    print("✅ Resume uploaded successfully!")
except (TimeoutException, NoSuchElementException) as e:
    print("❌ Resume upload failed!")
    print(f"⚠️ Error: {e}")

time.sleep(3)
driver.quit()
