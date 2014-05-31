from flask.ext.wtf import Form
from wtforms import SelectField

class IndicatorForm(Form):
    country = SelectField('country')
    sector = SelectField('sector')
