# -*- coding: utf-8 -*-
"""
Extrai, do export público oficial da WCA, os dados usados nos relatórios:

  1. sp_comps_2023.csv     — competições de SP de 2023 em diante (sem canceladas),
                             cada uma localizada em sua Região Administrativa (RA).
  2. event_freq.tsv        — em quantas dessas competições cada evento apareceu.
  3. comp_competitors.tsv  — nº de competidores distintos por competição.

Pré-requisitos:
  - Pasta WCA_export/ com o export descompactado (baixe em
    https://www.worldcubeassociation.org/export/results). NÃO vai para o Git.
  - ra_sp.geojson (as 16 Regiões Administrativas de SP, já incluído no repo).
  - Dependências: pandas, numpy, shapely.

Uso:  python prep_wca.py
"""
import os, json
import numpy as np
import pandas as pd
from shapely.geometry import shape, Point
from shapely.strtree import STRtree

BASE = os.path.dirname(os.path.abspath(__file__))
WCA_DIR = os.path.join(BASE, "WCA_export")
ANO_MIN = 2023

# ---- polígonos das RAs para localizar cada competição (ponto-em-polígono) ----
geoj = json.load(open(os.path.join(BASE, "ra_sp.geojson")))
ra_names = [f["properties"]["ra"] for f in geoj["features"]]
ra_geoms = [shape(f["geometry"]) for f in geoj["features"]]
tree = STRtree(ra_geoms)

def to_ra(lon, lat):
    pt = Point(lon, lat)
    for i in tree.query(pt):
        if ra_geoms[i].contains(pt):
            return ra_names[i]
    dists = [ra_geoms[i].distance(pt) for i in range(len(ra_geoms))]
    return ra_names[int(np.argmin(dists))]

# ---- 1. competições de SP, 2023+, não canceladas -----------------------------
comp = pd.read_csv(os.path.join(WCA_DIR, "WCA_export_competitions.tsv"),
                   sep="\t", low_memory=False)
sp = comp[(comp["country_id"] == "Brazil") &
          (comp["city_name"].str.contains(", São Paulo", na=False))].copy()
sp = sp[(sp["year"] >= ANO_MIN) & (sp["cancelled"] == 0)]
sp["lat"] = sp["latitude_microdegrees"] / 1e6
sp["lon"] = sp["longitude_microdegrees"] / 1e6
sp["RA_nome"] = [to_ra(lo, la) for lo, la in zip(sp["lon"], sp["lat"])]
sp["cidade"] = sp["city_name"].str.replace(", São Paulo", "", regex=False)
sp["grupo"] = np.where(sp["cidade"] == "São Paulo", "Capital",
              np.where(sp["RA_nome"] == "RM de São Paulo", "RMSP exc. capital",
                       "Interior/Litoral"))
sp[["id", "name", "cidade", "RA_nome", "year", "month", "day", "grupo"]] \
    .to_csv(os.path.join(BASE, "sp_comps_2023.csv"), index=False)
ids = set(sp["id"])
print(f"competições SP {ANO_MIN}+: {len(sp)}")

# ---- 2 e 3. varre os resultados (arquivo grande) por chunks ------------------
seen_ev, seen_pe = set(), set()
ev_cnt, pe_cnt = {}, {}
res_path = os.path.join(WCA_DIR, "WCA_export_results.tsv")
for chunk in pd.read_csv(res_path, sep="\t",
                         usecols=["competition_id", "event_id", "person_id"],
                         chunksize=500_000, low_memory=False):
    chunk = chunk[chunk["competition_id"].isin(ids)]
    for cid, eid, pid in zip(chunk["competition_id"], chunk["event_id"], chunk["person_id"]):
        ke = (cid, eid)
        if ke not in seen_ev:
            seen_ev.add(ke); ev_cnt[eid] = ev_cnt.get(eid, 0) + 1
        kp = (cid, pid)
        if kp not in seen_pe:
            seen_pe.add(kp); pe_cnt[cid] = pe_cnt.get(cid, 0) + 1

(pd.Series(ev_cnt).sort_values(ascending=False)
   .to_csv(os.path.join(BASE, "event_freq.tsv"), sep="\t", header=False))
(pd.Series(pe_cnt)
   .to_csv(os.path.join(BASE, "comp_competitors.tsv"), sep="\t", header=False))
print("event_freq.tsv e comp_competitors.tsv gerados.")
print(f"competições realizadas (com resultados): {len(pe_cnt)}")
