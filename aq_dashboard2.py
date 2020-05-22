from flask import Flask, request, render_template, jsonify
from openaq import OpenAQ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from openaq import parse_records
import itertools
from dotenv import load_dotenv



load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URL")

APP = Flask(__name__)

API = OpenAQ()

status, body = API.measurements(city='Los Angeles', parameter='pm25')


list1 = []
list2 = []

for x in range(1, 50):
    list1.append(body['results'][x]['date']['utc'])
    list2.append(body['results'][x]['value'])


tuplelist = zip(list1, list2)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '(Datetime: %s, Value: %s)' % (self.datetime, self.value)


@APP.route('/', methods = ['GET','POST'])
def output():

    newArray = []
    newArray = [tuplelist]
    cpl = list(itertools.product(*[i for i in newArray if i != []]))
    return render_template('template.html', cpl=cpl)

@APP.route('/records.json', methods = ['GET', 'POST'])
def record_displayer():
    condition = (Record.value >= 10)
    displays = Record.query.filter(condition).all()
    displays = parse_records(displays)
    return jsonify(displays)


@APP.route('/refresh', methods=['GET', 'POST'])
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    for x in range(1, 49):
        utc = Record(datetime = list1[x], value = list2[x])
        DB.session.add(utc)
    DB.session.commit()
    return 'Data refreshed!'
