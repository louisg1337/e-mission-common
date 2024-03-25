# __pragma__('kwargs')

def memoize(fn: function) -> function:
    '''
    Simple memoization decorator
    '''
    _cache = {}
    def wrapper(*args, **kwargs):
        if (str(args), str(kwargs)) not in _cache:
            _cache[(str(args), str(kwargs))] = fn(*args, **kwargs)
        return _cache[(str(args), str(kwargs))]
    return wrapper

# __pragma__('nokwargs')
