from __future__ import annotations

import argparse
import logging

import awkward
import pandas as pd
import uproot
from ROOT import TLorentzVector

import graphics_4vecs.plot_4vecs as p
import graphics_4vecs.transformations_4vecs as t

logging.basicConfig(level="INFO")  # Global setting
log = logging.getLogger("graphics_4vecs")


def read_root_file(root_file_path: str, tree_name: str) -> awkward.highlevel.Array:
    root_file = uproot.open(root_file_path)
    tree = root_file[tree_name]
    branches = tree.keys()

    branch_arrays = {}

    for branch_name in branches:
        renamed_branch_name = branch_name.replace("#", "plus").replace("~", "minus")
        branch_array = tree[branch_name].array()
        branch_arrays[renamed_branch_name] = branch_array

    return branch_arrays


def main() -> None:
    # parse user args
    parser = argparse.ArgumentParser("K3Pi Example")
    parser.add_argument("--file", help="Path to file with input data", type=str)
    parser.add_argument("--tree-name", help="Name of tree in ntuple", type=str)
    parser.add_argument("--num-events", help="Num of events to transform", type=int)
    args = parser.parse_args()
    file = args.file
    tree_name = args.tree_name
    num_events = args.num_events

    # read data from file
    branches = read_root_file(file, tree_name)
    K_E = branches["_1_Kplus_E"]
    K_Px = branches["_1_Kplus_Px"]
    K_Py = branches["_1_Kplus_Py"]
    K_Pz = branches["_1_Kplus_Pz"]
    pi_minus_2_E = branches["_2_piminus_E"]
    pi_minus_2_Px = branches["_2_piminus_Px"]
    pi_minus_2_Py = branches["_2_piminus_Py"]
    pi_minus_2_Pz = branches["_2_piminus_Pz"]
    pi_minus_3_E = branches["_3_piminus_E"]
    pi_minus_3_Px = branches["_3_piminus_Px"]
    pi_minus_3_Py = branches["_3_piminus_Py"]
    pi_minus_3_Pz = branches["_3_piminus_Pz"]
    pi_plus_4_E = branches["_4_piplus_E"]
    pi_plus_4_Px = branches["_4_piplus_Px"]
    pi_plus_4_Py = branches["_4_piplus_Py"]
    pi_plus_4_Pz = branches["_4_piplus_Pz"]
    # initial_data = {
    #     "K_E": K_E,
    #     "K_px": K_Px,
    #     "K_py": K_Py,
    #     "K_pz": K_Pz,
    #     "pi_minus_2_E": pi_minus_2_E,
    #     "pi_minus_2_px": pi_minus_2_Px,
    #     "pi_minus_2_py": pi_minus_2_Py,
    #     "pi_minus_2_pz": pi_minus_2_Pz,
    #     "pi_minus_3_E": pi_minus_3_E,
    #     "pi_minus_3_px": pi_minus_3_Px,
    #     "pi_minus_3_py": pi_minus_3_Py,
    #     "pi_minus_3_pz": pi_minus_3_Pz,
    #     "pi_plus_4_E": pi_plus_4_E,
    #     "pi_plus_4_px": pi_plus_4_Px,
    #     "pi_plus_4_py": pi_plus_4_Py,
    #     "pi_plus_4_pz": pi_plus_4_Pz,
    # }

    log.info("Performing Lorentz transformation")

    final_data: dict[str, list[float]] = {
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

    for i in range(num_events):
        k_plus = TLorentzVector()
        k_plus.SetPxPyPzE(K_Px[i], K_Py[i], K_Pz[i], K_E[i])

        pi_minus_2 = TLorentzVector()
        pi_minus_2.SetPxPyPzE(
            pi_minus_2_Px[i], pi_minus_2_Py[i], pi_minus_2_Pz[i], pi_minus_2_E[i]
        )

        pi_minus_3 = TLorentzVector()
        pi_minus_3.SetPxPyPzE(
            pi_minus_3_Px[i], pi_minus_3_Py[i], pi_minus_3_Pz[i], pi_minus_3_E[i]
        )

        pi_plus_4 = TLorentzVector()
        pi_plus_4.SetPxPyPzE(
            pi_plus_4_Px[i], pi_plus_4_Py[i], pi_plus_4_Pz[i], pi_plus_4_E[i]
        )

        # Boost k and pi- (2) to kpi- rest frame
        kpi_boost = (k_plus + pi_minus_2).BoostVector()
        boosted_k_plus = TLorentzVector(k_plus)
        boosted_k_plus.Boost(kpi_boost)
        boosted_pi_minus_2 = TLorentzVector(pi_minus_2)
        boosted_pi_minus_2.Boost(kpi_boost)

        # Boost pi- (3) and pi+ to pi-pi+ rest frame
        pipi_boost = (pi_minus_3 + pi_plus_4).BoostVector()
        boosted_pi_minus_3 = TLorentzVector(pi_minus_3)
        boosted_pi_minus_3.Boost(pipi_boost)
        boosted_pi_plus_4 = TLorentzVector(pi_plus_4)
        boosted_pi_plus_4.Boost(pipi_boost)

        final_data["K_E"].append(boosted_k_plus.E())
        final_data["K_px"].append(boosted_k_plus.Px())
        final_data["K_py"].append(boosted_k_plus.Py())
        final_data["K_pz"].append(boosted_k_plus.Pz())
        final_data["pi_minus_2_E"].append(boosted_pi_minus_2.E())
        final_data["pi_minus_2_px"].append(boosted_pi_minus_2.Px())
        final_data["pi_minus_2_py"].append(boosted_pi_minus_2.Py())
        final_data["pi_minus_2_pz"].append(boosted_pi_minus_2.Pz())
        final_data["pi_minus_3_E"].append(boosted_pi_minus_3.E())
        final_data["pi_minus_3_px"].append(boosted_pi_minus_3.Px())
        final_data["pi_minus_3_py"].append(boosted_pi_minus_3.Py())
        final_data["pi_minus_3_pz"].append(boosted_pi_minus_3.Pz())
        final_data["pi_plus_4_E"].append(boosted_pi_plus_4.E())
        final_data["pi_plus_4_px"].append(boosted_pi_plus_4.Px())
        final_data["pi_plus_4_py"].append(boosted_pi_plus_4.Py())
        final_data["pi_plus_4_pz"].append(boosted_pi_plus_4.Pz())

        # Convert data to pandas DataFrames
        # initial_df = pd.DataFrame(initial_data)
        final_df = pd.DataFrame(final_data)

        # Write DataFrames to CSV files
        # initial_df.to_csv('initial_branches.csv', index=False)
        final_df.to_csv("final_branches.csv", index=False)
    # end loop

    log.info("Hello World!")
    t.hello()
    p.hello()


# end main

# TODO


if __name__ == "__main__":
    main()
