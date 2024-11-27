# manage.py

from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask.cli import with_appcontext
import click

# Инициализация миграций
migrate = Migrate(app, db)

# Регистрация команд миграций в flask
@app.cli.command('db init')
def init_db():
    """Инициализация базы данных"""
    print("Initializing database...")

@app.cli.command('db migrate')
@with_appcontext
def migrate_db():
    """Создание миграций"""
    from flask_migrate import upgrade, migrate, init
    print("Creating migration...")
    migrate()

@app.cli.command('db upgrade')
def upgrade_db():
    """Применение миграций"""
    from flask_migrate import upgrade
    print("Upgrading database...")
    upgrade()

if __name__ == '__main__':
    app.run(debug=True)
