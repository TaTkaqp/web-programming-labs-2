from flask import Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    if 'message' in session:
        message = session['message']
        image = session['image']
        return render_template('lab9/congratulation.html', message=message, image=image)
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/lab9.html')


@lab9.route('/lab9/age/', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form['age']
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)


@lab9.route('/lab9/gender/', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form['gender']
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)


@lab9.route('/lab9/preference/', methods=['GET', 'POST'])
def preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    
    if request.method == 'POST':
        preference = request.form['preference']
        return redirect(url_for('lab9.sub_preference', name=name, age=age, gender=gender, preference=preference))
    return render_template('lab9/preference.html', name=name)


@lab9.route('/lab9/sub_preference/', methods=['GET', 'POST'])
def sub_preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')

    if request.method == 'POST':
        sub_preference = request.form['sub_preference']
        return redirect(url_for('lab9.congratulation', name=name, age=age, gender=gender, preference=preference, sub_preference=sub_preference))
    return render_template('lab9/sub_preference.html', name=name)


@lab9.route('/lab9/congratulation/')
def congratulation():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    sub_preference = request.args.get('sub_preference')

    message = ""
    image = ""

    if age < 18:
        message = f"Поздравляю тебя, {name}! Желаю тебе чудесных приключений и ярких моментов в жизни. Будь всегда {'' if gender == 'male' else 'всегда'}  дружелюбным{' и смелым' if gender == 'male' else ' и смелой'}, и, конечно же, наслаждайся каждым днем. Вот тебе подарок — "

        if preference == 'вкусное':
            if sub_preference == 'сладкое':
                message += "шоколадное пирожное."
                image = 'lab9/sugar.jpg'
            else: 
                message += "салат оливье"
                image = 'lab9/olivie.webp'
        else:  
            if sub_preference == 'декоративное':
                message += "красивую гирлянду."
                image = 'lab9/girlyanda.webp'
            else: 
                message += "мягкую игрушку."
                image = 'lab9/plush_toy.jpg'
    else:
        message = f"Поздравляю, {name}! Желаю тебе больших успехов в любых начинаниях. Пусть каждый день наполняется вдохновением и радостью. Вот твой подарок — "

        if preference == 'вкусное':
            if sub_preference == 'сладкое':
                message += "конфеты."
                image = 'lab9/cand.webp'
            else: 
                message += "селедка под шубой"
                image = 'lab9/shuba.jpg'
        else:  
            if sub_preference == 'декоративное':
                message += "красивый букет цветов."
                image = 'lab9/flowers.webp'
            else: 
                message += "варежки."
                image = 'lab9/sweet.jpg'

    session['message'] = message
    session['image'] = image
    return render_template('lab9/congratulation.html', message=message, image=image)


@lab9.route('/lab9/reset/')
def reset():
    session.clear()
    return redirect(url_for('lab9.lab'))

