import spacy
import nltk
from flask import Flask, request, jsonify, render_template


from nltk.tokenize import word_tokenize # "tokenisation" découpage de  phrase en mots
from nltk.tag import pos_tag            # POS tagging, identifie la grammaire des mots 

#nltk.download('popular')                # ensemble de ressource populairee 
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger_eng')

class LZbot :

    def __init__(self):
        self.greeting_keywords = ['hello', 'hi', 'hey', 'yo','greetings', 'hy']
        self.feeling_asking = ['how are you', 'okay', 'feel'] #?, 'how do you feel ?', 'are you okay ?', 'how are you', 'how do you feel', 'are you okay' ]
        self.help_asking = ['give', 'me', 'help']
        #help_asking_patterns = [["give", "help"], ["need", "help"], ["can", "you", "help"]]
        self.farewell_keywords = ['by', 'goodbye', 'bye', 'see you soon', 'see ya']
        self.doing_asking = ['what are you doing', 'what\'s new', 'wacho going on', 'what are you going on']
        self.injures = ['ugly', 'dumb', 'idiot', 'son of a', 'useless']
        self.thanks = ['thank you', 'thanks', 'thanksfull', 'thanks you very much']


    def preprocess(self, input_sentence) :
        """
        Tokenize une phrase et, tag chaque mot selon
        sa classe grammaticale et, retourne une liste 
        de mot, et tag.
        """
        words = word_tokenize(input_sentence)
        pos_tags = pos_tag(words)
        return pos_tags

    def recognize_intent(self,tokens):
        """
        fonction d'analyse des paternes côté utilisateur.
        """
        
        tokens = [token.lower() for token, pos in tokens]
        sentence = " ".join(tokens)

        if any(token in self.greeting_keywords for token in tokens):
            return "greeting"

        elif any(kw in sentence for kw in self.feeling_asking):
            return "feeling_asks"

        elif any(token in self.injures for token in tokens):
            return "injures"

        elif any(token in self.farewell_keywords for token in tokens):
            return "farewell"

        elif any(sentences in sentence for sentences in self.doing_asking):
            return "doing"

        elif any(token in self.thanks for token in tokens):
            return "thanks"    

        elif any(token in self.help_asking for token in tokens):
            return "asking_help"

        return "unknown"

    def generate_response(self, intent) :
        """
        fonction de génération de réponse.
        """ 
        response = {
            "greeting": "Hello ! How can I help you ?",
            "feeling_asks": "I'm feeling good today, tell me how can I help you ?",
            "asking_help": "Here is a list of what you can do :\nNothing...",
            "injures": "Please, stay polite.",
            "farewell": "Bye ! I really look forward to seeing you again.",
            "doing": "I am waiting for your needs.",
            "thanks": "You're welcome friend !",
            "unknown": "Sorry, I cannot understand for the moment..."
        }
        return response.get(intent, response["unknown"])

    def awnser(self, input_sentence):
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