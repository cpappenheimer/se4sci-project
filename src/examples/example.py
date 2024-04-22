from __future__ import annotations

import logging
import sys
from typing import Any

import awkward
import numpy as np
import numpy.typing as npt
import pandas as pd
import uproot

logging.basicConfig(level="INFO")  # Global setting
log = logging.getLogger("graphics_4vecs")


def read_root_file(root_file_path: str, tree_name: str) -> awkward.highlevel.Array:
    """
    Read a ROOT file and extract branch arrays.

    Args:
        root_file_path (str): Path to the ROOT file.
        tree_name (str): Name of the tree in the ROOT file.

    Returns:
        dict: Dictionary containing branch arrays.
    """
    root_file = uproot.open(root_file_path)
    tree = root_file[tree_name]
    branches = tree.keys()

    branch_arrays = {}

    for branch_name in branches:
        renamed_branch_name = branch_name.replace("#", "plus").replace("~", "minus")
        branch_array = tree[branch_name].array()
        branch_arrays[renamed_branch_name] = branch_array

    return branch_arrays


if len(sys.argv) != 3:
    root_file_path = "zenodo_version_D02Kpipipi_td_1000000events.root"
    tree_name = "DalitzEventList"
else:
    root_file_path = sys.argv[1]
    tree_name = sys.argv[2]

branches = read_root_file(root_file_path, tree_name)

if not branches:
    log = logging.getLogger("Error: Empty branches.")
    exit()

rest_frame: dict[str, list[float]] = {
    "K_E": branches.get("_1_Kplus_E", []),
    "K_px": branches.get("_1_Kplus_Px", []),
    "K_py": branches.get("_1_Kplus_Py", []),
    "K_pz": branches.get("_1_Kplus_Pz", []),
    "pi_minus_2_E": branches.get("_2_piminus_E", []),
    "pi_minus_2_px": branches.get("_2_piminus_Px", []),
    "pi_minus_2_py": branches.get("_2_piminus_Py", []),
    "pi_minus_2_pz": branches.get("_2_piminus_Pz", []),
    "pi_minus_3_E": branches.get("_3_piminus_E", []),
    "pi_minus_3_px": branches.get("_3_piminus_Px", []),
    "pi_minus_3_py": branches.get("_3_piminus_Py", []),
    "pi_minus_3_pz": branches.get("_3_piminus_Pz", []),
    "pi_plus_4_E": branches.get("_4_piplus_E", []),
    "pi_plus_4_px": branches.get("_4_piplus_Px", []),
    "pi_plus_4_py": branches.get("_4_piplus_Py", []),
    "pi_plus_4_pz": branches.get("_4_piplus_Pz", []),
}

rest_frame_df = pd.DataFrame(rest_frame)
rest_frame_df.to_csv("rest_frame_data.csv", index=False)


def lorentz_transform(
    E: float, px: float, py: float, pz: float, v: float
) -> npt.NDArray[Any]:
    """
    Perform Lorentz transformation on four-momenta.

    Args:
        E (float): Energy.
        px (float): x-component of momentum.
        py (float): y-component of momentum.
        pz (float): z-component of momentum.
        v (float): Velocity of the parent particle in meters per second.

    Returns:
        np.array: Transformed four-momenta.
    """
    p = np.array([E, px, py, pz])
    beta = v / 299792458  # Speed of light in meters per second
    gamma = 1 / np.sqrt(1 - beta**2)

    lambda_matrix = np.array(
        [
            [gamma, -gamma * beta, 0, 0],
            [-gamma * beta, gamma, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    return np.dot(lambda_matrix, p)  # type: ignore[no-any-return]


log = logging.getLogger("Performing Lorentz transformation")

lab_frame: dict[str, list[float]] = {
    "K_E": [],
    "K_px": [],
    "K_py": [],
    "K_pz": [],
    "pi_minus_2_E": [],
    "pi_minus_2_px": [],
    "pi_minus_2_py": [],
    "pi_minus_2_pz": [],
    "pi_minus_3_E": [],
    "pi_minus_3_px": [],
    "pi_minus_3_py": [],
    "pi_minus_3_pz": [],
    "pi_plus_4_E": [],
    "pi_plus_4_px": [],
    "pi_plus_4_py": [],
    "pi_plus_4_pz": [],
}

v = 0.5 * 299792458  # Example velocity: half the speed of light

for i in range(len(rest_frame["K_E"])):
    P_d1_lab = lorentz_transform(
        rest_frame["K_E"][i],
        rest_frame["K_px"][i],
        rest_frame["K_py"][i],
        rest_frame["K_pz"][i],
        v,
    )
    P_d2_lab = lorentz_transform(
        rest_frame["pi_minus_2_E"][i],
        rest_frame["pi_minus_2_px"][i],
        rest_frame["pi_minus_2_py"][i],
        rest_frame["pi_minus_2_pz"][i],
        v,
    )
    P_d3_lab = lorentz_transform(
        rest_frame["pi_minus_3_E"][i],
        rest_frame["pi_minus_3_px"][i],
        rest_frame["pi_minus_3_py"][i],
        rest_frame["pi_minus_3_pz"][i],
        v,
    )
    P_d4_lab = lorentz_transform(
        rest_frame["pi_plus_4_E"][i],
        rest_frame["pi_plus_4_px"][i],
        rest_frame["pi_plus_4_py"][i],
        rest_frame["pi_plus_4_pz"][i],
        v,
    )

    lab_frame["K_E"].append(P_d1_lab[0])
    lab_frame["K_px"].append(P_d1_lab[1])
    lab_frame["K_py"].append(P_d1_lab[2])
    lab_frame["K_pz"].append(P_d1_lab[3])

    lab_frame["pi_minus_2_E"].append(P_d2_lab[0])
    lab_frame["pi_minus_2_px"].append(P_d2_lab[1])
    lab_frame["pi_minus_2_py"].append(P_d2_lab[2])
    lab_frame["pi_minus_2_pz"].append(P_d2_lab[3])

    lab_frame["pi_minus_3_E"].append(P_d3_lab[0])
    lab_frame["pi_minus_3_px"].append(P_d3_lab[1])
    lab_frame["pi_minus_3_py"].append(P_d3_lab[2])
    lab_frame["pi_minus_3_pz"].append(P_d3_lab[3])

    lab_frame["pi_plus_4_E"].append(P_d4_lab[0])
    lab_frame["pi_plus_4_px"].append(P_d4_lab[1])
    lab_frame["pi_plus_4_py"].append(P_d4_lab[2])
    lab_frame["pi_plus_4_pz"].append(P_d4_lab[3])

lab_frame_df = pd.DataFrame(lab_frame)
lab_frame_df.to_csv("lab_frame_data.csv", index=False)
