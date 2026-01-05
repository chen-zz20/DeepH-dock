#!/bin/bash

_pwd=$(pwd)
script_path=$(realpath $(dirname $0))
script_relative_path=$(echo $script_path | awk -F'/tests/' '{print $2}')

cd ${script_path}
rm -rf poscars dft_calc
cp -rL poscars.clean poscars
cp -rL dft_calc.bak dft_calc

echo "[do] Running commands in ${script_relative_path} ..."
dock analyze dft-equiv gen poscars -n 4 --translate
sleep 1
dock analyze dft-equiv test dft_calc
echo "mv equiv_mae.png dft_calc/equiv_mae.png"
mv equiv_mae.png dft_calc/equiv_mae.png
sleep 1
echo "[done] Running commands"

echo "[do] Checking ..."
for d1 in $(ls poscars); do
  for f in $(ls poscars/$d1); do
    bash ../../check_file.sh $f poscars/$d1/$f poscars.bak/$d1/$f
  done
done
echo "[done] Checking"
cd ${_pwd}
