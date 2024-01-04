import time

from robot_module import robot_singleton
from robot_module import write_into_txt

if __name__ == '__main__':

    robot_singleton.connect()
    pegou = 0
    nao_pegou = 0
    results = f""
    for i in range(1, 51):
        list_ = robot_singleton.close_tool()
        pegou_ = list_[0]
        first_current = list_[1]
        second_current = list_[2]
        first_position = list_[3]
        second_position = list_[4]
        average = list_[5]
        difference = list_[6]

        print(pegou_)
        position_after = robot_singleton.attribute_from_gripper()['position']
        robot_singleton.open_tool(0.60)
        time.sleep(0.6)

        if pegou_:
            pegou += 1
        else:
            nao_pegou += 1
        result = (f"Rotation: {i}\n     {pegou_}\n     First Current: {first_current}\n"
                  f"     Second Current: {second_current}\n     Average: {average}\n     Difference: {difference}\n"
                  f"     First position: {first_position}\n     Second Position: {second_position}\n")
        results += result
        print(i)
    write_into_txt(results, "text_implet_not")
    print("Não pegou ", nao_pegou)
    print("Pegou ", pegou)
