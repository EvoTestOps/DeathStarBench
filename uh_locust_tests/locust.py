from locust import HttpUser, task, between
import random
import time
import uuid

class HotelReservationUser(HttpUser):
    wait_time = between(1, 3)

    def generate_user(self):
        """Match official test's user generation"""
        user_id = random.randint(0, 500)
        return f"Cornell_{user_id}", "".join([str(user_id)]*10)

    def generate_dates(self):
        """Match official test's date generation"""
        in_date = random.randint(9, 23)
        out_date = random.randint(in_date + 1, 24)
        
        in_date_str = f"2015-04-{'0' if in_date <= 9 else ''}{in_date}"
        out_date_str = f"2015-04-{'0' if out_date <= 9 else ''}{out_date}"
        return in_date_str, out_date_str

    def generate_location(self):
        """Match official test's location generation"""
        lat = 38.0235 + (random.randint(0, 481) - 240.5)/1000.0
        lon = -122.095 + (random.randint(0, 325) - 157.0)/1000.0
        return lat, lon

    def get_trace_headers(self):
        """Generate Jaeger compatible trace headers"""
        trace_id = format(random.getrandbits(64), '016x')
        span_id = format(random.getrandbits(64), '016x')
        parent_span_id = format(random.getrandbits(64), '016x')
        
        # Uber-Trace-Id format: trace-id:span-id:parent-span-id:flags
        uber_trace_id = f"{trace_id}:{span_id}:{parent_span_id}:1"
        
        headers = {
            'Uber-Trace-Id': uber_trace_id,
            'X-B3-TraceId': trace_id,
            'X-B3-SpanId': span_id,
            'X-B3-ParentSpanId': parent_span_id,
            'X-B3-Sampled': '1',
            'X-Request-Id': str(uuid.uuid4()),
            'jaeger-debug-id': str(uuid.uuid4()),
            'jaeger-baggage': 'service=hotel-reservation-loadtest'
        }
        return headers

    @task(600)  # 60% -> 600
    def search_hotels(self):
        """Search hotels endpoint"""
        in_date, out_date = self.generate_dates()
        lat, lon = self.generate_location()
        
        headers = self.get_trace_headers()
        
        with self.client.get(
            "/hotels",
            params={
                "inDate": in_date,
                "outDate": out_date,
                "lat": str(lat),
                "lon": str(lon)
            },
            headers=headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Search failed with status code: {response.status_code}")

    @task(390)  # 39% -> 390
    def get_recommendations(self):
        """Get recommendations endpoint"""
        lat, lon = self.generate_location()
        req_type = random.choices(["dis", "rate", "price"], weights=[0.33, 0.33, 0.34])[0]
        
        headers = self.get_trace_headers()
        
        with self.client.get(
            "/recommendations",
            params={
                "require": req_type,
                "lat": str(lat),
                "lon": str(lon)
            },
            headers=headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Recommendations failed with status code: {response.status_code}")

    @task(5)  # 0.5% -> 5
    def user_login(self):
        """User login endpoint"""
        username, password = self.generate_user()
        
        headers = self.get_trace_headers()
        
        with self.client.get(
            "/user",
            params={
                "username": username,
                "password": password
            },
            headers=headers,
            catch_response=True
        ) as response:
            if "Login successfully" in response.text:
                response.success()
            else:
                response.failure("Login failed")

    @task(5)  # 0.5% -> 5
    def make_reservation(self):
        """Reservation endpoint"""
        username, password = self.generate_user()
        in_date, out_date = self.generate_dates()
        hotel_id = random.randint(1, 80)
        
        headers = self.get_trace_headers()
        
        with self.client.get(
            "/reservation",
            params={
                "inDate": in_date,
                "outDate": out_date,
                "hotelId": str(hotel_id),
                "customerName": username,
                "username": username,
                "password": password,
                "number": "1"
            },
            headers=headers,
            catch_response=True
        ) as response:
            if "Reserve successfully" in response.text:
                response.success()
            else:
                response.failure("Reservation failed")
