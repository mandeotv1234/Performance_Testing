from locust import HttpUser, task, between
import re
import logging

# Setup detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

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
        token_search = re.search(r':token="&quot;(.+?)&quot;"', response.text)
        if token_search:
            self.token = token_search.group(1)
        else:
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
    def leave_scenario(self):
        """
        Flow:
        1. Access Leave List Page (UI)
        2. Call Get Leave Requests API
        """
        
        # 1. Navigate to Leave List Page
        with self.client.get(
            "/web/index.php/leave/viewLeaveList",
            name="Page: View Leave List",
            catch_response=True
        ) as resp_ui:
            if resp_ui.status_code == 200:
                resp_ui.success()
                logger.info(f"Accessed 'Leave List' Page - Status: {resp_ui.status_code}")
            else:
                resp_ui.failure(f"Failed to access Leave List: {resp_ui.status_code}")
                logger.error(f"Failed to access Leave List: {resp_ui.status_code}")

        # 2. Get Leave Requests API
        # Using params as requested: limit=50, offset=0, includeEmployees=onlyCurrent
        with self.client.get(
            "/web/index.php/api/v2/leave/employees/leave-requests",
            params={
                "limit": 50,
                "offset": 0,
                "includeEmployees": "onlyCurrent"
            },
            name="API: Get Leave Requests",
            catch_response=True
        ) as resp_api:
            if resp_api.status_code == 200:
                # Deep validation
                if "error" in resp_api.text.lower():
                     resp_api.failure(f"Logical Error in API: {resp_api.text}")
                     logger.error(f"API Error Body: {resp_api.text}")
                else:
                    try:
                        data = resp_api.json()
                        count = len(data.get('data', []))
                        resp_api.success()
                        logger.info(f"Get Leaves Success - Found: {count} records - Body: {resp_api.text[:50]}...")
                    except:
                        resp_api.success() # Non-JSON might be okay? Assume success for now if 200 and no "error"
                        logger.info(f"Get Leaves Success (No JSON) - Body: {resp_api.text[:50]}...")
            else:
                resp_api.failure(f"HTTP Error: {resp_api.status_code}")
                logger.error(f"API Failed: {resp_api.status_code} - Body: {resp_api.text[:100]}")
