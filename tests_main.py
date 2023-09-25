from robot_module import robot_singleton
from robot_module import write_into_json
if __name__ == '__main__':
    robot_singleton.connect()
    pegou = 0
    nao_pegou = 0
    for i in range(1, 101):
        pegou_ = robot_singleton.close_tool()
        robot_singleton.open_tool(0.60)
        if pegou_:
            pegou += 1
        else:
            nao_pegou += 1
    # for i in range(1, 11):
    #     list_destruction = robot_singleton.close_destruction()
    #     dict_destruction[i] = list_destruction
    #     robot_singleton.open_tool()
    print("Não pegou ", nao_pegou)
    print("Pegou ", pegou)
