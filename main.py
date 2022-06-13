from flask import (
    render_template as render,
    request, 
    redirect, 
    send_from_directory
)
from tinydb import TinyDB, Query
#from dashboard import server as app
import os
import pathlib
from flask import Flask, render_template
#from telegram.parser_tg import product_recomendations
from vk_pars.parser_vk import product_recommendations
import asyncio

session = {'username': ''}


products = {
    'Дебетовые карты': ['путешествия', 'инвестиции', 'улучшение условий труда'],
    'Кредитные карты': ['комфорт', 'удовольствие', 'гламур', 'технологии'],
    'Продукты для ЮЛ': ['путешествия', 'накопление сбережений', 'автомобиль', 'образование', 'финансы', 'инвестиции'],
    'Кредит' : ['деньги', 'успех', 'роскошь']
}

app = Flask(__name__)

app_path = str(pathlib.Path(__file__).parent.resolve())
db_path = os.path.join(app_path, os.path.join("data", "db.json"))

db = TinyDB(db_path, sort_keys=True, indent=4, separators=(',', ': '))
usr = db.table('users')
URL = db.table('URLs')


@app.errorhandler(404)
def page_not_found(e):
    return render('error.html')


@app.route('/assets/<path:path>', methods=['GET'])
def send_assets(path):
    return send_from_directory('assets', path)


@app.route('/data/<path:path>', methods=['GET'])
def send_data(path):
    return send_from_directory('data', path)


@app.route('/main', methods=['GET'])
def main_page():
    return render('main.html')
@app.route('/', methods=['GET'])
def signin():
    return render('signin.html')


@app.route('/signup', methods=['GET'])
def signup():
    return render('signup.html')


@app.route('/signout', methods=['GET'])
def signout():
    return redirect('/')



@app.route('/main', methods=["POST", "GET"])
def do_main():
    if request.method == 'POST':
        URL.insert({
            'URL': request.form['URL'],
            })
        
        message = product_recommendations(request.form['URL'], 10000)
        product_one = {'Дебетовые карты':message['Дебетовые карты']}
        product_two = {'Кредитные карты':message['Кредитные карты']}
        product_three = {'Продукты для ЮЛ':message['Продукты для ЮЛ']}
        product_four = {'Кредит':message['Кредит']}
        
        return render_template('main.html', product_one=product_one, 
        product_two=product_two, product_three = product_three,
        product_four=product_four)





@app.route('/signin', methods=['POST'])
def do_signin():
    User = Query()
    users = usr.search(User.name == request.form['username'])
    if not users:
        return render('signin.html', text='Wrong username or password')
    user = users[0]
    if user['password'] != request.form['password']:
        print(user['password'], request.form['password'])
    session['username'] = user['name']
    return redirect('/main')


@app.route('/signup', methods=['POST'])
def do_signup():
    User = Query()
    users = db.search(User.name == request.form['username'])
    if len(users) > 0:
        text = 'Such user have already exists'
        return render('signup.html', text=text)
    usr.insert({
        'name' : request.form['username'],
        'email': request.form['email'],
        'password': request.form['password']
    })
    return redirect('/signin')



if __name__ == '__main__':
    app.run(debug=True, port=8050)
