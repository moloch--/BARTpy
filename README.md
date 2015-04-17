BARTpy
========

Python bindings for the BART API


Usage
==========
```
./cli-bart.py --station 19th
```

Example Script
==============
```
from BART import BART

bart = BART()
for train in bart["24th"]:
    print "%d car train in %s" % (len(train), train.minutes)

for train in bart["24th"]["Richmond"]:
    print "%d car train in %s" % (len(train), train.minutes)

```