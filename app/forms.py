from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class IndicatorForm(Form):
    country = TextField('country',validators=[Required()])
    sector = TextField('sector',validators=[Required()])
