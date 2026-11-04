"""Classifica as referências por utilidade para o projeto.

A nota não mede qualidade científica: mede o quanto a referência serve a este
projeto (composto-alvo, modelo zebrafish/algas, tipo de estudo, acesso e resumo).
O resultado entra no tabela.json e é usado pelo painel.py e pelo publicar.py.
"""
import csv
import json
import re
import unicodedata
from pathlib import Path

import doi as doilib


def _norm(texto):
    texto = unicodedata.normalize("NFKD", str(texto or ""))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto.lower()).strip()


def _celulas(linha):
    s = linha.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def ler_frentes(pasta):
    """DOI -> {frentes, area, resultado, dados, metodo} a partir do REFERENCIAS.md."""
    caminho = Path(pasta) / "REFERENCIAS.md"
    if not caminho.exists():
        return {}
    atual, meta = "", {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            h = linha[3:].strip()
            if _norm(h) not in ("notas de verificacao", "tabela de referencias"):
                atual = h
            continue
        if not linha.lstrip().startswith("|"):
            continue
        cells = _celulas(linha)
        if len(cells) < 8 or cells[0].lower().startswith(("autores", "---")):
            continue
        d = doilib.achar(linha)
        if not d:
            continue
        meta.setdefault(d.lower(), {"frentes": [], "area": "", "resultado": "", "dados": "", "metodo": ""})
        m = meta[d.lower()]
        if atual and atual not in m["frentes"]:
            m["frentes"].append(atual)
        m["area"] = m["area"] or cells[6]
        m["resultado"] = m["resultado"] or cells[7]
        m["dados"] = m["dados"] or cells[4]
        m["metodo"] = m["metodo"] or cells[5]
    return meta


def ler_revistas(pasta):
    """Nome normalizado da revista -> (status, observação) a partir de revistas.csv."""
    caminho = Path(pasta) / "revistas.csv"
    if not caminho.exists():
        return {}
    saida = {}
    with open(caminho, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            chave = _norm(r.get("revista", ""))
            if chave:
                saida[chave] = (r.get("status", ""), r.get("observacao", ""))
    return saida


def _tags(titulo, area, resultado, frentes):
    base = _norm(" ".join([titulo, area, " ".join(frentes)]))
    com_resultado = _norm(" ".join([titulo, area, resultado, " ".join(frentes)]))
    tags = []
    if "geraniol" in base:
        tags.append("Geraniol")
    if "nootkat" in base:
        tags.append("Nootkatone")
    if "zebrafish" in com_resultado or "danio rerio" in com_resultado:
        tags.append("Zebrafish")
    if re.search(r"\balga|microalga|chlorella|raphidocelis|desmodesmus|scenedesmus|cianobact|cyanobact", com_resultado):
        tags.append("Algas")
    if "daphnia" in com_resultado:
        tags.append("Daphnia")
    if re.search(r"\bfish|\bpeixe|oncorhynchus|mykiss|pimephales|prochilodus|colossoma|rhamdia|oreochromis|tilapia", com_resultado) and "Zebrafish" not in tags:
        tags.append("Peixe")
    if re.search(r"\bregulatory|\bregulatorio|\befsa\b|\bepa\b", base) or "peer review of the pesticide" in base:
        tags.append("Regulatório")
    elif re.search(r"\breview|\brevisao|meta-analysis|metanalise|overview", base):
        tags.append("Revisão")
    if re.search(r"\boecd|\biso \d|guideline|diretriz|test no\.", base):
        tags.append("Diretriz")
    if re.search(r"terpen|essential oil|oleo essencial|monoterp|sesquiterp", base) and not ({"Geraniol", "Nootkatone"} & set(tags)):
        tags.append("Análogo")
    return tags


def classificar(linha, meta, revistas):
    titulo = linha.get("titulo", "")
    area = meta.get("area", "")
    resultado = meta.get("resultado", "")
    frentes = meta.get("frentes", [])
    tags = _tags(titulo, area, resultado, frentes)

    direto = bool({"Geraniol", "Nootkatone"} & set(tags))
    modelo = bool({"Zebrafish", "Algas", "Daphnia", "Peixe"} & set(tags))
    regulatorio = "Regulatório" in tags
    revisao = "Revisão" in tags and not regulatorio
    diretriz = "Diretriz" in tags
    analogo = "Análogo" in tags
    acesso = _norm(linha.get("acesso", ""))
    aberto = bool(acesso and acesso not in ("fechado", "closed"))
    resumo = bool(linha.get("resumo"))
    try:
        ano = int(linha.get("ano") or 0)
    except (TypeError, ValueError):
        ano = 0
    try:
        citacoes = int(linha.get("citacoes") or 0)
    except (TypeError, ValueError):
        citacoes = 0

    score = 0
    if direto:
        score += 40
    if "Zebrafish" in tags:
        score += 25
    if "Algas" in tags:
        score += 25
    if "Daphnia" in tags:
        score += 12
    if "Peixe" in tags:
        score += 12
    if revisao:
        score += 6
    if regulatorio:
        score += 20 if ({"Zebrafish", "Algas"} & set(tags)) else 8
    if diretriz:
        score += 20 if ({"Zebrafish", "Algas"} & set(tags)) else 5
    if not modelo:
        score -= 10
    if analogo:
        score -= 15
    if not revisao and not diretriz and not regulatorio:
        score += 10
    if aberto:
        score += 8
    if resumo:
        score += 8
    if ano >= 2020:
        score += 5
    if citacoes >= 100:
        score += 8
    if citacoes >= 1000:
        score += 12
    t = _norm(titulo)
    if "genome" in t or "stages of embryonic" in t:
        score += 6

    if score >= 65:
        prioridade = "Essencial"
    elif score >= 35:
        prioridade = "Contexto"
    else:
        prioridade = "Complementar"

    if diretriz:
        tipo = "Diretriz"
    elif regulatorio:
        tipo = "Regulatório"
    elif revisao:
        tipo = "Revisão"
    elif modelo or direto:
        tipo = "Experimental"
    else:
        tipo = "Contexto"

    motivo = []
    if direto:
        motivo.append("composto-alvo")
    for tag in ("Zebrafish", "Algas", "Daphnia", "Peixe"):
        if tag in tags:
            motivo.append(tag.lower())
    if revisao:
        motivo.append("revisão")
    if regulatorio:
        motivo.append("regulatório")
    if diretriz:
        motivo.append("diretriz")
    if analogo:
        motivo.append("análogo")
    if not motivo:
        motivo.append("contexto")

    status, obs = revistas.get(_norm(linha.get("revista", "")), ("", ""))
    return {
        "tags": tags,
        "tipo": tipo,
        "score": score,
        "prioridade": prioridade,
        "motivo": " + ".join(motivo),
        "frentes": frentes,
        "revista_status": status,
        "revista_obs": obs,
    }


def enriquecer(pasta, linhas):
    meta = ler_frentes(pasta)
    revistas = ler_revistas(pasta)
    for linha in linhas:
        linha.update(classificar(linha, meta.get(str(linha.get("doi", "")).lower(), {}), revistas))
    return linhas


def generico(pasta, linhas):
    """Ordenação de reserva para projetos sem configuração própria.

    Não tenta adivinhar composto ou modelo: usa a frente, o tipo de estudo,
    acesso, resumo, ano e citações. Foi feita para o exemplo do repositório e
    para qualquer tema que não traga um `relevancia.json`.
    """
    meta = ler_frentes(pasta)
    revistas = ler_revistas(pasta)
    for linha in linhas:
        m = meta.get(str(linha.get("doi", "")).lower(), {})
        frentes = m.get("frentes", [])
        tags = []
        for frente in frentes:
            label = re.sub(r"^\d+-", "", frente).replace("-", " ").strip()
            label = label[:1].upper() + label[1:] if label else ""
            if label and label not in tags:
                tags.append(label)
        texto = _norm(" ".join([linha.get("titulo", ""), m.get("area", "")]))
        if re.search(r"\breview|\brevisao|meta-analysis|metanalise|overview", texto):
            tags.append("Revisão")
        if re.search(r"\boecd|\biso \d|guideline|diretriz|test no\.", texto):
            tags.append("Diretriz")
        if not tags:
            tags.append("Contexto")

        revisao = "Revisão" in tags
        diretriz = "Diretriz" in tags
        acesso = _norm(linha.get("acesso", ""))
        aberto = bool(acesso and acesso not in ("fechado", "closed"))
        resumo = bool(linha.get("resumo"))
        try:
            ano = int(linha.get("ano") or 0)
        except (TypeError, ValueError):
            ano = 0
        try:
            citacoes = int(linha.get("citacoes") or 0)
        except (TypeError, ValueError):
            citacoes = 0

        score = 20
        if aberto:
            score += 10
        if resumo:
            score += 10
        if ano >= 2020:
            score += 5
        if revisao:
            score += 5
        score += min(citacoes // 10, 20)

        if score >= 50:
            prioridade = "Essencial"
        elif score >= 30:
            prioridade = "Contexto"
        else:
            prioridade = "Complementar"
        tipo = "Diretriz" if diretriz else "Revisão" if revisao else "Experimental"
        motivo = "frente: " + ", ".join(frentes[:2]) if frentes else "contexto"
        status, obs = revistas.get(_norm(linha.get("revista", "")), ("", ""))
        linha.update({
            "tags": tags[:5],
            "tipo": tipo,
            "score": score,
            "prioridade": prioridade,
            "motivo": motivo,
            "frentes": frentes,
            "revista_status": status,
            "revista_obs": obs,
        })
    return linhas


def legenda(pasta):
    caminho = Path(pasta) / "relevancia.json"
    if caminho.exists():
        try:
            cfg = json.loads(caminho.read_text(encoding="utf-8"))
            if cfg.get("legenda"):
                return str(cfg["legenda"])
        except (OSError, ValueError):
            pass
    return ("A nota soma frente, tipo de estudo, acesso aberto, resumo, ano e citações; "
            "não mede a qualidade da revista nem do artigo.")
