#!/usr/bin/env python
"""
Vectorized NumPy benchmark for erf function across different array sizes
This matches the stdlib vectorized benchmarks for chart comparison
"""

import numpy as np
import timeit
from scipy.special import erf
import sys

# Test different vector sizes (matching stdlib benchmarks)
VECTOR_SIZES = [10, 100, 1000, 10000, 100000, 1000000]
REPEATS = 3

def print_version():
    """Print the TAP version."""
    print("TAP version 13")

def print_results(size, elapsed, iterations):
    """Print benchmark results."""
    rate = iterations / elapsed
    print("# numpy::vectorized::erf::size=" + str(size))
    print("  ---")
    print("  iterations: " + str(iterations))
    print("  elapsed: " + str(elapsed))
    print("  rate: " + str(rate))
    print("  ...")

def benchmark_numpy_vectorized(size):
    """Benchmark NumPy vectorized erf for given array size."""
    # Generate random array once
    x = np.random.uniform(-1.0, 1.0, size)
    
    # Adjust iterations based on array size (like stdlib does)
    if size <= 100:
        iterations = 100000
    elif size <= 1000:
        iterations = 10000
    elif size <= 10000:
        iterations = 1000
    elif size <= 100000:
        iterations = 100
    else:
        iterations = 10
    
    def run_erf():
        return erf(x)
    
    # Time the vectorized operation
    elapsed = timeit.timeit(run_erf, number=iterations)
    
    return elapsed, iterations

def benchmark_pure_python_vectorized(size):
    """Benchmark pure Python erf for given array size (for comparison)."""
    import math
    
    # Generate random values
    x = [np.random.uniform(-1.0, 1.0) for _ in range(size)]
    
    # Adjust iterations based on array size
    if size <= 100:
        iterations = 10000  # Much lower for pure Python
    elif size <= 1000:
        iterations = 1000
    elif size <= 10000:
        iterations = 100
    elif size <= 100000:
        iterations = 10
    else:
        iterations = 1
    
    def run_erf():
        return [math.erf(val) for val in x]
    
    # Time the list comprehension
    elapsed = timeit.timeit(run_erf, number=iterations)
    
    return elapsed, iterations

def main():
    """Run vectorized benchmarks for all sizes."""
    print_version()
    
    print("\n=== NUMPY/SCIPY VECTORIZED BENCHMARKS ===")
    numpy_results = {}
    
    for size in VECTOR_SIZES:
        print(f"\nTesting NumPy vectorized erf with size {size}...")
        total_elapsed = 0
        total_iterations = 0
        
        for repeat in range(REPEATS):
            elapsed, iterations = benchmark_numpy_vectorized(size)
            total_elapsed += elapsed
            total_iterations += iterations
            print_results(size, elapsed, iterations)
            print(f"ok {repeat+1} benchmark finished")
        
        avg_elapsed = total_elapsed / REPEATS
        avg_rate = total_iterations / total_elapsed * REPEATS
        numpy_results[size] = avg_rate
        
        print(f"Average rate for size {size}: {avg_rate:.0f} ops/sec")
    
    print("\n=== PURE PYTHON VECTORIZED BENCHMARKS ===")
    python_results = {}
    
    for size in VECTOR_SIZES:
        print(f"\nTesting Pure Python vectorized erf with size {size}...")
        total_elapsed = 0
        total_iterations = 0
        
        for repeat in range(REPEATS):
            elapsed, iterations = benchmark_pure_python_vectorized(size)
            total_elapsed += elapsed
            total_iterations += iterations
            print(f"# python::vectorized::erf::size={size}")
            print("  ---")
            print(f"  iterations: {iterations}")
            print(f"  elapsed: {elapsed}")
            print(f"  rate: {iterations/elapsed}")
            print("  ...")
            print(f"ok {repeat+1} benchmark finished")
        
        avg_elapsed = total_elapsed / REPEATS
        avg_rate = total_iterations / total_elapsed * REPEATS
        python_results[size] = avg_rate
        
        print(f"Average rate for size {size}: {avg_rate:.0f} ops/sec")
    
    # Print summary comparison
    print("\n=== PERFORMANCE COMPARISON ===")
    print("Size\t\tNumPy (ops/sec)\t\tPython (ops/sec)\t\tSpeedup")
    print("-" * 70)
    
    for size in VECTOR_SIZES:
        numpy_rate = numpy_results[size]
        python_rate = python_results[size]
        speedup = numpy_rate / python_rate if python_rate > 0 else float('inf')
        
        print(f"{size}\t\t{numpy_rate:.0f}\t\t\t{python_rate:.0f}\t\t\t{speedup:.1f}x")
    
    # Print JSON for chart generation
    print("\n=== JSON DATA FOR CHART ===")
    print("NumPy results:", numpy_results)
    print("Python results:", python_results)

if __name__ == "__main__":
    main()
