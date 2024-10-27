import random
from locust import HttpUser, TaskSet, task, between
from faker import Faker

# Faker instance for generating random data
fake = Faker()

class OTPTasks(TaskSet):
    phone_number = None
    national_code = None
    otp_code = None

    @task
    def send_otp(self):
        """Simulate sending an OTP."""
        # Generate random phone number and national code
        self.phone_number = fake.msisdn()[3:14]  # Use last 11 digits to match the format
        self.national_code = fake.ssn()

        # Send OTP request
        response = self.client.post("/otp/send/", json={
            "phone_number": self.phone_number,
            "national_code": self.national_code
        })

        if response.status_code == 200:
            print("OTP sent successfully.")
        elif response.status_code == 400:
            print("Validation error: Phone and national code do not match.")
        elif response.status_code == 429:
            print("Too many OTP requests.")
        else:
            print(f"Unexpected status code: {response.status_code}")

    @task
    def verify_otp(self):
        """Simulate verifying the OTP sent in `send_otp`."""
        if not self.phone_number or not self.national_code:
            print("Skipping OTP verification as no OTP was sent.")
            return

        # Normally, we’d extract the OTP code from an SMS or log, but here, assume a random OTP.
        # Replace `123456` with a dynamic response if available.
        self.otp_code = "123456"  # Replace with real OTP if logging is available

        response = self.client.post("/otp/verify/", json={
            "phone_number": self.phone_number,
            "otp_code": self.otp_code
        })

        if response.status_code == 200:
            print("OTP verified successfully.")
        elif response.status_code == 400:
            print("Invalid or expired OTP.")
        elif response.status_code == 404:
            print("User does not exist.")
        else:
            print(f"Unexpected status code: {response.status_code}")

class WebsiteUser(HttpUser):
    tasks = [OTPTasks]
    wait_time = between(1, 3)  # Wait time between each task to simulate realistic load
    host = "http://192.168.19:8000"  # Replace with your Django server URL if differ=ent
