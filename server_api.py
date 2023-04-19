import flask
from flask import jsonify, request

from data_access import import_rooms_from_JSON, export_rooms_to_JSON

blueprint = flask.Blueprint(
    'room_queue_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/room/queue/<int:room_number>', methods=['GET'])
def get_room_queue(room_number):
    registredRooms = import_rooms_from_JSON()
    room = registredRooms[str(room_number)]
    return jsonify( {str(room_number): {"active_tickets": room["active_tickets"]}})


@blueprint.route('/api/room/new_ticket', methods=['POST'])
def add_new_ticket():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['room_number', 'visitor_name', 'message']):
        return jsonify({'error': 'Bad request'})
    registredRooms = import_rooms_from_JSON()
    room_number = request.json['room_number']
    if not str(room_number) in registredRooms:
        return jsonify({'error': 'Bad request'})
    current_number = len(registredRooms[room_number]["active_tickets"])
    registredRooms[room_number]["active_tickets"].append({
        "visitor_number": current_number,
        "visitor_name": request.json['visitor_name'],
        "message": request.json['message']
    })
    export_rooms_to_JSON(registredRooms)
    return jsonify({'success': 'OK'})

