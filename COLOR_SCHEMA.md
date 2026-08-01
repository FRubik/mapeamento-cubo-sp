# Esquema de cores

Os dois relatórios — a página pública (`index.html`) e o PDF interno dos delegados —
usam a mesma paleta, definida uma única vez em [`brand.py`](brand.py). Nenhum código
novo deve escrever um hex direto: importe de lá.

A paleta parte da identidade visual do Cubing SP: **preto, vermelho e branco**.

## O problema das três cores

Três cores bastam para a identidade (fundo, título, destaque), mas não para gráficos:
um gráfico com duas ou mais séries precisa de matizes que qualquer pessoa consiga
separar — inclusive quem tem daltonismo, que é ~8% dos homens. Preto e branco não
servem como série (são fundo e texto), e vermelho sozinho só resolve uma série.

A solução adotada:

- o **vermelho da marca é a série 1** e a cor de ênfase — é a cor que domina os dois
  documentos, então a identidade se mantém;
- **preto e branco** continuam sendo texto e superfície, como na logo;
- as séries 2 a 5 são matizes de apoio, escolhidos para conviver com o vermelho sem
  competir com ele e para passar nas checagens objetivas descritas abaixo.

## Valores

### Identidade

| Papel | Hex | Onde aparece |
|---|---|---|
| Vermelho da marca | `#cc0a14` | série 1, números-destaque, rótulos de seção, kickers |
| Preto da marca | `#0b0b0b` | capa do PDF, cabeçalho do site, títulos |
| Branco | `#ffffff` | superfície dos gráficos |

O vermelho medido na logo fica entre `#c80008` e `#d00008`; `#cc0a14` é esse mesmo
vermelho ajustado para uso em preenchimento de gráfico (contraste ≥ 3:1 sobre branco).

### Tinta e superfícies

| Papel | Hex |
|---|---|
| `INK` — títulos | `#0b0b0b` |
| `INK2` — texto corrido | `#46443f` |
| `MUTED` — legendas e notas | `#8a8981` |
| `GRID` — grades e filetes | `#e7e6e1` |
| `SOFT` — caixas de destaque | `#faf6f5` |
| `SOFT_LINE` — borda dessas caixas | `#f0dcd9` |

### Séries categóricas (ordem fixa)

| Slot | Hex | Uso |
|---|---|---|
| S1 | `#cc0a14` | série principal — a voz da pesquisa |
| S2 | `#2f66b0` | série 2 — o dado oficial da WCA |
| S3 | `#b8790a` | série 3 |
| S4 | `#00866c` | série 4 |
| S5 | `#7a4aa5` | série 5 |

A ordem é fixa e nunca é reciclada: um sexto grupo vira "Outros" ou um gráfico
separado, não uma cor nova.

**Convenção de leitura nos gráficos de duas séries:** vermelho é o que a comunidade
**quer** (demanda, preferência, desejo declarado); azul é o que **acontece hoje**
(oferta, prática, histórico da WCA). Vale nos dois relatórios — distância desejada ×
praticada, canais preferidos × usados, modalidade pedida × programada.

Passos escuros das mesmas cinco famílias, caso um dia exista modo escuro:
`#e8434b`, `#5b8fd6`, `#bd8420`, `#1aa285`, `#9d78d0`.

### Rampa sequencial — magnitude

Um só matiz, claro → escuro, para "quantas competições": `#e89e95`, `#d8726a`,
`#bf453f`, `#9c2226`, `#730c15`. Ausência de dado é cinza (`#e6e4e1`), fora da rampa.

### Rampa divergente — onde o valor alto é ruim

Distância até a competição mais próxima usa grafite → vermelho: `#3f3e3b`, `#6f6e69`,
`#a8a7a1`, `#d8726a`, `#9c2226`. Assim "quanto mais vermelho, pior" continua valendo,
com as duas cores da marca. Se a rampa sequencial fosse usada aqui, o município **bem**
servido ficaria escuro e a leitura se inverteria.

### Estado

`ALERTA` = `#9c2226` — tarja de confidencialidade e avisos. Reservado: nunca é
usado como série.

## Verificação

A paleta categórica foi validada com o script de checagem de paletas da skill de
dataviz (banda de luminosidade, chroma mínimo, separação sob daltonismo simulado,
contraste sobre a superfície):

| Checagem | Resultado |
|---|---|
| Banda de luminosidade (5 slots, claro) | PASS |
| Chroma mínimo | PASS |
| Separação sob protanopia/deuteranopia (pares adjacentes) | PASS — pior par ΔE 9.6 (mínimo 8) |
| Separação para visão normal | PASS — pior par ΔE 19.8 (mínimo 15) |
| Contraste sobre branco | PASS — todos ≥ 3:1 |
| Idem, três primeiros slots, todos os pares (dispersão/mapa) | PASS — ΔE 8.6 CVD / 17.8 normal |
| Rampa sequencial: luminosidade monotônica, matiz único, ponta clara ≥ 2:1 | PASS |
| Passos escuros (modo escuro) | PASS |

Para revalidar depois de qualquer mudança:

```bash
node <skill-dataviz>/scripts/validate_palette.js "#cc0a14,#2f66b0,#b8790a,#00866c,#7a4aa5" --mode light
node <skill-dataviz>/scripts/validate_palette.js "#e89e95,#d8726a,#bf453f,#9c2226,#730c15" --mode light --ordinal
```

## Regras de uso

1. **Nenhum hex fora de `brand.py`.** Se precisar de uma cor nova, acrescente lá com
   um nome de papel e revalide.
2. **Cor não é o único canal.** Toda série tem rótulo direto ou legenda; nada depende
   apenas da cor para ser lido.
3. **Vermelho é destaque, não decoração.** Gráfico de uma série só usa o vermelho da
   marca; quando há várias séries, o vermelho fica com a que o texto está discutindo.
4. **Texto usa tinta, não cor de série.** Números e rótulos ficam em `INK`/`INK2`;
   quem carrega a identidade é a marca colorida ao lado.
5. **O logotipo não entra nos relatórios** — a identidade vem da paleta. O arquivo
   `logo.jpg` fica fora do versionamento (`.gitignore`).
