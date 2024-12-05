
# from nltk.stem import WordNetLemmatizer
# import nltk
# import enchant

# nltk.download('wordnet')
# print(WordNetLemmatizer().lemmatize("dies"))

import spacy
nlp = spacy.load('en_core_web_sm')
print([token.lemma_ for token in nlp("explores")])