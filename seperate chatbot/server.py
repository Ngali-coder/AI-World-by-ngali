from flask import Flask, request, jsonify, render_template
import utils
from utils import get_response, predict_class, predict_classs
import re, json
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_get():
    return render_template("base.html")


lemmatizer = WordNetLemmatizer()
with open("./intents.json", 'r') as file:
    intents = json.load(file)


@app.route('/predict', methods=['POST'])
def predict():
    text = request.get_json().get("message")
    ints = predict_class(text)
    response = get_response(ints, intents)
    message = {"answer": response}
    return jsonify(message)



if __name__ == "__main__":
    print("Starting Python Flask Server For chatbot...")
    app.run(debug=True)
