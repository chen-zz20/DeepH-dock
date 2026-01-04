#!/bin/bash

script_path=$(realpath $(dirname $0))
script_relative_path=$(echo $script_path | awk -F'/examples/' '{print $2}')

rm -rf eigen
cp -r eigen.clean eigen

echo "[do] Running commands in ${script_relative_path} ..."
for d1 in $(ls eigen); do
  dock compute eigen find-fermi eigen/$d1 -d 0.1 -p 16
  dock compute eigen calc-dos eigen/$d1 -d 0.03 --energy-window -2.0 2.0 --energy-num 1000 -s 0.04 -p 16
  dock compute eigen calc-band eigen/$d1 -p 16
  dock compute eigen plot-band eigen/$d1 --energy-window -2.0 2.0
done
sleep 1
echo "[done] Running commands"

echo "[do] Checking ..."
for d1 in $(ls eigen); do
  for f in $(ls eigen/$d1); do
    bash ../../check_file.sh $f eigen/$d1/$f eigen.bak/$d1/$f
  done
done
echo "[done] Checking"
