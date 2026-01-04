from pathlib import Path
import json
import h5py
from tqdm import tqdm
from functools import partial
from joblib import Parallel, delayed

import numpy as np
import matplotlib.pyplot as plt

from deepx_dock.CONSTANT import DEEPX_HAMILTONIAN_FILENAME, DFT_DIRNAME
from deepx_dock.CONSTANT import DATASET_SPLIT_FILENAME
from deepx_dock.misc import get_data_dir_lister

EDGE_QUANTITY_STATISTIC_FIGURE = "edge_quantity_statistics.png"


def _validation_check(root_dir: Path, prev_dirname: Path):
    yield prev_dirname


class DatasetAnalyzer:
    def __init__(self, data_path, n_jobs=1, n_tier=0):
        self.data_path = Path(data_path)
        self.dft_data_path = self.data_path / DFT_DIRNAME
        self.n_jobs = n_jobs
        self.n_tier = n_tier

    def gen_dft_features(self):
        self._find_all_dft_data_dir()
        features = {
            "dft_dirname_list": self.all_dft_dirname,
        }
        return features
    
    def _find_all_dft_data_dir(self):
        print("[do] Locate all DFT data directories ...", flush=True)
        print(f"[rawdata] Processing DFT data in `{self.dft_data_path}`.")
        lister = get_data_dir_lister(
            self.dft_data_path, self.n_tier, _validation_check
        )
        all_dft_dir_list = [str(d) for d in tqdm(lister, desc="  +-[search]")]
        #
        structures_num = len(all_dft_dir_list)
        if structures_num == 0:
            raise FileNotFoundError(f"[error] No valid data found in `{self.dft_data_path}`")
        print(f"[rawdata] Found `{structures_num}` structures in `{self.dft_data_path}`.")
        #
        self.all_dft_dirname = sorted(all_dft_dir_list)
        self.all_dft_data_num = structures_num

    # ------------------------------------------------
    # Data Split JSON Generator
    # ------------------------------------------------
    def generate_data_split_json(self,
        features, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2,
        max_edge_num=-1, rng_seed=137
    ):
        assert (train_ratio + val_ratio + test_ratio) <= 1.0
        worker = partial(
            self._check_data_validation,
            dft_data_path=self.dft_data_path,
            max_edge_num=max_edge_num
        )
        results = Parallel(n_jobs=self.n_jobs)(
            delayed(worker)(dir_name)
            for dir_name in tqdm(features["dft_dirname_list"],desc="Data Split")
        )
        available_data_dirs = [name for name in results if name is not None]
        # Generate the data split
        available_data_num = len(available_data_dirs)
        print(f"[info] Total available data dirs: {available_data_num}")
        _rng = np.random.default_rng(rng_seed)
        _rng.shuffle(available_data_dirs)
        n_train = int(available_data_num * train_ratio)
        n_val = int(available_data_num * val_ratio)
        data_split = {
            "train":  available_data_dirs[:n_train],
            "validate": available_data_dirs[n_train:n_train+n_val],
            "test": available_data_dirs[n_train+n_val:]
        }
        # Save the json to file
        with open(DATASET_SPLIT_FILENAME, "w") as jfrp:
            json.dump(data_split, jfrp)
        print(f"[info] Data split json saved to ./{DATASET_SPLIT_FILENAME}.")
        return data_split
    
    @staticmethod
    def _check_data_validation(
        dir_name: str, dft_data_path: str | Path, max_edge_num: int = -1
    ):
        dir_path = Path(dft_data_path) / dir_name
        h_path = dir_path / DEEPX_HAMILTONIAN_FILENAME
        if h_path.is_file():
            with h5py.File(h_path, "r") as fh5:
                edge_num = len(np.array(fh5["atom_pairs"][:]))
                if (max_edge_num < 0) or (edge_num <= max_edge_num):
                    return dir_name
        return None

    # ------------------------------------------------
    # Statistic edges quantity
    # ------------------------------------------------
    def statistic_edge_quantity(self, features, bins=None):
        # Read the edge_quantity
        cache_path = self.data_path / "edge_statistic.h5"
        if cache_path.is_file():
            with h5py.File(cache_path, 'r') as h5file:
                results = np.array(h5file["edges_quantity"][:], dtype=int)
        else:
            worker = partial(
                self._read_edge_info,
                dft_data_path=self.dft_data_path,
            )
            results = Parallel(n_jobs=self.n_jobs)(
                delayed(worker)(dir_name)
                for dir_name in tqdm(
                    features["dft_dirname_list"], desc="Edge Analysis"
                )
            )
            results = np.array(results)
            with h5py.File(cache_path, "w") as h5file:
                h5file.create_dataset("edges_quantity", data=results)
        # Count!
        bins = 'auto' if bins is None else bins
        self.edge_counts, self.edge_bin = np.histogram(results, bins=bins)
    
    def plot_edge_quantity(self, dpi=300):
        bin_labels = [
            f"{int(self.edge_bin[i])}-{int(self.edge_bin[i+1])}" 
            for i in range(len(self.edge_bin)-1)
        ]
        save_figure_path = self.data_path / "edge_statistic.png"
        plt.bar(bin_labels, self.edge_counts, edgecolor='black')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel("Edges Quantity")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(save_figure_path, dpi=dpi)

    @staticmethod
    def _read_edge_info(dir_name: str, dft_data_path: str | Path):
        dir_path = Path(dft_data_path) / dir_name
        h_path = dir_path / DEEPX_HAMILTONIAN_FILENAME
        if h_path.is_file():
            with h5py.File(h_path, "r") as fh5:
                edge_num = len(np.array(fh5["atom_pairs"][:]))
                return edge_num

