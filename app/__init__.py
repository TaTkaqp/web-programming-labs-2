from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate  # Импортируем Migrate
import click

# Инициализация расширений
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'  # Замените на ваш секретный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Настройка для базы данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)  # Инициализируем Flask-Migrate

# Устанавливаем, куда перенаправлять пользователей, если они не авторизованы
login_manager.login_view = 'login'  # Указывает, что делать, если пользователь не авторизован

# Импортируем модели
from app import routes
from app.models import User

# Указываем функцию для загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.cli.command('create_admin')
@click.argument('username')
@click.argument('password')
def create_admin(username, password):
    """Создание пользователя с ролью админа."""
    # Проверим, существует ли уже админ
    admin = User.query.filter_by(username=username).first()
    if admin:
        print(f"User {username} already exists.")
        return

    # Хешируем пароль
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Создаем нового пользователя с ролью admin
    admin_user = User(username=username, password=hashed_password, role='admin')
    db.session.add(admin_user)
    db.session.commit()
    print(f"Admin user {username} created successfully.")
