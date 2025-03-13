from flask import Flask, request, jsonify, render_template
import requests
import spacy
import random
import re
from nltk.chat.util import Chat, reflections

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Define pairs of patterns and responses for conversational features
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how can I assist you today?",]
    ],
    [
        r"hi|hello|hey",
        ["Hello! How can I help you?", "Hi there! What can I do for you?", "Hey! How's it going?"]
    ],
    [
        r"what is your name?",
        ["I am a chatbot created to check the weather.", "You can call me WeatherWise Bot!"]
    ],
    [
        r"how are you?",
        ["I'm just a bunch of code, but thanks for asking!", "I'm doing great, thanks! How about you?"]
    ],
    [
        r"quit|bye",
        ["Bye! Have a great day!", "Goodbye! Take care!", "See you later!"]
    ],
    [
        r"ok|ok bye|okay",
        ["Anything else you would like to know",]
    ],
    [
        r"fine|nice|great",
        ["That's good to hear, anything I can help you with",]
    ],
        [
        r"no|nothing",
        ["Okay, Thankyou",]
    ],
    [
        r"Sumit",
        ["Sumit is a mad boy",]
    ],
    
]

def get_weather(city):
    """
    Fetches weather information for a given city using the OpenWeatherMap API.
    """
    api_key = '29878948ce69fb4a0b9edb3239fa1a67'  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        data = response.json()
        
        if data["cod"] == 200:  # Check if the response is successful
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temperature = main["temp"]
            return f"The temperature in {city} is {temperature}°C with {weather_desc}."
        else:
            return "City not found. Please check the city name and try again."
    except requests.exceptions.RequestException:
        return "Sorry, I couldn't fetch the weather information right now. Please try again later."

def extract_city(user_input):
    """
    Extracts a city name from the user's input using spaCy's Named Entity Recognition (NER).
    """
    doc = nlp(user_input)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE = Geopolitical Entity (e.g., cities, countries)
            return ent.text
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['input']
    
    # Check for weather query
    if "weather" in user_input.lower():
        city = extract_city(user_input)
        if city:
            weather_info = get_weather(city)
            return jsonify({"response": weather_info})
        return jsonify({"response": "I couldn't identify the city. Could you please specify it?"})
    
    # Handle conversational responses using NLTK
    chat = Chat(pairs, reflections)
    response = chat.respond(user_input)
    
    if response:
        return jsonify({"response": response})
    return jsonify({"response": "I'm sorry, I didn't understand that. Could you rephrase?"})

if __name__ == "__main__":
    app.run(debug=True)