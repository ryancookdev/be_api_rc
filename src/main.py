import argparse
import csv
import os
import time
import threading
from domain.Person import Person
from domain.UniqueQueue import UniqueQueue

queue = UniqueQueue()

def main():
    args = get_args()

    max_threads = 5
    for i in range(max_threads):
        print(f'Creating {max_threads} thread(s)')
        t = threading.Thread(target=worker)
        t.setDaemon(True)
        t.start()

    while True:
        print('Loading queue. Initial size: ' + str(queue.qsize()))
        files = [f for f in os.listdir(args.input_dir)]
        for file in files:
            queue.put(os.path.join(args.input_dir, file))
            print(f'Added to queue: {file}')
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
        process_input_file(filename)
        queue.task_done(filename)


def process_input_file(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # skip header
        for row in csv_reader:
            person = Person(row[0], row[1], row[2], row[3], row[4])
        time.sleep(1)

    # TODO: validate input dir exists
    # TODO: validate file ends with .csv
    # TODO: create output/error if they don't exist


def get_args():
    parser = argparse.ArgumentParser(description='Convert CSV to JSON')
    parser.add_argument('-i', '--input-dir', default='input', help='Name of the input directory')
    parser.add_argument('-o', '--output-dir', default='output', help='Name of the output directory')
    parser.add_argument('-e', '--error-dir', default='error', help='Name of the error directory')
    parser.add_argument('-w', '--wait', type=int, default=15, help='Name of the error directory')
    # TODO: validate arguments
    return parser.parse_args()


if __name__ == "__main__":
    main()
