import sqlite3
from app import app
from forms import IndicatorForm
from flask import render_template, flash, redirect, _app_ctx_stack, request, jsonify
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'db', 'indicators.sqlite')

def get_db():
    top = _app_ctx_stack.top
    db = getattr(top, '_database', None)
    if db is None:
        db = top._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
@app.route("/index", methods = ['GET','POST'])
def index():
    form = IndicatorForm(request.form)
    countrylist = []
    for country in query_db("select distinct post from indicators order by post"):
        countrylist.append((country[0],country[0]))
    form.country.choices = countrylist

    sectorlist = []
    for sector in query_db("select distinct project from indicators where post = ? order by project",[countrylist[0][0]]):
        sectorlist.append((sector[0],sector[0]))
    form.sector.choices = sectorlist

    if request.method == 'POST':
        flash('You chose country = ' + form.country.data + ', sector = ' + form.sector.data)
        return redirect('/index')
    return render_template('index.html',title='Home',form=form)

@app.route("/updatesectors") #, methods = ['POST'])
def updatesectors():
    country = request.args.get('country', 'Thailand')
    print country
    sectorlist = []
    for sector in query_db("select distinct project from indicators where post = ? order by project",[country]):
        sectorlist.append(sector[0])
    return jsonify({'options': sectorlist})

@app.teardown_appcontext
def close_connection(exception):
    top = _app_ctx_stack.top
    db = getattr(top, '_database', None)
    if db is not None:
        db.close()
