from robot_module import robot_singleton
from robot_module import write_into_txt
if __name__ == '__main__':
    robot_singleton.connect()
    results = f""
    for i in range(1, 51):
        tuple_ = robot_singleton.close_destruction()
        robot_singleton.open_tool(0.60)

        result = f"Rotation: {i}\n     Current_mottor: {tuple_[0]}\n     Position: {tuple_[1]}\n"
        results += result
    write_into_txt(results, "test_destruction")
