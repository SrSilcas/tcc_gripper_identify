from robot_module import robot_singleton

if __name__ == '__main__':
    robot_singleton.connect()
    pegou = 0
    nao_pegou = 0
    robot_singleton.move_joints([355.457763671875, 343.3833923339844, 42.44935607910156, 19.35491943359375, 58.05247497558594, 142.64401245117188])
    robot_singleton.move_cartesian([0.507779598236084, -0.3307042121887207, 0.5863333344459534, 91.85260772705078, -178.6480712890625, 32.224884033203125])
    robot_singleton.close_tool()
    robot_singleton.move_cartesian([0.499779598236084, -0.3107042121887207, 0.6123333344459534, 91.85260772705078, -178.6480712890625, 32.224884033203125])
    robot_singleton.move_cartesian([0.431779598236084, -0.1827042121887207, 0.6123333344459534, 91.85260772705078, -178.6480712890625, 32.224884033203125])
    # Novas
    # Position center for all medicine Joints
    robot_singleton.move_joints((265.6274108886719, 336.42291259765625, 149.8004150390625, 51.673675537109375,
                                273.62615966796875, 275.03228759765625))
    # Confirmation aruco Medicine 6 Joints
    robot_singleton.move_joints((239.69277954101562, 292.425537109375, 78.48074340820312, 22.57049560546875,
                                 282.9630432128906, 302.03717041015625))
    # Rotation End efactor 6 Joints
    robot_singleton.move_joints((239.69277954101562, 292.425537109375, 78.48074340820312, 22.57049560546875,
                                 282.9630432128906, 302.03717041015625+180))
    # Get Medicine 6 Carisian
    robot_singleton.move_cartesian((0.039432115852832794, -0.6257391571998596, 0.14494134485721588, 91.02909851074219, 178.90126037597656, 32.69298553466797))
    robot_singleton.close_tool()
    # recuo a cima medicine 6 cartisian

    robot_singleton.move_cartesian((0.039432115852832794-0.008, -0.6257391571998596+0.02, 0.14494134485721588+0.026, 91.02909851074219, 178.90126037597656, 32.69298553466797))
    robot_singleton.move_cartesian((0.04378148168325424 - 0.008, -0.6268088221549988 + 0.02, 0.13101805746555328 + 0.026, 91.06903076171875,
                                    178.91331481933594, 33.849117279052734))
    # recuo dentro medicine 6 cartisian
    robot_singleton.move_cartesian((0.04378148168325424 - 0.066, -0.6268088221549988 + 0.12, 0.13101805746555328 + 0.026, 91.06903076171875,
                                    178.91331481933594, 33.849117279052734))
    vari = robot_singleton.get_joint_angles()
    vari[0] = 327.17
    robot_singleton.move_joints(vari)
    # drop safe all medicine
    robot_singleton.move_joints((5.2446136474609375, 320.358642578125, 53.3184814453125, 271.3430480957031,
                                283.6111145019531, 359.119873046875))
    # drop all medicine
    robot_singleton.move_joints((0.9397430419921875, 299.651123046875, 49.955322265625, 272.50164794921875,
                                 300.5532531738281, 354.0183410644531))
    # open actuator
    robot_singleton.open_tool()

    # Position center for all medicine Joints
    robot_singleton.move_joints((265.6274108886719, 336.42291259765625, 149.8004150390625, 51.673675537109375,
                                273.62615966796875, 275.03228759765625))

    # Confirmation aruco Medicine 3 Joints
    robot_singleton.move_joints((285.48297119140625, 337.38861083984375, 133.25234985351562, 72.80349731445312,
                                 291.7298583984375, 278.9075927734375))
    # Rotation End efactor 3 Joints
    robot_singleton.move_joints((285.48297119140625, 337.38861083984375, 133.25234985351562, 72.80349731445312,
                                 291.7298583984375, 278.9075927734375+180))
    # Get Medicine 3 Carisian
    robot_singleton.move_cartesian((0.2772725224494934, -0.4790757894515991, 0.2895619571208954, 91.17072296142578, 178.04049682617188, 31.513904571533203))
    robot_singleton.close_tool()
    robot_singleton.move_cartesian((0.2772725224494934-0.008, -0.4790757894515991+0.02, 0.2895619571208954+0.024, 91.17072296142578, 178.04049682617188, 31.513904571533203))

    # Confirmation aruco Medicine 4 Joints
    robot_singleton.move_joints((284.7580261230469, 291.52734375, 128.84234619140625, 69.89837646484375,
                                 252.2189178466797, 265.07275390625))
    # Rotation End efactor 4 Joints
    robot_singleton.move_joints((284.7580261230469, 291.52734375, 128.84234619140625, 69.89837646484375,
                                 252.2189178466797, 265.07275390625+180))
    # Get Medicine 4 Carisian
    robot_singleton.move_cartesian((0.2781125605106354, -0.48251789808273315, 0.13842077553272247, 91.20516204833984, 179.04310607910156, 33.878089904785156))
    robot_singleton.close_tool()
    robot_singleton.move_cartesian((0.2781125605106354-0.008, -0.48251789808273315+0.02, 0.13842077553272247+0.024, 91.20516204833984, 179.04310607910156, 33.878089904785156))

    # Confirmation aruco Medicine 2 Joints
    robot_singleton.move_joints((351.6455078125, 294.0829162597656, 109.09567260742188, 137.81268310546875,
                                 272.2818908691406, 267.0229187011719))
    # Rotation End efactor 2 Joints
    robot_singleton.move_joints((351.6455078125, 294.0829162597656, 109.09567260742188, 137.81268310546875,
                                 272.2818908691406, 267.0229187011719+180))
    # Get Medicine 2 Carisian
    robot_singleton.move_cartesian((0.5072227716445923, -0.33957362174987793, 0.1415267139673233, 90.7174301147461, 178.65203857421875, 29.21040916442871))
    robot_singleton.close_tool()
    robot_singleton.move_cartesian((0.5115960836410522-0.008, -0.33078816533088684+0.02, 0.13798482716083527+0.024, 90.91927337646484, 179.27720642089844, 31.586959838867188))

    # Confirmation aruco Medicine 1 Joints
    robot_singleton.move_joints((352.14984130859375, 324.2068786621094, 115.96524047851562, 141.47735595703125,
                                 287.5470275878906, 248.85435485839844))
    # Rotation End efactor 1 Joints
    robot_singleton.move_joints((352.14984130859375, 324.2068786621094, 115.96524047851562, 141.47735595703125,
                                 287.5470275878906, 248.85435485839844+180))
    # Get Medicine 1 Carisian
    robot_singleton.move_cartesian((0.5113936066627502, -0.3306547999382019, 0.29217883944511414, 90.63101196289062, 179.57373046875, 31.22337532043457))
    robot_singleton.close_tool()
    robot_singleton.move_cartesian((0.5113936066627502-0.008, -0.3306547999382019+0.02, 0.29217883944511414+0.025, 90.63101196289062, 179.57373046875, 31.22337532043457))

    # Confirmation aruco Medicine 5 Joints
    robot_singleton.move_joints((241.27059936523438, 320.6772766113281, 87.35098266601562, 19.95086669921875,
                                 292.73077392578125, 321.035400390625))
    # Rotation End efactor 5 Joints
    robot_singleton.move_joints((241.27059936523438, 320.6772766113281, 87.35098266601562, 19.95086669921875,
                                 292.73077392578125, 321.035400390625+180))
    # Get Medicine 5 Carisian
    robot_singleton.move_cartesian((0.0392640084028244, -0.6235572695732117, 0.2889540195465088, 92.63505554199219, -175.43954467773438, 31.803190231323242))
    robot_singleton.close_tool()
    robot_singleton.move_cartesian((0.0392640084028244-0.008, -0.6235572695732117+0.02, 0.2889540195465088+0.024, 92.63505554199219, -175.43954467773438, 31.803190231323242))

    for i in range(1, 101):
        pegou_ = robot_singleton.close_tool()
        robot_singleton.open_tool(0.60)
        if pegou_:
            pegou += 1
        else:
            nao_pegou += 1
    # for i in range(1, 11):
    #     list_destruction = robot_singleton.close_destruction()
    #     dict_destruction[i] = list_destruction
    #     robot_singleton.open_tool()
    print("Não pegou ", nao_pegou)
    print("Pegou ", pegou)
