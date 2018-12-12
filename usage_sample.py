import quickbench
import numpy as np 

###
# Data that will be fed to the functions being benchmarked

N = 1000
A, B, C = np.random.randn(N,N), np.random.randn(N,1), np.random.randn(1,N)

datafunc = lambda: (A, B, C)

###
# Benchmarking lambda expressions

f1 = lambda A, B, C: (A @ B) @ C
f2 = lambda A, B, C: A @ (B @ C)
f3 = lambda A, B, C: np.einsum("ij,jk,kl->il", A, B, C)

quickbench.check(datafunc, [f1, f2, f3], compfunc=lambda x,y: np.allclose(x,y))
# > [1] <lambda> matches [0] <lambda>: True
# > [2] <lambda> matches [0] <lambda>: True

quickbench.bench(datafunc, [f1, f2, f3])
# > +-----------------+-----------------+-----------------+
# > |       Functions |      Time (tot) | Time (per iter) |
# > +-----------------+-----------------+-----------------+
# > |    [0] <lambda> |       0.057003s |       0.005700s |
# > |    [1] <lambda> |       0.383022s |       0.038302s |
# > |    [2] <lambda> |       0.050003s |       0.005000s |
# > +-----------------+-----------------+-----------------+



###
# Adding names for prettier prettyprint

names = ["naive1", "naive2", "einsum"]

quickbench.check(datafunc, [f1, f2, f3], compfunc=lambda x,y: np.allclose(x,y), names=names)
# >     naive2 matches     naive1: True
# >     einsum matches     naive1: True

quickbench.bench(datafunc, [f1, f2, f3], names=names)
# > +-----------------+-----------------+-----------------+
# > |       Functions |      Time (tot) | Time (per iter) |
# > +-----------------+-----------------+-----------------+
# > |          naive1 |       0.057003s |       0.005700s |
# > |          naive2 |       0.382022s |       0.038202s |
# > |          einsum |       0.049003s |       0.004900s |
# > +-----------------+-----------------+-----------------+



###
# Using the names of the function 

def good(A, B, C): return (A @ B) @ C
def bad(A, B, C): return A @ (B @ C)
def einsum(A, B, C): return np.einsum("ij,jk,kl->il", A, B, C)
funcs = [good, bad, einsum]

quickbench.check(datafunc, funcs, compfunc=lambda x,y: np.allclose(x,y))
# > [1] bad matches [0] good: True
# > [2] einsum matches [0] good: True

quickbench.bench(datafunc, funcs)
# > +-----------------+-----------------+-----------------+
# > |       Functions |      Time (tot) | Time (per iter) |
# > +-----------------+-----------------+-----------------+
# > |        [0] good |       0.058003s |       0.005800s |
# > |         [1] bad |       0.378022s |       0.037802s |
# > |      [2] einsum |       0.049003s |       0.004900s |
# > +-----------------+-----------------+-----------------+