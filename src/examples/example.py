from __future__ import annotations

import argparse
import logging

import awkward
import uproot

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
    parser.add_argument("--tree-name", help="Name of tree in ntuple")
    args = parser.parse_args()
    file = args.file
    tree_name = args.tree_name

    branches = read_root_file(file, tree_name)
    log.info(type(branches))

    # log.info("Hello World!")
    # t.hello()
    # p.hello()


# TODO


if __name__ == "__main__":
    main()
