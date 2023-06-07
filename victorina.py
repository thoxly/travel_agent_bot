import os
import json
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, CallbackQueryHandler


CHOOSE_TOPIC, QUESTION, NEXT_QUESTION = range(3)

def start_victorina(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Турция 🇹🇷", callback_data='turkey'), InlineKeyboardButton("Египет 🇪🇬", callback_data='egypt')], 
        [InlineKeyboardButton("Мальдивы 🇲🇻", callback_data='maldives'), InlineKeyboardButton("ОАЭ 🇦🇪", callback_data='uae')],
        [InlineKeyboardButton("Таиланд 🇹🇭", callback_data='thailand'), InlineKeyboardButton("Куба 🇨🇺", callback_data='cuba')],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите тему викторины:', reply_markup=markup)

    return CHOOSE_TOPIC

def topic_choice(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    context.user_data['topic'] = query.data
    path = f"/root/vicbot/victory_tour/victorina_questions_by_country/{query.data}.json"
    with open(path, 'r') as f:
        context.user_data['questions'] = json.load(f)

    return ask_question(update, context)

def ask_question(update: Update, context: CallbackContext) -> int:
    if not context.user_data['questions']:
        update.callback_query.message.reply_text("⭐ Викторина завершена!\nСпасибо за участие!\n\nМожете сыграть еще раз, выбрав другую страну /victorina 🧠\n\nИли вернуться в главное меню /start")
        return ConversationHandler.END

    question_data = random.choice(context.user_data['questions'])
    context.user_data['questions'].remove(question_data)
    context.user_data['current_question'] = question_data

    keyboard = [[InlineKeyboardButton(option, callback_data=str(i))] for i, option in enumerate(question_data['options'])]
    markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text(question_data['question'], reply_markup=markup)

    return QUESTION

def answer_question(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    selected_option_index = int(query.data)
    correct_answer_index = int(context.user_data['current_question']['correct_answer'])

    explanation = context.user_data['current_question']['explanation']
    response = explanation

    if selected_option_index == correct_answer_index:
        response = '🎉 Правильно!\n' + response
    else:
        response = 'Неправильно 😞\n ' + response


    keyboard = [[InlineKeyboardButton("Далее  ➡", callback_data='next')],
                [InlineKeyboardButton("Завершить ↩", callback_data='finish')]]
    markup = InlineKeyboardMarkup(keyboard)


    query.message.reply_text(response, reply_markup=markup)

    return NEXT_QUESTION

def next_question(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    if query.data == 'next':
        return ask_question(update, context)
    else:
        query.message.reply_text("⭐ Викторина завершена!\nСпасибо за участие!\n\nМожете сыграть еще раз, выбрав другую страну /victorina 🧠\n\nИли вернуться в главное меню /start")
        return ConversationHandler.END

def end_quiz(update: Update, context: CallbackContext) -> int:
    update.callback_query.message.reply_text("⭐ Викторина завершена!\nСпасибо за участие!\n\nМожете сыграть еще раз, выбрав другую страну /victorina 🧠\n\nИли вернуться в главное меню /start")
    return ConversationHandler.END

def victorina_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('victorina', start_victorina)],
        states={
            CHOOSE_TOPIC: [CallbackQueryHandler(topic_choice)],
            QUESTION: [CallbackQueryHandler(answer_question)],
            NEXT_QUESTION: [CallbackQueryHandler(next_question)],
        },
        fallbacks=[CallbackQueryHandler(end_quiz)],
        allow_reentry=True
    )
