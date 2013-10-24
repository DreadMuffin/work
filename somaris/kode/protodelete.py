#!/usr/bin/python
import re
import os

paths = ["PET3/","PET4/","PET5/","PET6/","PET26/"]

if os.getcwd()[-13:] == "/somaris/kode":
    """Empties all the directories in 'paths'. A check is made to ensure that
    I do not delete anything else due to being in another directory"""
    for path in paths:
        os.system("rm " + path + "* 2> /dev/null")
    print "Protocols deleted"
else:
    print "Currently in wrong directory"
