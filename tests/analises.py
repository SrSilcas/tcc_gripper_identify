import pandas as pd

read = pd.read_csv('tests\\tests_medications_with_35_csv\\dexametasona_overall_2024_03_05.csv')
read1 = pd.read_csv('tests\\tests_medications_with_35_csv\\dipirona_overall_2024_03_05.csv')
read2 = pd.read_csv('tests\\tests_medications_with_35_csv\\hypocaina_overall_2024_03_05.csv')
read3 = pd.read_csv('tests\\tests_medications_with_35_csv\\medicamento_fake_overall_2024_03_05.csv')
read4 = pd.read_csv('tests\\tests_medications_with_35_csv\\tigeciclina_overall_2024_03_05.csv')
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

