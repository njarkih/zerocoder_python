[English](#english) | [Русский](#русский)

---

# <a name="русский"></a>Telegram-бот для изучения английских фраз

Простой Telegram-бот, который помогает пользователям изучать английские фразы с использованием интервального повторения.

## Возможности
- Предустановленный набор фраз, разделённый по темам.
- Система интервального повторения: 1 день → 3 дня → 7 дней → 14 дней → 30 дней.
- Отслеживание прогресса пользователя, сохранение данных в `data.json`.
- Возможность выбрать тему для тренировки.
- Простая структура хранения данных в JSON (без базы данных).

## Установка

### Требования
- Python 3.8+
- Токен Telegram-бота (полученный через BotFather)

### Настройка
1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/your-username/telegram-phrase-bot.git
   cd telegram-phrase-bot
   ```
2. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```
3. Создайте файл `config.py` и добавьте ваш токен бота:
   ```python
   TOKEN = "your-telegram-bot-token"
   DATA_FILE = "data.json"
   PHRASES_FILE = "phrases.json"
   ```
4. Запустите бота:
   ```sh
   python bot.py
   ```

## Структура файлов
```
telegram-phrase-bot/
│── bot.py            # Основная логика бота
│── config.py         # Конфигурация (токен бота, пути к файлам)
│── data.json         # Хранение прогресса пользователя (создаётся автоматически)
│── phrases.json      # Предустановленные фразы
│── utils.py          # Вспомогательные функции (работа с JSON, логика повторений)
│── requirements.txt  # Зависимости проекта
│── README.md         # Документация проекта
```

## Использование
- Запустите бота и выберите тему.
- Бот отправит фразу на английском или русском.
- Посмотрите перевод и отметьте "Запомнил" или "Повторить".
- Бот запланирует следующее повторение в зависимости от вашего ответа.
- Отслеживайте прогресс и тренируйтесь по выбранным темам.

## Участие в разработке
Приветствуются pull request'ы! Вы можете улучшить функциональность или добавить новые возможности.

## Лицензия
Лицензия MIT

---

# <a name="english"></a>Telegram Bot for Learning English Phrases

A simple Telegram bot that helps users learn English phrases through spaced repetition.

## Features
- Predefined phrases categorized by topics.
- Spaced repetition system: 1 day → 3 days → 7 days → 14 days → 30 days.
- User progress tracking saved in `data.json`.
- Ability to choose a topic for practice.
- Simple JSON-based storage (no database required).

## Installation

### Prerequisites
- Python 3.8+
- A Telegram bot token (obtained via BotFather)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/telegram-phrase-bot.git
   cd telegram-phrase-bot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `config.py` file and add your bot token:
   ```python
   TOKEN = "your-telegram-bot-token"
   DATA_FILE = "data.json"
   PHRASES_FILE = "phrases.json"
   ```
4. Run the bot:
   ```sh
   python bot.py
   ```

## File Structure
```
telegram-phrase-bot/
│── bot.py            # Main bot logic
│── config.py         # Configuration (bot token, file paths)
│── data.json         # User progress storage (created automatically)
│── phrases.json      # Predefined phrases
│── utils.py          # Helper functions (JSON handling, repetition logic)
│── requirements.txt  # Dependencies
│── README.md         # Project documentation
```

## Usage
- Start the bot and select a topic.
- The bot will send a phrase in English or Russian.
- View the translation and mark it as "Remembered" or "Repeat".
- The bot schedules the next repetition based on your response.
- Track your progress and focus on specific topics.

## Contributing
Pull requests are welcome! Feel free to improve functionality or add new features.

## License
MIT License

