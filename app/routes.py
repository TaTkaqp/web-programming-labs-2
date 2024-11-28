from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.models import User, Message
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import DeleteMessageForm
import re

# Главная страница, доступная только для авторизованных пользователей
@app.route('/')
@login_required
def index():
    # Если текущий пользователь администратор, перенаправляем его на панель администратора
    if current_user.is_admin():
        return redirect(url_for('admin'))  # Панель администратора

    # Получение всех пользователей, кроме текущего
    users = User.query.filter(User.id != current_user.id, User.role != 'admin').all()

    # Получение последних сообщений для каждого пользователя
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
        flash('Сообщение не может быть пустым!', 'danger')
        return redirect(url_for('index'))

    receiver = User.query.get(receiver_id)

    if receiver:
        message = Message(text=text, sender_id=current_user.id, receiver_id=receiver.id)
        db.session.add(message)
        db.session.commit()
        flash('Ваше сообщение было отправлено!', 'success')
    else:
        flash('Получатель не найден!', 'danger')

    return redirect(url_for('index'))

# Чат с пользователем
@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    user = User.query.get_or_404(user_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user.id)) |
        ((Message.sender_id == user.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    form = DeleteMessageForm()  # Форма для удаления сообщений

    if request.method == 'POST':
        text = request.form['message']
        if text:
            message = Message(text=text, sender_id=current_user.id, receiver_id=user.id)
            db.session.add(message)
            db.session.commit()
            flash('Сообщение отправлено!', 'success')
            return redirect(url_for('chat', user_id=user.id))

    return render_template('chat.html', user=user, messages=messages, form=form)

# Удаление аккаунта
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        db.session.delete(current_user)  # Удаление текущего пользователя
        db.session.commit()  # Сохранение изменений в базе данных
        flash('Ваш аккаунт был успешно удален.', 'success')
        return redirect(url_for('login'))  # Перенаправление на страницу входа
    except Exception as e:
        db.session.rollback()  # Откат изменений в случае ошибки
        flash('Произошла ошибка при удалении аккаунта.', 'danger')
        return redirect(url_for('index'))  # Перенаправление на главную страницу

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка на существующего пользователя
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Такой пользователь уже существует. Пожалуйста, выберите другое имя.', 'danger')
            return redirect(url_for('register'))

        # Проверка пароля: только латинские буквы и минимум 6 символов
        if not re.match("^[A-Za-z0-9]{6,}$", password):
            flash('Пароль должен содержать только латинские буквы и цифры и быть длиной не менее 6 символов.', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт был создан! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Панель администратора
@app.route('/admin')
@login_required
def admin():
    if current_user.is_admin():  # Проверяем, является ли текущий пользователь администратором
        users = User.query.all()  # Получаем всех пользователей
        return render_template('admin_panel.html', users=users)
    else:
        flash('У вас нет прав для просмотра этой страницы.', 'danger')
        return redirect(url_for('index'))

# Удаление сообщения
@app.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)

    if message.sender_id == current_user.id or message.receiver_id == current_user.id:
        try:
            db.session.delete(message)
            db.session.commit()
            flash('Сообщение успешно удалено!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при удалении сообщения.', 'danger')
    else:
        flash('У вас нет прав на удаление этого сообщения.', 'danger')

    return redirect(url_for('chat', user_id=message.receiver_id if message.sender_id == current_user.id else message.sender_id))

# Удаление пользователя
@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.is_admin():
        user_to_delete = User.query.get_or_404(user_id)

        Message.query.filter(
            (Message.sender_id == user_to_delete.id) |
            (Message.receiver_id == user_to_delete.id)
        ).delete()

        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Пользователь был успешно удален!', 'success')
        return redirect(url_for('admin'))
    else:
        flash('У вас нет прав на выполнение этого действия.', 'danger')
        return redirect(url_for('admin'))

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin'))
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Добро пожаловать обратно, {user.username}!', 'success')

            if user.is_admin():
                return redirect(url_for('admin'))

            return redirect(url_for('index'))
        else:
            flash('Ошибка входа. Проверьте имя пользователя и пароль.', 'danger')

    return render_template('login.html')

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

@app.before_request
def before_request():
    if current_user.is_authenticated:
        pass
