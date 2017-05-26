#!/usr/bin/env python
from subprocess import call
import sys
import time

def run_cyclus(num_inp_files):
    for i in range(num_inp_files):
        call("cyclus %s.json -o %s.sqlite > out_serial_%s.log" % \
                (str(i), str(i), str(i)), shell=True)

if __name__ == "__main__":
    start = time.time()
    run_cyclus(int(sys.argv[1]))
    print(time.time() - start)

