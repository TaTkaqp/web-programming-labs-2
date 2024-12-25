from flask import Flask, url_for
import os
from os import path
from flask_sqlalchemy import SQLAlchemy

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab9 import lab9
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'сектерно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab9)


@app.route("/")
@app.route("/index")
def index():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Главная страница</title>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <h1>Меню</h1>
            <ul>
                <li><a href="/lab1">Лабораторная работа 1</a></li>
                <li><a href="/lab2">Лабораторная работа 2</a></li>
                <li><a href="/lab3">Лабораторная работа 3</a></li>
                <li><a href="/lab4/">Лабораторная работа 4</a></li>
                <li><a href="/lab5/">Лабораторная работа 5</a></li>
                <li><a href="/lab6/">Лабораторная работа 6</a></li>
                <li><a href="/lab7/">Лабораторная работа 7</a></li>
            </ul>
        </body>
    </html>
    '''


@app.errorhandler(404)
def handle_404_error(err):
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="404_image.png")
    
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Ошибка 404 - Страница не найдена</title>
            <link rel="stylesheet" type="text/css" href="{css_path}">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    background-color: #f8f9fa;
                    color: #343a40;
                }}
                .container {{
                    margin-top: 50px;
                }}
                h1 {{
                    font-size: 3em;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 1.2em;
                    margin-bottom: 30px;
                }}
                img {{
                    width: 300px;
                    height: auto;
                    margin-bottom: 30px;
                }}
                a {{
                    text-decoration: none;
                    color: #007bff;
                    font-weight: bold;
                }}
                a:hover {{
                    color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Ой! Страница не найдена (404)</h1>
                <img src="{img_path}" alt="404 error">
                <p>Кажется, Вы попали не туда. Давайте вернемся на главную страницу и попробуем снова!</p>
                <a href="/">Вернуться на главную</a>
            </div>
        </body>
    </html>
    ''', 404


@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for("static", filename="lab1.css")
    
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Ошибка 500 - Внутренняя ошибка сервера</title>
            <link rel="stylesheet" type="text/css" href="{css_path}">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    background-color: #f8f9fa;
                    color: #343a40;
                }}
                .container {{
                    margin-top: 50px;
                }}
                h1 {{
                    font-size: 3em;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 1.2em;
                    margin-bottom: 30px;
                }}
                a {{
                    text-decoration: none;
                    color: #007bff;
                    font-weight: bold;
                }}
                a:hover {{
                    color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Ошибка 500 - Внутренняя ошибка сервера</h1>
                <p>На сервере произошла ошибка. Пожалуйста, попробуйте позже.</p>
                <a href="/">Вернуться на главную</a>
            </div>
        </body>
    </html>
    ''', 500

