#!/usr/bin/python

import re
import os


paths = ["fprotokoller/","pdf/","tprotokoller/","temppdf/","fejlkorsler/",
        "dprotokoller"]

"""In seperate line so it's easy to comment out"""
#paths.extend("protokoller4/","protokoller3/")

if os.getcwd()[-13:] == "/somaris/kode":
    """Empties all the directories in 'paths'. A check is made to ensure that
    I do not delete anything else due to being in another directory"""
    for path in paths:
        os.system("rm " + path + "*")
else:
    print "Currently in wrong directory"
