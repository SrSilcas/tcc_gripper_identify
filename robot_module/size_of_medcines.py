from sklearn.linear_model import LinearRegression
import math

class utils:

    SIZES = {
        1.40: (1.40, 87.03, 90.86),
        0.85: (0.85, 90.80, 93.97),
        0.8: (0.8, 90.72, 93.82),
        1.50: (1.50, 86.76, 90.75),
        2.25: (2.25, 80.98, 83.19),
        3.65: (3.65, 0, 74.84),
        2.5: (2.5, 0, 79.74),
        2.4: (2.4, 0, 80.80),
        2.1: (2.1, 0, 83.77),
        1.81: (1.81, 0, 86.42),
    }
       


    def cauculate_approach(size_medicine):
        if size_medicine in utils.SIZES.keys():
            return utils.SIZES[size_medicine][2]

        x = [size[0] for size in utils.SIZES.values()]
        y = [opened[2] for opened in utils.SIZES.values()]

        model = LinearRegression()
        model.fit([[size] for size in x], y) 
        prevision = model.predict([[size_medicine]])
        return prevision



if __name__ == '__main__':
    print(utils.cauculate_approach(2.25))
