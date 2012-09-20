#!/usr/bin/python

FILE = "PETCT_WholeBody.MlAdult"


f = open(FILE,'r')
data = f.read()
data = data.split("\n")

screens = {0 : dict()}
screenno = 0

for item in data:
    # Identify series
    if item.startswith("PROTOCOL_ENTRY_NO:"):
        screenno = item.split()[1]
        screens[screenno] = dict()
        continue

    try:
        screens[screenno][item.split()[0]] = item.split()[1]
    except:
        pass

print screens[0]
