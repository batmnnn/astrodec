from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import swisseph as swe
import datetime
import random

app = Flask(__name__)

# Astrology part
def get_astrological_sign(birthdate):
    jd = swe.julday(birthdate.year, birthdate.month, birthdate.day)
    sun = swe.calc_ut(jd, swe.SUN)[0][0]  # Get Sun position
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return signs[int(sun // 30)]

# Cards part
def shuffle_and_draw(deck):
    random.shuffle(deck)
    return deck.pop()

# Tarot part
def get_tarot_card():
    tarot_deck = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
                  "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
                  "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
                  "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement",
                  "The World"]
    random.shuffle(tarot_deck)
    return tarot_deck.pop()

# Decision making part
def make_decision(birthdate):
    sign = get_astrological_sign(birthdate)
    
    # Standard deck of cards
    deck = list(range(1, 53))
    card = shuffle_and_draw(deck)
    
    # Tarot card
    tarot_card = get_tarot_card()
    
    decision = (f"Astrological Sign: {sign}. Card Drawn: {card}. "
                f"Tarot Card: {tarot_card}. Decision: {'Yes' if card % 13&3&7 == 0 else 'No'}.")
    return decision

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_decision', methods=['POST'])
def get_decision():
    data = request.form
    birthdate = datetime.datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
    decision = make_decision(birthdate)
    return jsonify({'decision': decision})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
