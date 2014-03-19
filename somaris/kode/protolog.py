#!/usr/bin/python

import os
import re

newfolder = "fprotokoller/"
oldfolder = "oldf/"

def loop():
    if os.getcwd()[-13:] == "/somaris/kode":
        os.system("date >> log.txt")
        os.system(">templog.txt")
        returnstring = ""
        news = os.listdir(newfolder)
        olds = os.listdir(oldfolder)
        for new in news:
            for old in olds:
                if new == old:
                    os.system("diff " + newfolder + new + " " +
                            oldfolder + old + " >> templog.txt")
                    continue
        os.system("cat templog.txt >> log.txt")

    else: print "Wrong dir"
loop()
