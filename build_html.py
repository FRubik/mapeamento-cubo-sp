# -*- coding: utf-8 -*-
import os, sys, json
# roda sempre a partir da pasta do script (raiz do repositório)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import mapdata

SCR = os.path.dirname(os.path.abspath(__file__))

# ---------------- paleta ----------------
BLUE="#2a78d6"; ORANGE="#eb6834"; AQUA="#1baf7a"; INK="#0b0b0b"; INK2="#52514e"
MUTED="#8a8981"; GRID="#ececE7"; SURF="#ffffff"
MAP_CLASSES = [("Sem competição","#e4e4df"),("1–2","#c6dbef"),("3–5","#8fbfe8"),
               ("6–10","#4a97d8"),("11 ou mais","#1f5fa8")]
MAP_CMAP = {k:v for k,v in MAP_CLASSES}

df = pd.read_csv("Mapeamento_SP_limpo_com_RA.csv")
C = list(df.columns)
N = len(df)

def multi_count(col):
    c=Counter()
    for v in df[col].dropna():
        for p in str(v).split(";"):
            p=p.strip()
            if p: c[p]+=1
    return c

# ---------------- estilo comum ----------------
def style(fig, height=360, legend=False):
    fig.update_layout(
        template="plotly_white", height=height,
        margin=dict(l=8,r=18,t=10,b=8),
        font=dict(family="Inter, Segoe UI, system-ui, -apple-system, sans-serif",
                  size=13, color=INK2),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(font_size=13, font_family="Inter, system-ui, sans-serif"),
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(size=12)),
        dragmode=False,
    )
    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False, automargin=True)
    return fig

CONFIG = {"displayModeBar": False, "responsive": True}
QA = os.environ.get("QA")=="1"
os.makedirs(os.path.join(SCR,"qa"), exist_ok=True)
def emb(fig, div_id):
    if QA:
        try:
            fig.write_image(os.path.join(SCR,"qa",div_id+".png"), width=760,
                            height=fig.layout.height or 360, scale=1.4)
        except Exception as e:
            print("QA falhou", div_id, e)
    return fig.to_html(full_html=False, include_plotlyjs=False,
                       div_id=div_id, config=CONFIG)

def hbar(cats, vals, order=None, color=BLUE, pct=False, suffix="", height=None,
         hovlabel="respostas"):
    data=list(zip(cats,vals))
    if order:
        idx={k:i for i,k in enumerate(order)}
        data=[d for d in data if d[0] in idx]
        data.sort(key=lambda d: idx[d[0]], reverse=True)
    else:
        data.sort(key=lambda d:d[1])
    cats=[d[0] for d in data]; vals=[d[1] for d in data]
    tot=sum(vals) if not pct else 100
    if pct:
        text=[f"{v}" for v in vals]
    else:
        text=[f"{v}" for v in vals]
    fig=go.Figure(go.Bar(
        x=vals, y=cats, orientation="h", marker_color=color,
        text=text, textposition="outside", cliponaxis=False,
        textfont=dict(size=12,color=INK2),
        hovertemplate="%{y}<br><b>%{x}</b> "+hovlabel+"<extra></extra>",
    ))
    h=height or max(240, 34*len(cats)+60)
    style(fig, h)
    fig.update_xaxes(range=[0, max(vals)*1.16])
    fig.update_layout(margin=dict(l=8,r=30,t=10,b=8))
    return fig

def grouped_hbar(cats, a_vals, b_vals, a_name, b_name, height=None, suffix=""):
    order=sorted(range(len(cats)), key=lambda i:a_vals[i])
    cats=[cats[i] for i in order]; a_vals=[a_vals[i] for i in order]; b_vals=[b_vals[i] for i in order]
    fig=go.Figure()
    fig.add_bar(y=cats, x=b_vals, name=b_name, orientation="h", marker_color=ORANGE,
                hovertemplate="%{y}<br>"+b_name+": <b>%{x}"+suffix+"</b><extra></extra>")
    fig.add_bar(y=cats, x=a_vals, name=a_name, orientation="h", marker_color=BLUE,
                hovertemplate="%{y}<br>"+a_name+": <b>%{x}"+suffix+"</b><extra></extra>")
    fig.update_layout(barmode="group", bargap=0.35, bargroupgap=0.08)
    h=height or max(300, 46*len(cats)+70)
    style(fig, h, legend=True)
    fig.update_layout(margin=dict(l=8,r=30,t=34,b=8))
    return fig

DIVS={}

# ============================================================
# PERFIL
# ============================================================
age_order=["Menos de 10 anos","10-12 anos","13-15 anos","16-18 anos","19-24 anos",
           "25-34 anos","35-44 anos","45+ anos"]
ac=df[C[1]].value_counts()
DIVS["idade"]=emb(hbar(list(ac.index),list(ac.values),order=age_order),"g_idade")

exp_order=["6 meses a 1 ano","1-2 anos","2-5 anos","5-10 anos","Mais de 10 anos"]
ec=df[C[4]].value_counts()
DIVS["tempo"]=emb(hbar(list(ec.index),list(ec.values),order=exp_order),"g_tempo")

lvl_order=["Sub-10 (abaixo de 10s)","Entre 10s e 20s","Entre 20s e 30s","Entre 30s e 1 min"]
lc=df[C[5]].value_counts()
DIVS["nivel"]=emb(hbar(list(lc.index),list(lc.values),order=lvl_order),"g_nivel")

freq_order=["Não participo","1 vez por ano","2-3 vezes por ano","A cada 2-3 meses","Mensalmente"]
fc=df[C[7]].value_counts()
DIVS["freq"]=emb(hbar(list(fc.index),list(fc.values),order=freq_order),"g_freq")

comp_order=["Nenhuma","1-2","3-5","6-10","11-20","21-50","51-100","Mais de 100"]
cc=df[C[6]].value_counts()
DIVS["compswca"]=emb(hbar(list(cc.index),list(cc.values),order=comp_order),"g_compswca")

# ============================================================
# GEOGRAFIA — respostas por macrorregião (4 níveis)
# ============================================================
near_ra={"RM de São Paulo","RA de Campinas","RA de Santos","RA de São José dos Campos"}
def tier(r,c):
    if r=="Fora de SP": return "Fora de SP"
    if c=="São Paulo": return "Capital (cidade de São Paulo)"
    if r in near_ra: return "Grande SP, Campinas, Baixada e Vale"
    return "Interior distante (Norte, Oeste, Sul)"
df["tier"]=[tier(r,c) for r,c in zip(df[C[26]],df[C[24]])]
tier_order=["Capital (cidade de São Paulo)","Grande SP, Campinas, Baixada e Vale",
            "Interior distante (Norte, Oeste, Sul)","Fora de SP"]
tc=df["tier"].value_counts()
DIVS["resp_macro"]=emb(hbar(list(tc.index),list(tc.values),order=tier_order,height=280),"g_respmacro")

# ============================================================
# WCA — competições
# ============================================================
sp=pd.read_csv(os.path.join(SCR,"sp_comps_2023.csv"))
# por ano
yr=sp.groupby("year").size()
fig=go.Figure(go.Bar(x=[str(int(y)) for y in yr.index], y=list(yr.values),
    marker_color=[BLUE,BLUE,BLUE,ORANGE], text=list(yr.values), textposition="outside",
    cliponaxis=False, textfont=dict(size=13,color=INK2),
    hovertemplate="%{x}<br><b>%{y}</b> competições<extra></extra>"))
style(fig,300); fig.update_yaxes(showgrid=True,gridcolor=GRID)
fig.update_layout(margin=dict(l=8,r=8,t=10,b=8))
fig.update_yaxes(range=[0,max(yr.values)*1.2])
DIVS["comps_ano"]=emb(fig,"g_compsano")

# por região nomeada (dado público -> pode detalhar)
REG={"RM de São Paulo":"Grande São Paulo (exceto capital)",
     "Santos":"Baixada Santista",
     "Campinas":"Região de Campinas",
     "S. J. dos Campos":"Vale do Paraíba"}
sp["reg"]=np.where(sp["cidade"]=="São Paulo","Capital (cidade de São Paulo)",
    sp["RA_nome"].map(REG).fillna("Demais regiões do interior"))
rx=sp["reg"].value_counts()
DIVS["comps_faixa"]=emb(hbar(list(rx.index),list(rx.values),
    color=BLUE,height=320,hovlabel="competições"),"g_compsfaixa")

# mapa por RA
allras=["RM de São Paulo","Campinas","Santos","S. J. dos Campos","Ribeirão Preto","Itapeva",
        "Pres. Prudente","Barretos","Franca","Sorocaba","S. J. Rio Preto","Registro",
        "Bauru","Central","Marília","Araçatuba"]
racount=sp["RA_nome"].value_counts().to_dict()
def cls(c):
    if c==0: return "Sem competição"
    if c<=2: return "1–2"
    if c<=5: return "3–5"
    if c<=10: return "6–10"
    return "11 ou mais"
mdf=pd.DataFrame({"ra":allras})
mdf["n"]=mdf["ra"].map(lambda r:int(racount.get(r,0)))
mdf["classe"]=mdf["n"].map(cls)
geoj=json.load(open(os.path.join(SCR,"ra_sp.geojson")))
figm=px.choropleth(mdf, geojson=geoj, locations="ra", featureidkey="properties.ra",
    color="classe", color_discrete_map=MAP_CMAP,
    category_orders={"classe":[c[0] for c in MAP_CLASSES]},
    custom_data=["ra","n"])
figm.update_traces(marker_line_color="#ffffff", marker_line_width=0.8,
    hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]} competições (2023+)<extra></extra>")
figm.update_geos(visible=False, fitbounds="locations", projection_type="mercator",
                 bgcolor="rgba(0,0,0,0)")
figm.update_layout(height=460, margin=dict(l=0,r=0,t=10,b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", size=13, color=INK2),
    legend=dict(title="", orientation="h", yanchor="bottom", y=-0.02, x=0.5, xanchor="center"),
    dragmode=False)
DIVS["mapa"]=emb(figm,"g_mapa")

# ============================================================
# DEMANDA x OFERTA de eventos
# ============================================================
wish=multi_count(C[9])   # gostaria de ver mais
ev=pd.read_csv(os.path.join(SCR,"event_freq.tsv"),sep="\t",names=["event_id","n_comps"])
offer={r.event_id:r.n_comps for r in ev.itertuples()}
NCOMPS=88
EVMAP=[("Megaminx","minx","Megaminx"),("Skewb","skewb","Skewb"),("Square-1","sq1","Square-1"),
 ("Clock","clock","Clock"),("Pyraminx","pyram","Pyraminx"),("3x3x3","333","3x3"),
 ("2x2x2","222","2x2"),("3x3 Uma Mão (OH)","333oh","OH (uma mão)"),
 ("4x4x4","444","4x4"),("5x5x5","555","5x5"),
 ("3x3 de Olhos Vendados (3BLD)","333bf","3BLD (às cegas)"),
 ("7x7x7","777","7x7"),("6x6x6","666","6x6"),
 ("3x3 Menor Nº de Movimentos (FMC)","333fm","FMC"),
 ("4x4 de Olhos Vendados (4BLD)","444bf","4BLD"),
 ("5x5 de Olhos Vendados (5BLD)","555bf","5BLD"),
 ("3x3 Multi-Blind (MBLD)","333mbf","MBLD")]
names=[e[2] for e in EVMAP]
demand=[round(wish.get(e[0],0)/N*100) for e in EVMAP]
offerp=[round(offer.get(e[1],0)/NCOMPS*100) for e in EVMAP]
DIVS["dem_of"]=emb(grouped_hbar(names,demand,offerp,
    "Quem quer ver mais (% da pesquisa)","Em % dos campeonatos de SP (2023+)",
    height=560,suffix="%"),"g_demof")

# ============================================================
# COBERTURA POPULACIONAL — o vazio em pessoas
# ============================================================
import cobertura
ANO_COB = 2025
MUN_COB = cobertura.municipios(ANO_COB)
FX = cobertura.por_faixa(MUN_COB)
POP_TOT = int(MUN_COB["pop"].sum())
LONGE = int(MUN_COB.loc[MUN_COB.km > 100, "pop"].sum())
COB_SERIE = {a: int(cobertura.municipios(a).query("km > 100")["pop"].sum())
             for a in (2023, 2024, 2025)}

def _mi(v):
    return f"{v/1e6:.1f}".replace(".", ",")

figc = go.Figure()
for perto, nome, cor in ((True, "a até 100 km de uma competição", BLUE),
                         (False, "a mais de 100 km", ORANGE)):
    sub = FX[FX["faixa"].isin(["até 25 km", "25–50 km", "50–100 km"]) == perto]
    figc.add_bar(y=sub["faixa"], x=sub["pop"]/1e6, name=nome, orientation="h",
                 marker_color=cor,
                 text=[f"{_mi(p)} mi ({q:.0f}%)" for p, q in zip(sub["pop"], sub["pct"])],
                 textposition="outside", cliponaxis=False,
                 textfont=dict(size=12, color=INK2),
                 hovertemplate="%{y}<br><b>%{customdata[0]}</b> pessoas · %{customdata[1]:.0f}% do estado"
                               "<extra></extra>",
                 customdata=np.stack([[f"{p:,}".replace(",", ".") for p in sub["pop"]],
                                      sub["pct"]], axis=-1))
style(figc, 380, legend=True)
figc.update_yaxes(categoryorder="array", categoryarray=list(FX["faixa"])[::-1])
figc.update_xaxes(range=[0, (FX["pop"].max()/1e6)*1.35],
                  title_text="milhões de habitantes", title_font_size=12)
figc.update_layout(margin=dict(l=8, r=30, t=36, b=8), bargap=0.34)
DIVS["cobertura"] = emb(figc, "g_cobertura")

# ============================================================
# RETENÇÃO DE ESTREANTES
# ============================================================
EST = pd.read_csv(os.path.join(SCR, "retencao_regiao.tsv"), sep="\t").set_index("regiao")
REF_BR = "Resto do Brasil (referência)"
REG_ORD = ["Capital (cidade de São Paulo)", "Grande SP, Campinas, Baixada e Vale",
           "Interior distante (Norte, Oeste, Sul)", REF_BR]
RET = EST.reindex(REG_ORD).rename(columns={"estreantes": "size", "taxa": "mean"})
_sp = RET.drop(index=REF_BR)
N_ESTREANTES_SP = int(_sp["size"].sum())
RET_SP = float(_sp["retidos"].sum() / N_ESTREANTES_SP)

figr = go.Figure()
for reg_sel, nome, cor in (([r for r in REG_ORD if r != REF_BR], "Competições de SP", AQUA),
                           ([REF_BR], "Média nacional", "#b9b9b3")):
    sub = RET.loc[reg_sel]
    figr.add_bar(y=[r.replace(" (referência)", "") for r in sub.index],
                 x=sub["mean"]*100, name=nome, orientation="h", marker_color=cor,
                 text=[f"{v*100:.0f}%" for v in sub["mean"]],
                 textposition="outside", cliponaxis=False,
                 textfont=dict(size=12, color=INK2),
                 customdata=sub["size"],
                 hovertemplate="%{y}<br><b>%{x:.0f}%</b> voltaram em até 12 meses"
                               "<br>%{customdata} estreantes<extra></extra>")
style(figr, 340, legend=True)
figr.update_yaxes(categoryorder="array",
                  categoryarray=[r.replace(" (referência)", "") for r in REG_ORD][::-1])
figr.update_xaxes(range=[0, 75], ticksuffix="%")
figr.update_layout(margin=dict(l=8, r=30, t=36, b=8), bargap=0.34)
DIVS["retencao"] = emb(figr, "g_retencao")

ENT = _sp["size"].astype(int)
fige = go.Figure(go.Bar(
    y=list(ENT.index), x=list(ENT.values), orientation="h", marker_color=BLUE,
    text=[f"{v} ({v/N_ESTREANTES_SP*100:.0f}%)" for v in ENT.values],
    textposition="outside", cliponaxis=False, textfont=dict(size=12, color=INK2),
    hovertemplate="%{y}<br><b>%{x}</b> estreantes<extra></extra>"))
style(fige, 340)
fige.update_yaxes(categoryorder="array", categoryarray=list(ENT.index)[::-1])
fige.update_xaxes(range=[0, ENT.max()*1.3])
fige.update_layout(margin=dict(l=8, r=30, t=10, b=8), bargap=0.34)
DIVS["entrada"] = emb(fige, "g_entrada")

# ============================================================
# DEMANDA LATENTE — popular × esquecido
# ============================================================
import demanda_eventos
DE = demanda_eventos.tabela(df)
LAT_AZUL = "#9fb6d4"

def _quadrante(sub, nome, cor):
    return go.Scatter(
        x=sub["oferta"]*100, y=sub["taxa"]*100, name=nome, mode="markers+text",
        text=["OH" if e.startswith("OH") else e for e in sub["evento"]],
        textposition=sub["textpos"], textfont=dict(size=11, color=INK2),
        marker=dict(size=sub["pratica"], sizemode="area",
                    sizeref=2.*DE["pratica"].max()/(34.**2), sizemin=6,
                    color=cor, line=dict(color=SURF, width=1.5)),
        customdata=np.stack([sub["evento"], sub["pratica"], sub["pede"]], axis=-1),
        hovertemplate="<b>%{customdata[0]}</b><br>aparece em %{x:.0f}% das competições<br>"
                      "%{y:.0f}% de quem pratica quer ver mais<br>"
                      "%{customdata[1]} praticantes · %{customdata[2]} pedidos<extra></extra>",
    )

TEXTPOS = {"5BLD":"bottom center","Skewb":"bottom center","6x6":"bottom left",
           "OH (uma mão)":"middle right","5x5":"top left","4x4":"top right"}
DE["textpos"] = [TEXTPOS.get(e, "top center") for e in DE["evento"]]
figq = go.Figure()
figq.add_shape(type="rect", x0=0, x1=demanda_eventos.OFERTA_BAIXA*100,
               y0=demanda_eventos.TAXA_ALTA*100, y1=132,
               fillcolor="#fdf1ea", line_width=0, layer="below")
figq.add_vline(x=demanda_eventos.OFERTA_BAIXA*100, line_color=GRID, line_width=1)
figq.add_hline(y=demanda_eventos.TAXA_ALTA*100, line_color=GRID, line_width=1)
figq.add_trace(_quadrante(DE[DE.latente], "Muito pedido, pouco programado", ORANGE))
figq.add_trace(_quadrante(DE[~DE.latente], "Já bem atendidos", LAT_AZUL))
figq.add_annotation(x=1.5, y=130, text="<b>DEMANDA LATENTE</b>", showarrow=False,
                    xanchor="left", yanchor="top", font=dict(size=12, color=ORANGE))
style(figq, 520, legend=True)
figq.update_xaxes(title_text="Em quantas competições de SP a modalidade aparece (2023+)",
                  range=[0, 76], ticksuffix="%", title_font_size=12)
figq.update_yaxes(title_text="Quer ver mais — % de quem já pratica", range=[26, 132],
                  ticksuffix="%", showgrid=True, gridcolor=GRID, title_font_size=12)
figq.update_layout(margin=dict(l=8, r=18, t=40, b=8))
DIVS["quadrante"] = emb(figq, "g_quadrante")

# tração: quanta gente o evento reúne quando é programado
_ref = DE[DE.evento.isin(["3x3", "2x2"])]
_bar = pd.concat([_ref.sort_values("media_part"), DE[DE.latente].sort_values("media_part")])
figt = go.Figure()
for sub, nome, cor in ((_bar[_bar.latente], "Demanda latente", ORANGE),
                       (_bar[~_bar.latente], "Régua de comparação", LAT_AZUL)):
    figt.add_bar(y=sub["evento"], x=sub["media_part"], name=nome, orientation="h",
                 marker_color=cor, text=[f"{v:.0f}" for v in sub["media_part"]],
                 textposition="outside", cliponaxis=False,
                 textfont=dict(size=12, color=INK2),
                 hovertemplate="%{y}<br><b>%{x:.0f}</b> competidores em média<extra></extra>")
style(figt, 420, legend=True)
# de baixo para cima: a régua embaixo, os eventos de demanda latente no topo
figt.update_yaxes(categoryorder="array", categoryarray=list(_bar["evento"]))
figt.update_xaxes(range=[0, _bar["media_part"].max()*1.14],
                  title_text="competidores, em média, por competição em que apareceu",
                  title_font_size=12)
figt.update_layout(margin=dict(l=8, r=30, t=36, b=8), bargap=0.34)
DIVS["tracao"] = emb(figt, "g_tracao")

# ============================================================
# DECISÃO / OBSTÁCULOS
# ============================================================
oc=df[C[17]].value_counts()
DIVS["obstaculo"]=emb(hbar(list(oc.index),list(oc.values),color=ORANGE),"g_obst")

dec=multi_count(C[14])
DIVS["decisao"]=emb(hbar(list(dec.keys()),list(dec.values()),hovlabel="menções"),"g_dec")

dist_order=["Só na minha cidade","Até 30 km","30-60 km","60-100 km","100-250 km","250-500 km","Mais de 500 km"]
des=df[C[10]].value_counts(); pra=df[C[11]].value_counts()
dv=[int(des.get(d,0)) for d in dist_order]; pv=[int(pra.get(d,0)) for d in dist_order]
figd=go.Figure()
figd.add_bar(y=dist_order,x=pv,name="Quanto viaja na prática",orientation="h",marker_color=ORANGE,
    hovertemplate="%{y}<br>na prática: <b>%{x}</b><extra></extra>")
figd.add_bar(y=dist_order,x=dv,name="Quanto gostaria de viajar (máx.)",orientation="h",marker_color=BLUE,
    hovertemplate="%{y}<br>gostaria: <b>%{x}</b><extra></extra>")
figd.update_layout(barmode="group",bargap=0.3,bargroupgap=0.08)
figd.update_yaxes(categoryorder="array",categoryarray=dist_order[::-1])
style(figd,420,legend=True); figd.update_layout(margin=dict(l=8,r=30,t=34,b=8))
DIVS["viagem"]=emb(figd,"g_viagem")

pay_order=["Até R$10","R$11-20","R$21-30","R$31-40","R$41-50","R$51-100","Mais de R$100","Depende do número de eventos"]
pc=df[C[15]].value_counts()
DIVS["pagar"]=emb(hbar(list(pc.index),list(pc.values),order=pay_order),"g_pagar")

# ============================================================
# DIVULGAÇÃO
# ============================================================
cw=multi_count(C[12]); gw=multi_count(C[13])
chans=["Site da WCA","WhatsApp / grupos","Instagram / redes sociais","Comunidade local / amigos",
       "Aviso direto do organizador","Discord","Telegram"]
cv=[cw.get(c,0) for c in chans]; gv=[gw.get(c,0) for c in chans]
DIVS["divulg"]=emb(grouped_hbar(chans,gv,cv,"Como gostaria de ser avisado","Como fica sabendo hoje",height=430),"g_divulg")

# salvar todos os divs + plotlyjs
try:
    from plotly.offline import get_plotlyjs
    plotlyjs = get_plotlyjs()
except Exception:
    import plotly
    p = os.path.join(os.path.dirname(plotly.__file__), "package_data", "plotly.min.js")
    plotlyjs = open(p).read()
STATS = {
    "n": int(N),
    "n_sp": int((df[C[25]]=="SP").sum()),
    "n_comps": int(len(sp)),
    "ras_sem_comp": int(sum(1 for r in allras if racount.get(r,0)==0)),
    "ano_cob": ANO_COB,
    "pop_longe": LONGE,
    "pop_longe_mi": _mi(LONGE),
    "pop_longe_pct": round(LONGE/POP_TOT*100),
    "pop_perto_pct": round(float(FX.loc[FX.faixa=="até 25 km","pct"].iloc[0])),
    "cob_2023_mi": _mi(COB_SERIE[2023]),
    "n_estreantes": N_ESTREANTES_SP,
    "ret_sp": round(RET_SP*100),
    "ret_br": round(float(RET.loc[REF_BR,"mean"])*100),
    "ret_interior": round(float(RET.loc["Interior distante (Norte, Oeste, Sul)","mean"])*100),
    "estreias_interior": int(RET.loc["Interior distante (Norte, Oeste, Sul)","size"]),
}
json.dump({"divs":DIVS,"stats":STATS}, open(os.path.join(SCR,"divs.json"),"w"))
open(os.path.join(SCR,"plotly.min.js"),"w").write(plotlyjs)
print("figuras geradas:", list(DIVS.keys()))
print("stats:", STATS)
print("respostas por macrorregião:", tc.to_dict())
print("comps por região:", rx.to_dict())
print("mapa classes:", mdf.set_index("ra")["n"].to_dict())
