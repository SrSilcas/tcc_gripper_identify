from robot_module import robot_singleton
import time

def gripper_move():
    robot_singleton.connect()
    while True:
        robot_singleton.open_tool(0.65)
        response = input('Digite o valor do tamanho da tampa:\n')
        size_ = input('Digite o tamanho do corpo:\n')
        try:
            response = float(response)
            size_ = float(size_)
        except:
            break
        
        return_ = robot_singleton.close_tool(response, size_)

        if return_[0]:
            print('Object is identify', end='')
        else:
            print('Object is not identify', end='')

        print(f'\nthe last position is {return_[1]} and the max and min approach is {return_[2]}, {return_[3]}\n')
        time.sleep(0.5)

if __name__ == '__main__':
    gripper_move()
