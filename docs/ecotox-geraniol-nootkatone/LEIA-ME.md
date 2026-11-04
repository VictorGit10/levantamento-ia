# Levantamento: Avaliação da ecotoxicidade aquática de geraniol e nootkatone com zebrafish e algas

Gerado em 04/11/2026.

## Abra primeiro

- [`RELATORIO.html`](index.html) — guia de leitura, síntese, tabela navegável com filtros e os resumos.
- [`SINTESE.md`](SINTESE.md) — o que o conjunto diz sobre zebrafish, algas, geraniol e nootkatone, com as lacunas e um desenho experimental sugerido.
- [`TABELA.md`](TABELA.md) — a mesma lista em texto, ordenada por utilidade para o projeto.
- [`REFERENCIAS.md`](REFERENCIAS.md) — as referências separadas por frente e o que cada busca concluiu.
- [`REVISAO-EXTERNA.md`](REVISAO-EXTERNA.md) — a busca independente do Codex/DeepSeek e as 5 referências que ela acrescentou.
- [`REVISAO-REVISTAS.md`](REVISAO-REVISTAS.md) — a checagem de periódicos (DOAJ, OpenAlex e lista do Beall).
- [`referencias.bib`](referencias.bib) — para importar no Zotero ou no Mendeley.

## O que já está pronto

- 75 referências com DOI.
- 44 em acesso aberto.
- 29 resumos de leitura (um deles é só o suplemento; ver a síntese).
- 3 bases e relatórios oficiais sem DOI.
- 0 revistas em alerta na checagem de periódicos; 50 fontes sem alerta e 1 documento oficial.
- O único `CONFERIR` do `conferir_doi.py` é a OECD 201: o DOI aponta para a versão atual, com título legado no Crossref; é o mesmo documento.

## PDFs que faltam

15 PDFs não foram baixados. A lista com o nome de arquivo de cada um está em [`pdfs/FALTANDO.md`](pdfs/FALTANDO.md).

Para completar: baixe o artigo pelo navegador (só acesso aberto), salve em `pdfs/` com o nome indicado e rode de novo o comando abaixo. O script aproveita o que já está na pasta.

- `pavela2016.pdf` — Essential Oils as Ecofriendly Biopesticides? Challenges and Constraints
- `chen2010.pdf` — Geraniol — A review of a commercially important fragrance material
- `jordan2012.pdf` — Efficacy of Plant-Derived and Synthetic Compounds on Clothing as Repellents AgainstIxodes scapularisandAmblyomma americanum(Acari: Ixodidae)
- `kusk2018.pdf` — Algal growth inhibition test results of 425 organic chemical substances
- `bharadwaj2012.pdf` — Efficacy and Environmental Persistence of Nootkatone for the Control of the Blacklegged Tick (Acari: Ixodidae) in Residential Landscapes
- `rico2017.pdf` — Effects of temperature, genetic variation and species competition on the sensitivity of algae populations to the antibiotic enrofloxacin
- `norris2022.pdf` — Mode of action and toxicological effects of the sesquiterpenoid, nootkatone, in insects
- `hundrinke2022.pdf` — Testing particles using the algal growth inhibition test (OECD 201): the suitability of in vivo chlorophyll fluorescence measurements
- `miura2021.pdf` — Study of the chemical composition and ecotoxicological evaluation of essential oils in Daphnia magna with potential use in aquaculture
- `carneiro2022.pdf` — Oxidative stress as the trigger for menthol-induced developmental alterations in zebrafish (Danio rerio) model
- … e mais 5.

## Como continuar

Rode a partir da pasta do repositório:

```bash
python ferramentas/preparar_resumos.py "projetos/ecotox-geraniol-nootkatone/cienciometria.csv" "projetos/ecotox-geraniol-nootkatone/pdfs" "projetos/ecotox-geraniol-nootkatone/resumos" modelos/PEDIDO-resumo.md "Avaliação da ecotoxicidade aquática de geraniol e nootkatone com zebrafish e algas" --abrir
python ferramentas/orquestrar.py "projetos/ecotox-geraniol-nootkatone/resumos" --paralelo 2
python ferramentas/painel.py "projetos/ecotox-geraniol-nootkatone"
python ferramentas/publicar.py "projetos/ecotox-geraniol-nootkatone"
```

## Formatos

| Camada | Arquivos | Para quê |
|---|---|---|
| Para ler | `RELATORIO.html`, `TABELA.md`, `REFERENCIAS.md` | consulta e leitura |
| Para citar | `referencias.bib` | Zotero, Mendeley, LaTeX |
| Para analisar | `cienciometria.csv`, `tabela.json`, `verificacao.csv`, `download.csv` | planilha e scripts |
| Interno | `pdfs/`, `resumos/*/TEXTO.txt`, `log.jsonl` | não publicar (direitos autorais) |

Os números dos resumos vêm com a página; confira no artigo antes de citar.
