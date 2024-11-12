import json
import os 
import nltk
from nltk.stem import WordNetLemmatizer
import random
from playsound import *

obj = SoundInit()
# Initialize NLTK components
lemmatizer = WordNetLemmatizer()
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)


#path 
path = r"C:\AI\new journey\the fastest journey\programming\Genius-algorithims\app\Backend\utils"
# Load the JSON files
def load_data():
    with open(os.path.join(path,'intents.json'), 'r') as file:
        intents = json.load(file)
    with open(os.path.join(path,'conversational_flow.json'), 'r') as file:
        flow = json.load(file)
    return intents, flow

# Preprocess input text
def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

# Check if pattern matches user input
def pattern_matches(pattern, user_input):
    pattern_tokens = set(preprocess(pattern))
    input_tokens = set(preprocess(user_input))
    return pattern_tokens.issubset(input_tokens)

# Get intent by tag
def get_intent_by_tag(tag, intents_data):
    for intent in intents_data["intents"]:
        if intent["tag"] == tag:
            return intent
    return None

# Get intents by context filter
def get_intents_by_context_filter(context_filter, intents_data):
    matching_intents = []
    for intent in intents_data["intents"]:
        if intent.get("context_filter") == context_filter:
            matching_intents.append(intent)
    return matching_intents

# Find matching intent for the current context
def find_matching_intent(user_input, 
                         current_context, intents_data, flow_data):
    # Handle greeting context
    if current_context == "greeting":
        # First check for greeting patterns
        greeting_intent = get_intent_by_tag("greeting", intents_data)
        if greeting_intent:
            for pattern in greeting_intent["patterns"]:
                if pattern_matches(pattern, user_input):
                    return greeting_intent
        
        # After greeting, check for confirm_identity patterns
        confirm_intent = get_intent_by_tag("confirm_identity", intents_data)
        if confirm_intent:
            for pattern in confirm_intent["patterns"]:
                if pattern_matches(pattern, user_input):
                    return confirm_intent
                    
        # If no confirm_identity match, check deny_identity patterns
        deny_intent = get_intent_by_tag("deny_identity", intents_data)
        if deny_intent:
            for pattern in deny_intent["patterns"]:
                if pattern_matches(pattern, user_input):
                    return deny_intent
        return None

    # For other contexts, check intents with matching context_filter
    matching_intents = get_intents_by_context_filter(current_context, intents_data)
    for intent in matching_intents:
        for pattern in intent["patterns"]:
            if pattern_matches(pattern, user_input):
                return intent
    return None

# Get next context based on the matched intent
def get_next_context(current_context, matched_intent, flow_data):
    if current_context in flow_data:
        intent_tag = matched_intent["tag"]
        if intent_tag in flow_data[current_context]:
            return flow_data[current_context][intent_tag]
    return None

def chat():
    intents_data, flow_data = load_data()
    current_context = "greeting"
    
    print("Bot: Hello! How can I assist you today?")
    
    
    while True:
        user_input = input("You: ")
        
        # Find matching intent for current context
        matched_intent = find_matching_intent(user_input, current_context, intents_data, flow_data)
        
        if matched_intent:
            # Get random response from matched intent
            response = random.choice(matched_intent["responses"])
            print(f"Bot: {response}")
            obj.play_sound(response+".mp3")
            
            # Debug info
            print(f"Debug - Current context: {current_context}")
            print(f"Debug - Matched tag: {matched_intent['tag']}")
            
            # Check if call should end
            if matched_intent.get("call_handle") == "end":
                print("Bot: Thank you for your time. Goodbye!")
                break
            
            # Update context from flow data
            next_context = get_next_context(current_context, matched_intent, flow_data)
            if next_context:
                current_context = next_context
            elif next_context == "end_call":
                print("Bot: Thank you for your time. Goodbye!")
                break
            
            # If no next context from flow, use context_filter
            if not next_context and matched_intent.get("context_filter"):
                current_context = matched_intent["context_filter"]
        else:
            print("Bot: I'm sorry, I didn't understand that. Could you please rephrase?")
            print(f"Debug - Current context: {current_context}")
            if current_context in flow_data:
                print(f"Debug - Available tags: {list(flow_data[current_context].keys())}")

if __name__ == "__main__":
    chat() 