from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from functions import *
import logging
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

app = Flask(__name__)

CORS(app)

def read_params(sd,ed):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    base = request.args.get('base')
    cur = request.args.get('cur')
    dmsg =request.args.get('dmsg')
    fmsg =request.args.get('fmsg')
    if not start_date:
        start_date = sd
    if not end_date:
        end_date = ed
    if not cur:
        cur = 'EUR'
    if not base:
        base = 'USD'
    return start_date, end_date, base, cur, dmsg, fmsg

def dates_func(sd,ed):
    app.logger.info("DATES SUBMITTED")
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    msg = None
    if validate(start_date) is False:
        msg = 'Start Date Invalid'
        start_date = sd
    if validate(end_date) is False:
        msg = 'Invalid Dates'
        end_date = ed
    return start_date, end_date, msg 

def cur_func(b, c):
    app.logger.info("CURRENCIES SUBMITTED")
    cur = request.form['cur'].upper()
    base = request.form['base'].upper()
    msg = None
    if cur not in currency_list:
            msg = 'Conversion Currency Not Valid'
            cur = c
    if base not in currency_list:
        if len(base) > 0:
            msg = 'Base Currency Not Valid'
        base = b
    return base, cur, msg

@app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
def index():
    df = get_forex('forex')
    min_date = min(pd.to_datetime(df['Date'])).strftime('%Y-%m-%d')
    max_date = max(pd.to_datetime(df['Date'])).strftime('%Y-%m-%d')

    start_date, end_date, base, cur, dmsg, fmsg = read_params(min_date,max_date)

    dmsg = None
    fmsg = None
    full_url = url_for('.index', **request.args)
    app.logger.info(full_url)

    if request.form.get("dates") == "Submit":
        start_date, end_date, dmsg = dates_func(min_date,max_date)
        #return redirect("/?start_date={sd}&end_date={ed}&base={base}&cur={cur}&dmsg={dmsg}&fmsg={fmsg}".format(sd=start_date,ed=end_date,base=base,cur=cur,dmsg=dmsg,fmsg=fmsg))
        return redirect("/?start_date={sd}&end_date={ed}&base={base}&cur={cur}".format(sd=start_date,ed=end_date,base=base,cur=cur))
    

    df = df[(start_date<=df["Date"]) & (df["Date"]<end_date)]

    if request.form.get("currencies") == "Submit":
        base, cur, fmsg = cur_func(base, cur)
        #return redirect("/?start_date={sd}&end_date={ed}&base={base}&cur={cur}&dmsg={dmsg}&fmsg={fmsg}".format(sd=start_date,ed=end_date,base=base,cur=cur,dmsg=dmsg,fmsg=fmsg))
        return redirect("/?start_date={sd}&end_date={ed}&base={base}&cur={cur}".format(sd=start_date,ed=end_date,base=base,cur=cur))
    
    if request.form.get("reverse") == "Reverse":
        cur, base, fmsg = cur_func(base, cur)
        #return redirect("/?start_date={sd}&end_date={ed}&base={base}&cur={cur}&dmsg={dmsg}&fmsg={fmsg}".format(sd=start_date,ed=end_date,base=base,cur=cur,dmsg=dmsg,fmsg=fmsg))
        return redirect("/?start_date={sd}&end_date={ed}&base={base}&cur={cur}".format(sd=start_date,ed=end_date,base=base,cur=cur))

    plot_url = make_plot(df, cur, base)
    return render_template('index.html', plot_url=plot_url, start_date=start_date, end_date=end_date, base=base, cur=cur, current_price = get_latest(base,cur), currency_list=currency_list_long) #, dmsg=dmsg,fmsg=fmsg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    #app.run(debug=True)