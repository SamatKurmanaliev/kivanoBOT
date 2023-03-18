import requests
from bs4 import BeautifulSoup
import telebot

bot_token = '6088707505:AAEfW2nThYyfgaZLaJup1BTXgy5La2gEIks'
bot = telebot.TeleBot(bot_token)

def get_products():
    url = "https://www.kivano.kg/mobilnye-telefony"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    for product in soup.find_all('div', {'class': 'product_listbox'}):
        name = product.find('div', {"class":"listbox_title"}).text.strip()
        price = product.find('div', {'class': 'listbox_price'}).find("strong").text.strip()
        product_link = url + product.find('div', {'class': 'listbox_img'}).find("a")["href"]
        products.append({'name': name, 'price': price, 'product_link': product_link})

    return products

@bot.message_handler(commands=['products'])
def handle_products_command(message):
    products = get_products()
    product_text = ''
    for product in products:
        product_text += f'{product["name"]} - {product["price"]} - {product["product_link"]}\n'
    bot.send_message(message.chat.id, f'Характеристики телефона:\n\n{product_text}')
@bot.message_handler(commands=['start'])
def hello(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    button1 = telebot.types.KeyboardButton('Kivano.kg телефоны ')
    button2 = telebot.types.KeyboardButton('Kivano.kg компьютеры')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id,'Приветстую тебя! Выбери категорию товаров!', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ['Kivano.kg телефоны', 'Kivano.kg компьютеры'])
def handle_kivano_command(message):
    if message.text == 'Kivano.kg телефоны':
        products = get_products()
        product_text = ''
        for product in products:
            product_text += f'{product["name"]} - {product["price"]} - {product["product_link"]}\n'

        bot.send_message(message.chat.id, f'Каталог телефонов:\n\n{product_text}')
    else:
        bot.send_message(message.chat.id, 'На данный момент у нас нет таких товаров! Приносим свои извинения!')




bot.polling()
