import requests
import json
import datetime as dt
import pandas as pd
import sqlite3

def get_today():
    now = dt.datetime.now()
    fixer_key = '881d6b40589d0fd7d6064ec37e9fbb0e'
    fixer = 'http://data.fixer.io/api/'
    params = {
        'access_key':fixer_key,
    }
    date = now.strftime("%Y-%m-%d")
    resp = requests.get(fixer+date,params=params)
    out = json.loads(resp.text)
    dates = {}
    data = out['rates']
    data['EUR'] = 1.0
    dates[date] = data
    today_df = pd.DataFrame.from_dict(dates, orient = 'index')
    for col in today_df:
        today_df[col] = today_df[col]*1/today_df['USD']
    today_df=today_df.reset_index()
    col = list(today_df.columns)
    col[0] = 'Date'
    today_df.columns = col
    today_df['Date'] = pd.to_datetime(today_df['Date'], infer_datetime_format = True)
    today_df.reset_index(drop=True)
    return today_df

def update_database(df):
    con = sqlite3.connect('database.db', timeout=10)
    df.to_sql('forex', con, if_exists='append', index=False)

try:
    today_df = get_today()
except:
    quit()

try:
    update_database(today_df)
except:
    quit()