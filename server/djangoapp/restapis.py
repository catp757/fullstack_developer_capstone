import requests
import os
from dotenv import load_dotenv

# This points to the .env file in the same folder as this script
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv()

backend_url = os.getenv("backend_url")

print("backend_url =", os.getenv("backend_url"))
print("sentiment_analyzer_url =", os.getenv("sentiment_analyzer_url"))

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    params = ""
    if (kwargs):
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"

    request_url = backend_url + endpoint + "?" + params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except BaseException:
        # If any error occurs
        print("Network exception occurred")


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")

# Add code for posting review


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        if response.status_code == 200:
            print("Review posted:", response.json())
            return True
        else:
            print("Failed to post review:", response.status_code, response.text)
            return False
    except Exception as e:
        print("Network exception occurred:", e)
        return False
