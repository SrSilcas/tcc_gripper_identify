from robot_module import robot_singleton
from robot_module import write_into_txt
if __name__ == '__main__':
    robot_singleton.connect()
    quadrante_1_joints = (117.713623046875, 294.66815185546875, 114.90582275390625, 276.2258605957031, 91.80364990234375, 90.01412963867188)
    quadrante_1_r1_grap = (-0.2827180325984955, 0.5357759594917297, 0.13340722024440765, -91.10689544677734, 179.8590545654297, 21.494564056396484)
    quadrante_1_r1_conf = (-0.2497715950012207, 0.43256765604019165, 0.1189563050866127, -91.38507080078125, 179.9244842529297, 21.491079330444336)
    quadrante_1_r2_grap = (-0.2824910879135132, 0.5355659127235413, 0.2912922203540802, -90.83451080322266, 179.82095336914062, 21.4840164184570)
    quadrante_1_r2_conf = (-0.24945518374443054, 0.43237927556037903, 0.2752854824066162, -91.14674377441406, 179.88165283203125, 21.475603103637695)

    pegou = 0
    nao_pegou = 0
    results = f""
    for i in range(1, 51):
        pegou_ = robot_singleton.close_tool()
        print(pegou_)
        current_affter = robot_singleton.atribue_from_gripper()['current_motor']
        position_after = robot_singleton.atribue_from_gripper()['position']
        robot_singleton.open_tool(0.60)
        if pegou_:
            pegou += 1
        else:
            nao_pegou += 1
        result = f"Rotation: {i}\n     {pegou_}\n     Current_mottor: {current_affter}\n     Position: {position_after}\n"
        results += result
        print(i)
    write_into_txt(results, "text_main_0.296_94.5")
    print("Não pegou ", nao_pegou)
    print("Pegou ", pegou)
