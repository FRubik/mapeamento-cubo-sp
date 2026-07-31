# -*- coding: utf-8 -*-
"""Baixa a população dos 645 municípios de SP (Censo 2022, IBGE) e salva
pop_mun_sp.json — código IBGE (7 dígitos) -> população residente.

Fonte: API de agregados do IBGE, tabela 4709 (Censo 2022), variável 93.
Dado público oficial; roda uma vez e o JSON fica versionado no repositório.
"""
import os, json, gzip, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
URL = ("https://servicodados.ibge.gov.br/api/v3/agregados/4709/periodos/2022"
       "/variaveis/93?localidades=N6[N3[35]]")

req = urllib.request.Request(URL, headers={"Accept-Encoding": "identity"})
with urllib.request.urlopen(req, timeout=120) as r:
    bruto = r.read()
if bruto[:2] == b"\x1f\x8b":          # a API responde gzip mesmo pedindo identity
    bruto = gzip.decompress(bruto)
dados = json.loads(bruto.decode("utf-8"))

pop = {}
for serie in dados[0]["resultados"][0]["series"]:
    cod = serie["localidade"]["id"]
    valor = serie["serie"]["2022"]
    pop[cod] = int(valor)

json.dump(pop, open(os.path.join(BASE, "pop_mun_sp.json"), "w"))
print(f"{len(pop)} municípios · população total {sum(pop.values()):,}".replace(",", "."))
