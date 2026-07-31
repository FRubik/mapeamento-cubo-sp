# -*- coding: utf-8 -*-
"""Cobertura populacional: a que distância os paulistas estão da competição mais próxima.

Converte o mapa de territórios em mapa de pessoas. Para cada um dos 645 municípios,
mede a distância do seu centro até a sede de competição mais próxima usada em SP de
2023 em diante, e agrega a população do Censo 2022 por faixa de distância.

Não é distância de estrada: é linha reta (haversine), então subestima o percurso real.
"""
import os, json, math
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))

FAIXAS = [(25, "até 25 km"), (50, "25–50 km"), (100, "50–100 km"),
          (200, "100–200 km"), (float("inf"), "mais de 200 km")]


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))


def _centroides():
    """centro aproximado de cada município (média dos vértices do maior anel)."""
    geo = json.load(open(os.path.join(BASE, "sp_mun.json")))
    out = {}
    for f in geo["features"]:
        g = f["geometry"]
        aneis = [g["coordinates"][0]] if g["type"] == "Polygon" else [p[0] for p in g["coordinates"]]
        maior = max(aneis, key=len)
        xs = [p[0] for p in maior]; ys = [p[1] for p in maior]
        out[f["properties"]["id"]] = (f["properties"]["name"],
                                      sum(ys)/len(ys), sum(xs)/len(xs))
    return out


def municipios(ano=None):
    """DataFrame por município: nome, população, km até a competição mais próxima.

    ano=None usa todas as sedes de 2023 em diante; ano=2025 usa só as daquele ano
    (a leitura mais realista: uma competição isolada em 2023 não atende quem mora
    lá em 2025).
    """
    cent = _centroides()
    pop = json.load(open(os.path.join(BASE, "pop_mun_sp.json")))
    sp = pd.read_csv(os.path.join(BASE, "sp_comps_2023.csv"))
    if ano is not None:
        sp = sp[sp.year == ano]
    sedes = sp[["lat", "lon"]].drop_duplicates().values.tolist()

    linhas = []
    for cod, (nome, lat, lon) in cent.items():
        d = min(_haversine(lat, lon, la, lo) for la, lo in sedes)
        linhas.append(dict(cod=cod, municipio=nome, pop=pop.get(cod, 0), km=d))
    m = pd.DataFrame(linhas)
    m["faixa"] = [next(rot for lim, rot in FAIXAS if k <= lim) for k in m["km"]]
    return m


def por_faixa(m=None):
    """população e nº de municípios em cada faixa de distância, na ordem das faixas."""
    if m is None:
        m = municipios()
    ordem = [rot for _, rot in FAIXAS]
    g = (m.groupby("faixa").agg(pop=("pop", "sum"), municipios=("municipio", "size"))
           .reindex(ordem).fillna(0).astype(int).reset_index())
    g["pct"] = g["pop"] / g["pop"].sum() * 100
    return g


if __name__ == "__main__":
    for ano in (None, 2023, 2024, 2025):
        mm = municipios(ano)
        longe = mm.loc[mm.km > 100, "pop"].sum()
        print(f"{'2023+' if ano is None else ano}: "
              f"{longe/mm['pop'].sum()*100:5.1f}% da população a mais de 100 km "
              f"({longe/1e6:.1f} mi)")
    print()
    m = municipios()
    g = por_faixa(m)
    print(g.to_string(index=False))
    tot = m["pop"].sum()
    longe = m.loc[m.km > 100, "pop"].sum()
    print(f"\npopulação de SP: {tot:,}".replace(",", "."))
    print(f"a mais de 100 km da competição mais próxima: {longe:,}".replace(",", ".")
          + f" ({longe/tot*100:.0f}%)")
    print("\nmaiores cidades a mais de 100 km:")
    print(m[m.km > 100].nlargest(8, "pop")[["municipio", "pop", "km"]]
          .assign(km=lambda d: d.km.round(0)).to_string(index=False))
