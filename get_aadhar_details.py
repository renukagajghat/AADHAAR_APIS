# #working code without headless browser
# from flask import Flask, request, jsonify
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import requests
# import time
# import mysql.connector

# # Flask app
# app = Flask(__name__)

# # Anticaptcha API Key
# ANTI_CAPTCHA_API_KEY = "2f91f49e0d8cafd925798b03d4aed443"

# # Aadhaar Verification URL
# AADHAAR_URL = "https://myaadhaar.uidai.gov.in/check-aadhaar-validity/en"

# def save_filename_to_db(aadhar_number, gender, age_band, mobile_no, state):
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='',
#             database='education_schema'
#         )
#         cursor = connection.cursor()
#         insert_query = '''
#             INSERT INTO aadhar_details (aadhar_number, gender, age_band, mobile_no, state)
#             VALUES (%s, %s, %s, %s, %s)
#         '''
#         cursor.execute(insert_query, (aadhar_number, gender, age_band, mobile_no, state))
#         connection.commit()
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

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

# def wait_for_latest_captcha(driver, timeout=30):
#     """Wait for the latest CAPTCHA to fully load."""
#     try:
#         WebDriverWait(driver, timeout).until(
#             EC.presence_of_element_located((By.XPATH, "//img[@alt='captcha']"))
#         )
#         captcha_image = driver.find_element(By.XPATH, "//img[@alt='captcha']")

#         # Wait until the 'src' attribute stabilizes (indicates the CAPTCHA is fully loaded)
#         initial_src = captcha_image.get_attribute("src")
#         WebDriverWait(driver, timeout).until(
#             lambda d: captcha_image.get_attribute("src") != initial_src
#         )
#         time.sleep(2)  # Optional: slight delay to ensure complete load
#         return captcha_image.get_attribute("src")
#     except Exception as e:
#         raise Exception(f"Failed to load the latest CAPTCHA: {e}")

# def check_aadhaar_validity(aadhaar_number):
#     """Automate Aadhaar validity check."""
#     driver = webdriver.Chrome()  # Replace with appropriate WebDriver if not using Chrome
#     driver.get(AADHAAR_URL)

#     try:
#         wait = WebDriverWait(driver, 200)

#         # Enter Aadhaar number
#         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "uid")))
#         aadhaar_input = driver.find_element(By.NAME, "uid")
#         aadhaar_input.send_keys(aadhaar_number)

#         # Wait for and solve the latest CAPTCHA
#         captcha_base64 = wait_for_latest_captcha(driver)
#         captcha_text = solve_captcha(captcha_base64)

#         # Enter CAPTCHA and submit
#         captcha_input = driver.find_element(By.NAME, "captcha")
#         captcha_input.clear()
#         captcha_input.send_keys(captcha_text)

#         proceed_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and contains(@class, "button_btn__HeAxz")]'))
#         )
#         driver.execute_script("arguments[0].scrollIntoView(true);", proceed_button)
#         proceed_button.click()

#         # Wait for the result page
#         try:
#             result_element = WebDriverWait(driver, 20).until(
#                 EC.visibility_of_element_located((By.CLASS_NAME, 'check-aadhaar-validity-response__card'))
#             )
#         except Exception as e:
#             if "timeout" in str(e).lower():
#                 return {"message": "Technical issue with the site. Please try again later.", "status": False}
#             return {"message": "Failed to proceed due to an unknown site error.", "status": False}

#         # Extract details
#         details = driver.find_elements(By.CLASS_NAME, 'verify-display-field')
#         data = {}
#         for detail in details:
#             label = detail.find_element(By.CLASS_NAME, 'verify-display-field__label').text.strip()
#             value = detail.find_elements(By.TAG_NAME, 'span')[-1].text.strip()
#             if label == "Age Band":
#                 data['age_band'] = value
#             elif label == "Gender":
#                 data['gender'] = value
#             elif label == "State":
#                 data['state'] = value
#             elif label == "Mobile":
#                 data['mobile_no'] = value

#         if not data:
#             raise Exception("Failed to extract details from the result page")

#         # Save to DB
#         save_filename_to_db(aadhaar_number, data.get("gender"), data.get("age_band"), data.get('mobile_no'), data.get("state"))

#         return {"message": "Aadhaar details fetched successfully", "status": True, "data": data}

#     except Exception as e:
#         return {"message": f"Error occurred: {e}", "status": False}

#     finally:
#         driver.quit()

# @app.route('/get-aadhaar-details', methods=['POST'])
# def get_aadhaar_details():
#     """API endpoint to validate Aadhaar number."""
#     data = request.get_json()
#     aadhaar_number = data.get("aadhaar_number")

#     if not aadhaar_number or len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
#         return jsonify({"message": "Invalid Aadhaar number", "status": False}), 400

#     result = check_aadhaar_validity(aadhaar_number)
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)




#working code with headless browser
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import mysql.connector

# Flask app
app = Flask(__name__)

#setup chrome options
options = Options()
options.add_argument("--headless")  # Enable headless mode
options.add_argument("--disable-gpu")  # Disable GPU for headless mode
options.add_argument("--no-sandbox")  # Bypass OS security model (Linux)
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
service = Service(executable_path='/usr/local/bin/chromedriver')

# Anticaptcha API Key
ANTI_CAPTCHA_API_KEY = "2f91f49e0d8cafd925798b03d4aed443"

# Aadhaar Verification URL
AADHAAR_URL = "https://myaadhaar.uidai.gov.in/check-aadhaar-validity/en"

def save_filename_to_db(aadhar_number, gender, age_band, mobile_no, state):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='education_schema'
        )
        cursor = connection.cursor()
        insert_query = '''
            INSERT INTO aadhar_details (aadhar_number, gender, age_band, mobile_no, state)
            VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (aadhar_number, gender, age_band, mobile_no, state))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

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

def wait_for_latest_captcha(driver, timeout=30):
    """Wait for the latest CAPTCHA to fully load."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='captcha']"))
        )
        captcha_image = driver.find_element(By.XPATH, "//img[@alt='captcha']")

        # Wait until the 'src' attribute stabilizes (indicates the CAPTCHA is fully loaded)
        initial_src = captcha_image.get_attribute("src")
        WebDriverWait(driver, timeout).until(
            lambda d: captcha_image.get_attribute("src") != initial_src
        )
        time.sleep(2)  # Optional: slight delay to ensure complete load
        return captcha_image.get_attribute("src")
    except Exception as e:
        raise Exception(f"Failed to load the latest CAPTCHA: {e}")

def check_aadhaar_validity(aadhaar_number):
    """Automate Aadhaar validity check."""

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(AADHAAR_URL)

    try:
        wait = WebDriverWait(driver, 200)

        # Enter Aadhaar number
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "uid")))
        aadhaar_input = driver.find_element(By.NAME, "uid")
        aadhaar_input.send_keys(aadhaar_number)

        # Wait for and solve the latest CAPTCHA
        captcha_base64 = wait_for_latest_captcha(driver)
        captcha_text = solve_captcha(captcha_base64)

        # Enter CAPTCHA and submit
        captcha_input = driver.find_element(By.NAME, "captcha")
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)

        proceed_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and contains(@class, "button_btn__HeAxz")]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", proceed_button)
        proceed_button.click()

        # Wait for the result page
        try:
            result_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'check-aadhaar-validity-response__card'))
            )
        except Exception as e:
            if "timeout" in str(e).lower():
                return {"message": "Technical issue with the site. Please try again later.", "status": False}
            return {"message": "Failed to proceed due to an unknown site error.", "status": False}

        # Extract details
        details = driver.find_elements(By.CLASS_NAME, 'verify-display-field')
        data = {}
        for detail in details:
            label = detail.find_element(By.CLASS_NAME, 'verify-display-field__label').text.strip()
            value = detail.find_elements(By.TAG_NAME, 'span')[-1].text.strip()
            if label == "Age Band":
                data['age_band'] = value
            elif label == "Gender":
                data['gender'] = value
            elif label == "State":
                data['state'] = value
            elif label == "Mobile":
                data['mobile_no'] = value

        if not data:
            raise Exception("Failed to extract details from the result page")

        # Save to DB
        save_filename_to_db(aadhaar_number, data.get("gender"), data.get("age_band"), data.get('mobile_no'), data.get("state"))

        return {"message": "Aadhaar details fetched successfully", "status": True, "data": data}

    except Exception as e:
        return {"message": f"Error occurred: {e}", "status": False}

    finally:
        driver.quit()


@app.route('/get-aadhaar-details', methods=['POST'])
def get_aadhaar_details():
    """API endpoint to validate Aadhaar number."""
    data = request.get_json()
    aadhaar_number = data.get("aadhaar_number")

    if not aadhaar_number or len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
        return jsonify({"message": "Invalid Aadhaar number", "status": False}), 400

    result = check_aadhaar_validity(aadhaar_number)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)







