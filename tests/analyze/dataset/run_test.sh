#!/bin/bash

script_path=$(realpath $(dirname $0))
script_relative_path=$(echo $script_path | awk -F'/examples/' '{print $2}')

rm -rf inputs
cp -r inputs.clean inputs

echo "[do] Running commands in ${script_relative_path} ..."
dock analyze dataset edge inputs -t 0 -p 4
sleep 1
dock analyze dataset split inputs -t 0 -p 4
sleep 1
echo "[done] Running commands"

echo "mv dataset_split.json inputs/dataset_split.json"
mv dataset_split.json inputs/dataset_split.json

echo "[do] Checking ..."
for f in $(ls inputs.bak); do
  bash ../../check_file.sh $f inputs/$f inputs.bak/$f
done
echo "[done] Checking"
