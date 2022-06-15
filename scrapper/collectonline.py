from users import users
import time
import requests
from sys import path
import telegram
# токен приложения ВК и бота в ТГ
from personal import VK_TOKEN, TELEGRAM_TOKEN

path.append('../')

bot = telegram.Bot(TELEGRAM_TOKEN)
failed = False
malo = False


def getonline():
    '''
    Function gets a list of zeros and ones for each user offline/online
    '''
    real_users = ','.join([str(m) for m in users.values()])
    url = 'https://api.vk.com/method/users.get?v=5.131'
    for _ in range(3):
        global malo
        global failed
        try:
            req = requests.get(
                url, params={'access_token': VK_TOKEN, 'user_ids': real_users, 'fields': 'last_seen,online'}, timeout=2)
            data = req.json()
            info = []
            # info = [1, 3, 0, 7, ...]
            # 1 — мобильная версия;
            # 2 — приложение для iPhone;
            # 3 — приложение для iPad;
            # 4 — приложение для Android;
            # 5 — приложение для Windows Phone;
            # 6 — приложение для Windows 10;
            # 7 — полная версия сайта;
            # 8 — невозможно определить.
            for user in data['response']:
                if user['online'] == 0:
                    status = '0'
                else:
                    if 'last_seen' in user.keys():
                        status = str(user['last_seen']['platform'])
                    else:
                        status = '8'
                info.append(status)
            if len(info) < 10:
                raise KeyError('В ответе сервера меньше 10 значений')
            # if sum(1 for m in info if int(m)) < 5 and not malo:
            #     bot.send_message(chat_id=133580838,
            #                      text=f'ℹ It\'s less than 5 gyus online (currently: {sum(1 for m in info if int(m))}).\n\nCurrent time: {time.strftime("%H:%M:%S, %d.%m.%Y")}')
            #     malo = True
            info = ', '.join(info)
            return info
        except Exception as exception:
            with open('errors.txt', 'a', encoding='utf-8') as error_file:
                error_file.write(time.strftime('%H:%M:%S, %d.%m.%Y'))
                error_file.write('\n')
                error_file.write('Data: ')
                error_file.write(str(data))
                error_file.write('\n')
                error_file.write('Exception: ')
                error_file.write(str(exception))
                error_file.write('\n\n')
            if not failed:
                if len(str(data)) > 1000:
                    bot.send_message(chat_id=133580838,
                                     text=f'''⚠ Script failed. Catched data and exception:\n\n`data = {str(data)[:500]}\n...\n{str(data)[-500:]}`\n\n`exception = {exception}`\n\nCurrent time: {time.strftime("%H:%M:%S, %d.%m.%Y")}''',
                                     parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    bot.send_message(chat_id=133580838,
                                     text=f'''⚠ Script failed. Catched data and exception:\n\n`data = {data}`\n\n`exception = {exception}`\n\nCurrent time: {time.strftime("%H:%M:%S, %d.%m.%Y")}''',
                                     parse_mode=telegram.ParseMode.MARKDOWN)
                failed = True
            time.sleep(0.4)
    return None


print(time.strftime('%H:%M:%S, %d.%m.%Y'), end='')
with open('log.txt', 'a', encoding='utf-8') as file:
    file.write(time.strftime('%H:%M:%S, %d.%m.%Y'))
bools = getonline()
if bools:
    date = time.strftime('%d-%m-%Y')
    # папка данных была удалена для уменьшения размера репозитория. её копия есть в репозитории в другой директории
    with open(f'data/{date}.csv', 'a', encoding='utf-8') as file:
        file.write(str(round(time.time())))
        file.write(', ')
        file.write(bools)
        file.write('\n')
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write(' | Done writing students.\n')
    print(' | Done writing students.', end='')
    if failed:
        bot.send_message(chat_id=133580838,
                         text=f'✅ Script failed, but collected data on another try!\n\nCurrent time: {time.strftime("%H:%M:%S, %d.%m.%Y")}')
else:
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write(' | Error.\n')
    print(' | Error.', end='')
    if failed:
        bot.send_message(chat_id=133580838,
                         text=f'❌ Script failed and did not recovered. Data for this period is lost.\n\nCurrent time: {time.strftime("%H:%M:%S, %d.%m.%Y")}')
