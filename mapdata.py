# -*- coding: utf-8 -*-
"""Prepara dados do mapa: cada município de SP -> RA -> nº de respostas."""
import json, re, unicodedata, os
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon as MplPoly
from matplotlib.collections import PatchCollection

BASE = os.path.dirname(os.path.abspath(__file__))

def _norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"\s+", " ", s)

# CSV RA -> rótulo RA da Wikipédia (as 16 RAs; nem todas têm respostas)
CSV2WIKI = {
    "RM de São Paulo": "1ª Grande SP",
    "RA de Campinas": "5ª Campinas",
    "RA de Santos": "2ª Santos",
    "RA de São José dos Campos": "3ª São José dos Campos",
    "RA de Ribeirão Preto": "6ª Ribeirão Preto",
    "RA de Itapeva": "16ª Itapeva",
    "RA de Presidente Prudente": "10ª Presidente Prudente",
    "RA de Barretos": "13ª Barretos",
    "RA de Franca": "14ª Franca",
    "RA de Sorocaba": "4ª Sorocaba",
    "RA de São José do Rio Preto": "8ª São José do Rio Preto",
    "RA de Bauru": "7ª Bauru",
    "RA de Araçatuba": "9ª Araçatuba",
    "RA de Marília": "11ª Marília",
    "RA de Registro": "2Aª Registro",
    "RA Central": "12ª Central",
}
# nome bonito para exibir por rótulo wiki
WIKI_NICE = {
    "1ª Grande SP": "RM de São Paulo",
    "5ª Campinas": "Campinas",
    "2ª Santos": "Santos",
    "3ª São José dos Campos": "S. J. dos Campos",
    "6ª Ribeirão Preto": "Ribeirão Preto",
    "16ª Itapeva": "Itapeva",
    "10ª Presidente Prudente": "Pres. Prudente",
    "13ª Barretos": "Barretos",
    "14ª Franca": "Franca",
    "4ª Sorocaba": "Sorocaba",
    "2Aª Registro": "Registro",
    "7ª Bauru": "Bauru",
    "8ª São José do Rio Preto": "S. J. Rio Preto",
    "9ª Araçatuba": "Araçatuba",
    "11ª Marília": "Marília",
    "12ª Central": "Central",
}
ALIAS = {  # nome no geojson -> nome na Wikipédia
    "Biritiba-Mirim": "Biritiba Mirim",
    "Embu": "Embu das Artes",
    "Florínia": "Florínea",
    "Luís Antônio": "Luiz Antônio",
    "Moji Mirim": "Mogi Mirim",
    "São Luís do Paraitinga": "São Luiz do Paraitinga",
}

def load():
    mun2ra = json.load(open(os.path.join(BASE, "mun2ra.json")))
    mun2ra_n = {_norm(k): v for k, v in mun2ra.items()}
    alias_n = {_norm(k): _norm(v) for k, v in ALIAS.items()}
    geo = json.load(open(os.path.join(BASE, "sp_mun.json")))
    df = pd.read_csv(os.path.join(BASE, "..", "..", "..", "Mapeamento_SP_limpo_com_RA.csv")) \
         if False else pd.read_csv(os.path.join("Mapeamento_SP_limpo_com_RA.csv"))
    ra_counts_csv = df["Região Administrativa"].value_counts().to_dict()
    # contagem por rótulo wiki
    wiki_counts = {}
    for csvra, wiki in CSV2WIKI.items():
        wiki_counts[wiki] = ra_counts_csv.get(csvra, 0)

    # montar polígonos por município com sua RA e contagem
    feats = []
    for f in geo["features"]:
        nm = f["properties"]["name"]
        key = _norm(nm)
        if key in alias_n:
            key = alias_n[key]
        ra = mun2ra_n.get(key)
        cnt = wiki_counts.get(ra, 0)
        polys = []
        g = f["geometry"]
        if g["type"] == "Polygon":
            rings = [g["coordinates"][0]]
        else:
            rings = [p[0] for p in g["coordinates"]]
        for ring in rings:
            polys.append(np.array(ring))
        feats.append({"name": nm, "ra": ra, "count": cnt, "rings": polys})
    return feats, wiki_counts

def ra_outlines(feats):
    """Dissolve os municípios por RA e devolve as linhas de contorno de cada RA
    como lista de arrays (x,y). Também devolve o contorno externo do estado."""
    from shapely.geometry import Polygon as ShPoly
    from shapely.ops import unary_union
    by_ra = {}
    all_polys = []
    for f in feats:
        if not f["ra"]:
            continue
        polys = []
        for ring in f["rings"]:
            if len(ring) >= 4:
                try:
                    p = ShPoly(ring).buffer(0)  # buffer(0) conserta pequenas invalidezes
                    if not p.is_empty:
                        polys.append(p)
                except Exception:
                    pass
        by_ra.setdefault(f["ra"], []).extend(polys)
        all_polys.extend(polys)

    def to_lines(geom):
        lines = []
        geoms = getattr(geom, "geoms", [geom])
        for g in geoms:
            if g.geom_type == "Polygon":
                lines.append(np.array(g.exterior.coords))
                for interior in g.interiors:
                    lines.append(np.array(interior.coords))
        return lines

    ra_lines = {}
    for ra, polys in by_ra.items():
        merged = unary_union(polys)
        ra_lines[ra] = to_lines(merged)
    state = to_lines(unary_union(all_polys))
    return ra_lines, state

def ra_centroids(feats):
    """centróide aproximado (média de vértices) por RA."""
    acc = {}
    for f in feats:
        if not f["ra"]:
            continue
        for ring in f["rings"]:
            acc.setdefault(f["ra"], []).append(ring)
    cent = {}
    for ra, rings in acc.items():
        allpts = np.vstack(rings)
        cent[ra] = (allpts[:, 0].mean(), allpts[:, 1].mean())
    return cent
