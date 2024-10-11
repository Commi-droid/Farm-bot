"بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"

import telebot
from telebot import types

bot = telebot.TeleBot('7392273151:AAGRCtyHVqJlOmiYtfJB-83_TJIcZtPu-YY')

user_states = {}

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_btn = types.KeyboardButton("Начать тестирование")
    markup.add(main_btn)
    bot.send_message(message.chat.id, 'Привет!\nЭто бот (бета-версия) проекта <b>«Алло, это фарма?»</b>. С помощью бота можно узнать, какие профессии в фарме подойдут тебе больше всего. Ответь на 4 вопроса, и мы пришлем тебе подборку материалов, которые помогут тебе с выбором направления для карьеры :) ', reply_markup=markup, parse_mode='html')

    markup = types.InlineKeyboardMarkup()
    pre_btn1 = types.InlineKeyboardButton(text='Наша группа в Telegram', url='https://t.me/pharmfm')
    markup.add(pre_btn1)
    bot.send_message(message.from_user.id, "Обязательно подпишись на основной канал, если ещё не сделал этого!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    user_id = message.chat.id

    if message.text == "Начать тестирование":
        user_states[user_id] = {'question_index': 0, 'answers': []}
        ask_question(user_id)

    elif user_id in user_states:
        handle_answer(user_id, message.text)

    elif message.text == "Вернуться в главное меню":
        user_states.pop(user_id, None) 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("Начать тестирование")
        markup.add(btn)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

def ask_question(user_id):
    questions = [
        "Любишь ли ты копаться и разбираться в документах?",
        "Хотел бы ты на работе часто общаться с людьми?",
        "Готов ли ты к большому уровню неопределенности, когда ситуация с задачами на работе может меняться еженедельно/ежемесячно?",
        "У тебя технический склад ума?"
    ]

    if user_states[user_id]['question_index'] < len(questions):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(user_id, text=questions[user_states[user_id]['question_index']], reply_markup=markup)
    else:
        finish_testing(user_id)

def handle_answer(user_id, answer):
    if answer in ["Да", "Нет"]:
        user_states[user_id]['answers'].append(answer)
        user_states[user_id]['question_index'] += 1 
        ask_question(user_id)
    else:
        bot.send_message(user_id, text="Пожалуйста, ответьте 'Да' или 'Нет'.")

def finish_testing(user_id):
    answers = user_states[user_id]['answers']
    
    professions = []
    
    if answers[0] == "Да" and answers[1] == "Нет" and answers[1] == "Нет" and answers[1] == "Нет":
        professions.append("Медицинский писатель или переводчик медицинских и фармацевтических текстов")
    if answers[1] == "Да" and answers[1] == "Да" and answers[1] == "Да" and answers[1] == "Нет":
        professions.append("Монитор клинического исследования")
    if answers[1] == "Да" and answers[1] == "Нет" and answers[1] == "Да" and answers[1] == "Нет":
        professions.append("Специалист по фармаконадзору")
    if answers[1] == "Да" and answers[1] == "Нет" and answers[1] == "Да" and answers[1] == "Да":
        professions.append("Дата менеджер или биостатистик")
    if answers[1] == "Да" and answers[1] == "Нет" and answers[1] == "Нет" and answers[1] == "Да":
        professions.append("Специалист на производстве")
    if answers[1] == "Да" and answers[1] == "Нет" and answers[1] == "Нет" and answers[1] == "Нет":
        professions.append("Специалист по обеспечению качества")
    if not professions:
        professions.append("Проведите больше времени на изучение различных профессий в фармацевтике.")

    result_message = "Тестирование завершено! Спасибо за участие.\n\nПодходящие профессии для вас:\n" + "\n".join(professions)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_btn = types.KeyboardButton("Вернуться в главное меню")
    markup.add(back_btn)

    bot.send_message(user_id, result_message, reply_markup=markup)
    
    user_states.pop(user_id, None) 

if __name__ == '__main__':
    bot.polling(none_stop=True)




    