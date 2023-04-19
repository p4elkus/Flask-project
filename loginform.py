from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError


class LoginForm(FlaskForm):

    def __init__(self, currentRegisteredRooms):
        super().__init__()
        keys = [key for key in currentRegisteredRooms]
        self.roomnumber.choices = keys
        self.currentRegisteredRooms = currentRegisteredRooms

    roomnumber = SelectField('Номер комнаты', validators=[DataRequired()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    def validate_username(self, username):
        if self.roomnumber.data != None:
            if username.data != self.currentRegisteredRooms[self.roomnumber.data]["username"]:
                raise ValidationError("This wrong login.")

    def validate_password(self, password):
        if self.roomnumber.data != None:
            if password.data != self.currentRegisteredRooms[self.roomnumber.data]["pwd"]:
                raise ValidationError("This wrong password.")
