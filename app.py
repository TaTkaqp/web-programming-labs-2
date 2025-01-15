import os
from app import app
from dotenv import load_dotenv

load_dotenv() 

# Получаем режим работы из переменной окружения
environment = os.environ.get("FLASK_ENV", "production")

if __name__ == "__main__":
    # Включаем отладочный режим только для разработки
    debug = environment == "development"

    # Получаем порт из переменной окружения или используем 5000 по умолчанию
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug)
