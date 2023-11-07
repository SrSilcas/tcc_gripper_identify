from robot_module import robot_singleton
from robot_module import write_into_txt
if __name__ == '__main__':
    robot_singleton.connect()
    results = f""
    for i in range(1, 51):
        list_ = robot_singleton.close_destruction()
        robot_singleton.open_tool(0.60)

        for element in list_:
            result = f"Rotation: {i}\n     Current_mottor: {element[0]}\n     Position: {element[1]}\n"
            results += result
    write_into_txt(results, "test_destruction")
