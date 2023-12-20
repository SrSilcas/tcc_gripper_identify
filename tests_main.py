from robot_module import robot_singleton
from robot_module import write_into_txt

if __name__ == '__main__':

    robot_singleton.connect()
    pegou = 0
    nao_pegou = 0
    results = f""
    for i in range(1, 51):
        pegou_ = robot_singleton.close_tool()
        print(pegou_)
        current_affter = robot_singleton.atribue_from_gripper()['current_motor']
        position_after = robot_singleton.atribue_from_gripper()['position']
        robot_singleton.open_tool(0.60)
        if pegou_:
            pegou += 1
        else:
            nao_pegou += 1
        result = f"Rotation: {i}\n     {pegou_}\n     Current_motor: {current_affter}\n     Position: {position_after}\n"
        results += result
        print(i)
    write_into_txt(results, "text_main_0.27_95_not")
    print("Não pegou ", nao_pegou)
    print("Pegou ", pegou)
