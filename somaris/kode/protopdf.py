#!/usr/bin/python

import re
import os

path = "tprotokoller/"
path2 = "pdf/"
listing = os.listdir(path)
for file in listing:
    os.system("pdflatex -output-directory " + path2 + " " + path + file)
