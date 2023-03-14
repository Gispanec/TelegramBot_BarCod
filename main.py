# Телеграм бот который расшифрвывает по фото ШК в формате EAN13

import settings
import datetime

import telebot
from pyzbar.pyzbar import decode
from PIL import Image


bot = telebot.TeleBot(settings.bot_key)


@bot.message_handler(content_types=['audio', 'voice', 'video', 'document',
                'text', 'location', 'contact', 'sticker'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Это не фото, отправьте фото ШК в формате EAN13 для его расшифровки")


@bot.message_handler(content_types=['photo'])
def get_photo_messages(message):
    user_id = str(message.from_user.id)
    message_barcode = message.photo[-1].file_id
    file_info = bot.get_file(message_barcode)
    downloaded_file = bot.download_file(file_info.file_path)
    data = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    with open('./img/' + user_id + '_' + data + '.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
    try:
        image_barcode = Image.open('./img/' + user_id + '_' + data + '.jpg')
        decode_bar = decode(image_barcode)
        image_barcode.close()
        bar_code = decode_bar[0].data.decode("utf-8")
        bot.send_message(message.from_user.id, bar_code)
    except:
        bot.send_message(message.from_user.id, "Не удалось распознать ШК, отправьте фото ШК  в формате EAN13")
bot.polling(none_stop=True, interval=0)