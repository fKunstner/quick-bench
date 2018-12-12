# quickbench
Some helper functions for benchmarking.

Nothing fancy, just got bored of writing timing and pretty-printing code.

## Installation 

* Clone the git repository, 
* `cd` to the repository containing `setup.py`
* run `pip install .` (or `pip install -e .` if you wish to edit the benchmarking code)

## Usage example

Say we want to figure out if [`np.einsum`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.einsum.html)
is smart enough to do matrix multiplication in the "correct" order.

To compute `A x B x C`, if the size of the matrices are 

    A : [1000 x 1000]
    B : [1000 x 1]
    C : [1 x 1000]
    
it is more efficient to compute `(A x B) x C` than `A x (B x C)`.

Let's define the functions we want to test, 

    def good(A, B, C): return (A @ B) @ C
    def bad(A, B, C): return A @ (B @ C)
    def einsum(A, B, C): return np.einsum("ij,jk,kl->il", A, B, C)
    funcs = [good, bad, einsum]

and some function to give them data

    N = 1000
    A, B, C = np.random.randn(N,N), np.random.randn(N,1), np.random.randn(1,N)
    datafunc = lambda: (A, B, C)

We can now do a quick benchmark 

    quickbench.bench(datafunc, funcs)
    # > +-----------------+-----------------+-----------------+
    # > |       Functions |      Time (tot) | Time (per iter) |
    # > +-----------------+-----------------+-----------------+
    # > |        [0] good |       0.058003s |       0.005800s |
    # > |         [1] bad |       0.378022s |       0.037802s |
    # > |      [2] einsum |       0.049003s |       0.004900s |
    # > +-----------------+-----------------+-----------------+
    
`np.einsum` is smart!

**For more examples, see `usage_sample.py`**
