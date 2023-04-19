import io
import json
import os


def export_rooms_to_JSON(registredRooms):

    with open('registred_rooms.json', 'w', encoding="utf8") as fp:
        json.dump(registredRooms, fp)


def import_rooms_from_JSON():
    if os.path.isfile("registred_rooms.json") and os.access("registred_rooms.json", os.R_OK):
        with open("registred_rooms.json", "rt", encoding="utf8") as f:
            file = f.read()
            if file:
                return json.loads(file)
    else:
        with io.open(os.path.join(".", 'registred_rooms.json'), 'w') as f:
            f.write("")
        return {}

    return {}