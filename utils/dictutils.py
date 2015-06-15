def deep_get(dictionary, path):
    """deep_get(dict, "a.b.c") -> D[a][b][c] if a, b and c exist. Defaults to None."""
    keys = path.split(".")
    return _recursive_deep_get(dictionary, keys)


def _recursive_deep_get(dictionary, keys):
    if isinstance(dictionary, dict) and len(keys) > 0:
        return _recursive_deep_get(dictionary.get(keys[0]), keys[1:])
    elif len(keys) == 0:
        return dictionary
    else:
        return None


def deep_set(dictionary, path, value):
    """deep_set(dict, "a.b.c", "x") -> D[a][b][c] = "x"."""
    keys = path.split(".")
    return _recursive_deep_set(dictionary, keys, value)


def _recursive_deep_set(dictionary, keys, value):
    key = keys[0]
    if len(keys) == 1:
        dictionary[key] = value
    else:
        if dictionary.get(key) is not None and isinstance(dictionary[key], dict):
            dictionary[key] = _recursive_deep_set(dictionary[key], keys[1:], value)
        else:
            dictionary[key] = _recursive_deep_set({}, keys[1:], value)
    return dictionary


def transform_dictionary(dictionary, path_map):
    """Transform a dictionary's structure.

    dictionary -- the original dictionary
    path_map -- mapping of paths in the original dictionary to paths in the new one,
                e.g. {"a.b": "a", "c": "d", "e": "f.g"} to map d2[a] = d1[a][b], d2[d] = d1[c] etc.
    """
    result = {}
    for source_path, destination_path in path_map.iteritems():
        value = deep_get(dictionary, source_path)
        if value is not None:
            deep_set(result, destination_path, value)
    return result
