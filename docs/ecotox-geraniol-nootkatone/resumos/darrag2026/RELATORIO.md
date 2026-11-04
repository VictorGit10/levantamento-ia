# RELATÓRIO — El Mehdi Darrag (2026)

## 1. Referência

Darrag, E. M.; Essadki, Y.; Zekri, S.; Chernane, H.; Romane, A.; Hdoufane, I.; Cherqaoui, D.; Oudra, B.; Meddich, A.; Vasconcelos, V.; Baçaoui, A. (2026). *Algicidal Monoterpenes Against Toxin-Producing Microcystis aeruginosa with Reduced Toxicity Toward Chlorella sorokiniana: In Vitro, Molecular Docking, and ADMET Study*. **Toxins**, 18, 258. DOI: 10.3390/toxins18060258. Publicado em 5 de junho de 2026 [p. 1]. O `TEXTO.txt` contém o artigo integral (34 páginas, incluindo referências e Apêndice A).

## 2. Pergunta do estudo

Dez monoterpenos têm atividade algicida seletiva contra a cianobactéria toxigênica *Microcystis aeruginosa* sem inibir a microalga benéfica *Chlorella sorokiniana*, e docking molecular e ADMET explicam essa seletividade? [p. 3]

## 3. Área e dados

- Local: laboratórios da Faculdade de Ciências Semlalia, Universidade Cadi Ayyad, Marrakech, Marrocos [p. 1].
- Organismos: *M. aeruginosa* cepa MCAUt, não axênica, monoclonal e toxigênica, isolada do reservatório eutrófico Lalla Takerkoust em 2015 [p. 23]; *C. sorokiniana* não axênica, isolada em 2017 de um lago artificial do Departamento de Biologia da mesma faculdade [p. 23].
- Compostos: 10 monoterpenos (borneol, α-terpinene, 2-carene, carvacrol, camphor, carvone, α-pinene, thymol, geraniol, limonene) com pureza ≥ 98% [p. 22], mais controles positivo (sulfato de cobre 30 mg/mL) e negativo (DMSO) [p. 3, 23].
- Delineamento: 2 organismos × 10 compostos × 2 ensaios (disco e MIC), cada tratamento em triplicata [p. 23–24]; 6 proteínas-alvo × 10 ligantes = 60 pares de docking [p. 9–10]; ADMET in silico para os 10 compostos [p. 5–8].
- Datas de acesso às bases: SwissADME e ProTox-II em 12/08/2022, VEGA HUB em 26/05/2026, PubChem em 10/02/2025 [p. 24–25].
- Não há sensores nem trabalho de campo; todos os dados são de bancada ou computacionais [p. 22–25].

## 4. Método

- **Disc diffusion method (DDM)**: ágar duplo, disco de 6 mm embebido com 20 µL de solução 50 mg/mL (1 mg/disco), incubação de 10 dias a 2500 lux, fotoperíodo 15:9 e 25 ± 2 °C; halo medido em mm [p. 23].
- **MIC por microdiluição em caldo**: placas de 96 poços, inóculo ajustado a 4 × 10⁶ células/mL, volume final de 200 µL, 8 dias de incubação [p. 23–24].
- **Selectivity index (SI)** = MIC de *C. sorokiniana* / MIC de *M. aeruginosa* [p. 24].
- **In silico**: SwissADME e ProTox-3.0; ecotoxicidade por modelos QSAR do VEGA HUB (Arnot–Gobas, EPA, IRFMN, ProtoQSAR-Combase, CONCERT) [p. 24]; docking em 6 proteínas preditas por AlphaFold2, com cavidades por POCASA e CB-Dock2, minimização MMFF94 e AutoDock Vina 1.2.5 [p. 24–25].

## 5. Resultados principais

- DDM contra *M. aeruginosa*: halos de 6.9 a 43.6 mm; apenas 5 dos 10 compostos ativos; thymol com o maior halo, 43.57 ± 0.12 mm [p. 1, 3].
- DDM contra *C. sorokiniana*: 9 dos 10 ativos, halos de 8.6 a 29.2 mm, carvacrol o maior (29.20 ± 0.35 mm); camphor sem halo [p. 3].
- MIC para *M. aeruginosa*: 0.25 mg/mL com carvacrol, carvone e thymol; 0.5 mg/mL com camphor, 2-carene e α-pinene; 1 mg/mL com borneol; > 1 mg/mL com α-terpinene, geraniol e limonene [p. 4].
- MIC para *C. sorokiniana*: 0.125 mg/mL com 2-carene, α-pinene e thymol; 0.25 mg/mL com carvacrol; 0.5 mg/mL com carvone; 1 mg/mL com borneol, α-terpinene, geraniol e limonene; camphor inativo [p. 4].
- SI: carvone 2.00 e camphor > 1.00 (preferência pela cianobactéria); thymol 0.50, 2-carene 0.25, α-pinene 0.25, demais < 1.00 [p. 3].
- Docking: afinidades de −3.9 a −6.2 kcal/mol no conjunto composto–alvo; a ATP synthase de *M. aeruginosa* foi o alvo mais receptivo (α-terpinene e carvacrol −6.2 kcal/mol; limonene −6.1; carvone −6.0), e a SOD de *M. aeruginosa* o menos receptivo (−3.9 a −4.4 kcal/mol) [p. 10].
- Cavidades: maior sítio em AF-P51764-F1 (*M. aeruginosa*, fotossíntese), 812 Å³ (VD 2527); SOD com 80 e 94 Å³ [p. 9].
- ADME: LogP consenso de 2.37 (camphor) a 3.44 (α-pinene); TPSA ≤ 20.23 Å²; bioavailability score 0.55 para todos; todos atravessam a barreira hematoencefálica e nenhum é substrato de P-gp; só thymol e carvacrol inibem CYP1A2 [p. 5–6].
- ProTox: todos não hepatotóxicos (probabilidade 0.65, carvone, a 0.86, α-pinene), não carcinogênicos (0.60–0.83); LD50 oral predita de 500 a 4800 mg/kg, classes 4 e 5 [p. 6].
- VEGA HUB: BCF de 1.52 a 3.34 log(L/kg), com 2-carene (3.24), limonene (3.02), α-pinene (3.34) e α-terpinene (3.01) no limiar REACH de 3.3 log(L/kg); LC50 em peixe de 1.84 (2-carene) a 100 mg/L (borneol); EC50 em *Daphnia magna* de 1.10 (limonene) a 21.96 mg/L (carvone); EC50 em algas de 2.24 a 74.65 mg/L; NOEC em minhoca de 11.13 (carvone) a 197.07 mg/kg (geraniol) [p. 6, 8].

## 6. Limitações que os próprios autores reconhecem

- As duas cepas são não axênicas, e a influência de bactérias heterotróficas associadas sobre a atividade inibitória não pode ser excluída; recomendam cepas axênicas [p. 18].
- Nenhuma das 6 proteínas tem estrutura tridimensional resolvida experimentalmente no PDB; todas são modelos AlphaFold2, e a ausência de estados de referência com ligante impede validar diretamente a geometria das cavidades [p. 20].
- SwissADME e ProTox-3.0 foram treinados sobretudo com fármacos sintéticos, e os modelos QSAR não capturam evaporação, fotodegradação nem biotransformação microbiana, de modo que o risco previsto pode superestimar o risco real [p. 19].
- O DDM subestima compostos hidrofóbicos e voláteis (difusão pobre em ágar, volatilização, adsorção à matriz); os autores consideram o MIC mais confiável [p. 5].
- Não se deve assumir correspondência quantitativa direta entre afinidade de docking e MIC [p. 20]; faltam ensaios de inibição enzimática, co-cristalização e estudos OECD TG 201, 202 e 203 [p. 19, 22].

## 7. O que serve ao projeto e o que não serve

- **Serve**: o geraniol foi testado nas duas algas — MIC > 1 mg/mL contra *M. aeruginosa* e 1 mg/mL contra *C. sorokiniana*, SI < 1, sem halo contra *M. aeruginosa* e 13.03 mm contra *C. sorokiniana* [p. 3]; é um dos menos ativos do painel [p. 4].
- **Serve**: perfil ecotoxicológico in silico do geraniol para comparação com dados experimentais — BCF 2.44 log(L/kg), LC50 em peixe 9.81 mg/L, EC50 em *Daphnia* 16.09 mg/L, EC50 em algas 2.73 mg/L, NOEC em minhoca 197.07 mg/kg, LD50 oral 2100 mg/kg (classe 5) [p. 8].
- **Serve**: o desenho MIC + SI e o alerta sobre volatilização e adsorção no DDM são úteis para padronizar ensaios com monoterpenos voláteis [p. 5, 24].
- **Não serve**: não há dados de nootkatone (composto não testado) nem qualquer ensaio com zebrafish — a toxicidade em peixe é apenas predição QSAR para *Fathead Minnow* (EPA), não experimento [p. 6, 8].

## 8. Frases citáveis (literais)

> "As both algal strains used in this study were non-axenic, the potential influence of associated heterotrophic bacteria on the observed inhibitory activity cannot be entirely excluded." [p. 18]

> "Empirical validation through standardized OECD guideline studies (TG 201 for algae, TG 202 for Daphnia magna, and TG 203 for fish) remains an essential next step before any of these candidates can be responsibly advanced toward field-scale bloom management applications." [p. 19]
