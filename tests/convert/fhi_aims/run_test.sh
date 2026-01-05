#!/bin/bash

_pwd=$(pwd)
script_path=$(realpath $(dirname $0))
script_relative_path=$(echo $script_path | awk -F'/tests/' '{print $2}')

cd ${script_path}
rm -rf single_atoms_deeph

echo "[do] Running commands in ${script_relative_path} ..."
dock convert fhi-aims single-atom-to-deeph single_atoms_aims.bak single_atoms_deeph -t 0
sleep 1
echo "[done] Running commands"

echo "[do] Checking ..."
for d1 in $(ls single_atoms_deeph); do
  for f in $(ls single_atoms_deeph/$d1); do
    bash ../../check_file.sh $f single_atoms_deeph/$d1/$f single_atoms_deeph.bak/$d1/$f
  done
done
echo "[done] Checking"
cd ${_pwd}
