from flask import Flask, render_template, url_for, redirect, session, request, jsonify
import mysql.connector as sql
import utils
from utils import get_response, predict_class
import json
from nltk.stem import WordNetLemmatizer
import math
import pickle
import random


# ____________________connection to the database________________________________--
connection = sql.connect(host='localhost', port='3306'
                            , database='defenceProject', user='ngali', password='123456')
cursor = connection.cursor()
db_connection = sql.connect(host='localhost', port='3306'
                            , database='defenceProject', user='ngali', password='123456')
db_cursor = db_connection.cursor()

# _________________creating the app and the secrete key______________________________
app = Flask(__name__)
app.secret_key = "super secret key"


# __________________Routing to my different folders______________________________
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/manager',  methods=['GET', 'POST'])
def manager():
    return render_template('manager.html')


@app.route('/manager_choice', methods=['GET', 'POST'])
def manager_choice():
    return render_template('managerchoice.html')


@app.route('/client_choice', methods=['GET', 'POST'])
def client_choice():
    return render_template("clientchoice.html")


@app.route('/final_client_login',  methods=['GET', 'POST'])
def final_client_login():
    return render_template('finalclient.html')


# _____________________login and logout for manager and client_________________________________
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute(f"SELECT * FROM user WHERE username={username} AND password={password};")
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            return redirect(url_for('client_choice'))
        else:
            msg = 'Incorrect username or password. please try again'
    return render_template('finalclient.html', msg=msg)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    msg = ''
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    cursor.execute(f" INSERT INTO user VALUES(2, '{username}', '{email}', '{password}')  ;")
    msg = 'Registration successful. You will be able to login now.'
    return redirect(url_for('final_client_login'), msg)


@app.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    msg=''
    if request.method == 'POST':
        usernames = request.form['usernames']
        passwords = request.form['passwords']
        cursor.execute(f"SELECT * FROM manager WHERE username={usernames} AND password={passwords};")
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            return redirect(url_for('manager_choice'))
        else:
            msg = 'Incorrect username or password. please try again'
    return render_template('manager.html', msg=msg)


@app.route('/logout_manager', methods=['GET', 'POST'])
def logout_manager():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login_manager'))


@app.route('/registration_manager', methods=['GET', 'POST'])
def registration_manager():
    msg = ''
    usernames = request.form['usernames']
    email = request.form['email']
    passwords = request.form['passwords']
    cursor.execute(f" INSERT INTO manager VALUES(2, '{usernames}', '{email}', '{passwords}')  ;")
    msg = 'Registration successful. You will be able to login now.'
    return redirect(url_for('manager'), msg)


# ____________________________beginning of chatbot model____________________________________________

@app.route('/chatbot', methods=['GET'])
def chatbot():
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


# _____________________________SENTIMENT ANALYSIS model_________________________________________________________

f = open('model_classifier.pickle', 'rb')
model = pickle.load(f)
f.close()


@app.route('/sentiment_analysis', methods=['GET', 'POST'])
def sentiment_analysis():
    return render_template("client.html")


@app.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    tweet = request.form['tweet']
    tweet_dict = {token: True for token in utils.lemmatize_tokens(utils.clean_tokens(tweet.split()))}
    text = model.classify(tweet_dict)
    return text


# @app.route('/sentiments', methods=['GET', 'POST'])
# def sentiments():
#     product_name = request.form['product_name']
#     return product_name

@app.route('/throw_text', methods=['GET', 'POST'])
def throw_text():
    p1 = f"Wow! we are really touched to hear that awesome comment about our products" \
         f" \U0001F923 \U0001F605. We are improving on our quality everyday. Thanks \U0001F923"
    p2 = f"That is awesome, we're the best when it comes to this particular product" \
         f" \U0001F923 \U0001F605. Enjoy your day. Thanks \U0001F923"
    p3 = f"Hey! Thanks for complementing our products" \
         f" \U0001F923 \U0001F605. Order more to have discount . Thanks \U0001F923"
    p4 = f"Hello, we are more excited to know you like our products" \
         f" \U0001F923 \U0001F605. Order more to have discount . Thanks \U0001F923"
    n1 = f"Hello, we are so sorry you have a problem with our products" \
         f" \U0001F910 \U0001F612. We are looking up to improving the quality. Thanks \U0001F612"
    n2 = f"So sad getting a regret from our client about our products" \
         f" \U0001F910 \U0001F612. Worry not my dear, our quality will be improved shortly. Thanks \U0001F612"
    n3 = f"Hey my dear! We are so sorry you didn't like our products" \
         f" \U0001F910 \U0001F612. We are looking up to improving the quality soon. Thanks \U0001F612"
    n4 = f"We are sorry you had a problem with our products" \
         f" \U0001F910 \U0001F612. Trust us. Next time time you won't have this issue again Thanks \U0001F612"
    positive = [p1, p2, p3, p4]
    negative = [n1, n2, n3, n4]
    status = sentiment()
    if status == 'positive':
        result = random.choice(positive)
    else:
        result = random.choice(negative)
    response = jsonify({
        'text': result
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


# @app.route('/insert_comment', methods=['GET', 'POST'])
# def insert_comment():
#     tweet = request.form['tweet']
#     db_cursor.execute(
#         f"INSERT INTO comments VALUES(1, '{tweet}');")
#     response = jsonify({
#         'message': 'Success'
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response


# def send_email():
#     import smtplib
#     import requests
#     # do this setting to be able to see the mail: open you google account and
#     # navigate to security section and enable "less secure app access".
#     # by default, its off. so you turn it on. this is not recommened. do it just for this test
#     client_name = requests.form['client_name']
#     product_name = request.form['product_name']
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login('ngaliabiru@gmail.com', 'abiru@123')
#     text=sentiment()
#     if text == 'negative':
#         server.sendmail('ngaliabiru@gmail.com', 'kepgangemilie@gmail.com', f"Notifications: the client {client_name}"
#                                                        f" is not happy about the product {product_name}. "
#                                                               f"Please you need to improve the quality "
#                                                        f"This is what he says: mment")
#
#     else:
#         server.sendmail('ngaliabiru@gmail.com', '@gmail.com', f"Notifications: the client {client_name}"
#                                                               f" is very happy about the product {product_name}. "
#                                                               f"This is what he says: mment")

# _____________________________beginning of sales forecast model____________________________


@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    return render_template('forecast.html')


@app.route('/forecast_sales', methods=['GET', 'POST'])
def forecast_sales():
    month3 = float(request.form['month3'])
    month2 = float(request.form['month2'])
    month1 = float(request.form['month3'])
    response = jsonify({
        'estimated_sales': abs(math.ceil(utils.forecast(month3, month2, month1)))
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_categorie_id', methods=['GET', 'POST'])
def get_categorie_id():
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    variable = request.form['variable']
    db_cursor.execute(
        f"SELECT tarticles.categorie, COUNT(tarticles.categorie) as cat, "
        f"tcommandes.ligne FROM tarticles JOIN tcommandes ON tcommandes.ligne IN"
        f" (SELECT tlignecommande.id FROM tlignecommande WHERE tlignecommande.datelivraison BETWEEN"
        f" '{start_date}' AND '{end_date}') GROUP BY categorie  ORDER BY COUNT(tarticles.categorie) DESC  LIMIT 10 ;")
    table_rows = db_cursor.fetchall()
    response = jsonify({
        'id_categorie': table_rows[int(variable)][0]
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_categorie_name', methods=['GET', 'POST'])
def get_categorie_name():
    categorie_id = request.form['categorie_id']
    db_cursor.execute(f"select tcategorie.nom from tcategorie where tcategorie.id={categorie_id};")
    table_rows = db_cursor.fetchall()
    response = jsonify({
        'category_name': table_rows
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_client_name', methods=['GET', 'POST'])
def get_client_name():
    categorie_id = request.form['categorie_id']
    db_cursor.execute(f"SELECT tclients.nom FROM tclients"
                      f" WHERE tclients.id = (SELECT tlignecommande.client FROM tlignecommande"
                      f" WHERE tlignecommande.id = (SELECT tcommandes.ligne FROM tcommandes "
                      f"WHERE tcommandes.id = (SELECT tcommandes.id FROM tcommandes "
                      f"WHERE tcommandes.article = (SELECT tarticles.id FROM tarticles "
                      f"WHERE tarticles.categorie={categorie_id} limit 1) limit 1 ) limit 5 ) limit  10 );")
    table_rows = db_cursor.fetchall()
    response = jsonify({
        'client_name': table_rows
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/possibility', methods=['GET', 'POST'])
def possibility():
    categorie_id = request.form['categorie_id']
    expected_sales = request.form['expected_sales']
    estimated_sales = request.form['estimated_sales']
    db_connection = sql.connect(host='localhost', port='3306'
                                , database='defenceProject', user='root', password='123456')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"SELECT tclients.nom FROM tclients"
                      f" WHERE tclients.id = (SELECT tlignecommande.client FROM tlignecommande"
                      f" WHERE tlignecommande.id = (SELECT tcommandes.ligne FROM tcommandes "
                      f"WHERE tcommandes.id = (SELECT tcommandes.id FROM tcommandes "
                      f"WHERE tcommandes.article = (SELECT tarticles.id FROM tarticles "
                      f"WHERE tarticles.categorie={categorie_id} limit 1) limit 1 ) limit 5 ) limit  10 );")

    client_name = db_cursor.fetchall()
    db_cursor.execute(f"SELECT tcategorie.nom from tcategorie WHERE tcategorie.id= {categorie_id}")
    categorie_name = db_cursor.fetchall()
    if float(expected_sales) <= float(estimated_sales):
        response = jsonify({
            'possibility_check': f"""

                          POSSIBLE.

        It's possible to make the sales you expected on three conditions:
        1). Make sure to sell at least 40% of {expected_sales} units by selling
         {categorie_name} to {client_name} because he or she is the best
          customer for this category within the chosen period.
        2). Also condition {client_name} to buy other categories mentioned in
        the list above to be able to get his favorite products, so that, you
        can have at least 5% of {expected_sales} units from this.
        3). You can then get the remaining sales by selling other categories mentioned above
        to their best client this month to be able to have 55% of {expected_sales} units
        Note that you have a greater chance to make these sales.

        NB: if you do this, you have 90% chance of getting your expected sales. THANKS.
                     PREDICTION BY NGALI.

        """
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
    if float(estimated_sales) < float(expected_sales) <= float(estimated_sales) * (0.2 * float(estimated_sales)):
        response = jsonify({
            'possibility_check': f"""
                                 SLIGHTLY POSSIBLE.

                This is slightly possible if you respect these condictions:
                1). Make sure to sell at least 40% of {expected_sales} quantities by selling
                 {categorie_name} to {client_name} because he or she is the best
                  customer for this category within the chosen period.
                2). Also condition {client_name} to buy other categories mentioned in
                the list above to be able to get his favorite products, so that, you
                can have at least 5% of {expected_sales} quantities from this.
                3). You can then get the remaining sales by selling other categories mentioned above
                to their best client this month to be able to have 55% of {expected_sales} .
                Note that the probability to have these sales is a little low.

                NB: if you do this, you have 90% chance of getting your expected sales. THANKS.
                             PREDICTION BY NGALI.
                """
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
    if float(expected_sales) > float(estimated_sales) * (0.2 * float(estimated_sales)):
        response = jsonify({
            'possibility_check': f"""
                                 IMPOSSIBLE.

                We regret telling you that the sales you expect is not possible.
                However, we can increase your chances.
                Respect these conditions to get your required sales:
                1). Make sure to sell at least 40% of {expected_sales} units by selling
                 {categorie_name} to {client_name} because he or she is the best
                  customer for this category within the chosen period.
                2). Also condition {client_name} to buy other categories mentioned in
                the list above to be able to get his favorite products, so that, you
                can have at least 5% of {expected_sales} units from this.
                3). You can then get the remaining sales by selling other categories mentioned above
                to their best client this month to be able to have 55% of {expected_sales} units
                Note that the probability to have these sales is very low.

                NB: if you do this, you have 90% chance of getting your expected sales. THANKS.
                             PREDICTION BY NGALI.
                """
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# ____________________________price prediction_________________________________________-


@app.route('/predict_price', methods=['GET', 'POST'])
def predict_price():
    return render_template('predict_price.html')


@app.route('/get_code_names', methods=['GET'])
def get_code_names():
    response = jsonify({
        'code': utils.get_code_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_save_price', methods=['GET', 'POST'])
def predict_save_price():
    prix = float(request.form['prix'])
    code = request.form['code']
    try:
        prix_achat = int(float(request.form['prix_achat']))
        categorie = int(request.form['categorie'])
    except ValueError:
        prix_achat=356
        categorie=418
    response = jsonify({
        'estimated_price': math.ceil(utils.get_estimated_price(code, prix *(1.5), prix_achat, categorie).tolist()[0])
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For the whole project...")
    utils.load_saved_artifacts()
    app.run(debug=True)
