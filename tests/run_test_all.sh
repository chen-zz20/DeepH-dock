#!/bin/bash

_pwd=$(pwd)
script_path=$(realpath $(dirname $0))

example_dirs=(analyze/dataset analyze/dft_equiv analyze/error compute/eigen convert/abacus convert/deeph convert/fhi_aims convert/hopcp convert/openmx convert/siesta)

echo "cd ${script_path}"
cd ${script_path}
for example_dir in ${example_dirs[@]}; do
    cd ${example_dir}
    bash run_test.sh
    cd ${script_path}
    echo ""
done
echo "cd ${_pwd}"
cd ${_pwd}
