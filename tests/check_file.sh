#!/bin/bash

f=$1
f1=$2
f2=$3

if [[ "$f" == *.h5 ]]; then
    python ../../check_h5.py $f1 $f2 -t 1e-20
elif [[ "$f" == *.dat ]]; then
    python ../../check_dat.py $f1 $f2 -t 1e-20
elif [[ "$f" == *.petsc ]]; then
    python ../../check_petsc.py $f1 $f2 -t 1e-20
elif [[ "$f" == *.png ]]; then
    exit
else
    diff $f1 $f2
fi
