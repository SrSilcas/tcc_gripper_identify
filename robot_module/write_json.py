import json


def write_into_json(list_mensage: tuple, indice: int):
    with ("tests.json", 'w') as arqv:
        data = {
            indice: {
                "position": list_mensage[1],
                "current": list_mensage[0]
            }
        }
        json.dump(data, arqv)
