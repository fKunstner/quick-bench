import time

def __checknames(funcs, names):
    if names is not None:
        assert len(funcs) == len(names), "The number of names (%d) needs to match the number of functions (%d)" % (len(names), len(funcs))
    else:
        names = ["[%d] %s" % (i, func.__name__) for i, func in enumerate(funcs)]
    return names 

def check(datafunc, funcs, names=None, compfunc=None):
    r"""
    Verifies that the functions in `funcs` return the same values.
    
    Each function in `funcs` is run with the output of `datafunc` as argument,
    and the comparison is carried using `compfunc` on the output of the functions 
    in `funcs`. 
    
    If `compfunc` is `None`, uses standard `==` check.
    """
    names = __checknames(funcs, names)
    results = []
    
    for i, func in enumerate(funcs):
        results.append(func(*datafunc()))
        
    if compfunc is None:
        compfunc = lambda x, y : x == y
    for j in range(1,len(funcs)):
        print("%10s matches %10s: %s" % (names[j], names[0], compfunc(results[0], results[j])))

def bench(datafunc, funcs, names=None, reps=10, prettyprint=True):
    r"""
    Runs each function in `funcs` with the output of `datafunc` as argument,
    for `reps` repetitions (defaults to 10) and returns the total running time.
    
    If `prettyprint` is `True`, prints a table with the results. 
    
    If `names` is None, tries to infer a sensible name for the functions.
    """
    names = __checknames(funcs, names)
    
    times = []
    for i, func in enumerate(funcs):
        start = time.time()
        for rep in range(reps):
            func(*datafunc())
        end = time.time()
        times.append(end-start)
    
    if prettyprint:
        cellsep = ("-"*15)
        sep = "+-"+cellsep+"-+-"+cellsep+"-+-"+cellsep+"-+"
        
        print(sep)
        print("| %15s | %15s | %15s |" % ("Functions", "Time (tot)", "Time (per iter)"))
        print(sep)
        for i in range(len(funcs)):
            print("| %15s | %14fs | %14fs |" % (names[i], times[i], times[i]/reps))
        print(sep)
            
    return times 
