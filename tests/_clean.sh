#!/bin/bash

_pwd=$(pwd)

example_dirs=(analyze/dataset analyze/dft_equiv analyze/error compute/eigen convert/abacus convert/deeph convert/fhi_aims convert/hopcp convert/openmx convert/siesta)

for example_dir in ${example_dirs[@]}; do
    cd ${example_dir}
    for d1 in $(/bin/ls .); do
        if [[ "$d1" == *.sh ]]; then
            continue
        elif [[ "$d1" == *.clean ]]; then
            continue
        elif [[ "$d1" == *.bak ]]; then
            continue
        elif [[ "$d1" == *.ipynb ]]; then
            continue
        else
            echo "rm -r ${example_dir}/${d1}"
            rm -r ${d1}
        fi
    done
    cd $_pwd
done
