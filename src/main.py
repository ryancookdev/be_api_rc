import argparse
import os
import time

def main():
    args = get_args()

    process_queue = []
    while 1:
        files = [f for f in os.listdir(args.input_dir)]
        time.sleep(args.wait)

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
