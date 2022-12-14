from flask import Flask, render_template, request, flash
import json
from modules import add_db, prices


app = Flask(__name__)
app.config['SECRET_KEY'] = '05e71d11b20fd1258ccf4de08c594938'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # converting "str" to "int"
        data = {key: int(value) for key, value in request.form.to_dict().items()}
        # checks if data has 0 value then don't append to database
        data = {key: value for key, value in data.items() if value != 0}
        if data:
            # add to database and return time and check name for printing
            add_db(data)
        return render_template('index.html', data=data)
    return render_template('index.html')


@app.route('/database')
def database():
    try:
        with open('database\\db.json', 'r') as f:
            data = json.load(f)
        data = {k: v[:300] for k, v in data.items()}
        return render_template('database.html', data=data, prices=prices)
    except:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
