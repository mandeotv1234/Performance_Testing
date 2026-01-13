from locust import HttpUser, task, between
import pandas as pd
import random
import re
import logging
import json

# Setup detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Load CSV Data
try:
    search_df = pd.read_csv("search_data.csv")
    search_keywords = search_df['keyword'].tolist()
    
    employee_df = pd.read_csv("employee_data.csv")
    employee_data_list = employee_df.to_dict('records') # Convert to list of dicts
except Exception as e:
    logger.error(f"Error loading CSV data: {e}")
    search_keywords = ["Alice", "Bob"]
    employee_data_list = [{"firstName": "Test", "middleName": "User", "lastName": "1"}]

class OrangeHRMUser(HttpUser):
    wait_time = between(1, 3) 
    host = "http://34.171.145.96"

    def on_start(self):
        """Login and get CSRF Token"""
        self.client.verify = False 
        
        # 1. GET Login Page
        response = self.client.get("/web/index.php/auth/login")
        logger.info(f"Accessed Login Page: {response.status_code}")
        
        # Extract CSRF Token
        # Pattern 1: :token="&quot;...&quot;"
        token_search = re.search(r':token="&quot;(.+?)&quot;"', response.text)
        if token_search:
            self.token = token_search.group(1)
        else:
             # Pattern 2: input name="_token" value="..."
            token_search_fallback = re.search(r'name="_token" value="(.+?)"', response.text)
            if token_search_fallback:
                self.token = token_search_fallback.group(1)
            else:
                self.token = ""
                logger.error("CSRF Token not found!")

        # 2. POST Login
        login_response = self.client.post("/web/index.php/auth/validate", data={
            "_token": self.token,
            "username": "mandeotv",
            "password": "Vlchinsu1234*"
        })
        
        if "dashboard" in login_response.url:
             logger.info("Login Successful")
        else:
             logger.warning("Login might have failed, check response.")

    @task
    def user_flow(self):
        """
        Flow:
        1. Access Add Employee Page (UI Log)
        2. Create Employee (POST API with new data)
        3. Access View Employee List (UI Log)
        4. Search Employee (GET API)
        """
        
        # 1. Navigate to Add Employee Page
        resp_add_page = self.client.get(
            "/web/index.php/pim/addEmployee",
            name="Page: Add Employee"
        )
        logger.info(f"Accessed 'Add Employee' Page - Status: {resp_add_page.status_code}")

        # 2. Create Employee (POST API)
        # Select random employee data from CSV
        emp_data = random.choice(employee_data_list)
        payload = {
            "firstName": emp_data["firstName"],
            "middleName": emp_data["middleName"],
            "lastName": emp_data["lastName"],
            "empPicture": None,
            "employeeId": ""
        }
        
        # NOTE: Some apps require the CSRF token in headers for AJAX/API calls
        # We'll try adding it to headers if standard cookie handling isn't enough, 
        # but typically OrangeHRM might look for a cookie or a header "X-CSRF-TOKEN".
        # We will optimistically just send the JSON first, but if it fails (419), we might need headers.
        # Assuming typical Laravel/Symfony:
        headers = {
            "Content-Type": "application/json"
        }
        # If the token from login is needed for API calls (often distinct from form _token),
        # but usually session cookie handles auth. Let's see. 
        
        resp_create = self.client.post(
            "/web/index.php/api/v2/pim/employees",
            json=payload,
            headers=headers,
            name="API: Create Employee"
        )
        
        if resp_create.status_code in [200, 201]:
             logger.info(f"Created Employee: {emp_data['firstName']} {emp_data['lastName']} - Status: {resp_create.status_code}")
        else:
             logger.error(f"Failed to Create Employee: {resp_create.status_code} - Body: {resp_create.text[:100]}")


        # 3. Navigate to Employee List
        resp_list_page = self.client.get(
            "/web/index.php/pim/viewEmployeeList",
             name="Page: View Employee List"
        )
        logger.info(f"Accessed 'Employee List' Page - Status: {resp_list_page.status_code}")


        # 4. Search Employee (GET API)
        keyword = random.choice(search_keywords)
        resp_search = self.client.get(
            "/web/index.php/api/v2/pim/employees",
            params={
                "limit": 50,
                "offset": 0,
                "model": "detailed",
                "includeEmployees": "onlyCurrent",
                "sortField": "employee.firstName",
                "sortOrder": "ASC",
                "nameOrId": keyword
            },
            name="API: Search Employee"
        )
        
        # Log basic stats about search results
        try:
            data = resp_search.json()
            count = len(data.get('data', []))
            logger.info(f"Search '{keyword}' - Status: {resp_search.status_code} - Found: {count} records")
        except:
             logger.info(f"Search '{keyword}' - Status: {resp_search.status_code} - Response not JSON")
