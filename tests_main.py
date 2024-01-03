import time

from robot_module import robot_singleton
from robot_module import write_into_txt

if __name__ == '__main__':

    robot_singleton.connect()
    pegou = 0
    nao_pegou = 0
    results = f""
    for i in range(1, 51):
        tuple_ = robot_singleton.close_tool()
        pegou_ = tuple_[0]
        current_after = tuple_[1]
        average = tuple_[2]
        difference = tuple_[3]
        print(pegou_)
        position_after = robot_singleton.atribute_from_gripper()['position']
        robot_singleton.open_tool(0.60)
        time.sleep(0.6)
        if pegou_:
            pegou += 1
        else:
            nao_pegou += 1
        result = (f"Rotation: {i}\n     {pegou_}\n     Current_motor: {current_after}\n"
                  f"     Position: {position_after}\n     Average: {average}\n     Difference: {difference}\n")
        results += result
        print(i)
    write_into_txt(results, "text_implet_get")
    print("Não pegou ", nao_pegou)
    print("Pegou ", pegou)
