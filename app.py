import csv
from ctypes.wintypes import DWORD
from distutils.log import debug
from pickle import TRUE
from traceback import print_tb
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

from pymongo import MongoClient
import pandas as pd

connection = MongoClient("mongodb+srv://admin:kJvQFZXu0vy387c9@cluster0.jdcgk.mongodb.net/cloudDB?retryWrites=true&w=majority")
db = connection['cloudDB']
collection = db['tweetdata']
df =pd.DataFrame(list(collection.find({}))) 

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/<string:page_name>', methods=['GET', 'POST'])
def html_page(page_name):
    return render_template(page_name, tables=[df.to_html(classes='data')], titles=df.columns.values)


# def write_to_file(data):
#     with open('database.txt', mode='a') as database:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         file = database.write(f'\n{email},{subject},{message}')


def write_to_csv(data):
    with open('database.csv', 'a', newline='') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        writer = csv.writer(csvfile)
        writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong!'

