from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

class DataForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    content = FileField('content')
