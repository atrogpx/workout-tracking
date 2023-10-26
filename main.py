import requests
from datetime import datetime
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

SHEET_USERNAME = os.environ["SHEET_USERNAME"]
SHEET_PROJECTNAME = "workoutsTracking"
SHEET_NAME = "workouts"
sheet_endpoint = f"https://api.sheety.co/{SHEET_USERNAME}/{SHEET_PROJECTNAME}/{SHEET_NAME}"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}
exercise_text = input("Tell me which exercises you did: ")
parameters = {
    "query": exercise_text,
    "gender": "female",
    "weight_kg": 70,
    "height_cm": 174,
    "age": 20
}
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
      "workout": {
        "date": today_date,
        "time": now_time,
        "exercise": exercise["user_input"].title(),
        "duration": exercise["duration_min"],
        "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)
    print(sheet_response.text)
