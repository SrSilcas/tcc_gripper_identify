import pandas as pd

read = pd.read_csv('tests\\tests_medications_with_35_csv\\dexametasona_overall_2024_03_05.csv')
read1 = pd.read_csv('tests\\tests_medications_with_35_csv\\dipirona_overall_2024_03_05.csv')
read2 = pd.read_csv('tests\\tests_medications_with_35_csv\\hypocaina_overall_2024_03_05.csv')
read3 = pd.read_csv('tests\\tests_medications_with_35_csv\\medicamento_fake_overall_2024_03_05.csv')
read4 = pd.read_csv('tests\\tests_medications_with_35_csv\\tigeciclina_overall_2024_03_05.csv')
read5 = pd.read_csv('tests\\tests_medications_with_35_csv\\colistemato_overall_2024_03_05.csv')
read6 = pd.read_csv('tests\\tests_medications_with_35_csv\\estructor_18_1_overall_2024_03_05.csv')
read7 = pd.read_csv('tests\\tests_medications_with_35_csv\\estructor_21_overall_2024_03_05.csv')
read8 = pd.read_csv('tests\\tests_medications_with_35_csv\\estructor_23_overall_2024_03_05.csv')
read9 = pd.read_csv('tests\\tests_medications_with_35_csv\\estructor_24_overall_2024_03_05.csv')
read10 = pd.read_csv('tests\\tests_medications_with_35_csv\\estructor_25_overall_2024_03_05.csv')
read11 = pd.read_csv('tests\\tests_medications_with_35_csv\\estructor_36_5_overall_2024_03_05.csv')

print('DEXAMETASONA')
print(read.describe())
print('\n')

print('DIPIRONA')
print(read1.describe())
print('\n')

print('HYPOCAINA')
print(read2.describe())
print('\n')

print('MEDICAMENTO_FAKE')
print(read3.describe())
print('\n')

print('TIGECICLINA')
print(read4.describe())

print('COLISTEMATO')
print(read5.describe())

print('ESTRUCTOR 18.1')
print(read6.describe())

print('ESTRUCTOR 21')
print(read7.describe())

print('ESTRUCTOR 23')
print(read8.describe())

print('ESTRUCTOR 24')
print(read9.describe())

print('ESTRUCTOR 25')
print(read10.describe())

print('ESTRUCTOR 36.5')
print(read11.describe())

