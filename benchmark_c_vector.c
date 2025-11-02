/**
* C benchmark for pure C erf implementation across different vector sizes
* Used to establish baseline performance for comparison with JS and native addon
*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>

#define REPEATS 3

/**
* Returns current time in seconds
*/
static double tic( void ) {
    struct timeval tv;
    gettimeofday( &tv, NULL );
    return (double)tv.tv_sec + (double)tv.tv_usec/1.0e6;
}

/**
* Generates random double between -1 and 1
*/
static double rand_double( void ) {
    int r = rand();
    return 2.0 * ((double)r / (double)RAND_MAX) - 1.0;
}

/**
* Benchmarks erf for a given vector size
*/
static double benchmark_vector( int size ) {
    double *values = malloc( size * sizeof(double) );
    double elapsed;
    double y;
    double t;
    int i, j;
    int iterations = 1000000 / size; // Adjust iterations based on vector size
    
    if ( iterations < 1 ) iterations = 1;
    
    // Generate random values
    for ( i = 0; i < size; i++ ) {
        values[i] = rand_double();
    }
    
    t = tic();
    for ( i = 0; i < iterations; i++ ) {
        for ( j = 0; j < size; j++ ) {
            y = erf( values[j] );
            if ( y != y ) { // NaN check
                printf( "should not return NaN\n" );
                break;
            }
        }
    }
    elapsed = tic() - t;
    
    free( values );
    
    // Calculate operations per second
    double ops_per_sec = (double)(iterations * size) / elapsed;
    printf( "Vector size: %d, Elapsed: %.6f s, Rate: %.0f ops/sec\n", 
            size, elapsed, ops_per_sec );
    
    return ops_per_sec;
}

/**
* Main execution sequence
*/
int main( void ) {
    int vector_sizes[] = { 10, 100, 1000, 10000, 100000, 1000000 };
    int num_sizes = sizeof(vector_sizes) / sizeof(vector_sizes[0]);
    double rates[6];
    int i, j;
    
    // Use current time to seed random number generator
    srand( time( NULL ) );
    
    printf( "=== C ERF BENCHMARK RESULTS ===\n" );
    printf( "Vector Size\tRate (ops/sec)\n" );
    
    for ( i = 0; i < num_sizes; i++ ) {
        double total_rate = 0.0;
        
        // Run multiple repeats and average
        for ( j = 0; j < REPEATS; j++ ) {
            total_rate += benchmark_vector( vector_sizes[i] );
        }
        
        rates[i] = total_rate / REPEATS;
        printf( "%d\t\t%.0f\n", vector_sizes[i], rates[i] );
    }
    
    printf( "\n=== NORMALIZED RESULTS (relative to largest vector) ===\n" );
    double max_rate = rates[num_sizes - 1]; // Use largest vector as baseline
    
    for ( i = 0; i < num_sizes; i++ ) {
        double normalized = rates[i] / max_rate;
        printf( "Vector size %d: %.3f\n", vector_sizes[i], normalized );
    }
    
    return 0;
}
