/**
* Script to generate benchmark data for N-API overhead analysis
* Tests JavaScript vs Native addon performance across different vector sizes
*/

'use strict';

// MODULES //

var bench = require( '@stdlib/bench' );
var uniform = require( '@stdlib/random/array/uniform' );
var isnan = require( '@stdlib/math/base/assert/is-nan' );
var resolve = require( 'path' ).resolve;
var tryRequire = require( '@stdlib/utils/try-require' );

// VARIABLES //

var erf = require( '@stdlib/math/base/special/erf' ); // JavaScript implementation
var erfNative = tryRequire( resolve( __dirname, 'lib/node_modules/@stdlib/math/base/special/erf/lib/native.js' ) );

var VECTOR_SIZES = [ 10, 100, 1000, 10000, 100000, 1000000 ];
var results = {
    javascript: {},
    native: {}
};

// FUNCTIONS //

/**
* Benchmarks JavaScript implementation for a given vector size
*/
function benchmarkJS( size, callback ) {
    var name = 'erf::js::' + size;
    
    bench( name, function benchmark( b ) {
        var x = uniform( size, -1.0, 1.0, { 'dtype': 'generic' });
        var y;
        var i, j;

        b.tic();
        for ( i = 0; i < b.iterations; i++ ) {
            for ( j = 0; j < size; j++ ) {
                y = erf( x[j] );
                if ( isnan( y ) ) {
                    b.fail( 'should not return NaN' );
                }
            }
        }
        b.toc();
        
        results.javascript[size] = {
            rate: b.hz,
            elapsed: b.elapsed,
            iterations: b.iterations
        };
        
        callback();
    });
}

/**
* Benchmarks native addon implementation for a given vector size
*/
function benchmarkNative( size, callback ) {
    if ( erfNative instanceof Error ) {
        console.log( 'Native addon not available, skipping...' );
        callback();
        return;
    }
    
    var name = 'erf::native::' + size;
    
    bench( name, function benchmark( b ) {
        var x = uniform( size, -1.0, 1.0, { 'dtype': 'generic' });
        var y;
        var i, j;

        b.tic();
        for ( i = 0; i < b.iterations; i++ ) {
            for ( j = 0; j < size; j++ ) {
                y = erfNative( x[j] );
                if ( isnan( y ) ) {
                    b.fail( 'should not return NaN' );
                }
            }
        }
        b.toc();
        
        results.native[size] = {
            rate: b.hz,
            elapsed: b.elapsed,
            iterations: b.iterations
        };
        
        callback();
    });
}

/**
* Runs benchmarks for all vector sizes
*/
function runBenchmarks() {
    var i = 0;
    
    function next() {
        if ( i >= VECTOR_SIZES.length ) {
            printResults();
            return;
        }
        
        var size = VECTOR_SIZES[i];
        console.log( 'Benchmarking vector size:', size );
        
        benchmarkJS( size, function() {
            benchmarkNative( size, function() {
                i++;
                next();
            });
        });
    }
    
    next();
}

/**
* Prints results in a format suitable for chart generation
*/
function printResults() {
    console.log( '\n=== BENCHMARK RESULTS ===' );
    console.log( 'Vector Size\tJS Rate (ops/sec)\tNative Rate (ops/sec)\tSpeedup' );
    
    VECTOR_SIZES.forEach( function( size ) {
        var jsRate = results.javascript[size] ? results.javascript[size].rate : 0;
        var nativeRate = results.native[size] ? results.native[size].rate : 0;
        var speedup = nativeRate > 0 ? (nativeRate / jsRate).toFixed(2) : 'N/A';
        
        console.log( size + '\t\t' + jsRate.toFixed(0) + '\t\t\t' + nativeRate.toFixed(0) + '\t\t\t' + speedup );
    });
    
    // Output JSON for chart generation
    console.log( '\n=== JSON DATA ===' );
    console.log( JSON.stringify( results, null, 2 ) );
}

// MAIN //

console.log( 'Starting N-API overhead analysis...' );
runBenchmarks();
