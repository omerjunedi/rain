# set up credentials and api call
import requests
import random
from secret import API_KEY, CITY_ID, CITY_NAME, ACCOUNT_SID, AUTH_TOKEN, SHAWTY_BAES_NUMBER, MY_TWILIO_NUMBER, CONFIRMATION_NUMBER, LATITUDE, LONGITUDE
from twilio.rest import Client
from time import strftime, localtime, sleep



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
def check_weather():

    BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather?id="
    complete_url = BASE_URL + CITY_ID + "&appid=" + API_KEY + "&units=metric"
    data = requests.get(complete_url).json()
    weather = data["weather"]
    forecast = weather[0]["main"]
    is_rainy = False
    # id's under 600 correspond to sometype of rain in OpenWeatherAPI
    if weather[0]["id"] < 600:
        is_rainy = True

    send_message(forecast, is_rainy)
    
# Old approach was to run the script at 8:00 AM and send message based on that, only problem is that it checks the current weather only. So if it rains later in the day,
# it won't send anything which sort of defeats the purpose of this. The new approach is to check the next 12 hours at intervals of 3-hours and send a message if it is forcasted
# to rain at any of those times. The text message also includes at which time it is forecasted to rain. 
def check_rain_next_12_hours():
    url: str = f"https://api.openweathermap.org/data/2.5/forecast?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}"
    data = requests.get(url).json()

    is_rainy = False
    for i in range(5):
        if data['list'][i]['weather'][0]['id'] < 600:
            is_rainy = True
            forecast = data['list'][i]['weather'][0]['main']
            time = strftime('%Y-%m-%d %H:%M:%S', localtime(data['list'][i]['dt']))
        
        send_message(forecast, is_rainy, time)




def send_message(forecast: str, is_rainy: bool, time: str = "Right Now!"):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    if is_rainy:
        quote, nickname = select_quote_and_name()
        message = client.messages.create(
            body=f"\n{quote}Please consider taking an umbrella. Forecast in {CITY_NAME}: {forecast} at {time}.\nI like you a lot {nickname} :)",
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
            body=f"Not raining today in {CITY_NAME} forecast is {forecast} at {time}",
            from_=MY_TWILIO_NUMBER,
            to=CONFIRMATION_NUMBER
        )

def main():
    check_rain_next_12_hours()

if __name__ == "__main__":
    main()