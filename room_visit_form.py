from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError


class RoomVisitForm(FlaskForm):

    def __init__(self, room):
        super().__init__()
        self.room = room

    message = TextAreaField('Результат приёма')
    submit = SubmitField('Позвать следующего')

    def validate_message(self, message):
        if self.room["active_ticket"]["visitor_number"] != "":
            if not message.data or message.data == "":
                raise ValidationError("Данные о приёме должны быть записаны!")
