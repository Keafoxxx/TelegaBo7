import telebot
from extensions import CurrencyConverter, APIException
from config import TOKEN

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Инструкция по использованию
help_text = """
🤖 *Бот для конвертации валют*

*Как пользоваться:*
Отправьте сообщение в формате:
`<валюта1> <валюта2> <количество>`

*Пример:*
`USD EUR 100` - конвертирует 100 долларов в евро
`EUR RUB 50` - конвертирует 50 евро в рубли

*Доступные команды:*
/start - начать работу
/help - показать справку
/values - показать доступные валюты

*Доступные валюты:*
- USD (доллар США)
- EUR (евро)
- RUB (российский рубль)
"""


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    """Обработчик команд /start и /help"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')


@bot.message_handler(commands=['values'])
def handle_values(message):
    """Обработчик команды /values - показывает доступные валюты"""
    values_text = """
💱 *Доступные валюты:*

*USD* - Доллар США 🇺🇸
*EUR* - Евро 🇪🇺  
*RUB* - Российский рубль 🇷🇺

Используйте формат: `ВАЛЮТА1 ВАЛЮТА2 КОЛИЧЕСТВО`
Пример: `USD EUR 100`
    """
    bot.send_message(message.chat.id, values_text, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def handle_conversion(message):
    """Обработчик текстовых сообщений для конвертации валют"""
    try:
        # Разбиваем сообщение на части
        parts = message.text.split()

        # Проверяем количество аргументов
        if len(parts) != 3:
            raise APIException(
                "Неверный формат запроса.\n\nИспользуйте: <валюта1> <валюта2> <количество>\nПример: USD EUR 100")

        base, quote, amount = parts

        # Выполняем конвертацию
        result = CurrencyConverter.get_price(base, quote, amount)

        # Форматируем результат
        response = f"💱 *Результат конвертации:*\n\n"
        response += f"`{amount} {base.upper()} = {result} {quote.upper()}`"

        bot.send_message(message.chat.id, response, parse_mode='Markdown')

    except APIException as e:
        # Обрабатываем наши пользовательские исключения
        error_message = f"❌ *Ошибка:* {str(e)}"
        bot.send_message(message.chat.id, error_message, parse_mode='Markdown')

    except Exception as e:
        # Обрабатываем непредвиденные ошибки
        error_message = f"❌ *Произошла непредвиденная ошибка:* {str(e)}"
        bot.send_message(message.chat.id, error_message, parse_mode='Markdown')


# Обработчик для всех остальных типов сообщений
@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def handle_other_messages(message):
    """Обработчик неподдерживаемых типов сообщений"""
    bot.reply_to(message, "❌ Я работаю только с текстовыми сообщениями для конвертации валют.")


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
