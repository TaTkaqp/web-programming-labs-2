from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    if name is None:
        name = "Незвестный"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name')
    resp.set_cookie('age')
    resp.set_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    if user == '':
        errors['user'] = 'Заполните поле ввода имени!'
    elif age == '':
        errors['age'] = 'Заполните поле ввода возраста!'
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    global price
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80 
    else:
        price = 70 
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10  
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings') 
def settings():
    color = request.args.get('color') 
    backgroundcolor = request.args.get('backgroundcolor')
    fontsize = request.args.get('fontsize')
    headers = request.args.get('headers')

    if color: 
        resp = make_response(redirect('/lab3/settings')) 
        resp.set_cookie('color', color)

    if backgroundcolor: 
        resp.set_cookie('backgroundcolor', backgroundcolor)

    if fontsize: 
        resp.set_cookie('fontsize', fontsize)

    if headers:
        resp.set_cookie('headers', headers)
        return resp
         
    color = request.cookies.get('color') 
    backgroundcolor = request.cookies.get('backgroundcolor')
    fontsize = request.cookies.get('fontsize')
    headers = request.cookies.get('headers')   
    resp = make_response(render_template('lab3/settings.html', color=color, backgroundcolor=backgroundcolor, fontsize=fontsize, headers=headers)) 
    return resp

@lab3.route('/lab3/del_settings')
def del_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.set_cookie('color') 
    resp.set_cookie('backgroundcolor')
    resp.set_cookie('fontsize')
    resp.set_cookie('headers')
    return resp


@lab3.route('/lab3/train')
def train():
    ticket = 0
    FIO = request.args.get('FIO')
    age = request.args.get('age')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    place1 = request.args.get('place1')
    place2 = request.args.get('place2')
    date = request.args.get('date')
    belay = request.args.get('belay')
    if age is None:
        age = 0
    else:
        age = int(age)
    if age < 18:
        ticket += 700
        ticket_type = "Детский билет"
    else:
        ticket += 1000
        ticket_type = "Взрослый билет"
    if shelf == 'lower' or shelf == 'lower-side':
        ticket += 100
    if linen == 'withlinen':
        ticket += 75
    if baggage == 'withbaggage':
        ticket += 250
    if belay == 'withbelay':
        ticket += 150
    return render_template('lab3/train.html', FIO=FIO, age=age, ticket=ticket, shelf=shelf, linen=linen, baggage=baggage, belay=belay, ticket_type=ticket_type, place1=place1, place2=place2, date=date)

@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket.html')

