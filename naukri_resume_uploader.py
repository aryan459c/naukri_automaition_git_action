import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Load credentials from environment variables
USERNAME = os.environ.get("USERNAME", "")
PASSWORD = os.environ.get("PASSWORD", "")
RESUME_PATH = os.path.abspath("Sunil_kumar_Python_Automation_Tester.pdf")

# Setup headless Chrome for GitHub Actions
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1080)

try:
    # Step 1: Open Naukri and login
    driver.get("https://www.naukri.com/")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()

    # Email Input
    email_input = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Enter your active Email ID / Username"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", email_input)
    time.sleep(1)
    email_input.send_keys(USERNAME)

    # Password Input
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Enter your password"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", password_input)
    time.sleep(1)
    password_input.send_keys(PASSWORD)

    # Submit Login
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Wait for profile link to confirm login success
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "mnjuser/profile")]'))
    )
    print("✅ Logged in successfully.")

    # Step 2: Navigate to profile
    driver.get("https://www.naukri.com/mnjuser/profile")

    # Step 3: Delete existing resume if present
    try:
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'i[data-title="delete-resume"]'))
        )
        print("🔹 Old resume found. Deleting...")
        delete_button.click()

        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='lightbox model_open flipOpen']//button[@class='btn-dark-ot']")
            )
        )
        confirm_button.click()
        print("✅ Old resume deleted successfully.")
        time.sleep(2)
        driver.refresh()

    except TimeoutException:
        print("🔸 No existing resume found. Proceeding to upload.")

    # Step 4: Upload new resume
    try:
        upload_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="attachCV"]'))
        )
        upload_element.send_keys(RESUME_PATH)
        print("✅ Resume uploaded successfully!")

    except (TimeoutException, NoSuchElementException) as e:
        print("❌ Resume upload failed!")
        print(f"⚠️ Error: {e}")

except Exception as e:
    print("❌ Unexpected error occurred!")
    print(f"⚠️ {e}")

finally:
    time.sleep(3)
    driver.quit()
