# Mapeamento da Comunidade Paulista de Cubo Mágico

Análise de uma pesquisa feita com a comunidade de cubo mágico de São Paulo (2026),
cruzada com o histórico oficial de competições da **WCA** (World Cube Association).

O objetivo foi entender quem é a comunidade, de onde vêm as pessoas, o que atrapalha
a participação e onde acontecem (ou faltam) campeonatos no estado.

## 📄 Relatório público

O resultado final, pensado para todos os públicos, é uma página única e interativa:

- **[`index.html`](index.html)** — gráficos interativos (Plotly),
  autocontido (funciona offline, sem dependências externas).

> O arquivo já se chama `index.html`: basta ativar o Pages nas configurações do repositório.

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
| `index.html` | Relatório público final (interativo). |
| `limpar_respostas.py` | Limpa o CSV bruto do formulário: normaliza a cidade digitada e acrescenta `Cidade (limpa)`, `UF` e `Região Administrativa`. |
| `brand.py` | Paleta única dos dois relatórios, derivada da identidade visual do Cubing SP. |
| `COLOR_SCHEMA.md` | O esquema de cores: valores, papéis, convenções e as checagens de acessibilidade. |
| `build_html.py` | Gera as figuras Plotly a partir dos dados. |
| `assemble.py` | Monta o HTML final (texto + gráficos). |
| `mapdata.py` | Associa cada município de SP à sua Região Administrativa e dissolve os polígonos. |
| `prep_wca.py` | Extrai do export da WCA os dados de competições usados na análise. |
| `prep_wca_eventos.py` | Extrai quantas pessoas competiram cada evento em cada competição de SP. |
| `prep_wca_retencao.py` | Estreantes em competições de SP e se voltaram a competir em 12 meses. |
| `prep_wca_delegados.py` | Delegados e organizadores de cada competição paulista, com a data da competição (permite considerar só o que já aconteceu). |
| `prep_pop_ibge.py` | Baixa a população dos municípios de SP (Censo 2022). |
| `demanda_eventos.py` | Demanda **latente** por modalidade: separa "popular" de "está faltando". |
| `cobertura.py` | Distância de cada município à competição mais próxima, ponderada pela população. |
| `sp_comps_2023.csv` | Competições oficiais de SP (2023+), já localizadas por RA. |
| `event_freq.tsv` | Frequência de cada evento nas competições de SP. |
| `event_participants.tsv` | Competidores por evento em cada competição de SP. |
| `retencao_regiao.tsv` | Estreantes e taxa de retorno em 12 meses, por região da 1ª competição. |
| `pop_mun_sp.json` | População dos 645 municípios de SP (Censo 2022). |
| `comp_competitors.tsv` | Nº de competidores por competição. |
| `ra_sp.geojson` | As 16 Regiões Administrativas de SP (contornos). |
| `sp_mun.json`, `mun2ra.json` | Malha municipal de SP e mapeamento município → RA. |

## 🔁 Como reproduzir

```bash
python -m venv venv && source venv/bin/activate
pip install pandas numpy matplotlib shapely plotly

# limpar as respostas brutas do formulário (gera Mapeamento_SP_limpo_com_RA.csv)
python limpar_respostas.py

# (opcional) reextrair os dados da WCA — requer a pasta WCA_export/ baixada
python prep_wca.py            # competições de SP (2023+), por RA
python prep_wca_eventos.py    # competidores por evento
python prep_wca_retencao.py   # estreantes e retenção em 12 meses
python prep_wca_delegados.py  # delegados e organizadores (só relatório interno)
python prep_pop_ibge.py       # população municipal (Censo 2022)

# conferir as métricas derivadas
python demanda_eventos.py
python cobertura.py

# gerar as figuras e montar o HTML público
python build_html.py
python assemble.py
```

`limpar_respostas.py` avisa no terminal toda cidade que não conseguiu casar com a lista
oficial de municípios — nesse caso, basta acrescentá-la aos dicionários do próprio script.

Rodar o `build_html.py` a partir da pesquisa completa exige o CSV bruto das respostas,
que **não** é distribuído. Os arquivos agregados incluídos aqui permitem reproduzir a
parte de competições e inspecionar toda a metodologia.

## 📚 Fontes de dados

- **Pesquisa da comunidade** — formulário aberto, respostas voluntárias (2026). Retrato de
  quem participou, não uma amostra estatística.
- **Competições** — [WCA Results Export](https://www.worldcubeassociation.org/export/results) (dado público oficial).
- **Malha geográfica** — municípios de SP ([IBGE / geodata-br](https://github.com/tbrugz/geodata-br)),
  agrupados nas 16 Regiões Administrativas do estado.
- **População** — [Censo 2022, tabela 4709 (IBGE)](https://sidra.ibge.gov.br/tabela/4709), usada
  para ponderar a distância até a competição mais próxima.

---

Gerado com apoio de análise assistida. Números de 2026; o ano de 2026 está incompleto no
recorte da WCA.
