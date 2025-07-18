import spacy
import nltk

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

#nltk.download('popular')

# charger le model installé  :

def preprocess(input_sentence) :
    """
    
    """
    words = word_tokenize(input_sentence)
    pos_tags = pos_tag(words)
    return pos_tags


LZnlp = spacy.load('en_core_web_sm')

doc = LZnlp("this is a test")

print([(w.text, w.pos_) for w in doc])

doc1 = LZnlp("i love chatbots")

print([(w.text, w.pos_) for w in doc1])


# Définition des entrées : 

input_sentence = input("entrez votre texte : ")
processed_sentece = preprocess(input_sentence)
print(processed_sentece)