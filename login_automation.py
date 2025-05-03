from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Setup
driver = webdriver.Chrome()  # No Service object
driver.maximize_window()

# Array of objects with different test cases
test_cases = [
    {"username_value": "standard_user", "password_value": "standard_user", "expected_error_code": "Epic sadface: Username and password do not match any user in this service"},
    {"username_value": "", "password_value": "secret_sauce", "expected_error_code": "Epic sadface: Username is required"},
    {"username_value": "standard_user", "password_value": "", "expected_error_code": "Epic sadface: Password is required"},
    {"username_value": "", "password_value": "", "expected_error_code": "Epic sadface: Username is required"},  # New test case with both fields empty
    {"username_value": "standard_user", "password_value": "secret_sauce", "expected_error_code": ""},

]

try:
    for test_case in test_cases:
        username_value = test_case["username_value"]
        password_value = test_case["password_value"]
        expected_error_code = test_case["expected_error_code"]

        # Step 1: Open the login page
        driver.get("https://www.saucedemo.com/")

        # Step 2: Locate username and password fields
        username_field = driver.find_element(By.XPATH, "//input[@id='user-name']")
        password_field = driver.find_element(By.XPATH, "//input[@id='password']")

        # Step 3: Enter credentials based on the test case
        username_field.send_keys(username_value)
        password_field.send_keys(password_value)

        # Step 4: Click the login button
        login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
        login_button.click()

        # Step 5: Check for error message after login attempt
        time.sleep(2)  # Allow time for the error message to load

        try:
            error_message = driver.find_element(By.XPATH, "//h3[@data-test='error']").text
            print(f"\nTesting with: \nUsername: '{username_value}'\nPassword: '{password_value}'")
            print(f"Expected error code: '{expected_error_code}'")
            print(f"Current error message: '{error_message}'")
            
            if error_message == expected_error_code:
                print(f"\033[92m[PASS] - Correct error message: {error_message}\033[0m")  # Green for pass
            else:
                print(f"\033[91m[FAIL] - Mismatch: Expected '{expected_error_code}', but got '{error_message}'\033[0m")  # Red for mismatch
        except:
            print("\033[91m[FAIL] - Error message not found\033[0m")  # Red for error message not found

except Exception as e:
    print(f"Test failed: {e}")

finally:
    time.sleep(3)
    driver.quit()
