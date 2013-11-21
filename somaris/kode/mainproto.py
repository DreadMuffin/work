#!/usr/bin/python

import re
import os
"""Executes all the scripts, needed to create the pdfs"""
execfile("cleanup.py")
execfile("xmlfolder.py")
execfile("protoscript34.py")
execfile("fieldsaligner.py")
execfile("protoscript56.py")
execfile("prototexfolder.py")
execfile("databasify.py")
execfile("protodb.py")
execfile("protopdf.py")

os.system("cp pdf/* /var/www/protocols/pdf")


