def write_into_txt(list_mensage: str, name_arqv: str):
    with open(name_arqv, 'w') as arqv:
        arqv.write(list_mensage)
