import telebot
import datetime
import time

from utils import load_phrases, load_progress, save_progress, get_next_review_interval, should_show_phrase
from utils import choose_language, get_phrase_by_guid, get_translation, get_random_phrase_and_text

from config import TOKEN


bot = telebot.TeleBot(TOKEN)

# словарь для хранения выбора пользователя
user_topics = {}

@bot.message_handler(commands=['help'])
def help_message(message):
    user_id = message.chat.id
    help_text = (
        "Я помогу тебе запоминать IT-фразы!\n"
        "📌 Команды:\n"
        "🔹 /start - Начать работу\n"
        "🔹 Модули - Выбрать тему для изучения\n"
        "🔹 Стоп - Завершить текущую сессию\n"
        "🔹 /help - Справка"
    )
    bot.send_message(user_id, help_text)

# приветствие от бота
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Привет! Я помогу тебе запомнить фразы для коммуникации в IT.", reply_markup=get_modules_button())

# список модулей
def get_modules_button():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("📚 Модули", callback_data='modules'))
    return markup

# Обработчик кнопки "Модули"
@bot.callback_query_handler(func=lambda call: call.data == "modules")
def handle_modules_list(call):
    modules_message(call.message)

def modules_message(message, selected_module=None):
    user_id = message.chat.id
    modules_with_count = []
    module_mapping = {}  # Словарь для соответствия номеров и модулей

    # Если модуль не передан, загружаем все модули
    if selected_module is None:
        phrases_data = load_phrases()
        modules = phrases_data["modules"]
    else:
        modules = [selected_module]

    index = 1  # Нумерация модулей
    for module in modules:
        module_name = module["name"]
        modules_with_count.append(
            telebot.types.InlineKeyboardButton(f"{module_name}", callback_data=f"module_{index}")
        )
        module_mapping[str(index)] = module  # Запоминаем модуль по номеру
        index += 1

    # Сохраняем маппинг для пользователя
    user_topics[message.chat.id] = {'modules': module_mapping}

    # Отправляем список модулей в виде кнопок
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(*modules_with_count)
    bot.send_message(user_id, "Доступные модули:", reply_markup=markup)

# Обработчик выбора модуля
@bot.callback_query_handler(func=lambda call: call.data.startswith('module_'))
def handle_module_selection(call):
    user_id = call.message.chat.id
    selected_number = call.data.split('_')[1]
    
    # Получаем выбранный модуль
    module_mapping = user_topics.get(user_id, {}).get('modules', {})
    selected_module = module_mapping.get(selected_number)
    
    if selected_module:
        topics_message(call.message, selected_module, selected_number)
    else:
        bot.send_message(user_id, "❌ Некорректный выбор. Выберите модуль заново.", reply_markup=get_modules_button())

def topics_message(message, selected_module, selected_number):
    user_id = message.chat.id
    topics_with_count = []
    topic_mapping = {}  # Словарь для соответствия номеров и тем

    index = 1  # Нумерация тем
    for topic in selected_module["topics"]:
        topic_name = topic["name"]
        phrases = topic.get("phrases", [])
        phrase_count = len(phrases)
        progress = load_progress()  # Загружаем текущий прогресс
        learned_phrase_count = len([phrase for phrase in phrases if should_show_phrase(user_id, phrase, progress, phrases)])

        topics_with_count.append(
            telebot.types.InlineKeyboardButton(f"{topic_name} ({learned_phrase_count} из {phrase_count})", callback_data=f"topic_{index}")
        )
        topic_mapping[str(index)] = topic  # Запоминаем тему по номеру
        index += 1

    # Сохраняем маппинг для пользователя
    if user_id not in user_topics:
        user_topics[user_id] = {}

    user_topics[user_id]['topics'] = topic_mapping

    # Отправляем список тем в виде кнопок
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(*topics_with_count)
    markup.add(telebot.types.InlineKeyboardButton("🔙 Назад", callback_data=f"back_to_modules"))
    bot.send_message(user_id, "Доступные темы в модуле:", reply_markup=markup)


# Обработчик кнопки "Назад" для возврата к выбору модулей
@bot.callback_query_handler(func=lambda call: call.data == 'back_to_modules')
def handle_back_to_modules(call):
    user_id = call.message.chat.id
    selected_module = user_topics.get(user_id, {}).get("last_selected_module")
    modules_message(call.message, selected_module)


# Обрабатывает выбор темы
@bot.callback_query_handler(func=lambda call: call.data.startswith('topic_'))
def handle_topic_selection(call):
    user_id = call.message.chat.id
    selected_number = call.data.split('_')[1]
    
    # Получаем выбранную тему
    topic_mapping = user_topics.get(user_id, {}).get('topics', {})
    selected_topic = topic_mapping.get(selected_number)

    # сохранение выбранной темы
    user_topics[user_id]["last_selected_topic"] = selected_topic
    
    if selected_topic:
        phrases = selected_topic.get("phrases", [])
        if phrases:
            progress = load_progress()  # Загружаем текущий прогресс
            learned_phrase_count = len([phrase for phrase in phrases if should_show_phrase(user_id, phrase, progress, phrases)])

            bot.send_message(
                user_id, 
                f"✅ Вы выбрали тему: *{selected_topic['name']}*\n\nФраз для изучения: {learned_phrase_count} из {len(phrases)}", 
                parse_mode="Markdown",
                reply_markup=telebot.types.ReplyKeyboardRemove()  # Убираем клавиатуру
            )
            start_training(user_id, phrases)
        else:
            bot.send_message(user_id, "⚠️ В этой теме нет фраз. Выберите другую.", reply_markup=telebot.types.ReplyKeyboardRemove())
            topics_message(call.message, selected_topic, selected_number)  # Показываем список тем снова
    else:
        bot.send_message(user_id, "❌ Некорректный выбор. Выберите тему заново.", reply_markup=telebot.types.ReplyKeyboardRemove())
        topics_message(call.message, selected_topic, selected_number)  # Показываем список тем снова



# Начало изучения фраз
def start_training(user_id, phrases):
    progress = load_progress()  # Загружаем текущий прогресс

    # Получаем случайную фразу и текст
    phrase, context, text, language = get_random_phrase_and_text(user_id, phrases, progress)

    if phrase:        
        # Отправляем и ожидаем действия пользователя
        bot.send_message(
            user_id, 
            f"Контекст: _{context}_\n\n{text}", 
            parse_mode="Markdown",
            reply_markup=get_translation_button(phrase, language))
    else:
        bot.send_message(user_id, 
                         "Все фразы по данной теме повторены. Продолжите повторение завтра или выберите другую тему.\nНажми кнопку 'Модули' для выбора новой темы.", 
                         reply_markup=get_modules_button())

# Кнопка для запроса перевода фразы
def get_translation_button(phrase, language):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton('🔍 Перевод', callback_data=f"translate_{phrase['guid']}_{language}"),
        telebot.types.InlineKeyboardButton('🍹🏖️🌊 Стоооп', callback_data=f"stop_{phrase['guid']}")
    )
    return markup

# Обработчик кнопки Стоп
@bot.callback_query_handler(func=lambda call: call.data.startswith('stop_'))
def handle_stop(call):
    user_id = call.message.chat.id
    bot.send_message(user_id, "Чтобы продолжить, нажми кнопку 'Модули' для просмотра списка тем.",
                     reply_markup=get_modules_button())

 # Обработчик запроса перевода
@bot.callback_query_handler(func=lambda call: call.data.startswith('translate_'))
def handle_translation_request(call):
    user_id = call.message.chat.id
    # Извлекаем GUID фразы и язык из callback_data
    data = call.data.split('_')
    phrase_guid = data[1]
    language = data[2]
    phrase = get_phrase_by_guid(phrase_guid)  # Функция для получения фразы по GUID

    if not phrase:
        bot.send_message(user_id, "Ошибка! Фраза не найдена.")
        return    

    # Получаем перевод с помощью функции
    translation = get_translation(phrase, language)

    # Отправляем перевод фразы
    bot.send_message(user_id, translation, reply_markup=get_repeat_or_remember_button(phrase))


# Кнопки для выбора действия пользователя
def get_repeat_or_remember_button(phrase):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton('✅ Запомнил', callback_data=f"remembered_{phrase['guid']}"),
        telebot.types.InlineKeyboardButton('🔄 Повторить', callback_data=f"repeat_{phrase['guid']}")
    )
    return markup

# Обработка ответа пользователя (Запомнил / Повторить)
@bot.callback_query_handler(func=lambda call: call.data.startswith(('remembered', 'repeat')))
def handle_user_response(call):
    user_id = call.message.chat.id
    progress = load_progress()  # Загружаем текущий прогресс
    user_progress = progress.get(str(user_id), {})

    # Получаем последнюю выбранную тему
    selected_topic = user_topics.get(user_id, {}).get("last_selected_topic")

    if not selected_topic:
        bot.send_message(user_id, "Ошибка! Не удалось определить выбранную тему. Выберите тему заново.", reply_markup=get_modules_button())
        return

    phrases = selected_topic.get("phrases", [])  # Берем фразы из выбранной темы

    # Извлекаем action (remembered или repeat) и guid фразы из callback_data
    action, phrase_guid = call.data.split('_', 1)

    # Ищем фразу по GUID в текущей теме
    phrase = next((p for p in phrases if p["guid"] == phrase_guid), None)
    
    if not phrase:
        bot.send_message(user_id, "Ошибка! Не удалось найти фразу.")
        return

    # Инициализация прогресса, если его еще нет
    if str(user_id) not in progress:
        progress[str(user_id)] = {}

    phrase_progress = user_progress.get(phrase['guid'], {'repetition_stage': 0, 'last_reviewed': str(datetime.datetime.now().date())})

    if action == 'remembered':
        # Увеличиваем этап повторений
        phrase_progress['repetition_stage'] += 1
    elif action == 'repeat':
        # Уменьшаем этап повторений
        phrase_progress['repetition_stage'] = max(0, phrase_progress['repetition_stage'] - 1)

    # Обновляем дату последнего повторения
    phrase_progress['last_reviewed'] = str(datetime.datetime.now().date())
    user_progress[phrase['guid']] = phrase_progress
    progress[str(user_id)] = user_progress  # Обновляем прогресс пользователя
    save_progress(progress)  # Сохраняем прогресс

    # Оповещаем пользователя
    if action == 'remembered':
        bot.send_message(user_id, f"Фраза обновлена. Следующее повторение через {get_next_review_interval(phrase_progress['repetition_stage'])} дня.\n\n"
                                  f"Оставшиеся фразы для повторения: {len([p for p in phrases if should_show_phrase(user_id, p, progress, phrases)])} из {len(phrases)}.")
    elif action == 'repeat':
        bot.send_message(user_id, "Фраза оставлена в списке на изучение.")

    # Повторяем обучение
    start_training(user_id, phrases)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)  # Добавляем паузу перед перезапуском
