from robot_module import robot_singleton
from robot_module import write_into_txt
if __name__ == '__main__':
    robot_singleton.connect()
    pegou = 0
    nao_pegou = 0
    results = f""
    for i in range(1, 101):
        pegou_ = robot_singleton.close_tool()
        print(pegou_)
        current_affter = robot_singleton.atribue_from_gripper()['current_motor']
        if pegou_:
            pegou += 1
        else:
            nao_pegou += 1
        result = f"Rotation: {i}\n      {pegou_}\n      Current mottor {current_affter}\n"
        results += result
        robot_singleton.open_tool(0.60)
    write_into_txt(results)
    # for i in range(1, 11):
    #     list_destruction = robot_singleton.close_destruction()
    #     dict_destruction[i] = list_destruction
    #     robot_singleton.open_tool()
    print("Não pegou ", nao_pegou)
    print("Pegou ", pegou)
