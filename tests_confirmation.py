from robot_module import robot_singleton
from robot_module import write_into_txt


if __name__ == '__main__':

    robot_singleton.connect()
    confirmou = 0
    nao_confirmou = 0
    results = f""
    robot_singleton.close_tool()
    for i in range(1, 51):

        return_ = robot_singleton.confirmation_gripper()
        print(return_[0])

        if return_[0]:
            confirmou += 1
        else:
            nao_confirmou += 1
        result = f"Rotation: {i}\n{return_[0]}\n   Current: {return_[1]}\n   Initial current: {return_[2]}\n"
        results += result
        print(i)

    write_into_txt(results, "confirmation_tests")

    robot_singleton.open_tool()

    print("Confirmou ", confirmou)
    print("Não Confirmou ", nao_confirmou)
