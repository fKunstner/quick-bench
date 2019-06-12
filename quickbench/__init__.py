from time import perf_counter_ns as tick


def __checknames(funcs, names):
    if names is not None:
        assert len(funcs) == len(names), "The number of names (%d) needs to match the number of functions (%d)" % (len(names), len(funcs))
    else:
        names = ["[%d] %s" % (i, func.__name__) for i, func in enumerate(funcs)]
    return names


def time(func, args={}, reps=3):

    times = []
    for rep in range(reps):
        start = tick()
        func(**args)
        end = tick()
        times.append(end - start)

    return min(times)


def check(funcs, args={}, names=None, compfunc=None):
    r"""
    Verifies that the functions in `funcs` return the same values.

    If `compfunc` is `None`, uses standard `==` check.
    """
    names = __checknames(funcs, names)
    results = []

    for i, func in enumerate(funcs):
        results.append(func(**args))

    if compfunc is None:
        def compfunc(x, y):
            return x == y
    for j in range(1, len(funcs)):
        print("%10s matches %10s: %s" % (names[j], names[0], compfunc(results[0], results[j])))


def bench(funcs, args={}, names=None, reps=3, prettyprint=True):
    r"""
    Runs each function in `funcs` for `reps` repetitions (defaults to 10) and returns the total running time.
    If `prettyprint` is `True`, prints a table with the results.
    If `names` is None, tries to infer a sensible name for the functions.
    """
    names = __checknames(funcs, names)

    times = [time(func, args, reps=reps) for func in funcs]

    if prettyprint:
        cellsep = ("-" * 15)
        sep = "+-" + cellsep + "-+-" + cellsep + "-+"

        print(sep)
        print("| %15s | %15s |" % ("Functions", "Time (tot)"))
        print(sep)
        for i in range(len(funcs)):
            print("| %15s | %14fs |" % (names[i], times[i] / 10**9))
        print(sep)

    return times
