#!/bin/bash

script_path=$(realpath $(dirname $0))
script_relative_path=$(echo $script_path | awk -F'/examples/' '{print $2}')

rm -rf petsc

echo "[do] Running commands in ${script_relative_path} ..."
dock convert hopcp from-deeph deeph.bak petsc -t 0 -p 1
sleep 1
echo "[done] Running commands"

echo "[do] Checking ..."
for d1 in $(ls petsc); do
  for f in $(ls petsc/$d1); do
    bash ../../check_file.sh $f petsc/$d1/$f petsc.bak/$d1/$f
  done
done
echo "[done] Checking"
