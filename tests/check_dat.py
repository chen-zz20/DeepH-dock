import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename1', type=str)
parser.add_argument('filename2', type=str)
parser.add_argument('-t', '--threshold', type=float, default=1e-14)
args = parser.parse_args()

try:
    a1 = np.loadtxt(args.filename1)
    a2 = np.loadtxt(args.filename2)
    max_diff = np.max(np.abs(a1 - a2))
    if max_diff > args.threshold:
        print(f"File {args.filename1} and {args.filename2} do not match! Max diff: {max_diff}")
except ValueError:
    with open(args.filename1) as f1, open(args.filename2) as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        for i, line1 in enumerate(lines1):
            line2 = lines2[i]
            line1 = " ".join(line1.split())
            line2 = " ".join(line2.split())
            if line1 != line2:
                print(f"Line {i+1} of file {args.filename1} and {args.filename2} do not match! `{line1}` vs `{line2}`")
