def linear_search(data, query, field):
    """Busca linear por substring no campo especificado. O(n)."""
    query_lower = query.lower()
    return [
        item for item in data
        if query_lower in str(item.get(field, '')).lower()
    ]


def binary_search_by_year(sorted_data, target_year):
    """
    Busca binária em lista ordenada por ano. O(log n) para encontrar posição,
    depois expansão linear para coletar todos os registros do mesmo ano.
    Requer que sorted_data esteja ordenado por 'year' (Nones no final).
    """
    valid = [m for m in sorted_data if m.get('year') is not None]
    lo, hi = 0, len(valid) - 1
    found_idx = -1

    while lo <= hi:
        mid = (lo + hi) // 2
        mid_year = valid[mid]['year']
        if mid_year == target_year:
            found_idx = mid
            break
        elif mid_year < target_year:
            lo = mid + 1
        else:
            hi = mid - 1

    if found_idx == -1:
        return []

    results = []
    i = found_idx
    while i >= 0 and valid[i]['year'] == target_year:
        results.append(valid[i])
        i -= 1
    i = found_idx + 1
    while i < len(valid) and valid[i]['year'] == target_year:
        results.append(valid[i])
        i += 1
    return results
