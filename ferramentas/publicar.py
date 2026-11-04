"""Gera um RELATORIO.html autocontido a partir de tabela.json e dos resumos.

Uso: python publicar.py <pasta-do-levantamento> [--saida RELATORIO.html]

O HTML abre com dois cliques, sem servidor e sem internet: a tabela tem busca,
filtro por acesso e ordenação, e cada resumo abre numa janela. É a camada
humana da entrega; o TABELA.md continua sendo a versão de texto, e o
tabela.json / cienciometria.csv são a camada de dados.
"""
import argparse
import csv
import datetime
import html
import json
import re
import sys
import urllib.parse
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import painel  # noqa: E402
import relevancia  # noqa: E402
from projeto import barrar_exemplo, opcao_exemplo  # noqa: E402

try:
    import markdown
except ImportError:  # pragma: no cover - só acontece se faltar a dependência
    markdown = None


def md_para_html(texto):
    """Markdown -> HTML, sem deixar HTML cru do modelo passar."""
    seguro = (texto or "").replace("&", "&amp;").replace("<", "&lt;")
    if markdown:
        try:
            corpo = markdown.markdown(seguro, extensions=["tables", "sane_lists"])
        except Exception:
            return "<pre>" + seguro + "</pre>"
        # Markdown permite links com esquemas perigosos; o resumo vem de um PDF,
        # então não dá para confiar cegamente no texto.
        return re.sub(r'\b(href|src)="(?:javascript|data|vbscript):[^"]*"',
                      r'\1="#"', corpo, flags=re.I)
    return "<pre>" + seguro + "</pre>"


def _resumo_rel(caminho):
    """Só aceita caminhos relativos dentro de resumos/ (sem .. ou absoluto)."""
    caminho = str(caminho or "").replace("\\", "/")
    partes = caminho.split("/")
    if not caminho.startswith("resumos/") or ".." in partes or ":" in partes[0]:
        return ""
    return caminho


def _titulo(pasta):
    try:
        texto = (pasta / "REFERENCIAS.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return pasta.name
    m = re.search(r"^#\s+Referências:\s*(.+)$", texto, re.M)
    return m.group(1).strip() if m else pasta.name


def _celula(texto):
    return html.escape(str(texto or ""))


def _numero(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0


def _badge_prioridade(valor):
    valor = valor or "Complementar"
    classe = {"Essencial": "essencial", "Contexto": "contexto", "Complementar": "complementar"}.get(valor, "complementar")
    return f'<span class="badge {classe}">{_celula(valor)}</span>'


def _tags_html(tags):
    partes = []
    for tag in tags or []:
        if tag in ("Zebrafish", "Algas", "Daphnia", "Peixe"):
            classe = "modelo"
        elif tag in ("Revisão", "Diretriz", "Regulatório"):
            classe = "tipo"
        elif tag in ("Geraniol", "Nootkatone"):
            classe = "comp"
        else:
            classe = ""
        partes.append(f'<span class="tag {classe}">{_celula(tag)}</span>')
    return "".join(partes) or '<span class="mudo">—</span>'


def _status_revista(l):
    status = l.get("revista_status") or ""
    if status == "ALERTA":
        return '<span class="rev-alerta">revista em alerta</span>'
    if status == "CONFERIR":
        return '<span class="rev-conferir">revista a conferir</span>'
    if status == "OFICIAL":
        return '<span class="rev-oficial">documento oficial</span>'
    return ""


def _linha(l):
    autores = l.get("autores") or (f'{l.get("autor") or ""} ({l.get("ano") or ""})'.strip())
    titulo = _celula(l.get("titulo"))
    doi = urllib.parse.quote(str(l.get("doi") or ""), safe="/()")
    acesso = _celula(l.get("acesso") or "—")
    resumo = _resumo_rel(l.get("resumo"))
    if resumo:
        nome = Path(resumo).parent.name
        botao = (f'<a class="ler" href="{html.escape(resumo, quote=True)}" '
                 f'data-resumo="{html.escape(nome)}">ler</a>')
        if l.get("preprint"):
            botao += ' <span class="mudo">(preprint)</span>'
    else:
        botao = '<span class="mudo">—</span>'
    tags = l.get("tags") or []
    tema = " ".join(tags)
    prioridade = l.get("prioridade") or "Complementar"
    score = int(_numero(l.get("score")))
    revista = _celula(l.get("revista"))
    fwci = _celula(l.get("fwci")) or "—"
    percentil = _celula(l.get("percentil")) or "—"
    meta = (f'{int(_numero(l.get("citacoes")))} citações · FWCI {fwci} · '
            f'percentil {percentil}')
    status_revista = _status_revista(l)
    if status_revista:
        meta += " · " + status_revista
    return (
        f'<tr data-score="{score}" data-prioridade="{html.escape(prioridade, quote=True)}" '
        f'data-tema="{html.escape(tema, quote=True)}" data-ano="{int(_numero(l.get("ano")))}" '
        f'data-citacoes="{int(_numero(l.get("citacoes")))}" '
        f'data-acesso="{html.escape(l.get("acesso") or "", quote=True)}">'
        f'<td>{_badge_prioridade(prioridade)}<span class="score">{score}</span></td>'
        f'<td>{_celula(autores)}. <a href="https://doi.org/{doi}" target="_blank" rel="noopener">{titulo}</a>. '
        f'<span class="mudo">{revista}</span><div class="meta">{meta}</div></td>'
        f'<td>{_tags_html(tags)}</td>'
        f'<td class="n">{_celula(l.get("ano")) or "—"}</td>'
        f'<td class="n">{int(_numero(l.get("citacoes")))}</td>'
        f'<td>{acesso}</td><td>{botao}</td></tr>')


def _opcoes_acesso(linhas):
    valores = sorted({l.get("acesso") or "" for l in linhas if l.get("acesso")})
    return "\n".join(
        f'        <option value="{html.escape(v, quote=True)}">{html.escape(v)}</option>'
        for v in valores)


def _opcoes_tema(linhas):
    tags = []
    for l in linhas:
        for tag in l.get("tags", []):
            if tag not in tags:
                tags.append(tag)
    ordem = ["Geraniol", "Nootkatone", "Zebrafish", "Algas", "Daphnia", "Peixe",
             "Revisão", "Diretriz", "Regulatório", "Análogo"]
    tags = [t for t in ordem if t in tags] + [t for t in tags if t not in ordem]
    return "\n".join(
        f'        <option value="{html.escape(t, quote=True)}">{html.escape(t)}</option>'
        for t in tags)


def _opcoes_prioridade():
    return "\n".join(
        f'        <option value="{v}">{v}</option>'
        for v in ("Essencial", "Contexto", "Complementar"))


def _item_guia(l):
    autores = _celula(l.get("autores"))
    titulo = _celula(l.get("titulo"))
    doi = urllib.parse.quote(str(l.get("doi") or ""), safe="/()")
    resumo = _resumo_rel(l.get("resumo"))
    botao = ""
    if resumo:
        nome = Path(resumo).parent.name
        botao = (f' <a class="ler" href="{html.escape(resumo, quote=True)}" '
                 f'data-resumo="{html.escape(nome)}">ler</a>')
    return (f'<li>{_badge_prioridade(l.get("prioridade"))} '
            f'<a href="https://doi.org/{doi}" target="_blank" rel="noopener">{autores}</a> — '
            f'{titulo}. <span class="mudo">{_celula(l.get("revista"))}, {_celula(l.get("ano"))}</span>{botao}</li>')


def _guia(linhas):
    usados = set()

    def escolher(quantidade, filtro):
        saida = []
        for linha in linhas:
            if len(saida) >= quantidade:
                break
            if linha.get("doi") in usados:
                continue
            if filtro(linha):
                saida.append(linha)
                usados.add(linha.get("doi"))
        return saida

    essenciais = escolher(6, lambda l: l.get("prioridade") == "Essencial")
    metodos = escolher(5, lambda l: "Diretriz" in (l.get("tags") or []))
    if not metodos:
        metodos = escolher(4, lambda l: "Revisão" in (l.get("tags") or []))
    contexto = escolher(5, lambda l: l.get("prioridade") == "Contexto" and "Revisão" in (l.get("tags") or []))
    if not contexto:
        contexto = escolher(4, lambda l: l.get("prioridade") == "Contexto")
    base_modelo = escolher(4, lambda l: ({"Zebrafish", "Algas"} & set(l.get("tags") or []))
                          and ("Revisão" in (l.get("tags") or [])
                               or "genome" in (l.get("titulo") or "").lower()
                               or "stages of embryonic" in (l.get("titulo") or "").lower()))

    blocos = [
        ("1. Comece por estes",
         "As referências com maior utilidade para este projeto, segundo a nota da tabela.",
         essenciais),
        ("2. Para desenhar o estudo",
         "Diretrizes, protocolos e métodos que definem dados, controles e critérios.",
         metodos),
        ("3. Para interpretar e discutir",
         "Revisões e estudos de contexto para explicar mecanismos, comparar abordagens e reconhecer limitações.",
         contexto),
    ]
    if base_modelo:
        blocos.append(("4. Base do tema",
                       "Referências de base que sustentam o modelo, o método ou o conceito central.",
                       base_modelo))
    cartoes = []
    for titulo, descricao, itens in blocos:
        lista = "".join(_item_guia(l) for l in itens) or '<li class="mudo">Sem itens nesta categoria.</li>'
        cartoes.append(f'<div class="card"><h3>{titulo}</h3><p class="mudo">{descricao}</p><ul>{lista}</ul></div>')
    return '<div class="guia-grid">' + "".join(cartoes) + "</div>"


def _sintese(pasta):
    caminho = Path(pasta) / "SINTESE.md"
    if not caminho.exists():
        return '<p class="mudo">A síntese ainda não foi escrita. Rode a etapa de síntese ou crie <code>SINTESE.md</code>.</p>'
    texto = caminho.read_text(encoding="utf-8")
    texto = re.sub(r"^#\s+.*\n+", "", texto, count=1)
    return md_para_html(texto)


def _revistas(pasta):
    caminho = Path(pasta) / "revistas.csv"
    if not caminho.exists():
        return ('<p class="mudo">A revisão de revistas ainda não foi feita. '
                'Crie <code>revistas.csv</code> para mostrar esta seção.</p>', "", 0, {})
    with open(caminho, encoding="utf-8-sig") as f:
        linhas = list(csv.DictReader(f))
    contagem = {"OK": 0, "ALERTA": 0, "CONFERIR": 0, "OFICIAL": 0}
    for l in linhas:
        contagem[l.get("status", "")] = contagem.get(l.get("status", ""), 0) + 1
    mdpi = sum(1 for l in linhas if "MDPI" in (l.get("editora") or "") or "Multidisciplinary Digital" in (l.get("editora") or ""))
    classe = "aviso" if contagem.get("ALERTA") or contagem.get("CONFERIR") else "ok"
    resumo = (
        f'<p class="{classe}"><strong>{len(linhas)} fontes.</strong> '
        f'{contagem.get("OK", 0)} sem indício nas três checagens; {contagem.get("ALERTA", 0)} na lista histórica do Beall; '
        f'{contagem.get("CONFERIR", 0)} para conferir; {contagem.get("OFICIAL", 0)} documento(s) oficial(is). '
        f'Nenhuma fonte do corpus foi removida. {mdpi} periódico(s) MDPI: não constam na lista do Beall '
        f'(o próprio site diz que a editora foi excluída), estão no DOAJ ou no núcleo OpenAlex e têm debate público sobre qualidade; '
        f'não são tratados aqui como predatórios. A checagem é por nome, não detecta sequestro de título nem retratação artigo a artigo: '
        f'“sem indício” não é um selo de qualidade.</p>')
    cab = ("<div class=\"tablewrap\"><table><thead><tr><th>Revista</th><th>Editora</th><th>ISSN</th>"
           "<th>DOAJ</th><th>OpenAlex core</th><th>Beall</th><th>Refs</th><th>Status</th></tr></thead><tbody>")
    corpo = []
    for l in linhas:
        status = l.get("status", "")
        classe_status = {"OK": "rev-ok", "ALERTA": "rev-alerta", "CONFERIR": "rev-conferir", "OFICIAL": "rev-oficial"}.get(status, "")
        corpo.append(
            f'<tr><td>{_celula(l.get("revista"))}</td><td>{_celula(l.get("editora"))}</td>'
            f'<td>{_celula(l.get("issn"))}</td><td>{_celula(l.get("doaj"))}</td>'
            f'<td>{_celula(l.get("openalex_core"))}</td><td>{_celula(l.get("beall"))}</td>'
            f'<td class="n">{_celula(l.get("refs"))}</td>'
            f'<td><span class="{classe_status}">{_celula(status)}</span></td></tr>')
    tabela = cab + "".join(corpo) + "</tbody></table></div>"
    return resumo, tabela, len(linhas), contagem


def _resumos(pasta, linhas):
    blocos = []
    for l in linhas:
        caminho_rel = _resumo_rel(l.get("resumo"))
        if not caminho_rel:
            continue
        caminho = pasta / caminho_rel
        try:
            texto = caminho.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        nome = caminho.parent.name
        titulo = l.get("autores") or f'{l.get("autor") or ""} ({l.get("ano") or ""})'
        blocos.append(
            f'<section class="resumo" id="resumo-{html.escape(nome, quote=True)}" '
            f'data-titulo="{html.escape(titulo, quote=True)}">'
            f'<div class="md">{md_para_html(texto)}</div></section>')
    return "\n".join(blocos)


def _bases(pasta):
    try:
        texto = (pasta / "REFERENCIAS.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return []
    return painel.bases_sem_doi(texto)


def _faltando(pasta):
    # O caminho oficial é a raiz do projeto; o fallback aceita o log antigo
    # que o preparar_resumos.py gravava dentro de pdfs/.
    for caminho in (pasta / "download.csv", pasta / "pdfs" / "download.csv"):
        if not caminho.exists():
            continue
        try:
            with open(caminho, encoding="utf-8-sig") as f:
                return [r for r in csv.DictReader(f)
                        if (r.get("estado") or "") in ("falhou", "rejeitado", "invalido")]
        except (OSError, UnicodeError):
            continue
    return None


def gerar(pasta, saida=None):
    pasta = Path(pasta)
    if not (pasta / "tabela.json").exists():
        raise FileNotFoundError(f"{pasta/'tabela.json'} não existe; rode o painel.py antes.")
    linhas = json.loads((pasta / "tabela.json").read_text(encoding="utf-8"))
    # Não mostre "ler" para um resumo que não existe mais (tabela.json antigo).
    for linha in linhas:
        rel = _resumo_rel(linha.get("resumo"))
        if linha.get("resumo") and not (rel and (pasta / rel).is_file()):
            linha["resumo"] = ""
    tema = _titulo(pasta)
    bases = _bases(pasta)
    faltando = _faltando(pasta)
    abertos = sum(1 for l in linhas
                  if l.get("acesso") and l.get("acesso") not in ("fechado", "closed"))
    resumos = sum(1 for l in linhas if l.get("resumo"))
    essenciais = sum(1 for l in linhas if l.get("prioridade") == "Essencial")
    contexto = sum(1 for l in linhas if l.get("prioridade") == "Contexto")
    complementar = sum(1 for l in linhas if l.get("prioridade") == "Complementar")
    rev_resumo, rev_tabela, n_revistas, _rev_contagem = _revistas(pasta)
    subtitulo = (f"{len(linhas)} referências · {abertos} em acesso aberto · "
                 f"{resumos} resumos · {essenciais} essenciais")

    if faltando is None:
        bloco_faltando = ('<p class="mudo">Sem <code>download.csv</code> neste projeto. '
                          'No exemplo do repositório, o log da primeira execução não foi '
                          'preservado; num projeto novo, rode o <code>preparar_resumos.py</code> '
                          'para gerar a lista do que falta.</p>')
        n_faltando = "—"
    elif not faltando:
        bloco_faltando = '<p class="ok">Todos os PDFs de acesso aberto foram baixados.</p>'
        n_faltando = 0
    else:
        linhas_f = ["<div class=\"tablewrap\"><table><thead><tr><th>Arquivo</th><th>DOI</th>"
                    "<th>Título</th><th>Motivo</th></tr></thead><tbody>"]
        for r in faltando:
            linhas_f.append(
                f'<tr><td><code>{_celula(r.get("slug"))}.pdf</code></td>'
                f'<td>{_celula(r.get("doi"))}</td><td>{_celula(r.get("titulo"))}</td>'
                f'<td>{_celula(r.get("detalhe"))}</td></tr>')
        linhas_f.append("</tbody></table></div>")
        linhas_f.append('<p class="aviso">Salve cada PDF em <code>pdfs/</code> com o nome da '
                        'primeira coluna e rode o <code>preparar_resumos.py</code> de novo. '
                        'A lista também está em <code>pdfs/FALTANDO.md</code>.</p>')
        bloco_faltando = "\n".join(linhas_f)
        n_faltando = len(faltando)

    blocos_bases = []
    for autor, titulo, link in bases:
        blocos_bases.append(
            f'<tr><td>{_celula(autor)}</td><td>{_celula(titulo)}</td>'
            f'<td><a href="{html.escape(link, quote=True)}" target="_blank" rel="noopener">{_celula(link)}</a></td></tr>')
    bloco_bases = "\n".join(blocos_bases) or '<tr><td colspan="3" class="mudo">Nenhuma base sem DOI.</td></tr>'

    pagina = (RAIZ / "modelos" / "relatorio.html").read_text(encoding="utf-8")
    trocas = {
        "TITULO": html.escape(tema),
        "SUBTITULO": html.escape(subtitulo),
        "DATA": datetime.date.today().strftime("%d/%m/%Y"),
        "N_REFS": len(linhas),
        "N_ABERTOS": abertos,
        "N_RESUMOS": resumos,
        "N_ESSENCIAIS": essenciais,
        "N_CONTEXTO": contexto,
        "N_COMPLEMENTAR": complementar,
        "N_BASES": len(bases),
        "N_FALTANDO": n_faltando,
        "N_REVISTAS": n_revistas,
        "LEGENDA": relevancia.legenda(pasta),
        "OPCOES_ACESSO": _opcoes_acesso(linhas),
        "OPCOES_TEMA": _opcoes_tema(linhas),
        "OPCOES_PRIORIDADE": _opcoes_prioridade(),
        "GUIA": _guia(linhas),
        "SINTESE": _sintese(pasta),
        "REVISTAS_RESUMO": rev_resumo,
        "REVISTAS_TABELA": rev_tabela,
        "TABELA": "\n".join(_linha(l) for l in linhas),
        "BASES": bloco_bases,
        "FALTANDO": bloco_faltando,
        "RESUMOS": _resumos(pasta, linhas),
    }
    marcadores = set(re.findall(r"\{\{([A-Z_]+)\}\}", pagina))
    assert marcadores <= set(trocas), f"marcadores sem valor: {sorted(marcadores - set(trocas))}"
    pagina = re.sub(r"\{\{([A-Z_]+)\}\}",
                    lambda m: str(trocas[m.group(1)]), pagina)
    destino = Path(saida) if saida else pasta / "RELATORIO.html"
    destino.write_text(pagina, encoding="utf-8")
    print(f"{len(linhas)} referências, {resumos} resumos, {len(bases)} bases sem DOI -> {destino}")
    return destino


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gera um RELATORIO.html autocontido a partir da tabela e dos resumos.")
    ap.add_argument("pasta", help="pasta do levantamento (ex.: projetos/meu-tema)")
    ap.add_argument("--saida", default="", help="arquivo de saída (padrão: <pasta>/RELATORIO.html)")
    opcao_exemplo(ap)
    a = ap.parse_args(argv)
    barrar_exemplo(ap, a, a.pasta, a.saida)
    gerar(a.pasta, a.saida or None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
