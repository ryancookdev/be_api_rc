import argparse
import csv
import os
import time
from Domain.Person import Person

def main():
    args = get_args()

    process_queue = []
    while 1:
        files = [f for f in os.listdir(args.input_dir)]
        for file in files:
            process_input_file(os.path.join(args.input_dir, file))
        time.sleep(args.wait)


def process_input_file(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # skip header
        for row in csv_reader:
            person = Person(row[0], row[1], row[2], row[3], row[4])

    # TODO: validate input dir exists
    # TODO: validate file ends with .csv
    # TODO: create output/error if they don't exist


def get_args():
    parser = argparse.ArgumentParser(description='Convert CSV to JSON')
    parser.add_argument('-i', '--input-dir', default='input', help='Name of the input directory')
    parser.add_argument('-o', '--output-dir', default='output', help='Name of the output directory')
    parser.add_argument('-e', '--error-dir', default='error', help='Name of the error directory')
    parser.add_argument('-w', '--wait', type=int, default=10, help='Name of the error directory')
    # TODO: validate arguments
    return parser.parse_args()


if __name__ == "__main__":
    main()
