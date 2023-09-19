from robot_module import robot_singleton
from robot_module import write_into_json
if __name__ == '__main__':
    robot_singleton.connect()
    for i in range(1, 11):
        pegou = robot_singleton.close_tool()
        print(pegou)
        robot_singleton.open_tool(0.70)

    # for i in range(1, 11):
    #     list_destruction = robot_singleton.close_destruction()
    #     write_into_json(list_destruction, i)
    #     robot_singleton.open_tool()
