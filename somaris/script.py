#!/usr/bin/python

FILE = "PETCT_WholeBody.MlAdult"


f = open(FILE,'r')
data = f.read()
data = data.split("\n")

for i in data:
    if "ReconTaskNumber" in i:
        print i
