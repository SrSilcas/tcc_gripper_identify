import csv
import time
from robot_module import robot_singleton
from robot_module import write_into_txt


def write_into_csv(dates, csv_name):
    with open(csv_name, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dates)


if __name__ == '__main__':
    csv_name = '.csv'
    robot = robot_singleton()
    robot.connect()
    write_into_csv(('response', 'position', 'deviation', 'average'), csv_name)
    count = 0
    while count < 100:
        robot.open_tool(0.6)
        identification, position, deviation, average = robot.close_tool()
        write_into_csv((identification, position, deviation, average), csv_name)
        count += 1
