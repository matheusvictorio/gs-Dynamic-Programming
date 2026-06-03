import csv
import os
import urllib.request

DATA_URL = "https://data.nasa.gov/resource/gh4g-9sfh.csv?$limit=50000"
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'meteorites.csv')


def download_data(logger=None):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    msg = "Baixando base de dados da NASA (Meteorite Landings)..."
    if logger:
        logger(msg)
    else:
        print(msg)
    try:
        urllib.request.urlretrieve(DATA_URL, DATA_PATH)
        ok = f"Download concluido: {DATA_PATH}"
        if logger:
            logger(ok)
        else:
            print(ok)
    except Exception as e:
        raise RuntimeError(f"Erro ao baixar dados: {e}")


def _parse_year(raw):
    if not raw:
        return None
    try:
        return int(str(raw).strip()[:4])
    except ValueError:
        return None


def _parse_float(raw):
    if not raw or str(raw).strip() == '':
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def load_data(logger=None):
    if not os.path.exists(DATA_PATH):
        download_data(logger)

    meteorites = []
    try:
        with open(DATA_PATH, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    meteorite = {
                        'name':     row.get('name', '').strip(),
                        'id':       row.get('id', '').strip(),
                        'nametype': row.get('nametype', '').strip(),
                        'recclass': row.get('recclass', '').strip(),
                        'mass':     _parse_float(row.get('mass (g)')),
                        'fall':     row.get('fall', '').strip(),
                        'year':     _parse_year(row.get('year')),
                        'lat':      _parse_float(row.get('reclat')),
                        'lon':      _parse_float(row.get('reclong')),
                    }
                    meteorites.append(meteorite)
                except Exception:
                    continue
    except FileNotFoundError as e:
        raise RuntimeError(f"Arquivo nao encontrado: {e}")

    return meteorites


def export_to_csv(meteorites, path):
    if not meteorites:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = ['name', 'id', 'nametype', 'recclass', 'mass', 'fall', 'year', 'lat', 'lon']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(meteorites)
