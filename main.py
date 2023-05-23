# set up credentials and api call
import requests
import random
from secret import API_KEY, CITY_ID, CITY_NAME, ACCOUNT_SID, AUTH_TOKEN
from twilio.rest import Client
BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather?id="



def select_quote_and_name() -> tuple(str):
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
    
    # id's under 600 correspond to sometype of rain in OpenWeatherAPI
    if weather[0]["id"] < 600:
        forecast = weather[0]["main"]
        send_message(forecast)

def send_message(forecast: str):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    quote, name = select_quote_and_name()
    message = client.messages.create(
        body=f"\n{quote}Please consider taking an umbrella. [Forecast in {CITY_NAME}: {forecast}]\nLove you {name}",
        from_="+18444410160",
        to="+12488803467"
    )
    print(message.sid)

def main():
    api_call()

if __name__ == "__main__":
    main()