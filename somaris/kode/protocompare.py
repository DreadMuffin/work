#!/usr/bin/python

import os
import sys

file1 = sys.argv[1]
file2 = sys.argv[2]
path = "fprotokoller/"



os.system("diff -y --suppress-common-lines -w -i " + path + file1 + " " +
        path + file2 + " > foo.txt")








