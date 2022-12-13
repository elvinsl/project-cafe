from datetime import date
from time import time
from hashlib import md5
import json


prices = {
    'pive': 1.5,
    'pendir': 1,
    'cay': 2,
}


def calc_price(data):
    total = 0
    for k, v in data.items():
        total += prices[k] * v
    
    return f'{str(total)} ₼'


def add_db(data):
    time_date = date.today().isoformat()
    check_name = md5(str(time()).encode()).hexdigest()[10:17].upper()
    masa_number = data['masa']
    data.pop('masa')
    price = calc_price(data)
    new_data = {check_name: data}
    new_data[check_name]['total'] = price
    new_data[check_name]['masa'] = masa_number
    with open('db.json', 'r') as f:
        try:
            json_data = json.load(f)
        except:
            json_data = dict()
    try:
        json_data[time_date].insert(0, new_data)
    except:
        new_json_data = {time_date: [new_data]}
        new_json_data.update(json_data)
        json_data = new_json_data
        # json_data.update({time_date: [new_data]})
    finally:
        with open('db.json', 'w') as f:
            json.dump(json_data, f)


def get_monthly_price(date):
    with open('db.json', 'r') as f:
        data = json.load(f)

    total = 0

    for i in data[date]:
        try:
            total += float(list(i.values())[0]['total'].split(' ')[0])
        except:
            continue


    return total
