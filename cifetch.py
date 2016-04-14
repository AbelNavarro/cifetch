#!/usr/bin/python

import argparse
import os
import urllib2
import ssl
import zipfile


def main():
    parser = argparse.ArgumentParser(description='cifetch - supportconfig fetcher from ci.suse.de')
    parser.add_argument('build_number', type=int, help="Build number, i.e. 28945")
    args = parser.parse_args()

    print "build_number: {}".format(args.build_number)

    # If the directory already created for this build?
    directory = "/home/abel/work/ci.suse.de/{}".format(args.build_number)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print "created directory: " + directory

    # Is the zip file already downloaded?
    filepath = directory + "/artifacts.zip"
    if os.path.isfile(filepath):
        print "file was already downloaded"
 
    else:
        # Download file
        url = "https://ci.suse.de/job/openstack-mkcloud/{}/artifact/.artifacts/*zip*/.artifacts.zip".format(args.build_number)
        print "url: " + url
 
        context = ssl._create_unverified_context()       
        fileurl = urllib2.urlopen(url, context=context)
        with open(filepath, 'wb') as output:
            output.write(fileurl.read())
 
    # Unzip file regardless of previous content
    zipfile.ZipFile(filepath).extractall(directory)
    print "Unziped file."

    os.symlink(directory + "/.artifacts", directory + "/artifacts")


if __name__ == '__main__':
    main()
