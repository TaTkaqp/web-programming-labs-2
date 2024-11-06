from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
def web ():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
    <!doctype html> 
        <html> 
        <head>
            <title>Лабораторная 1</title>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
            <body> 
               <h1>web-сервер на flask<h1> 
            </body> 
        </html> ''',200, {
             'X-Server': 'sample',
             'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author ():
    name = "Бугаёва Наталья Владимировна"
    group = "ФБИ-21"
    faculty = "ФБ"
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
        <!doctype html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
            <body>
                <p>Студент: '''+ name +'''</p>
                <p>Группа: '''+ group +'''</p>
                <p>Факультет: '''+ faculty +'''</p>
                <a href="/web">web</a>
            <body>
        </html>'''


@lab1.route("/lab1/oak")
def oak():
    css_path = url_for("static", filename="lab1/lab1.css")
    img_path = url_for("static", filename="lab1/oak.jpg")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src='{img_path} '>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''


count = 0

@lab1.route("/lab1/counter")
def counter():
    global count
    count += 1
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + ''' <br>
        <a href="/lab1/reset_counter">Очистить счётчик</a><br>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''

@lab1.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        Счётчик обнулён!<br>
        <a href="/lab1/counter">Вернуться к счётчику</a><br>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


resource = False

@lab1.route("/lab1/created")
def created():
    css_path = url_for("static", filename="lab1/lab1.css")
    global resource
    if resource:
        return '''
<!doctype html>
<html>
    <head>
        <title>Создание ресурса</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1 class="resource">Отказано:ресурс уже создан</h1>
    </body>
</html>
''', 400
    else:
        resource = True
        return '''
<!doctype html>
<html>
    <head>
        <title>Создание ресурса</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Успешно: ресурс создан</h1>
    </body>
</html>
''', 201


@lab1.route("/lab1/delete")
def delete():
    css_path = url_for("static", filename="lab1/lab1.css")
    global resource
    if resource:
        resource = False
        return '''
<!doctype html>
<html>
    <head>
        <title>Удаление ресурса</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Успешно: ресурс удален</h1>
    </body>
    </body>
</html>
''', 200
    else:
        return '''
<!doctype html>
<html>
    <head>
        <title>Разрушение башни</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Отказано: ресурс еще не создан</h1>
    </body>
    </body>
</html>
''', 400


@lab1.route("/lab1/resource")
def resource_status():
    css_path = url_for("static", filename="lab1/lab1.css")
    if resource:
        status = "Ресурс создан"
    else:
        status = "Ресурс еще не создан"
    return '''
<!doctype html>
<html>
    <head>
        <title>Статус постройки</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>''' + status + '''</h1>
        <div>
            <a href="/lab1/created">Создать ресурс</a><br>
        </div>
        <div>
            <a href="/lab1/delete">Удалить ресурс</a>
        </div>
    </body>
</html>
'''


@lab1.route("/lab1")
def lab():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <p>
                Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.
                Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
            </p>
            <h2>Список роутов</h2>
            <ul>
                <li><a href="/lab1/author">Автор</a></li>
                <li><a href="/lab1/web">Web сервер на Flask</a></li>
                <li><a href="/lab1/oak">Дуб и ЕжИк</a></li>
                <li><a href="/lab1/counter">Посещения</a></li>
                <li><a href="/lab1/created">СУспех</a></li>
                <li><a href="/lab1/error">Ошибка 500</a></li>
                <li><a href="/lab1/418">I'm a teapot</a></li>
                <li><a href="/lab1/student_choice">Forest</a></li>
                <li><a href="/lab1/resource">Ресурс</a></li>
                <li><a href="/lab1/400">400</a></li>
                <li><a href="/lab1/402">402</a></li>
                <li><a href="/lab1/403">403</a></li>
                <li><a href="/lab1/405">405</a></li>
                <li><a href="/lab1/418">418</a></li>
            </ul>
            <a href="/">На главную</a>
        </body>
    </html>
    '''


@lab1.route("/lab1/400")
def error_400():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>400: Bad Request</h1>
        <p>Ошибка 400: Сервер не может обработать запрос из-за ошибки клиента.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 400

@lab1.route("/lab1/401")
def error_401():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>401: Unauthorized</h1>
        <p>Ошибка 401: Необходима аутентификация для доступа к ресурсу!!!</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html> 
    ''', 401

@lab1.route("/lab1/402")
def error_402():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
<head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>402: Payment Required</h1>
        <p>Ошибка 402: Требуется оплата для доступа к ресурсу.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 402

@lab1.route("/lab1/403")
def error_403():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>403: Forbidden</h1>
        <p>Ошибка 403: Доступ к ресурсу запрещен.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 403


@lab1.route("/lab1/405")
def error_405():
    css_path = url_for("static", filename="lab1/lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>405: Method Not Allowed</h1>
        <p>Ошибка 405: Метод запроса не поддерживается данным ресурсом.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 405

@lab1.route("/lab1/418")
def error_418():
    css_path = url_for("static", filename="lab1/lab1.css")
    img_path = url_for("static", filename="lab1/teapot.jpg")
    return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <h1>418: I'm a teapot</h1>
            <p>Ошибка 418: Cервер отказывается заваривать кофе, поскольку он постоянно является чайником</p>
            <img src="{img_path}" alt="I'm a teapot">
            <br>
            <a href="/lab1">На страницу лабораторной 1</a>
        </body>
    </html>
    ''', 418


@lab1.route("/lab1/error")
def generate_error():
    # Пример ошибки деления на ноль
    error = 1 / 0
    return "This will not be reached because of the error"


@lab1.route("/lab1/student_choice")
def student_choice():
    css_path = url_for("static", filename="lab1/lab1.css")
    img_path = url_for("static", filename="lab1/forest.jpg")
    
    # Текст статьи
    text = '''
    Природа — это невероятный источник вдохновения для людей всех возрастов и профессий. Леса, горы, 
    реки и океаны — все это часть огромной и сложной экосистемы, которая поддерживает жизнь на планете.

    В лесах живет огромное количество растений и животных, каждый из которых выполняет свою роль в 
    поддержании экологического баланса. Деревья, например, поглощают углекислый газ и выделяют кислород, необходимый для жизни человека.

    Чистые реки и озера обеспечивают водой миллионы людей по всему миру. Однако загрязнение и неправильное 
    использование природных ресурсов могут привести к серьезным экологическим проблемам.

    Забота о природе — это ответственность каждого из нас. Сохранение лесов, воды и дикой природы поможет 
    будущим поколениям наслаждаться красотой планеты и здоровой средой для жизни.
    '''

    return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
            <title>Загадочная природа</title>
        </head>
        <body>
            <h1>О чудесах природы</h1>
            <p>{text}</p>
            <img src="{img_path}" alt="Природа" style="width:1000px;height:auto;">
            <br>
            <a href="/lab1">На страницу лабораторной 1</a>
        </body>
    </html>
    ''', 200, {
        'Content-Language': 'ru',  # Устанавливаем заголовок Content-Language для русского языка
        'X-Author': 'Student',  # Нестандартный заголовок
        'X-Powered-By': 'FlaskApp'  # Нестандартный заголовок
    }