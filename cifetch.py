#!/usr/bin/python

import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='cifetch - supportconfig fetcher from ci.suse.de')
    parser.add_argument('build_number', type=int, help="Build number, i.e. 28945")
    args = parser.parse_args()

    print "build_number: {}".format(args.build_number)

    # If the directory already created for this build?
    directory="/home/abel/work/ci.suse.de/{}".format(args.build_number)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Is the zip file already downloaded?

    # Unzip file regardless of previous content

if __name__ == '__main__':
    main()
