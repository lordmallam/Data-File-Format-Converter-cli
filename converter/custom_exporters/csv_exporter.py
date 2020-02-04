import csv
from datetime import datetime

def csv_exporter(data, folder):
    file_name = f'{folder}/trivago-{datetime.today().strftime("%Y-%m-%d-%H-%M-%S")}.csv'
    with open(file_name, 'w') as csv_file:
        props = []
        csv_writer = csv.writer(csv_file)
        for item in data:
            if not len(props):
                props = item.keys()
                csv_writer.writerow(props)
            csv_writer.writerow(item.values())
    return file_name