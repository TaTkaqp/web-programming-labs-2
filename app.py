from flask import Flask, url_for, redirect
app = Flask (__name__)

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
