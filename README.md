# 📋 Telegram Form Bot → Google Sheets

Телеграм-бот, который собирает анкету пользователя на русском или узбекском языке и сохраняет данные прямо в **Google Sheets** через **Make (Webhook)**.

---

## 🚀 Возможности
- 🌐 Выбор языка: 🇷🇺 Русский / 🇺🇿 O‘zbek  
- 📝 Пошаговое заполнение анкеты  
- 📅 Проверка правильности даты рождения (формат `ДД.ММ.ГГГГ`)  
- 📞 Проверка телефонного номера (только цифры)  
- 🔗 Интеграция с **Google Sheets** через Make Webhook  
- ✅ Валидация всех вводимых данных

---

## 🛠 Технологии
- **Python 3.13**
- **aiogram** — асинхронный Telegram Bot API
- **python-dotenv** — хранение токенов и ключей в `.env`
- **requests** — отправка данных в Make
- **re (RegEx)** — валидация данных

---

## 📂 Структура проекта
Proect2/
├── bot.py # Точка входа бота
├── config.py # Загрузка токенов и Webhook из .env
├── handlers.py # Логика бота и валидация данных
├── localizations.py # Тексты на русском и узбекском
├── states.py # FSM состояния анкеты
├── requirements.txt # Зависимости проекта
├── .env # Токен бота и Webhook (в Git не попадает)
└── README.md # Описание проекта

yaml
Копировать
Редактировать

---

## 📦 Установка и запуск
```bash
# 1. Клонируем репозиторий
git clone https://github.com/MrGVR-dev/telegram-form-bot.git
cd telegram-form-bot

# 2. Создаём виртуальное окружение
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/Mac

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Создаём .env файл и добавляем:
BOT_TOKEN=твой_токен_бота
MAKE_WEBHOOK=твой_webhook_make

# 5. Запускаем бота
python bot.py
📸 Пример работы
Пользователь пишет /start

Выбирает язык

Заполняет поля анкеты

Данные отправляются в Google Sheets

🔒 Безопасность
Файл .env добавлен в .gitignore — токены не попадут в GitHub

Можно добавить лимиты на количество запросов в минуту

🧑‍💻 Автор
Telegram: @MrGVR

GitHub: MrGVR-dev
