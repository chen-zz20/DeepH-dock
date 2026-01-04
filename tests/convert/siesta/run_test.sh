#!/bin/bash

script_path=$(realpath $(dirname $0))
script_relative_path=$(echo $script_path | awk -F'/examples/' '{print $2}')

rm -rf deeph

echo "[do] Running commands in ${script_relative_path} ..."
dock convert siesta to-deeph siesta.bak deeph -t 0 -p 1
sleep 1
echo "[done] Running commands"

echo "[do] Checking ..."
for d1 in $(ls deeph); do
  for f in $(ls deeph/$d1); do
    bash ../../check_file.sh $f deeph/$d1/$f deeph.bak/$d1/$f
  done
done
echo "[done] Checking"
