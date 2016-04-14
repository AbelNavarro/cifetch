#!/usr/bin/python

import argparse


def main():
    parser = argparse.ArgumentParser(description='cifetch - supportconfig fetcher from ci.suse.de')
    args = parser.parse_args()

    print "done."

if __name__ == '__main__':
    main()
