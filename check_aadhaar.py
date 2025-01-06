#working code withot headless
# from flask import Flask, request, jsonify
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import requests
# import time

# # Flask app
# app = Flask(__name__)

# # Anticaptcha API Key
# ANTI_CAPTCHA_API_KEY = "2f91f49e0d8cafd925798b03d4aed443"

# # Aadhaar Verification URL
# AADHAAR_URL = "https://myaadhaar.uidai.gov.in/check-aadhaar-validity/en"

# def solve_captcha(base64_image):
#     """Solve captcha using Anticaptcha."""
#     if not base64_image:
#         raise ValueError("Captcha image data is missing")

#     base64_data = base64_image.split(",")[1]  # Extract Base64 part
#     url = "https://api.anti-captcha.com/createTask"
#     data = {
#         "clientKey": ANTI_CAPTCHA_API_KEY,
#         "task": {
#             "type": "ImageToTextTask",
#             "body": base64_data,
#             "phrase": False,
#             "case": False,
#             "numeric": False,
#             "math": 0,
#             "minLength": 4,
#             "maxLength": 6
#         }
#     }
#     response = requests.post(url, json=data)
#     task_id = response.json().get("taskId")

#     if not task_id:
#         raise Exception("Failed to create captcha task")

#     time.sleep(10)
#     result_url = "https://api.anti-captcha.com/getTaskResult"
#     while True:
#         result_response = requests.post(result_url, json={"clientKey": ANTI_CAPTCHA_API_KEY, "taskId": task_id})
#         result = result_response.json()
#         if result.get("status") == "ready":
#             return result["solution"]["text"]
#         time.sleep(5)

# def check_aadhaar_validity(aadhaar_number):
#     """Automate Aadhaar validity check."""
#     driver = webdriver.Chrome()  # Replace with appropriate WebDriver if not using Chrome
#     driver.get(AADHAAR_URL)

#     try:
#         wait = WebDriverWait(driver, 200)

#         # Enter Aadhaar number
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "uid")))
#         aadhaar_input = driver.find_element(By.NAME, "uid")
#         aadhaar_input.send_keys(aadhaar_number)

#         # Solve captcha
#         for _ in range(5):
#             captcha_image = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//img[@alt='captcha']"))
#             )
#             captcha_base64 = captcha_image.get_attribute("src")
#             if captcha_base64:
#                 break
#             time.sleep(2)
#         else:
#             raise Exception("Failed to load captcha image")

#         captcha_text = solve_captcha(captcha_base64)

#         captcha_input = driver.find_element(By.NAME, "captcha")
#         captcha_input.send_keys(captcha_text)

#         proceed_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and contains(@class, "button_btn__HeAxz")]'))
#         )
#         driver.execute_script("arguments[0].scrollIntoView(true);", proceed_button)
#         proceed_button.click()

#         wait = WebDriverWait(driver, 200)

#         # Wait for the next page or result element to appear
#         result_element = WebDriverWait(driver, 100).until(
#             EC.visibility_of_element_located((By.CLASS_NAME, 'check-aadhaar-validity-response__cong'))
#         )
#         result_text = result_element.text.strip()
        
#         if "exists" in result_text.lower():
#             return {"message": "Aadhaar exists", "status": True}
#         else:
#             return {"message": "Aadhaar does not exist", "status": False}
        

#     except Exception as e:
#         return {"message": f"Error occurred: {e}", "status": False}

#     finally:
#         driver.quit()

# @app.route('/check-aadhaar', methods=['POST'])
# def check_aadhaar():
#     """API endpoint to validate Aadhaar number."""
#     data = request.get_json()
#     aadhaar_number = data.get("aadhaar_number")

#     if not aadhaar_number or len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
#         return jsonify({"message": "Invalid Aadhaar number", "status": False}), 400

#     result = check_aadhaar_validity(aadhaar_number)
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)

#working code of headless bowser
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# Flask app
app = Flask(__name__)

# Anticaptcha API Key
ANTI_CAPTCHA_API_KEY = "2f91f49e0d8cafd925798b03d4aed443"

# Aadhaar Verification URL
AADHAAR_URL = "https://myaadhaar.uidai.gov.in/check-aadhaar-validity/en"

def solve_captcha(base64_image):
    """Solve captcha using Anticaptcha."""
    if not base64_image:
        raise ValueError("Captcha image data is missing")

    base64_data = base64_image.split(",")[1]  # Extract Base64 part
    url = "https://api.anti-captcha.com/createTask"
    data = {
        "clientKey": ANTI_CAPTCHA_API_KEY,
        "task": {
            "type": "ImageToTextTask",
            "body": base64_data,
            "phrase": False,
            "case": False,
            "numeric": False,
            "math": 0,
            "minLength": 4,
            "maxLength": 6
        }
    }
    response = requests.post(url, json=data)
    task_id = response.json().get("taskId")

    if not task_id:
        raise Exception("Failed to create captcha task")

    time.sleep(10)
    result_url = "https://api.anti-captcha.com/getTaskResult"
    while True:
        result_response = requests.post(result_url, json={"clientKey": ANTI_CAPTCHA_API_KEY, "taskId": task_id})
        result = result_response.json()
        if result.get("status") == "ready":
            return result["solution"]["text"]
        time.sleep(5)

def check_aadhaar_validity(aadhaar_number):
    """Automate Aadhaar validity check."""
    options = Options()
    options.add_argument("--headless")  # This makes Chrome run in headless mode
    options.add_argument("--disable-gpu")  # Disables GPU acceleration for headless mode (optional)
    options.add_argument("--no-sandbox")  # Optional for running in certain environments like Docker

    driver = webdriver.Chrome(options=options)  # Use the options when creating the WebDriver
    driver.get(AADHAAR_URL)

    try:
        wait = WebDriverWait(driver, 200)

        # Enter Aadhaar number
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "uid")))
        aadhaar_input = driver.find_element(By.NAME, "uid")
        aadhaar_input.send_keys(aadhaar_number)

        # Solve captcha
        for _ in range(5):
            captcha_image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='captcha']"))
            )
            captcha_base64 = captcha_image.get_attribute("src")
            if captcha_base64:
                break
            time.sleep(2)
        else:
            raise Exception("Failed to load captcha image")

        captcha_text = solve_captcha(captcha_base64)

        captcha_input = driver.find_element(By.NAME, "captcha")
        captcha_input.send_keys(captcha_text)

        proceed_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and contains(@class, "button_btn__HeAxz")]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", proceed_button)
        proceed_button.click()

        wait = WebDriverWait(driver, 200)

        # Wait for the next page or result element to appear
        result_element = WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'check-aadhaar-validity-response__cong'))
        )
        result_text = result_element.text.strip()
        
        if "exists" in result_text.lower():
            return {"message": "Aadhaar exists", "status": True}
        else:
            return {"message": "Aadhaar does not exist", "status": False}
        

    except Exception as e:
        return {"message": f"Error occurred: {e}", "status": False}

    finally:
        driver.quit()

@app.route('/check-aadhaar', methods=['POST'])
def check_aadhaar():
    """API endpoint to validate Aadhaar number."""
    data = request.get_json()
    aadhaar_number = data.get("aadhaar_number")

    if not aadhaar_number or len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
        return jsonify({"message": "Invalid Aadhaar number", "status": False}), 400

    result = check_aadhaar_validity(aadhaar_number)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
