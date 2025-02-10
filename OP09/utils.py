import os
import json
import datetime
import random

from config import PHRASES_FILE, DATA_FILE


# Загрузка данных из файла phrases.json
def load_phrases():
    if os.path.exists(PHRASES_FILE):
        with open(PHRASES_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}

# Загрузка прогресса пользователя из файла
def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}
    
# Сохранение прогресса в файл
def save_progress(progress):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(progress, file, ensure_ascii=False, indent=4)

# Получить интервал для следующего повторения
def get_next_review_interval(repetition_stage):
    intervals = [1, 3, 7, 14, 30]
    return intervals[min(repetition_stage, len(intervals) - 1)]

# Проверка, нужно ли показывать фразу
def should_show_phrase(user_id, phrase, progress, phrases):
    user_progress = progress.get(str(user_id), {})
    phrase_progress = user_progress.get(phrase['guid'], None)

    if not phrase_progress:
        return True  # Если фраза еще не изучалась, показываем ее
    
    last_reviewed = datetime.datetime.strptime(phrase_progress['last_reviewed'], '%Y-%m-%d')
    interval_days = get_next_review_interval(phrase_progress['repetition_stage'])
    
    # Если фраза не запомнена (repetition_stage == 0), она может появляться снова в тот же день
    if phrase_progress['repetition_stage'] == 0:
        return True

    # Проверяем, пришел ли срок повторения
    if (datetime.datetime.now() - last_reviewed).days >= interval_days:
        return True

    return False

# выбирает язык для следущей фразы
def choose_language():
    return random.choice(['ru', 'en'])

# Функция для получения фразы по guid
def get_phrase_by_guid(guid):
    # Здесь должен быть код для поиска фразы по ее guid
    # например, в списке фраз или в базе данных
    for module in load_phrases()["modules"]:
        for topic in module["topics"]:
            for phrase in topic.get("phrases", []):
                if phrase['guid'] == guid:
                    return phrase
    return None  # Если фраза не найдена

# Функция для выбора фразы и языка
def get_random_phrase_and_text(user_id, phrases, progress):
    # Фильтруем фразы, которые нужно повторить
    due_phrases = [phrase for phrase in phrases if should_show_phrase(user_id, phrase, progress, phrases)]
    
    if due_phrases:
        phrase = random.choice(due_phrases)  # Выбираем случайную фразу из тех, что нужно учить
        language = choose_language()  # Выбираем язык

        context = phrase['context']
        
        # Возвращаем текст фразы на выбранном языке
        if language == 'ru':
            text = phrase['ru']
        else:
            text = phrase['en']
        
        return phrase, context, text, language
    else:
        return None, None, None, None  # Если фраз для повторения нет, возвращаем None

# Функция для получения перевода фразы
def get_translation(phrase, language):
    if language == 'ru':
        return phrase['en']  # Возвращаем перевод на русский
    else:
        return phrase['ru']  # Возвращаем перевод на английский
