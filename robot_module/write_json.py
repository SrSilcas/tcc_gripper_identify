import json
# todo termina isso aqui pfvr obg


def write_into_json(list_mensage: dict):
    with open("tests.json", 'w') as arqv:
        data = {}

        for key, information in list_mensage.items():
            data.add(
                (
                    f"{key}",
                    {
                        f"Position: {information[0]}",
                        f"Current: {information[1]}"
                    }
                )
            )

        json.dump(data, arqv)
