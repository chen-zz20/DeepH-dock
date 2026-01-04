#!/bin/bash

_pwd=$(pwd)

example_dirs=(analyze/dataset analyze/dft_equiv analyze/error compute/eigen convert/abacus convert/deeph convert/fhi_aims convert/hopcp convert/openmx convert/siesta)

for example_dir in ${example_dirs[@]}; do
    cd ${example_dir}
    bash run_test.sh
    cd $_pwd
    echo ""
done
