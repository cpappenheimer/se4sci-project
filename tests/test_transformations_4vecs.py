from __future__ import annotations

import logging

import numpy as np
import pandas as pd
import pytest

log = logging.getLogger("graphics_4vecs")


def test_transformations_4vecs_hello():
    log.info("Hello from test transformations")


@pytest.fixture()
def root_file_path():
    return "/se4sci-project/zenodo_version_D02Kpipipi_td_1000000events.root"


@pytest.fixture()
def tree_name():
    return "DalitzEventList"


def read_root_file(root_file_path, tree_name):
    branches = read_root_file(root_file_path, tree_name)
    assert isinstance(branches, dict)
    assert branches != {}


def lorentz_transform():
    E = 10.0
    px = 2.0
    py = 3.0
    pz = 4.0
    v = 0.5 * 299792458
    transformed = lorentz_transform(E, px, py, pz, v)
    expected_transformed = np.array([10.0, 0.0, 3.0, 4.0])
    np.testing.assert_allclose(transformed, expected_transformed)


# To test CSV generation, we can check if the CSV files are created
def csv_generation(root_file_path, tree_name):
    rest_frame = read_root_file(root_file_path, tree_name)
    if not rest_frame:
        pytest.skip("Empty branches, CSV generation skipped")
    else:
        rest_frame_df = pd.DataFrame(rest_frame)
        rest_frame_df.to_csv("rest_frame_data.csv", index=False)
        assert "rest_frame_data.csv" in os.listdir()

        lab_frame = {}
        for key in rest_frame:
            lab_frame[key] = [
                np.random.uniform(0, 10) for _ in range(len(rest_frame[key]))
            ]

        lab_frame_df = pd.DataFrame(lab_frame)
        lab_frame_df.to_csv("lab_frame_data.csv", index=False)
        assert "lab_frame_data.csv" in os.listdir()


# TODO
