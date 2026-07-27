# Mapeamento da Comunidade Paulista de Cubo Mágico

Análise de uma pesquisa feita com a comunidade de cubo mágico de São Paulo (2026),
cruzada com o histórico oficial de competições da **WCA** (World Cube Association).

O objetivo foi entender quem é a comunidade, de onde vêm as pessoas, o que atrapalha
a participação e onde acontecem (ou faltam) campeonatos no estado.

## 📄 Relatório público

O resultado final, pensado para todos os públicos, é uma página única e interativa:

- **[`relatorio_publico.html`](relatorio_publico.html)** — gráficos interativos (Plotly),
  autocontido (funciona offline, sem dependências externas).

> Para publicar como site (GitHub Pages), renomeie/duplique o arquivo como `index.html`
> e ative o Pages nas configurações do repositório.

## 🔒 Confidencialidade

Foi prometido sigilo a quem respondeu à pesquisa. Por isso:

- As **respostas brutas** (com nome, WhatsApp e e-mail) **não** estão no repositório.
- No material público, a origem das respostas aparece apenas em **grandes blocos
  regionais**, nunca por cidade ou região específica.
- O relatório técnico detalhado (por Região Administrativa, com falas literais) é de uso
  interno da delegação e **não** é publicado aqui.

Os arquivos sensíveis estão listados no [`.gitignore`](.gitignore).

## 🗂️ Estrutura

| Arquivo | O que é |
|---|---|
| `relatorio_publico.html` | Relatório público final (interativo). |
| `build_html.py` | Gera as figuras Plotly a partir dos dados. |
| `assemble.py` | Monta o HTML final (texto + gráficos). |
| `mapdata.py` | Associa cada município de SP à sua Região Administrativa e dissolve os polígonos. |
| `prep_wca.py` | Extrai do export da WCA os dados de competições usados na análise. |
| `sp_comps_2023.csv` | Competições oficiais de SP (2023+), já localizadas por RA. |
| `event_freq.tsv` | Frequência de cada evento nas competições de SP. |
| `comp_competitors.tsv` | Nº de competidores por competição. |
| `ra_sp.geojson` | As 16 Regiões Administrativas de SP (contornos). |
| `sp_mun.json`, `mun2ra.json` | Malha municipal de SP e mapeamento município → RA. |

## 🔁 Como reproduzir

```bash
python -m venv venv && source venv/bin/activate
pip install pandas numpy shapely plotly kaleido

# (opcional) reextrair os dados da WCA — requer a pasta WCA_export/ baixada
python prep_wca.py

# gerar as figuras e montar o HTML público
python build_html.py
python assemble.py
```

Rodar o `build_html.py` a partir da pesquisa completa exige o CSV bruto das respostas,
que **não** é distribuído. Os arquivos agregados incluídos aqui permitem reproduzir a
parte de competições e inspecionar toda a metodologia.

## 📚 Fontes de dados

- **Pesquisa da comunidade** — formulário aberto, respostas voluntárias (2026). Retrato de
  quem participou, não uma amostra estatística.
- **Competições** — [WCA Results Export](https://www.worldcubeassociation.org/export/results) (dado público oficial).
- **Malha geográfica** — municípios de SP ([IBGE / geodata-br](https://github.com/tbrugz/geodata-br)),
  agrupados nas 16 Regiões Administrativas do estado.

---

Gerado com apoio de análise assistida. Números de 2026; o ano de 2026 está incompleto no
recorte da WCA.
