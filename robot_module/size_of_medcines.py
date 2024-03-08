from sklearn.linear_model import LinearRegression
import math

class utils:

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
       
    def cauculate_approach(size_medicine):
        if size_medicine in utils.SIZES.keys():
            return utils.SIZES[size_medicine]

        x = [size for size in utils.SIZES.keys()]
        y = [opened for opened in utils.SIZES.values()]

        model = LinearRegression()
        model.fit([[size] for size in x], y) 
        prevision = model.predict([[size_medicine]])
        return prevision.min().__round__(2)



if __name__ == '__main__':
    print(utils.cauculate_approach(2.2))
