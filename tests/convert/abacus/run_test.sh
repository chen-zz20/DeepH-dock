#!/bin/bash

script_path=$(realpath $(dirname $0))
script_relative_path=$(echo $script_path | awk -F'/examples/' '{print $2}')

rm -rf deeph_data

echo "[do] Running commands in ${script_relative_path} ..."
dock convert abacus to-deeph abacus_data deeph_data -t 0 -p 2
sleep 1
echo "[done] Running commands"

echo "[do] Checking ..."
for d1 in $(ls deeph_data); do
  for f in $(ls deeph_data/$d1); do
    bash ../../check_file.sh $f deeph_data/$d1/$f deeph_data.bak/$d1/$f
  done
done
echo "[done] Checking"
