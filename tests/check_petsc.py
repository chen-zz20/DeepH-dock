from petsc4py import PETSc
import numpy as np
from scipy.sparse import csr_matrix
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename1", type=str)
parser.add_argument("filename2", type=str)
parser.add_argument("-t", "--threshold", type=float, default=1e-14)
args = parser.parse_args()


def load_petsc(filename):
    viewer = PETSc.Viewer().createBinary(filename, mode="r")
    R_mat = PETSc.Mat()
    R_mat.load(viewer)
    indptr, indices, data = R_mat.getValuesCSR()
    data = data.real.astype(np.int32)
    R_array = csr_matrix((data, indices, indptr), shape=R_mat.getSize()).toarray()
    R_mat.destroy()
    blocks = {}
    for key in R_array:
        block_mat = PETSc.Mat()
        block_mat.load(viewer)
        indptr, indices, data = block_mat.getValuesCSR()
        blocks[tuple(key.tolist())] = csr_matrix(
            (data, indices, indptr), shape=block_mat.getSize()
        )
        block_mat.destroy()
    viewer.destroy()
    return blocks


data1 = load_petsc(args.filename1)
data2 = load_petsc(args.filename2)

for key in data1.keys():
    if key not in data2:
        print(f"R {key} in {args.filename1} is missing in {args.filename2}")
        continue
    matrix1 = data1[key]
    matrix2 = data2[key]
    if matrix1.shape != matrix2.shape:
        print(f"Shape mismatch for key {key}: {matrix1.shape} vs {matrix2.shape}")
        continue
    max_diff = np.max(np.abs(matrix1 - matrix2))
    if max_diff > args.threshold:
        print(
            f"R {key} in {args.filename1} and {args.filename2} do not match! Max diff: {max_diff}"
        )
for key in data2.keys():
    if key not in data1:
        print(f"R {key} in {args.filename2} is missing in {args.filename1}")
        continue
