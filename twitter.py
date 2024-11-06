from requests_oauthlib import OAuth1Session
import os
import json
import logging
consumer_key = "DONT LOOK HERE"
consumer_secret = "DONT LOOK HERE TOO!"

token_file = "access_tokens.json"
weather_file = "weather_data.json"
log_file = "tweet_log.txt"

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler(log_file)
                    ])

def get_access_tokens():
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    logging.info(f"Please go here and authorize: {authorization_url}")
    verifier = input("Paste the PIN here: ")

    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    with open(token_file, "w") as file:
        json.dump(oauth_tokens, file)

    return oauth_tokens

def load_access_tokens():
    if os.path.exists(token_file):
        with open(token_file, "r") as file:
            return json.load(file)
    else:
        return get_access_tokens()

tokens = load_access_tokens()
access_token = tokens["oauth_token"]
access_token_secret = tokens["oauth_token_secret"]

with open(weather_file, "r") as file:
    weather_data = json.load(file)
    
tweet_text = (
    f"📍 {weather_data['city_name']}, {weather_data['region']}, {weather_data['country']} 🇮🇳\n"
    f"🌡️ Temp: {weather_data['temp_c']}°C\n"
    f"🌦️ Condition: {weather_data['condition_text']}\n"
    f"💨 Wind: {weather_data['wind_speed_kph']} kph\n"
    f"💧 Humidity: {weather_data['humidity']}%\n"
    f"🌅 Sunrise: {weather_data['sunrise']} | 🌇 Sunset: {weather_data['sunset']}\n"
    f"🌧️ Rain Chance: {weather_data['chance_of_rain']}%\n"
    f"Time: {weather_data['localtime']}"
)

logging.info(f"Tweet Text: {tweet_text}")

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

payload = {"text": tweet_text}
response = oauth.post("https://api.twitter.com/2/tweets", json=payload)

if response.status_code != 201:
    raise Exception(f"Request returned an error: {response.status_code} {response.text}")

logging.info(f"Response code: {response.status_code}")
#logging.info(f"Response JSON: {json.dumps(response.json(), indent=4)}")
