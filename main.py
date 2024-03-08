from robot_module import robot_singleton

def gripper_move():
    robot_singleton.connect()
    while True:    
        response = input('Digite o valor do tamanho da tampa')
        size_ = input('Digite o tamanho do corpo')
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

        print(f'the last position is {return_[1]} and the max and min approach is {return_[2]}, {return_[3]}')

if __name__ == '__main__':
    gripper_move()
