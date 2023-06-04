import telebot
import time
from telebot import types

bot = telebot.TeleBot('6190440272:AAFpX1fZTeeR2RI_3meYc3qsXfmUiH92YkU')

count = 0
stats = []
summa = 0

def price(self):
    self = self.split()
    v = self[1]
    if self[0].lower() == 'эспрессо':
        return 130
    if self[0].lower() == 'ристретто':
        return 100
    if self[0].lower() == 'американо':
        match v:
            case '0,2':
                return 160
            case '0,3':
                return 250
            case '0,4':
                return 300
    if self[0].lower() == 'капучино':
        match v:
            case '0,2':
                return 210
            case '0,3':
                return 250
            case '0,4':
                return 300
    if self[0].lower() == 'латте':
        match v:
            case '0,2':
                return 210
            case '0,3':
                return 250
            case '0,4':
                return 300
    if self[0].lower() == 'флет-уайт':
        return 250
    if self[0].lower() == 'раф':
        return 350
    if self[0].lower().strip() == 'картошка':
        return 160
    if self[0].lower() == 'выпечка':
        return 150
    if self[0].lower() == 'салат' or self[0].lower() == 'кола' or self[0].lower() == 'вода' or self[0].lower() == 'бутер':
        return 200

def dop(self):
    if '+' in self:
        self_v = self.split()
        self = self.split('+')
        sum_dop = 0
        for i in range(len(self)):
            if self[i].strip() == 'сироп':
                if self_v[1] == '0,2':
                    sum_dop += 20
                    continue
                elif self_v[1] == '0,3':
                    sum_dop += 30
                    continue
                elif self_v[1] == '0,4':
                    sum_dop += 40
                    continue
        for i in range(len(self)):
            if self[i].strip() == 'молоко':
                if self_v[1] == '0,2':
                    sum_dop += 90
                    continue
                elif self_v[1] == '0,3':
                    sum_dop += 120
                    continue
                elif self_v[1] == '0,4':
                    sum_dop += 140
                    continue
        return sum_dop
    else:
        return 0

def skidon(self):
    if 'учитель' in self:
        return (price(self) * 0.25)
    if 'ученик' in self:
        return (price(self) * 0.10)
    return 0

@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardMarkup()
    print(message.chat.id)
    bt1 = types.KeyboardButton('/addstats')
    bt2 = types.KeyboardButton('/seestats')
    markup.add(bt1, bt2)
    bot.send_message(message.chat.id, 'привет я бот, который поможет тебе сделать стастику', reply_markup=markup)
    # bot.send_message(message.chat.id, 'ввведите команду /help для получения информации о доступных коммандах!')

@bot.message_handler(commands=['addstats'])
def addstats(message):
    bot.send_message(message.chat.id, 'введите, что у вас купили сейчас')
    bot.register_next_step_handler(message, addstats2)
def addstats2(message):
    global count, stats
    txt = message.text
    count += 1
    if txt == 'стоп':
        return 0
    stat = f'{count}. {txt} {price(txt) + dop(txt)}'
    stats.append(stat)
    print(stats)
    bot.send_message(242670281, f'{count}. {txt} {price(txt) + dop(txt) - skidon(txt)}')
    bot.send_message(message.chat.id, f'{count}. {txt} {price(txt) + dop(txt) - skidon(txt)}')
    bot.send_message(message.chat.id, 'данные записаны')

@bot.message_handler(commands=['seestats'])
def seestat(message):
    global summa
    for i in stats:
        bot.send_message(message.chat.id, i)
        bot.send_message(242670281, i)
    for i in stats:
        s = i.split()
        summa += int(s[-1])
    bot.send_message(message.chat.id, f'сумма всего: {summa}')
    bot.send_message(242670281, f'сумма всего: {summa}')

@bot.message_handler(commands=['del'])
def deletestat(message):
    global stats, count
    stats = ''
    count = 0
    bot.send_message(message.chat.id, 'данные удалены')

while True:
    try:
        bot.polling()
    except:
        time.sleep(15)
