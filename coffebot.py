import sqlite3
import pip
import telebot
import time
from telebot import types
import datetime
# pip.main(['install', 'pytelegrambotapi'])
# from background import keep_alive
from datetime import datetime

bot = telebot.TeleBot('6190440272:AAFpX1fZTeeR2RI_3meYc3qsXfmUiH92YkU')

count = 0
stats = []
summa = 0.0
id_admin = 0
all_admin = [242670281, 978762336, 976010760, 795001718, 1421699721, 802923483]
name_barista = ''

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, number TEXT PRIMARY KEY, coming INT, summa INT, rank TEXT);''')
conn.commit()
conn.close()

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
    if self[0].lower() == 'матча':
        match v:
            case '0,2':
                return 250
            case '0,3':
                return 280
            case '0,4':
                return 300
    if self[0].lower() == 'бамбл':
        return 250
    if self[0].lower() == 'айс-латте':
        return 250
    if self[0].lower().strip() == 'картошка':
        return 190
    if self[0].lower().strip() == 'бизе':
        return 250
    if self[0].lower() == 'выпечка':
        return 150
    if self[0].lower() == 'салат' or self[0].lower().strip() == 'водамаленькая' or self[0].lower() == 'кола' or self[
        0].lower() == 'бутер':
        return 200
    if self[0].lower().strip() == 'водабольшая':
        return 250
    if self[0].lower() == 'чай':
        match v:
            case '0,3':
                return 180
            case '0,4':
                return 240
    if self[0].lower().strip() == 'какао':
        match v:
            case '0,2':
                return 220
            case '0,3':
                return 250
            case '0,4':
                return 280
    return 0


def loyal(txt, sumc):
    txt = txt.split(':')[1].split()
    print(txt)
    #name, number
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT number FROM users WHERE number = {txt[0]}')
    data_u = cursor.fetchone()
    if data_u is None:
        print(0, 'new')
        cursor.execute(f"INSERT INTO users (name, number, coming, summa, rank) VALUES ('{txt[1]}', '{txt[0]}', '{1}', '{sumc}', 'посетитель');")
        print(1)
        conn.commit()
        conn.close()
    else:
        com = cursor.execute(f'SELECT comming FORM users WHERE number = "{txt[0]}"')[0]
        cursor.execute(f'UPDATE users SET comming = "{com + 1}" WHERE number = "{txt[0]}"')
        sum_cush = cursor.execute(f'SELECT summa FROM users WHERE number = "{txt[0]}"')[0]
        cursor.execute(f'UPDATE users SET summa = "{sum_cush + sumc}" WHERE number = "{txt[0]}"')
        print(1)
        conn.commit()
        conn.close()

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
                elif self_v[0].lower().strip() == 'флет-уайт':
                    sum_dop += 20
                    continue
                elif self_v[0].lower().strip() == 'айс-латте':
                    sum_dop += 20
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
                elif self_v[0].lower().strip() == 'флет-уайт':
                    sum_dop += 90
                    continue
                elif self_v[0].lower().strip() == 'айс-латте':
                    sum_dop += 120
                    continue
                elif self_v[0].lower().strip() == 'раф':
                    sum_dop += 120
                    continue
        return sum_dop
    return 0


def skidon(self):
    a = self.split()
    if 'учитель' in self:
        return (price(self) * 0.25)
    if 'ученик' in self:
        return (price(self) * 0.10)
    if 'админ' in self:
        return (price(self) - 100)
    for i in range(len(a)):
        if a[i].lower() == 'скидка':
            chislo = float(a[i + 1])
            return (price(self) * (chislo/100))
    return 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'привет я бот кофейни "Кофе для души". Хотите заказать кофе?')
    bot.send_message(message.chat.id, 'если вы хотите заказать кофе, напишите в чат "сделать заказ"')
    print(message.chat.id)


@bot.message_handler(commands=['adminstart'])
def adstart(message):
    if message.chat.id in all_admin:
        markup = types.ReplyKeyboardMarkup()
        print(message.chat.id)
        bt1 = types.KeyboardButton('/addstats')
        bt2 = types.KeyboardButton('/seestats')
        markup.add(bt1, bt2)
        bot.send_message(message.chat.id, "вы вошли в систему администрации для контроля статистики.", reply_markup=markup)
        bot.send_message(message.chat.id, 'введите имя баристы')
        bot.register_next_step_handler(message, adstart2)


def adstart2(message):
    global id_admin, name_barista
    if message.text.lower().strip() == 'петя':
        name_barista = 'петя'
        bot.send_message(message.chat.id, 'Здравствуйте Пётр!')
        id_admin = 978762336
    # if message.text.lower().strip() == 'вика':
    #     name_barista = 'вика'
    #     bot.send_message(message.chat.id, 'Здравствуйте Виктория!')
    #     bot.send_message(message.chat.id, 'чтобы увидеть какие есть команды и их назначение введите /ahelp')
    #     id_admin = 976010760
    if message.text.lower().strip() == 'федя':
        name_barista = 'федя'
        bot.send_message(message.chat.id, 'Здравсвуй Федя Скин')
        bot.send_message(message.chat.id, 'чтобы ты не тупил, можешь увидеть команды и их примерное значение /ahelp')
        id_admin = 795001718
    if message.text.lower().strip() == 'кристина':
        name_barista = 'кристина'
        bot.send_message(message.chat.id, 'Привет Кристина!')
        bot.send_message(message.chat.id, 'Чтобы ты не затупила для тебя есть комманда /ahelp, которая более менее поможет тебе с ботом! Хорошей работы.')
        id_admin = 1421699721
    if message.text.lower().strip() == 'захар':
        name_barista = 'захар'
        bot.send_message(message.chat.id, 'Здравствуйте Захар.')
        bot.send_message(message.chat.id, 'Если ты запутался как записывать код и какие есть комманды в общем, то для тебя есть хорошая комманда /ahelp. Хорошей смены!')
        id_admin = 802923483
# bot.send_message(message.chat.id, datetime.now('%H:%M'))
# bot.send_message(message.chat.id, 'ввведите команду /help для получения информации о доступных коммандах!')


@bot.message_handler(commands=['ahelp'])
def takehelp(message):
    if message.chat.id in all_admin:
        bot.send_message(message.chat.id,
                         'привет я бот для кофейни. и я помогу записать покупки за сегодня и в конце дня показать их тебе и их сумму')
        bot.send_message(message.chat.id,
                         'после старта ты видишь кнопки /addstats(после ее нажатия ты добавляешь то, что у тебя купили) и кнопку /seestats(после ее нажатия у тебя появится вся статистика за последнее время). Так же в боте есть еще функции.')
        bot.send_message(message.chat.id,
                         'Первая функция /del(удаляет всю статистику за сегодня) и вторая ВАЖНАЯ "итог"(в любом регистре) он отправляет тебе и твоему начальнику отчет за рабочий день! Так же /addlist, если бот слетел и весь твой список тоже '
                         'ты можешь ввести в одном сообщении весь список без цен, но с номерами через знак, который тебе скажут после вписывания команды. На этом все')


@bot.message_handler(commands=['addstats'])
def addstats(message):
    if message.chat.id in all_admin:
        bot.send_message(message.chat.id, 'введите, что у вас купили сейчас ( спроси про номер )')
        bot.register_next_step_handler(message, addstats2)


def addstats2(message):
    global count, stats
    txt = message.text
    count += 1
    if txt == 'стоп':
        return 0
    cush = price(txt) + dop(txt) - skidon(txt)
    if ':' in txt:
        loyal(txt, cush)
    stat = f'{count}. {txt} {round(cush)}'
    stats.append(stat)
    print(stats)
    #bot.send_message(242670281, f'{count}. {txt} {price(txt) + dop(txt) - skidon(txt)}')
    bot.send_message(message.chat.id, f'{count}. {txt} {round(cush)}')
    bot.send_message(message.chat.id, 'данные записаны')


@bot.message_handler(commands=['seestats'])
def seestat(message):
    summa = 0
    if message.chat.id in all_admin:
        for i in stats:
            s = i.split()
            summa += int(s[-1])
        for i in stats:
          bot.send_message(message.chat.id, i)
        bot.send_message(message.chat.id, f'сумма всего: {summa}')


@bot.message_handler(commands=['del'])
def deletestat(message):
    if message.chat.id == id_admin:
        global stats, count
        chat_id = message.chat.id
        b = 0
        for i in range(1000):
            try:
                bot.delete_message(chat_id, message.message_id - i)
            except:
                b = i
                break
        stats = []
        count = 0
        bot.send_message(message.chat.id, 'данные удалены')


@bot.message_handler(commands=['addlist'])
def addlist(message):
    bot.send_message(message.chat.id, 'введи список полностью. между напитками поставь данный знак -- ";"')
    bot.register_next_step_handler(message, addlist2)
def addlist2(message):
    global stats, count
    stats = message.text.split(';')
    bot.send_message(message.chat.id, 'данные введены')
    for i in stats:
        bot.send_message(message.chat.id, i)
        count += 1


@bot.message_handler(content_types=['text'])
def txt(message):
    if message.text.lower().strip() == 'итог':
        if message.chat.id == id_admin:
            summa = 0
            for i in stats:
                s = i.split()
                summa += int(s[-1])
            for i in stats:
                bot.send_message(message.chat.id, i)
                bot.send_message(242670281, i)
            bot.send_message(message.chat.id, f'сумма всего: {summa}')
            bot.send_message(242670281, f'сумма всего: {summa}')
            bot.send_message(message.chat.id, f'сегодня работал я! {name_barista}')
            bot.send_message(242670281, f'работал сегодня: {name_barista}')
            if datetime.weekday() == 0:
                bot.send_message(message.chat.id, 'отлично поработал, время payday')
                bot.send_message(242670281, 'отлично поработали, время payday!')
    if message.text.lower().strip() == 'сделать заказ':
        bot.send_message(message.chat.id, 'напишите четко как скажу вам я: "название кофе" "Обьем" "учитель вы или ученик, если никто, ничего не пишите" "нал или безнал" если вам нужны добавки или альт. молоко то пишите через "+" "молоко или сироп" если и то и то, два +')
        bot.send_message(message.chat.id, 'пример: капучино 0,4 ученик безнал + молоко + сироп')
        bot.send_message(message.chat.id, 'так же, если вы учавствуете в программе лояльности, вы через знак ":" можете написать свой номер или зарегестрироваться прямо на месте. Have a good day!!')
        bot.register_next_step_handler(message, buycoffee)
    if message.text.lower().strip() == 'покажи мою статистику':
        bot.send_message(message.chat.id, 'введите свой номер телефона')
        bot.register_next_step_handler(message, inf)


def inf(message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    bdd = cursor.execute(f'SELECT * FROM users WHERE number = "{message.text}"').fetchone()
    bot.send_message(message.chat.id, f'Номер телефона:{bdd[1]}\nПоходов:{bdd[2]}\nВсего потрачено:{bdd[3]}\nРанг:{bdd[4]}')


def buycoffee(message):
    bot.send_message(id_admin, message.text)
    bot.send_message(message.chat.id, 'ваш заказ принят баристой')
    bot.send_message(message.chat.id, "вы так же можете оплатить переводом сразу, просто когда придете получать заказ, покажите чек о переводе ( 89160221501 : Алена Геннадьевна)")


@bot.message_handler(commands=['givestat'])
def givestat1(message):
    if message.chat.id == id_admin:
        bot.send_message(message.chat.id, 'введите номер телефона')
        bot.register_next_step_handler(message, givestat2)
def givestat2(message):
    lst = cursor.execute(f'SELECT * FROM users WHERE number = "{message.text}"').fetchone()
    if lst is None:
        bot.send_message(message.chat.id, 'Такого номера нет, но можно совершить покупку и сказать номер для регистрации')
    else:
        bot.send_message(message.chat.id, f'Номер телефона:{lst[1]}\nПоходов:{lst[2]}\nВсего потрачено:{lst[3]}\nРанг:{lst[4]}')

# keep_alive()
while True:
    try:
        bot.polling()
    except:
        time.sleep(15)
