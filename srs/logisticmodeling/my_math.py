def combinations(iterable, r):
    """From library itertools"""
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def chain(*iterables):
    """From library itertools"""
    # chain('ABC', 'DEF') → A B C D E F
    for it in iterables:
        for element in it:
            yield element

def all_combinations(any_list):
    return chain(*map(lambda x: combinations(any_list, x), range(0, len(any_list)+1)))

def remove_equal_elements(arr):
    n = []
    for i in arr:
        if i not in n:
            n.append(i)
    return n
