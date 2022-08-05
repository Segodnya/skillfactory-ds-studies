# export FLASK_APP=recapp.py
# export FLASK_ENV=development
# flask run
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from zipfile import ZipFile


app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'

# Create a ZipFile Object and load sample.zip in it
with ZipFile('visitors.zip', 'r') as zipObj:
    # Extract all the contents of zip file in current directory
    zipObj.extractall()
visitors = pd.read_csv('visitors.csv')


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    start = request.form['action'] == 'Predict'
    visitorid = int(request.form['visitorid'])
    if start:
        # top 3 value_counts() items from train dataset
        top3 = [5411, 461686, 187946]
        if visitorid not in visitors.visitorid.values:
            first, second, third = top3[0], top3[1], top3[2]
            return '<h1>{}, {}, {}</h1>'.format(first, second, third)
        else:
            # Get the row with visitorid
            row = visitors[visitors.visitorid == visitorid]
            # Get the list of items from the row
            items_list = []
            try:
                items_list.append(int(row['first'].values))
            except:
                items_list.append(np.nan)
            try:
                items_list.append(int(row['second'].values))
            except:
                items_list.append(np.nan)
            try:
                items_list.append(int(row['third'].values))
            except:
                items_list.append(np.nan)
            # Get the number of Nans in the item_list
            cold_start_count = row.cold_start_count.values[0]
            # If there is 1 Nan in the row, replace it with top3[0]
            if cold_start_count == 1:
                items_list[2] = top3[0]
                first, second, third = items_list[0], items_list[1], items_list[2]
                return '<h1>{}, {}, {}</h1>'.format(first, second, third)
            # If there are 2 Nans in the row, replace it with top3[0] and top3[1]
            elif cold_start_count == 2:
                items_list[1] = top3[0]
                items_list[2] = top3[1]
                first, second, third = items_list[0], items_list[1], items_list[2]
                return '<h1>{}, {}, {}</h1>'.format(first, second, third)
            # If there are 3 Nans in the row, replace it with top3[0], top3[1] and top3[2]
            elif cold_start_count == 3:
                items_list[0] = top3[0]
                items_list[1] = top3[1]
                items_list[2] = top3[2]
                first, second, third = items_list[0], items_list[1], items_list[2]
                return '<h1>{}, {}, {}</h1>'.format(first, second, third)
            else:
                first, second, third = items_list[0], items_list[1], items_list[2]
                return '<h1>{}, {}, {}</h1>'.format(first, second, third)
        