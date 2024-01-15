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