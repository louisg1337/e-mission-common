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


# e-mission-phone www/js/diary/timelineHelper.ts unpackServerData()
def flatten_db_entry(entry: dict) -> dict:
    '''
    DB entries retrieved from the server have '_id', 'metadata', and 'data' fields.
    This function returns a shallow copy of the obj, which flattens the 'data' field into the top
    level, while also including '_id', 'metadata.key', and 'metadata.origin_key'.
    '''
    return {
        **entry['data'],
        '_id': entry['_id'],
        'key': entry['metadata']['key'],
        'origin_key': entry['metadata']['origin_key'] if 'origin_key' in entry['metadata'] else entry['metadata']['key']
    }
