import telebot
from telebot import types

from frontend import Bot_inline_btns

tg_api = '6667593230:AAH2ZgrEVgdE4DEt49ksZ-qD1ThJkEXIPag'
bot = telebot.TeleBot(tg_api)


def main():
    @bot.message_handler(commands=['start'])
    def start_msg(message):
        #print(f'{message.from_user.first_name}, {message.from_user.last_name}') #имя фамилия пользователя
        buttons = Bot_inline_btns()
        bot.send_message(message.chat.id, 'Привет!👋\n'
                                          'Благодарим за покупку🖤\n'
                                          'Мы подготовили для вас приятный бонус, '
                                          'чтобы получить его, напишите отзыв😊\n'
                                          'Если у вас возникли какие-то проблемы с заказом '
                                          'свяжитесь с нашим менеджером👨‍💻\n'
                                          'Мы поможем в решении любого вопроса!', reply_markup=buttons.start_btns())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        buttons = Bot_inline_btns()
        if call.data == 'take_gift':
            bot.send_message(call.message.chat.id,
                             'Для получения подарка:\n1.Отправьте фото отзыва!\n2.Нажмите кнопку "Поделиться контактом"',
                             reply_markup=buttons.share_number_btn())
            telebot.TeleBot.create_forum_topic(bot, chat_id=-1002003996301, name=f'{call.message.from_user.first_name} {call.message.from_user.last_name} ОТЗЫВ', icon_color=0x6FB9F0)

        elif call.data == 'write_manager':
            bot.send_message(call.message.chat.id, 'Выберите пожалуйста категорию обращения!',
                             reply_markup=buttons.write_manager_btns())
        elif call.data in ['another_question', 'complectation_product', 'quality_product']:
            if call.message and call.message.chat:
                bot.send_message(call.message.chat.id, 'Пожалуйста, подробно опишите проблему!\n'
                                                       'Так же по возможности приложите фотографии, демонстрирующие '
                                                       'проблему.\n'
                                                       'Мы ответим в течении 24 часов!')
            telebot.TeleBot.create_forum_topic(bot, chat_id=-1002003996301, name=f'{call.message.from_user.first_name} {call.message.from_user.last_name} ПРОБЛЕМА С ТОВАРОМ', icon_color=0x6FB9F0,
                                               icon_custom_emoji_id='T')
            # print(telebot.TeleBot.create_forum_topic(bot, chat_id=-1002003996301, name='topic', icon_color=0x6FB9F0,
            # icon_custom_emoji_id='T')) # в возвращаемом объекте есть id топика

    # контакт пользователя
    @bot.message_handler(content_types=['contact'])
    def text(message):
        if message.contact is not None:
            print(message.contact)

    bot.polling(none_stop=True)


if '__main__' == __name__:
    main()


#40 строка, придумать как импортировать имя фамилию пользователя, чтобы создавались топики с проблемами пользователей
#сделать так, чтобы после использования кнопки "получить подарок" бота нельзя повторно использовать
#после использования проблемы с товаром, бота так же нельзя повторно использовать
#сделать соединение с пользователем и менеджером
#добавить таблицу excel
#добавить функцию: когда пользователь нажмет "получить подарок", бот ждет когда человек отправит фото отзыва и свой контакт, потом бот создает топик и скидывает туда данные пользователя (фото+контакт)
#добавить статусы
#после добавления функции соединения настроить бота для менеджеров (кнопка "проблема решена" для проблем с товаром и кнопка "бонус выплачен" или "бонус отклонен" для получить подарок)