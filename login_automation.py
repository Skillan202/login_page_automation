# Import required modules from Selenium and Python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the Chrome browser (no Service object used here)
driver = webdriver.Chrome()
driver.maximize_window()  # Maximize the browser window for better visibility

# Array of test cases, each represented as a dictionary
# Contains different combinations of username and password with expected error messages
test_cases = [
    {"username_value": "standard_user", "password_value": "standard_user", "expected_error_code": "Epic sadface: Username and password do not match any user in this service"},
    {"username_value": "", "password_value": "secret_sauce", "expected_error_code": "Epic sadface: Username is required"},
    {"username_value": "standard_user", "password_value": "", "expected_error_code": "Epic sadface: Password is required"},
    {"username_value": "", "password_value": "", "expected_error_code": "Epic sadface: Username is required"},  # Both fields empty
    {"username_value": "standard_user", "password_value": "secret_sauce", "expected_error_code": ""},  # Valid credentials
]

try:
    # Loop through each test case
    for test_case in test_cases:
        # Extract test data
        username_value = test_case["username_value"]
        password_value = test_case["password_value"]
        expected_error_code = test_case["expected_error_code"]

        # Step 1: Open the Sauce Demo login page
        driver.get("https://www.saucedemo.com/")

        # Step 2: Locate username and password input fields using XPath
        username_field = driver.find_element(By.XPATH, "//input[@id='user-name']")
        password_field = driver.find_element(By.XPATH, "//input[@id='password']")

        # Step 3: Enter username and password from the test case
        username_field.send_keys(username_value)
        password_field.send_keys(password_value)

        # Step 4: Click the login button
        login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
        login_button.click()

        # Step 5: Wait for a short time to allow the page to process the login
        time.sleep(2)

        try:
            # Try to locate the error message element after login attempt
            error_message = driver.find_element(By.XPATH, "//h3[@data-test='error']").text
            
            # Print test case details
            print(f"\nTesting with: \nUsername: '{username_value}'\nPassword: '{password_value}'")
            print(f"Expected error code: '{expected_error_code}'")
            print(f"Current error message: '{error_message}'")
            
            # Compare actual and expected error messages
            if error_message == expected_error_code:
                print(f"\033[92m[PASS] - Correct error message: {error_message}\033[0m")  # Green = PASS
            else:
                print(f"\033[91m[FAIL] - Mismatch: Expected '{expected_error_code}', but got '{error_message}'\033[0m")  # Red = FAIL
        except:
            # If no error message element is found
            print("\033[91m[FAIL] - Error message not found\033[0m")

except Exception as e:
    # Catch any unexpected exception and print it
    print(f"Test failed: {e}")

finally:
    # Wait for 3 seconds before closing the browser
    time.sleep(3)
    driver.quit()  # Close the browser and end the WebDriver session
