#!/bin/bash

for i in `seq 0 $1`; do
    cyclus $i.json -o $i.sqlite > out_$i.log
done

