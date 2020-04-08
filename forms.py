from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

class APIKeyForm(FlaskForm):
    """API Form."""
    name = StringField('Key', [DataRequired()])
    email = StringField('Code')
    recaptcha = RecapchaField()
    submit = SubmitField('Submit')
    