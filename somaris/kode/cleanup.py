#!/usr/bin/python

import re
import os


paths = ["fprotokoller/","pdf/","tprotokoller/","temppdf/","fejlkorsler/","protokoller34/"]

if os.getcwd()[-13:] == "/somaris/kode":
    for path in paths:
        os.system("rm " + path + "*")
else:
    print "Currently in wrong directory"
