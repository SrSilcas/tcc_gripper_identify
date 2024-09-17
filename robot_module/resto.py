def close_tool(self, cap_size: float = 0, body_size: float = 0) -> Union[
    tuple[bool, Any, Union[float, int], Union[float, int], int], tuple[
        bool, Union[int, Any], Union[float, int], Union[float, int], int]]:
    """
    This function close the gripper and try detected object

    Args:
        :param(float, optional) cap_size: size for cap of object in cm. Defaults to 0.
        :param(float, optional) body_size: size for body of object in cm. Defaults to 0.

    Returns:
        :return(bool) tuple[0]: whether an object was detected or not detected
        :return(float) tuple[1]: when gripper identify the object the third
        :return(float) tuple[2]: max approach calculate for this object and the
        :return(float) tuple[2]: min approach calculate for this object
    """
    self.currents = []
    self.have_medicine = False
    currents = []
    position = 0

    if cap_size != 0 and body_size != 0:

        max_approach = self.__calculate_size(cap_size)
        min_approach = self.__calculate_size(body_size) - 1
    else:

        max_approach = 94
        min_approach = 84

    if self.gripper_test:
        return True, self.attribute_from_gripper()['position'], max_approach, min_approach, len(self.currents)

    while not self.have_medicine and self.attribute_from_gripper()["position"] < max_approach:
        deviation = None
        average = None
        self.__close()
        first_current = self.attribute_from_gripper()["current_motor"]

        if 4 > first_current > 0:

            if len(currents) > 2:
                deviation = statistics.stdev(currents)
                average = statistics.mean(currents)
        else:

            print("atypical current")

        if deviation is not None and self.attribute_from_gripper()['position'] > min_approach:
            position = self.attribute_from_gripper()['position']
            if self.__verification(first_current, deviation, average):
                self.__close(have_medicine_=True)
                # thread = threading.Thread(target=self.confirmation)
                # thread.start()
                self.have_medicine = True

        if 4 > first_current > 0 and len(currents) < 7:
            currents.append(first_current)
            self.currents.append(first_current)

    return self.have_medicine, position, max_approach, min_approach, len(self.currents)


def __close(self, have_medicine_: bool = False) -> None:
    """
    This Function close the gripper

    Args:
        :param(bool, optional) have_medicine_: Already medicine inside the gripper. Defaults to False.

    Returns:
        :return None
    """
    gripper_command = Base_pb2.GripperCommand()
    finger = gripper_command.gripper.finger.add()
    gripper_command.mode = Base_pb2.GRIPPER_POSITION
    finger.finger_identifier = 1
    finger.value = self.__increment(have_medicine=have_medicine_)
    self.base.SendGripperCommand(gripper_command)