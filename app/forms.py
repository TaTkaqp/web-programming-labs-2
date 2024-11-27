from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.csrf import CSRFProtect

class DeleteMessageForm(FlaskForm):
    submit = SubmitField('Delete')
