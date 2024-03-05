import csv
import time
import statistics
from robot_module import robot_singleton


def write_into_csv(dates, csv_name):
    with open(csv_name, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dates)


if __name__ == '__main__':

    csv_overall_name = 'tests_medications_with_35_csv\\tigeciclina_overall_2024_03_05.csv'
    csv_statistics_name = 'tests_medications_with_35_csv\\tigeciclina_statistics_2024_03_05.csv'

    robot = robot_singleton
    robot.connect()

    try:
        arqv = open(csv_overall_name)
        arqv.close()

    except:
        write_into_csv(('response', 'position', 'deviation', 'average'), csv_overall_name)
    
    try:
        arqv = open(csv_statistics_name)
        arqv.close()

    except:
        write_into_csv(('P deviation', 'P average', 'P median', 'D deviation', 'D average',
                        'D median', 'A deviation', 'A average', 'A median'), csv_statistics_name)
    
    count = 0
    positions = []
    deviations = []
    averages = []

    while count < 100:
        robot.open_tool(0.65)

        time.sleep(1)
        if count == 50:
            print('METADE')
        
        identification, position, deviation, average = robot.close_tool()
        
        write_into_csv((identification, position, deviation, average), csv_overall_name)
                
        positions.append(position)
        deviations.append(deviation)
        averages.append(average)
        time.sleep(0.5)
        count += 1

    p_deviation = statistics.stdev(positions)
    p_average = statistics.mean(positions)
    p_median = statistics.median(positions)

    d_deviation = statistics.stdev(deviations)
    d_average = statistics.mean(deviations)
    d_median = statistics.median(deviations)

    a_deviation = statistics.stdev(averages)
    a_average = statistics.mean(averages)
    a_median = statistics.median(averages)

    write_into_csv((p_deviation, p_average, p_median, d_deviation, d_average,
                    d_median, a_deviation, a_average, a_median),
                   csv_statistics_name)

    robot.open_tool(0.65)
    print('Acabou')
