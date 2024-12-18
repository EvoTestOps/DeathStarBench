from locust import HttpUser, task, between
import random
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class HotelReservationUser(HttpUser):
    wait_time = between(2, 5)
    
    def on_start(self):
        self.user_id = random.randint(0, 500)
        self.username = f"Cornell_{self.user_id}"
        self.password = str(self.user_id) * 10
        
        # Test connection on startup
        try:
            with self.client.get("/hotels", 
                params={
                    "inDate": "2015-04-09",
                    "outDate": "2015-04-10",
                    "lat": "37.7749",
                    "lon": "-122.4194"
                },
                catch_response=True) as response:
                if response.status_code == 200:
                    logger.info("Successfully connected to hotel service")
                else:
                    logger.error(f"Initial connection test failed: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"Connection error during startup: {str(e)}")

    def generate_dates(self):
        in_date = random.randint(9, 23)
        out_date = random.randint(in_date + 1, 24)
        
        in_date_str = f"2015-04-{'0' if in_date <= 9 else ''}{in_date}"
        out_date_str = f"2015-04-{'0' if out_date <= 9 else ''}{out_date}"
        
        return in_date_str, out_date_str
    
    def generate_location(self):
        lat = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
        lon = -122.095 + (random.randint(0, 325) - 157.0) / 1000.0
        return lat, lon

    @task(600)
    def search_hotels(self):
        params = {
            "inDate": "2015-04-09",
            "outDate": "2015-04-10",
            "lat": "37.7749",
            "lon": "-122.4194"
         }
    
        with self.client.get("/hotels", params=params, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(390)
    def get_recommendations(self):
        lat, lon = self.generate_location()
        requirement = random.choices(["dis", "rate", "price"], weights=[0.33, 0.33, 0.34])[0]
        
        try:
            with self.client.get(
                "/recommendations",
                params={
                    "require": requirement,
                    "lat": str(lat),
                    "lon": str(lon)
                },
                catch_response=True,
                timeout=10
            ) as response:
                if response.status_code == 200:
                    response.success()
                    logger.debug("Recommendations retrieved successfully")
                else:
                    logger.error(f"Recommendations failed: HTTP {response.status_code}")
                    response.failure(f"HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"Recommendations request failed: {str(e)}")

    @task(5)
    def user_login(self):
        try:
            with self.client.post(
                "/user",
                params={
                    "username": self.username,
                    "password": self.password
                },
                catch_response=True,
                timeout=10
            ) as response:
                if response.status_code == 200 and "Login successfully" in response.text:
                    response.success()
                    logger.debug(f"Login successful for user {self.username}")
                else:
                    error_msg = f"Login failed: HTTP {response.status_code}"
                    logger.error(error_msg)
                    response.failure(error_msg)
        except Exception as e:
            logger.error(f"Login request failed: {str(e)}")

    @task(5)
    def make_reservation(self):
        in_date, out_date = self.generate_dates()
        hotel_id = str(random.randint(1, 80))
        
        try:
            with self.client.post(
                "/reservation",
                params={
                    "customerName": self.username,
                    "username": self.username,
                    "password": self.password,
                    "hotelId": hotel_id,
                    "inDate": in_date,
                    "outDate": out_date,
                    "number": "1"
                },
                catch_response=True,
                timeout=10
            ) as response:
                if response.status_code == 200 and "Reserve successfully" in response.text:
                    response.success()
                    logger.debug(f"Reservation successful for hotel {hotel_id}")
                else:
                    error_msg = f"Reservation failed: HTTP {response.status_code}"
                    logger.error(error_msg)
                    response.failure(error_msg)
        except Exception as e:
            logger.error(f"Reservation request failed: {str(e)}")
