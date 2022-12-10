from flask import Flask, render_template, request, flash
import json
from datetime import date
from time import time
from hashlib import md5


app = Flask(__name__)
app.config['SECRET_KEY'] = '05e71d11b20fd1258ccf4de08c594938'


def add_db(data):
    time_date = date.today().isoformat()
    check_name = md5(str(time()).encode()).hexdigest()[10:17].upper()
    new_data = {check_name: data}
    with open('db.json', 'r') as f:
        try:
            json_data = json.load(f)
        except:
            json_data = dict()
    try:
        json_data[time_date].append(new_data)
    except:
        json_data.update({time_date: [new_data]})
    finally:
        with open('db.json', 'w') as f:
            json.dump(json_data, f)
    return time_date, check_name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # checks if data has 0 value then don't append to database
        data = {key: value for key, value in request.form.to_dict().items() if value != '0'}
        time_date, check_name = add_db(data)
        flash(f'Tarix : {time_date}, Cek Nomresi : {check_name}, Sifarisler : {data}', category='success')
        return render_template('index.html', data=data)
    return render_template('index.html')


@app.route('/database')
def database():
    with open('db.json', 'r') as f:
        data = json.load(f)
    return render_template('database.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)