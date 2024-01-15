from flask import Flask, request, jsonify, render_template
import utils
from utils import get_response, predict_class, predict_classs
import re, json
from nltk.stem import WordNetLemmatizer

# app = Flask(__name__)


# @app.route('/', methods=['GET'])
# def index_get():
#     return render_template("base.html")


# lemmatizer = WordNetLemmatizer()
# with open("./intents.json", 'r') as file:
#     intents = json.load(file)


# @app.route('/predict', methods=['POST'])
# def predict():
#     text = request.get_json().get("message")
#     ints = predict_class(text)
#     response = get_response(ints, intents)
#     message = {"answer": response}
#     return jsonify(message)



# if __name__ == "__main__":
#     print("Starting Python Flask Server For chatbot...")
#     app.run(debug=True)









from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.app_context()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=False)

# $ python
# >>> from project import app, db
# >>> app.app_context().push()
# >>> db.create_all()
class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    email = EmailField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


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

#
# @app.route('/final_client',  methods=['GET', 'POST'])
# def final_client():
#     form = LoginForm()
#     return render_template('finalclient.html', form=form)


@app.route('/c_register',  methods=['GET', 'POST'])
def c_register():
    form = RegisterForm()
    forms = LoginForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('finalclient.html'))

    return render_template('finalclient.html', form=form, forms=forms)


# @app.route('/c_login', methods=['GET', 'POST'])
# def c_login():
#     form = LoginForm()
#     return render_template('finalclient.html', form=form)
#
#
# @app.route('/c_register', methods=['GET', 'POST'])
# def c_register():
#     form = RegisterForm()
#     return render_template('finalclient.html', form=form)


# @ app.route('/mregister', methods=['GET', 'POST'])
# def mregister():
#     form = RegisterForm()
#
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data)
#         new_user = User(username=form.username.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('manager_choice'))
#
#     return render_template('manager.html', form=form)


#
#
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
#


#
#
# @app.route('/')
# def home():
#     return render_template('home.html')
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 login_user(user)
#                 return redirect(url_for('dashboard'))
#     return render_template('login.html', form=form)
#
#
# @app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     return render_template('dashboard.html')
#
#
# @app.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
#
#
# @ app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data)
#         new_user = User(username=form.username.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#
#     return render_template('register.html', form=form)
#


# ____________________________chatbot____________________________________________


from flask import Flask, request, jsonify, render_template
import utils
from utils import get_response, predict_class, predict_classs
import re, json
from nltk.stem import WordNetLemmatizer

# app = Flask(__name__)


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



# _____________________________SENTIMENT ANALYSIS_________________________________________________________

import json

from flask import Flask, request, jsonify
import utils
import re
import math
import pickle
import random

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
    # response = jsonify({
    #     'text': model.classify(tweet_dict)
    # })
    # response.headers.add('Access-Control-Allow-Origin', '*')

    return text


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


@app.route('/insertComment', methods=['GET', 'POST'])
def insertComment():
    tweet = request.form['tweet']
    import mysql.connector as sql
    db_connection = sql.connect(host='localhost', port='3306'
                                , database='defenceProject', user='root', password='123456')

    db_cursor = db_connection.cursor()

    db_cursor.execute(
        f"INSERT INTO comments VALUES(1, '{tweet}');")
    response = jsonify({
        'message': 'Success'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# _____________________________sales forecast____________________________

from flask import Flask, request, jsonify
import utils
import re
import math


@app.route('/forecat', methods=['GET', 'POST'])
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
    # k = 0
    variable = request.form['variable']
    import mysql.connector as sql
    db_connection = sql.connect(host='localhost', port='3306'
                                , database='defenceProject', user='root', password='123456')

    db_cursor = db_connection.cursor()

    db_cursor.execute(
        f"SELECT tarticles.categorie, COUNT(tarticles.categorie) as cat, "
        f"tcommandes.ligne FROM tarticles JOIN tcommandes ON tcommandes.ligne IN"
        f" (SELECT tlignecommande.id FROM tlignecommande WHERE tlignecommande.datelivraison BETWEEN"
        f" '{start_date}' AND '{end_date}') GROUP BY categorie  ORDER BY COUNT(tarticles.categorie) DESC  LIMIT 10 ;")
    table_rows = db_cursor.fetchall()
    # response = jsonify({})
    response = jsonify({
        'id_categorie': table_rows[int(variable)][0]
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
    # datas = pd.DataFrame(table_rows)
    return response


@app.route('/get_categorie_name', methods=['GET', 'POST'])
def get_categorie_name():
    categorie_id = request.form['categorie_id']

    import mysql.connector as sql
    import pandas as pd
    db_connection = sql.connect(host='localhost', port='3306'
                                , database='defenceProject', user='root', password='123456')

    db_cursor = db_connection.cursor()

    db_cursor.execute(f"select tcategorie.nom from tcategorie where tcategorie.id={categorie_id};")

    table_rows = db_cursor.fetchall()
    response = jsonify({
        'category_name': table_rows
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    # datas = pd.DataFrame(table_rows)
    return response


@app.route('/get_client_name', methods=['GET', 'POST'])
def get_client_name():
    categorie_id = request.form['categorie_id']

    import mysql.connector as sql
    import pandas as pd
    db_connection = sql.connect(host='localhost', port='3306'
                                , database='defenceProject', user='root', password='123456')

    db_cursor = db_connection.cursor()

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
    expected_sales = request.form['expected_sales']
    estimated_sales = request.form['estimated_sales']
    categorie_id = request.form['categorie_id']

    import mysql.connector as sql
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

    db_connection = sql.connect(host='localhost', port='3306'
                                , database='defenceProject', user='root', password='123456')

    db_cursor = db_connection.cursor()

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


from flask import Flask, request, jsonify
import utils
import re
import math


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
    # prix_achat = request.form['prix_achat']
    # categorie = request.form['categorie']
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
