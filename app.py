from flask import Flask, url_for, redirect
app = Flask (__name__)

@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>
            Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
            Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <a href="/">На главную</a>
    </body>
</html>
    """

@app.errorhandler(404)
def not_found (err):
     return"Такой страницы не существует", 404

@app.route("/")
@app.route("/lab1/web")
def web ():
    return """<!doctype html> 
        <html> 
            <body> 
               <h1>web-сервер на flask<h1> 
            </body> 
        </html>""",200, {
             'X-Server': 'sample',
             'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author ():
    name = "Бугаёва Наталья Владимировна"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """+ name +"""</p>
                <p>Группа: """+ group +"""</p>
                <p>Факультет: """+ faculty +"""</p>
                <a href="/web">web</a>
            <body>
        </html>"""

@app.route("/lab1/info")
def info ():
     return redirect ("/lab1/author")

@app.route("/lab1/oak")
def oak():
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="oak.jpg")
    return """
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href='""" + css_path + """'>
    </head>
    <body>
        <h1>Дуб</h1>
        <img src='""" + img_path + """'>
        <a href="/web">web</a>
    </body>
</html>
"""

count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + ''' <br>
        <a href="/lab1/reset_counter">Очистить счётчик</a><br>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        Счётчик обнулён!<br>
        <a href="/lab1/counter">Вернуться к счётчику</a><br>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''

@app.route ("/lab1/created")
def created ():
     return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>Это как-то было создано...</i></div>
    </body>
</html>
''', 201

from flask import abort

@app.route("/lab1/400")
def error_400():
    return '''
<!doctype html>
<html>
    <body>
        <h1>400: Bad Request</h1>
        <p>Ошибка 400: Сервер не может обработать запрос из-за ошибки клиента.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 400

@app.route("/lab1/401")
def error_401():
    return '''
<!doctype html>
<html>
    <body>
        <h1>401: Unauthorized</h1>
        <p>Ошибка 401: Необходима аутентификация для доступа к ресурсу.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 401

@app.route("/lab1/402")
def error_402():
    return '''
<!doctype html>
<html>
    <body>
        <h1>402: Payment Required</h1>
        <p>Ошибка 402: Требуется оплата для доступа к ресурсу.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 402

@app.route("/lab1/403")
def error_403():
    return '''
<!doctype html>
<html>
    <body>
        <h1>403: Forbidden</h1>
        <p>Ошибка 403: Доступ к ресурсу запрещен.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 403

@app.route("/lab1/405")
def error_405():
    return '''
<!doctype html>
<html>
    <body>
        <h1>405: Method Not Allowed</h1>
        <p>Ошибка 405: Метод запроса не поддерживается данным ресурсом.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 405

@app.route("/lab1/418")
def error_418():
    return '''
<!doctype html>
<html>
    <body>
        <h1>418: I'm a teapot</h1>
        <p>Ошибка 418: Я чайник. Запрос не может быть обработан, так как сервер — это чайник.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 418