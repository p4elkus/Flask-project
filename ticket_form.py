from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class TicketForm(FlaskForm):

    def __init__(self, currentRegisteredRooms):
        super().__init__()
        self.roomnumber.choices = list(currentRegisteredRooms.keys())
        self.currentRegisteredRooms = currentRegisteredRooms

    roomnumber = SelectField('Номер комнаты')
    name = StringField('Ваше имя', validators=[DataRequired()])
    message = TextAreaField('Цель визита')
    submit = SubmitField('Встать в очередь')
