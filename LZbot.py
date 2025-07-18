import spacy
import nltk

#nltk.download('popular')

# charger le model installé  :

LZnlp = spacy.load('en_core_web_sm')

doc = LZnlp("this is a test")

print([(w.text, w.pos_) for w in doc])

doc1 = LZnlp("i love chatbots")

print([(w.text, w.pos_) for w in doc1])
