from app import app
from forms import IndicatorForm
from flask import render_template, flash, redirect

@app.route("/")
@app.route("/index", methods = ['GET','POST'])
def index():
    form = IndicatorForm()
    if form.validate_on_submit():
        flash('You entered ' + form.country.data + ', ' + form.sector.data)
        return redirect('/index')
    return render_template('index.html',title='Home',form=form)
