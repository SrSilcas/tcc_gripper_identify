from sklearn.linear_model import LinearRegression
import math

class utils:

    SIZES = {
        'medicamento_fake': (1.40, 87.03, 90.86),
        'hypocaina': (0.85, 90.80, 93.97),
        'dipirona': (0.8, 90.72, 93.82),
        'dexametasona': (0.8, 90.79, 93.85),
        'tigeciclina': (1.50, 86.76, 90.75),
    }
        # 'colistemato': (2.25, , ),


    def cauculate_approach(size_medicine):
        x = [size[0] for size in utils.SIZES.values()]
        y = [opened[2] for opened in utils.SIZES.values()]

        model = LinearRegression()
        model.fit([[size] for size in x], y) 
        prevision = model.predict([[size_medicine]])
        print(prevision)



if __name__ == '__main__':
    utils.cauculate_approach(2.25)
