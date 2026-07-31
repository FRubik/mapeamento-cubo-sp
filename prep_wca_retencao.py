# -*- coding: utf-8 -*-
"""Retenção de estreantes: quem entrou na comunidade por uma competição paulista
voltou a competir no ano seguinte?

Estreante = pessoa cuja PRIMEIRA competição da WCA (no mundo) foi uma competição
de SP de 2023 em diante. Retido = participou de pelo menos mais uma competição
(em qualquer lugar) dentro de 365 dias após a estreia.

Só entram no cálculo as estreias com 365 dias completos até a data do export —
quem estreou no mês passado ainda não teve chance de voltar.

Saída: estreantes_sp.tsv — person_id, comp_estreia, data_estreia, regiao, retido
"""
import os, json, datetime
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
WCA_DIR = os.path.join(BASE, "WCA_export")

meta = json.load(open(os.path.join(WCA_DIR, "metadata.json")))
DATA_EXPORT = datetime.date.fromisoformat(meta["export_date"][:10])
CORTE = DATA_EXPORT - datetime.timedelta(days=365)
print("export:", DATA_EXPORT, "| estreias consideradas até:", CORTE)

# ---- data de toda competição do mundo (para achar a estreia e o retorno) ----
comp = pd.read_csv(os.path.join(WCA_DIR, "WCA_export_competitions.tsv"),
                   sep="\t", low_memory=False,
                   usecols=["id", "year", "month", "day", "country_id",
                            "city_name", "cancelled"])
comp = comp[(comp.year > 1900) & (comp.month.between(1, 12)) & (comp.day.between(1, 31))]
datas = {r.id: datetime.date(int(r.year), int(r.month), int(r.day))
         for r in comp.itertuples()}

# régua de comparação: estreantes do resto do Brasil no mesmo período
br = comp[(comp.country_id == "Brazil") & (comp.year >= 2023) & (comp.cancelled == 0) &
          (~comp.city_name.str.contains(", São Paulo", na=False))]
resto_br = set(br["id"])

# ---- região da competição de estreia (mesma divisão do relatório) ----
sp = pd.read_csv(os.path.join(BASE, "sp_comps_2023.csv"))
CINTURAO = {"RM de São Paulo", "Campinas", "Santos", "S. J. dos Campos"}
def regiao(r):
    if r.cidade == "São Paulo":
        return "Capital (cidade de São Paulo)"
    if r.RA_nome in CINTURAO:
        return "Grande SP, Campinas, Baixada e Vale"
    return "Interior distante (Norte, Oeste, Sul)"
reg_comp = {r.id: regiao(r) for r in sp.itertuples()}

# ---- uma passada pelos resultados: competições distintas por pessoa ----
pessoa_comps = {}
res = os.path.join(WCA_DIR, "WCA_export_results.tsv")
for chunk in pd.read_csv(res, sep="\t", usecols=["competition_id", "person_id"],
                         chunksize=1_000_000, low_memory=False):
    for cid, pid in zip(chunk["competition_id"], chunk["person_id"]):
        s = pessoa_comps.get(pid)
        if s is None:
            pessoa_comps[pid] = s = set()
        s.add(cid)
print("pessoas no export:", len(pessoa_comps))

linhas = []
for pid, comps in pessoa_comps.items():
    datadas = [(datas[c], c) for c in comps if c in datas]
    if not datadas:
        continue
    d0, c0 = min(datadas)
    if d0 > CORTE:
        continue                      # ainda não teve 12 meses para voltar
    if c0 in reg_comp:
        reg = reg_comp[c0]
    elif c0 in resto_br:
        reg = "Resto do Brasil (referência)"
    else:
        continue                      # não estreou no Brasil em 2023+
    limite = d0 + datetime.timedelta(days=365)
    retido = any(d0 < d <= limite for d, _ in datadas)
    linhas.append((pid, c0, d0.isoformat(), reg, int(retido), len(comps)))

out = pd.DataFrame(linhas, columns=["person_id", "comp_estreia", "data_estreia",
                                    "regiao", "retido", "n_comps"])
out.sort_values("data_estreia").to_csv(
    os.path.join(BASE, "estreantes_sp.tsv"), sep="\t", index=False)

# agregado por região — é o que os relatórios usam e o que vai para o repositório
agg = (out.groupby("regiao")["retido"].agg(estreantes="size", retidos="sum")
          .reset_index())
agg["taxa"] = (agg["retidos"] / agg["estreantes"]).round(4)
agg.to_csv(os.path.join(BASE, "retencao_regiao.tsv"), sep="\t", index=False)

print(f"{len(out)} estreantes em competições de SP (2023+) com janela de 12 meses")
print(agg.to_string(index=False))
