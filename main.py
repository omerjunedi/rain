# set up credentials and api call
import requests
import random
from secret import API_KEY, CITY_ID, CITY_NAME, ACCOUNT_SID, AUTH_TOKEN, SHAWTY_BAES_NUMBER, MY_TWILIO_NUMBER, CONFIRMATION_NUMBER
from twilio.rest import Client
import time
BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather?id="



def select_quote_and_name() -> tuple[str]:
    with open("quotes.txt", 'r') as file:
        quote = file.readlines()

    with open("nicknames.txt", 'r') as file:
        nickname = file.readlines()
    
    s_quote = random.choice(quote).replace("â€™", "'")
    s_name = random.choice(nickname)

    return s_quote, s_name

# make api call
# get relavent data from json object
def api_call():

    complete_url = BASE_URL + CITY_ID + "&appid=" + API_KEY + "&units=metric"
    data = requests.get(complete_url).json()
    weather = data["weather"]
    forecast = weather[0]["main"]
    is_rainy = False
    # id's under 600 correspond to sometype of rain in OpenWeatherAPI
    if weather[0]["id"] < 600:
        is_rainy = True

    send_message(forecast, is_rainy)
    

def send_message(forecast: str, is_rainy: bool):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    if is_rainy:
        quote, nickname = select_quote_and_name()
        message = client.messages.create(
            body=f"\n{quote}Please consider taking an umbrella. [Forecast in {CITY_NAME}: {forecast}]\nI like you a lot {nickname} :)",
            from_=MY_TWILIO_NUMBER,
            to=SHAWTY_BAES_NUMBER
        )
        time.sleep(10)
        if message.status != "failed" and message.status != "canceled" and message.status != "undelivered":
            confimation_message = client.messages.create(
                body=f"Message sent to SC: {message.body}\n Date: {message.date_sent}",
                from_=MY_TWILIO_NUMBER,
                to=CONFIRMATION_NUMBER
            )
        else:
            with open("errors.txt", 'a') as f:
                f.write(f"{message.error_code} | {message.error_message} | {message.date_created}")
    else:
        message = client.messages.create(
            body=f"Not raining today in {CITY_NAME} forecast is {forecast}",
            from_=MY_TWILIO_NUMBER,
            to=CONFIRMATION_NUMBER
        )

def main():
    api_call()

if __name__ == "__main__":
    main()