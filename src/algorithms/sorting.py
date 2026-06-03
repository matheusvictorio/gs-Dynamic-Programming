def _safe_key(func, item, default=float('inf')):
    val = func(item)
    return (1, default) if val is None else (0, val)


def quick_sort(data, key_func, reverse=False):
    """Quick Sort recursivo. Valores None vão para o final."""
    if len(data) <= 1:
        return data
    pivot_val = _safe_key(key_func, data[len(data) // 2])
    left = [x for x in data if _safe_key(key_func, x) < pivot_val]
    middle = [x for x in data if _safe_key(key_func, x) == pivot_val]
    right = [x for x in data if _safe_key(key_func, x) > pivot_val]
    result = quick_sort(left, key_func) + middle + quick_sort(right, key_func)
    return result[::-1] if reverse else result


def merge_sort(data, key_func, reverse=False):
    """Merge Sort estável. Valores None vão para o final."""
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], key_func)
    right = merge_sort(data[mid:], key_func)
    result = _merge(left, right, key_func)
    return result[::-1] if reverse else result


def _merge(left, right, key_func):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        lk = _safe_key(key_func, left[i])
        rk = _safe_key(key_func, right[j])
        if lk <= rk:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
