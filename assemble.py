# -*- coding: utf-8 -*-
import os, json
SCR=os.path.dirname(os.path.abspath(__file__))
_J=json.load(open(os.path.join(SCR,"divs.json")))
D=_J["divs"]
S=_J["stats"]
N, N_SP = S["n"], S["n_sp"]
N_COMPS, RAS_SEM = S["n_comps"], S["ras_sem_comp"]
ANO_COB, POP_LONGE_MI, POP_LONGE_PCT = S["ano_cob"], S["pop_longe_mi"], S["pop_longe_pct"]
POP_PERTO_PCT, COB_2023_MI = S["pop_perto_pct"], S["cob_2023_mi"]
N_ESTR, RET_SP, RET_BR = S["n_estreantes"], S["ret_sp"], S["ret_br"]
RET_INT, ESTR_INT = S["ret_interior"], S["estreias_interior"]
PLOTLYJS=open(os.path.join(SCR,"plotly.min.js")).read()

def chart(div_key, title, desc):
    return f"""<figure class="chart">
  <h3>{title}</h3>
  <p class="cap">{desc}</p>
  {D[div_key]}
</figure>"""

CSS = """
/* paleta da marca — ver brand.py e COLOR_SCHEMA.md */
:root{--red:#cc0a14;--red-dark:#9c2226;--blue:#2f66b0;--ink:#0b0b0b;--ink2:#46443f;
--muted:#8a8981;--surf:#ffffff;--soft:#faf6f5;--line:#e7e6e1;--radius:14px;}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:#fbfbfa;color:var(--ink2);
font-family:"Inter",Segoe UI,system-ui,-apple-system,sans-serif;line-height:1.62;font-size:16.5px;}
.wrap{max-width:880px;margin:0 auto;padding:0 20px 90px;}
header.hero{background:linear-gradient(135deg,#151515,#000);color:#fff;padding:58px 0 44px;margin-bottom:8px;}
header.hero .wrap{padding-bottom:0}
.kick{letter-spacing:.16em;font-size:12.5px;text-transform:uppercase;opacity:.9;font-weight:700}
header.hero h1{color:#fff;font-size:34px;line-height:1.12;margin:.35em 0 .25em;font-weight:800;letter-spacing:-.01em}
header.hero p{color:#e6e2e0;font-size:18px;margin:.2em 0 0;max-width:44em}
.cubes{display:flex;gap:6px;margin-bottom:16px}
.cubes span{width:22px;height:22px;border-radius:5px;border:1px solid rgba(255,255,255,.25)}
h2{color:var(--ink);font-size:26px;margin:2.4em 0 .1em;font-weight:800;letter-spacing:-.01em;
padding-top:.3em;border-top:2px solid var(--line)}
h2 .num{color:var(--red);font-weight:800}
h3{color:var(--ink);font-size:18px;margin:1.1em 0 .1em;font-weight:700}
p{margin:.7em 0}
a{color:var(--red)}
.lead{font-size:18px;color:var(--ink2)}
.chart{margin:1.4em 0 1.8em;background:var(--surf);border:1px solid var(--line);
border-radius:var(--radius);padding:16px 16px 6px;box-shadow:0 1px 2px rgba(20,20,40,.03)}
.chart .cap{color:var(--muted);font-size:14px;margin:.1em 0 .6em}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid2 .chart{margin:0}
@media(max-width:680px){.grid2{grid-template-columns:1fr}header.hero h1{font-size:27px}}
.box{background:var(--soft);border:1px solid #f0dcd9;border-left:4px solid var(--red);
border-radius:10px;padding:14px 18px;margin:1.3em 0}
.box.warn{background:#fbf6ec;border-color:#eadfc6;border-left-color:#b8790a}
.box h4{margin:.1em 0 .3em;color:var(--ink);font-size:15.5px;letter-spacing:.02em;text-transform:uppercase}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin:1.4em 0}
.kpi{flex:1;min-width:150px;background:var(--surf);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.kpi b{display:block;font-size:30px;color:var(--red);font-weight:800;line-height:1}
.kpi small{color:var(--muted);font-size:13px}
.gloss{columns:2;column-gap:26px;font-size:15px}
.gloss dt{font-weight:700;color:var(--ink)}
.gloss dd{margin:0 0 .7em;color:var(--ink2)}
@media(max-width:680px){.gloss{columns:1}}
ul.take li{margin:.5em 0}
footer{border-top:2px solid var(--line);margin-top:3em;padding-top:1.4em;color:var(--muted);font-size:14px}
.tag{display:inline-block;background:#f7e7e6;color:var(--red-dark);border-radius:999px;
padding:2px 11px;font-size:12.5px;font-weight:600;margin-bottom:.5em}
"""

CUBES = "".join(f'<span style="background:{c}"></span>' for c in
                ["#ffffff","#cc0a14","#ffffff","#cc0a14","#cc0a14","#ffffff"])

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

<p class="lead">Em julho de 2026, {N} pessoas que praticam cubo mágico responderam a uma pesquisa sobre como vivem o hobby: onde moram, o que competem, o que atrapalha e o que gostariam de ver mudar. Reunimos essas respostas e as comparamos com o histórico oficial de competições da <b>WCA</b>. Esta página conta, em linguagem simples, o que encontramos.</p>

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
  <div class="kpi"><b>{N}</b><small>pessoas responderam</small></div>
  <div class="kpi"><b>{N_SP}</b><small>moram em São Paulo</small></div>
  <div class="kpi"><b>{N_COMPS}</b><small>competições em SP desde 2023</small></div>
  <div class="kpi"><b>{RAS_SEM}</b><small>regiões do estado sem nenhuma competição</small></div>
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

{chart('comps_ano','Competições em São Paulo por ano','Total de competições oficiais no estado. 2026 aparece em vermelho porque o ano ainda não terminou.')}

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

<h2><span class="num">4.</span> O mesmo vazio, medido em pessoas</h2>
<p>O mapa da seção anterior mostra território. Mas território não vai a campeonato — gente vai. Então refizemos a conta em pessoas: para cada um dos 645 municípios de São Paulo, medimos a distância até a competição mais próxima realizada em {ANO_COB} e somamos a população de cada faixa (Censo 2022).</p>

{chart('cobertura','Onde mora a população, em relação à competição mais próxima', f'Distância em linha reta do centro de cada município até a sede de competição mais próxima de {ANO_COB}, somando a população do Censo 2022. Por ser linha reta, a viagem real é sempre maior.')}

<p>O resultado tem dois lados. O primeiro é tranquilizador: <b>{POP_PERTO_PCT}% dos paulistas</b> moram a menos de 25 km de uma sede de competição. Na média, o estado é bem servido — reflexo de a maior parte da população estar na Grande São Paulo e em Campinas.</p>

<div class="box warn">
  <h4>O que a média esconde</h4>
  <p style="margin:.3em 0">Em {ANO_COB}, <b>{POP_LONGE_MI} milhões de paulistas</b> ({POP_LONGE_PCT}% do estado) não tiveram <b>nenhuma</b> competição a menos de 100 km de casa. São cidades grandes e com cena própria de cubo mágico — Bauru, Marília, Araçatuba, Franca. A situação vem melhorando (eram {COB_2023_MI} milhões em 2023), mas a lacuna ainda tem o tamanho de uma região metropolitana inteira.</p>
</div>

<p>Essa conta também mostra <b>onde uma competição nova rende mais</b>. Mais um campeonato na capital atende gente que já tem vários por ano a poucos quilômetros. Um campeonato em Bauru ou Marília aproxima, de uma vez, centenas de milhares de pessoas que hoje não têm nada perto.</p>

<h2><span class="num">5.</span> Quem começa, continua — o difícil é começar</h2>
<p>Fica a pergunta natural: será que a distância faz as pessoas <b>desistirem</b> do hobby? Dá para responder com o histórico da WCA, sem depender do que a pesquisa diz. Pegamos todas as pessoas cuja <b>primeira competição na vida</b> foi um campeonato paulista de 2023 em diante — {N_ESTR} pessoas — e vimos quantas voltaram a competir em até 12 meses.</p>

<div class="grid2">
  <figure class="chart"><h3>Voltaram a competir em até 1 ano</h3><p class="cap">Por região da primeira competição. A última barra é a média do resto do Brasil.</p>{D['retencao']}</figure>
  <figure class="chart"><h3>Onde as pessoas estrearam</h3><p class="cap">Número de estreantes por região da primeira competição.</p>{D['entrada']}</figure>
</div>

<p>A resposta é <b>não</b> — e com folga. {RET_SP}% dos estreantes paulistas voltaram a competir dentro de um ano, acima da média nacional ({RET_BR}%). E quem estreou no interior distante voltou <i>mais</i> ({RET_INT}%) do que quem estreou na capital, não menos. Faz sentido: quem enfrenta 200 km para a primeira competição já é alguém bastante decidido. (São só {ESTR_INT} pessoas nesse grupo, então o número exato é impreciso — mas a direção é clara.)</p>

<div class="box">
  <h4>Onde está o gargalo, então</h4>
  <p style="margin:.3em 0">Está na <b>entrada</b>, não na saída. Das {N_ESTR} estreias em competições paulistas, apenas <b>{ESTR_INT}</b> aconteceram no interior distante — a mesma região onde moram os {POP_LONGE_MI} milhões de pessoas da seção anterior. A comunidade não perde quem entra: ela simplesmente quase não recebe gente nova de fora do eixo capital–Campinas, porque lá não existe uma primeira competição para ir.</p>
</div>

<h2><span class="num">6.</span> O que a comunidade quer competir × o que aparece</h2>
<p>Cada competição escolhe quais modalidades vai oferecer. Comparamos o que as pessoas <b>gostariam de ver mais</b> (na pesquisa) com o que <b>de fato apareceu</b> nas competições paulistas desde 2023. O descompasso é claro em duas modalidades muito queridas:</p>
{chart('dem_of','Demanda × oferta de modalidades','Barra vermelha: % de quem gostaria de ver a modalidade mais vezes. Barra azul: % das competições de SP que ofereceram a modalidade.')}
<p><b>Megaminx e Skewb</b> estão entre os mais desejados, mas aparecem em apenas cerca de um em cada quatro campeonatos. Vale um detalhe curioso: São Paulo tem uma cena forte de <b>competições especializadas</b> (só Clock, só de olhos vendados, só Big Cubes, só Square-1…) — cerca de um terço dos torneios. O problema é que elas se concentram em cidades como São Bernardo, Cubatão e Campinas, e quase nunca na capital.</p>

<h2><span class="num">7.</span> Popular não é a mesma coisa que faltando</h2>
<p>O gráfico anterior tem uma armadilha, e vale desarmá-la: contar quantas pessoas pediram uma modalidade mede o <b>tamanho da torcida</b>, não o que está em falta. O 3x3 é o mais praticado de todos — é natural que apareça no topo dos pedidos, mesmo estando em dois terços das competições. A pergunta certa é outra: <b>entre quem já pratica aquela modalidade, que fração gostaria de vê-la mais vezes?</b></p>

<p>É isso que o gráfico abaixo mostra. Cada bolha é uma modalidade; o tamanho dela é quanta gente pratica. Quanto mais à <b>esquerda</b>, menos as competições paulistas a programam. Quanto mais <b>acima</b>, maior a proporção de praticantes insatisfeitos com essa oferta. O canto vermelho — muito pedida, pouco programada — é onde mora a <b>demanda latente</b>.</p>

{chart('quadrante','Demanda latente: o que falta × o que só é popular','Cada bolha é uma modalidade. Eixo horizontal: em quantas competições ela aparece. Eixo vertical: quantos dos seus praticantes querem vê-la mais. Passe o mouse para os números.')}

<p>O quadro muda bastante. O <b>Clock</b> sai de cena: parecia muito pedido, mas é a 2ª modalidade mais programada do estado — o que parecia demanda era só o tamanho da base. Já <b>Megaminx, Skewb e Square-1</b> passam no teste: continuam no topo mesmo depois do ajuste, e aparecem em menos de um terço dos campeonatos.</p>

<div class="box warn">
  <h4>O achado mais forte: as modalidades de olhos vendados</h4>
  <p style="margin:.3em 0">Nas três modalidades de blind com cubos grandes (4BLD, 5BLD e MBLD), a proporção chega a <b>100%</b> — ou seja, <b>há mais gente pedindo a modalidade do que gente que já compete nela</b>. São pessoas que querem começar e não encontram onde. No gráfico anterior, essas modalidades apareciam no rodapé da lista, como se fossem irrelevantes; elas são, na verdade, o caso mais claro de demanda represada da pesquisa inteira.</p>
</div>

<p>Sobra o contra-argumento clássico de quem monta um campeonato: "ninguém compete nessas modalidades, não compensa o tempo de cronograma". Os dados oficiais da WCA dizem o contrário. Quando essas modalidades <i>entram</i> na programação, elas trazem gente:</p>

{chart('tracao','Quantos competidores a modalidade reúne quando é programada','Média de competidores por competição em que a modalidade apareceu (SP, 2023 em diante). 3x3 e 2x2 servem de régua.')}

<p>Skewb e Megaminx reúnem cerca de <b>20 competidores</b> cada vez que entram no cronograma — perto da metade do 3x3 da mesma competição. Não é nicho: é público que hoje só não aparece porque não é chamado.</p>

<div class="box">
  <h4>Para quem organiza um campeonato</h4>
  <p style="margin:.3em 0">Se a intenção é atrair gente que hoje não vai, a lista curta que a pesquisa aponta é <b>Megaminx, Skewb e Square-1</b> — bom público, baixa oferta — e um bloco de <b>olhos vendados</b> (3BLD como porta de entrada, 4BLD/5BLD/MBLD para o pessoal que está esperando há tempo). São modalidades de cronograma curto: cabem ao lado do 3x3 sem esticar o dia, e provavelmente trarão competidores que, do contrário, ficariam em casa.</p>
</div>

<h2><span class="num">8.</span> O que pesa na decisão e o que atrapalha</h2>
<p>Na hora de decidir se vai a uma competição, três coisas dominam: <b>onde</b> ela acontece, <b>quais modalidades</b> terá e <b>em que data</b> cai. O preço da inscrição pesa bem menos do que se costuma imaginar.</p>
<div class="grid2">
  <figure class="chart"><h3>O que mais pesa na decisão</h3><p class="cap">Fatores considerados (cada pessoa marcou até 3).</p>{D['decisao']}</figure>
  <figure class="chart"><h3>Maior obstáculo para competir mais</h3><p class="cap">A principal barreira apontada.</p>{D['obstaculo']}</figure>
</div>
<p>A distância aparece dos dois lados. E há um detalhe revelador: comparando <b>quanto as pessoas gostariam de viajar</b> com <b>quanto realmente viajam</b>, boa parte já se desloca no limite (ou além) do que gostaria — sinal de que faltam competições perto.</p>
{chart('viagem','Quanto gostariam de viajar × quanto viajam de fato','Distância máxima desejada (vermelho) e distância praticada (azul).')}
{chart('pagar','Quanto topariam pagar de inscrição','Faixa de preço aceita pela comunidade.')}

<h2><span class="num">9.</span> Como a comunidade quer ser avisada</h2>
<p>Hoje a maioria descobre as competições pelo site da WCA. Mas, perguntadas sobre como <b>gostariam</b> de ser avisadas, as pessoas colocam o <b>WhatsApp</b> em primeiro lugar — à frente do próprio site e do Instagram.</p>
{chart('divulg','Como ficam sabendo hoje × como gostariam','Canais de divulgação: uso atual (azul) e preferência (vermelho).')}

<h2><span class="num">10.</span> Em resumo</h2>
<ul class="take">
  <li><b>Localização é tudo.</b> Distância é o maior obstáculo e o principal fator na decisão de competir.</li>
  <li><b>A capital não sofre de falta de competições em número</b> — sofre de baixa oferta das modalidades preferidas e de um desejo de competir com mais frequência.</li>
  <li><b>O interior distante é o verdadeiro vazio:</b> seis regiões sem nenhuma competição desde 2023 e viagens de centenas de quilômetros para o resto. Em {ANO_COB}, <b>{POP_LONGE_MI} milhões de paulistas</b> não tiveram competição a menos de 100 km.</li>
  <li><b>Quem entra, fica — o difícil é entrar.</b> {RET_SP}% dos estreantes voltam a competir em um ano (média nacional: {RET_BR}%), mas só {ESTR_INT} das {N_ESTR} estreias aconteceram no interior distante.</li>
  <li><b>Megaminx e Skewb</b> são muito pedidos e pouco oferecidos.</li>
  <li><b>Popular não é o mesmo que faltando.</b> Descontando o tamanho da torcida de cada modalidade, quem realmente está em falta é <b>Megaminx, Skewb, Square-1</b> e as modalidades <b>de olhos vendados</b> — nestas últimas, há mais gente querendo entrar do que gente que já compete.</li>
  <li><b>WhatsApp</b> é o canal que a comunidade quer para receber avisos.</li>
</ul>

<footer>
  <p><b>Sobre os dados.</b> Pesquisa com {N} respostas voluntárias ({N_SP} de São Paulo), coletadas em 2026 — é um retrato de quem participou, não uma amostra estatística da população. Perguntas de múltipla escolha permitem mais de uma marcação, então as somas podem passar do total de pessoas. As competições vêm do export público oficial da WCA; cada uma foi localizada em sua Região Administrativa pela latitude/longitude registrada. O ano de 2026 está incompleto. Populações citadas são aproximadas (Censo 2022).</p>
  <p><b>Confidencialidade.</b> A origem das respostas é mostrada apenas em grandes blocos regionais; nenhum dado individual, cidade ou contato é divulgado.</p>
  <p><b>Cobertura e estreantes.</b> A distância até a competição mais próxima é medida em linha reta, do centro do município à sede — a viagem real é sempre maior. A população vem do Censo 2022 (IBGE). "Estreante" é quem fez a primeira competição da vida em São Paulo de 2023 em diante; só entram as estreias com 12 meses completos para voltar a competir.</p>
  <p>Fontes: <a href="https://www.worldcubeassociation.org/export/results">WCA Results Export</a> · população dos municípios: <a href="https://sidra.ibge.gov.br/tabela/4709">Censo 2022 (IBGE)</a> · malha municipal de SP (IBGE / geodata-br) · divisão em Regiões Administrativas (Governo de SP).</p>
</footer>
</div>
</body>
</html>"""

out=os.path.join(SCR,"index.html")   # nome usado pelo GitHub Pages
open(out,"w").write(HTML)
print("gerado:", out, "-", round(len(HTML)/1024/1024,2), "MB")
