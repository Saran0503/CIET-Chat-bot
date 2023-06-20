import pandas as pd
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

# Read the Excel sheet data and convert the "Input" column to string type
df = pd.read_excel('C:/Users/MSI/Desktop/Book.xlsx', dtype={'Input': str})

# Convert the data into a list of tuples containing (input, response) pairs
conversations = df[['Input', 'Response']].apply(tuple, axis=1).tolist()


# Create a chatbot instance
chatbot = ChatBot('MyChatBot')

# Train the chatbot using the conversations from the Excel sheet
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Define stemmer and stop words
stemmer = SnowballStemmer("english")
stop_words = set(stopwords.words("english"))

# Create a Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    
    # Get the user input from the request
    inputText = request.json['inputText']
    #print('Input text:', inputText)

    
    # Preprocess user input
    tokens = word_tokenize(inputText.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]
    bow = Counter(stemmed_tokens)

    # Find the most common words in the bag of words
    common_words = [word for word, count in bow.most_common(5)]

    # Match user input with "Input" column in the Excel sheet
    max_percentage_match = 0
    matched_input = None
    for row in conversations:
        input_text = str(row[0]).lower()
        input_tokens = word_tokenize(input_text)
        input_stemmed_tokens = [stemmer.stem(token) for token in input_tokens if token not in stop_words]
        input_bow = Counter(input_stemmed_tokens)
        common_tokens = set(input_stemmed_tokens) & set(stemmed_tokens)
        if len(common_tokens) > 0:
            percentage_match = sum([input_bow[token] for token in common_tokens]) / sum(input_bow.values())
            if percentage_match > max_percentage_match:
                max_percentage_match = percentage_match
                matched_input = input_text
                bot_response = row[1]

    if matched_input is None:
        bot_response = "Sorry, I can't understand. Could you please provide more information about that?"
        
    # Return the chatbot response as a JSON object
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)