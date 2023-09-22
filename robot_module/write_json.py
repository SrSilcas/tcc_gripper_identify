import json


def write_into_json(list_mensage: dict):
    with open("tests.json", 'w') as arqv:
        data = {
            {
                list_mensage
            }
        }
        json.dump(data, arqv)
