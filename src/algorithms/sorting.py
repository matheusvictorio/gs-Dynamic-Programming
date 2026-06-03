def quick_sort(data, key_func, reverse=False):
    """Quick Sort recursivo. Valores None sempre vão para o final."""
    valid = [x for x in data if key_func(x) is not None]
    nones = [x for x in data if key_func(x) is None]
    sorted_valid = _quick_sort_impl(valid, key_func)
    if reverse:
        sorted_valid = sorted_valid[::-1]
    return sorted_valid + nones


def _quick_sort_impl(data, key_func):
    if len(data) <= 1:
        return data
    pivot_val = key_func(data[len(data) // 2])
    left = [x for x in data if key_func(x) < pivot_val]
    middle = [x for x in data if key_func(x) == pivot_val]
    right = [x for x in data if key_func(x) > pivot_val]
    return _quick_sort_impl(left, key_func) + middle + _quick_sort_impl(right, key_func)


def merge_sort(data, key_func, reverse=False):
    """Merge Sort estável. Valores None sempre vão para o final."""
    valid = [x for x in data if key_func(x) is not None]
    nones = [x for x in data if key_func(x) is None]
    sorted_valid = _merge_sort_impl(valid, key_func)
    if reverse:
        sorted_valid = sorted_valid[::-1]
    return sorted_valid + nones


def _merge_sort_impl(data, key_func):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = _merge_sort_impl(data[:mid], key_func)
    right = _merge_sort_impl(data[mid:], key_func)
    return _merge(left, right, key_func)


def _merge(left, right, key_func):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
