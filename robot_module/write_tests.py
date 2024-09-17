def write_into_txt(list_mensage: str, name_arqv: str):
    with open(name_arqv, 'a+') as arqv:
        arqv.write(list_mensage)


def get_information(tuple_information: tuple, name_tuple: tuple, rotation=0):
    number_of_information = 0

    for i in range(len(tuple_information)):
        number_of_information += 1

    information = f''
    for i in range(len(tuple_information[0])):
        information += f'Rotation {rotation + 1}\n'
        rotation += 1
        for j in range(number_of_information):

            information += f'   {name_tuple[j]}: {tuple_information[j][i]}\n'

    return information, rotation
