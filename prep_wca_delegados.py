# -*- coding: utf-8 -*-
"""Quem sustenta o calendário paulista: delegados e organizadores por competição.

Lê os campos `delegates` e `organizers` do export da WCA — formato
`[{Nome}{mailto:email}] [{Nome}{mailto:email}]` — para as competições de SP de
2023 em diante, e salva um par (competição, pessoa) por linha.

A data da competição vai junto para que a análise possa considerar apenas as
competições **já realizadas** (as futuras já constam no export).

Saída: delegados_sp.tsv — comp_id, ano, data, papel, nome
"""
import os, re
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
WCA_DIR = os.path.join(BASE, "WCA_export")
NOME = re.compile(r"\{([^{}]*)\}\{mailto:")


def _pessoas(campo):
    if not isinstance(campo, str):
        return []
    return [n.strip() for n in NOME.findall(campo) if n.strip()]


sp = pd.read_csv(os.path.join(BASE, "sp_comps_2023.csv"))
comp = pd.read_csv(os.path.join(WCA_DIR, "WCA_export_competitions.tsv"), sep="\t",
                   low_memory=False, usecols=["id", "delegates", "organizers"])
comp = comp[comp["id"].isin(set(sp["id"]))]
ano = dict(zip(sp["id"], sp["year"]))
data = dict(zip(sp["id"], pd.to_datetime(dict(year=sp["year"], month=sp["month"],
                                              day=sp["day"])).dt.strftime("%Y-%m-%d")))

linhas = []
for r in comp.itertuples():
    for papel, campo in (("delegado", r.delegates), ("organizador", r.organizers)):
        for nome in _pessoas(campo):
            linhas.append((r.id, ano[r.id], data[r.id], papel, nome))

out = pd.DataFrame(linhas, columns=["comp_id", "ano", "data", "papel", "nome"])
out.to_csv(os.path.join(BASE, "delegados_sp.tsv"), sep="\t", index=False)
print(f"{len(out)} vínculos em {out.comp_id.nunique()} competições")
for papel in ("delegado", "organizador"):
    sub = out[out.papel == papel]
    print(f"  {papel}s distintos: {sub.nome.nunique()}")
