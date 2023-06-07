from telegram.ext import CallbackContext

def send_request_to_admin(context: CallbackContext, user_id: int) -> None:
    request_info = f"Новая заявка от пользователя с ID {user_id}: \nТелефон: {context.user_data['phone']} \nИмя:{context.user_data['name']}\nВылет из:{context.user_data['departure_city']} \nНаправление:{context.user_data['destination']} \n \nДата вылета(ДД-ММ-ГГГГ): {context.user_data['start_date']}\nКоличество ночей: {context.user_data['nights']}\nКоличество взрослых: {context.user_data['adults']}   \nКоличество детей: {context.user_data.get('children_num', '0')} \nДопы: {context.user_data['ask_addition_info']} "
    context.bot.send_message(chat_id=298161005, text=request_info)  
        
