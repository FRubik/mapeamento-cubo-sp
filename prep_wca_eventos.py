# -*- coding: utf-8 -*-
"""Extrai, do export da WCA, quantas pessoas distintas competiram cada evento em
cada competição de SP (2023+).

Saída: event_participants.tsv  — competition_id, event_id, n_pessoas
Serve para medir a TRAÇÃO de cada modalidade (quanta gente ela puxa quando é
oferecida), e não só em quantas competições ela apareceu.
"""
import os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
WCA_DIR = os.path.join(BASE, "WCA_export")

sp = pd.read_csv(os.path.join(BASE, "sp_comps_2023.csv"))
ids = set(sp["id"])

vistos = set()          # (comp, evento, pessoa)
cont = {}               # (comp, evento) -> nº de pessoas
res = os.path.join(WCA_DIR, "WCA_export_results.tsv")
for chunk in pd.read_csv(res, sep="\t",
                         usecols=["competition_id", "event_id", "person_id"],
                         chunksize=500_000, low_memory=False):
    chunk = chunk[chunk["competition_id"].isin(ids)]
    for cid, eid, pid in zip(chunk["competition_id"], chunk["event_id"], chunk["person_id"]):
        k = (cid, eid, pid)
        if k not in vistos:
            vistos.add(k)
            cont[(cid, eid)] = cont.get((cid, eid), 0) + 1

out = pd.DataFrame([(c, e, n) for (c, e), n in cont.items()],
                   columns=["competition_id", "event_id", "n_pessoas"])
out.sort_values(["competition_id", "event_id"]).to_csv(
    os.path.join(BASE, "event_participants.tsv"), sep="\t", index=False)
print(f"{len(out)} pares competição×evento em {out['competition_id'].nunique()} competições")
