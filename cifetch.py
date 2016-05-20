#!/usr/bin/python

import argparse
import os
import urllib2
import ssl
import zipfile
import glob


# which-like function, copied from http://stackoverflow.com/a/377028/1753665
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


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

    # .artifacts is hard to spot, use a symlink
    artifacts_dir = directory + "/.artifacts"
    artifacts_lnk = directory + "/artifacts"
    if not os.path.exists(artifacts_lnk):
        os.symlink(artifacts_dir, artifacts_lnk)

    # uncompress all tarballs (bz2)
    for bz2file in glob.glob(artifacts_dir + "/*.tbz"):
        print bz2file
        os.system("tar jxvf " + bz2file + " --directory " + artifacts_dir)
    
    # if split-supportconfig is in the path, split all pluging openstack files
    if which('split-supportconfig') is not None:
        print "we can use split-supportconfig"
        prev_dir = os.getcwd()
        for root, dirs, files in os.walk(artifacts_dir):
            for file in files:
                if file == "plugin-suse_openstack_cloud.txt":
                    os.chdir(root)
                    os.system("split-supportconfig " + file)

        os.chdir(prev_dir)



if __name__ == '__main__':
    main()
