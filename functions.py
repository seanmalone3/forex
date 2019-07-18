import sqlite3
from os import path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64
import seaborn as sns
import datetime

ROOT = path.dirname(path.relpath((__file__)))

def update_forex(ex_date, base, usd, eur, gbp):
    con = sqlite3.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('insert into forex (ex_date, base, usd, eur, gbp) values(?, ?, ?, ?, ?)', (ex_date, base, usd, eur, gbp))
    con.commit()
    con.close()

def create_table(name):
    con = sqlite3.connect(path.join(ROOT, 'database.db'))
    df = pd.read_csv(path.join(ROOT,"2017-2019_forex.csv"))
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format = True)
    df.to_sql(name, con, index=False, if_exists='replace')
    return pd.read_sql('select * from {}'.format(name), con)

def get_forex(table):
    con = sqlite3.connect(path.join(ROOT, 'database.db'))
    return pd.read_sql('select * from {}'.format(table), con)
    #cur = con.cursor()
    #cur.execute('select * from {}'.format(table))
    #data = cur.fetchall()
    #return data

def convert(df,cur='EUR',base='USD',reverse=False):
    if reverse:
        return df[base]/df[cur]
    else:  
        return df[cur]/df[base]

def make_plot(df, cur='EUR', base='USD'):
    x = pd.to_datetime(df['Date'], infer_datetime_format=True)
    y = convert(df,cur,base)
    
    img = io.BytesIO()
    sns.set_style("darkgrid")
    sns.set_context("notebook", font_scale=1.4)
    fig, ax = plt.subplots()
    ax.plot(x,y)

    locator = mdates.AutoDateLocator(minticks=4,maxticks=31)
    formatter = mdates.AutoDateFormatter(locator)

    plt.gcf()
    fig.set_size_inches(9, 5)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    #ax.set_facecolor('red')
    fig.patch.set_visible(False) 
    plt.title('{cur} to {base} Currency Conversion'.format(cur=cur,base=base))
    plt.ylabel('{cur} / {base}'.format(cur=cur,base=base))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(img, format='png') #facecolor=fig.get_facecolor(),edgecolor='none') 
    plt.close()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except:
        return False

currency_list = ['AED',
 'AFN',
 'ALL',
 'AMD',
 'ANG',
 'AOA',
 'ARS',
 'AUD',
 'AWG',
 'AZN',
 'BAM',
 'BBD',
 'BDT',
 'BGN',
 'BHD',
 'BIF',
 'BMD',
 'BND',
 'BOB',
 'BRL',
 'BSD',
 'BTC',
 'BTN',
 'BWP',
 'BYN',
 'BYR',
 'BZD',
 'CAD',
 'CDF',
 'CHF',
 'CLF',
 'CLP',
 'CNY',
 'COP',
 'CRC',
 'CUC',
 'CUP',
 'CVE',
 'CZK',
 'DJF',
 'DKK',
 'DOP',
 'DZD',
 'EGP',
 'ERN',
 'ETB',
 'EUR',
 'FJD',
 'FKP',
 'GBP',
 'GEL',
 'GGP',
 'GHS',
 'GIP',
 'GMD',
 'GNF',
 'GTQ',
 'GYD',
 'HKD',
 'HNL',
 'HRK',
 'HTG',
 'HUF',
 'IDR',
 'ILS',
 'IMP',
 'INR',
 'IQD',
 'IRR',
 'ISK',
 'JEP',
 'JMD',
 'JOD',
 'JPY',
 'KES',
 'KGS',
 'KHR',
 'KMF',
 'KPW',
 'KRW',
 'KWD',
 'KYD',
 'KZT',
 'LAK',
 'LBP',
 'LKR',
 'LRD',
 'LSL',
 'LTL',
 'LVL',
 'LYD',
 'MAD',
 'MDL',
 'MGA',
 'MKD',
 'MMK',
 'MNT',
 'MOP',
 'MRO',
 'MUR',
 'MVR',
 'MWK',
 'MXN',
 'MYR',
 'MZN',
 'NAD',
 'NGN',
 'NIO',
 'NOK',
 'NPR',
 'NZD',
 'OMR',
 'PAB',
 'PEN',
 'PGK',
 'PHP',
 'PKR',
 'PLN',
 'PYG',
 'QAR',
 'RON',
 'RSD',
 'RUB',
 'RWF',
 'SAR',
 'SBD',
 'SCR',
 'SDG',
 'SEK',
 'SGD',
 'SHP',
 'SLL',
 'SOS',
 'SRD',
 'STD',
 'SVC',
 'SYP',
 'SZL',
 'THB',
 'TJS',
 'TMT',
 'TND',
 'TOP',
 'TRY',
 'TTD',
 'TWD',
 'TZS',
 'UAH',
 'UGX',
 'USD',
 'UYU',
 'UZS',
 'VEF',
 'VND',
 'VUV',
 'WST',
 'XAF',
 'XAG',
 'XAU',
 'XCD',
 'XDR',
 'XOF',
 'XPF',
 'YER',
 'ZAR',
 'ZMK',
 'ZMW',
 'ZWL']