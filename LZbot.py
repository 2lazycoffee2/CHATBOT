import spacy
import nltk
import random

import datetime

import unicodedata
import re
from rapidfuzz import fuzz


from flask import Flask, request, jsonify, render_template

from nltk.tokenize import word_tokenize # "tokenisation" découpage de  phrase en mots
from nltk.tag import pos_tag            # POS tagging, identifie la grammaire des mots 

#nltk.download('popular')                # ensemble de ressource populairee 
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger_eng')

class LZbot :

    def __init__(self):

        self.identity = ["who you are", "who are you", "your name",  "what is your name", "what’s your name", "who am I talking to", "are you a bot"]
        self.date_keywords = ['date']
        self.time_keywords = ['time', 'hour', 'clock']
        self.weather_keywords = ['weather', 'temperature']

        self.greeting_keywords = ['hello', 'hi', 'hey','greetings', 'hy']
        self.feeling_asking = ['how are you', 'okay', 'feel', 'how are'] #?, 'how do you feel ?', 'are you okay ?', 'how are you', 'how do you feel', 'are you okay' ]
        self.help_asking = ['give', 'me', 'help']
        #help_asking_patterns = [["give", "help"], ["need", "help"], ["can", "you", "help"]]
        self.farewell_keywords = ['by', 'goodbye', 'bye', 'see you soon', 'see ya']
        self.doing_asking = ['what are you doing', 'what\'s new', 'wacho going on', 'what are you going on']
        self.compliments = ['smart', 'inteligent', 'good bot', 'nice job', 'well done']
        self.injures = ['ugly', 'dumb', 'idiot', 'son of a', 'useless']
        self.thanks = ['thank', 'thanks', 'thanksfull', 'thanks you very much']


    def normalize(self, text):
        """
        normalisation, simplifie le texte 
        reçu en minuscule sans accents.
        """
        text = text.lower() # minuscule par défaut

        text = unicodedata.normalize('NFD', text)                           # décompose les accents
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')  # suppression des accents

        text = re.sub(r'[^\w\s]', '', text)                                # suppression de caractères spéciaux
        return text
  
    def is_similar(self, word1, word2):
        """
        fonction pour répondre malgré
        les erreurs utilisateurs.
        """
        len_avg = (len(word1) + len(word2)) / 2
        dynamic_threshold = 90 if len_avg > 6 else 80
        return fuzz.ratio(word1, word2) >= dynamic_threshold 

    def preprocess(self, input_sentence) :
        """
        Tokenize une phrase et, tag chaque mot selon
        sa classe grammaticale et, retourne une liste 
        de mot, et tag.
        """
        words = word_tokenize(self.normalize(input_sentence))
        pos_tags = pos_tag(words)
        return pos_tags

    def recognize_intent(self,tokens):
        """
        fonction d'analyse des paternes côté utilisateur.
        """
        
        tokens = [token.lower() for token, pos in tokens]
        sentence = " ".join(tokens)

        if any(self.is_similar(token, kw) for token in tokens for kw in self.thanks):
                    return "thanks"
        elif any(self.is_similar(kw, sentence)for kw in self.identity):
            return "identity"
        
        elif any(self.is_similar(token, kw) for token in tokens for kw in self.compliments):
            return "compliments"
        
        elif any(self.is_similar(token, kw) for token in tokens for kw in self.greeting_keywords):
            return "greeting"

        elif any(self.is_similar(token, kw) for token in tokens for kw in self.date_keywords):
            return "get_date"

        elif any(self.is_similar(token, kw) for token in tokens for kw in self.time_keywords):
            return "get_time"

        elif any(self.is_similar(token, kw) for token in tokens for kw in self.weather_keywords):
            return "get_weather"

        elif any(self.is_similar(kw, sentence) for kw in self.feeling_asking):
            return "feeling_asks"

        elif any(self.is_similar(token, inj) for token in tokens for inj in self.injures):
            return "injures"

        elif any(self.is_similar(token, kw) for token in tokens for kw in self.farewell_keywords):
            return "farewell"

        elif any(self.is_similar(phrase, sentence) for phrase in self.doing_asking):
            return "doing"

        elif any(self.is_similar(token, kw) for token in tokens for kw in self.help_asking):
            return "asking_help"

        return "unknown"

    def generate_response(self, intent) :
        """
        fonction de génération de réponse
        en fonction de l'entrée utilisateur.
        """ 
        response = {
            "identity" : ["I am LZbot, made by LazyCoffee, here is his github : https://github.com/2lazycoffee2", "I am a virtual assistant. A simple ChatBot model.", "I am LZbot, happy to help you !" ],
            "greeting": ["Hello ! How can I help you ?", "Hey Hey, ready to work ?", "Hello, Your assistant is ready !"],
            "feeling_asks": ["I'm feeling good today, tell me how can I help you ?", "I am fine, thank you. I hope you're good to !", "Everything is fine for me, tell me how can I help you ?"],
            "asking_help": ["Here is a list of what you can do :\nNothing...", "You asked for some help ! Here is your possibilities : \n"],
            "injures": ["Please, stay polite.", "Respect, do you know what is it ?", "Hey ! That's not cool.", "Be respectfull please."],
            "compliments":["I do my work sir !", "Here for you !", "This is just my job"],
            "farewell": "Bye ! I really look forward to seeing you again.",
            "doing": ["I am waiting for your instructions.", "I'm on the net. Tell me how can I help you ? "],
            "thanks": ["You're welcome friend !", "No problem !", "You're welcome."],
            "unknown": ["Sorry, I cannot understand for the moment...",  "I don't get it, please, retry."]
        }
        if intent == "get_date":
            return f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}."
        elif intent == "get_time":
            return f"The current time is {datetime.datetime.now().strftime('%H:%M')}."
        return random.choice(response.get(intent, response["unknown"]))

    def awnser(self, input_sentence):
        """
        fonction de réponse. Traite l'entrée
        et, réponds.
        """
        processed_sentence = self.preprocess(input_sentence)
        intent = self.recognize_intent(processed_sentence)
        response = self.generate_response(intent)
        return response

#LZnlp = spacy.load('en_core_web_sm')    # Chargement du modèle en anglais pour les premiers tests
#doc = LZnlp("this is a test")   
#print([(w.text, w.pos_) for w in doc])  # Print chaque token.
#doc1 = LZnlp("i love chatbots")
#print([(w.text, w.pos_) for w in doc1])


app = Flask(__name__)
bot = LZbot()
@app.route('/')
def home():
    """
    Renvoie la page index.html
    """
    return render_template('index.html')

@app.route('/chat', methods = ['POST'])
def chat():
    user_input = request.json.get('message')
    response = bot.awnser(user_input)
    return jsonify({'response':response})

   # fetch('https//127.0.0.1:5000/chat'),


if __name__ == '__main__':
    app.run(debug = True)

#while True :
#    user_sentence = input("enter your sentence : ")
#    bot_response = LZbot(user_sentence)
#    print("LZbot :",bot_response)