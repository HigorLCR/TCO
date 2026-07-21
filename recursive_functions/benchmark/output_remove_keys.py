
def remove_keys(d, keys):
    while not not keys:
        key = keys[0]
        if key in d:
            del d[key]
        d, keys = (d, keys[1:])
    return d


base_dict = {str(i): i for i in range(500)}
keys_to_remove = [str(i) for i in range(0, 500, 2)]

# --- benchmark ---
def chamada():
    return remove_keys(dict(base_dict), keys_to_remove)
