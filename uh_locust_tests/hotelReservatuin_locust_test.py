from locust import HttpUser, task, between
import random

class HotelReservationUser(HttpUser):
    wait_time = between(1, 3)  # User thought time 1-3 seconds
    
    def generate_user(self):
        """Generate random users"""
        user_id = random.randint(0, 500)
        return f"Cornell_{user_id}", "".join([str(user_id)]*10)
    
    def generate_dates(self):
        """Generate random dates"""
        in_date = random.randint(9, 23)
        out_date = in_date + random.randint(1, 5)
        
        in_date_str = f"2015-04-{in_date:02d}"
        out_date_str = f"2015-04-{out_date:02d}"
        return in_date_str, out_date_str
    
    def generate_location(self):
        """Generate random location"""
        lat = 38.0235 + (random.randint(0, 481) - 240.5)/1000.0
        lon = -122.095 + (random.randint(0, 325) - 157.0)/1000.0
        return lat, lon

    @task(40)
    def search_hotels(self):
        """Search for hotels (40% probability)"""
        in_date, out_date = self.generate_dates()
        lat, lon = self.generate_location()
        
        self.client.get(f"/hotels", params={
            "inDate": in_date,
            "outDate": out_date,
            "lat": str(lat),
            "lon": str(lon)
        })

    @task(39)
    def get_recommendations(self):
        """Get recommendations (39% probability)"""
        lat, lon = self.generate_location()
        req_type = random.choice(["dis", "rate", "price"])
        
        self.client.get(f"/recommendations", params={
            "require": req_type,
            "lat": str(lat),
            "lon": str(lon)
        })

    @task(5)
    def user_login(self):
        """User login (5% probability)"""
        username, password = self.generate_user()
        
        self.client.post(f"/user", params={
            "username": username,
            "password": password
        })

    @task(5)
    def make_reservation(self):
        """Book a room (5% probability)"""
        username, password = self.generate_user()
        in_date, out_date = self.generate_dates()
        hotel_id = random.randint(1, 80)
        
        self.client.post(f"/reservation", params={
            "inDate": in_date,
            "outDate": out_date,
            "hotelId": str(hotel_id),
            "customerName": username,
            "username": username,
            "password": password,
            "number": "1"
        })

    @task(11)
    def err_make_reservation(self):
        """Book a room (Missing inDate parameter)"""
        username, password = self.generate_user()
        out_date = self.generate_dates()[1]  # only obtain out_date
        hotel_id = random.randint(1, 80)

        with self.client.post(
            f"/reservation",
            params={
                "outDate": out_date,
                "hotelId": str(hotel_id),
                "customerName": username,
                "username": username,  
                "password": password,
                "number": "1"
            },
            catch_response=True,
            name="reservation_missing_date"
        ) as response:
            if response.status_code == 400:
                # The expected error situation is marked as success
                response.success()
                print(f"Expected error: {response.status_code}")
            else:
                # Unexpected status code, marked as failed
                response.failure(f"Unexpected status code: {response.status_code}")

        
