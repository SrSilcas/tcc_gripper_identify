from sklearn.linear_model import LinearRegression
import math

class Utils:

    SIZES = {
        1.40: 90.86,
        0.85: 93.97,
        0.8: 93.82,
        1.50: 90.75,
        2.25: 83.19,
        3.65: 74.84,
        2.5: 79.74,
        2.4: 80.80,
        2.1: 83.77,
        1.81: 86.42,
    }
       
    def calculate_approach(size_)-> float:
        """
        This function utilize linear regression for calculate with the size
        who much the gripper close for this size

        Args:
            size_ (float): size for object

        Returns:
            float: quantity for gripper close
        """
        if size_ in Utils.SIZES.keys():
            return Utils.SIZES[size_]

        x = [size for size in Utils.SIZES.keys()]
        y = [opened for opened in Utils.SIZES.values()]

        model = LinearRegression()
        model.fit([[size] for size in x], y) 
        prevision = model.predict([[size_]])
        return prevision.min().__round__(2)



if __name__ == '__main__':
    print(Utils.calculate_approach(2.2))
