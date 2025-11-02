#!/usr/bin/env python
"""
Benchmark scipy.special.erf with 1D contiguous float64 arrays
Matches stdlib vectorized benchmark pattern
"""

from __future__ import print_function
import timeit
import numpy as np
from scipy.special import erf

NAME = "erf"
REPEATS = 3
ITERATIONS = 1000000
MIN = 1  # 10^MIN
MAX = 6  # 10^MAX
COUNT = [0]  # use a list to allow modification within nested scopes


def print_version():
    """Print the TAP version."""
    print("TAP version 13")


def print_summary(total, passing):
    """Print the benchmark summary.

    # Arguments

    * `total`: total number of tests
    * `passing`: number of passing tests

    """
    print("#")
    print("1.." + str(total))  # TAP plan
    print("# total " + str(total))
    print("# pass  " + str(passing))
    print("#")
    print("# ok")


def print_results(iterations, elapsed):
    """Print benchmark results.

    # Arguments

    * `iterations`: number of iterations
    * `elapsed`: elapsed time (in seconds)

    # Examples

    ``` python
    python> print_results(1000000, 0.131009101868)
    ```
    """
    rate = iterations / elapsed

    print("  ---")
    print("  iterations: " + str(iterations))
    print("  elapsed: " + str(elapsed))
    print("  rate: " + str(rate))
    print("  ...")


def benchmark(name, setup, stmt, iterations):
    """Run the benchmark and print benchmark results.

    # Arguments

    * `name`: benchmark name (suffix)
    * `setup`: benchmark setup
    * `stmt`: statement to benchmark
    * `iterations`: number of iterations

    # Examples

    ``` python
    python> benchmark("::random", "from random import random;", "y = random()", 1000000)
    ```
    """
    t = timeit.Timer(stmt, setup=setup)

    i = 0
    while i < REPEATS:
        print("# python::scipy::" + NAME + name)
        COUNT[0] += 1
        elapsed = t.timeit(number=iterations)
        print_results(iterations, elapsed)
        print("ok " + str(COUNT[0]) + " benchmark finished")
        i += 1


def main():
    """Run the benchmarks."""
    print_version()

    iters = ITERATIONS
    p = MIN
    while p <= MAX:
        n = 10**p
        p += 1
        name = ":contiguous=true,ndims=1,dtype=float64,len="+str(n)
        setup = "import numpy as np; from scipy.special import erf;"
        setup += "x = np.random.uniform(-1.0, 1.0, ("+str(n)+")).astype('float64');"
        stmt = "y = erf(x)"
        benchmark(name, setup, stmt, iters)
        iters //= 4

    print_summary(COUNT[0], COUNT[0])


if __name__ == "__main__":
    main()
