import json 
import os
import nltk 
from nltk.stem import WordNetLemmatizer

# Initialize NLTK components
lemmatizer = WordNetLemmatizer()
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)


intents = json.load(open(r"app\Backend\utils\intents.json"))
seq_flow = json.load(open(r"app\Backend\utils\conversational_flow.json"))


def process_text(text):
    ignore_symbol = [',','!','.',';']
    tokens = nltk.word_tokenize(text.lower())
    return [lemmatizer.lemmatize(token) for token in tokens if token not in ignore_symbol]



def check_matches(pattrens,user_input):
    pattrens = set(process_text(pattrens))
    user_input = set(process_text(user_input))
    return pattrens.issubset(user_input)


def get_intent_by_tag(tag):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return intent
    return None


def get_intent_by_context_filter(context_filter):
    matching_filter = []
    for intent in intents["intents"]:
        if intent.get("context_filter") == context_filter:
            matching_filter.append(intent)
    return matching_filter
    