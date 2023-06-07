# travel_agent_bot - Chatbot для тегерам

##
Основной модуль проекта vicbot.py для тегерам представляет собой Telegram-бот, который предоставляет различные функции для пользователей. Бот может выполнять следующие команды:

- `/start` - начало работы с ботом и вывод основного меню.
- `/tour_application` - запускает процесс заявки на подбор тура.
- `/tour_info` - предоставляет информацию о текущем туре.
- `/memo` - выводит памятку с полезной информацией.
- `/victorina` - запускает викторину.
- `/cancel` - отменяет текущую операцию и возвращает пользователя в основное меню.

### Взаимодействие с ботом

После запуска бота и его подключения к Telegram, вы можете начать взаимодействовать с ним, отправляя ему сообщения или команды. Он будет отвечать на команды `/start`, `/tour_application`, `/tour_info`, `/memo`, `/victorina`, а также на другие текстовые сообщения, предоставляя автоматические ответы.

### Дополнительные модули

- `tour_info.py` - модуль, отвечающий за информацию о туре.
- `tour_application.py` - модуль, реализующий заявку на подбор тура.
- `victorina.py` - модуль, реализующий викторину.
- `country_info.py` - модуль, предоставляющий информацию о стране.
- `message_handlers.py` - модуль, содержащий обработчики текстовых сообщений.

## tour_application.py

Модуль `tour_application.py` отвечает за функционал заявки на подбор тура.

### Зависимости

- `logging`
- `telegram`
- `telegram.ext`
- `emoji`
- `vicbot_calendar`
- `datetime`
- `admin_utils`

### Переменные состояния

Модуль использует переменные состояния для управления процессом заявки на подбор тура:

- `NAME` - имя пользователя
- `PHONE` - номер телефона пользователя
- `PHONE_WAITING` - ожидание номера телефона
- `DEPARTURE` - выбор города отправления
- `DESTINATION` - выбор места назначения
- `DATES` - выбор даты вылета
- `DATES_SELECTED` - выбор конкретной даты вылета
- `NIGHTS` - выбор количества ночей
- `ADULTS` - выбор количества взрослых
- `CHILDREN` - выбор наличия детей
- `CHILDREN_NUM` - выбор количества детей
- `ADDITION_INFO` - получение дополнительной информации

### Основные функции

- `ask_for_name(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя его имя.
- `ask_for_phone(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя его номер телефона.
- `phone(update: Update, context: CallbackContext) -> int` - сохраняет номер телефона пользователя.
- `departure(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя город отправления.
- `destination(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя место назначения.
- `dates(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя дату вылета.
- `dates_selected(update: Update, context: CallbackContext) -> int` - сохраняет выбранную дату вылета.
- `nights(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя количество ночей.
- `adults(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя количество взрослых.
- `children(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя наличие детей.
- `children_num(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя количество детей.
- `ask_addition_info(update: Update, context: CallbackContext) -> int` - запрашивает у пользователя дополнительную информацию.
- `cancel(update: Update, context: CallbackContext) -> int` - отменяет текущую заявку.

### ConversationHandler

Модуль экспортирует функцию `get_tour_application_conversation_handler()`, которая возвращает `ConversationHandler`, управляющий процессом заявки на подбор тура.

```python
def get_tour_application_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('tour_application', ask_for_name)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, ask_for_phone)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, ask_for_phone)],
            PHONE_WAITING: [MessageHandler(Filters.contact | Filters.text & ~Filters.command, phone)],
            DEPARTURE: [CallbackQueryHandler(departure)],
            DESTINATION: [CallbackQueryHandler(destination)],
            DATES: [CallbackQueryHandler(dates)],
            DATES_SELECTED: [CallbackQueryHandler(dates_selected, pattern='^calendar,'),
                            CallbackQueryHandler(inline_handler, pattern='^(previous-month|next-month)')],
            NIGHTS: [MessageHandler(Filters.text, nights)],
            ADULTS: [CallbackQueryHandler(adults)],
            CHILDREN: [CallbackQueryHandler(children)],
            CHILDREN_NUM: [CallbackQueryHandler(children_num)],
            ADDITION_INFO: [MessageHandler(Filters.text & ~Filters.command, ask_addition_info)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
```

## tour_info.py

Модуль `tour_info.py` отвечает за функционал получения информации о туре.

### Зависимости

- `pandas`
- `numpy`
- `telegram`
- `telegram.ext`

### Основные функции

- `start_tour_info(update: Update, context: CallbackContext) -> int` - начинает процесс получения информации о туре.
- `handle_tour_id(update: Update, context: CallbackContext) -> int` - обрабатывает введенный номер телефона и выводит информацию о туре.
- `cancel(update: Update, context: CallbackContext) -> int` - отменяет текущий процесс и возвращает пользователя в главное меню.

### ConversationHandler

Модуль экспортирует функцию `get_tour_info_conversation_handler()`, которая возвращает `ConversationHandler`, управляющий процессом получения информации о туре.

```python
def get_tour_info_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('tour_info', start_tour_info)],
        states={
            TOUR_ID: [MessageHandler(Filters.text & ~Filters.command, handle_tour_id)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
 ```

## victorina.py

Модуль `victorina.py` отвечает за функционал викторины.

### Зависимости

- `os`
- `json`
- `random`
- `telegram`
- `telegram.ext`

### Основные функции

- `start_victorina(update: Update, context: CallbackContext) -> int` - начинает викторину и предлагает выбрать тему.
- `topic_choice(update: Update, context: CallbackContext) -> int` - обрабатывает выбор темы и загружает вопросы из соответствующего JSON-файла.
- `ask_question(update: Update, context: CallbackContext) -> int` - задает вопрос из списка и предлагает варианты ответов.
- `answer_question(update: Update, context: CallbackContext) -> int` - обрабатывает ответ пользователя на вопрос и выводит результат.
- `next_question(update: Update, context: CallbackContext) -> int` - переходит к следующему вопросу или завершает викторину.
- `end_quiz(update: Update, context: CallbackContext) -> int` - завершает викторину.

### ConversationHandler

Модуль экспортирует функцию `victorina_conv_handler()`, которая возвращает `ConversationHandler`, управляющий процессом викторины.

```python
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



		

