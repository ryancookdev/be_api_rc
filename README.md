# SCOIR Technical Interview for Back-End Engineers
This repo contains an exercise intended for Back-End Engineers.

## Instructions
1. Fork this repo.
1. Using technology of your choice, complete [the assignment](./Assignment.md).
1. Update this README with
    * a `How-To` section containing any instructions needed to execute your program.
    * an `Assumptions` section containing documentation on any assumptions made while interpreting the requirements.
1. Before the deadline, submit a pull request with your solution.

## Expectations
1. Please take no more than 8 hours to work on this exercise. Complete as much as possible and then submit your solution.
1. This exercise is meant to showcase how you work. With consideration to the time limit, do your best to treat it like a production system.

## How-To
This project requires Python 3. To run the script:
```
mkdir input
cp sample-data/valid.csv input
python src/main.py
```
CTRL-C to kill the process

To see a full list of command line arguments:
`python src/main.py --help`.

## Assumptions
1. Non-csv input files should not cause errors and should not be deleted.
1. A file should not be processed more than once. But after it has been removed from the input folder, another file by the same name can be processed.
1. Need to be able to efficiently process a large number of files, which may contain a large number or records.
1. Need to be able to easily configure processing details (polling time, max thread count, etc).
1. Need to be able to run the program with and without log output.
1. This script will be run in a POSIX environment with Python 3 installed.
