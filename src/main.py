import argparse
import csv
import json
import os
import time
# import threading
import multiprocessing
from domain.Person import Person
from domain.UniqueQueue import UniqueQueue

parser = argparse.ArgumentParser(description='Convert CSV to JSON')
parser.add_argument('-i', '--input-dir', default='input',
                    help='Name of the input directory')
parser.add_argument('-o', '--output-dir', default='output',
                    help='Name of the output directory')
parser.add_argument('-e', '--error-dir', default='error',
                    help='Name of the error directory')
parser.add_argument('-w', '--wait', type=int, default=15,
                    help='Delay in seconds for polling the input directory')
parser.add_argument('-t', '--threads', type=int, default=1,
                    help='Number of threads for processing input files')
parser.add_argument('-v', '--verbosity', action='store_true',
                    help='Print processing steps')
args = parser.parse_args()

queue = UniqueQueue()

def main():
    verify_directories()
    create_workers()
    while True:
        load_queue()
        time.sleep(args.wait)


def verify_directories():
    if not os.path.exists(args.input_dir):
        raise Exception(f"Input directory '{args.input_dir}' does not exist")
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    if not os.path.exists(args.error_dir):
        os.makedirs(args.error_dir)


def create_workers():
    log(f'Creating {args.threads} thread(s)')
    for i in range(args.threads):
        t = multiprocessing.Process(target=worker, args=(queue, )) 
        # t = threading.Thread(target=worker)
        t.start()


def worker(queue):
    while True:
        if queue.empty():
            log('Waiting for work...')
            time.sleep(2)
            continue
        filename = queue.get()
        log(f'Processing: {filename}')
        json = process_csv_file(filename)
        write_json_file(filename, json)
        os.remove(os.path.join(args.input_dir, filename))
        queue.task_done(filename)
        log(f'Completed: {filename}')


def load_queue():
    filenames = [f for f in os.listdir(args.input_dir)]
    for filename in filenames:
        if filename.endswith('.csv'):
            added = queue.put(filename)
            if added:
                log(f'Added to queue: {filename}')


def process_csv_file(filename):
    data = []
    with open(os.path.join(args.input_dir, filename)) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # TODO: validate CSV data
            # person = Person(row['INTERNAL_ID'], row['FIRST_NAME'], row['MIDDLE_NAME'], row['LAST_NAME'], row['PHONE_NUM'])
            person = {}
            person['id'] = row['INTERNAL_ID']
            person['name'] = {}
            person['name']['first'] = row['FIRST_NAME']
            if row['MIDDLE_NAME']:
                person['name']['middle'] = row['MIDDLE_NAME']
            person['name']['last'] = row['LAST_NAME']
            person['phone'] = row['PHONE_NUM']
            data.append(person)
    return data


def write_json_file(filename, data):
    json_filename = filename.replace('.csv', '.json')
    with open(os.path.join(args.output_dir, json_filename), 'w') as json_file:
        json_file.write(json.dumps(data, indent=4))


def log(message):
    if args.verbosity:
        print(message)


if __name__ == "__main__":
    main()
