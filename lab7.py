from flask import Blueprint, render_template, request
from datetime import datetime


lab7 = Blueprint('lab7', __name__)


films = [
    {
        "title_ru": "Ёлки 11",
        "title": "Ёлки 11",
        "year": 2024,
        "description": "Судьбы многих людей из разных уголков страны переплетутся самым неожиданным образом, чтобы поздравить одинокую учительницу Валентину Михайловну. Всем им предстоит осознать нечто важное и сделать правильный выбор, чтобы вступить в Новый год с новыми надеждами."
    },
    {
        "title_ru": "Субстанция",
        "title": "The Substance",
        "year": 2024,
        "description": "Слава голливудской звезды Элизабет Спаркл осталась в прошлом, хоть она всё ещё ведёт популярное фитнес-шоу на телевидении. Когда её передачу собираются перезапустить с новой звездой, Элизабет решает принять уникальный препарат «Субстанция». Так на свет появляется молодая и сексуальная Сью. Однако у совершенства есть своя цена, и расплата не заставит себя долго ждать."
    },
    {
        "title_ru": "Остров проклятых",
        "title": "Shutter Island",
        "year": 2009,
        "description": "Два американских судебных пристава отправляются на один из островов в штате Массачусетс, чтобы расследовать исчезновение пациентки клиники для умалишенных преступников. При проведении расследования им придется столкнуться с паутиной лжи, обрушившимся ураганом и смертельным бунтом обитателей клиники."
    },
    {
        "title_ru": "Интерстеллар ",
        "title": "Interstellar",
        "year": 2016,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title_ru": "Побег из Шоушенка",
        "title": "The Shawshank Redemption",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
    },
]


@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Film not found"}, 404
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Film not found"}, 404
    return films[id]





@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Film not found"}, 404
    film = request.get_json()
    if film['title_ru'] == '':
        return {'title_ru': 'Укажите русское название'}, 400
    if film['year'] == '':
        return {'year': 'Укажите год'}, 400
    current_year = datetime.now().year
    year = int(film['year'])
    if year < 1895 or year > current_year:
        return {'year': f'Год должен быть от 1895 до {current_year}'}, 400
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    if film['title'] == '':
        film['title'] = film['title_ru']
    films[id] = film
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if film['title'] == '' and film['title_ru'] == '':
        return {'title': 'Укажите оригинальное название'}, 400
    if film['title_ru'] == '':
        return {'title_ru': 'Укажите русское название'}, 400
    if film['year'] == '':
        return {'year': 'Укажите год'}, 400
    current_year = datetime.now().year
    year = int(film['year'])
    if year < 1895 or year > current_year:
        return {'year': f'Год должен быть от 1895 до {current_year}'}, 400
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    description = film.get('description', '')
    if len(description) > 2000:
        return {'description': 'Описание превышает 2000 символов'}, 400
    if film['title'] == '':
        film['title'] = film['title_ru']
    films.append(film)
    id = {'id': len(films) - 1}
    return id

