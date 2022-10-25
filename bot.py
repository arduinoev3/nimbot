import telebot
from telebot import types
from collections import deque
token="1122823442:AAE2gFGVMxybOYWj-6ljGjFTwZji4Po87SI"


bot=telebot.TeleBot(token)


N = 4
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

        for p in players:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton("Я стартапер")
            item2=types.KeyboardButton("Я работник")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(p, "Игроки нашлись!!! Теперь напиши свой выбор - выбери кнопку",reply_markup=markup)
        
        games.append([players, 0, [-1] * N, [0] * N])



@bot.message_handler()
def start_message(message):
    global players, games, N

    id = message.chat.id
    g, i = search(id)


    if g == None:
        bot.send_message(id, "Тебя нет в игре - введи /start")
        return
    
    if message.text not in {"Я стартапер", "Я работник"}:
        bot.send_message(id, "Неа")
        return
    
    if message.text == "Я стартапер":
        games[g][2][i] = 0
    else:
        games[g][2][i] = 1

    if -1 not in games[g][2]:

        if 0 in games[g][2] and 1 in games[g][2]:
            workers = sum(games[g][2])
            startups = N - workers

            payoff_workers = workers

            if startups == 1:
                payoff_startups = 106
            elif startups == 2:
                payoff_startups = 41
            else:
                payoff_startups = 26
            
            for i in range(0, len(games[g][0])):
                if games[g][2][i]:
                    games[g][3][i] += payoff_workers
                else:
                    games[g][3][i] += payoff_startups


        games[g][2] = [-1] * N
        games[g][1] += 1

        for i in range(0, len(games[g][0])):
            bot.send_message(games[g][0][i], f"Раунд окончен - твой балл {games[g][3][i]}. Продолжаем!")
        
        for game in games:
            for res in game[3]:
                print(" " * (5 - len(str(res))), res, sep="", end="")
            print("|", " " * (7 - len(str(sum(game[3]) / 4))), sum(game[3]) / 4, "|", sep="")


bot.infinity_polling()