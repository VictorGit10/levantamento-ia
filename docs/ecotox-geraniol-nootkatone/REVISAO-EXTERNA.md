# Revisão externa da busca

## 1. Método

Busca independente feita em 04/11/2026, em português e inglês, por ferramenta de busca na web
(Google Scholar, PubMed, Europe PMC, Crossref, OpenAlex e páginas de editoras/órgãos). Termos
principais: "geraniol ecotoxicidade aquática", "geraniol algae EC50", "nootkatone Daphnia/Artemia/mussel",
"geraniol/nootkatone destino ambiental hidrólise fotodegradação biodegradação", "óleos essenciais
organismos não-alvo aquáticos revisão", "terpenoides ecotoxicologia revisão", "botanical insecticides
non-target aquatic organisms review". Também consultei a conclusão de registro da EFSA e bases
regulatórias (dossiê UE) para os endpoints aquáticos de geraniol.

O que consegui abrir: páginas de resultado com metadados completos de doi.org, PubMed, ScienceDirect,
MDPI (inclusive o PDF aberto de Molecules), ProQuest e DTU Orbit. A chamada HTTP direta à API do
Crossref estava bloqueada no ambiente de execução, então a confirmação dos DOIs foi feita resolvendo
cada DOI nas páginas oficiais acima (todas mostram o DOI, autores, título e revista). Não baixei PDFs
de artigos fechados; não alterei nenhum arquivo do corpus além de gravar este relatório.

## 2. Cobertura por frente

- **1 — zebrafish como modelo:** cobre bem. Estão presentes os seminais (Howe et al. 2013; Kimmel et al.
  1995), a validação do FET (Braunbeck et al. 2015), a comparação FET × teste agudo (Birke & Scholz 2019)
  e as diretrizes OECD 203/210/212/236. Não identifiquei lacuna relevante.
- **2 — nootkatone:** cobre bem para química, atividade inseticida/acaricida/repelente, modo de ação e
  registro (EPA 2020a/2020b). Cobre parcialmente em ecotoxicidade aquática: há o zebrafish de Konig et al.
  (2026) e o EC50 de peixe/invertebrado da EPA, mas continua sem EC50 algal (nem na documentação da EPA) e
  sem estudo primário em outra espécie de peixe, Daphnia, Artemia, mexilhão ou anfípode.
- **3 — geraniol:** cobre bem para química, inseticida e toxicologia, incluindo o único LC50 em zebrafish
  (Singulani et al. 2018). Tem uma lacuna importante de cobertura: a frente concluiu que "não há EC50 algal
  experimental", mas esse valor **existe em fonte regulatória** (conclusão da EFSA) — ver seção 3. Falta
  incluir revisões seminais/atuais do geraniol (Chen & Viljoen 2010; Mączka et al. 2020).
- **4 — algas como modelo:** cobre bem (OECD 201, ISO 8692, espécies, endpoints, fluorescência, citometria,
  variabilidade entre espécies). Cobre parcialmente por não citar a maior compilação algal experimental
  homogênea disponível (Kusk et al. 2018, 425 compostos), que pode conter geraniol.
- **5 — estudos ecotoxicológicos aquáticos dos dois compostos e terpenoides próximos:** cobre bem para
  zebrafish (compostos-alvo e análogos) e para a meta-análise Daphnia × óleos essenciais (Afonso et al. 2024).
  Cobre parcialmente: não há dado experimental publicado de Daphnia/Artemia/mexilhão/anfípode para geraniol
  ou nootkatone; os únicos valores de Daphnia/peixe para geraniol são regulatórios (EFSA).

## 3. Referências ausentes que valem a pena

| Autores (ano) | Título | Revista | DOI | Por que entra | Frente |
|---|---|---|---|---|---|
| EFSA (2012) | Conclusion on the peer review of the pesticide risk assessment of the active substance geraniol | EFSA Journal 10(11):2915 | 10.2903/j.efsa.2012.2915 | Traz os endpoints regulatórios de referência do geraniol: EC50 algal experimental (48,0 mg/L, *Raphidocelis subcapitata*, 72 h), EC50 de *Daphnia magna* (16,1 mg/L, 48 h) e LC50 de peixe (11,6 mg/L, *Oncorhynchus mykiss*, 96 h). Muda a conclusão da síntese: **existe** EC50 algal para geraniol em fonte de agência; o que falta é o dado publicado revisado por pares. | 3/4/5 |
| Chen & Viljoen (2010) | Geraniol — a review of a commercially important fragrance material | South African Journal of Botany 76(4):643–651 | 10.1016/j.sajb.2010.05.008 | Revisão seminal do geraniol (fontes, biossíntese, atividade biológica e toxicidade); base citada por quase toda a literatura posterior do composto. | 3 |
| Mączka, Wińska & Grabarczyk (2020) | One Hundred Faces of Geraniol | Molecules 25(14):3303 | 10.3390/molecules25143303 | Revisão recente e aberta que consolida bioatividade, metabolismo e segurança do geraniol; cobre o período 2015–2026 que a frente prioriza. | 3 |
| Kusk, Christensen & Nyholm (2018) | Algal growth inhibition test results of 425 organic chemical substances | Chemosphere 204:405–412 | 10.1016/j.chemosphere.2018.04.047 | Maior compilação algal experimental homogênea (EC50 de 425 compostos em *P. subcapitata*, sistema fechado, 48 h). Vale conferir no material suplementar se geraniol está na lista — é a fonte mais provável para um EC50 algal experimental fora do corpus. | 4/5 |
| Pavela & Benelli (2016) | Essential Oils as Ecofriendly Biopesticides? Challenges and Constraints | Trends in Plant Science 21(12):1000–1007 | 10.1016/j.tplants.2016.10.005 | Revisão de referência sobre os limites dos biopesticidas de óleos essenciais, incluindo toxicidade a organismos não-alvo e as barreiras regulatórias (autorização, formulação). Contexto direto para a pergunta do projeto. | 2/5 |

## 4. Referências do corpus que parecem fora do escopo ou duvidosas

Não encontrei referência claramente fora do escopo que precise ser removida. Duas merecem atenção,
mas já estão sinalizadas nas próprias notas das frentes:

| Referência | Problema | O que fazer |
|---|---|---|
| Cavaco & Faria (2024), *Toxics* | Estudo de triagem in silico/base de dados; não mede destino ambiental nem ecotoxicidade experimental. | Manter, desde que sempre citado como modelagem/predição (a frente já registra isso). |
| Darrag et al. (2026), *Toxins* | Os valores de LC50/EC50 são predições ADMET/QSAR, não medidas experimentais. | Manter com a ressalva de "valor predito" (a síntese já faz isso). |

## 5. Veredito

A busca atual é suficiente e de boa qualidade para os objetivos do projeto: cobre bem os dois modelos
(zebrafish e algas) e os dois compostos, com as lacunas experimentais corretamente identificadas. A
correção principal é de precisão: a síntese diz que "não foi encontrado EC50 algal para geraniol", mas
esse valor existe em fonte regulatória (EFSA: 48 mg/L em *R. subcapitata*), e há EC50 de Daphnia (16,1 mg/L)
e LC50 de peixe (11,6 mg/L). O que realmente falta — e que o projeto pode preencher como contribuição
original — é o **dado experimental publicado/revisado por pares** de EC50 algal (para os dois compostos)
e de Daphnia, além do EC50 algal do nootkatone, que não aparece nem na documentação da EPA. Recomendo
acrescentar as cinco referências da seção 3 e reformular na síntese a frase sobre o EC50 algal de geraniol
para "sem EC50 algal publicado em periódico revisado por pares; existe o valor regulatório da EFSA".