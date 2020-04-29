from flask import Flask, request, render_template
from openaq import OpenAQ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *


APP = Flask(__name__)

API = OpenAQ()

status, body = API.measurements(city='Los Angeles', parameter='pm25')


list1 = []
list2 = []

for x in range(1, 50):
    list1.append(body['results'][x]['date']['utc'])
    list2.append(body['results'][x]['value'])


APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)



class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __init__(self, datetime, value):
        self.datetime = datetime
        self.value = value

    def __repr__(self):
        utc_records = self.Record.query.all()
        return utc_records


@APP.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model.save()
        # Failure to return a redirect or render_template
    else:
        return render_template('template.html')

@APP.route('/')
def root():
    condition = (Record.value >= 10)
    records = Record.query.filter(condition).all()
    print(records)
    return records




@APP.route('/refresh', methods=['GET', 'POST'])
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Reupdacord objects with it, and add to db
    # utc1 = Record(datetime = list1[0], value = list2[0])
    # utc2 = Record(datetime = list1[1], value = list2[1])
    # utc3 = Record(datetime = list1[2], value = list2[2])
    # utc4 = Record(datetime = list1[3], value = list2[3])
    # utc5 = Record(datetime = list1[4], value = list2[4])
    # utc6 = Record(datetime = list1[5], value = list2[5])
    # utc7 = Record(datetime = list1[16], value = list2[6])
    # DB.session.add(utc1)
    # DB.session.add(utc2)
    # DB.session.add(utc3)
    # DB.session.add(utc4)
    # DB.session.add(utc5)
    # DB.session.add(utc6)
    # DB.session.add(utc7)
    for x in range(1, 49):
        utc = Record(datetime = list1[x], value = list2[x])
        DB.session.add(utc)
    DB.session.commit()
    return 'Data refreshed!'

breakpoint()