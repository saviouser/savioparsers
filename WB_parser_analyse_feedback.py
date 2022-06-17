import json
import requests
from fake_useragent import UserAgent
import csv
import  time
from datetime import datetime, date, timedelta
from pprint import pprint
import random

from sqlite3 import  Error




file_result = "result_data.csv"

file_id= 'id_list.csv'
# imtId ='32079259'
id_list = ''
id = 21401242



user = UserAgent().random
print(user)
HEADER = {'user-agent': user}
# HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
# response = SESSION.post(link, headers=HEADER, verify=False).text
# r = SESSION.get('https://www.wildberries.ru', verify=False)
# print(jar := SESSION.cookies)

def get_card__properties(id):
    url = f'https://wbx-content-v2.wbstatic.net/ru/{id}.json'
    print(url)
    r = requests.get(url, headers= HEADER, verify=False)
    print(r.status_code)
    # pprint(r.json())
    if r.status_code != 200:
        return int(r.status_code)
    try:
        result_json = r.json()
        # pprint(result_json)
    except:
        result_json = "Error"
    return result_json

def get_ful_feedbacks(imt_id):
    url = 'https://public-feedbacks.wildberries.ru/api/v1/summary/full'
    payload = {
        'imtId': imt_id,
        'skip': 0,
        'take': 20
    }
    r = requests.post(url, headers=HEADER, verify=False, json=payload)
    print('2 full', r.status_code)
    # pprint(r.json())
    if r.status_code != 200:
        return int(r.status_code)
    try:
        result_json = r.json()
        # result_json = json.loads(r.text)
        # pprint(result_json)

    except:
        result_json = "Error"
    return result_json

def get_site_feedbacks(imt_id, n):
    url = 'https://public-feedbacks.wildberries.ru/api/v1/feedbacks/site'
    payload = {'imtId': imt_id,
        'order': 'dateDesc',
        'skip': n * 20,
        'take': 20
    }
    r = requests.post(url, headers=HEADER, verify=False, json=payload)
    print('2site', r.status_code)
    # pprint(r.json())
    if r.status_code != 200:
        return int(r.status_code)
    try:
        result_json = r.json()
        # result_json = json.loads(r.text)
        # pprint(result_json)

    except:
        result_json = "Error"
    return result_json

def get_url(payload, category_eng):


    url = f'https://wbxcatalog-ru.wildberries.ru/{category_eng}/catalog'
    payload_base = {
    'appType': '1',
    'cardSize': 'c516x688',
    'couponsGeo': '12,3,18,15,21',
    'curr': 'rub',
    'dest': '-1029256,-102269,-1278703,-1255563',
    'emp': '0',
    'lang': 'ru',
    'locale': 'ru',
    'pricemarginCoeff': '1.0',
    'reg':'0',
    'regions': '68,64,83,4,38,80,33,70,82,86,75,30,69,48,22,1,66,31,40,71',
    'sort': 'popular',
    'spp': '0',
    'stores': '117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043',
    }
    payload_base.update(payload)
    # pprint(payload_base)
    return url, payload_base

def get_txt_json(url, payload):
    r = requests.get(url, headers= HEADER, verify=False, params=payload)
    print(r.status_code)
    if r.status_code != 200:
        return int(r.status_code)
    try:
        result_json = json.loads(r.text)
    except:
        result_json = "Error"
    return result_json

def get_id_list(category, file=file_id):
    with open(file, newline='', encoding= 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # for row in reader:
        row_set = {row[0] if row[1] == category else '' for row in reader }
        row_list = list(row_set)[1:]
        print(category, row_list)
        return row_list


def get_catalog_position():
    global COUNT
    category_dict = {
        'Рюкзаки': ['aksessuary/sumki-i-ryukzaki/ryukzaki#c6596809', None, '138', 'bags', None],
        'Джеггинсы': ['zhenshchinam/odezhda/dzhinsy-dzhegginsy', '1687', '180;1687', 'jeans', '2'],
        'Джинсы': ['zhenshchinam/odezhda/dzhinsy-dzhegginsy', '180', '180;1687', 'jeans', '2'],
        'Брюки': ['zhenshchinam/odezhda/bryuki-i-shorty', '11', '11;147;148;313;1695;2287;3835', 'pants', '2'],
        'Шорты': ['zhenshchinam/odezhda/bryuki-i-shorty/shorty', '151', '151;216;5267', 'shorts', '2'],
        'Футболки': ['zhenshchinam/odezhda/futbolki-i-topy', '192', '185;192;219;1206;2230', 'tops_tshirts', '2'],
        'Юбки': ['zhenshchinam/odezhda/yubki', None, '38', 'skirts', '2']
                }

    for category in category_dict.keys():
        COUNT= 0
        count = 0
        id_numbers = get_id_list(category)
        print(id_numbers)
        breakout_flag = False
        for i in range(1,101):
            time.sleep(random.randrange(5,10)/10)
            print(category,page := i)
            count = i*100
            category_eng = category_dict[category][3]
            payload = {
                'page': f'{page}',
                'kind': category_dict[category][4],
                'subject': category_dict[category][2],
                'xsubject': category_dict[category][1]
            }
            url = get_url(payload, category_eng)[0]
            payload = get_url(payload, category_eng)[1]
            products = get_txt_json(url, payload)

            if products == "Error":
                print(f'Категория {category} Страница {page} не прочитана')
            else:
                products = products['data']['products']
                # print(products)
                data = {}
                for product in products:
                    # print(product['id'])
                    if str(product['id']) in id_numbers:
                        data['date'] = datetime.now()
                        data['id_number'] = product['id']
                        data['position'] = count
                        data['page'] = page
                        data['category'] = category
                        print(COUNT, data)
                        insert_data_position_to_sqlite(data)
                        COUNT += 1

                    if COUNT == len(id_numbers):
                        print(f'ДОСРОЧНО Последняя страница {page}, позиция'
                                     f' {count +100} количество id {COUNT}')
                        breakout_flag = True
                        break
                    count += 1
                if breakout_flag:
                    break



    print(f'Последняя страница {page}, позиция {count +100} количество id {COUNT}')


def write_title_csv(file):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        data = {'date': 'Дата',
                'id_number': 'Артикул WB',
                'page': 'Страница',
                'position': 'Номер позиции',
                'category': 'Категория'
                }
        writer.writerow((data['date'],
                         data['id_number'],
                         data['position'],
                         data['page'],
                         data['category']
                         ))


def write_csv(file, data):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def get_count_from_json(txt_data, id_list):
    dict_data = json.loads(txt_data)
    id_number = dict_data['data']['products']
    count = 0
    data = {}
    for d in y:
        if d['id'] in id_list:
            data['date'] = datetime.now()
            data['id_number'] = d['id']
            data['position'] = count
            data['page']
            write_csv(FILE2, data)
        count += 1
        print(d['id'], d['brand'])
    return count


def check_today_data_position_in_database():
    today = str(date.today() - timedelta(days=0))
    print('Сегодня', today)
    conn = connect_to_sqlite(DATABASE)
    table_sql = 'positions'
    cursor = conn.cursor()
    query = f"SELECT max(date) from positions ;"
    cursor.execute(query)
    max_date = cursor.fetchall()[0][0]
    print(max_date)
    print('Последняя дата в SQLite', max_date)

    column = 'date'
    if today == max_date:
        print("Данные на сегодня есть")
        query = f"DELETE FROM {table_sql} WHERE {column} = \"{today}\";"
        print(query)
        # cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        print("Данные удалены")
        query = f"SELECT max(date) from positions ;"
        cursor.execute(query)
        max_date = cursor.fetchall()[0][0]

        print('Теперь последняя дата в SQLite', max_date)

        cursor.close()
        conn.close()

    else:
        print("Данных на сегодня нет")
        return

def insert_data_position_to_sqlite(data):
    today = str(date.today() - timedelta(days=0))
    conn = connect_to_sqlite(DATABASE)

    query = '''INSERT INTO positions (date, nm_id, pos_number, page, category) VALUES (?,?,?,?,?);'''
    val = [
        today, data['id_number'], data['position'], data['page'], data['category']
         ]
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()
    print('Записаны данные на сегодня')

    query = f"SELECT max(date) from positions ;"
    cursor.execute(query)
    max_date = cursor.fetchall()[0][0]

    print('Теперь последняя дата в SQLite', max_date)

    cursor.close()
    conn.close()
    return


def main():
    id =  9761690
    result = get_card__properties(id)
    # print(result)
    print(imt_id := result['imt_id'])
    result = get_ful_feedbacks(imt_id)
    feedback_count = result['feedbackCount']
    if (feedback_count-20) % 20 == 0:
        n = (feedback_count-20)//20
    else:
        n = (feedback_count-20)//20 + 1
    if n > 250 :
        n = 250

    print(feedback_count, n)
    id = str(id)
    data_list = []

    for feedback in result['feedbacks']:
        # print('1', feedback['nmId'])
        if feedback['nmId'] == int(id):
            feedback_date = feedback['createdDate']
            data_list.append(feedback_date)
            len_data_list = len(data_list)
            print(len_data_list, feedback_date)

    for i in range(1,n+1):
        result = get_site_feedbacks(imt_id, i)
        for feedback in result['feedbacks']:
            # print('1', feedback['nmId'])
            if feedback['nmId'] == int(id):
                data_list.append(feedback['createdDate'])
                len_data_list = len(data_list)
                feedback_date = feedback['createdDate']
                print(i, len_data_list, feedback_date)

    data_list = [[x[:10]] for x in data_list]
    print(data_list)
    write_csv(file_result, data_list)






if __name__ == '__main__':
    main()
