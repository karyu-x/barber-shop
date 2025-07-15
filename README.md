# 💈 Barber Project

Telegram-бот для бронирования в барбершопе, с административной и пользовательской панелью.

---

## 📦 Возможности

- 📅 Бронирование времени пользователем
- ✅ Подтверждение администрацией
- ❌ Отмена брони с указанием причины
- 🧑‍💼 FSM для пошаговых меню
- 📑 История записей
- 🌐 Мультиязычность (RU / UZ / EN)

---

## 🚀 Установка

1. Клонируй репозиторий:

```bash
git clone https://github.com/yourusername/barber_project.git
cd barber_project
```

2. Создай и активируй виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

3. Установи зависимости:

```bash
pip install -r requirements.txt
```

4. ⚙️ Настройки
Создай файл .env:

BOT_TOKEN=your_bot_token_here
BASE_URL=https://your.backend.api


5. ▶️ Запуск

```bash
python main.py
```

📁 Структура проекта

barber_project/
│
├── handlers/          # Хендлеры
│   ├── user/          # Пользовательские
│   └── admin/         # Административные
│
├── keyboards/         # Кнопки
│
├── states/            # FSM состояния
│
├── database.py        # Работа с API/БД
├── config.py          # Настройки проекта
├── main.py            # Точка входа
├── requirements.txt   # Зависимости
├── .gitignore
└── README.md