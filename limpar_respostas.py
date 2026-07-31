# -*- coding: utf-8 -*-
"""Limpa o CSV bruto do formulário e acrescenta Cidade (limpa), UF e Região Administrativa.

Entrada : "Mapeamento da Comunidade de Cubo Mágico de SP.csv" (export do Google Forms)
Saída   : Mapeamento_SP_limpo_com_RA.csv  (base usada por gen_pdf.py e build_html.py)

A cidade digitada é casada com a lista oficial dos 645 municípios de SP (mun2ra.json).
Cidades de fora do estado e apelidos/bairros são resolvidos pelos dicionários abaixo.
"""
import os, re, json, csv, unicodedata, sys

BASE = os.path.dirname(os.path.abspath(__file__))
BRUTO = os.path.join(BASE, "Mapeamento da Comunidade de Cubo Mágico de SP.csv")
SAIDA = os.path.join(BASE, "Mapeamento_SP_limpo_com_RA.csv")

COL_CIDADE = "Em qual cidade você mora?"

# rótulo da RA no mun2ra.json -> rótulo usado nesta base
WIKI2CSV = {
    "1ª Grande SP": "RM de São Paulo",
    "2ª Santos": "RA de Santos",
    "2Aª Registro": "RA de Registro",
    "3ª São José dos Campos": "RA de São José dos Campos",
    "4ª Sorocaba": "RA de Sorocaba",
    "5ª Campinas": "RA de Campinas",
    "6ª Ribeirão Preto": "RA de Ribeirão Preto",
    "7ª Bauru": "RA de Bauru",
    "8ª São José do Rio Preto": "RA de São José do Rio Preto",
    "9ª Araçatuba": "RA de Araçatuba",
    "10ª Presidente Prudente": "RA de Presidente Prudente",
    "11ª Marília": "RA de Marília",
    "12ª Central": "RA Central",
    "13ª Barretos": "RA de Barretos",
    "14ª Franca": "RA de Franca",
    "16ª Itapeva": "RA de Itapeva",
}

# bairros/apelidos que na verdade são um município de SP
APELIDOS_SP = {
    "itaim paulista": "São Paulo",
    "sp": "São Paulo",
    "sampa": "São Paulo",
    "embu": "Embu das Artes",
    "sao caetano": "São Caetano do Sul",
    "abc": "Santo André",
    "rp": "Ribeirão Preto",
    "sjc": "São José dos Campos",
    "sjrp": "São José do Rio Preto",
}

# cidades de fora do estado (nome normalizado -> nome oficial, UF)
FORA_DE_SP = {
    "niteroi": ("Niterói", "RJ"),
    "fortaleza": ("Fortaleza", "CE"),
    "osorio": ("Osório", "RS"),
    "brasilia": ("Brasília", "DF"),
    "uberaba": ("Uberaba", "MG"),
    "bh": ("Belo Horizonte", "MG"),
    "belo horizonte": ("Belo Horizonte", "MG"),
    "rio de janeiro": ("Rio de Janeiro", "RJ"),
    "curitiba": ("Curitiba", "PR"),
    "salvador": ("Salvador", "BA"),
    "porto alegre": ("Porto Alegre", "RS"),
    "goiania": ("Goiânia", "GO"),
    "recife": ("Recife", "PE"),
    "florianopolis": ("Florianópolis", "SC"),
    "vitoria": ("Vitória", "ES"),
    "manaus": ("Manaus", "AM"),
    "belem": ("Belém", "PA"),
    "campo grande": ("Campo Grande", "MS"),
    "cuiaba": ("Cuiabá", "MT"),
    "natal": ("Natal", "RN"),
    "joao pessoa": ("João Pessoa", "PB"),
    "maceio": ("Maceió", "AL"),
    "aracaju": ("Aracaju", "SE"),
    "teresina": ("Teresina", "PI"),
    "sao luis": ("São Luís", "MA"),
    "palmas": ("Palmas", "TO"),
    "macapa": ("Macapá", "AP"),
    "boa vista": ("Boa Vista", "RR"),
    "rio branco": ("Rio Branco", "AC"),
    "porto velho": ("Porto Velho", "RO"),
}

UFS = {"AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT","PA","PB",
       "PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"}


def norm(s):
    """minúsculo, sem acento, sem pontuação de separação, espaços colapsados."""
    s = s.replace("’", "'").replace("`", "'")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[-/.]", " ", s)
    s = re.sub(r"[^a-z' ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def separa_uf(texto):
    """Tira um sufixo de UF ('Terra Roxa-SP', 'campinas sp', 'Osório - RS')."""
    t = texto.strip()
    m = re.search(r"[\s,\-/]+([A-Za-z]{2})\s*$", t)
    if m and m.group(1).upper() in UFS:
        return t[:m.start()].strip(), m.group(1).upper()
    return t, None


def carrega_municipios():
    mun2ra = json.load(open(os.path.join(BASE, "mun2ra.json")))
    por_norm = {}
    for nome, ra in mun2ra.items():
        por_norm[norm(nome)] = (nome, WIKI2CSV[ra])
    return por_norm


def resolve(bruto, municipios):
    """devolve (cidade_limpa, uf, RA, aviso|None)."""
    texto = (bruto or "").strip()
    if not texto:
        return "", "", "", "cidade em branco"

    # "Valinhos, mas as vezes Franco da rocha" -> primeira cidade citada
    principal = re.split(r"\s*(?:,|;|/| e | ou | mas )\s*", texto, maxsplit=1)[0]
    principal, uf_sufixo = separa_uf(principal)
    chave = norm(principal)

    if chave in APELIDOS_SP:
        principal = APELIDOS_SP[chave]
        chave = norm(principal)

    if chave in municipios and uf_sufixo in (None, "SP"):
        nome, ra = municipios[chave]
        return nome, "SP", ra, None

    if chave in FORA_DE_SP:
        nome, uf = FORA_DE_SP[chave]
        return nome, uf, "Fora de SP", None

    if uf_sufixo and uf_sufixo != "SP":
        return principal.title(), uf_sufixo, "Fora de SP", \
               f"cidade de fora de SP não catalogada: {texto!r} -> {principal.title()}/{uf_sufixo}"

    return principal.title(), "", "", f"cidade não reconhecida: {texto!r}"


def main():
    municipios = carrega_municipios()
    with open(BRUTO, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f))
    if not linhas:
        sys.exit("CSV bruto vazio")
    campos = list(linhas[0].keys())

    avisos = []
    for row in linhas:
        # espaços sobrando nas respostas ("Dinheiro ") viram rótulos duplicados nos gráficos
        for k, v in list(row.items()):
            if isinstance(v, str):
                row[k] = v.strip()
        cidade, uf, ra, aviso = resolve(row.get(COL_CIDADE, ""), municipios)
        row["Cidade (limpa)"] = cidade
        row["UF"] = uf
        row["Região Administrativa"] = ra
        if aviso:
            avisos.append(aviso)

    with open(SAIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos + ["Cidade (limpa)", "UF", "Região Administrativa"])
        w.writeheader()
        w.writerows(linhas)

    print(f"{len(linhas)} respostas -> {os.path.basename(SAIDA)}")
    ufs = {}
    ras = {}
    for row in linhas:
        ufs[row["UF"]] = ufs.get(row["UF"], 0) + 1
        ras[row["Região Administrativa"]] = ras.get(row["Região Administrativa"], 0) + 1
    print("UF:", dict(sorted(ufs.items(), key=lambda kv: -kv[1])))
    print("RA:", dict(sorted(ras.items(), key=lambda kv: -kv[1])))
    for a in avisos:
        print("AVISO:", a)


if __name__ == "__main__":
    main()
