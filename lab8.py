from flask import Blueprint, render_template, request, session,redirect, current_app, flash, url_for
from db import db
from db.models import users,articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_
lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    user_login = session.get('login', "anonymous")  # Получаем логин пользователя из сессии или устанавливаем "anonymous" по умолчанию
    return render_template('lab8/lab8.html', login=session.get('login'))

@lab8.route('/lab8/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    # Получаем логин и пароль из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверяем, существует ли пользователь с таким логином
    login_exists = users.query.filter_by(login=login_form).first() #SELECT * FROM users WHERE login = :login LIMIT 1
    if login_exists:
        return render_template('lab8/register.html', error = 'Такой пользователь уже существует')
    
    # Хэшируем пароль и создаём нового пользователя
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    # Логиним нового пользователя и сохраняем логин в сессии
    login_user(new_user)
    session['login'] = login_form
    return redirect('/lab8/')

# Вход пользователя
@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
            return render_template('lab8/login.html')
    
    # Получаем данные из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    # Проверяем наличие пользователя в базе данных
    user = users.query.filter_by(login = login_form).first()
    if user:
         if check_password_hash(user.password, password_form):
              login_user(user) # Авторизуем пользователя
              session['login'] = user.login # Сохраняем логин в сессии
              return redirect ('/lab8/')
    
    # В случае ошибки отображаем сообщение
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверны')

# Список статей текущего пользователя
@lab8.route('/lab8/articles', methods=['GET'])
@login_required
def articles_list():
    # Получаем статьи, принадлежащие текущему пользователю
    all_articles = articles.query.filter_by(user_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=all_articles)

# Выход пользователя
@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user() # Завершаем сессию пользователя
    session.pop('login', None) # Удаляем логин из сессии
    return redirect('/lab8/')

# Создание новой статьи
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    # Получаем данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')  

    if not title or not article_text:
        return render_template('lab8/create.html', error="Название и текст статьи обязательны.")

    # Создаём новую статью
    new_article = articles(
        user_id=current_user.id,
        title=title,
        article_text=article_text,
    )

    # Сохраняем статью в базе данных
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles')

# Редактирование статьи
@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id) # Получаем статью по её ID

    # Проверяем, принадлежит ли статья текущему пользователю
    if article.user_id != current_user.id:
        return redirect('/lab8/articles')

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)

    # Получаем данные из формы. Обновляем данные статьи
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'  
    is_favorite = request.form.get('is_favorite') == 'on'  

    if not title or not article_text:
        return render_template('lab8/edit.html', article=article, error="Название и текст статьи обязательны.")

    # Обновляем статью
    article.title = title
    article.article_text = article_text
    article.is_public = is_public
    article.is_favorite = is_favorite
    db.session.commit()

    return redirect('/lab8/articles')

# Удаление статьи
@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    # Получаем статью по ID
    article = articles.query.get_or_404(article_id)
    
    # Проверяем, принадлежит ли статья текущему пользователю
    if article.user_id != current_user.id:
        return redirect ('/lab8')

    db.session.delete(article)
    db.session.commit()

    flash("Статья успешно удалена!", "success")
    return redirect ('/lab8/articles')
