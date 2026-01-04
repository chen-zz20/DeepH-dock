import h5py
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename1', type=str)
parser.add_argument('filename2', type=str)
parser.add_argument('-t', '--threshold', type=float, default=1e-14)
args = parser.parse_args()

with h5py.File(args.filename1, 'r') as f1, h5py.File(args.filename2, 'r') as f2:
    for key in f1.keys():
        if key not in f2.keys():
            print(f"Key {key} in {args.filename1} is missing in {args.filename2}")
            continue
        data1 = f1[key][()]
        data2 = f2[key][()]
        if data1.shape:
            data1 = np.array(data1)
            data2 = np.array(data2)
            if type(data1.ravel()[0]) not in [np.strings, np.bool, str, bool, bytes]:
                max_diff = np.max(np.abs(data1 - data2))
            else:
                continue
        else:
            if type(data1) not in [np.strings, np.bool, str, bool, bytes]:
                max_diff = abs(data1 - data2)
            else:
                continue
        if max_diff > args.threshold:
            print(f"Key {key} in {args.filename1} and {args.filename2} do not match! Max diff: {max_diff}")
    for key in f2.keys():
        if key not in f1.keys():
            print(f"Key {key} in {args.filename2} is missing in {args.filename1}")
            continue
