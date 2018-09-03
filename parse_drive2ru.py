import requests
import re
import time
import random
import schedule
import threading
import sqlite3
from multiprocessing import Process
from bs4 import BeautifulSoup

number = 1012561
link_to_models = 'https://www.drive2.ru/cars'
db_path = "C:\\Users\\yoyo\\PycharmProjects\\auto\\drive.db"
header = {
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
'Cache-Control' : 'no-cache',
'Connection' : 'keep-alive',
'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
'cookie': ".AUI=_wfqzlwoyisJAAFiAwx-8lJXa2FwLie3AKhEK_E5Yyoh_IEEd2uj; .UTZ=1535781207 -420; .AUIV=_wfqzlwoyisRAAFiAwx-8lJXawjVwe6vDK91EGzOis7vJaNlQxd2fkmt8EjAvlk; _ym_uid=1527218522327629422; _ga=GA1.2.130567386.1527218522; __gads=ID=4e150417dd42069b:T=1527218525:S=ALNI_Mbb6ifjZZyEGJ0wtICc3lvqZnlB3A; .AMET=bBd22WCTtQM4nx-8qaj4Z9BIw6xToAIii6xdKJPmFQj1ksQJ26UVrYOfRaQi1OM0wICR21FAarpPkTJwUDyJjiPBvZt2Ub8j_oredxgPoeLCdq48GOHeIXZU83HmQeLr; addruid=l15C2s7tA50Bx27nH28EP27g1N; _ym_d=1529683571; tmr_detect=0%7C1535803562728; cmtchd=MTUzNTM0MDgwMjM1Nw==; _gid=GA1.2.338517497.1535340808; .PBIK=AgaRxcBAAANXAQAAAAAGxvrAQAACgQcOWIBAAAExAAAAAAHmigb9XV5_-r-1ytrRu-W7r7j1NQ; _AFF=5; rheftjdd=rheftjddVal; _ym_isad=1",
'host' : 'www.drive2.ru',
'pragma' : 'no-cache',
'Referer' : 'https://www.drive2.ru/',
'TE' : 'Trailers',
'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0",
'x-requested-with': 'XMLHttpRequest'
}

def db_connection():
    connect = sqlite3.connect(db_path)
    return connect


def get_link_list(link_to_models):
    model_list = []
    page = requests.get(link_to_models, headers=header).text
    soup_page = BeautifulSoup(page, "lxml")
    for model in soup_page.find_all('span', class_='c-makes__item is-important js-makes-item'):
        if re.search(r'[а-яА-Я]+', model.find('a', 'c-link').string) == None:
            model_list.append("https://www.drive2.ru/r/" + model.string)
    return model_list


def write_auto_list(number): #генерим список активных тачек.
    models = get_link_list(link_to_models)
    #models = ['Acura']
    links = {}
    id = []
    while number < 1055000:
        for model in models:
            model_html = requests.get(model + '/' + str(number), headers=header)
            soup_model = BeautifulSoup(model_html.text, "lxml")
            try:
                if soup_model.find('span', class_='c-user-card__status').text.find('месяц') != -1 or soup_model.find('span', class_='c-user-card__status').text.find('недел') != -1:
                    print('Старье ' + str(number))
                    number += 1
                    break
            except AttributeError:
                pass
            try:
                chk = soup_model.find(class_='c-lb-card__title').find(class_='c-link').get('href')
            except AttributeError:
                print('Пустой БЖ' +str(number))
                number += 1
                break
            if (model_html.status_code == 200) and (soup_model.find('h1', 'c-car-info__caption').text) is not None and soup_model.find('h1', 'c-car-info__caption').text.find('Бывшая') == -1:
                print(str(model) + str(number) + '/' + str(soup_model.find('h1', 'c-car-info__caption').text))
                id.append(soup_model.find('a', class_="c-link c-link--color00 c-username c-username--wrap").get('data-ihc-id'))
                links.update({str(model) + '/' + str(number):str(soup_model.find('h1', 'c-car-info__caption').text)})
                number += 1
                break
            else:
                if model == 'https://www.drive2.ru/r/Volvo':
                    number += 1
                    break
                else:
                    print('Бывшая ' + str(model) + '/' + str(number))
                    #continue
                    number += 1
                    break
    connect = sqlite3.connect("C:\\Users\\yoyo\\PycharmProjects\\auto\\drive.db")
    with connect:
        cursor = connect.cursor()
        i = 0
        for link in links.items():
            cursor.execute("INSERT INTO bj_list(link, info, user_id) VALUES (?, ?, ?);", (link[0], link[1], id[i]))
            i += 1


def gen_phrase():
    part_1 = ['!', '!', '!']
    part_2 = ['! ', '. ', '!! ']
    part_3 = ['Норм ', 'Крутой ', 'Интересный ', 'Лютый ', 'Веселый ']
    part_4 = ['аппарат ', 'авто ', 'трактор ']
    part_5 = ['когда-то был ', 'когдато катал ', 'когда-то катал ', 'когдато был ']
    part_6 = ['такойже', 'похожий', 'такой-же']
    part_7 = ['. ', '! ', '!! ']
    part_8 = ['Лайк.', 'Прожал кнопки.', 'Лойс']
    complete_text = part_3[random.randint(0, len(part_3) - 1)] + part_4[random.randint(0, len(part_4) - 1)] + \
                    part_5[random.randint(0, len(part_5) - 1)] + part_6[random.randint(0, len(part_6) - 1)] + \
                    part_7[random.randint(0, len(part_7) - 1)] + part_8[random.randint(0, len(part_8) - 1)]
    return complete_text


def get_ownerId_bj(link):
    bj_page = requests.get(link[:37], headers=header).text
    bj_soup = BeautifulSoup(bj_page, 'lxml')
    return int(str(bj_soup.find(class_='c-lb-card__title').find(class_='c-link').get('href')[3:-1]))


def subscribe_like():
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA journal_mode=WAL")
    cursor = connection.cursor()
    get_work_set = """SELECT * from bj_list ORDER BY like_sub ASC LIMIT 300;"""
    cursor.execute(get_work_set)
    rows = cursor.fetchall()
    for row in rows:
        k = row[0]
        like_payload = {
            '_': 'like',
            'type': 'c',
            'id': str(row[0])[30:37],
            '.FCTX': '_wfqzlwoyiseAAQcQnJ1LldlYi4xOjQ3MzM3Njg2NTM0ODc0ODExOaQLV00tWU70CYwutSfmUNNvwboI'
        }
        sub_payload = {
            '_': 'subscribe',
            'type': 'car',
            'id': str(row[0])[30:37],
            '.FCTX': '_wfqzlwoyiseAAQcQnJ1LldlYi4xOjQ3MzM3Njg2NTM0ODc0ODExOaQLV00tWU70CYwutSfmUNNvwboI'
        }
        requests.post('https://www.drive2.ru/ajax/like.cshtml', headers=header, data=like_payload)
        with connection:
            if requests.post('https://www.drive2.ru/ajax/subscription', headers=header, data=sub_payload).status_code == 200:
                try:
                    cursor.execute('''UPDATE bj_list SET like_sub = 1 WHERE link = (?)''', (k,))
                except sqlite3.OperationalError:
                    time.sleep(random.randint(3, 15))
                    cursor.execute('''UPDATE bj_list SET like_sub = 1 WHERE link = (?)''', (k,))
            else:
                print(str(requests.post('https://www.drive2.ru/ajax/subscription', headers=header, data=sub_payload).status_code) + ' ERROR ' + ' Subscribed and liked ' + str(row[0]))
                return False
            connection.commit()
        print("I'm running on thread %s" % threading.current_thread() + ' Subscribed and liked ' + str(row[0]))
        time.sleep(random.randint(200, 500))


def personal_messaging():
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA journal_mode=WAL")
    cursor = connection.cursor()
    get_work_set = """SELECT * from bj_list WHERE like_sub = 1 and bj_comment IS NULL and pm IS NULL and profile_comment IS NULL ORDER BY pm ASC LIMIT 10;"""
    cursor.execute(get_work_set)
    rows = cursor.fetchall()
    for row in rows:
        k = row[0]
        link = get_ownerId_bj(k)
        message_payload = {
            '_': 'post',
            'partner': link,
            'messageId': 636695861674643689,
            'text': gen_phrase(),
            '.FCTX': '_wfqzlwoyiseAAQcQnJ1LldlYi4xOjQ3MzM3Njg2NTM0ODc0ODExOaQLV00tWU70CYwutSfmUNNvwboI'
        }
        with connection:
            if requests.post('https://www.drive2.ru/ajax/messages.cshtml', headers=header, data=message_payload).status_code == 200:
                try:
                    cursor.execute('''UPDATE bj_list SET pm = 1 WHERE link = (?)''', (k,))
                except sqlite3.OperationalError:
                    time.sleep(random.randint(3, 15))
                    cursor.execute('''UPDATE bj_list SET pm = 1 WHERE link = (?)''', (k,))
            else:
                print(str(requests.post('https://www.drive2.ru/ajax/messages.cshtml', headers=header, data=message_payload).status_code) + ' ERROR ' + ' PM sent ' + str(row[0]))
                return False
            connection.commit()
        print("I'm running on thread %s" % threading.current_thread() + ' PM sent ' + str(row[0]))
        time.sleep(random.randint(2000, 5000))


def profile_commenting():
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA journal_mode=WAL")
    cursor = connection.cursor()
    get_work_set = """SELECT * from bj_list WHERE like_sub = 1 and bj_comment IS NULL and pm IS NULL and profile_comment IS NULL ORDER BY profile_comment ASC LIMIT 10;"""
    cursor.execute(get_work_set)
    rows = cursor.fetchall()
    for row in rows:
        k = row[0]
        comment_payload = {
            '_': 'cc',
            'text': gen_phrase(),
            'owner': 'c',
            'ownerId': str(row[0])[30:37],
            '.FCTX': '_wfqzlwoyiseAAQcQnJ1LldlYi4xOjQ3MzM3Njg2NTM0ODc0ODExOaQLV00tWU70CYwutSfmUNNvwboI'
        }
        with connection:
            if requests.post('https://www.drive2.ru/ajax/forums.cshtml', headers=header, data=comment_payload).status_code == 200:
                try:
                    cursor.execute('''UPDATE bj_list SET profile_comment = 1 WHERE link = (?)''', (k,))
                except sqlite3.OperationalError:
                    time.sleep(random.randint(3, 15))
                    cursor.execute('''UPDATE bj_list SET profile_comment = 1 WHERE link = (?)''', (k,))
            else:
                print(str(requests.post('https://www.drive2.ru/ajax/forums.cshtml', headers=header, data=comment_payload).status_code) + ' ERROR ' + ' profile commented ' + str(row[0]))
                return False
            connection.commit()
        print("I'm running on thread %s" % threading.current_thread() + ' profile commented ' + str(row[0]))
        time.sleep(random.randint(200, 500))


def bj_commenting():
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA journal_mode=WAL")
    cursor = connection.cursor()
    get_work_set = """SELECT * from bj_list WHERE like_sub = 1 AND bj_comment IS NULL and pm IS NULL and profile_comment IS NULL ORDER BY bj_comment ASC LIMIT 10;"""
    cursor.execute(get_work_set)
    rows = cursor.fetchall()
    for row in rows:
        k = row[0]
        link = get_ownerId_bj(k)
        bj_comment_payload = {
            '_': 'cc',
            '.FCTX': '_wfqzlwoyiseAAQcQnJ1LldlYi4xOjQ3MzM3Njg2NTM0ODc0ODExOaQLV00tWU70CYwutSfmUNNvwboI',
            'owner': 'cjr',
            'ownerId': str(link),
            'text': gen_phrase()
        }
        with connection:
            if requests.post('https://www.drive2.ru/ajax/forums.cshtml', headers=header, data=bj_comment_payload).status_code == 200:
                try:
                    cursor.execute('''UPDATE bj_list SET bj_comment = 1 WHERE link = (?)''', (k,))
                except sqlite3.OperationalError:
                    time.sleep(random.randint(3, 15))
                    cursor.execute('''UPDATE bj_list SET bj_comment = 1 WHERE link = (?)''', (k,))
            else:
                print(str(requests.post('https://www.drive2.ru/ajax/forums.cshtml', headers=header, data=bj_comment_payload).status_code) + ' ERROR ' + ' bj commented ' + str(row[0]))
                return False
            connection.commit()
        print("I'm running on thread %s" % threading.current_thread() + ' bj commented ' + str(row[0]))
        time.sleep(random.randint(200, 500))


def unsubscription():
    get_sub_payload = {
        '_': 'get',
        'type': 'carsubscriptions',
        'key': 'wbxgTGaSVTyaQ4n9dP0Rmv58dFtxubVgdm_yByd4bL94ii_3prPovsQWz - bZxaflJ9SbSBK7PlEj4ELuFQursqIE_PMshsWdxOFakd7CadjY29qIbVugCzN0FYhbsb9PAzjynhncuEz4eZOVJRfq2w',
        'id': 473376865348748119,
        '.FCTX': '_wfqzlwoyiseAAQcQnJ1LldlYi4xOjQ3MzM3Njg2NTM0ODc0ODExOaQLV00tWU70CYwutSfmUNNvwboI'
    }
    print(requests.post('https://www.drive2.ru/ajax/subscription', headers=header, data=get_sub_payload).text)


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


def run_subscribe_like():
    schedule.every(24).hours.do(subscribe_like())
    run_schedule()


def run_personal_messaging():
    time.sleep(1)
    schedule.every(24).hours.do(personal_messaging())
    run_schedule()


def run_profile_commenting():
    time.sleep(5)
    schedule.every(24).hours.do(profile_commenting())
    run_schedule()


def run_bj_commenting():
    time.sleep(10)
    schedule.every(24).hours.do(bj_commenting())
    run_schedule()

def run_job():
    sub_like = Process(target=run_subscribe_like)
    pm = Process(target=run_personal_messaging)
    profile = Process(target=run_profile_commenting)
    bj = Process(target=run_bj_commenting)
    sub_like.start()
    pm.start()
    profile.start()
    bj.start()
    sub_like.join()
    pm.join()
    profile.join()
    bj.join()

if __name__ == "__main__":
    run_job()