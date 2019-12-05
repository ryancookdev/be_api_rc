import argparse
import csv
import json
import os
import time
import threading
from domain.Person import Person
from domain.UniqueQueue import UniqueQueue

parser = argparse.ArgumentParser(description='Convert CSV to JSON')
parser.add_argument('-i', '--input-dir', default='input', help='Name of the input directory')
parser.add_argument('-o', '--output-dir', default='output', help='Name of the output directory')
parser.add_argument('-e', '--error-dir', default='error', help='Name of the error directory')
parser.add_argument('-w', '--wait', type=int, default=15, help='Name of the error directory')
args = parser.parse_args()
# TODO: validate arguments

queue = UniqueQueue()
max_threads = 5

def main():
    for i in range(max_threads):
        print(f'Creating {max_threads} thread(s)')
        t = threading.Thread(target=worker)
        t.setDaemon(True)
        t.start()

    while True:
        print('Loading queue. Initial size: ' + str(queue.qsize()))
        filenames = [f for f in os.listdir(args.input_dir)]
        for filename in filenames:
            queue.put(filename)
            print(f'Added to queue: {filename}')
        print('Queue loaded. Size: ' + str(queue.qsize()))
        time.sleep(args.wait)


def worker():
    while True:
        if queue.empty():
            print('Waiting for work...')
            time.sleep(2)
            continue
        filename = queue.get()
        print(f'Worker processing: {filename}')
        json = process_csv_file(filename)
        write_json_file(filename, json)
        queue.task_done(filename)


def process_csv_file(filename):
    # TODO: validate input dir exists
    # TODO: validate file ends with .csv
    # TODO: create output/error if they don't exist

    data = []
    with open(os.path.join(args.input_dir, filename)) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # person = Person(row['INTERNAL_ID'], row['FIRST_NAME'], row['MIDDLE_NAME'], row['LAST_NAME'], row['PHONE_NUM'])
            person = {}
            person['id'] = row['INTERNAL_ID']
            person['name'] = {}
            person['name']['first'] = row['FIRST_NAME']
            person['name']['middle'] = row['MIDDLE_NAME']
            person['name']['last'] = row['LAST_NAME']
            person['phone'] = row['PHONE_NUM']
            data.append(person)
    return data


def write_json_file(filename, data):
    with open(os.path.join(args.output_dir, filename), 'w') as json_file:
        json_file.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
