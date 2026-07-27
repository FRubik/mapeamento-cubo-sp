# -*- coding: utf-8 -*-
import os, json
SCR=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(os.path.join(SCR,"divs.json")))["divs"]
PLOTLYJS=open(os.path.join(SCR,"plotly.min.js")).read()

def chart(div_key, title, desc):
    return f"""<figure class="chart">
  <h3>{title}</h3>
  <p class="cap">{desc}</p>
  {D[div_key]}
</figure>"""

CSS = """
:root{--blue:#2a78d6;--orange:#eb6834;--ink:#0b0b0b;--ink2:#41403d;--muted:#7c7b74;
--surf:#ffffff;--soft:#f6f8fb;--line:#e7e6e1;--radius:14px;}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:#fbfbfa;color:var(--ink2);
font-family:"Inter",Segoe UI,system-ui,-apple-system,sans-serif;line-height:1.62;font-size:16.5px;}
.wrap{max-width:880px;margin:0 auto;padding:0 20px 90px;}
header.hero{background:linear-gradient(135deg,#2a78d6,#1f5fa8);color:#fff;padding:58px 0 44px;margin-bottom:8px;}
header.hero .wrap{padding-bottom:0}
.kick{letter-spacing:.16em;font-size:12.5px;text-transform:uppercase;opacity:.9;font-weight:700}
header.hero h1{color:#fff;font-size:34px;line-height:1.12;margin:.35em 0 .25em;font-weight:800;letter-spacing:-.01em}
header.hero p{color:#eaf1fb;font-size:18px;margin:.2em 0 0;max-width:44em}
.cubes{display:flex;gap:6px;margin-bottom:16px}
.cubes span{width:22px;height:22px;border-radius:5px;border:1px solid rgba(0,0,0,.12)}
h2{color:var(--ink);font-size:26px;margin:2.4em 0 .1em;font-weight:800;letter-spacing:-.01em;
padding-top:.3em;border-top:2px solid var(--line)}
h2 .num{color:var(--blue);font-weight:800}
h3{color:var(--ink);font-size:18px;margin:1.1em 0 .1em;font-weight:700}
p{margin:.7em 0}
a{color:var(--blue)}
.lead{font-size:18px;color:var(--ink2)}
.chart{margin:1.4em 0 1.8em;background:var(--surf);border:1px solid var(--line);
border-radius:var(--radius);padding:16px 16px 6px;box-shadow:0 1px 2px rgba(20,20,40,.03)}
.chart .cap{color:var(--muted);font-size:14px;margin:.1em 0 .6em}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid2 .chart{margin:0}
@media(max-width:680px){.grid2{grid-template-columns:1fr}header.hero h1{font-size:27px}}
.box{background:var(--soft);border:1px solid #dfe7f2;border-left:4px solid var(--blue);
border-radius:10px;padding:14px 18px;margin:1.3em 0}
.box.warn{background:#fff7f1;border-color:#f6d8c4;border-left-color:var(--orange)}
.box h4{margin:.1em 0 .3em;color:var(--ink);font-size:15.5px;letter-spacing:.02em;text-transform:uppercase}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin:1.4em 0}
.kpi{flex:1;min-width:150px;background:var(--surf);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.kpi b{display:block;font-size:30px;color:var(--blue);font-weight:800;line-height:1}
.kpi small{color:var(--muted);font-size:13px}
.gloss{columns:2;column-gap:26px;font-size:15px}
.gloss dt{font-weight:700;color:var(--ink)}
.gloss dd{margin:0 0 .7em;color:var(--ink2)}
@media(max-width:680px){.gloss{columns:1}}
ul.take li{margin:.5em 0}
footer{border-top:2px solid var(--line);margin-top:3em;padding-top:1.4em;color:var(--muted);font-size:14px}
.tag{display:inline-block;background:#eef4fc;color:var(--blue);border-radius:999px;
padding:2px 11px;font-size:12.5px;font-weight:600;margin-bottom:.5em}
"""

CUBES = "".join(f'<span style="background:{c}"></span>' for c in
                ["#ffffff","#f5c518","#009b48","#e0342b","#2a78d6","#eb6834"])

HTML = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>A comunidade paulista de cubo mágico — pesquisa 2026</title>
<meta name="description" content="Retrato da comunidade de cubo mágico de São Paulo: perfil, geografia das competições e o que a comunidade pede — cruzando a pesquisa com os dados oficiais da WCA.">
<style>{CSS}</style>
<script>{PLOTLYJS}</script>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="cubes">{CUBES}</div>
  <div class="kick">Pesquisa da comunidade · 2026</div>
  <h1>A comunidade paulista de cubo mágico</h1>
  <p>O que a pesquisa mostra sobre quem somos, e o que os dados oficiais da WCA revelam sobre onde acontecem (e onde faltam) campeonatos em São Paulo.</p>
</div></header>

<div class="wrap">

<p class="lead">Entre junho e julho de 2026, pessoas que praticam cubo mágico responderam a uma pesquisa sobre como vivem o hobby: onde moram, o que competem, o que atrapalha e o que gostariam de ver mudar. Reunimos essas respostas e as comparamos com o histórico oficial de competições da <b>WCA</b>. Esta página conta, em linguagem simples, o que encontramos.</p>

<div class="box">
  <h4>Como ler esta página</h4>
  <p style="margin:.3em 0">Todos os gráficos são interativos: passe o mouse (ou toque) para ver os números exatos. Alguns termos aparecem o tempo todo — aqui está o essencial:</p>
  <dl class="gloss">
    <dt>WCA</dt><dd>World Cube Association, a entidade mundial que regula e oficializa as competições de cubo mágico.</dd>
    <dt>Competição oficial</dt><dd>Torneio reconhecido pela WCA, onde os tempos entram no ranking mundial.</dd>
    <dt>Delegado</dt><dd>Pessoa credenciada pela WCA para autorizar e supervisionar as competições. São poucos por estado.</dd>
    <dt>Evento / modalidade</dt><dd>Cada tipo de quebra-cabeça disputado: 3x3, 2x2, Megaminx, Pyraminx, Skewb, de olhos vendados (blind) etc.</dd>
    <dt>Sub-10</dt><dd>Jeito de dizer o nível: resolver o 3x3 com média abaixo de 10 segundos.</dd>
    <dt>Região Administrativa (RA)</dt><dd>Divisão oficial do estado de São Paulo em 16 regiões, usada aqui para localizar as competições.</dd>
  </dl>
</div>

<div class="kpis">
  <div class="kpi"><b>61</b><small>pessoas responderam</small></div>
  <div class="kpi"><b>55</b><small>moram em São Paulo</small></div>
  <div class="kpi"><b>97</b><small>competições em SP desde 2023</small></div>
  <div class="kpi"><b>6</b><small>regiões do estado sem nenhuma competição</small></div>
</div>

<div class="box warn">
  <h4>Sobre confidencialidade</h4>
  <p style="margin:.3em 0">Prometemos sigilo a quem respondeu. Por isso, a origem das respostas aparece apenas em <b>grandes blocos regionais</b> — nunca por cidade ou por região específica, o que poderia identificar pessoas. Já os dados de competições são públicos (WCA) e podem ser detalhados livremente.</p>
</div>

<h2><span class="num">1.</span> Quem respondeu</h2>
<p>A comunidade que respondeu é, ao mesmo tempo, <b>jovem e experiente</b>: há muita gente entre 13 e 24 anos, mas boa parte já disputou dezenas de competições. Ou seja, são pessoas que conhecem bem o cenário sobre o qual estão opinando.</p>

<div class="grid2">
  <figure class="chart"><h3>Idade</h3><p class="cap">Faixa etária de quem respondeu.</p>{D['idade']}</figure>
  <figure class="chart"><h3>Há quanto tempo praticam</h3><p class="cap">Tempo de prática de cubo mágico.</p>{D['tempo']}</figure>
</div>
<div class="grid2">
  <figure class="chart"><h3>Nível no 3x3</h3><p class="cap">Melhor média aproximada no cubo 3x3.</p>{D['nivel']}</figure>
  <figure class="chart"><h3>Com que frequência competem</h3><p class="cap">Ritmo de participação em competições.</p>{D['freq']}</figure>
</div>
{chart('compswca','Quantas competições oficiais já disputaram','Experiência acumulada em torneios da WCA.')}

<h2><span class="num">2.</span> De onde vieram as respostas</h2>
<p>Aqui há uma diferença importante em relação ao resto da página. Como prometemos sigilo a quem respondeu, a origem das respostas aparece só em <b>quatro grandes blocos</b> — nunca por cidade ou região específica, o que poderia identificar pessoas (são poucas respostas de cada lugar). Um dos blocos junta a <b>Grande São Paulo (fora da capital) com Campinas, a Baixada Santista e o Vale do Paraíba</b> — todas a até cerca de 200&nbsp;km da capital. Outro reúne o <b>interior distante</b> (Norte, Oeste e Sul do estado). Mais adiante, ao falar de competições — que são dado público —, detalhamos cada uma dessas regiões separadamente.</p>
{chart('resp_macro','Respostas por bloco regional','Quantas pessoas de cada grande região participaram. Blocos amplos, propositalmente, para preservar o anonimato.')}
<p>A maioria das respostas veio da capital e do seu entorno imediato. Isso já adianta um ponto importante: o interior distante é enorme, mas está pouco representado — tanto na pesquisa quanto, como veremos, no calendário de competições.</p>

<h2><span class="num">3.</span> "Falta campeonato na capital"?</h2>
<p>Essa é uma percepção comum entre quem mora na cidade de São Paulo. Fomos aos dados oficiais da WCA (competições de 2023 em diante) para entender se ela se sustenta. A resposta é <b>sim e não</b> — e a parte mais interessante está no interior.</p>

{chart('comps_ano','Competições em São Paulo por ano','Total de competições oficiais no estado. 2026 aparece em laranja porque o ano ainda não terminou.')}

<p>Primeiro, o número por região — agora com os nomes que a comunidade usa, já que competição é dado público. A capital <b>não</b> aparece mal: sozinha, a cidade de São Paulo sedia tantos torneios quanto <i>toda</i> a Grande São Paulo (fora a capital) somada. E as regiões vizinhas — Baixada Santista e Campinas — também concentram bastante coisa.</p>
{chart('comps_faixa','Competições desde 2023, por região','Onde acontecem as competições paulistas. "Demais regiões do interior" reúne todo o Norte, Oeste e Sul do estado.')}

<div class="box">
  <h4>O que os números dizem sobre a capital</h4>
  <p style="margin:.3em 0">Em quantidade absoluta, a capital está entre as áreas <b>mais</b> servidas do estado — ela fica no centro do maior aglomerado de competições. A sensação de "falta" tem a ver com outros fatores: muita gente gostaria de competir <b>todo mês</b> (a realidade fica em torno de 7 competições por ano na cidade), e as <b>modalidades preferidas</b> raramente entram na programação — como veremos na próxima seção.</p>
</div>

<p>O ponto realmente crítico aparece quando olhamos o mapa. Quase toda competição "do interior" está, na verdade, num cinturão colado na capital (Campinas, Baixada, Vale). O <b>interior distante</b> — Norte, Oeste e Sul — teve apenas <b>10 competições em três anos e meio</b>, espalhadas por dois terços do território do estado. E <b>seis Regiões Administrativas inteiras não tiveram nenhuma competição</b> desde 2023.</p>

{chart('mapa','Mapa: competições por Região Administrativa (2023 em diante)','Cada região colorida pelo número de competições. Em cinza, as regiões que não tiveram nenhuma. Passe o mouse para ver os nomes e números.')}

<div class="box warn">
  <h4>A conclusão honesta</h4>
  <p style="margin:.3em 0">Não é o caso de "capital desassistida × interior bem servido". É o contrário do que a soma sugere: as competições se concentram num <b>cinturão leste compacto</b>, e quem mora no interior distante (Rio Preto, Bauru, Marília, Araçatuba, Presidente Prudente, Franca…) precisa de viagens de <b>200 a 400&nbsp;km</b> para competir. A distância, aliás, é o obstáculo nº 1 de toda a comunidade.</p>
</div>

<h2><span class="num">4.</span> O que a comunidade quer competir × o que aparece</h2>
<p>Cada competição escolhe quais modalidades vai oferecer. Comparamos o que as pessoas <b>gostariam de ver mais</b> (na pesquisa) com o que <b>de fato apareceu</b> nas competições paulistas desde 2023. O descompasso é claro em duas modalidades muito queridas:</p>
{chart('dem_of','Demanda × oferta de modalidades','Barra azul: % de quem gostaria de ver a modalidade mais vezes. Barra laranja: % das competições de SP que ofereceram a modalidade.')}
<p><b>Megaminx e Skewb</b> estão entre os mais desejados, mas aparecem em apenas cerca de um em cada quatro campeonatos. Vale um detalhe curioso: São Paulo tem uma cena forte de <b>competições especializadas</b> (só Clock, só de olhos vendados, só Big Cubes, só Square-1…) — cerca de um terço dos torneios. O problema é que elas se concentram em cidades como São Bernardo, Cubatão e Campinas, e quase nunca na capital.</p>

<h2><span class="num">5.</span> O que pesa na decisão e o que atrapalha</h2>
<p>Na hora de decidir se vai a uma competição, três coisas dominam: <b>onde</b> ela acontece, <b>quais modalidades</b> terá e <b>em que data</b> cai. O preço da inscrição pesa bem menos do que se costuma imaginar.</p>
<div class="grid2">
  <figure class="chart"><h3>O que mais pesa na decisão</h3><p class="cap">Fatores considerados (cada pessoa marcou até 3).</p>{D['decisao']}</figure>
  <figure class="chart"><h3>Maior obstáculo para competir mais</h3><p class="cap">A principal barreira apontada.</p>{D['obstaculo']}</figure>
</div>
<p>A distância aparece dos dois lados. E há um detalhe revelador: comparando <b>quanto as pessoas gostariam de viajar</b> com <b>quanto realmente viajam</b>, boa parte já se desloca no limite (ou além) do que gostaria — sinal de que faltam competições perto.</p>
{chart('viagem','Quanto gostariam de viajar × quanto viajam de fato','Distância máxima desejada (azul) e distância praticada (laranja).')}
{chart('pagar','Quanto topariam pagar de inscrição','Faixa de preço aceita pela comunidade.')}

<h2><span class="num">6.</span> Como a comunidade quer ser avisada</h2>
<p>Hoje a maioria descobre as competições pelo site da WCA. Mas, perguntadas sobre como <b>gostariam</b> de ser avisadas, as pessoas colocam o <b>WhatsApp</b> em primeiro lugar — à frente do próprio site e do Instagram.</p>
{chart('divulg','Como ficam sabendo hoje × como gostariam','Canais de divulgação: uso atual (laranja) e preferência (azul).')}

<h2><span class="num">7.</span> Em resumo</h2>
<ul class="take">
  <li><b>Localização é tudo.</b> Distância é o maior obstáculo e o principal fator na decisão de competir.</li>
  <li><b>A capital não sofre de falta de competições em número</b> — sofre de baixa oferta das modalidades preferidas e de um desejo de competir com mais frequência.</li>
  <li><b>O interior distante é o verdadeiro vazio:</b> seis regiões sem nenhuma competição desde 2023 e viagens de centenas de quilômetros para o resto.</li>
  <li><b>Megaminx e Skewb</b> são muito pedidos e pouco oferecidos.</li>
  <li><b>WhatsApp</b> é o canal que a comunidade quer para receber avisos.</li>
</ul>

<footer>
  <p><b>Sobre os dados.</b> Pesquisa com {61} respostas voluntárias (55 de São Paulo), coletadas em 2026 — é um retrato de quem participou, não uma amostra estatística da população. Perguntas de múltipla escolha permitem mais de uma marcação, então as somas podem passar do total de pessoas. As competições vêm do export público oficial da WCA; cada uma foi localizada em sua Região Administrativa pela latitude/longitude registrada. O ano de 2026 está incompleto. Populações citadas são aproximadas (Censo 2022).</p>
  <p><b>Confidencialidade.</b> A origem das respostas é mostrada apenas em grandes blocos regionais; nenhum dado individual, cidade ou contato é divulgado.</p>
  <p>Fontes: <a href="https://www.worldcubeassociation.org/export/results">WCA Results Export</a> · malha municipal de SP (IBGE / geodata-br) · divisão em Regiões Administrativas (Governo de SP).</p>
</footer>
</div>
</body>
</html>"""

out=os.path.join(SCR,"relatorio_publico.html")
open(out,"w").write(HTML)
print("gerado:", out, "-", round(len(HTML)/1024/1024,2), "MB")
