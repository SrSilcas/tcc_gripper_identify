from robot_module import robot_singleton
from robot_module import write_into_json
if __name__ == '__main__':
    robot_singleton.connect()
    pegou = 0
    nao_pegou = 0
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
    robot_singleton.move_cartesian((0.04378148168325424, -0.6268088221549988, 0.13101805746555328, 91.06903076171875,
                                    178.91331481933594, 33.849117279052734))
    robot_singleton.close_tool()
    # recuo a cima medicine 6 cartisian
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
    robot_singleton.move_cartesian((0.2849084436893463, -0.48072537779808044, 0.2754789888858795, 91.1758804321289,
                                   178.0609130859375, 31.485599517822266))
    robot_singleton.close_tool()

    # Confirmation aruco Medicine 4 Joints
    robot_singleton.move_joints((284.7580261230469, 291.52734375, 128.84234619140625, 69.89837646484375,
                                 252.2189178466797, 265.07275390625))
    # Rotation End efactor 4 Joints
    robot_singleton.move_joints((284.7580261230469, 291.52734375, 128.84234619140625, 69.89837646484375,
                                 252.2189178466797, 265.07275390625+180))
    # Get Medicine 4 Carisian
    robot_singleton.move_cartesian((0.28177502751350403, -0.4811064302921295, 0.1223825067281723, 91.19490814208984,
                                   179.0008544921875, 33.90068435668945))
    robot_singleton.close_tool()

    # Confirmation aruco Medicine 2 Joints
    robot_singleton.move_joints((351.6455078125, 294.0829162597656, 109.09567260742188, 137.81268310546875,
                                 272.2818908691406, 267.0229187011719))
    # Rotation End efactor 2 Joints
    robot_singleton.move_joints((351.6455078125, 294.0829162597656, 109.09567260742188, 137.81268310546875,
                                 272.2818908691406, 267.0229187011719+180))
    # Get Medicine 2 Carisian
    robot_singleton.move_cartesian((0.5183528065681458, -0.32973045110702515, 0.12836343050003052, 90.84122467041016,
                                    179.36619567871094, 33.870208740234375))
    robot_singleton.close_tool()

    # Confirmation aruco Medicine 1 Joints
    robot_singleton.move_joints((352.14984130859375, 324.2068786621094, 115.96524047851562, 141.47735595703125,
                                 287.5470275878906, 248.85435485839844))
    # Rotation End efactor 1 Joints
    robot_singleton.move_joints((352.14984130859375, 324.2068786621094, 115.96524047851562, 141.47735595703125,
                                 287.5470275878906, 248.85435485839844+180))
    # Get Medicine 1 Carisian
    robot_singleton.move_cartesian((0.514650285243988, -0.328733891248703, 0.2791138291358948, 90.5988540649414,
                                    179.53021240234375, 33.941680908203125))
    robot_singleton.close_tool()

    # Confirmation aruco Medicine 5 Joints
    robot_singleton.move_joints((241.27059936523438, 320.6772766113281, 87.35098266601562, 19.95086669921875,
                                 292.73077392578125, 321.035400390625))
    # Rotation End efactor 5 Joints
    robot_singleton.move_joints((241.27059936523438, 320.6772766113281, 87.35098266601562, 19.95086669921875,
                                 292.73077392578125, 321.035400390625+180))
    # Get Medicine 5 Carisian
    robot_singleton.move_cartesian((0.04481153190135956, -0.6291782259941101, 0.2726109027862549, 92.64905548095703,
                                    -179.89691162109375, 30.28757095336914))
    robot_singleton.close_tool()

    # for i in range(1, 101):
    #     pegou_ = robot_singleton.close_tool()
    #     robot_singleton.open_tool(0.60)
    #     if pegou_:
    #         pegou += 1
    #     else:
    #         nao_pegou += 1
    # # for i in range(1, 11):
    # #     list_destruction = robot_singleton.close_destruction()
    # #     dict_destruction[i] = list_destruction
    # #     robot_singleton.open_tool()
    # print("Não pegou ", nao_pegou)
    # print("Pegou ", pegou)
