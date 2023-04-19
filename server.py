from flask import Flask, url_for, render_template, redirect

import server_api
from data_access import export_rooms_to_JSON, import_rooms_from_JSON
from loginform import LoginForm
from registration_form import RegistrationForm
from room_visit_form import RoomVisitForm
from ticket_form import TicketForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

registredRooms = {}
closedRooms = []


def prepare_parameters():
    param = {}
    param['style'] = f"{url_for('static', filename='css/style.css')}"
    param['icon'] = f"{url_for('static', filename='img/Logo.png')}"
    return param


@app.route('/')
@app.route('/index')
@app.route('/index/')
def base():
    r = list(registredRooms.values())
    return render_template('index.html', rooms=r, **prepare_parameters())


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(registredRooms.keys())
    if form.validate_on_submit():
        registredRooms[str(form.roomnumber.data)] = {
            "number": str(form.roomnumber.data),
            "username": form.username.data,
            "pwd": form.password.data,
            "active_ticket": {
                "visitor_number": "",
                "visitor_name": "Еще нет поситителя",
                "message": ""
            },
            "active_tickets": [],
            "closed_tickets": []
        }
        export_rooms_to_JSON(registredRooms)
        return redirect('/success/Вы успешно зарегистрировали команту!')
    return render_template('registration.html', title='Регистрация кабинета', form=form, **prepare_parameters())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(registredRooms)
    if form.validate_on_submit():
        return redirect(f'/room/{form.roomnumber.data}')
    return render_template('login.html', title='Авторизация', form=form, **prepare_parameters())


@app.route('/request_ticket', methods=['GET', 'POST'])
def request_ticket():
    form = TicketForm(registredRooms)
    if form.validate_on_submit():
        current_number = len(registredRooms[form.roomnumber.data]["active_tickets"])
        registredRooms[form.roomnumber.data]["active_tickets"].append({
            "visitor_number": current_number,
            "visitor_name": form.name.data,
            "message": form.message.data
        })
        export_rooms_to_JSON(registredRooms)
        return redirect(
            f'/success/Вы успешно завели талон! Ваш номер {current_number} в комнату {form.roomnumber.data}. Ждите как вас вызовут')
    return render_template('request_ticket.html', title='Получение талона', form=form, **prepare_parameters())


@app.route('/room/close/<int:number>')
def close_room(number):
    closedRooms.append(registredRooms.pop(str(number)))
    export_rooms_to_JSON(registredRooms)
    return redirect(f'/success/Вы успешно закрыли комнату!')


@app.route('/room/<int:number>', methods=['GET', 'POST'])
def room(number):
    if str(number) in registredRooms:
        room = registredRooms[str(number)]
        room_visit_form = RoomVisitForm(room)
        if room_visit_form.validate_on_submit():
            if room["active_ticket"]["visitor_number"] != "":
                room["active_ticket"]["message"] = room_visit_form.message.data

            room["closed_tickets"].append(room["active_ticket"])

            if room["active_tickets"]:
                room["active_ticket"] = room["active_tickets"].pop(0)
            else:
                room["active_ticket"] = {
                    "visitor_number": "",
                    "visitor_name": "Еще нет поситителя",
                    "message": ""
                }
            export_rooms_to_JSON(registredRooms)
        return render_template('room.html', title='Комната', room=room, form=room_visit_form, **prepare_parameters())
    else:
        return "Такой комнаты нет"


@app.route('/success/<string:msg>')
def success(msg):
    return render_template('success.html', message=msg, **prepare_parameters())


if __name__ == '__main__':
    registredRooms = import_rooms_from_JSON()
    app.register_blueprint(server_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
