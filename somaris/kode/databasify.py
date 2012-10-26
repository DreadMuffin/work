#!/usr/bin/python

import os

source = "fprotokoller/"
dest = "dprotokoller/"

listing = os.listdir(source)

for file in listing:
    fields = open(source + file,'r').read().split("\n")
    output = []
    output.append("\'" + file[9:-7] + "\'")
    output.append("\'" + file[-6:-1] + "\'")
    output.append("\'" + fields[1][-5:] + "\'")
    length = 0
    for i in fields:
        if len(i) < 6:
            length += 1
    output.append(str(length))
    output.append("NOW()")

    f = open(dest + file,'w')
    f.write(','.join(output))
    print ','.join(output)
    f.close()




