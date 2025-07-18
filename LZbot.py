import spacy
import nltk

from nltk.tokenize import word_tokenize # "tokenisation" découpage de  phrase en mots
from nltk.tag import pos_tag            # POS tagging, identifie la grammaire des mots 

#nltk.download('popular')                # ensemble de ressource populairee 
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger_eng')


def preprocess(input_sentence) :
    """
    Tokenize une ohrase et, tag chaque mot selon
    sa classe grammaticale et, retourne une liste 
    de mot, et tag.
    """
    words = word_tokenize(input_sentence)
    pos_tags = pos_tag(words)
    return pos_tags

def recognize_intent(tokens):
    greeting_keywords = ['hello', 'hi', 'hey', 'greetings']
    tokens = [token.lower() for token, pos in tokens]
    if any(token in greeting_keywords for token in tokens):
        return "greeting"
    return "unknown"

def generate_response(intent) : 
    if intent == "greeting":
        return "Hello ! How can i help you ?"
    else :
        return "sorry, i cannot understand for the moment..."

def LZbot(input_sentence):
    processed_sentence = preprocess(input_sentence)
    intent = recognize_intent(processed_sentence)
    response = generate_response(intent)
    return response

#LZnlp = spacy.load('en_core_web_sm')    # Chargement du modèle en anglais pour les premiers tests
#doc = LZnlp("this is a test")   
#print([(w.text, w.pos_) for w in doc])  # Print chaque token.
#doc1 = LZnlp("i love chatbots")
#print([(w.text, w.pos_) for w in doc1])

print("WELCOME TO LZBOT, FEEL FREE TO TALK WITH ME !")
while True :
    user_sentence = input("enter your sentence : ")
    bot_response = LZbot(user_sentence)
    print(bot_response)