from __future__ import annotations

import logging

import graphics_4vecs.plot_4vecs as p
import graphics_4vecs.transformations_4vecs as t

logging.basicConfig(level="INFO")  # Global setting
log = logging.getLogger("graphics_4vecs")


def main() -> None:
    log.info("Hello World!")

    t.hello()
    p.hello()


# TODO


if __name__ == "__main__":
    main()
