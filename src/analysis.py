def general_stats(meteorites):
    total = len(meteorites)
    masses = [m['mass'] for m in meteorites if m['mass'] is not None]
    years = [m['year'] for m in meteorites if m['year'] is not None]

    stats = {'total': total}
    if masses:
        stats['com_massa'] = len(masses)
        stats['massa_total_kg'] = round(sum(masses) / 1000, 2)
        stats['massa_media_g'] = round(sum(masses) / len(masses), 2)
        stats['massa_maxima_g'] = max(masses)
        stats['massa_minima_g'] = min(masses)
    if years:
        stats['ano_mais_antigo'] = min(years)
        stats['ano_mais_recente'] = max(years)

    classes = {}
    for m in meteorites:
        c = m['recclass'] or 'Desconhecida'
        classes[c] = classes.get(c, 0) + 1
    stats['top_classes'] = sorted(classes.items(), key=lambda x: x[1], reverse=True)[:10]
    stats['total_classes'] = len(classes)
    return stats


def geographic_distribution(meteorites):
    dist = {
        'Hemisferio Norte': 0,
        'Hemisferio Sul': 0,
        'Sem coordenadas': 0,
    }
    for m in meteorites:
        if m['lat'] is None:
            dist['Sem coordenadas'] += 1
        elif m['lat'] >= 0:
            dist['Hemisferio Norte'] += 1
        else:
            dist['Hemisferio Sul'] += 1
    return dist


def temporal_distribution(meteorites):
    by_century = {}
    for m in meteorites:
        if m['year']:
            century = (m['year'] // 100) * 100
            label = f"{century}-{century + 99}"
            by_century[label] = by_century.get(label, 0) + 1
    return dict(sorted(by_century.items()))


def fell_vs_found(meteorites):
    counts = {}
    for m in meteorites:
        key = m['fall'] or 'Desconhecido'
        counts[key] = counts.get(key, 0) + 1
    return counts
