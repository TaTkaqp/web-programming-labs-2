from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.models import User, Message
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import DeleteMessageForm
import re

# Главная страница, доступна только авторизованным пользователям
@app.route('/')
@login_required
def index():
    # Если текущий пользователь администратор, перенаправляем на панель администратора
    if current_user.is_admin():
        return redirect(url_for('admin'))  # Панель администратора

    # Получаем всех пользователей, кроме текущего
    users = User.query.filter(User.id != current_user.id, User.role != 'admin').all()

    # Получаем последние сообщения для каждого пользователя
    last_messages = {}
    for user in users:
        last_message = Message.query.filter(
            (Message.sender_id == current_user.id) & (Message.receiver_id == user.id) |
            (Message.sender_id == user.id) & (Message.receiver_id == current_user.id)
        ).order_by(Message.timestamp.desc()).first()

        last_messages[user.id] = last_message

    return render_template('index.html', users=users, last_messages=last_messages)

# Отправка сообщения
@app.route('/send_message/<int:receiver_id>', methods=['POST'])
@login_required
def send_message(receiver_id):
    text = request.form['message']

    if not text:
        flash('Message cannot be empty!', 'danger')
        return redirect(url_for('index'))

    receiver = User.query.get(receiver_id)

    if receiver:
        message = Message(text=text, sender_id=current_user.id, receiver_id=receiver.id)
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent!', 'success')
    else:
        flash('Receiver not found!', 'danger')

    return redirect(url_for('index'))





@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    user = User.query.get_or_404(user_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user.id)) |
        ((Message.sender_id == user.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    form = DeleteMessageForm()  # Создаем форму для удаления сообщений

    if request.method == 'POST':
        text = request.form['message']
        if text:
            message = Message(text=text, sender_id=current_user.id, receiver_id=user.id)
            db.session.add(message)
            db.session.commit()
            flash('Message sent!', 'success')
            return redirect(url_for('chat', user_id=user.id))

    return render_template('chat.html', user=user, messages=messages, form=form)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        # Удаляем все связанные записи с пользователем
        db.session.delete(current_user)  # Удаление пользователя
        db.session.commit()  # Подтверждение изменений в базе данных
        flash('Your account has been deleted successfully.', 'success')  # Успешное удаление
        return redirect(url_for('login'))  # Перенаправление на страницу входа
    except Exception as e:
        db.session.rollback()  # Откат изменений в случае ошибки
        flash('An error occurred while deleting your account.', 'danger')  # Ошибка
        return redirect(url_for('index'))  # Перенаправление на главную страницу

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка на существование пользователя
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('User already exists. Please choose a different username.', 'danger')
            return redirect(url_for('register'))

        # Проверка пароля: только латинские символы и минимум 6 символов
        if not re.match("^[A-Za-z0-9]{6,}$", password):
            flash('Password must contain only Latin letters and digits and be at least 6 characters long.', 'danger')
            return redirect(url_for('register'))

        # Хеширование пароля
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/admin')
@login_required
def admin():
    if current_user.is_admin():  # Проверяем, является ли текущий пользователь администратором
        users = User.query.all()  # Получаем всех пользователей

        return render_template('admin_panel.html', users=users)
    else:
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('index'))  # Перенаправляем на главную страницу

# Удаление сообщения
@app.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    # Находим сообщение по ID
    message = Message.query.get_or_404(message_id)

    # Проверка: если это сообщение текущего пользователя или его собеседника
    if message.sender_id == current_user.id or message.receiver_id == current_user.id:
        try:
            db.session.delete(message)  # Удаляем сообщение
            db.session.commit()  # Подтверждаем изменения
            flash('Message deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()  # Откат изменений в случае ошибки
            flash('An error occurred while deleting the message.', 'danger')
    else:
        flash('You do not have permission to delete this message.', 'danger')

    # Перенаправляем обратно в чат с этим собеседником
    return redirect(url_for('chat', user_id=message.receiver_id if message.sender_id == current_user.id else message.sender_id))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.is_admin():  # Проверяем, является ли текущий пользователь администратором
        user_to_delete = User.query.get_or_404(user_id)

        # Удаляем все связанные сообщения с этим пользователем
        Message.query.filter(
            (Message.sender_id == user_to_delete.id) |
            (Message.receiver_id == user_to_delete.id)
        ).delete()

        db.session.delete(user_to_delete)  # Удаляем пользователя
        db.session.commit()  # Подтверждаем изменения в базе данных
        flash('User has been deleted successfully!', 'success')
        return redirect(url_for('admin'))  # Перенаправляем на админскую панель
    else:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('admin'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Если пользователь уже авторизован, перенаправляем в зависимости от его роли
        if current_user.is_admin():  # Если администратор, перенаправляем на админ-панель
            return redirect(url_for('admin'))
        return redirect(url_for('index'))  # Для обычных пользователей на главную страницу

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Поиск пользователя в базе данных
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)  # Авторизуем пользователя

            flash(f'Welcome back, {user.username}!', 'success')

            # Если это администратор, перенаправляем на админ-панель
            if user.is_admin():
                return redirect(url_for('admin'))

            # Для обычных пользователей перенаправляем на главную страницу
            return redirect(url_for('index'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html')


# Страница логаута
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# Дополнительная кастомизация для обработки авторизации на всех страницах
@app.before_request
def before_request():
    if current_user.is_authenticated:
        # Это можно использовать для логики или информации о текущем пользователе
        pass
