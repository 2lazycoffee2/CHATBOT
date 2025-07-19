import spacy
import nltk
from flask import Flask, request, jsonify


from nltk.tokenize import word_tokenize # "tokenisation" découpage de  phrase en mots
from nltk.tag import pos_tag            # POS tagging, identifie la grammaire des mots 

#nltk.download('popular')                # ensemble de ressource populairee 
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger_eng')


def preprocess(input_sentence) :
    """
    Tokenize une phrase et, tag chaque mot selon
    sa classe grammaticale et, retourne une liste 
    de mot, et tag.
    """
    words = word_tokenize(input_sentence)
    pos_tags = pos_tag(words)
    return pos_tags

def recognize_intent(tokens):
    """
    fonction d'analyse des paternes côté utilisateur.
    """
    greeting_keywords = ['hello', 'hi', 'hey', 'greetings']
    feeling_asking = ['how', 'are', 'you', 'okay', 'feel'] #?, 'how do you feel ?', 'are you okay ?', 'how are you', 'how do you feel', 'are you okay' ]
    help_asking = ['give', 'me', 'help']
    #help_asking_patterns = [["give", "help"], ["need", "help"], ["can", "you", "help"]]
    farewell_keywords = ['by', 'goodbye', 'bye', 'see you soon', 'see ya']
    doing_asking = ['what', 'are', 'you', 'doing']

    injures = ['ugly', 'dumb', 'idiot', 'son of a', 'useless']
    
    tokens = [token.lower() for token, pos in tokens]
    if any(token in greeting_keywords for token in tokens):
        return "greeting"
    elif any(token in feeling_asking for token in tokens):
        return "feeling_asks"
    elif any(token in help_asking for token in tokens):
        return "asking_help"
    elif any(token in injures for token in tokens):
        return "injures"
    elif any(token in farewell_keywords for token in tokens):
        return "farewell"
    elif any(token in doing_asking for token in tokens):
        return "doing"
        
    return "unknown"

def generate_response(intent) :
    """
    fonction de génération de réponse.
    """ 
    if intent == "greeting":
        return "Hello ! How can i help you ?"
    elif intent == "feeling_asks" :
        return "Im feeling good today, tell me how can i help you ?"
    elif intent == "asking_help" :
        return "here is a list of what you can do : \nnothing... "
    elif intent == "injures":
        return "please, stay polite."
    elif intent == "farewell":
        return "Bye ! I realy look forward to seing you again."
    elif intent == "doing":
        return "I am waiting for your needs "
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


app = Flask(__name__)
@app.route('/')
def home():
    return "WELCOME TO LZBOT, FEEL FREE TO TALK WITH ME !"

@app.route('/chat', methods = ['POST'])
def chat():
    user_input = request.json.get('message')
    response = LZbot(user_input)
    return jsonify({'response':response})

    fetch('https//127.0.0.1:5000/chat'),


if __name__ == '__main__':
    app.run(debug = True)

#while True :
#    user_sentence = input("enter your sentence : ")
#    bot_response = LZbot(user_sentence)
#    print("LZbot :",bot_response)