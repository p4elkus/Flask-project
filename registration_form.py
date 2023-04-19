from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError


class RegistrationForm(FlaskForm):

    def __init__(self, currentRegisteredNumbers):
        super().__init__()
        self.currentRegisteredNumbers = currentRegisteredNumbers

    roomnumber = IntegerField('Номер комнаты', validators=[])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')

    def validate_roomnumber(self, roomnumber):
        if roomnumber.data in self.currentRegisteredNumbers:
            raise ValidationError("This room already exist! Change number.")
        if roomnumber.data is None:
            raise ValidationError("Empty field!")
