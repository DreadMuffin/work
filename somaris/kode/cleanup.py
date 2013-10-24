#!/usr/bin/python

import re
import os


paths = ["fprotokoller/","pdf/","tprotokoller/","temppdf/","fejlkorsler/",
        "dprotokoller/","fprotokoller34/"]

"""In seperate line so it's easy to comment out"""
paths.extend(["PET4noxml/","PET3noxml/","PET26noxml"])

if os.getcwd()[-13:] == "/somaris/kode":
    """Empties all the directories in 'paths'. A check is made to ensure that
    I do not delete anything else due to being in another directory"""
    for path in paths:
        os.system("rm " + path + "* 2> /dev/null")
    print "Deleted all temporary and final files"
else:
    print "Currently in wrong directory"
