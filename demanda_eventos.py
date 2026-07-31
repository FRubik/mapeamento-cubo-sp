# -*- coding: utf-8 -*-
"""Demanda LATENTE por modalidade: separa "modalidade popular" de "modalidade que falta".

O problema que este módulo resolve: contar quantas pessoas pediram cada evento mede
popularidade, não carência — o 3x3 é o mais pedido em números absolutos e também o
mais oferecido. As três métricas abaixo desfazem essa confusão:

  taxa    = pede / pratica     — entre quem pratica o evento, quantos querem vê-lo mais.
                                 Corrige o viés de tamanho da base. Acima de 100%
                                 significa que há gente pedindo um evento que ainda
                                 nem compete: quer entrar e não tem onde.
  oferta  = % das competições de SP (2023+) que programaram o evento. É a variável
                                 que o organizador de fato controla.
  tracao  = participantes do evento / participantes do 3x3 na MESMA competição, em
                                 média. Mede quanta gente o evento puxa quando entra
                                 no cronograma, sem depender do tamanho da competição.

Participação absoluta NÃO serve como medida de demanda: só existe participante onde
houve oferta, então um evento nunca programado "prova" que ninguém o quer.
"""
import os
from collections import Counter
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))

# rótulo na pesquisa, id na WCA, nome curto para os gráficos
EVENTOS = [
    ("3x3x3", "333", "3x3"),
    ("2x2x2", "222", "2x2"),
    ("4x4x4", "444", "4x4"),
    ("5x5x5", "555", "5x5"),
    ("6x6x6", "666", "6x6"),
    ("7x7x7", "777", "7x7"),
    ("3x3 Uma Mão (OH)", "333oh", "OH (uma mão)"),
    ("Clock", "clock", "Clock"),
    ("Megaminx", "minx", "Megaminx"),
    ("Pyraminx", "pyram", "Pyraminx"),
    ("Skewb", "skewb", "Skewb"),
    ("Square-1", "sq1", "Square-1"),
    ("3x3 de Olhos Vendados (3BLD)", "333bf", "3BLD"),
    ("4x4 de Olhos Vendados (4BLD)", "444bf", "4BLD"),
    ("5x5 de Olhos Vendados (5BLD)", "555bf", "5BLD"),
    ("3x3 Multi-Blind (MBLD)", "333mbf", "MBLD"),
    ("3x3 Menor Nº de Movimentos (FMC)", "333fm", "FMC"),
]

# limiares dos quadrantes, escolhidos para serem explicáveis em palavras:
TAXA_ALTA = 0.50    # metade ou mais dos praticantes quer ver o evento mais vezes
OFERTA_BAIXA = 1/3  # aparece em menos de uma competição a cada três


def _multi_count(df, col):
    c = Counter()
    for v in df[col].dropna():
        for p in str(v).split(";"):
            p = p.strip()
            if p:
                c[p] += 1
    return c


def tabela(df=None):
    """DataFrame por evento com pratica, pede, taxa, oferta, tracao, media_part, latente."""
    if df is None:
        df = pd.read_csv(os.path.join(BASE, "Mapeamento_SP_limpo_com_RA.csv"))
    C = list(df.columns)
    pratica = _multi_count(df, C[8])   # eventos que COMPETE
    pede = _multi_count(df, C[9])      # eventos que GOSTARIA de ver mais

    ep = pd.read_csv(os.path.join(BASE, "event_participants.tsv"), sep="\t")
    n_comps = ep["competition_id"].nunique()
    base333 = ep[ep.event_id == "333"].set_index("competition_id")["n_pessoas"].to_dict()

    linhas = []
    for rotulo, eid, nome in EVENTOS:
        sub = ep[ep.event_id == eid]
        shares = [r.n_pessoas / base333[r.competition_id] for r in sub.itertuples()
                  if base333.get(r.competition_id)]
        pr, pe = pratica.get(rotulo, 0), pede.get(rotulo, 0)
        linhas.append(dict(
            evento=nome, event_id=eid,
            pratica=pr, pede=pe,
            taxa=(pe / pr) if pr else 0.0,
            oferta=len(sub) / n_comps,
            media_part=float(sub["n_pessoas"].mean()) if len(sub) else 0.0,
            tracao=(sum(shares) / len(shares)) if shares else 0.0,
        ))
    t = pd.DataFrame(linhas)
    t["latente"] = (t["taxa"] >= TAXA_ALTA) & (t["oferta"] <= OFERTA_BAIXA)
    return t.sort_values("taxa", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    t = tabela()
    pd.set_option("display.width", 200)
    print(t.assign(taxa=lambda d: (d.taxa*100).round(0),
                   oferta=lambda d: (d.oferta*100).round(0),
                   tracao=lambda d: (d.tracao*100).round(0),
                   media_part=lambda d: d.media_part.round(1)).to_string(index=False))
    print("\ndemanda latente:", ", ".join(t.loc[t.latente, "evento"]))
