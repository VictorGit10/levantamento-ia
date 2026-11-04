import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "ferramentas"))

import relevancia  # noqa: E402


def test_classificar_composto_e_modelo():
    linha = {
        "doi": "10.1234/exemplo",
        "titulo": "Geraniol toxicity in zebrafish embryos",
        "revista": "Exemplo",
        "acesso": "aberto (revista)",
        "resumo": "resumos/exemplo/RELATORIO.md",
        "ano": "2024",
        "citacoes": 10,
    }
    meta = {"area": "zebrafish", "resultado": "LC50", "frentes": ["1-zebrafish-modelo"]}
    c = relevancia.classificar(linha, meta, {})
    assert "Geraniol" in c["tags"]
    assert "Zebrafish" in c["tags"]
    assert c["score"] > 0
    assert c["prioridade"] in ("Essencial", "Contexto")


def test_generico_nao_quebra_projeto_sem_config(tmp_path):
    (tmp_path / "REFERENCIAS.md").write_text(
        "## 1-sensores\n\n"
        "| Autores (ano) | Título | Revista | DOI/link | Dados | Método | Área | Resultado principal |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| Silva (2020) | Sensores ópticos | Revista | 10.1234/exemplo | 10 amostras | Campo | sensores | R2 = 0,9 |\n",
        encoding="utf-8",
    )
    linhas = [{
        "doi": "10.1234/exemplo", "titulo": "Sensores ópticos", "revista": "Revista",
        "acesso": "fechado", "resumo": "", "ano": "2020", "citacoes": 10,
    }]
    relevancia.generico(tmp_path, linhas)
    assert linhas[0]["tags"]
    assert linhas[0]["score"] > 0
    assert linhas[0]["prioridade"] in ("Essencial", "Contexto", "Complementar")


def test_legenda_padrao(tmp_path):
    texto = relevancia.legenda(tmp_path)
    assert "frente" in texto.lower()
