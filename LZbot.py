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


#LZnlp = spacy.load('en_core_web_sm')    # Chargement du modèle en anglais pour les premiers tests
#doc = LZnlp("this is a test")   
#print([(w.text, w.pos_) for w in doc])  # Print chaque token.
#doc1 = LZnlp("i love chatbots")
#print([(w.text, w.pos_) for w in doc1])


# Définition des entrées : 

input_sentence = input("entrez votre texte : ")
processed_sentence = preprocess(input_sentence)
print(processed_sentence)