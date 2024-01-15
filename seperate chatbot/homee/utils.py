import pickle
import random
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import mysql.connector as sql
# from tensorflow.keras.models import load_model

from tensorflow.python.keras.models import load_model

lemmatizer=WordNetLemmatizer()
with open("intents.json", 'r') as file:
    intents = json.load(file)

words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentences(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentences(sentence)
    bag=[0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word==w:
                bag[i]=1
    return np.array(bag)



# def get_response(intents_json):
#     # tag=intents_list[0]['intent']
#     list_of_intents = intents_json['intents']
#     for i in list_of_intents:
#         result = random.choice(i['responses'])
#         break
#     return result
#         # if i['tag'] == tag:






def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD=0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]],'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag=intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result




def predict_classs(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD=0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append(classes[r[0]])
    return return_list


# def products(text):
#     # text =requests.form['text']
#     result = predict_classs(text)
#     if result == 'products':
#
#         db_connection = sql.connect(host='localhost', port='3306'
#                                     , database='defenceProject', user='root', password='123456')
#
#         db_cursor = db_connection.cursor()
#
#         db_cursor.execute(f"select tcategorie.nom from tcategorie where tcategorie.id={categorie_id};")
#
#         table_rows = db_cursor.fetchall()
#         response = jsonify({
#             'category_name': table_rows
#         })
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         # datas = pd.DataFrame(table_rows)
#         return response
#









# print("Go! Bot is running!")
#
# while True:
#     message = input("")
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     print(res)









# ________________________________sentiment analysis__________________________________-

import pickle
import nltk
import string
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import classify
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier
from random import shuffle


# possitive=nltk.corpus.twitter_samples.strings('positive_tweets.json')
# negative=nltk.corpus.twitter_samples.strings('negative_tweets.json')

positive_tweets = nltk.corpus.twitter_samples.tokenized('positive_tweets.json')
negative_tweets = nltk.corpus.twitter_samples.tokenized('negative_tweets.json')


def is_clean(word: str):
    if word.startswith('@'):
        return False
    if word.startswith('http://') or word.startswith('https://'):
        return False
    if word in string.punctuation:
        return False
    if word.isnumeric():
        return False
    if word in stopwords.words('english'):
        return False
    return True


def clean_tokens(tokens: list):
    return [word.lower() for word in tokens if is_clean(word)]


positive_tweets_clean = [clean_tokens(tokens) for tokens in positive_tweets]
negative_tweets_clean = [clean_tokens(tokens) for tokens in negative_tweets]

lemmatizer = WordNetLemmatizer()


def lemmatize(word: str, tag: str):
    if tag.startswith('NN'):
        pos = 'n'
    elif tag.startswith('VB'):
        pos = 'v'
    else:
        pos = 'a'
    return lemmatizer.lemmatize(word, pos)


def lemmatize_tokens(tokens: list):
    return [lemmatize(word, tag) for word, tag in pos_tag(tokens)]


positive_tweets_normalized = [lemmatize_tokens(tokens) for tokens in positive_tweets_clean]
negative_tweets_normalized = [lemmatize_tokens(tokens) for tokens in negative_tweets_clean]

positive_dataset = [({token: True for token in tokens}, 'positive') for tokens in positive_tweets_normalized]
negative_dataset = [({token: True for token in tokens}, 'negative') for tokens in negative_tweets_normalized]

if __name__ == '__main__':
    tweet = 'please i am really angry right now'
    tweet_dict = {token: True for token in lemmatize_tokens(clean_tokens(tweet.split()))}
    print(model.classify(tweet_dict))


    # _________________________forecast________________________________________

import pickle
import json
import numpy as np

from copy import deepcopy as dc
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.nn as nn

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'


class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_stacked_layers):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_stacked_layers = num_stacked_layers

        self.lstm = nn.LSTM(input_size, hidden_size, num_stacked_layers,
                                batch_first=True)

        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
            batch_size = x.size(0)
            h0 = torch.zeros(self.num_stacked_layers, batch_size, self.hidden_size).to(device)
            c0 = torch.zeros(self.num_stacked_layers, batch_size, self.hidden_size).to(device)

            out, _ = self.lstm(x, (h0, c0))
            out = self.fc(out[:, -1, :])
            return out


model = LSTM(1, 4, 1)
model.to(device)
model.load_state_dict(torch.load('./model2.pth'))
model.eval()


def forecast(month3, month2, month1):
    sales_three_months_ago = month3
    sales_two_months_ago = month2
    last_month_sales = month1

    x1 = [sales_three_months_ago, sales_two_months_ago, last_month_sales]

    x1 = torch.tensor(x1).float()

    x1 = x1.reshape((-1, 1))

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x1 = scaler.fit_transform(x1)

    x1 = torch.tensor(x1).float()
    x1 = x1.reshape((-1, 3, 1))
    test_predictions = model(x1.to(device)).detach().cpu().numpy().flatten()

    dummies = np.zeros((x1.shape[0], 4))

    dummies[:, 0] = test_predictions
    dummies = scaler.inverse_transform(dummies)

    test_predictions = dc(dummies[:, 0])
    return test_predictions


    if __name__ == '__main__':
        results = forecast(5895, 58968, 785785)
        print(results)


# _________________________________price prediction______________________________________


import pickle
import json
import numpy as np

__code = None
__data_columns = None
__model = None

def get_estimated_price(code,prix,prix_achat,categorie):
    try:
        loc_index = __data_columns.index(code.lower())
    except:
        loc_index = -1

    x = np.zeros(1887)
    x[0] = prix
    x[1] = prix_achat
    x[2] = categorie
    if loc_index>=0:
        x[loc_index] = 1

    return (__model.predict([x])[0])


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __code

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __code = __data_columns[3:]  # first 3 columns are prix, prix_achat, categorie

    global __model
    if __model is None:
        with open('./artifacts/save_prix_predict_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_code_names():
    return __code

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_code_names())
    # print(get_estimated_price('SAG30C',100, 562, 35))
    print(get_estimated_price('076CAST', 1000, 252, 26))
    print(get_estimated_price('1/5MPFP', 1020, 38, 452)) # other location
    print(get_estimated_price('1/5PBAR', 4230, 631, 212))  # other location