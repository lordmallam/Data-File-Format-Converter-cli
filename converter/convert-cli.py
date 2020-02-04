#! /usr/bin/env python
import argparse
from processor import Processor

def run(args):
    # ./files/input/Hotels_Case_Study_Python_role.csv
    # ./files/output
    p = Processor()
    p.convert(
        args.input,
        args.output,
        args.out_format,
        args.with_errors,
        args.errors_file
    )


def main():
    parser=argparse.ArgumentParser(description='Converts files from one format to another')
    parser.add_argument('-in', help='Input file to convert', dest='input', type=str, required=True)
    parser.add_argument('-out', help='Output folder (./path/to/dir)', dest='output', type=str, default='./files/output')
    parser.add_argument('-format', help='Format of output file', dest='out_format', type=str, default='json')
    parser.add_argument('-force', help='Force export with errors', dest='with_errors', type=bool, default=False)
    parser.add_argument('-error-file', help='File to write errors to', dest='errors_file', type=str, default='./files/output/errors.json')
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__=='__main__':
	main()
