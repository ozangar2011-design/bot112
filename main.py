import sqlite3

import telebot
import telebot
from telebot import types
import json
import os
from datetime import datetime

TOKEN = "ставте токен от телеграма сюда."

bot = telebot.TeleBot(TOKEN)

RESULTS_FILE = "../results.json"

questions = [
    {
        "question": "Как называется ошибка в коде, которую находят на этапе выполнения программы?",
        "answers": ["Синтаксическая", "Логическая", "Компиляции", "Ошибка выполнения (runtime error)"],
        "correct": 3
    },
    {
        "question": "Что такое переменная в программировании?",
        "answers": ["Именованная область памяти для хранения данных", "Функция для вывода текста", "Тип цикла", "Название языка программирования"],
        "correct": 0
    },
    {
        "question": "Какой оператор используется для сравнения на равенство в большинстве языков программирования (например Python, JS)?",
        "answers": ["=", "==", "!=", "<>"],
        "correct": 1
    },
    {
        "question": "Что делает цикл (loop) в программе?",
        "answers": ["Хранит данные", "Выводит ошибку", "Повторяет действия несколько раз", "Завершает программу"],
        "correct": 2
    },
    {
        "question": "Как называется набор инструкций, оформленный как отдельный именованный блок кода, который можно вызывать много раз?",
        "answers": ["Переменная", "Массив", "Функция", "Цикл"],
        "correct": 2
    },
    {
        "question": "Что такое массив?",
        "answers": ["Одно значение без имени", "Набор значений, хранящихся под одним именем", "Тип ошибки", "Команда для вывода текста"],
        "correct": 1
    },
    {
        "question": "Что делает условный оператор if?",
        "answers": ["Повторяет код несколько раз", "Хранит данные", "Выполняет код только если условие верно", "Останавливает программу навсегда"],
        "correct": 2
    },
    {
        "question": "Что означает термин 'баг' (bug) в программировании?",
        "answers": ["Новая функция", "Ошибка в программе", "Название языка", "Тип переменной"],
        "correct": 1
    },
    {
        "question": "Какой тип данных используется для хранения текста?",
        "answers": ["Integer", "Boolean", "String", "Float"],
        "correct": 2
    },
    {
        "question": "Что такое алгоритм?",
        "answers": ["Последовательность шагов для решения задачи", "Язык программирования", "Ошибка в коде", "Название переменной"],
        "correct": 0
    },
    {
        "question": "Какой тип данных хранит значения true или false?",
        "answers": ["String", "Boolean", "Integer", "Array"],
        "correct": 1
    },
    {
        "question": "Что делает функция print (или её аналог) в программе?",
        "answers": ["Считает сумму чисел", "Выводит информацию на экран", "Создаёт цикл", "Удаляет переменную"],
        "correct": 1
    },
    {
        "question": "Что такое компиляция?",
        "answers": ["Процесс превращения кода в программу, понятную компьютеру", "Процесс написания кода", "Тип ошибки", "Тип переменной"],
        "correct": 0
    },
    {
        "question": "Какой из вариантов является примером цикла?",
        "answers": ["if", "for", "print", "return"],
        "correct": 1
    },
    {
        "question": "Что делает оператор return в функции?",
        "answers": ["Начинает цикл", "Возвращает результат работы функции", "Создаёт переменную", "Выводит ошибку"],
        "correct": 1
    },
    {
        "question": "Что такое комментарий в коде?",
        "answers": ["Часть кода, которая выполняется первой", "Пояснение в коде, которое не выполняется программой", "Тип ошибки", "Функция для вывода текста"],
        "correct": 1
    },
    {
        "question": "Какой оператор используется для присваивания значения переменной в большинстве языков?",
        "answers": ["==", "=", "!=", "->"],
        "correct": 1
    },
    {
        "question": "Что такое IDE?",
        "answers": ["Язык программирования", "Программа для написания и запуска кода", "Тип ошибки", "Тип цикла"],
        "correct": 1
    },
    {
        "question": "Что произойдёт, если в коде есть синтаксическая ошибка?",
        "answers": ["Программа выполнится медленнее", "Программа не запустится", "Ничего не изменится", "Программа выполнится без изменений"],
        "correct": 1
    },
    {
        "question": "Что такое отладка (debugging)?",
        "answers": ["Написание нового кода с нуля", "Процесс поиска и исправления ошибок в коде", "Удаление программы", "Компиляция кода"],
        "correct": 1
    }
]

users = {}


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Начать тест", "Результаты")
    return markup


def load_results():
    if not os.path.exists(RESULTS_FILE):
        return []

    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_results(results):
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)


def save_result(name, user_id, score, answers):
    results = load_results()

    results.append({
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "name": name,
        "user_id": user_id,
        "score": score,
        "total": len(questions),
        "answers": answers
    })

    save_results(results)


def send_question(chat_id):
    user = users[chat_id]
    question_number = user["question"]
    question = questions[question_number]

    markup = types.InlineKeyboardMarkup(row_width=1)

    for index, answer in enumerate(question["answers"]):
        button = types.InlineKeyboardButton(
            text=answer,
            callback_data=f"answer:{index}"
        )
        markup.add(button)

    bot.send_message(
        chat_id,
        f"Вопрос {question_number + 1} из {len(questions)}\n\n{question['question']}",
        reply_markup=markup
    )


def start_test(chat_id, name=None):
    users[chat_id] = {
        "name": name or "",
        "question": 0,
        "score": 0,
        "answers": []
    }

    if name:
        bot.send_message(
            chat_id,
            f"Приятно познакомиться, {name}! Начинаем тест из 20 вопросов.",
            reply_markup=main_keyboard()
        )
        send_question(chat_id)


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id

    users[chat_id] = {
        "name": "",
        "question": 0,
        "score": 0,
        "answers": []
    }

    bot.send_message(
        chat_id,
        "Привет! Я помогу проверить знания по основам программирования.\n\nКак тебя зовут?",
        reply_markup=main_keyboard()
    )
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    chat_id = message.chat.id
    name = message.text.strip()

    if not name or name in ("Результаты", "Начать тест"):
        bot.send_message(chat_id, "Напиши своё имя.")
        bot.register_next_step_handler(message, get_name)
        return

    users[chat_id]["name"] = name

    bot.send_message(
        chat_id,
        f"Приятно познакомиться, {name}!\nНажми «Начать тест», чтобы начать.",
        reply_markup=main_keyboard()
    )


@bot.message_handler(func=lambda message: message.text == "Начать тест")
def start_test_button(message):
    chat_id = message.chat.id

    name = users.get(chat_id, {}).get("name", "")

    if not name:
        bot.send_message(chat_id, "Сначала нажми /start и введи своё имя.")
        return

    start_test(chat_id, name)


@bot.message_handler(func=lambda message: message.text == "Результаты")
def show_results(message):
    results = load_results()

    if not results:
        bot.send_message(message.chat.id, "Пока сохранённых результатов нет.")
        return

    text_parts = ["Сохранённые результаты:\n"]

    for number, result in enumerate(results, start=1):
        text_parts.append(
            f"{number}. {result['name']}\n"
            f"ID: {result['user_id']}\n"
            f"Дата: {result['date']}\n"
            f"Результат: {result['score']} из {result['total']}\n"
        )

        if result.get("answers"):
            text_parts.append("Ответы:")
            for answer in result["answers"]:
                mark = "✓" if answer["correct"] else "✗"
                text_parts.append(
                    f"{mark} {answer['number']}. {answer['selected']} "
                    f"(правильный: {answer['correct_answer']})"
                )

        text_parts.append("")

    full_text = "\n".join(text_parts)

    for i in range(0, len(full_text), 4000):
        bot.send_message(message.chat.id, full_text[i:i + 4000])


@bot.callback_query_handler(func=lambda call: call.data.startswith("answer:"))
def check_answer(call):
    chat_id = call.message.chat.id

    if chat_id not in users or not users[chat_id].get("name"):
        bot.answer_callback_query(call.id, "Сначала нажми /start")
        return

    user = users[chat_id]
    question_number = user["question"]

    if question_number >= len(questions):
        bot.answer_callback_query(call.id, "Тест уже закончен.")
        return

    question = questions[question_number]
    selected_answer = int(call.data.split(":")[1])
    correct_answer = question["correct"]

    bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    is_correct = selected_answer == correct_answer

    user["answers"].append({
        "number": question_number + 1,
        "question": question["question"],
        "selected": question["answers"][selected_answer],
        "correct_answer": question["answers"][correct_answer],
        "correct": is_correct
    })

    if is_correct:
        user["score"] += 1
        bot.answer_callback_query(call.id, "Правильно!")
        bot.send_message(chat_id, "Правильно!")
    else:
        bot.answer_callback_query(call.id, "Неправильно!")
        bot.send_message(
            chat_id,
            f"Неправильно!\nПравильный ответ: {question['answers'][correct_answer]}"
        )

    user["question"] += 1

    if user["question"] < len(questions):
        send_question(chat_id)
    else:
        score = user["score"]
        total = len(questions)
        name = user["name"]
        answers = user["answers"]

        save_result(name, chat_id, score, answers)

        bot.send_message(
            chat_id,
            f"Тест закончен!\n\n"
            f"Ты ответил правильно на {score} из {total}.\n\n"
            f"Твой результат сохранён. Нажми «Результаты», чтобы посмотреть сохранённые данные.",
            reply_markup=main_keyboard()
        )

        del users[chat_id]


print("Бот запущен...")
bot.infinity_polling()
