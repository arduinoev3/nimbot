import telebot
from telebot import types
from collections import deque
token="1122823442:AAE2gFGVMxybOYWj-6ljGjFTwZji4Po87SI"


bot=telebot.TeleBot(token)


N = 2
queue = deque()
games = []

def search(id):
    global games

    for i in range(0, len(games)):
        if games[i][0].index(id) != -1:
            return i, games[i][0].index(id)
    
    return None, None



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! ищу игроков")
    global queue, N, games

    if message.chat.id not in queue:
        queue.append(message.chat.id)

    if len(queue) >= N:
        players = [queue.popleft() for _ in range(N)]

        bot.send_message(players[0], "Игроки нашлись!!! Теперь напиши свой выбор - сейчас на столе 13 камешков. Делай свой выбор и напиши нам число от 1 до 4. Задача - забрать последний камень")
        bot.send_message(players[1], "Игроки нашлись!!! Ты ходишь вторым - жди")
        
        games.append([players, 0, 13])



@bot.message_handler()
def start_message(message):
    global players, games, N

    id = message.chat.id
    g, i = search(id)


    if g == None:
        bot.send_message(id, "Тебя нет в игре - введи /start")
        return
    
    if message.text not in {"1", "2", "3", "4"}:
        bot.send_message(id, "Неа")
        return

    if games[g][2] > 0:
        how = int(message.text)

        if i != games[g][1] % 2:
            bot.send_message(id, "Сейчас не твой ход")
        else:
            games[g][2] -= how
            games[g][1] += 1

            if games[g][2] <= 0:
                bot.send_message(id, "Ты выиграл")
                bot.send_message(games[g][0][games[g][1] % 2], f"Ты проиграл")
            else:
                bot.send_message(id, "Ход завершен. Ждем соперника")
                bot.send_message(games[g][0][games[g][1] % 2], f"Ходи, на столе {games[g][2]} камней")
    


bot.infinity_polling()