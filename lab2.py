from flask import Blueprint, url_for, redirect, render_template, request
lab2 = Blueprint('lab2', __name__)


@lab2.route("/lab2/a")
def a():
    return 'без слэша'



@lab2.route("/lab2/a/")
def a2():
    return 'со слэшем'


flower_list = [
    {'name': 'роза', 'price': 150},
    {'name': 'тюльпан', 'price': 160},
    {'name': 'незабудка', 'price': 200},
    {'name': 'ромашка', 'price': 100},
]




@lab2.route("/lab2/add_flower/<name>/<int:price>")
def add_flower(name, price):
    flower_list.append({'name': name, 'price': price})
    return render_template('lab2/add_flower.html', name=name, price=price, flower_list=flower_list)


@lab2.route("/lab2/add_flower/<name>")
def add_flower_noprice(name):
    return render_template('lab2/add_flower_noprice.html'), 400


@lab2.route("/lab2/add_flower/", methods=['GET', 'POST'])
def add_flowers():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        flower_list.append({'name': name, 'price': price})
        return render_template('lab2/add_flower.html', name=name, price=price, flower_list=flower_list)
    return render_template('lab2/add_flower400.html'), 400


@lab2.route("/lab2/all_flowers/")
def all_flowers():
    return render_template('lab2/all_flowers.html', flower_list=flower_list)


@lab2.route("/lab2/clean_flowers/")
def clean_flowers():
    global flower_list
    flower_list = []
    return render_template('lab2/clean_flowers.html')


@lab2.route("/lab2/delete_flower/<int:flower_id>")
def delete_flower_id(flower_id):
    if flower_id >= len(flower_list):
        return render_template('lab2/delete_flower_id404.html'), 404
    else:
        del flower_list[flower_id]
        return redirect("/lab2/all_flowers/")


@lab2.route("/lab2/delete_flower/")
def delete_flower():
    return render_template('lab2/delete_flower.html')


@lab2.route("/lab2/example")
def example():
    name = 'Бугаева Наталья'
    number = '2'
    group = 'ФБИ-21'
    course = '3 курс'
    fruits = [
        {'name':'яблоки', 'price': 100},
        {'name':'груши', 'price': 120},
        {'name':'апельсины', 'price': 80},
        {'name':'мандарины', 'price': 95},
        {'name':'манго', 'price': 321}
    ]
    return render_template('lab2/example.html', number=number, name=name, group=group, course=course, fruits=fruits)


@lab2.route("/lab2/")
def lab():
    return render_template('lab2/lab2.html')


@lab2.route("/lab2/filters")
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route("/lab2/calc/<int:a>/<int:b>")
def calc(a,b):
    return render_template('lab2/calc.html', a=a, b=b)


@lab2.route("/lab2/calc/")
def calc1():
    return redirect("/lab2/calc/1/1")


@lab2.route("/lab2/calc/<int:a>")
def calc2(a):
    return redirect(f"/lab2/calc/{a}/1")


@lab2.route("/lab2/books")
def books():
    books = [
        {'author': 'Джордж Оруэлл', 'title': '"1984"', 'genre': 'антиутопия', 'pages': 328},
        {'author': 'Габриэль Гарсия Маркес', 'title': '"Сто лет одиночества"', 'genre': 'роман', 'pages': 432},
        {'author': 'Джейн Остин', 'title': '"Гордость и предубеждение"', 'genre': 'роман', 'pages': 432},
        {'author': 'Харпер Ли', 'title': '"Убить пересмешника"', 'genre': 'роман', 'pages': 296},
        {'author': 'Франц Кафка', 'title': '"Превращение"', 'genre': 'повесть', 'pages': 108},
        {'author': 'Маргарет Этвуд', 'title': '"Служанка"', 'genre': 'фантастика', 'pages': 368},
        {'author': 'Стивен Кинг', 'title': '"Сияние"', 'genre': 'хоррор', 'pages': 688},
        {'author': 'Эрнест Хемингуэй', 'title': '"Старик и море"', 'genre': 'повесть', 'pages': 128},
        {'author': 'Фитцджеральд Скотт', 'title': '"Велик Gatsby"', 'genre': 'роман', 'pages': 180},
        {'author': 'Джоди Пиколт', 'title': '"Под знаком луны"', 'genre': 'роман', 'pages': 400}
]

    return render_template('lab2/books.html', books=books)


@lab2.route("/lab2/avto")
def avto():
    avto = [
    {
        'name': 'Tesla Model S',
        'image': 'lab2/tesla.jpg',
        'description': 'Электромобиль с замечательной динамикой разгона и автономностью до 650 км на одном заряде.'
    },
    {
        'name': 'BMW 3 Series',
        'image': 'lab2/bmw.jpg',
        'description': 'Спортивный седан с комфортным интерьером и передовыми технологиями управления.'
    },
    {
        'name': 'Audi Q5',
        'image': 'lab2/audi.jpg',
        'description': 'Компактный кроссовер, известный своим элегантным дизайном и высокими показателями безопасности.'
    },
    {
        'name': 'Toyota Camry',
        'image': 'lab2/toyota.webp',
        'description': 'Популярный седан с высоким уровнем надежности и комфорта, идеальный для семейных поездок.'
    },
    {
        'name': 'Ford Mustang',
        'image': 'lab2/ford.webp',
        'description': 'Cпортивный автомобиль с мощным двигателем и агрессивным дизайном.'
    },
    {
        'name': 'Mercedes-Benz G-Class',
        'image': 'lab2/merc.jpeg',
        'description': 'Роскошный внедорожник с мощным двигателем и уникальным стилем, способный справиться с любыми условиями бездорожья.'
    }
]
    return render_template('lab2/avto.html', avto=avto)

