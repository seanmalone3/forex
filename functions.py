import sqlite3
from os import path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64
import seaborn as sns
import datetime
import requests
import json

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

short_list = ['CAD','EUR',
 'HKD',
 'ISK',
 'PHP',
 'DKK',
 'HUF',
 'CZK',
 'AUD',
 'RON',
 'SEK',
 'IDR',
 'INR',
 'BRL',
 'RUB',
 'HRK',
 'JPY',
 'THB',
 'CHF',
 'SGD',
 'PLN',
 'BGN',
 'TRY',
 'CNY',
 'NOK',
 'NZD',
 'ZAR',
 'USD',
 'MXN',
 'ILS',
 'GBP',
 'KRW',
 'MYR']

def get_latest(base,cur):
    fixer_latest = 'https://api.exchangeratesapi.io/latest'
    # if cur.upper() in short_list: 
    if all(x in currency_list for x in [base, cur]):
        try:
            resp = requests.get(fixer_latest)
            out = json.loads(resp.text)
            data = out['rates']
            data['EUR'] = 1/data['USD']
            return round(data[cur]/data[base],5)
        except:
            return "Instant price not available."
    else:
        return "Instant price not available."

currency_list_long = ['AED : United Arab Emirates Dirham',
'AFN : Afghan Afghani',
'ALL : Albanian Lek',
'AMD : Armenian Dram',
'ANG : Netherlands Antillean Guilder',
'AOA : Angolan Kwanza',
'ARS : Argentine Peso',
'AUD : Australian Dollar',
'AWG : Aruban Florin',
'AZN : Azerbaijani Manat',
'BAM : Bosnia-Herzegovina Convertible Mark',
'BBD : Barbadian Dollar',
'BDT : Bangladeshi Taka',
'BGN : Bulgarian Lev',
'BHD : Bahraini Dinar',
'BIF : Burundian Franc',
'BMD : Bermudan Dollar',
'BND : Brunei Dollar',
'BOB : Bolivian Boliviano',
'BRL : Brazilian Real',
'BSD : Bahamian Dollar',
'BTC : Bitcoin',
'BTN : Bhutanese Ngultrum',
'BWP : Botswanan Pula',
'BYR : Belarusian Ruble',
'BYN : New Belarusian Ruble',
'BZD : Belize Dollar',
'CAD : Canadian Dollar',
'CDF : Congolese Franc',
'CHF : Swiss Franc',
'CLF : Chilean Unit of Account (UF)',
'CLP : Chilean Peso',
'CNY : Chinese Yuan',
'COP : Colombian Peso',
'CRC : Costa Rican Colón',
'CUC : Cuban Convertible Peso',
'CUP : Cuban Peso',
'CVE : Cape Verdean Escudo',
'CZK : Czech Republic Koruna',
'DJF : Djiboutian Franc',
'DKK : Danish Krone',
'DOP : Dominican Peso',
'DZD : Algerian Dinar',
'EGP : Egyptian Pound',
'ERN : Eritrean Nakfa',
'ETB : Ethiopian Birr',
'EUR : Euro',
'FJD : Fijian Dollar',
'FKP : Falkland Islands Pound',
'GBP : British Pound Sterling',
'GEL : Georgian Lari',
'GGP : Guernsey Pound',
'GHS : Ghanaian Cedi',
'GIP : Gibraltar Pound',
'GMD : Gambian Dalasi',
'GNF : Guinean Franc',
'GTQ : Guatemalan Quetzal',
'GYD : Guyanaese Dollar',
'HKD : Hong Kong Dollar',
'HNL : Honduran Lempira',
'HRK : Croatian Kuna',
'HTG : Haitian Gourde',
'HUF : Hungarian Forint',
'IDR : Indonesian Rupiah',
'ILS : Israeli New Sheqel',
'IMP : Manx pound',
'INR : Indian Rupee',
'IQD : Iraqi Dinar',
'IRR : Iranian Rial',
'ISK : Icelandic Króna',
'JEP : Jersey Pound',
'JMD : Jamaican Dollar',
'JOD : Jordanian Dinar',
'JPY : Japanese Yen',
'KES : Kenyan Shilling',
'KGS : Kyrgystani Som',
'KHR : Cambodian Riel',
'KMF : Comorian Franc',
'KPW : North Korean Won',
'KRW : South Korean Won',
'KWD : Kuwaiti Dinar',
'KYD : Cayman Islands Dollar',
'KZT : Kazakhstani Tenge',
'LAK : Laotian Kip',
'LBP : Lebanese Pound',
'LKR : Sri Lankan Rupee',
'LRD : Liberian Dollar',
'LSL : Lesotho Loti',
'LTL : Lithuanian Litas',
'LVL : Latvian Lats',
'LYD : Libyan Dinar',
'MAD : Moroccan Dirham',
'MDL : Moldovan Leu',
'MGA : Malagasy Ariary',
'MKD : Macedonian Denar',
'MMK : Myanma Kyat',
'MNT : Mongolian Tugrik',
'MOP : Macanese Pataca',
'MRO : Mauritanian Ouguiya',
'MUR : Mauritian Rupee',
'MVR : Maldivian Rufiyaa',
'MWK : Malawian Kwacha',
'MXN : Mexican Peso',
'MYR : Malaysian Ringgit',
'MZN : Mozambican Metical',
'NAD : Namibian Dollar',
'NGN : Nigerian Naira',
'NIO : Nicaraguan Córdoba',
'NOK : Norwegian Krone',
'NPR : Nepalese Rupee',
'NZD : New Zealand Dollar',
'OMR : Omani Rial',
'PAB : Panamanian Balboa',
'PEN : Peruvian Nuevo Sol',
'PGK : Papua New Guinean Kina',
'PHP : Philippine Peso',
'PKR : Pakistani Rupee',
'PLN : Polish Zloty',
'PYG : Paraguayan Guarani',
'QAR : Qatari Rial',
'RON : Romanian Leu',
'RSD : Serbian Dinar',
'RUB : Russian Ruble',
'RWF : Rwandan Franc',
'SAR : Saudi Riyal',
'SBD : Solomon Islands Dollar',
'SCR : Seychellois Rupee',
'SDG : Sudanese Pound',
'SEK : Swedish Krona',
'SGD : Singapore Dollar',
'SHP : Saint Helena Pound',
'SLL : Sierra Leonean Leone',
'SOS : Somali Shilling',
'SRD : Surinamese Dollar',
'STD : São Tomé and Príncipe Dobra',
'SVC : Salvadoran Colón',
'SYP : Syrian Pound',
'SZL : Swazi Lilangeni',
'THB : Thai Baht',
'TJS : Tajikistani Somoni',
'TMT : Turkmenistani Manat',
'TND : Tunisian Dinar',
'TOP : Tongan Paʻanga',
'TRY : Turkish Lira',
'TTD : Trinidad and Tobago Dollar',
'TWD : New Taiwan Dollar',
'TZS : Tanzanian Shilling',
'UAH : Ukrainian Hryvnia',
'UGX : Ugandan Shilling',
'USD : United States Dollar',
'UYU : Uruguayan Peso',
'UZS : Uzbekistan Som',
'VEF : Venezuelan Bolívar Fuerte',
'VND : Vietnamese Dong',
'VUV : Vanuatu Vatu',
'WST : Samoan Tala',
'XAF : CFA Franc BEAC',
'XAG : Silver (troy ounce)',
'XAU : Gold (troy ounce)',
'XCD : East Caribbean Dollar',
'XDR : Special Drawing Rights',
'XOF : CFA Franc BCEAO',
'XPF : CFP Franc',
'YER : Yemeni Rial',
'ZAR : South African Rand',
'ZMK : Zambian Kwacha (pre-2013)',
'ZMW : Zambian Kwacha',
'ZWL : Zimbabwean Dollar']