import argparse
import csv
import json
import multiprocessing
import os
import time
from UniqueQueue import UniqueQueue
from Person import Person

parser = argparse.ArgumentParser(description='Convert CSV to JSON')
parser.add_argument('-i', '--input-dir', default='input',
                    help='Name of the input directory')
parser.add_argument('-o', '--output-dir', default='output',
                    help='Name of the output directory')
parser.add_argument('-e', '--error-dir', default='error',
                    help='Name of the error directory')
parser.add_argument('-p', '--polling', type=int, default=10,
                    help='Delay in seconds for polling the input directory')
parser.add_argument('-w', '--workers', type=int, default=1,
                    help='Number of workers for processing input files')
parser.add_argument('-v', '--verbosity', action='store_true',
                    help='Print processing steps')
args = parser.parse_args()

queue = UniqueQueue()

def main():
    verify_directories()
    create_workers()
    while True:
        load_queue()
        time.sleep(args.polling)


def verify_directories():
    if not os.path.exists(args.input_dir):
        raise Exception(f"Input directory '{args.input_dir}' does not exist")
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    if not os.path.exists(args.error_dir):
        os.makedirs(args.error_dir)


def create_workers():
    log(f'Creating {args.workers} worker(s)')
    for i in range(args.workers):
        w = multiprocessing.Process(target=worker, args=(queue, )) 
        w.start()


def worker(queue):
    while True:
        if queue.empty():
            time.sleep(2)
            continue
        filename = queue.get()
        log(f'Processing: {filename}')
        result = process_csv_file(filename)
        people = result[0]
        errors = result[1]
        if len(people):
            write_json_file(filename, people)
        if len(errors):
            write_error_file(filename, errors)
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
    people = []
    errors = []
    with open(os.path.join(args.input_dir, filename)) as csv_file:
        reader = csv.DictReader(csv_file)
        row_id = 0
        for row in reader:
            row_id += 1
            try:
                person = Person(
                    row['INTERNAL_ID'],
                    row['FIRST_NAME'],
                    row['MIDDLE_NAME'],
                    row['LAST_NAME'],
                    row['PHONE_NUM'])
                people.append(person)
            except Exception as e:
                errors.append((row_id, e))
    return (people, errors)


def write_json_file(filename, people):
    json_filename = filename.replace('.csv', '.json')
    with open(os.path.join(args.output_dir, json_filename), 'w') as json_file:
        people_json = []
        for person in people:
            person_json = {}
            person_json['id'] = person.internal_id
            person_json['name'] = {}
            person_json['name']['first'] = person.first_name
            if person.middle_name:
                person_json['name']['middle'] = person.middle_name
            person_json['name']['last'] = person.last_name
            person_json['phone'] = person.phone
            people_json.append(person_json)
        json_file.write(json.dumps(people_json, indent=4))


def write_error_file(filename, errors):
    with open(os.path.join(args.error_dir, filename), 'w') as error_file:
        writer = csv.writer(error_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for error in errors:
            row_number = error[0]
            error_message = error[1]
            writer.writerow([row_number, error_message])


def log(message):
    if args.verbosity:
        print(message)


if __name__ == "__main__":
    main()
