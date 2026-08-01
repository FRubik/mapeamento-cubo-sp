# -*- coding: utf-8 -*-
"""Paleta única dos dois relatórios, derivada da identidade visual do Cubing SP.

A marca tem três cores: preto, vermelho e branco. Isso basta para a identidade
(títulos, destaques, superfícies), mas não para gráficos — séries diferentes
precisam de matizes distinguíveis, inclusive por quem tem daltonismo. Então o
vermelho da marca é a série 1 e a cor de ênfase, o preto/branco formam a base
de texto e fundo, e as séries seguintes são matizes de apoio escolhidos para
passar nas checagens de contraste e separação (ver COLOR_SCHEMA.md).

Importe daqui — nenhum hex deve ser escrito direto em build_html.py ou gen_pdf.py.
"""

# --- identidade (medida na logo) ---------------------------------------------
BRAND_RED   = "#cc0a14"   # vermelho do logotipo, ajustado para uso em gráfico
BRAND_BLACK = "#0b0b0b"   # fundo do logotipo
BRAND_WHITE = "#ffffff"

# --- tinta e superfícies ------------------------------------------------------
INK    = BRAND_BLACK      # títulos
INK2   = "#46443f"        # texto corrido
MUTED  = "#8a8981"        # legendas, notas de rodapé
GRID   = "#e7e6e1"        # grades e filetes
SURF   = BRAND_WHITE      # superfície dos gráficos
SOFT   = "#faf6f5"        # caixas de destaque (vermelho lavado)
SOFT_LINE = "#f0dcd9"     # borda das caixas de destaque

# --- séries categóricas (ordem fixa; nunca reciclar) --------------------------
# Validadas em light: banda de luminosidade, chroma, separação CVD (protan/deutan)
# e contraste >= 3:1. Os três primeiros slots também passam em all-pairs.
S1 = BRAND_RED            # série principal / ênfase
S2 = "#2f66b0"            # azul-aço
S3 = "#b8790a"            # âmbar
S4 = "#00866c"            # verde-petróleo
S5 = "#7a4aa5"            # roxo
CAT = [S1, S2, S3, S4, S5]

# passos escuros das mesmas cinco famílias, caso um dia exista modo escuro
CAT_DARK = ["#e8434b", "#5b8fd6", "#bd8420", "#1aa285", "#9d78d0"]

# --- rampa sequencial (magnitude): um só matiz, claro -> escuro ---------------
SEQ = ["#e89e95", "#d8726a", "#bf453f", "#9c2226", "#730c15"]
SEQ_ZERO = "#e6e4e1"      # ausência de dado (cinza, fora da rampa)

# --- estado (uso reservado; nunca como série) ---------------------------------
ALERTA = "#9c2226"        # tarja de confidencialidade, avisos

# --- rampa divergente: neutro (ok) -> vermelho (problema) ---------------------
# Usada onde o valor alto é ruim — distância até a competição mais próxima.
# Mantém a leitura "quanto mais vermelho, pior" nas duas cores da marca.
DIV = ["#3f3e3b", "#6f6e69", "#a8a7a1", SEQ[1], SEQ[3]]

# --- rampa do mapa: faixas de competições por região --------------------------
MAP_CLASSES = [("Sem competição", SEQ_ZERO), ("1–2", SEQ[0]), ("3–5", SEQ[1]),
               ("6–10", SEQ[2]), ("11+", SEQ[3])]


def map_color(n):
    """Cor de uma região pelo número de competições (mesma rampa nos dois relatórios)."""
    if n == 0:  return SEQ_ZERO
    if n <= 2:  return SEQ[0]
    if n <= 5:  return SEQ[1]
    if n <= 10: return SEQ[2]
    return SEQ[3]


def texto_sobre(cor):
    """Tinta legível sobre um preenchimento da rampa."""
    return BRAND_WHITE if cor in (SEQ[2], SEQ[3], SEQ[4]) else INK
