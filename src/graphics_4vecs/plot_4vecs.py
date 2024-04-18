from __future__ import annotations

import logging

log = logging.getLogger("graphics_4vecs")


def hello() -> None:
    log.info("Hello from plot")


def f(x: float) -> float:
    """
    TEST DOC GENERATION

    One-line summary of function

    Much longer and more detailed paragraph(s) about the function.  This is in
    the NumPy style.

    Parameters
    ----------
    x : float
        This is a parameter. Notice the type - that predates Python 3!

    Returns
    -------
    float
        A description of what it returns.

    Raises
    ------
    AssertionError
        Explain what you can raise and why.


    References
    ----------
    .. [1] "NumPy", https://numpy.org

    Examples
    --------
    >>> y = f(1.0)
    >>> y = f(2.0)
    """

    return x * 2


# TODO
