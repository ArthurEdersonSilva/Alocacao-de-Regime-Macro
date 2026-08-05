# Relatório Analítico Detalhado

## Alocação Quantitativa por Regimes Macroeconômicos

**Versão do gerador:** 3.0.0  
**Gerado em:** 05/08/2026 06:00:24 Hora oficial do Brasil  
**Período disponível na base consolidada:** 31/01/2020 a 31/08/2026  
**Universo:** 12 ativos selecionados  

> O relatório separa desenvolvimento, validação e teste final fora da amostra. Resultados desses blocos não devem ser misturados, pois cumprem funções diferentes.

---

## 1. Resumo executivo

A estratégia utiliza inflação e atividade econômica para classificar o cenário brasileiro e ajustar uma carteira multimercado. A avaliação temporal oficial é:

| Período | Função | Início oficial | Fim oficial | Início disponível | Fim disponível | Meses disponíveis | Meses esperados | Cobertura | Ajusta parâmetros? | Altera regras? | Estratégia | Benchmark | CDI | Excesso vs benchmark | Excesso vs CDI | Volatilidade anualizada | Sharpe | Drawdown máximo | Turnover total | Custo total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Desenvolvimento e calibração | Construção, testes e escolha dos parâmetros | 01/01/2020 | 31/12/2023 | 31/01/2020 | 31/12/2023 | 48 | 48 | 100,00% | Sim | Sim | 34,22% | 34,22% | 36,32% | 0,00% | -2,10% | 8,51% | -0,00 | -8,32% | 219,69% | 0,22% |
| Validação | Avaliação das regras e parâmetros congelados | 01/01/2024 | 31/12/2025 | 31/01/2024 | 31/12/2025 | 24 | 24 | 100,00% | Não | Não | 22,15% | 22,15% | 26,76% | 0,00% | -4,61% | 6,47% | -0,26 | -2,98% | 44,01% | 0,04% |
| Teste final fora da amostra | Teste final de generalização sem novos ajustes | 01/01/2026 | 02/08/2026 | 31/01/2026 | 31/07/2026 | 7 | 8 | 87,50% | Não | Não | 5,04% | 5,04% | 5,66% | 0,00% | -0,62% | 14,94% | -0,04 | -3,45% | 12,73% | 0,01% |

- A estratégia acumulou **72,22%**, com volatilidade anualizada de **8,33%** e drawdown máximo de **-8,32%**.
- A diferença acumulada contra o benchmark foi de **0,00%**.
- O melhor ativo no período foi **GC=F**, com **171,53%**.
- O pior ativo no período foi **JPYBRL=X**, com **-12,50%**.
- O melhor regime para a estratégia foi **Expansão inflacionária**.
- O pior regime para a estratégia foi **Estagflação**.
- A estratégia superou o benchmark em **0,00%** das janelas móveis de 12 meses.

### Regra de interpretação dos resultados

- **2020–2023:** resultados de desenvolvimento podem refletir calibração e não são prova de generalização.
- **2024–2025:** validação com parâmetros e regras congelados.
- **2026:** teste final fora da amostra, também sem alteração de regras ou parâmetros.

---

## 2. Metodologia temporal oficial

| Período | Função | Ajusta parâmetros? | Altera regras? |
| --- | --- | ---: | ---: |
| 01/01/2020 a 31/12/2023 | Desenvolvimento e calibração | Sim | Sim |
| 01/01/2024 a 31/12/2025 | Validação | Não | Não |
| 01/01/2026 a 02/08/2026 | Teste final fora da amostra | Não | Não |

```text
Dados e retornos: mensais
Rebalanceamento: mensal
Confirmação do regime: 3 meses
Defasagem do sinal: 1 mês
Recalibração walk-forward: anual
Treino inicial: 48 meses
Janela de treino: expansiva
Focus: consulta semanal, mas sinal oficial mensal
```

---

## 3. Fontes, qualidade e atualização

### Arquivos centrais

| arquivo | caminho | existe | modificacao_utc | tamanho_bytes | possivelmente_desatualizado |
| --- | --- | --- | --- | --- | --- |
| selecao | data/processed/ativos_selecionados_modelo.csv | Sim | 04/08/2026 23:53 | 1951 | Não |
| retornos | data/processed/retornos_ativos.csv | Sim | 04/08/2026 23:57 | 394387 | Não |
| macro | data/processed/dados_macro_mensais.csv | Sim | 04/08/2026 23:57 | 49127 | Não |
| regimes | data/processed/regimes_macroeconomicos.csv | Sim | 04/08/2026 23:58 | 71965 | Não |
| alocacao | data/processed/alocacao_portfolio_mensal.csv | Sim | 05/08/2026 00:06 | 81281 | Não |
| backtest | data/processed/backtest_portfolio_mensal.csv | Sim | 05/08/2026 00:06 | 124847 | Não |
| series_finais | outputs/tabelas/06_12_series_modelos_finais.csv | Sim | 05/08/2026 00:09 | 34101 | Não |
| metricas_finais | outputs/tabelas/06_12_metricas_finais_modelos.csv | Sim | 05/08/2026 00:09 | 2705 | Não |
| pesos_oficiais | outputs/tabelas/06_12_pesos_oficiais_atuais.csv | Sim | 05/08/2026 00:09 | 1316 | Não |
| scorecard | outputs/tabelas/07_05_scorecard_executivo.csv | Não | — | 0 | Não |
| auditoria | outputs/auditoria/08_06_diagnostico_final_corrigido.csv | Não | — | 0 | Não |

### Cobertura das bases

| base | registros | inicio | fim | colunas | ausentes |
| --- | --- | --- | --- | --- | --- |
| retornos_diarios | 1597 | 03/01/2020 | 04/08/2026 | 13 | 0 |
| retornos_mensais | 80 | 31/01/2020 | 31/08/2026 | 13 | 0 |
| macro | 272 | 31/01/2004 | 31/08/2026 | 12 | 84 |
| regimes | 255 | 31/03/2005 | 31/05/2026 | 25 | 172 |
| alocacao | 77 | 31/01/2020 | 31/05/2026 | 57 | 0 |
| backtest | 77 | 31/01/2020 | 31/05/2026 | 90 | 0 |
| series_finais | 29 | 31/01/2024 | 31/05/2026 | 73 | 0 |

### Inventário das saídas do pipeline

| Origem | Arquivo | Caminho | Extensão | Modificação UTC | Bytes | Situação temporal |
| --- | --- | --- | --- | --- | --- | --- |
| graficos | 01_atualizacao_series_macro.png | outputs/graficos/01_atualizacao_series_macro.png | .png | 04/08/2026 23:57 | 45.546 | Mesma execução provável |
| graficos | 01_cobertura_dados_ativos.png | outputs/graficos/01_cobertura_dados_ativos.png | .png | 04/08/2026 23:57 | 104.134 | Mesma execução provável |
| graficos | 02_08_precos_normalizados_commodities.png | outputs/graficos/02_08_precos_normalizados_commodities.png | .png | 04/08/2026 23:57 | 216.167 | Mesma execução provável |
| graficos | 02_08_precos_normalizados_moedas.png | outputs/graficos/02_08_precos_normalizados_moedas.png | .png | 04/08/2026 23:57 | 269.364 | Mesma execução provável |
| graficos | 02_08_precos_normalizados_renda_fixa.png | outputs/graficos/02_08_precos_normalizados_renda_fixa.png | .png | 04/08/2026 23:57 | 154.959 | Mesma execução provável |
| graficos | 02_08_precos_normalizados_renda_variavel.png | outputs/graficos/02_08_precos_normalizados_renda_variavel.png | .png | 04/08/2026 23:57 | 240.984 | Mesma execução provável |
| graficos | 02_09_retorno_acumulado_commodities.png | outputs/graficos/02_09_retorno_acumulado_commodities.png | .png | 04/08/2026 23:57 | 216.683 | Mesma execução provável |
| graficos | 02_09_retorno_acumulado_moedas.png | outputs/graficos/02_09_retorno_acumulado_moedas.png | .png | 04/08/2026 23:57 | 269.208 | Mesma execução provável |
| graficos | 02_09_retorno_acumulado_renda_fixa.png | outputs/graficos/02_09_retorno_acumulado_renda_fixa.png | .png | 04/08/2026 23:57 | 154.774 | Mesma execução provável |
| graficos | 02_09_retorno_acumulado_renda_variavel.png | outputs/graficos/02_09_retorno_acumulado_renda_variavel.png | .png | 04/08/2026 23:57 | 241.419 | Mesma execução provável |
| graficos | 02_10_volatilidade_movel_commodities.png | outputs/graficos/02_10_volatilidade_movel_commodities.png | .png | 04/08/2026 23:57 | 174.471 | Mesma execução provável |
| graficos | 02_10_volatilidade_movel_moedas.png | outputs/graficos/02_10_volatilidade_movel_moedas.png | .png | 04/08/2026 23:57 | 224.573 | Mesma execução provável |
| graficos | 02_10_volatilidade_movel_renda_fixa.png | outputs/graficos/02_10_volatilidade_movel_renda_fixa.png | .png | 04/08/2026 23:57 | 109.957 | Mesma execução provável |
| graficos | 02_10_volatilidade_movel_renda_variavel.png | outputs/graficos/02_10_volatilidade_movel_renda_variavel.png | .png | 04/08/2026 23:57 | 191.719 | Mesma execução provável |
| graficos | 02_11_drawdown_ativos_commodities.png | outputs/graficos/02_11_drawdown_ativos_commodities.png | .png | 04/08/2026 23:57 | 258.434 | Mesma execução provável |
| graficos | 02_11_drawdown_ativos_moedas.png | outputs/graficos/02_11_drawdown_ativos_moedas.png | .png | 04/08/2026 23:57 | 268.203 | Mesma execução provável |
| graficos | 02_11_drawdown_ativos_renda_fixa.png | outputs/graficos/02_11_drawdown_ativos_renda_fixa.png | .png | 04/08/2026 23:57 | 199.988 | Mesma execução provável |
| graficos | 02_11_drawdown_ativos_renda_variavel.png | outputs/graficos/02_11_drawdown_ativos_renda_variavel.png | .png | 04/08/2026 23:57 | 303.256 | Mesma execução provável |
| graficos | 02_12_correlacao_retornos_commodities.png | outputs/graficos/02_12_correlacao_retornos_commodities.png | .png | 04/08/2026 23:57 | 43.715 | Mesma execução provável |
| graficos | 02_12_correlacao_retornos_consolidada.png | outputs/graficos/02_12_correlacao_retornos_consolidada.png | .png | 04/08/2026 23:57 | 167.629 | Mesma execução provável |
| graficos | 02_12_correlacao_retornos_moedas.png | outputs/graficos/02_12_correlacao_retornos_moedas.png | .png | 04/08/2026 23:57 | 51.268 | Mesma execução provável |
| graficos | 02_12_correlacao_retornos_renda_fixa.png | outputs/graficos/02_12_correlacao_retornos_renda_fixa.png | .png | 04/08/2026 23:57 | 52.909 | Mesma execução provável |
| graficos | 02_12_correlacao_retornos_renda_variavel.png | outputs/graficos/02_12_correlacao_retornos_renda_variavel.png | .png | 04/08/2026 23:57 | 55.059 | Mesma execução provável |
| graficos | 02_13_ipca_12_meses.png | outputs/graficos/02_13_ipca_12_meses.png | .png | 04/08/2026 23:57 | 109.701 | Mesma execução provável |
| graficos | 02_14_ibc_br_dessazonalizado.png | outputs/graficos/02_14_ibc_br_dessazonalizado.png | .png | 04/08/2026 23:57 | 127.635 | Mesma execução provável |
| graficos | 02_15_tendencias_inflacao_crescimento.png | outputs/graficos/02_15_tendencias_inflacao_crescimento.png | .png | 04/08/2026 23:57 | 157.329 | Mesma execução provável |
| graficos | 04_desempenho_acumulado_bruto.png | outputs/graficos/04_desempenho_acumulado_bruto.png | .png | 05/08/2026 00:06 | 76.387 | Mesma execução provável |
| graficos | 04_diferenca_carteiras.png | outputs/graficos/04_diferenca_carteiras.png | .png | 05/08/2026 00:06 | 32.123 | Mesma execução provável |
| graficos | 04_drawdown_carteiras.png | outputs/graficos/04_drawdown_carteiras.png | .png | 05/08/2026 00:06 | 118.478 | Mesma execução provável |
| graficos | 05_contribuicao_media_por_regime.png | outputs/graficos/05_contribuicao_media_por_regime.png | .png | 05/08/2026 00:06 | 95.751 | Atual ou posterior às bases centrais |
| graficos | 05_desempenho_bruto_liquido.png | outputs/graficos/05_desempenho_bruto_liquido.png | .png | 05/08/2026 00:06 | 103.687 | Atual ou posterior às bases centrais |
| graficos | 05_drawdown_liquido.png | outputs/graficos/05_drawdown_liquido.png | .png | 05/08/2026 00:06 | 123.010 | Atual ou posterior às bases centrais |
| graficos | 05_impacto_acumulado_custos.png | outputs/graficos/05_impacto_acumulado_custos.png | .png | 05/08/2026 00:06 | 67.555 | Atual ou posterior às bases centrais |
| graficos | 05_indice_final_por_custo.png | outputs/graficos/05_indice_final_por_custo.png | .png | 05/08/2026 00:06 | 89.773 | Atual ou posterior às bases centrais |
| graficos | 05_retorno_liquido_medio_por_regime.png | outputs/graficos/05_retorno_liquido_medio_por_regime.png | .png | 05/08/2026 00:06 | 74.051 | Atual ou posterior às bases centrais |
| graficos | 05_retorno_movel_12m.png | outputs/graficos/05_retorno_movel_12m.png | .png | 05/08/2026 00:06 | 100.662 | Atual ou posterior às bases centrais |
| graficos | 05_retornos_liquidos_anuais.png | outputs/graficos/05_retornos_liquidos_anuais.png | .png | 05/08/2026 00:06 | 42.503 | Atual ou posterior às bases centrais |
| graficos | 05_turnover_mensal.png | outputs/graficos/05_turnover_mensal.png | .png | 05/08/2026 00:06 | 63.613 | Atual ou posterior às bases centrais |
| graficos | 05_vantagem_liquida_por_custo.png | outputs/graficos/05_vantagem_liquida_por_custo.png | .png | 05/08/2026 00:06 | 53.400 | Atual ou posterior às bases centrais |
| graficos | 05_volatilidade_movel_12m.png | outputs/graficos/05_volatilidade_movel_12m.png | .png | 05/08/2026 00:06 | 110.868 | Atual ou posterior às bases centrais |
| graficos | 06_02_mudancas_regime_por_confirmacao.png | outputs/graficos/06_02_mudancas_regime_por_confirmacao.png | .png | 05/08/2026 00:07 | 80.706 | Atual ou posterior às bases centrais |
| graficos | 06_02_series_regimes_suavizados.png | outputs/graficos/06_02_series_regimes_suavizados.png | .png | 05/08/2026 00:07 | 155.885 | Atual ou posterior às bases centrais |
| graficos | 06_03_desempenho_liquido_regimes_suavizados.png | outputs/graficos/06_03_desempenho_liquido_regimes_suavizados.png | .png | 05/08/2026 00:07 | 211.688 | Atual ou posterior às bases centrais |
| graficos | 06_03_diferenca_liquida_vs_benchmark.png | outputs/graficos/06_03_diferenca_liquida_vs_benchmark.png | .png | 05/08/2026 00:07 | 134.460 | Atual ou posterior às bases centrais |
| graficos | 06_03_turnover_regimes_suavizados.png | outputs/graficos/06_03_turnover_regimes_suavizados.png | .png | 05/08/2026 00:07 | 368.294 | Atual ou posterior às bases centrais |
| graficos | 06_04_desempenho_fora_amostra.png | outputs/graficos/06_04_desempenho_fora_amostra.png | .png | 05/08/2026 00:07 | 194.639 | Atual ou posterior às bases centrais |
| graficos | 06_04_diferenca_fora_amostra.png | outputs/graficos/06_04_diferenca_fora_amostra.png | .png | 05/08/2026 00:08 | 124.997 | Atual ou posterior às bases centrais |
| graficos | 06_05_desempenho_teste_pesos_otimizados.png | outputs/graficos/06_05_desempenho_teste_pesos_otimizados.png | .png | 05/08/2026 00:08 | 195.863 | Atual ou posterior às bases centrais |
| graficos | 06_05_diferenca_teste_pesos_otimizados.png | outputs/graficos/06_05_diferenca_teste_pesos_otimizados.png | .png | 05/08/2026 00:08 | 124.997 | Atual ou posterior às bases centrais |
| graficos | 06_05_retorno_volatilidade_treino.png | outputs/graficos/06_05_retorno_volatilidade_treino.png | .png | 05/08/2026 00:08 | 157.017 | Atual ou posterior às bases centrais |
| graficos | 06_06_contribuicao_ativos_teste.png | outputs/graficos/06_06_contribuicao_ativos_teste.png | .png | 05/08/2026 00:08 | 213.065 | Atual ou posterior às bases centrais |
| graficos | 06_06_excesso_retorno_por_regime.png | outputs/graficos/06_06_excesso_retorno_por_regime.png | .png | 05/08/2026 00:08 | 167.720 | Atual ou posterior às bases centrais |
| graficos | 06_06_turnover_por_regime.png | outputs/graficos/06_06_turnover_por_regime.png | .png | 05/08/2026 00:08 | 148.755 | Atual ou posterior às bases centrais |
| graficos | 06_07_comparacao_pesos_por_regime.png | outputs/graficos/06_07_comparacao_pesos_por_regime.png | .png | 05/08/2026 00:08 | 638.032 | Atual ou posterior às bases centrais |
| graficos | 06_07_desempenho_periodo_avaliacao.png | outputs/graficos/06_07_desempenho_periodo_avaliacao.png | .png | 05/08/2026 00:08 | 200.460 | Atual ou posterior às bases centrais |
| graficos | 06_07_diferenca_vs_benchmark_avaliacao.png | outputs/graficos/06_07_diferenca_vs_benchmark_avaliacao.png | .png | 05/08/2026 00:08 | 124.551 | Atual ou posterior às bases centrais |
| graficos | 06_08_cdi_acumulado.png | outputs/graficos/06_08_cdi_acumulado.png | .png | 05/08/2026 00:08 | 52.455 | Atual ou posterior às bases centrais |
| graficos | 06_09_desempenho_avaliacao_cdi.png | outputs/graficos/06_09_desempenho_avaliacao_cdi.png | .png | 05/08/2026 00:08 | 288.574 | Atual ou posterior às bases centrais |
| graficos | 06_09_diferenca_vs_benchmark_5_ativos.png | outputs/graficos/06_09_diferenca_vs_benchmark_5_ativos.png | .png | 05/08/2026 00:08 | 236.660 | Atual ou posterior às bases centrais |
| graficos | 06_09_excesso_rolling_12m_treino.png | outputs/graficos/06_09_excesso_rolling_12m_treino.png | .png | 05/08/2026 00:08 | 213.755 | Atual ou posterior às bases centrais |
| graficos | 06_09_pesos_cdi_por_regime.png | outputs/graficos/06_09_pesos_cdi_por_regime.png | .png | 05/08/2026 00:08 | 153.151 | Atual ou posterior às bases centrais |
| graficos | 06_10_desempenho_comparadores_avaliacao.png | outputs/graficos/06_10_desempenho_comparadores_avaliacao.png | .png | 05/08/2026 00:08 | 358.369 | Atual ou posterior às bases centrais |
| graficos | 06_10_diferenca_modelo_vs_referencias.png | outputs/graficos/06_10_diferenca_modelo_vs_referencias.png | .png | 05/08/2026 00:08 | 328.303 | Atual ou posterior às bases centrais |
| graficos | 06_10_distribuicao_sensibilidade_vs_benchmark.png | outputs/graficos/06_10_distribuicao_sensibilidade_vs_benchmark.png | .png | 05/08/2026 00:08 | 104.667 | Atual ou posterior às bases centrais |
| graficos | 06_10_risco_retorno_avaliacao.png | outputs/graficos/06_10_risco_retorno_avaliacao.png | .png | 05/08/2026 00:08 | 151.770 | Atual ou posterior às bases centrais |
| graficos | 06_10_rolling_12m_avaliacao.png | outputs/graficos/06_10_rolling_12m_avaliacao.png | .png | 05/08/2026 00:08 | 310.568 | Atual ou posterior às bases centrais |
| graficos | 06_11_confirmacao_por_recalibracao.png | outputs/graficos/06_11_confirmacao_por_recalibracao.png | .png | 05/08/2026 00:09 | 91.715 | Atual ou posterior às bases centrais |
| graficos | 06_11_desempenho_walk_forward.png | outputs/graficos/06_11_desempenho_walk_forward.png | .png | 05/08/2026 00:09 | 366.779 | Atual ou posterior às bases centrais |
| graficos | 06_11_diferenca_walk_forward.png | outputs/graficos/06_11_diferenca_walk_forward.png | .png | 05/08/2026 00:09 | 258.925 | Atual ou posterior às bases centrais |
| graficos | 06_11_pesos_cdi_por_recalibracao.png | outputs/graficos/06_11_pesos_cdi_por_recalibracao.png | .png | 05/08/2026 00:09 | 219.508 | Atual ou posterior às bases centrais |
| graficos | 06_11_rolling_12m_walk_forward.png | outputs/graficos/06_11_rolling_12m_walk_forward.png | .png | 05/08/2026 00:09 | 259.101 | Atual ou posterior às bases centrais |
| graficos | 06_12_desempenho_modelos_finais.png | outputs/graficos/06_12_desempenho_modelos_finais.png | .png | 05/08/2026 00:09 | 365.238 | Atual ou posterior às bases centrais |
| graficos | 06_12_drawdown_modelos_finais.png | outputs/graficos/06_12_drawdown_modelos_finais.png | .png | 05/08/2026 00:09 | 343.902 | Atual ou posterior às bases centrais |
| graficos | 06_12_pesos_oficiais_por_regime.png | outputs/graficos/06_12_pesos_oficiais_por_regime.png | .png | 05/08/2026 00:09 | 206.629 | Atual ou posterior às bases centrais |
| graficos | 06_12_risco_retorno_modelos_finais.png | outputs/graficos/06_12_risco_retorno_modelos_finais.png | .png | 05/08/2026 00:09 | 160.585 | Atual ou posterior às bases centrais |
| graficos | 07_02_desempenho_acumulado.png | outputs/graficos/07_02_desempenho_acumulado.png | .png | 05/08/2026 00:10 | 368.181 | Atual ou posterior às bases centrais |
| graficos | 07_02_drawdown_comparativo.png | outputs/graficos/07_02_drawdown_comparativo.png | .png | 05/08/2026 00:10 | 345.910 | Atual ou posterior às bases centrais |
| graficos | 07_02_retornos_anuais.png | outputs/graficos/07_02_retornos_anuais.png | .png | 05/08/2026 00:10 | 142.523 | Atual ou posterior às bases centrais |
| graficos | 07_02_risco_retorno.png | outputs/graficos/07_02_risco_retorno.png | .png | 05/08/2026 00:10 | 166.005 | Atual ou posterior às bases centrais |
| modelo_final | alocacoes_iniciais_automaticas.json | outputs/modelo_final/alocacoes_iniciais_automaticas.json | .json | 05/08/2026 00:06 | 2.566 | Mesma execução provável |
| modelo_final | manifesto_arquivos.csv | outputs/modelo_final/manifesto_arquivos.csv | .csv | 05/08/2026 00:09 | 3.483 | Atual ou posterior às bases centrais |
| modelo_final | metricas_modelo_oficial.json | outputs/modelo_final/metricas_modelo_oficial.json | .json | 05/08/2026 00:09 | 643 | Atual ou posterior às bases centrais |
| modelo_final | modelo_oficial.json | outputs/modelo_final/modelo_oficial.json | .json | 05/08/2026 00:09 | 4.436 | Atual ou posterior às bases centrais |
| tabelas | 01_status_blocos_bcb.csv | outputs/tabelas/01_status_blocos_bcb.csv | .csv | 04/08/2026 23:57 | 1.607 | Mesma execução provável |
| tabelas | 01_status_coleta_macro.csv | outputs/tabelas/01_status_coleta_macro.csv | .csv | 04/08/2026 23:57 | 480 | Mesma execução provável |
| tabelas | 01_validacao_ativos.csv | outputs/tabelas/01_validacao_ativos.csv | .csv | 04/08/2026 23:57 | 5.506 | Mesma execução provável |
| tabelas | 01_validacao_series_macro.csv | outputs/tabelas/01_validacao_series_macro.csv | .csv | 04/08/2026 23:57 | 617 | Mesma execução provável |
| tabelas | 02_01_ativos_selecionados_utilizados.csv | outputs/tabelas/02_01_ativos_selecionados_utilizados.csv | .csv | 04/08/2026 23:57 | 2.099 | Mesma execução provável |
| tabelas | 02_04_pontos_atencao_qualidade.csv | outputs/tabelas/02_04_pontos_atencao_qualidade.csv | .csv | 04/08/2026 23:57 | 337 | Mesma execução provável |
| tabelas | 02_04_qualidade_ativos.csv | outputs/tabelas/02_04_qualidade_ativos.csv | .csv | 04/08/2026 23:57 | 1.090 | Mesma execução provável |
| tabelas | 02_04_qualidade_series_macro.csv | outputs/tabelas/02_04_qualidade_series_macro.csv | .csv | 04/08/2026 23:57 | 391 | Mesma execução provável |
| tabelas | 02_05_periodos_disponiveis_ativos.csv | outputs/tabelas/02_05_periodos_disponiveis_ativos.csv | .csv | 04/08/2026 23:57 | 550 | Mesma execução provável |
| tabelas | 02_05_precos_periodo_comum.csv | outputs/tabelas/02_05_precos_periodo_comum.csv | .csv | 04/08/2026 23:57 | 322.338 | Mesma execução provável |
| tabelas | 02_06_resumo_desempenho_ativos.csv | outputs/tabelas/02_06_resumo_desempenho_ativos.csv | .csv | 04/08/2026 23:57 | 2.331 | Mesma execução provável |
| tabelas | 02_06_resumo_desempenho_ativos_formatado.csv | outputs/tabelas/02_06_resumo_desempenho_ativos_formatado.csv | .csv | 04/08/2026 23:57 | 1.029 | Mesma execução provável |
| tabelas | 02_07_resumo_dados_macro_mensais.csv | outputs/tabelas/02_07_resumo_dados_macro_mensais.csv | .csv | 04/08/2026 23:57 | 1.275 | Mesma execução provável |
| tabelas | 02_08_resumo_precos_normalizados.csv | outputs/tabelas/02_08_resumo_precos_normalizados.csv | .csv | 04/08/2026 23:57 | 1.512 | Mesma execução provável |
| tabelas | 02_09_resumo_retorno_acumulado.csv | outputs/tabelas/02_09_resumo_retorno_acumulado.csv | .csv | 04/08/2026 23:57 | 856 | Mesma execução provável |
| tabelas | 02_10_resumo_volatilidade_movel.csv | outputs/tabelas/02_10_resumo_volatilidade_movel.csv | .csv | 04/08/2026 23:57 | 1.671 | Mesma execução provável |
| tabelas | 02_11_resumo_drawdown_ativos.csv | outputs/tabelas/02_11_resumo_drawdown_ativos.csv | .csv | 04/08/2026 23:57 | 1.982 | Mesma execução provável |
| tabelas | 02_12_pares_correlacao_retornos.csv | outputs/tabelas/02_12_pares_correlacao_retornos.csv | .csv | 04/08/2026 23:57 | 4.269 | Mesma execução provável |
| tabelas | 02_12_resumo_correlacao_retornos.csv | outputs/tabelas/02_12_resumo_correlacao_retornos.csv | .csv | 04/08/2026 23:57 | 242 | Mesma execução provável |
| tabelas | 02_16_conferencia_final_arquivos.csv | outputs/tabelas/02_16_conferencia_final_arquivos.csv | .csv | 04/08/2026 23:57 | 895 | Mesma execução provável |
| tabelas | 02_diagnostico_imab11_por_ano.csv | outputs/tabelas/02_diagnostico_imab11_por_ano.csv | .csv | 04/08/2026 23:57 | 534 | Mesma execução provável |
| tabelas | 02_diagnostico_imab11_ultimos_registros.csv | outputs/tabelas/02_diagnostico_imab11_ultimos_registros.csv | .csv | 04/08/2026 23:57 | 1.648 | Mesma execução provável |
| tabelas | 02_segmento_commodities_correlacao.csv | outputs/tabelas/02_segmento_commodities_correlacao.csv | .csv | 04/08/2026 23:57 | 176 | Mesma execução provável |
| tabelas | 02_segmento_commodities_desempenho.csv | outputs/tabelas/02_segmento_commodities_desempenho.csv | .csv | 04/08/2026 23:57 | 700 | Mesma execução provável |
| tabelas | 02_segmento_commodities_drawdown.csv | outputs/tabelas/02_segmento_commodities_drawdown.csv | .csv | 04/08/2026 23:57 | 634 | Mesma execução provável |
| tabelas | 02_segmento_commodities_pares_correlacao.csv | outputs/tabelas/02_segmento_commodities_pares_correlacao.csv | .csv | 04/08/2026 23:57 | 242 | Mesma execução provável |
| tabelas | 02_segmento_commodities_precos_normalizados.csv | outputs/tabelas/02_segmento_commodities_precos_normalizados.csv | .csv | 04/08/2026 23:57 | 465 | Mesma execução provável |
| tabelas | 02_segmento_commodities_resumo_correlacao.csv | outputs/tabelas/02_segmento_commodities_resumo_correlacao.csv | .csv | 04/08/2026 23:57 | 242 | Mesma execução provável |
| tabelas | 02_segmento_commodities_retorno_acumulado.csv | outputs/tabelas/02_segmento_commodities_retorno_acumulado.csv | .csv | 04/08/2026 23:57 | 254 | Mesma execução provável |
| tabelas | 02_segmento_commodities_volatilidade_movel.csv | outputs/tabelas/02_segmento_commodities_volatilidade_movel.csv | .csv | 04/08/2026 23:57 | 560 | Mesma execução provável |
| tabelas | 02_segmento_moedas_correlacao.csv | outputs/tabelas/02_segmento_moedas_correlacao.csv | .csv | 04/08/2026 23:57 | 194 | Mesma execução provável |
| tabelas | 02_segmento_moedas_desempenho.csv | outputs/tabelas/02_segmento_moedas_desempenho.csv | .csv | 04/08/2026 23:57 | 720 | Mesma execução provável |
| tabelas | 02_segmento_moedas_drawdown.csv | outputs/tabelas/02_segmento_moedas_drawdown.csv | .csv | 04/08/2026 23:57 | 647 | Mesma execução provável |
| tabelas | 02_segmento_moedas_pares_correlacao.csv | outputs/tabelas/02_segmento_moedas_pares_correlacao.csv | .csv | 04/08/2026 23:57 | 260 | Mesma execução provável |
| tabelas | 02_segmento_moedas_precos_normalizados.csv | outputs/tabelas/02_segmento_moedas_precos_normalizados.csv | .csv | 04/08/2026 23:57 | 456 | Mesma execução provável |
| tabelas | 02_segmento_moedas_resumo_correlacao.csv | outputs/tabelas/02_segmento_moedas_resumo_correlacao.csv | .csv | 04/08/2026 23:57 | 235 | Mesma execução provável |
| tabelas | 02_segmento_moedas_retorno_acumulado.csv | outputs/tabelas/02_segmento_moedas_retorno_acumulado.csv | .csv | 04/08/2026 23:57 | 269 | Mesma execução provável |
| tabelas | 02_segmento_moedas_volatilidade_movel.csv | outputs/tabelas/02_segmento_moedas_volatilidade_movel.csv | .csv | 04/08/2026 23:57 | 575 | Mesma execução provável |
| tabelas | 02_segmento_renda_fixa_correlacao.csv | outputs/tabelas/02_segmento_renda_fixa_correlacao.csv | .csv | 04/08/2026 23:57 | 204 | Mesma execução provável |
| tabelas | 02_segmento_renda_fixa_desempenho.csv | outputs/tabelas/02_segmento_renda_fixa_desempenho.csv | .csv | 04/08/2026 23:57 | 716 | Mesma execução provável |
| tabelas | 02_segmento_renda_fixa_drawdown.csv | outputs/tabelas/02_segmento_renda_fixa_drawdown.csv | .csv | 04/08/2026 23:57 | 650 | Mesma execução provável |
| tabelas | 02_segmento_renda_fixa_pares_correlacao.csv | outputs/tabelas/02_segmento_renda_fixa_pares_correlacao.csv | .csv | 04/08/2026 23:57 | 270 | Mesma execução provável |
| tabelas | 02_segmento_renda_fixa_precos_normalizados.csv | outputs/tabelas/02_segmento_renda_fixa_precos_normalizados.csv | .csv | 04/08/2026 23:57 | 482 | Mesma execução provável |
| tabelas | 02_segmento_renda_fixa_resumo_correlacao.csv | outputs/tabelas/02_segmento_renda_fixa_resumo_correlacao.csv | .csv | 04/08/2026 23:57 | 237 | Mesma execução provável |
| tabelas | 02_segmento_renda_fixa_retorno_acumulado.csv | outputs/tabelas/02_segmento_renda_fixa_retorno_acumulado.csv | .csv | 04/08/2026 23:57 | 268 | Mesma execução provável |
| tabelas | 02_segmento_renda_fixa_volatilidade_movel.csv | outputs/tabelas/02_segmento_renda_fixa_volatilidade_movel.csv | .csv | 04/08/2026 23:57 | 518 | Mesma execução provável |
| tabelas | 02_segmento_renda_variavel_correlacao.csv | outputs/tabelas/02_segmento_renda_variavel_correlacao.csv | .csv | 04/08/2026 23:57 | 200 | Mesma execução provável |
| tabelas | 02_segmento_renda_variavel_desempenho.csv | outputs/tabelas/02_segmento_renda_variavel_desempenho.csv | .csv | 04/08/2026 23:57 | 714 | Mesma execução provável |
| tabelas | 02_segmento_renda_variavel_drawdown.csv | outputs/tabelas/02_segmento_renda_variavel_drawdown.csv | .csv | 04/08/2026 23:57 | 651 | Mesma execução provável |
| tabelas | 02_segmento_renda_variavel_pares_correlacao.csv | outputs/tabelas/02_segmento_renda_variavel_pares_correlacao.csv | .csv | 04/08/2026 23:57 | 266 | Mesma execução provável |
| tabelas | 02_segmento_renda_variavel_precos_normalizados.csv | outputs/tabelas/02_segmento_renda_variavel_precos_normalizados.csv | .csv | 04/08/2026 23:57 | 484 | Mesma execução provável |
| tabelas | 02_segmento_renda_variavel_resumo_correlacao.csv | outputs/tabelas/02_segmento_renda_variavel_resumo_correlacao.csv | .csv | 04/08/2026 23:57 | 235 | Mesma execução provável |
| tabelas | 02_segmento_renda_variavel_retorno_acumulado.csv | outputs/tabelas/02_segmento_renda_variavel_retorno_acumulado.csv | .csv | 04/08/2026 23:57 | 266 | Mesma execução provável |
| tabelas | 02_segmento_renda_variavel_volatilidade_movel.csv | outputs/tabelas/02_segmento_renda_variavel_volatilidade_movel.csv | .csv | 04/08/2026 23:57 | 582 | Mesma execução provável |
| tabelas | 03_validacoes_regimes_macroeconomicos.csv | outputs/tabelas/03_validacoes_regimes_macroeconomicos.csv | .csv | 04/08/2026 23:58 | 708 | Mesma execução provável |
| tabelas | 04_ativos_aprovados_utilizados.csv | outputs/tabelas/04_ativos_aprovados_utilizados.csv | .csv | 05/08/2026 00:06 | 2.657 | Mesma execução provável |
| tabelas | 04_metricas_portfolio.csv | outputs/tabelas/04_metricas_portfolio.csv | .csv | 05/08/2026 00:06 | 545 | Mesma execução provável |
| tabelas | 04_pesos_por_regime.csv | outputs/tabelas/04_pesos_por_regime.csv | .csv | 05/08/2026 00:06 | 1.257 | Mesma execução provável |
| tabelas | 04_validacoes_alocacao.csv | outputs/tabelas/04_validacoes_alocacao.csv | .csv | 05/08/2026 00:06 | 647 | Mesma execução provável |
| tabelas | 05_configuracoes_backtest.csv | outputs/tabelas/05_configuracoes_backtest.csv | .csv | 05/08/2026 00:06 | 662 | Atual ou posterior às bases centrais |
| tabelas | 05_contribuicao_media_por_regime.csv | outputs/tabelas/05_contribuicao_media_por_regime.csv | .csv | 05/08/2026 00:06 | 1.958 | Atual ou posterior às bases centrais |
| tabelas | 05_custo_break_even.csv | outputs/tabelas/05_custo_break_even.csv | .csv | 05/08/2026 00:06 | 282 | Atual ou posterior às bases centrais |
| tabelas | 05_desempenho_por_regime.csv | outputs/tabelas/05_desempenho_por_regime.csv | .csv | 05/08/2026 00:06 | 1.704 | Atual ou posterior às bases centrais |
| tabelas | 05_diagnostico_estrategia.csv | outputs/tabelas/05_diagnostico_estrategia.csv | .csv | 05/08/2026 00:06 | 367 | Atual ou posterior às bases centrais |
| tabelas | 05_metricas_backtest.csv | outputs/tabelas/05_metricas_backtest.csv | .csv | 05/08/2026 00:06 | 1.722 | Atual ou posterior às bases centrais |
| tabelas | 05_metricas_backtest_formatadas.csv | outputs/tabelas/05_metricas_backtest_formatadas.csv | .csv | 05/08/2026 00:06 | 876 | Atual ou posterior às bases centrais |
| tabelas | 05_metricas_moveis_12m.csv | outputs/tabelas/05_metricas_moveis_12m.csv | .csv | 05/08/2026 00:06 | 10.816 | Atual ou posterior às bases centrais |
| tabelas | 05_resultados_anuais.csv | outputs/tabelas/05_resultados_anuais.csv | .csv | 05/08/2026 00:06 | 920 | Atual ou posterior às bases centrais |
| tabelas | 05_resumo_final_backtest.csv | outputs/tabelas/05_resumo_final_backtest.csv | .csv | 05/08/2026 00:06 | 1.002 | Atual ou posterior às bases centrais |
| tabelas | 05_resumo_turnover_custos.csv | outputs/tabelas/05_resumo_turnover_custos.csv | .csv | 05/08/2026 00:06 | 455 | Atual ou posterior às bases centrais |
| tabelas | 05_sensibilidade_custos.csv | outputs/tabelas/05_sensibilidade_custos.csv | .csv | 05/08/2026 00:06 | 1.114 | Atual ou posterior às bases centrais |
| tabelas | 05_turnover_custos_mensal.csv | outputs/tabelas/05_turnover_custos_mensal.csv | .csv | 05/08/2026 00:06 | 21.617 | Atual ou posterior às bases centrais |
| tabelas | 05_validacao_final_backtest.csv | outputs/tabelas/05_validacao_final_backtest.csv | .csv | 05/08/2026 00:06 | 785 | Atual ou posterior às bases centrais |
| tabelas | 06_01_inventario_bases.csv | outputs/tabelas/06_01_inventario_bases.csv | .csv | 05/08/2026 00:07 | 597 | Atual ou posterior às bases centrais |
| tabelas | 06_01_resumo_modelo_original.csv | outputs/tabelas/06_01_resumo_modelo_original.csv | .csv | 05/08/2026 00:07 | 562 | Atual ou posterior às bases centrais |
| tabelas | 06_01_status_ativos_adicionais.csv | outputs/tabelas/06_01_status_ativos_adicionais.csv | .csv | 05/08/2026 00:07 | 101 | Atual ou posterior às bases centrais |
| tabelas | 06_02_regimes_suavizados.csv | outputs/tabelas/06_02_regimes_suavizados.csv | .csv | 05/08/2026 00:07 | 8.380 | Atual ou posterior às bases centrais |
| tabelas | 06_02_resumo_suavizacao_regimes.csv | outputs/tabelas/06_02_resumo_suavizacao_regimes.csv | .csv | 05/08/2026 00:07 | 358 | Atual ou posterior às bases centrais |
| tabelas | 06_02_resumo_suavizacao_regimes_formatado.csv | outputs/tabelas/06_02_resumo_suavizacao_regimes_formatado.csv | .csv | 05/08/2026 00:07 | 305 | Atual ou posterior às bases centrais |
| tabelas | 06_03_comparacao_regimes_suavizados.csv | outputs/tabelas/06_03_comparacao_regimes_suavizados.csv | .csv | 05/08/2026 00:07 | 1.668 | Atual ou posterior às bases centrais |
| tabelas | 06_03_comparacao_regimes_suavizados_formatada.csv | outputs/tabelas/06_03_comparacao_regimes_suavizados_formatada.csv | .csv | 05/08/2026 00:07 | 920 | Atual ou posterior às bases centrais |
| tabelas | 06_03_pesos_originais_por_regime.csv | outputs/tabelas/06_03_pesos_originais_por_regime.csv | .csv | 05/08/2026 00:07 | 1.176 | Atual ou posterior às bases centrais |
| tabelas | 06_03_series_mensais_regimes_suavizados.csv | outputs/tabelas/06_03_series_mensais_regimes_suavizados.csv | .csv | 05/08/2026 00:07 | 244.015 | Atual ou posterior às bases centrais |
| tabelas | 06_04_selecao_cenario_treino.csv | outputs/tabelas/06_04_selecao_cenario_treino.csv | .csv | 05/08/2026 00:07 | 679 | Atual ou posterior às bases centrais |
| tabelas | 06_04_series_fora_amostra.csv | outputs/tabelas/06_04_series_fora_amostra.csv | .csv | 05/08/2026 00:07 | 2.927 | Atual ou posterior às bases centrais |
| tabelas | 06_04_validacao_treino_teste.csv | outputs/tabelas/06_04_validacao_treino_teste.csv | .csv | 05/08/2026 00:07 | 2.865 | Atual ou posterior às bases centrais |
| tabelas | 06_04_validacao_treino_teste_formatada.csv | outputs/tabelas/06_04_validacao_treino_teste_formatada.csv | .csv | 05/08/2026 00:07 | 1.559 | Atual ou posterior às bases centrais |
| tabelas | 06_05_grade_otimizacao_pesos.csv | outputs/tabelas/06_05_grade_otimizacao_pesos.csv | .csv | 05/08/2026 00:08 | 11.035 | Atual ou posterior às bases centrais |
| tabelas | 06_05_grade_otimizacao_pesos_formatada.csv | outputs/tabelas/06_05_grade_otimizacao_pesos_formatada.csv | .csv | 05/08/2026 00:08 | 5.734 | Atual ou posterior às bases centrais |
| tabelas | 06_05_parametros_selecionados.csv | outputs/tabelas/06_05_parametros_selecionados.csv | .csv | 05/08/2026 00:08 | 1.072 | Atual ou posterior às bases centrais |
| tabelas | 06_05_pesos_selecionados_por_regime.csv | outputs/tabelas/06_05_pesos_selecionados_por_regime.csv | .csv | 05/08/2026 00:08 | 1.324 | Atual ou posterior às bases centrais |
| tabelas | 06_05_series_teste_parametros_selecionados.csv | outputs/tabelas/06_05_series_teste_parametros_selecionados.csv | .csv | 05/08/2026 00:08 | 13.810 | Atual ou posterior às bases centrais |
| tabelas | 06_06_contribuicao_ativos_por_regime.csv | outputs/tabelas/06_06_contribuicao_ativos_por_regime.csv | .csv | 05/08/2026 00:08 | 22.519 | Atual ou posterior às bases centrais |
| tabelas | 06_06_contribuicao_ativos_por_regime_formatado.csv | outputs/tabelas/06_06_contribuicao_ativos_por_regime_formatado.csv | .csv | 05/08/2026 00:08 | 11.506 | Atual ou posterior às bases centrais |
| tabelas | 06_06_diagnostico_por_regime.csv | outputs/tabelas/06_06_diagnostico_por_regime.csv | .csv | 05/08/2026 00:08 | 3.472 | Atual ou posterior às bases centrais |
| tabelas | 06_06_diagnostico_por_regime_formatado.csv | outputs/tabelas/06_06_diagnostico_por_regime_formatado.csv | .csv | 05/08/2026 00:08 | 1.953 | Atual ou posterior às bases centrais |
| tabelas | 06_06_regimes_problematicos_teste.csv | outputs/tabelas/06_06_regimes_problematicos_teste.csv | .csv | 05/08/2026 00:08 | 531 | Atual ou posterior às bases centrais |
| tabelas | 06_06_resumo_diagnostico.csv | outputs/tabelas/06_06_resumo_diagnostico.csv | .csv | 05/08/2026 00:08 | 558 | Atual ou posterior às bases centrais |
| tabelas | 06_06_series_mensais_diagnostico.csv | outputs/tabelas/06_06_series_mensais_diagnostico.csv | .csv | 05/08/2026 00:08 | 130.736 | Atual ou posterior às bases centrais |
| tabelas | 06_07_betas_selecionados_por_regime.csv | outputs/tabelas/06_07_betas_selecionados_por_regime.csv | .csv | 05/08/2026 00:08 | 835 | Atual ou posterior às bases centrais |
| tabelas | 06_07_grade_ajustes_por_regime.csv | outputs/tabelas/06_07_grade_ajustes_por_regime.csv | .csv | 05/08/2026 00:08 | 6.508 | Atual ou posterior às bases centrais |
| tabelas | 06_07_grade_ajustes_por_regime_formatada.csv | outputs/tabelas/06_07_grade_ajustes_por_regime_formatada.csv | .csv | 05/08/2026 00:08 | 3.467 | Atual ou posterior às bases centrais |
| tabelas | 06_07_metricas_comparativas.csv | outputs/tabelas/06_07_metricas_comparativas.csv | .csv | 05/08/2026 00:08 | 1.821 | Atual ou posterior às bases centrais |
| tabelas | 06_07_metricas_comparativas_formatadas.csv | outputs/tabelas/06_07_metricas_comparativas_formatadas.csv | .csv | 05/08/2026 00:08 | 982 | Atual ou posterior às bases centrais |
| tabelas | 06_07_pesos_otimizados_por_regime.csv | outputs/tabelas/06_07_pesos_otimizados_por_regime.csv | .csv | 05/08/2026 00:08 | 3.178 | Atual ou posterior às bases centrais |
| tabelas | 06_07_resumo_ajuste_regimes.csv | outputs/tabelas/06_07_resumo_ajuste_regimes.csv | .csv | 05/08/2026 00:08 | 801 | Atual ou posterior às bases centrais |
| tabelas | 06_07_series_mensais_otimizadas.csv | outputs/tabelas/06_07_series_mensais_otimizadas.csv | .csv | 05/08/2026 00:08 | 39.888 | Atual ou posterior às bases centrais |
| tabelas | 06_08_arquivos_proxy_removidos.csv | outputs/tabelas/06_08_arquivos_proxy_removidos.csv | .csv | 05/08/2026 00:08 | 434 | Atual ou posterior às bases centrais |
| tabelas | 06_08_resumo_renda_fixa.csv | outputs/tabelas/06_08_resumo_renda_fixa.csv | .csv | 05/08/2026 00:08 | 257 | Atual ou posterior às bases centrais |
| tabelas | 06_08_status_fontes_renda_fixa.csv | outputs/tabelas/06_08_status_fontes_renda_fixa.csv | .csv | 05/08/2026 00:08 | 320 | Atual ou posterior às bases centrais |
| tabelas | 06_08_validacao_renda_fixa.csv | outputs/tabelas/06_08_validacao_renda_fixa.csv | .csv | 05/08/2026 00:08 | 326 | Atual ou posterior às bases centrais |
| tabelas | 06_09_grade_otimizacao_cdi.csv | outputs/tabelas/06_09_grade_otimizacao_cdi.csv | .csv | 05/08/2026 00:08 | 1.736.584 | Atual ou posterior às bases centrais |
| tabelas | 06_09_grade_otimizacao_cdi_formatada.csv | outputs/tabelas/06_09_grade_otimizacao_cdi_formatada.csv | .csv | 05/08/2026 00:08 | 906.199 | Atual ou posterior às bases centrais |
| tabelas | 06_09_metricas_treino_avaliacao.csv | outputs/tabelas/06_09_metricas_treino_avaliacao.csv | .csv | 05/08/2026 00:08 | 2.372 | Atual ou posterior às bases centrais |
| tabelas | 06_09_metricas_treino_avaliacao_formatadas.csv | outputs/tabelas/06_09_metricas_treino_avaliacao_formatadas.csv | .csv | 05/08/2026 00:08 | 1.272 | Atual ou posterior às bases centrais |
| tabelas | 06_09_parametros_selecionados_cdi.csv | outputs/tabelas/06_09_parametros_selecionados_cdi.csv | .csv | 05/08/2026 00:08 | 828 | Atual ou posterior às bases centrais |
| tabelas | 06_09_pesos_selecionados_5_ativos.csv | outputs/tabelas/06_09_pesos_selecionados_5_ativos.csv | .csv | 05/08/2026 00:08 | 1.061 | Atual ou posterior às bases centrais |

---

## 4. Universo de investimento

| ticker | segmento | classe | status |
| --- | --- | --- | --- |
| GC=F | Commodities | COMMODITY_OURO | APROVADO |
| NG=F | Commodities | COMMODITY_GAS_NATURAL | APROVADO |
| ZC=F | Commodities | COMMODITY_MILHO | APROVADO |
| EURBRL=X | Moedas | MOEDA_EURO | APROVADO_COM_RESSALVAS |
| JPYBRL=X | Moedas | MOEDA_IENE | APROVADO_COM_RESSALVAS |
| USDBRL=X | Moedas | MOEDA_DOLAR | APROVADO_COM_RESSALVAS |
| B5MB11.SA | Renda Fixa | RENDA_FIXA_INFLACAO_IMAB5 | APROVADO_COM_RESSALVAS |
| IB5M11.SA | Renda Fixa | RENDA_FIXA_INFLACAO_IMAB5_MAIS | APROVADO_COM_RESSALVAS |
| IMAB11.SA | Renda Fixa | RENDA_FIXA_INFLACAO_IMAB | APROVADO_COM_RESSALVAS |
| BOVV11.SA | Renda Variável | RENDA_VARIAVEL_BRASIL_IBOVESPA | APROVADO |
| FIND11.SA | Renda Variável | RENDA_VARIAVEL_FINANCEIRO | APROVADO |
| MATB11.SA | Renda Variável | RENDA_VARIAVEL_MATERIAIS | APROVADO |

### Distribuição por segmento

| segmento | quantidade |
| --- | --- |
| Commodities | 3 |
| Moedas | 3 |
| Renda Fixa | 3 |
| Renda Variável | 3 |

---

## 5. Indicadores e regimes macroeconômicos

| indicador | coluna | primeiro | último | mínimo | máximo | observações |
| --- | --- | --- | --- | --- | --- | --- |
| IPCA mensal | IPCA_MENSAL_PCT | 0,2100 | 0,1600 | -0,6800 | 1,6200 | 78 |
| IPCA em 12 meses | IPCA_12M_PCT | 4,1917 | 4,6413 | 1,8775 | 12,1315 | 78 |
| Tendência da inflação | IPCA_VARIACAO_3M_PP | 1,6566 | 0,4985 | -4,7181 | 2,8606 | 78 |
| IBC-Br | IBC_BR | 92,4520 | 109,5299 | 83,9582 | 117,8089 | 77 |
| IBC-Br dessazonalizado | IBC_BR_DESSAZONALIZADO | 97,6733 | 111,0359 | 83,0387 | 111,0359 | 77 |
| Tendência da atividade | IBC_BR_TENDENCIA_3M_PCT | 0,4709 | 0,7187 | -11,3480 | 8,8239 | 77 |
| CDI mensal | CDI_MENSAL_PCT | 0,3766 | 0,0525 | 0,0525 | 1,2757 | 80 |

```text
Atividade alta + inflação em queda = Expansão desinflacionária
Atividade alta + inflação em alta = Expansão inflacionária
Atividade em queda + inflação em alta = Estagflação
Atividade em queda + inflação em queda = Recessão desinflacionária
```

### Desempenho consolidado por regime

| regime | nome_regime | meses | frequencia | retorno_estrategia | volatilidade_estrategia | drawdown_estrategia | retorno_benchmark | volatilidade_benchmark | drawdown_benchmark | retorno_cdi | volatilidade_cdi | drawdown_cdi | excesso_vs_benchmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 34 | 44,16% | 6,09% | 7,47% | -8,03% | 6,09% | 7,47% | -8,03% | 39,22% | 0,57% | 0,00% | 0,00% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | 30 | 38,96% | 27,46% | 9,34% | -6,36% | 27,46% | 9,34% | -6,36% | 23,16% | 1,35% | 0,00% | 0,00% |
| ESTAGFLACAO | Estagflação | 5 | 6,49% | 0,69% | 3,29% | -1,42% | 0,69% | 3,29% | -1,42% | 1,82% | 0,26% | 0,00% | 0,00% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | 8 | 10,39% | 26,49% | 5,72% | -0,55% | 26,49% | 5,72% | -0,55% | 4,59% | 1,79% | 0,00% | 0,00% |

---

## 6. Desenvolvimento e calibração

**Intervalo oficial:** 01/01/2020 a 31/12/2023  
**Função:** Construção, testes e escolha dos parâmetros  
**Ajusta parâmetros:** Sim  
**Altera regras:** Sim  

> A cobertura mensal disponível contempla todo o intervalo oficial.

### Métricas da carteira

| serie | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Estratégia | 48 | 34,22% | 7,64% | 8,51% | -0,00 | -8,32% | 58,33% | 5,15% | -6,36% |
| Benchmark estático | 48 | 34,22% | 7,64% | 8,51% | -0,00 | -8,32% | 58,33% | 5,15% | -6,36% |
| CDI | 48 | 36,32% | 8,05% | 1,33% | 5,85 | 0,00% | 100,00% | 1,17% | 0,13% |

### Resultado por regime dentro do período

| regime | nome_regime | meses | frequencia | retorno_estrategia | volatilidade_estrategia | drawdown_estrategia | retorno_benchmark | volatilidade_benchmark | drawdown_benchmark | retorno_cdi | volatilidade_cdi | drawdown_cdi | excesso_vs_benchmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 21 | 43,75% | 1,20% | 5,56% | -8,03% | 1,20% | 5,56% | -8,03% | 22,61% | 0,61% | 0,00% | 0,00% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | 17 | 35,42% | 13,91% | 11,44% | -6,36% | 13,91% | 11,44% | -6,36% | 8,16% | 1,23% | 0,00% | 0,00% |
| ESTAGFLACAO | Estagflação | 5 | 10,42% | 0,69% | 3,29% | -1,42% | 0,69% | 3,29% | -1,42% | 1,82% | 0,26% | 0,00% | 0,00% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | 5 | 10,42% | 15,64% | 7,39% | -0,55% | 15,64% | 7,39% | -0,55% | 0,96% | 0,12% | 0,00% | 0,00% |

### Segmentos

| segmento | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commodities | 48 | 66,30% | 13,56% | 25,22% | 0,31 | -32,72% | 54,17% | 18,91% | -12,27% |
| Moedas | 48 | 10,33% | 2,49% | 14,42% | -0,29 | -27,20% | 52,08% | 16,47% | -8,64% |
| Renda Fixa | 48 | 6,42% | 1,57% | 8,94% | -0,65 | -12,08% | 56,25% | 6,80% | -11,44% |
| Renda Variável | 48 | 29,19% | 6,61% | 26,03% | 0,08 | -33,79% | 56,25% | 16,16% | -27,66% |

### Ativos

| ticker | segmento | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MATB11.SA | Renda Variável | 48 | 67,30% | 13,73% | 28,02% | 0,32 | -32,82% | 58,33% | 14,45% | -19,77% |
| GC=F | Commodities | 48 | 36,04% | 8,00% | 14,22% | 0,06 | -16,86% | 52,08% | 9,47% | -6,92% |
| ZC=F | Commodities | 48 | 21,14% | 4,91% | 31,31% | 0,06 | -43,66% | 58,33% | 31,15% | -24,03% |
| NG=F | Commodities | 48 | 20,50% | 4,77% | 71,09% | 0,30 | -75,72% | 52,08% | 51,71% | -41,13% |
| USDBRL=X | Moedas | 48 | 20,16% | 4,70% | 15,54% | -0,13 | -18,25% | 52,08% | 15,78% | -7,54% |
| IB5M11.SA | Renda Fixa | 48 | 19,48% | 4,55% | 11,70% | -0,23 | -12,30% | 54,17% | 8,08% | -12,30% |
| EURBRL=X | Moedas | 48 | 19,36% | 4,52% | 13,96% | -0,17 | -24,33% | 56,25% | 16,11% | -7,67% |
| BOVV11.SA | Renda Variável | 48 | 14,59% | 3,46% | 26,59% | -0,02 | -35,99% | 56,25% | 16,11% | -30,11% |
| IMAB11.SA | Renda Fixa | 48 | 3,57% | 0,88% | 6,49% | -0,99 | -8,24% | 33,33% | 5,04% | -7,51% |
| FIND11.SA | Renda Variável | 48 | 2,14% | 0,53% | 32,02% | -0,06 | -36,72% | 50,00% | 17,93% | -33,12% |
| B5MB11.SA | Renda Fixa | 48 | -3,77% | -0,96% | 11,01% | -0,73 | -17,04% | 25,00% | 7,27% | -14,52% |
| JPYBRL=X | Moedas | 48 | -7,63% | -1,97% | 15,94% | -0,52 | -39,65% | 54,17% | 17,51% | -11,87% |

### 5 melhores meses

| data | regime | nome_regime | retorno_estrategia | retorno_benchmark | retorno_cdi |
| --- | --- | --- | --- | --- | --- |
| 31/08/2020 | Recessão desinflacionária | Recessão desinflacionária | 5,15% | 5,15% | 0,16% |
| 30/04/2020 | Expansão inflacionária | Expansão inflacionária | 4,98% | 4,98% | 0,28% |
| 31/10/2020 | Expansão inflacionária | Expansão inflacionária | 4,44% | 4,44% | 0,16% |
| 31/12/2020 | Expansão inflacionária | Expansão inflacionária | 4,04% | 4,04% | 0,16% |
| 30/04/2021 | Expansão inflacionária | Expansão inflacionária | 4,00% | 4,00% | 0,21% |

### 5 piores meses

| data | regime | nome_regime | retorno_estrategia | retorno_benchmark | retorno_cdi |
| --- | --- | --- | --- | --- | --- |
| 31/03/2020 | Expansão inflacionária | Expansão inflacionária | -6,36% | -6,36% | 0,34% |
| 30/06/2022 | Expansão inflacionária | Expansão inflacionária | -5,09% | -5,09% | 1,02% |
| 28/02/2023 | Expansão desinflacionária | Expansão desinflacionária | -2,61% | -2,61% | 0,92% |
| 31/01/2023 | Expansão desinflacionária | Expansão desinflacionária | -2,38% | -2,38% | 1,12% |
| 29/02/2020 | Expansão inflacionária | Expansão inflacionária | -2,09% | -2,09% | 0,29% |

![Desempenho — Desenvolvimento e calibração](graficos_periodos/01_desenvolvimento_calibracao.png)

**Interpretação:** este bloco foi usado para construir e calibrar o modelo. Resultados fortes aqui não devem ser tratados isoladamente como evidência fora da amostra.

---

## 7. Validação

**Intervalo oficial:** 01/01/2024 a 31/12/2025  
**Função:** Avaliação das regras e parâmetros congelados  
**Ajusta parâmetros:** Não  
**Altera regras:** Não  

> A cobertura mensal disponível contempla todo o intervalo oficial.

### Métricas da carteira

| serie | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Estratégia | 24 | 22,15% | 10,52% | 6,47% | -0,26 | -2,98% | 70,83% | 3,51% | -3,64% |
| Benchmark estático | 24 | 22,15% | 10,52% | 6,47% | -0,26 | -2,98% | 70,83% | 3,51% | -3,64% |
| CDI | 24 | 26,76% | 12,59% | 0,55% | 21,82 | 0,00% | 100,00% | 1,28% | 0,79% |

### Resultado por regime dentro do período

| regime | nome_regime | meses | frequencia | retorno_estrategia | volatilidade_estrategia | drawdown_estrategia | retorno_benchmark | volatilidade_benchmark | drawdown_benchmark | retorno_cdi | volatilidade_cdi | drawdown_cdi | excesso_vs_benchmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 8 | 33,33% | -0,20% | 6,30% | -1,34% | -0,20% | 6,30% | -1,34% | 7,47% | 0,49% | 0,00% | 0,00% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | 13 | 54,17% | 11,90% | 6,00% | -2,98% | 11,90% | 6,00% | -2,98% | 13,86% | 0,48% | 0,00% | 0,00% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | 3 | 12,50% | 9,38% | 2,28% | 0,00% | 9,38% | 2,28% | 0,00% | 3,59% | 0,40% | 0,00% | 0,00% |

### Segmentos

| segmento | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commodities | 24 | 57,02% | 25,31% | 23,98% | 0,56 | -11,05% | 54,17% | 18,50% | -8,19% |
| Moedas | 24 | 14,14% | 6,84% | 8,17% | -0,59 | -9,91% | 62,50% | 4,54% | -4,39% |
| Renda Fixa | 24 | 1,23% | 0,61% | 2,12% | -5,45 | -2,67% | 58,33% | 1,15% | -1,29% |
| Renda Variável | 24 | 15,58% | 7,51% | 12,81% | -0,31 | -9,54% | 62,50% | 6,89% | -6,30% |

### Ativos

| ticker | segmento | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GC=F | Commodities | 24 | 110,72% | 45,16% | 13,02% | 2,07 | -4,83% | 75,00% | 10,57% | -2,97% |
| NG=F | Commodities | 24 | 55,34% | 24,63% | 61,31% | 0,45 | -27,24% | 58,33% | 37,42% | -22,66% |
| FIND11.SA | Renda Variável | 24 | 25,56% | 12,05% | 20,73% | 0,07 | -16,33% | 58,33% | 13,15% | -8,14% |
| EURBRL=X | Moedas | 24 | 22,24% | 10,56% | 8,04% | -0,19 | -5,67% | 62,50% | 5,50% | -5,09% |
| BOVV11.SA | Renda Variável | 24 | 21,36% | 10,16% | 12,77% | -0,11 | -11,38% | 58,33% | 6,66% | -4,80% |
| USDBRL=X | Moedas | 24 | 15,40% | 7,42% | 10,16% | -0,41 | -14,08% | 62,50% | 6,06% | -5,15% |
| JPYBRL=X | Moedas | 24 | 4,60% | 2,27% | 10,71% | -0,84 | -13,89% | 37,50% | 7,49% | -3,75% |
| IB5M11.SA | Renda Fixa | 24 | 3,48% | 1,72% | 6,37% | -1,60 | -7,91% | 58,33% | 3,44% | -3,86% |
| IMAB11.SA | Renda Fixa | 24 | 0,00% | 0,00% | 0,00% | -21,82 | 0,00% | 0,00% | 0,00% | 0,00% |
| B5MB11.SA | Renda Fixa | 24 | 0,00% | 0,00% | 0,00% | -21,82 | 0,00% | 0,00% | 0,00% | 0,00% |
| MATB11.SA | Renda Variável | 24 | -1,76% | -0,88% | 15,01% | -0,79 | -16,94% | 50,00% | 8,73% | -9,45% |
| ZC=F | Commodities | 24 | -7,12% | -3,62% | 19,03% | -0,73 | -18,26% | 54,17% | 12,37% | -10,98% |

### 5 melhores meses

| data | regime | nome_regime | retorno_estrategia | retorno_benchmark | retorno_cdi |
| --- | --- | --- | --- | --- | --- |
| 31/10/2025 | Recessão desinflacionária | Recessão desinflacionária | 3,51% | 3,51% | 1,28% |
| 30/09/2024 | Expansão inflacionária | Expansão inflacionária | 3,49% | 3,49% | 0,84% |
| 30/11/2025 | Recessão desinflacionária | Recessão desinflacionária | 3,31% | 3,31% | 1,05% |
| 31/03/2025 | Expansão inflacionária | Expansão inflacionária | 3,14% | 3,14% | 0,96% |
| 31/08/2024 | Expansão inflacionária | Expansão inflacionária | 3,02% | 3,02% | 0,87% |

### 5 piores meses

| data | regime | nome_regime | retorno_estrategia | retorno_benchmark | retorno_cdi |
| --- | --- | --- | --- | --- | --- |
| 31/01/2024 | Expansão desinflacionária | Expansão desinflacionária | -3,64% | -3,64% | 0,97% |
| 31/07/2025 | Expansão inflacionária | Expansão inflacionária | -2,41% | -2,41% | 1,28% |
| 29/02/2024 | Expansão desinflacionária | Expansão desinflacionária | -1,34% | -1,34% | 0,80% |
| 30/06/2025 | Expansão inflacionária | Expansão inflacionária | -0,59% | -0,59% | 1,10% |
| 31/10/2024 | Expansão inflacionária | Expansão inflacionária | -0,51% | -0,51% | 0,93% |

![Desempenho — Validação](graficos_periodos/02_validacao.png)

**Interpretação:** o objetivo é verificar se as regras definidas no desenvolvimento continuaram funcionando sem novos ajustes.

---

## 8. Teste final fora da amostra

**Intervalo oficial:** 01/01/2026 a 02/08/2026  
**Função:** Teste final de generalização sem novos ajustes  
**Ajusta parâmetros:** Não  
**Altera regras:** Não  

> A base disponível cobre 7 de 8 meses do intervalo oficial. As conclusões deste bloco são parciais.

### Métricas da carteira

| serie | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Estratégia | 5 | 5,04% | 12,53% | 14,94% | -0,04 | -3,45% | 40,00% | 8,68% | -1,77% |
| Benchmark estático | 5 | 5,04% | 12,53% | 14,94% | -0,04 | -3,45% | 40,00% | 8,68% | -1,77% |
| CDI | 5 | 5,66% | 14,13% | 0,29% | 46,00 | 0,00% | 100,00% | 1,21% | 1,00% |

### Resultado por regime dentro do período

| regime | nome_regime | meses | frequencia | retorno_estrategia | volatilidade_estrategia | drawdown_estrategia | retorno_benchmark | volatilidade_benchmark | drawdown_benchmark | retorno_cdi | volatilidade_cdi | drawdown_cdi | excesso_vs_benchmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 5 | 100,00% | 5,04% | 14,94% | -3,45% | 5,04% | 14,94% | -3,45% | 5,66% | 0,29% | 0,00% | 0,00% |

### Segmentos

| segmento | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commodities | 7 | -10,24% | -16,90% | 16,55% | -1,86 | -14,43% | 28,57% | 4,90% | -6,98% |
| Moedas | 7 | -10,21% | -16,86% | 9,26% | -3,40 | -5,47% | 42,86% | 1,35% | -5,72% |
| Renda Fixa | 7 | 26,11% | 48,84% | 30,24% | 1,01 | -1,95% | 57,14% | 23,18% | -1,75% |
| Renda Variável | 7 | 7,99% | 14,08% | 21,94% | 0,08 | -11,92% | 57,14% | 12,38% | -4,99% |

### Ativos

| ticker | segmento | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMAB11.SA | Renda Fixa | 7 | 43,02% | 84,67% | 49,05% | 1,18 | -0,98% | 71,43% | 37,96% | -0,98% |
| B5MB11.SA | Renda Fixa | 7 | 32,63% | 62,28% | 40,29% | 1,04 | -2,26% | 57,14% | 30,73% | -2,12% |
| BOVV11.SA | Renda Variável | 7 | 10,83% | 19,28% | 21,06% | 0,29 | -8,65% | 42,86% | 12,53% | -7,25% |
| FIND11.SA | Renda Variável | 7 | 9,01% | 15,94% | 25,14% | 0,16 | -12,99% | 71,43% | 14,13% | -7,54% |
| MATB11.SA | Renda Variável | 7 | 3,44% | 5,96% | 25,61% | -0,19 | -15,31% | 71,43% | 10,46% | -8,46% |
| IB5M11.SA | Renda Fixa | 7 | 2,88% | 4,99% | 5,90% | -1,41 | -2,63% | 57,14% | 2,48% | -2,15% |
| ZC=F | Commodities | 7 | 0,06% | 0,10% | 17,53% | -0,69 | -11,19% | 57,14% | 6,78% | -7,61% |
| GC=F | Commodities | 7 | -7,35% | -12,26% | 29,78% | -0,76 | -23,09% | 42,86% | 10,96% | -11,79% |
| USDBRL=X | Moedas | 7 | -8,82% | -14,63% | 12,31% | -2,32 | -4,68% | 42,86% | 2,58% | -6,82% |
| EURBRL=X | Moedas | 7 | -10,70% | -17,64% | 7,19% | -4,52 | -5,73% | 28,57% | 0,59% | -5,27% |
| JPYBRL=X | Moedas | 7 | -11,17% | -18,38% | 9,05% | -3,69 | -7,54% | 28,57% | 1,25% | -5,06% |
| NG=F | Commodities | 7 | -30,84% | -46,86% | 60,21% | -0,95 | -36,91% | 42,86% | 18,90% | -34,34% |

### 5 melhores meses

| data | regime | nome_regime | retorno_estrategia | retorno_benchmark | retorno_cdi |
| --- | --- | --- | --- | --- | --- |
| 31/01/2026 | Expansão desinflacionária | Expansão desinflacionária | 8,68% | 8,68% | 1,16% |
| 31/05/2026 | Expansão desinflacionária | Expansão desinflacionária | 0,10% | 0,10% | 1,07% |
| 30/04/2026 | Expansão desinflacionária | Expansão desinflacionária | -0,74% | -0,74% | 1,09% |
| 28/02/2026 | Expansão desinflacionária | Expansão desinflacionária | -0,98% | -0,98% | 1,00% |
| 31/03/2026 | Expansão desinflacionária | Expansão desinflacionária | -1,77% | -1,77% | 1,21% |

### 5 piores meses

| data | regime | nome_regime | retorno_estrategia | retorno_benchmark | retorno_cdi |
| --- | --- | --- | --- | --- | --- |
| 31/03/2026 | Expansão desinflacionária | Expansão desinflacionária | -1,77% | -1,77% | 1,21% |
| 28/02/2026 | Expansão desinflacionária | Expansão desinflacionária | -0,98% | -0,98% | 1,00% |
| 30/04/2026 | Expansão desinflacionária | Expansão desinflacionária | -0,74% | -0,74% | 1,09% |
| 31/05/2026 | Expansão desinflacionária | Expansão desinflacionária | 0,10% | 0,10% | 1,07% |
| 31/01/2026 | Expansão desinflacionária | Expansão desinflacionária | 8,68% | 8,68% | 1,16% |

![Desempenho — Teste final fora da amostra](graficos_periodos/03_teste_final_fora_amostra.png)

**Interpretação:** este é o principal teste de generalização. Qualquer cobertura inferior ao intervalo oficial deve ser tratada como resultado parcial.

---

## 9. Comparação entre desenvolvimento, validação e teste final

| Período | Função | Início oficial | Fim oficial | Início disponível | Fim disponível | Meses disponíveis | Meses esperados | Cobertura | Ajusta parâmetros? | Altera regras? | Estratégia | Benchmark | CDI | Excesso vs benchmark | Excesso vs CDI | Volatilidade anualizada | Sharpe | Drawdown máximo | Turnover total | Custo total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Desenvolvimento e calibração | Construção, testes e escolha dos parâmetros | 01/01/2020 | 31/12/2023 | 31/01/2020 | 31/12/2023 | 48 | 48 | 100,00% | Sim | Sim | 34,22% | 34,22% | 36,32% | 0,00% | -2,10% | 8,51% | -0,00 | -8,32% | 219,69% | 0,22% |
| Validação | Avaliação das regras e parâmetros congelados | 01/01/2024 | 31/12/2025 | 31/01/2024 | 31/12/2025 | 24 | 24 | 100,00% | Não | Não | 22,15% | 22,15% | 26,76% | 0,00% | -4,61% | 6,47% | -0,26 | -2,98% | 44,01% | 0,04% |
| Teste final fora da amostra | Teste final de generalização sem novos ajustes | 01/01/2026 | 02/08/2026 | 31/01/2026 | 31/07/2026 | 7 | 8 | 87,50% | Não | Não | 5,04% | 5,04% | 5,66% | 0,00% | -0,62% | 14,94% | -0,04 | -3,45% | 12,73% | 0,01% |

A comparação deve priorizar validação e teste final. O bloco de desenvolvimento explica como o modelo foi escolhido; os outros dois blocos avaliam sua capacidade de generalização.

---

## 10. Análise individual dos ativos no período completo

| ticker | segmento | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GC=F | Commodities | 80 | 171,53% | 16,16% | 16,04% | 0,43 | -23,09% | 58,75% | 10,96% | -11,79% |
| MATB11.SA | Renda Variável | 80 | 72,84% | 8,55% | 24,23% | 0,07 | -32,82% | 57,50% | 14,45% | -19,77% |
| BOVV11.SA | Renda Variável | 80 | 54,84% | 6,78% | 22,43% | -0,01 | -35,99% | 56,25% | 16,11% | -30,11% |
| IMAB11.SA | Renda Fixa | 80 | 48,57% | 6,12% | 15,53% | -0,16 | -8,24% | 27,50% | 37,96% | -7,51% |
| FIND11.SA | Renda Variável | 80 | 40,38% | 5,22% | 28,01% | -0,01 | -36,72% | 55,00% | 17,93% | -33,12% |
| EURBRL=X | Moedas | 80 | 31,15% | 4,15% | 11,99% | -0,38 | -24,33% | 56,25% | 16,11% | -7,67% |
| B5MB11.SA | Renda Fixa | 80 | 28,54% | 3,84% | 14,70% | -0,32 | -17,04% | 21,25% | 30,73% | -14,52% |
| IB5M11.SA | Renda Fixa | 80 | 27,53% | 3,71% | 9,80% | -0,54 | -12,30% | 56,25% | 8,08% | -12,30% |
| USDBRL=X | Moedas | 80 | 27,27% | 3,68% | 13,72% | -0,35 | -18,99% | 55,00% | 15,78% | -7,54% |
| NG=F | Commodities | 80 | 25,68% | 3,49% | 66,49% | 0,24 | -80,68% | 52,50% | 51,71% | -41,13% |
| ZC=F | Commodities | 80 | 18,77% | 2,61% | 26,80% | -0,12 | -53,80% | 57,50% | 31,15% | -24,03% |
| JPYBRL=X | Moedas | 80 | -12,50% | -1,98% | 13,94% | -0,73 | -43,32% | 47,50% | 17,51% | -11,87% |

### Ativos por ano

| periodo | ticker | segmento | retorno | meses |
| --- | --- | --- | --- | --- |
| 2020 | GC=F | Commodities | 24,04% | 12 |
| 2020 | NG=F | Commodities | 14,14% | 12 |
| 2020 | ZC=F | Commodities | 21,20% | 12 |
| 2020 | EURBRL=X | Moedas | 42,15% | 12 |
| 2020 | JPYBRL=X | Moedas | 36,18% | 12 |
| 2020 | USDBRL=X | Moedas | 29,69% | 12 |
| 2020 | B5MB11.SA | Renda Fixa | 4,17% | 12 |
| 2020 | IB5M11.SA | Renda Fixa | 2,59% | 12 |
| 2020 | IMAB11.SA | Renda Fixa | 5,78% | 12 |
| 2020 | BOVV11.SA | Renda Variável | 0,29% | 12 |
| 2020 | FIND11.SA | Renda Variável | -9,46% | 12 |
| 2020 | MATB11.SA | Renda Variável | 47,38% | 12 |
| 2021 | GC=F | Commodities | -4,14% | 12 |
| 2021 | NG=F | Commodities | 47,03% | 12 |
| 2021 | ZC=F | Commodities | 25,61% | 12 |
| 2021 | EURBRL=X | Moedas | 1,48% | 12 |
| 2021 | JPYBRL=X | Moedas | -1,39% | 12 |
| 2021 | USDBRL=X | Moedas | 9,49% | 12 |
| 2021 | B5MB11.SA | Renda Fixa | -6,43% | 12 |
| 2021 | IB5M11.SA | Renda Fixa | -7,89% | 12 |
| 2021 | IMAB11.SA | Renda Fixa | -2,96% | 12 |
| 2021 | BOVV11.SA | Renda Variável | -11,89% | 12 |
| 2021 | FIND11.SA | Renda Variável | -24,78% | 12 |
| 2021 | MATB11.SA | Renda Variável | 11,83% | 12 |
| 2022 | GC=F | Commodities | 0,38% | 12 |
| 2022 | NG=F | Commodities | 28,03% | 12 |
| 2022 | ZC=F | Commodities | 14,01% | 12 |
| 2022 | EURBRL=X | Moedas | -13,70% | 12 |
| 2022 | JPYBRL=X | Moedas | -20,80% | 12 |
| 2022 | USDBRL=X | Moedas | -7,64% | 12 |
| 2022 | B5MB11.SA | Renda Fixa | -1,27% | 12 |
| 2022 | IB5M11.SA | Renda Fixa | 4,31% | 12 |
| 2022 | IMAB11.SA | Renda Fixa | 0,89% | 12 |
| 2022 | BOVV11.SA | Renda Variável | 5,46% | 12 |
| 2022 | FIND11.SA | Renda Variável | 11,67% | 12 |
| 2022 | MATB11.SA | Renda Variável | -5,61% | 12 |
| 2023 | GC=F | Commodities | 13,98% | 12 |
| 2023 | NG=F | Commodities | -43,91% | 12 |
| 2023 | ZC=F | Commodities | -30,21% | 12 |
| 2023 | EURBRL=X | Moedas | -4,12% | 12 |
| 2023 | JPYBRL=X | Moedas | -13,16% | 12 |
| 2023 | USDBRL=X | Moedas | -8,37% | 12 |
| 2023 | B5MB11.SA | Renda Fixa | 0,00% | 12 |
| 2023 | IB5M11.SA | Renda Fixa | 21,22% | 12 |
| 2023 | IMAB11.SA | Renda Fixa | 0,00% | 12 |
| 2023 | BOVV11.SA | Renda Variável | 22,95% | 12 |
| 2023 | FIND11.SA | Renda Variável | 34,30% | 12 |
| 2023 | MATB11.SA | Renda Variável | 7,54% | 12 |
| 2024 | GC=F | Commodities | 25,66% | 12 |
| 2024 | NG=F | Commodities | 53,93% | 12 |
| 2024 | ZC=F | Commodities | -4,64% | 12 |
| 2024 | EURBRL=X | Moedas | 20,00% | 12 |
| 2024 | JPYBRL=X | Moedas | 15,04% | 12 |
| 2024 | USDBRL=X | Moedas | 28,34% | 12 |
| 2024 | B5MB11.SA | Renda Fixa | 0,00% | 12 |
| 2024 | IB5M11.SA | Renda Fixa | -8,89% | 12 |
| 2024 | IMAB11.SA | Renda Fixa | 0,00% | 12 |
| 2024 | BOVV11.SA | Renda Variável | -10,02% | 12 |
| 2024 | FIND11.SA | Renda Variável | -14,15% | 12 |
| 2024 | MATB11.SA | Renda Variável | -11,91% | 12 |
| 2025 | GC=F | Commodities | 67,69% | 12 |
| 2025 | NG=F | Commodities | 0,91% | 12 |
| 2025 | ZC=F | Commodities | -2,60% | 12 |
| 2025 | EURBRL=X | Moedas | 1,87% | 12 |
| 2025 | JPYBRL=X | Moedas | -9,08% | 12 |
| 2025 | USDBRL=X | Moedas | -10,08% | 12 |
| 2025 | B5MB11.SA | Renda Fixa | 0,00% | 12 |
| 2025 | IB5M11.SA | Renda Fixa | 13,57% | 12 |
| 2025 | IMAB11.SA | Renda Fixa | 0,00% | 12 |
| 2025 | BOVV11.SA | Renda Variável | 34,88% | 12 |
| 2025 | FIND11.SA | Renda Variável | 46,25% | 12 |
| 2025 | MATB11.SA | Renda Variável | 11,52% | 12 |
| 2026 | GC=F | Commodities | -5,28% | 8 |
| 2026 | NG=F | Commodities | -32,85% | 8 |
| 2026 | ZC=F | Commodities | 5,56% | 8 |
| 2026 | EURBRL=X | Moedas | -10,12% | 8 |
| 2026 | JPYBRL=X | Moedas | -9,44% | 8 |
| 2026 | USDBRL=X | Moedas | -8,21% | 8 |
| 2026 | B5MB11.SA | Renda Fixa | 33,58% | 8 |
| 2026 | IB5M11.SA | Renda Fixa | 3,15% | 8 |
| 2026 | IMAB11.SA | Renda Fixa | 43,45% | 8 |
| 2026 | BOVV11.SA | Renda Variável | 11,35% | 8 |
| 2026 | FIND11.SA | Renda Variável | 9,46% | 8 |
| 2026 | MATB11.SA | Renda Variável | 5,16% | 8 |

### Ativos por semestre

| periodo | ticker | segmento | retorno | meses |
| --- | --- | --- | --- | --- |
| 2020 — 1º semestre | GC=F | Commodities | 17,61% | 6 |
| 2020 — 1º semestre | NG=F | Commodities | -17,48% | 6 |
| 2020 — 1º semestre | ZC=F | Commodities | -13,54% | 6 |
| 2020 — 1º semestre | EURBRL=X | Moedas | 35,33% | 6 |
| 2020 — 1º semestre | JPYBRL=X | Moedas | 35,94% | 6 |
| 2020 — 1º semestre | USDBRL=X | Moedas | 34,50% | 6 |
| 2020 — 1º semestre | B5MB11.SA | Renda Fixa | -5,98% | 6 |
| 2020 — 1º semestre | IB5M11.SA | Renda Fixa | -5,52% | 6 |
| 2020 — 1º semestre | IMAB11.SA | Renda Fixa | -1,72% | 6 |
| 2020 — 1º semestre | BOVV11.SA | Renda Variável | -19,78% | 6 |
| 2020 — 1º semestre | FIND11.SA | Renda Variável | -26,88% | 6 |
| 2020 — 1º semestre | MATB11.SA | Renda Variável | -11,05% | 6 |
| 2020 — 2º semestre | GC=F | Commodities | 5,47% | 6 |
| 2020 — 2º semestre | NG=F | Commodities | 38,32% | 6 |
| 2020 — 2º semestre | ZC=F | Commodities | 40,18% | 6 |
| 2020 — 2º semestre | EURBRL=X | Moedas | 5,04% | 6 |
| 2020 — 2º semestre | JPYBRL=X | Moedas | 0,18% | 6 |
| 2020 — 2º semestre | USDBRL=X | Moedas | -3,58% | 6 |
| 2020 — 2º semestre | B5MB11.SA | Renda Fixa | 10,79% | 6 |
| 2020 — 2º semestre | IB5M11.SA | Renda Fixa | 8,58% | 6 |
| 2020 — 2º semestre | IMAB11.SA | Renda Fixa | 7,64% | 6 |
| 2020 — 2º semestre | BOVV11.SA | Renda Variável | 25,02% | 6 |
| 2020 — 2º semestre | FIND11.SA | Renda Variável | 23,83% | 6 |
| 2020 — 2º semestre | MATB11.SA | Renda Variável | 65,69% | 6 |
| 2021 — 1º semestre | GC=F | Commodities | -6,36% | 6 |
| 2021 — 1º semestre | NG=F | Commodities | 50,70% | 6 |
| 2021 — 1º semestre | ZC=F | Commodities | 51,74% | 6 |
| 2021 — 1º semestre | EURBRL=X | Moedas | -7,60% | 6 |
| 2021 — 1º semestre | JPYBRL=X | Moedas | -10,89% | 6 |
| 2021 — 1º semestre | USDBRL=X | Moedas | -4,87% | 6 |
| 2021 — 1º semestre | B5MB11.SA | Renda Fixa | -2,71% | 6 |
| 2021 — 1º semestre | IB5M11.SA | Renda Fixa | -0,50% | 6 |
| 2021 — 1º semestre | IMAB11.SA | Renda Fixa | -1,29% | 6 |
| 2021 — 1º semestre | BOVV11.SA | Renda Variável | 6,62% | 6 |
| 2021 — 1º semestre | FIND11.SA | Renda Variável | -0,32% | 6 |
| 2021 — 1º semestre | MATB11.SA | Renda Variável | 25,22% | 6 |
| 2021 — 2º semestre | GC=F | Commodities | 2,37% | 6 |
| 2021 — 2º semestre | NG=F | Commodities | -2,44% | 6 |
| 2021 — 2º semestre | ZC=F | Commodities | -17,22% | 6 |
| 2021 — 2º semestre | EURBRL=X | Moedas | 9,83% | 6 |
| 2021 — 2º semestre | JPYBRL=X | Moedas | 10,66% | 6 |
| 2021 — 2º semestre | USDBRL=X | Moedas | 15,09% | 6 |
| 2021 — 2º semestre | B5MB11.SA | Renda Fixa | -3,83% | 6 |
| 2021 — 2º semestre | IB5M11.SA | Renda Fixa | -7,43% | 6 |
| 2021 — 2º semestre | IMAB11.SA | Renda Fixa | -1,68% | 6 |
| 2021 — 2º semestre | BOVV11.SA | Renda Variável | -17,36% | 6 |
| 2021 — 2º semestre | FIND11.SA | Renda Variável | -24,53% | 6 |
| 2021 — 2º semestre | MATB11.SA | Renda Variável | -10,69% | 6 |
| 2022 — 1º semestre | GC=F | Commodities | -0,47% | 6 |
| 2022 — 1º semestre | NG=F | Commodities | 52,32% | 6 |
| 2022 — 1º semestre | ZC=F | Commodities | 24,79% | 6 |
| 2022 — 1º semestre | EURBRL=X | Moedas | -16,44% | 6 |
| 2022 — 1º semestre | JPYBRL=X | Moedas | -23,52% | 6 |
| 2022 — 1º semestre | USDBRL=X | Moedas | -9,15% | 6 |
| 2022 — 1º semestre | B5MB11.SA | Renda Fixa | -1,27% | 6 |
| 2022 — 1º semestre | IB5M11.SA | Renda Fixa | 3,85% | 6 |
| 2022 — 1º semestre | IMAB11.SA | Renda Fixa | 0,89% | 6 |
| 2022 — 1º semestre | BOVV11.SA | Renda Variável | -5,87% | 6 |
| 2022 — 1º semestre | FIND11.SA | Renda Variável | 1,16% | 6 |
| 2022 — 1º semestre | MATB11.SA | Renda Variável | -16,60% | 6 |
| 2022 — 2º semestre | GC=F | Commodities | 0,85% | 6 |
| 2022 — 2º semestre | NG=F | Commodities | -15,95% | 6 |
| 2022 — 2º semestre | ZC=F | Commodities | -8,64% | 6 |
| 2022 — 2º semestre | EURBRL=X | Moedas | 3,29% | 6 |
| 2022 — 2º semestre | JPYBRL=X | Moedas | 3,56% | 6 |
| 2022 — 2º semestre | USDBRL=X | Moedas | 1,66% | 6 |
| 2022 — 2º semestre | B5MB11.SA | Renda Fixa | 0,00% | 6 |
| 2022 — 2º semestre | IB5M11.SA | Renda Fixa | 0,44% | 6 |
| 2022 — 2º semestre | IMAB11.SA | Renda Fixa | 0,00% | 6 |
| 2022 — 2º semestre | BOVV11.SA | Renda Variável | 12,03% | 6 |
| 2022 — 2º semestre | FIND11.SA | Renda Variável | 10,39% | 6 |
| 2022 — 2º semestre | MATB11.SA | Renda Variável | 13,17% | 6 |
| 2023 — 1º semestre | GC=F | Commodities | 5,58% | 6 |
| 2023 — 1º semestre | NG=F | Commodities | -38,63% | 6 |
| 2023 — 1º semestre | ZC=F | Commodities | -18,40% | 6 |
| 2023 — 1º semestre | EURBRL=X | Moedas | -5,62% | 6 |
| 2023 — 1º semestre | JPYBRL=X | Moedas | -14,65% | 6 |
| 2023 — 1º semestre | USDBRL=X | Moedas | -7,81% | 6 |
| 2023 — 1º semestre | B5MB11.SA | Renda Fixa | 0,00% | 6 |
| 2023 — 1º semestre | IB5M11.SA | Renda Fixa | 15,82% | 6 |
| 2023 — 1º semestre | IMAB11.SA | Renda Fixa | 0,00% | 6 |
| 2023 — 1º semestre | BOVV11.SA | Renda Variável | 7,65% | 6 |
| 2023 — 1º semestre | FIND11.SA | Renda Variável | 19,66% | 6 |
| 2023 — 1º semestre | MATB11.SA | Renda Variável | -9,57% | 6 |
| 2023 — 2º semestre | GC=F | Commodities | 7,95% | 6 |
| 2023 — 2º semestre | NG=F | Commodities | -8,61% | 6 |
| 2023 — 2º semestre | ZC=F | Commodities | -14,47% | 6 |
| 2023 — 2º semestre | EURBRL=X | Moedas | 1,58% | 6 |
| 2023 — 2º semestre | JPYBRL=X | Moedas | 1,74% | 6 |
| 2023 — 2º semestre | USDBRL=X | Moedas | -0,61% | 6 |
| 2023 — 2º semestre | B5MB11.SA | Renda Fixa | 0,00% | 6 |
| 2023 — 2º semestre | IB5M11.SA | Renda Fixa | 4,66% | 6 |
| 2023 — 2º semestre | IMAB11.SA | Renda Fixa | 0,00% | 6 |
| 2023 — 2º semestre | BOVV11.SA | Renda Variável | 14,21% | 6 |
| 2023 — 2º semestre | FIND11.SA | Renda Variável | 12,24% | 6 |
| 2023 — 2º semestre | MATB11.SA | Renda Variável | 18,92% | 6 |
| 2024 — 1º semestre | GC=F | Commodities | 12,24% | 6 |
| 2024 — 1º semestre | NG=F | Commodities | 1,72% | 6 |
| 2024 — 1º semestre | ZC=F | Commodities | -16,24% | 6 |
| 2024 — 1º semestre | EURBRL=X | Moedas | 9,96% | 6 |
| 2024 — 1º semestre | JPYBRL=X | Moedas | 0,30% | 6 |
| 2024 — 1º semestre | USDBRL=X | Moedas | 13,97% | 6 |
| 2024 — 1º semestre | B5MB11.SA | Renda Fixa | 0,00% | 6 |
| 2024 — 1º semestre | IB5M11.SA | Renda Fixa | -4,83% | 6 |
| 2024 — 1º semestre | IMAB11.SA | Renda Fixa | 0,00% | 6 |
| 2024 — 1º semestre | BOVV11.SA | Renda Variável | -7,60% | 6 |
| 2024 — 1º semestre | FIND11.SA | Renda Variável | -11,94% | 6 |
| 2024 — 1º semestre | MATB11.SA | Renda Variável | -9,77% | 6 |
| 2024 — 2º semestre | GC=F | Commodities | 11,96% | 6 |
| 2024 — 2º semestre | NG=F | Commodities | 51,33% | 6 |
| 2024 — 2º semestre | ZC=F | Commodities | 13,85% | 6 |
| 2024 — 2º semestre | EURBRL=X | Moedas | 9,13% | 6 |
| 2024 — 2º semestre | JPYBRL=X | Moedas | 14,69% | 6 |
| 2024 — 2º semestre | USDBRL=X | Moedas | 12,60% | 6 |
| 2024 — 2º semestre | B5MB11.SA | Renda Fixa | 0,00% | 6 |
| 2024 — 2º semestre | IB5M11.SA | Renda Fixa | -4,26% | 6 |
| 2024 — 2º semestre | IMAB11.SA | Renda Fixa | 0,00% | 6 |
| 2024 — 2º semestre | BOVV11.SA | Renda Variável | -2,62% | 6 |
| 2024 — 2º semestre | FIND11.SA | Renda Variável | -2,51% | 6 |
| 2024 — 2º semestre | MATB11.SA | Renda Variável | -2,36% | 6 |
| 2025 — 1º semestre | GC=F | Commodities | 26,41% | 6 |
| 2025 — 1º semestre | NG=F | Commodities | -12,20% | 6 |
| 2025 — 1º semestre | ZC=F | Commodities | -7,02% | 6 |
| 2025 — 1º semestre | EURBRL=X | Moedas | -0,16% | 6 |
| 2025 — 1º semestre | JPYBRL=X | Moedas | -3,42% | 6 |
| 2025 — 1º semestre | USDBRL=X | Moedas | -11,55% | 6 |
| 2025 — 1º semestre | B5MB11.SA | Renda Fixa | 0,00% | 6 |
| 2025 — 1º semestre | IB5M11.SA | Renda Fixa | 10,08% | 6 |
| 2025 — 1º semestre | IMAB11.SA | Renda Fixa | 0,00% | 6 |
| 2025 — 1º semestre | BOVV11.SA | Renda Variável | 15,80% | 6 |
| 2025 — 1º semestre | FIND11.SA | Renda Variável | 31,36% | 6 |
| 2025 — 1º semestre | MATB11.SA | Renda Variável | -9,22% | 6 |
| 2025 — 2º semestre | GC=F | Commodities | 32,65% | 6 |
| 2025 — 2º semestre | NG=F | Commodities | 14,93% | 6 |
| 2025 — 2º semestre | ZC=F | Commodities | 4,76% | 6 |
| 2025 — 2º semestre | EURBRL=X | Moedas | 2,03% | 6 |
| 2025 — 2º semestre | JPYBRL=X | Moedas | -5,86% | 6 |
| 2025 — 2º semestre | USDBRL=X | Moedas | 1,66% | 6 |
| 2025 — 2º semestre | B5MB11.SA | Renda Fixa | 0,00% | 6 |
| 2025 — 2º semestre | IB5M11.SA | Renda Fixa | 3,17% | 6 |
| 2025 — 2º semestre | IMAB11.SA | Renda Fixa | 0,00% | 6 |
| 2025 — 2º semestre | BOVV11.SA | Renda Variável | 16,48% | 6 |
| 2025 — 2º semestre | FIND11.SA | Renda Variável | 11,34% | 6 |
| 2025 — 2º semestre | MATB11.SA | Renda Variável | 22,85% | 6 |
| 2026 — 1º semestre | GC=F | Commodities | -7,94% | 6 |
| 2026 — 1º semestre | NG=F | Commodities | -17,55% | 6 |
| 2026 — 1º semestre | ZC=F | Commodities | -6,30% | 6 |
| 2026 — 1º semestre | EURBRL=X | Moedas | -9,64% | 6 |
| 2026 — 1º semestre | JPYBRL=X | Moedas | -10,34% | 6 |
| 2026 — 1º semestre | USDBRL=X | Moedas | -6,95% | 6 |
| 2026 — 1º semestre | B5MB11.SA | Renda Fixa | 31,87% | 6 |
| 2026 — 1º semestre | IB5M11.SA | Renda Fixa | 1,93% | 6 |
| 2026 — 1º semestre | IMAB11.SA | Renda Fixa | 41,85% | 6 |
| 2026 — 1º semestre | BOVV11.SA | Renda Variável | 7,01% | 6 |
| 2026 — 1º semestre | FIND11.SA | Renda Variável | 3,94% | 6 |
| 2026 — 1º semestre | MATB11.SA | Renda Variável | -5,33% | 6 |
| 2026 — 2º semestre | GC=F | Commodities | 2,90% | 2 |
| 2026 — 2º semestre | NG=F | Commodities | -18,56% | 2 |
| 2026 — 2º semestre | ZC=F | Commodities | 12,66% | 2 |
| 2026 — 2º semestre | EURBRL=X | Moedas | -0,52% | 2 |
| 2026 — 2º semestre | JPYBRL=X | Moedas | 1,00% | 2 |
| 2026 — 2º semestre | USDBRL=X | Moedas | -1,35% | 2 |
| 2026 — 2º semestre | B5MB11.SA | Renda Fixa | 1,29% | 2 |
| 2026 — 2º semestre | IB5M11.SA | Renda Fixa | 1,19% | 2 |
| 2026 — 2º semestre | IMAB11.SA | Renda Fixa | 1,13% | 2 |
| 2026 — 2º semestre | BOVV11.SA | Renda Variável | 4,05% | 2 |
| 2026 — 2º semestre | FIND11.SA | Renda Variável | 5,32% | 2 |
| 2026 — 2º semestre | MATB11.SA | Renda Variável | 11,08% | 2 |

### Ativos por regime

| regime | nome_regime | ticker | segmento | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | GC=F | Commodities | 34 | 63,25% | 18,89% | 16,07% | 0,43 | -12,81% | 58,82% | 10,96% | -11,14% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | NG=F | Commodities | 34 | -78,06% | -41,46% | 64,60% | -0,65 | -87,27% | 47,06% | 29,93% | -41,13% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | ZC=F | Commodities | 34 | -31,69% | -12,59% | 19,48% | -1,19 | -48,56% | 50,00% | 13,53% | -10,98% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | EURBRL=X | Moedas | 34 | -0,02% | -0,01% | 9,64% | -1,16 | -14,40% | 52,94% | 5,50% | -7,16% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | JPYBRL=X | Moedas | 34 | -22,36% | -8,54% | 13,28% | -1,48 | -29,18% | 44,12% | 7,49% | -11,87% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | USDBRL=X | Moedas | 34 | -3,27% | -1,17% | 11,71% | -1,03 | -18,28% | 52,94% | 5,74% | -6,88% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | B5MB11.SA | Renda Fixa | 34 | 38,62% | 12,22% | 18,32% | 0,07 | -1,17% | 14,71% | 30,73% | -1,17% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | IB5M11.SA | Renda Fixa | 34 | 26,02% | 8,51% | 7,96% | -0,41 | -4,83% | 58,82% | 7,24% | -3,41% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | IMAB11.SA | Renda Fixa | 34 | 43,45% | 13,58% | 22,54% | 0,14 | -0,36% | 17,65% | 37,96% | -0,36% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | BOVV11.SA | Renda Variável | 34 | 22,59% | 7,45% | 17,95% | -0,17 | -13,63% | 55,88% | 12,63% | -10,21% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | FIND11.SA | Renda Variável | 34 | 12,37% | 4,20% | 23,31% | -0,22 | -17,07% | 55,88% | 16,27% | -13,69% |
| EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | MATB11.SA | Renda Variável | 34 | 20,26% | 6,73% | 21,55% | -0,14 | -17,46% | 58,82% | 13,31% | -10,88% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | GC=F | Commodities | 30 | 35,56% | 12,94% | 13,80% | 0,35 | -11,17% | 50,00% | 10,08% | -6,45% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | NG=F | Commodities | 30 | 68,26% | 23,14% | 70,48% | 0,50 | -51,66% | 53,33% | 51,71% | -33,41% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | ZC=F | Commodities | 30 | 72,99% | 24,51% | 30,81% | 0,58 | -18,26% | 60,00% | 31,15% | -17,14% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | EURBRL=X | Moedas | 30 | 20,61% | 7,78% | 15,26% | 0,02 | -9,33% | 56,67% | 16,11% | -7,67% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | JPYBRL=X | Moedas | 30 | 13,14% | 5,06% | 16,36% | -0,13 | -15,23% | 46,67% | 17,51% | -7,13% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | USDBRL=X | Moedas | 30 | 22,74% | 8,54% | 17,18% | 0,07 | -12,60% | 56,67% | 15,78% | -7,54% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | B5MB11.SA | Renda Fixa | 30 | -9,50% | -3,91% | 12,52% | -0,92 | -14,52% | 16,67% | 7,12% | -14,52% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | IB5M11.SA | Renda Fixa | 30 | -3,51% | -1,42% | 11,67% | -0,78 | -12,35% | 53,33% | 5,36% | -12,30% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | IMAB11.SA | Renda Fixa | 30 | -3,51% | -1,42% | 6,61% | -1,42 | -8,24% | 26,67% | 4,64% | -7,51% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | BOVV11.SA | Renda Variável | 30 | -0,89% | -0,36% | 28,92% | -0,15 | -30,11% | 53,33% | 16,11% | -30,11% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | FIND11.SA | Renda Variável | 30 | 2,41% | 0,96% | 35,50% | -0,02 | -33,12% | 50,00% | 17,93% | -33,12% |
| EXPANSAO_INFLACIONARIA | Expansão inflacionária | MATB11.SA | Renda Variável | 30 | 11,70% | 4,53% | 27,81% | -0,00 | -27,42% | 56,67% | 14,45% | -19,77% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | GC=F | Commodities | 8 | 36,09% | 58,77% | 16,43% | 2,65 | -4,07% | 87,50% | 10,57% | -4,07% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | NG=F | Commodities | 8 | 109,82% | 203,93% | 62,67% | 2,00 | -5,30% | 62,50% | 46,19% | -5,30% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | ZC=F | Commodities | 8 | 33,13% | 53,61% | 17,80% | 2,12 | -6,65% | 87,50% | 10,28% | -6,65% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | EURBRL=X | Moedas | 8 | 11,96% | 18,47% | 7,24% | 1,20 | -1,74% | 62,50% | 4,82% | -1,25% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | JPYBRL=X | Moedas | 8 | -0,94% | -1,40% | 9,61% | -0,71 | -6,97% | 50,00% | 4,36% | -2,75% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | USDBRL=X | Moedas | 8 | 4,42% | 6,70% | 10,58% | 0,02 | -4,62% | 50,00% | 4,58% | -4,59% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | B5MB11.SA | Renda Fixa | 8 | 5,15% | 7,83% | 11,45% | 0,11 | -5,90% | 37,50% | 7,27% | -3,05% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | IB5M11.SA | Renda Fixa | 8 | 7,38% | 11,27% | 13,02% | 0,36 | -6,44% | 62,50% | 8,08% | -3,71% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | IMAB11.SA | Renda Fixa | 8 | 8,25% | 12,63% | 8,99% | 0,57 | -3,50% | 37,50% | 5,04% | -2,46% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | BOVV11.SA | Renda Variável | 8 | 32,36% | 52,27% | 18,82% | 2,00 | -8,16% | 75,00% | 9,03% | -4,82% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | FIND11.SA | Renda Variável | 8 | 26,22% | 41,81% | 26,09% | 1,22 | -13,82% | 75,00% | 13,11% | -8,34% |
| RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | MATB11.SA | Renda Variável | 8 | 55,10% | 93,17% | 18,62% | 3,21 | -0,46% | 75,00% | 12,91% | -0,46% |
| ESTAGFLACAO | Estagflação | GC=F | Commodities | 5 | -0,68% | -1,62% | 19,20% | -0,23 | -7,74% | 60,00% | 7,65% | -6,92% |
| ESTAGFLACAO | Estagflação | NG=F | Commodities | 5 | 100,17% | 428,88% | 44,38% | 4,09 | 0,00% | 100,00% | 34,04% | 1,88% |
| ESTAGFLACAO | Estagflação | ZC=F | Commodities | 5 | -27,47% | -53,73% | 44,20% | -1,59 | -25,83% | 40,00% | 9,63% | -24,03% |
| ESTAGFLACAO | Estagflação | EURBRL=X | Moedas | 5 | -2,93% | -6,88% | 14,88% | -0,71 | -7,66% | 60,00% | 2,73% | -7,66% |
| ESTAGFLACAO | Estagflação | JPYBRL=X | Moedas | 5 | -1,33% | -3,15% | 13,97% | -0,49 | -6,02% | 60,00% | 3,58% | -6,02% |
| ESTAGFLACAO | Estagflação | USDBRL=X | Moedas | 5 | 1,46% | 3,54% | 13,68% | -0,01 | -5,40% | 60,00% | 4,46% | -5,40% |
| ESTAGFLACAO | Estagflação | B5MB11.SA | Renda Fixa | 5 | -1,72% | -4,07% | 4,56% | -1,76 | -3,35% | 40,00% | 1,05% | -2,32% |
| ESTAGFLACAO | Estagflação | IB5M11.SA | Renda Fixa | 5 | -1,36% | -3,24% | 5,51% | -1,31 | -3,54% | 40,00% | 1,96% | -2,42% |
| ESTAGFLACAO | Estagflação | IMAB11.SA | Renda Fixa | 5 | -0,98% | -2,33% | 3,18% | -2,08 | -1,74% | 60,00% | 0,64% | -1,24% |
| ESTAGFLACAO | Estagflação | BOVV11.SA | Renda Variável | 5 | -6,63% | -15,18% | 16,65% | -1,16 | -12,61% | 40,00% | 5,83% | -6,57% |
| ESTAGFLACAO | Estagflação | FIND11.SA | Renda Variável | 5 | -9,01% | -20,28% | 19,75% | -1,26 | -14,98% | 20,00% | 7,02% | -8,50% |
| ESTAGFLACAO | Estagflação | MATB11.SA | Renda Variável | 5 | -18,88% | -39,48% | 12,97% | -4,02 | -15,11% | 20,00% | 0,13% | -9,79% |

---

## 11. Análise por segmento

| segmento | meses | retorno_total | retorno_anualizado | volatilidade_anualizada | sharpe | drawdown_maximo | meses_positivos | melhor_mes | pior_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commodities | 80 | 138,16% | 13,90% | 24,02% | 0,26 | -41,07% | 52,50% | 18,91% | -12,27% |
| Moedas | 80 | 14,30% | 2,02% | 12,39% | -0,53 | -27,20% | 55,00% | 16,47% | -8,64% |
| Renda Fixa | 80 | 36,44% | 4,77% | 11,42% | -0,37 | -12,08% | 57,50% | 23,18% | -11,44% |
| Renda Variável | 80 | 62,62% | 7,57% | 22,09% | 0,02 | -33,79% | 58,75% | 16,16% | -27,66% |

---

## 12. Episódios macroeconômicos

Cada episódio representa uma sequência contínua de meses no mesmo regime.

| episodio | regime | nome_regime | inicio | fim | meses | retorno_estrategia | retorno_benchmark | retorno_cdi | excesso_vs_benchmark | melhor_ativo | retorno_melhor_ativo | pior_ativo | retorno_pior_ativo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 31/01/2020 | 31/01/2020 | 1 | -0,67% | -0,67% | 0,38% | 0,00% | USDBRL=X | 5,62% | NG=F | -13,24% |
| 2 | EXPANSAO_INFLACIONARIA | Expansão inflacionária | 29/02/2020 | 30/04/2020 | 3 | -3,75% | -3,75% | 0,92% | 0,00% | JPYBRL=X | 28,47% | FIND11.SA | -34,15% |
| 3 | RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | 31/05/2020 | 30/09/2020 | 5 | 15,64% | 15,64% | 0,96% | 0,00% | MATB11.SA | 44,01% | IB5M11.SA | 2,92% |
| 4 | EXPANSAO_INFLACIONARIA | Expansão inflacionária | 31/10/2020 | 30/04/2021 | 7 | 17,78% | 17,78% | 1,17% | 0,00% | ZC=F | 95,25% | JPYBRL=X | -8,02% |
| 5 | ESTAGFLACAO | Estagflação | 31/05/2021 | 30/09/2021 | 5 | 0,69% | 0,69% | 1,82% | 0,00% | NG=F | 100,17% | ZC=F | -27,47% |
| 6 | EXPANSAO_INFLACIONARIA | Expansão inflacionária | 31/10/2021 | 31/01/2022 | 4 | 0,68% | 0,68% | 2,60% | 0,00% | ZC=F | 16,63% | NG=F | -16,93% |
| 7 | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 28/02/2022 | 31/05/2022 | 4 | 3,08% | 3,08% | 3,60% | 0,00% | NG=F | 67,11% | JPYBRL=X | -20,12% |
| 8 | EXPANSAO_INFLACIONARIA | Expansão inflacionária | 30/06/2022 | 31/08/2022 | 3 | -0,19% | -0,19% | 3,25% | 0,00% | NG=F | 12,06% | MATB11.SA | -19,60% |
| 9 | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 30/09/2022 | 31/07/2024 | 23 | -2,06% | -2,06% | 25,18% | 0,00% | GC=F | 41,67% | NG=F | -77,69% |
| 10 | EXPANSAO_INFLACIONARIA | Expansão inflacionária | 31/08/2024 | 31/08/2025 | 13 | 11,90% | 11,90% | 13,86% | 0,00% | NG=F | 47,20% | MATB11.SA | -4,66% |
| 11 | RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | 30/09/2025 | 30/11/2025 | 3 | 9,38% | 9,38% | 3,59% | 0,00% | NG=F | 61,83% | JPYBRL=X | -6,97% |
| 12 | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 31/12/2025 | 31/05/2026 | 6 | 5,79% | 5,79% | 6,95% | 0,00% | IMAB11.SA | 43,26% | NG=F | -32,16% |

### Episódio 1 — Expansão desinflacionária

- Período: **31/01/2020 a 31/01/2020**.
- Duração: **1 meses**.
- Estratégia: **-0,67%**.
- Benchmark: **-0,67%**.
- Excesso: **0,00%**.
- Melhor ativo: **USDBRL=X** (5,62%).
- Pior ativo: **NG=F** (-13,24%).

### Episódio 2 — Expansão inflacionária

- Período: **29/02/2020 a 30/04/2020**.
- Duração: **3 meses**.
- Estratégia: **-3,75%**.
- Benchmark: **-3,75%**.
- Excesso: **0,00%**.
- Melhor ativo: **JPYBRL=X** (28,47%).
- Pior ativo: **FIND11.SA** (-34,15%).

### Episódio 3 — Recessão desinflacionária

- Período: **31/05/2020 a 30/09/2020**.
- Duração: **5 meses**.
- Estratégia: **15,64%**.
- Benchmark: **15,64%**.
- Excesso: **0,00%**.
- Melhor ativo: **MATB11.SA** (44,01%).
- Pior ativo: **IB5M11.SA** (2,92%).

### Episódio 4 — Expansão inflacionária

- Período: **31/10/2020 a 30/04/2021**.
- Duração: **7 meses**.
- Estratégia: **17,78%**.
- Benchmark: **17,78%**.
- Excesso: **0,00%**.
- Melhor ativo: **ZC=F** (95,25%).
- Pior ativo: **JPYBRL=X** (-8,02%).

### Episódio 5 — Estagflação

- Período: **31/05/2021 a 30/09/2021**.
- Duração: **5 meses**.
- Estratégia: **0,69%**.
- Benchmark: **0,69%**.
- Excesso: **0,00%**.
- Melhor ativo: **NG=F** (100,17%).
- Pior ativo: **ZC=F** (-27,47%).

### Episódio 6 — Expansão inflacionária

- Período: **31/10/2021 a 31/01/2022**.
- Duração: **4 meses**.
- Estratégia: **0,68%**.
- Benchmark: **0,68%**.
- Excesso: **0,00%**.
- Melhor ativo: **ZC=F** (16,63%).
- Pior ativo: **NG=F** (-16,93%).

### Episódio 7 — Expansão desinflacionária

- Período: **28/02/2022 a 31/05/2022**.
- Duração: **4 meses**.
- Estratégia: **3,08%**.
- Benchmark: **3,08%**.
- Excesso: **0,00%**.
- Melhor ativo: **NG=F** (67,11%).
- Pior ativo: **JPYBRL=X** (-20,12%).

### Episódio 8 — Expansão inflacionária

- Período: **30/06/2022 a 31/08/2022**.
- Duração: **3 meses**.
- Estratégia: **-0,19%**.
- Benchmark: **-0,19%**.
- Excesso: **0,00%**.
- Melhor ativo: **NG=F** (12,06%).
- Pior ativo: **MATB11.SA** (-19,60%).

### Episódio 9 — Expansão desinflacionária

- Período: **30/09/2022 a 31/07/2024**.
- Duração: **23 meses**.
- Estratégia: **-2,06%**.
- Benchmark: **-2,06%**.
- Excesso: **0,00%**.
- Melhor ativo: **GC=F** (41,67%).
- Pior ativo: **NG=F** (-77,69%).

### Episódio 10 — Expansão inflacionária

- Período: **31/08/2024 a 31/08/2025**.
- Duração: **13 meses**.
- Estratégia: **11,90%**.
- Benchmark: **11,90%**.
- Excesso: **0,00%**.
- Melhor ativo: **NG=F** (47,20%).
- Pior ativo: **MATB11.SA** (-4,66%).

### Episódio 11 — Recessão desinflacionária

- Período: **30/09/2025 a 30/11/2025**.
- Duração: **3 meses**.
- Estratégia: **9,38%**.
- Benchmark: **9,38%**.
- Excesso: **0,00%**.
- Melhor ativo: **NG=F** (61,83%).
- Pior ativo: **JPYBRL=X** (-6,97%).

### Episódio 12 — Expansão desinflacionária

- Período: **31/12/2025 a 31/05/2026**.
- Duração: **6 meses**.
- Estratégia: **5,79%**.
- Benchmark: **5,79%**.
- Excesso: **0,00%**.
- Melhor ativo: **IMAB11.SA** (43,26%).
- Pior ativo: **NG=F** (-32,16%).

---

## 13. Transições de regime

| transicao | data | regime_anterior | novo_regime | retorno_3m_antes | retorno_mes_0_a_3 |
| --- | --- | --- | --- | --- | --- |
| 1 | 29/02/2020 | Expansão desinflacionária | Expansão inflacionária | -0,67% | -0,76% |
| 2 | 31/05/2020 | Expansão inflacionária | Recessão desinflacionária | -3,75% | 16,28% |
| 3 | 31/10/2020 | Recessão desinflacionária | Expansão inflacionária | 8,74% | 11,93% |
| 4 | 31/05/2021 | Expansão inflacionária | Estagflação | 5,23% | -0,58% |
| 5 | 31/10/2021 | Estagflação | Expansão inflacionária | -0,16% | 0,68% |
| 6 | 28/02/2022 | Expansão inflacionária | Expansão desinflacionária | 2,47% | 3,08% |
| 7 | 30/06/2022 | Expansão desinflacionária | Expansão inflacionária | 4,52% | -1,09% |
| 8 | 30/09/2022 | Expansão inflacionária | Expansão desinflacionária | -0,19% | -1,24% |
| 9 | 31/08/2024 | Expansão desinflacionária | Expansão inflacionária | 2,82% | 8,35% |
| 10 | 30/09/2025 | Expansão inflacionária | Recessão desinflacionária | -1,65% | 10,16% |
| 11 | 31/12/2025 | Recessão desinflacionária | Expansão desinflacionária | 9,38% | 6,48% |

---

## 14. Contribuições, turnover e custos

| ticker | segmento | contribuicao | peso_medio |
| --- | --- | --- | --- |
| NG=F | Commodities | 15,57% | 8,33% |
| GC=F | Commodities | 9,82% | 8,33% |
| MATB11.SA | Renda Variável | 5,95% | 8,33% |
| BOVV11.SA | Renda Variável | 4,86% | 8,33% |
| FIND11.SA | Renda Variável | 4,57% | 8,33% |
| IMAB11.SA | Renda Fixa | 3,84% | 8,33% |
| ZC=F | Commodities | 3,00% | 8,33% |
| B5MB11.SA | Renda Fixa | 2,70% | 8,33% |
| EURBRL=X | Moedas | 2,64% | 8,33% |
| USDBRL=X | Moedas | 2,42% | 8,33% |
| IB5M11.SA | Renda Fixa | 2,38% | 8,33% |
| JPYBRL=X | Moedas | -0,75% | 8,33% |

### Comparação de turnover e custos por bloco

| Período | Turnover total | Custo total |
| --- | --- | --- |
| Desenvolvimento e calibração | 219,69% | 0,22% |
| Validação | 44,01% | 0,04% |
| Teste final fora da amostra | 12,73% | 0,01% |

---

## 15. Otimização e walk-forward

### Métricas finais já produzidas pelo pipeline

| periodo | data_inicial | data_final | cenario | rotulo | quantidade_meses | retorno_total_bruto | retorno_total_liquido | retorno_anualizado_liquido | volatilidade_anualizada_liquida | retorno_volatilidade | sharpe_excesso_cdi | sortino_excesso_cdi | calmar | maximo_drawdown | meses_positivos | melhor_mes | pior_mes | turnover_total | turnover_medio_mensal | custo_acumulado_simples | indice_final_liquido | diferenca_indice_vs_benchmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WALK_FORWARD_OOS | 2024-01-31 | 2026-05-31 | WALK_FORWARD | Modelo walk-forward | 29 | 0.3205019208778228 | 0.3196629481503703 | 0.1216226433424276 | 0.0484875291036367 | 2.5083283390760656 | -0.1049655992784551 | -0.1673750940879433 | 5.357093940217334 | -0.0227031007295521 | 0.8620689655172413 | 0.0566567844118466 | -0.0179516728737971 | 0.6355267972425722 | 0.0219147171462955 | 0.0006355267972425 | 131.96629481503703 | 3.1701706938942777 |
| WALK_FORWARD_OOS | 2024-01-31 | 2026-05-31 | MODELO_FIXO_CELULA_9 | Modelo fixo da Célula 9 | 29 | 0.3196290824056769 | 0.3189022206637757 | 0.1213550535783392 | 0.0524732890824183 | 2.312701484897016 | -0.0980966679881078 | -0.1624973395844905 | 5.345307454869976 | -0.0227031007295521 | 0.7931034482758621 | 0.0642696004953939 | -0.0179516728737971 | 0.5509456710095276 | 0.0189981265865354 | 0.0005509456710095 | 131.89022206637756 | 3.0940979452348074 |
| WALK_FORWARD_OOS | 2024-01-31 | 2026-05-31 | MODELO_ANTERIOR_SEM_CDI | Modelo anterior sem CDI | 29 | 0.2837798425110196 | 0.2830515983295576 | 0.1086403246834308 | 0.0814442627155637 | 1.3339223790734869 | -0.1816683180172291 | -0.2814742467202838 | 2.205183108134672 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.5674200230987332 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295575 | -0.4909642881870013 |
| WALK_FORWARD_OOS | 2024-01-31 | 2026-05-31 | BENCHMARK_5_ATIVOS | Benchmark de pesos iguais | 29 | 0.2886532397636245 | 0.2879612412114276 | 0.1103937744137797 | 0.075185248915226 | 1.4682903362899349 | -0.1817411580905756 | -0.281581341632256 | 2.4985737797089094 | -0.0441827154796449 | 0.6551724137931034 | 0.0810413030709897 | -0.0328216019121329 | 0.5371319306277863 | 0.0185217907113029 | 0.0005371319306277 | 128.79612412114275 | 0.0 |
| WALK_FORWARD_OOS | 2024-01-31 | 2026-05-31 | CARTEIRA_ESTATICA | Carteira estática | 29 | 0.3080682907860192 | 0.307558836471981 | 0.1173541797814363 | 0.0489366605750817 | 2.398083122189837 | -0.1820809519662244 | -0.2820808388884011 | 5.169081579622239 | -0.0227031007295521 | 0.7931034482758621 | 0.0567512744995997 | -0.0179516728737971 | 0.3895433918334091 | 0.0134325307528761 | 0.0003895433918334 | 130.7558836471981 | 1.959759526055336 |
| WALK_FORWARD_OOS | 2024-01-31 | 2026-05-31 | CDI_100 | 100% CDI | 29 | 0.3393334023744503 | 0.3393334023744503 | 0.1285106682782399 | 0.005293250328511 | 24.27821476457359 | 4.620634699064077 | inf | nan | 0.0 | 1.0 | 0.0127573250874795 | 0.0078833696783628 | 0.0 | 0.0 | 0.0 | 133.93334023744504 | 5.137216116302284 |

### Pesos oficiais já produzidos pelo pipeline

| regime | numero_recalibracao | data_final_treino | data_inicial_aplicacao | data_final_aplicacao | nome_regime | meses_confirmacao | peso_NG=F | peso_ZC=F | peso_GC=F | peso_USDBRL=X | peso_EURBRL=X | peso_JPYBRL=X | peso_IMAB11.SA | peso_B5MB11.SA | peso_IB5M11.SA | peso_BOVV11.SA | peso_FIND11.SA | peso_MATB11.SA | peso_CDI | soma_pesos | soma_pesos_recalculada |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | 3 | 2025-12-31 | 2026-01-31 | 2026-05-31 | Expansão desinflacionária | 2 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.5 | 1.0 | 0.9999999999999992 |
| EXPANSAO_INFLACIONARIA | 3 | 2025-12-31 | 2026-01-31 | 2026-05-31 | Expansão inflacionária | 2 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.4 | 1.0 | 1.0 |
| ESTAGFLACAO | 3 | 2025-12-31 | 2026-01-31 | 2026-05-31 | Estagflação | 2 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.0416666666666666 | 0.5 | 1.0 | 0.9999999999999992 |
| RECESSAO_DESINFLACIONARIA | 3 | 2025-12-31 | 2026-01-31 | 2026-05-31 | Recessão desinflacionária | 2 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.4 | 1.0 | 1.0 |

### Scorecard existente

_Nenhum dado disponível._

> A recalibração walk-forward é anual, com treino inicial de 48 meses e janela expansiva. Arquivos anteriores às bases centrais atuais devem ser tratados como resultados de uma execução anterior.

---

## 16. Modelo final

### alocacoes_iniciais_automaticas.json

Caminho: `outputs/modelo_final/alocacoes_iniciais_automaticas.json`

```json
{
  "metodo": "PESOS_IGUAIS_ENTRE_ATIVOS_SELECIONADOS",
  "provisorio": true,
  "quantidade_ativos": 12,
  "peso_individual": 0.08333333333333333,
  "ativos_selecionados": [
    "NG=F",
    "ZC=F",
    "GC=F",
    "USDBRL=X",
    "EURBRL=X",
    "JPYBRL=X",
    "IMAB11.SA",
    "B5MB11.SA",
    "IB5M11.SA",
    "BOVV11.SA",
    "FIND11.SA",
    "MATB11.SA"
  ],
  "pesos_por_regime": {
    "EXPANSAO_DESINFLACIONARIA": {
      "NG=F": 0.08333333333333333,
      "ZC=F": 0.08333333333333333,
      "GC=F": 0.08333333333333333,
      "USDBRL=X": 0.08333333333333333,
      "EURBRL=X": 0.08333333333333333,
      "JPYBRL=X": 0.08333333333333333,
      "IMAB11.SA": 0.08333333333333333,
      "B5MB11.SA": 0.08333333333333333,
      "IB5M11.SA": 0.08333333333333333,
      "BOVV11.SA": 0.08333333333333333,
      "FIND11.SA": 0.08333333333333333,
      "MATB11.SA": 0.08333333333333333
    },
    "EXPANSAO_INFLACIONARIA": {
      "NG=F": 0.08333333333333333,
      "ZC=F": 0.08333333333333333,
      "GC=F": 0.08333333333333333,
      "USDBRL=X": 0.08333333333333333,
      "EURBRL=X": 0.08333333333333333,
      "JPYBRL=X": 0.08333333333333333,
      "IMAB11.SA": 0.08333333333333333,
      "B5MB11.SA": 0.08333333333333333,
      "IB5M11.SA": 0.08333333333333333,
      "BOVV11.SA": 0.08333333333333333,
      "FIND11.SA": 0.08333333333333333,
      "MATB11.SA": 0.08333333333333333
    },
    "ESTAGFLACAO": {
      "NG=F": 0.08333333333333333,
      "ZC=F": 0.08333333333333333,
      "GC=F": 0.08333333333333333,
      "USDBRL=X": 0.08333333333333333,
      "EURBRL=X": 0.08333333333333333,
      "JPYBRL=X": 0.08333333333333333,
      "IMAB11.SA": 0.08333333333333333,
      "B5MB11.SA": 0.08333333333333333,
      "IB5M11.SA": 0.08333333333333333,
      "BOVV11.SA": 0.08333333333333333,
      "FIND11.SA": 0.08333333333333333,
      "MATB11.SA": 0.08333333333333333
    },
    "RECESSAO_DESINFLACIONARIA": {
      "NG=F": 0.08333333333333333,
      "ZC=F": 0.08333333333333333,
      "GC=F": 0.08333333333333333,
      "USDBRL=X": 0.08333333333333333,
      "EURBRL=X": 0.08333333333333333,
      "JPYBRL=X": 0.08333333333333333,
      "IMAB11.SA": 0.08333333333333333,
      "B5MB11.SA": 0.08333333333333333,
      "IB5M11.SA": 0.08333333333333333,
      "BOVV11.SA": 0.08333333333333333,
      "FIND11.SA": 0.08333333333333333,
      "MATB11.SA": 0.08333333333333333
    }
  },
  "observacao": "Pesos iniciais gerados automaticamente. A etapa 06 deve otimizar os pesos finais."
}
```

### manifesto_arquivos.csv

Caminho: `outputs/modelo_final/manifesto_arquivos.csv`

| arquivo | tipo | tamanho_bytes | sha256 |
| --- | --- | --- | --- |
| outputs\tabelas\06_11_resumo_walk_forward.csv | ENTRADA | 1999 | 6adffa19d893d4542c0551cd3c4d2db9fccca63cc9ab4339d26796e24ac5c7a6 |
| outputs\tabelas\06_11_parametros_por_recalibracao.csv | ENTRADA | 1006 | 0eb14a196a15caac4fe10f76d2c4852687bd122b087e79ddfa6d44b6daab46be |
| outputs\tabelas\06_11_pesos_por_recalibracao.csv | ENTRADA | 3227 | 819993dd3c343bfb8f32c9a3fa79889bbfa0e55e71fa20482edbe615a52c8dec |
| outputs\tabelas\06_11_estabilidade_parametros.csv | ENTRADA | 665 | 9684babce93745d53fd22aa279fda173411adc17341a6986764ec2ee1bbfb979 |
| outputs\tabelas\06_11_series_walk_forward.csv | ENTRADA | 74321 | 787f786eba5281384ffc9ecfbacdbc74c761a0267d7ea904baa87206997e41e9 |
| outputs\tabelas\06_11_metricas_comparativas.csv | ENTRADA | 2786 | bd7cfc7f6f2ec3de43df583b5e2e0581e3ae3e53ca766555ca426b623b5f3143 |
| outputs\tabelas\06_11_validacoes.csv | ENTRADA | 591 | 77e45e0384dd3a42b65f98a3ad38a502361f142543e167a9bd7e334407373197 |
| outputs\tabelas\06_10_resumo_final_robustez.csv | ENTRADA | 1559 | a054cacf3ec4065daf7b44048d43ad9221c7190fbb4e841311c1c8bad7b2179f |
| outputs\tabelas\06_09_resumo_otimizacao_cdi.csv | ENTRADA | 947 | 36049a990ae836a9b459408b988806cbd9d3e2bb52ffe7bbbbdcb048d34caa69 |
| outputs\tabelas\06_08_status_fontes_renda_fixa.csv | ENTRADA | 320 | e79a89f150d1a0c454a6c8501f29fd0a1c3bb01bad8c0026a5efe337315b553b |
| data\processed\retornos_ativos_ampliados_mensais.csv | ENTRADA | 19147 | 0fba45958f067dae8b9b89d715e3aaae677326ad65010a0856614064301c6041 |
| outputs\tabelas\06_07_pesos_otimizados_por_regime.csv | ENTRADA | 3178 | a099a45267a8fe4bcb5e3c20cc863f1fd57bafd46331c185c72c03ca5be00042 |
| outputs\tabelas\06_12_decisao_final_modelo.csv | SAIDA | 884 | cd895d2e4cb4fd8c84553d1f6cabb6cd8c0b466eea94e4d24e10cc9bcfeefacb |
| outputs\tabelas\06_12_configuracao_modelo_oficial.csv | SAIDA | 1255 | 31aa96671fcd104b75b0d2121612e7a65ffd036e4e9ceab40eda162ed07a8486 |
| outputs\tabelas\06_12_pesos_oficiais_atuais.csv | SAIDA | 1316 | 9f72299b5e8c955771e2f2069d7dbecda1c53a7c26e3e6e753068252a5008f9e |
| outputs\tabelas\06_12_metricas_finais_modelos.csv | SAIDA | 2705 | 419a7c9dcc71b818ba4d9434800424c3407340a6e200e32bfa93589ece32fdbd |
| outputs\tabelas\06_12_metricas_finais_modelos_formatadas.csv | SAIDA | 1617 | b3d067ff4116ae5ba52801e1186f47d89ab6506179ad3a6de32c8adc03d91c8b |
| outputs\tabelas\06_12_series_modelos_finais.csv | SAIDA | 34101 | ae52e3fae6de7cfb8f98477ad3231f9ddd6ccfcadb24aec2872500559e24907e |
| outputs\tabelas\06_12_limitacoes_metodologicas.csv | SAIDA | 1215 | 836d87253d76e5c9f89e8fa05aa1508bd63345acfe8de0bca1f00313ec0bd280 |
| outputs\tabelas\06_12_validacoes_finais.csv | SAIDA | 1166 | 0691b7e946d1b3e03e92cd117cd91a97c77b09ce0794210be717d4cd2a30777d |
| outputs\tabelas\06_12_resumo_modelo_final.csv | SAIDA | 1417 | 707e0505ef957e8038953452abf75b0e5f9e1a258d2b5a00a6c086ec1eeaeb0a |
| outputs\modelo_final\modelo_oficial.json | SAIDA | 4436 | b1d63a3517ac796ba338631887f29750dbef9a88507a9473d8308a7540106a0c |
| outputs\modelo_final\metricas_modelo_oficial.json | SAIDA | 643 | 3eeaaa3e855f7629c450a1bd28a4b96f09d78ed8218326a792a20d7f7a65b5c8 |
| outputs\graficos\06_12_desempenho_modelos_finais.png | SAIDA | 365238 | 938a3b1e9faa18ddccb4e5b7d83eba1e7ea3d3f71808e76b60b08157e59b8b2d |
| outputs\graficos\06_12_drawdown_modelos_finais.png | SAIDA | 343902 | e529966a05e00b8a5752574563ce9c5f4bf1ea55daa1226a03ca4f235b592c76 |
| outputs\graficos\06_12_pesos_oficiais_por_regime.png | SAIDA | 206629 | 420f2c5c4b11ca391eb726b1c46c2246e8eab80307ce00710f79456f140a238d |
| outputs\graficos\06_12_risco_retorno_modelos_finais.png | SAIDA | 160585 | ae1b45159e09f4aa02e55b7352d4bcf8750933a50989e62df305bbf6dc2fda32 |

### metricas_modelo_oficial.json

Caminho: `outputs/modelo_final/metricas_modelo_oficial.json`

```json
{
  "modelo_oficial": "WALK_FORWARD",
  "indice_final": 131.96629481503703,
  "retorno_anualizado": 0.1216226433424276,
  "volatilidade_anualizada": 0.0484875291036367,
  "retorno_volatilidade": 2.5083283390760656,
  "sharpe_excesso_cdi": -0.1049655992784551,
  "sortino_excesso_cdi": -0.1673750940879433,
  "calmar": 5.357093940217334,
  "maximo_drawdown": -0.0227031007295521,
  "turnover_total": 0.6355267972425722,
  "indice_challenger": 128.30515983295575,
  "indice_benchmark": 128.79612412114275,
  "diferenca_vs_challenger": 3.661134982081279,
  "diferenca_vs_benchmark": 3.1701706938942777
}
```

### modelo_oficial.json

Caminho: `outputs/modelo_final/modelo_oficial.json`

```json
{
  "projeto": {
    "nome": "Alocação Quantitativa por Regimes Macroeconômicos",
    "modelo_oficial": "Modelo walk-forward com CDI",
    "modelo_challenger": "Modelo anterior sem CDI",
    "status": "APROVADO PELO WALK-FORWARD"
  },
  "dados": {
    "frequencia": "mensal",
    "ativos": [
      "NG=F",
      "ZC=F",
      "GC=F",
      "USDBRL=X",
      "EURBRL=X",
      "JPYBRL=X",
      "IMAB11.SA",
      "B5MB11.SA",
      "IB5M11.SA",
      "BOVV11.SA",
      "FIND11.SA",
      "MATB11.SA",
      "CDI"
    ],
    "quantidade_ativos": 13,
    "taxa_livre_risco": "CDI",
    "benchmark": "Pesos iguais com rebalanceamento mensal",
    "ima_b_oficial_parcial_incluido": false,
    "imab11_etf_incluido": true,
    "motivo_exclusao_ima_b_oficial": "A série oficial SGS 12466 possui cobertura parcial."
  },
  "metodologia": {
    "tipo_janela_treino": "expansiva",
    "meses_treino_inicial": 48,
    "recalibracao_meses": 12,
    "rebalanceamento": "mensal",
    "custo_por_turnover": 0.001,
    "confirmacoes_testadas": [
      1,
      2,
      3
    ],
    "pesos_cdi_testados": [
      0.0,
      0.1,
      0.2,
      0.3,
      0.4,
      0.5
    ]
  },
  "configuracao_atual": {
    "numero_recalibracao": 3,
    "candidato": "conf_2m_cdi_50_40_50_40",
    "meses_confirmacao": 2,
    "data_final_treino": "2025-12-31",
    "data_inicial_vigencia": "2026-01-31",
    "pesos_por_regime": {
      "EXPANSAO_DESINFLACIONARIA": {
        "NG=F": 0.0416666666666666,
        "ZC=F": 0.0416666666666666,
        "GC=F": 0.0416666666666666,
        "USDBRL=X": 0.0416666666666666,
        "EURBRL=X": 0.0416666666666666,
        "JPYBRL=X": 0.0416666666666666,
        "IMAB11.SA": 0.0416666666666666,
        "B5MB11.SA": 0.0416666666666666,
        "IB5M11.SA": 0.0416666666666666,
        "BOVV11.SA": 0.0416666666666666,
        "FIND11.SA": 0.0416666666666666,
        "MATB11.SA": 0.0416666666666666,
        "CDI": 0.5
      },
      "EXPANSAO_INFLACIONARIA": {
        "NG=F": 0.05,
        "ZC=F": 0.05,
        "GC=F": 0.05,
        "USDBRL=X": 0.05,
        "EURBRL=X": 0.05,
        "JPYBRL=X": 0.05,
        "IMAB11.SA": 0.05,
        "B5MB11.SA": 0.05,
        "IB5M11.SA": 0.05,
        "BOVV11.SA": 0.05,
        "FIND11.SA": 0.05,
        "MATB11.SA": 0.05,
        "CDI": 0.4
      },
      "ESTAGFLACAO": {
        "NG=F": 0.0416666666666666,
        "ZC=F": 0.0416666666666666,
        "GC=F": 0.0416666666666666,
        "USDBRL=X": 0.0416666666666666,
        "EURBRL=X": 0.0416666666666666,
        "JPYBRL=X": 0.0416666666666666,
        "IMAB11.SA": 0.0416666666666666,
        "B5MB11.SA": 0.0416666666666666,
        "IB5M11.SA": 0.0416666666666666,
        "BOVV11.SA": 0.0416666666666666,
        "FIND11.SA": 0.0416666666666666,
        "MATB11.SA": 0.0416666666666666,
        "CDI": 0.5
      },
      "RECESSAO_DESINFLACIONARIA": {
        "NG=F": 0.05,
        "ZC=F": 0.05,
        "GC=F": 0.05,
        "USDBRL=X": 0.05,
        "EURBRL=X": 0.05,
        "JPYBRL=X": 0.05,
        "IMAB11.SA": 0.05,
        "B5MB11.SA": 0.05,
        "IB5M11.SA": 0.05,
        "BOVV11.SA": 0.05,
        "FIND11.SA": 0.05,
        "MATB11.SA": 0.05,
        "CDI": 0.4
      }
    }
  },
  "validacao": {
    "status_walk_forward": "APROVADO",
    "criterios_aprovados": 6,
    "total_criterios": 6,
    "periodo_avaliacao": {
      "inicio": "2024-01-31",
      "fim": "2026-05-31"
    },
    "observacao": "O período de avaliação já foi analisado e não representa um holdout final intocado."
  }
}
```

---

## 17. Auditoria e controles

_Nenhum dado disponível._

---

## 18. Janelas móveis e estabilidade

| comparação | janelas | proporção positiva | melhor excesso | pior excesso |
| --- | --- | --- | --- | --- |
| Benchmark | 66 | 0,00% | 0,00% | 0,00% |
| CDI | 66 | 34,85% | 35,27% | -20,39% |

---

## 19. Gráficos oficiais do pipeline

Os gráficos abaixo foram copiados de `outputs/graficos` para a pasta desta execução. A situação temporal informa se o arquivo parece pertencer à mesma execução das bases centrais.

| etapa | arquivo | origem | copia_relatorio | modificacao_utc | status_atualizacao |
| --- | --- | --- | --- | --- | --- |
| Etapa 01 — Coleta e qualidade | 01_atualizacao_series_macro.png | outputs/graficos/01_atualizacao_series_macro.png | graficos_pipeline/01_atualizacao_series_macro.png | 2026-08-04 23:57:25.550895+00:00 | Mesma execução provável |
| Etapa 01 — Coleta e qualidade | 01_cobertura_dados_ativos.png | outputs/graficos/01_cobertura_dados_ativos.png | graficos_pipeline/01_cobertura_dados_ativos.png | 2026-08-04 23:57:25.354205+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_08_precos_normalizados_commodities.png | outputs/graficos/02_08_precos_normalizados_commodities.png | graficos_pipeline/02_08_precos_normalizados_commodities.png | 2026-08-04 23:57:33.118711+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_08_precos_normalizados_moedas.png | outputs/graficos/02_08_precos_normalizados_moedas.png | graficos_pipeline/02_08_precos_normalizados_moedas.png | 2026-08-04 23:57:36.934587+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_08_precos_normalizados_renda_fixa.png | outputs/graficos/02_08_precos_normalizados_renda_fixa.png | graficos_pipeline/02_08_precos_normalizados_renda_fixa.png | 2026-08-04 23:57:39.031750+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_08_precos_normalizados_renda_variavel.png | outputs/graficos/02_08_precos_normalizados_renda_variavel.png | graficos_pipeline/02_08_precos_normalizados_renda_variavel.png | 2026-08-04 23:57:35.299289+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_09_retorno_acumulado_commodities.png | outputs/graficos/02_09_retorno_acumulado_commodities.png | graficos_pipeline/02_09_retorno_acumulado_commodities.png | 2026-08-04 23:57:33.466736+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_09_retorno_acumulado_moedas.png | outputs/graficos/02_09_retorno_acumulado_moedas.png | graficos_pipeline/02_09_retorno_acumulado_moedas.png | 2026-08-04 23:57:37.296515+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_09_retorno_acumulado_renda_fixa.png | outputs/graficos/02_09_retorno_acumulado_renda_fixa.png | graficos_pipeline/02_09_retorno_acumulado_renda_fixa.png | 2026-08-04 23:57:39.328785+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_09_retorno_acumulado_renda_variavel.png | outputs/graficos/02_09_retorno_acumulado_renda_variavel.png | graficos_pipeline/02_09_retorno_acumulado_renda_variavel.png | 2026-08-04 23:57:35.636702+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_10_volatilidade_movel_commodities.png | outputs/graficos/02_10_volatilidade_movel_commodities.png | graficos_pipeline/02_10_volatilidade_movel_commodities.png | 2026-08-04 23:57:33.803672+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_10_volatilidade_movel_moedas.png | outputs/graficos/02_10_volatilidade_movel_moedas.png | graficos_pipeline/02_10_volatilidade_movel_moedas.png | 2026-08-04 23:57:37.766464+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_10_volatilidade_movel_renda_fixa.png | outputs/graficos/02_10_volatilidade_movel_renda_fixa.png | graficos_pipeline/02_10_volatilidade_movel_renda_fixa.png | 2026-08-04 23:57:39.626209+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_10_volatilidade_movel_renda_variavel.png | outputs/graficos/02_10_volatilidade_movel_renda_variavel.png | graficos_pipeline/02_10_volatilidade_movel_renda_variavel.png | 2026-08-04 23:57:35.983550+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_11_drawdown_ativos_commodities.png | outputs/graficos/02_11_drawdown_ativos_commodities.png | graficos_pipeline/02_11_drawdown_ativos_commodities.png | 2026-08-04 23:57:34.232621+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_11_drawdown_ativos_moedas.png | outputs/graficos/02_11_drawdown_ativos_moedas.png | graficos_pipeline/02_11_drawdown_ativos_moedas.png | 2026-08-04 23:57:38.364299+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_11_drawdown_ativos_renda_fixa.png | outputs/graficos/02_11_drawdown_ativos_renda_fixa.png | graficos_pipeline/02_11_drawdown_ativos_renda_fixa.png | 2026-08-04 23:57:39.925101+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_11_drawdown_ativos_renda_variavel.png | outputs/graficos/02_11_drawdown_ativos_renda_variavel.png | graficos_pipeline/02_11_drawdown_ativos_renda_variavel.png | 2026-08-04 23:57:36.311420+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_12_correlacao_retornos_commodities.png | outputs/graficos/02_12_correlacao_retornos_commodities.png | graficos_pipeline/02_12_correlacao_retornos_commodities.png | 2026-08-04 23:57:34.813688+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_12_correlacao_retornos_consolidada.png | outputs/graficos/02_12_correlacao_retornos_consolidada.png | graficos_pipeline/02_12_correlacao_retornos_consolidada.png | 2026-08-04 23:57:41.204377+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_12_correlacao_retornos_moedas.png | outputs/graficos/02_12_correlacao_retornos_moedas.png | graficos_pipeline/02_12_correlacao_retornos_moedas.png | 2026-08-04 23:57:38.727095+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_12_correlacao_retornos_renda_fixa.png | outputs/graficos/02_12_correlacao_retornos_renda_fixa.png | graficos_pipeline/02_12_correlacao_retornos_renda_fixa.png | 2026-08-04 23:57:40.321867+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_12_correlacao_retornos_renda_variavel.png | outputs/graficos/02_12_correlacao_retornos_renda_variavel.png | graficos_pipeline/02_12_correlacao_retornos_renda_variavel.png | 2026-08-04 23:57:36.603809+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_13_ipca_12_meses.png | outputs/graficos/02_13_ipca_12_meses.png | graficos_pipeline/02_13_ipca_12_meses.png | 2026-08-04 23:57:41.433500+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_14_ibc_br_dessazonalizado.png | outputs/graficos/02_14_ibc_br_dessazonalizado.png | graficos_pipeline/02_14_ibc_br_dessazonalizado.png | 2026-08-04 23:57:41.672162+00:00 | Mesma execução provável |
| Etapa 02 — Análise exploratória | 02_15_tendencias_inflacao_crescimento.png | outputs/graficos/02_15_tendencias_inflacao_crescimento.png | graficos_pipeline/02_15_tendencias_inflacao_crescimento.png | 2026-08-04 23:57:42.009839+00:00 | Mesma execução provável |
| Etapa 04 — Alocação | 04_desempenho_acumulado_bruto.png | outputs/graficos/04_desempenho_acumulado_bruto.png | graficos_pipeline/04_desempenho_acumulado_bruto.png | 2026-08-05 00:06:12.609282+00:00 | Mesma execução provável |
| Etapa 04 — Alocação | 04_diferenca_carteiras.png | outputs/graficos/04_diferenca_carteiras.png | graficos_pipeline/04_diferenca_carteiras.png | 2026-08-05 00:06:13.090356+00:00 | Mesma execução provável |
| Etapa 04 — Alocação | 04_drawdown_carteiras.png | outputs/graficos/04_drawdown_carteiras.png | graficos_pipeline/04_drawdown_carteiras.png | 2026-08-05 00:06:12.846852+00:00 | Mesma execução provável |
| Etapa 05 — Backtest | 05_contribuicao_media_por_regime.png | outputs/graficos/05_contribuicao_media_por_regime.png | graficos_pipeline/05_contribuicao_media_por_regime.png | 2026-08-05 00:06:55.537318+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_desempenho_bruto_liquido.png | outputs/graficos/05_desempenho_bruto_liquido.png | graficos_pipeline/05_desempenho_bruto_liquido.png | 2026-08-05 00:06:53.806908+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_drawdown_liquido.png | outputs/graficos/05_drawdown_liquido.png | graficos_pipeline/05_drawdown_liquido.png | 2026-08-05 00:06:54.113154+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_impacto_acumulado_custos.png | outputs/graficos/05_impacto_acumulado_custos.png | graficos_pipeline/05_impacto_acumulado_custos.png | 2026-08-05 00:06:54.455203+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_indice_final_por_custo.png | outputs/graficos/05_indice_final_por_custo.png | graficos_pipeline/05_indice_final_por_custo.png | 2026-08-05 00:06:55.777477+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_retorno_liquido_medio_por_regime.png | outputs/graficos/05_retorno_liquido_medio_por_regime.png | graficos_pipeline/05_retorno_liquido_medio_por_regime.png | 2026-08-05 00:06:55.109845+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_retorno_movel_12m.png | outputs/graficos/05_retorno_movel_12m.png | graficos_pipeline/05_retorno_movel_12m.png | 2026-08-05 00:06:56.452894+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_retornos_liquidos_anuais.png | outputs/graficos/05_retornos_liquidos_anuais.png | graficos_pipeline/05_retornos_liquidos_anuais.png | 2026-08-05 00:06:56.191447+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_turnover_mensal.png | outputs/graficos/05_turnover_mensal.png | graficos_pipeline/05_turnover_mensal.png | 2026-08-05 00:06:54.755093+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_vantagem_liquida_por_custo.png | outputs/graficos/05_vantagem_liquida_por_custo.png | graficos_pipeline/05_vantagem_liquida_por_custo.png | 2026-08-05 00:06:55.987801+00:00 | Atual ou posterior às bases centrais |
| Etapa 05 — Backtest | 05_volatilidade_movel_12m.png | outputs/graficos/05_volatilidade_movel_12m.png | graficos_pipeline/05_volatilidade_movel_12m.png | 2026-08-05 00:06:56.737875+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_02_mudancas_regime_por_confirmacao.png | outputs/graficos/06_02_mudancas_regime_por_confirmacao.png | graficos_pipeline/06_02_mudancas_regime_por_confirmacao.png | 2026-08-05 00:07:53.882444+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_02_series_regimes_suavizados.png | outputs/graficos/06_02_series_regimes_suavizados.png | graficos_pipeline/06_02_series_regimes_suavizados.png | 2026-08-05 00:07:54.909217+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_03_desempenho_liquido_regimes_suavizados.png | outputs/graficos/06_03_desempenho_liquido_regimes_suavizados.png | graficos_pipeline/06_03_desempenho_liquido_regimes_suavizados.png | 2026-08-05 00:07:56.844985+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_03_diferenca_liquida_vs_benchmark.png | outputs/graficos/06_03_diferenca_liquida_vs_benchmark.png | graficos_pipeline/06_03_diferenca_liquida_vs_benchmark.png | 2026-08-05 00:07:58.798142+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_03_turnover_regimes_suavizados.png | outputs/graficos/06_03_turnover_regimes_suavizados.png | graficos_pipeline/06_03_turnover_regimes_suavizados.png | 2026-08-05 00:07:57.995264+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_04_desempenho_fora_amostra.png | outputs/graficos/06_04_desempenho_fora_amostra.png | graficos_pipeline/06_04_desempenho_fora_amostra.png | 2026-08-05 00:07:59.745801+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_04_diferenca_fora_amostra.png | outputs/graficos/06_04_diferenca_fora_amostra.png | graficos_pipeline/06_04_diferenca_fora_amostra.png | 2026-08-05 00:08:00.506178+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_05_desempenho_teste_pesos_otimizados.png | outputs/graficos/06_05_desempenho_teste_pesos_otimizados.png | graficos_pipeline/06_05_desempenho_teste_pesos_otimizados.png | 2026-08-05 00:08:03.871926+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_05_diferenca_teste_pesos_otimizados.png | outputs/graficos/06_05_diferenca_teste_pesos_otimizados.png | graficos_pipeline/06_05_diferenca_teste_pesos_otimizados.png | 2026-08-05 00:08:04.331409+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_05_retorno_volatilidade_treino.png | outputs/graficos/06_05_retorno_volatilidade_treino.png | graficos_pipeline/06_05_retorno_volatilidade_treino.png | 2026-08-05 00:08:03.328991+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_06_contribuicao_ativos_teste.png | outputs/graficos/06_06_contribuicao_ativos_teste.png | graficos_pipeline/06_06_contribuicao_ativos_teste.png | 2026-08-05 00:08:06.279632+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_06_excesso_retorno_por_regime.png | outputs/graficos/06_06_excesso_retorno_por_regime.png | graficos_pipeline/06_06_excesso_retorno_por_regime.png | 2026-08-05 00:08:05.586385+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_06_turnover_por_regime.png | outputs/graficos/06_06_turnover_por_regime.png | graficos_pipeline/06_06_turnover_por_regime.png | 2026-08-05 00:08:06.773776+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_07_comparacao_pesos_por_regime.png | outputs/graficos/06_07_comparacao_pesos_por_regime.png | graficos_pipeline/06_07_comparacao_pesos_por_regime.png | 2026-08-05 00:08:12.494326+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_07_desempenho_periodo_avaliacao.png | outputs/graficos/06_07_desempenho_periodo_avaliacao.png | graficos_pipeline/06_07_desempenho_periodo_avaliacao.png | 2026-08-05 00:08:10.831053+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_07_diferenca_vs_benchmark_avaliacao.png | outputs/graficos/06_07_diferenca_vs_benchmark_avaliacao.png | graficos_pipeline/06_07_diferenca_vs_benchmark_avaliacao.png | 2026-08-05 00:08:11.262910+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_08_cdi_acumulado.png | outputs/graficos/06_08_cdi_acumulado.png | graficos_pipeline/06_08_cdi_acumulado.png | 2026-08-05 00:08:12.786564+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_09_desempenho_avaliacao_cdi.png | outputs/graficos/06_09_desempenho_avaliacao_cdi.png | graficos_pipeline/06_09_desempenho_avaliacao_cdi.png | 2026-08-05 00:08:23.083692+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_09_diferenca_vs_benchmark_5_ativos.png | outputs/graficos/06_09_diferenca_vs_benchmark_5_ativos.png | graficos_pipeline/06_09_diferenca_vs_benchmark_5_ativos.png | 2026-08-05 00:08:23.615837+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_09_excesso_rolling_12m_treino.png | outputs/graficos/06_09_excesso_rolling_12m_treino.png | graficos_pipeline/06_09_excesso_rolling_12m_treino.png | 2026-08-05 00:08:24.733412+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_09_pesos_cdi_por_regime.png | outputs/graficos/06_09_pesos_cdi_por_regime.png | graficos_pipeline/06_09_pesos_cdi_por_regime.png | 2026-08-05 00:08:24.118814+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_10_desempenho_comparadores_avaliacao.png | outputs/graficos/06_10_desempenho_comparadores_avaliacao.png | graficos_pipeline/06_10_desempenho_comparadores_avaliacao.png | 2026-08-05 00:08:28.507977+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_10_diferenca_modelo_vs_referencias.png | outputs/graficos/06_10_diferenca_modelo_vs_referencias.png | graficos_pipeline/06_10_diferenca_modelo_vs_referencias.png | 2026-08-05 00:08:29.372469+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_10_distribuicao_sensibilidade_vs_benchmark.png | outputs/graficos/06_10_distribuicao_sensibilidade_vs_benchmark.png | graficos_pipeline/06_10_distribuicao_sensibilidade_vs_benchmark.png | 2026-08-05 00:08:29.793738+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_10_risco_retorno_avaliacao.png | outputs/graficos/06_10_risco_retorno_avaliacao.png | graficos_pipeline/06_10_risco_retorno_avaliacao.png | 2026-08-05 00:08:28.892311+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_10_rolling_12m_avaliacao.png | outputs/graficos/06_10_rolling_12m_avaliacao.png | graficos_pipeline/06_10_rolling_12m_avaliacao.png | 2026-08-05 00:08:30.349034+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_11_confirmacao_por_recalibracao.png | outputs/graficos/06_11_confirmacao_por_recalibracao.png | graficos_pipeline/06_11_confirmacao_por_recalibracao.png | 2026-08-05 00:09:01.508631+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_11_desempenho_walk_forward.png | outputs/graficos/06_11_desempenho_walk_forward.png | graficos_pipeline/06_11_desempenho_walk_forward.png | 2026-08-05 00:09:00.517763+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_11_diferenca_walk_forward.png | outputs/graficos/06_11_diferenca_walk_forward.png | graficos_pipeline/06_11_diferenca_walk_forward.png | 2026-08-05 00:09:01.154644+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_11_pesos_cdi_por_recalibracao.png | outputs/graficos/06_11_pesos_cdi_por_recalibracao.png | graficos_pipeline/06_11_pesos_cdi_por_recalibracao.png | 2026-08-05 00:09:02.068937+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_11_rolling_12m_walk_forward.png | outputs/graficos/06_11_rolling_12m_walk_forward.png | graficos_pipeline/06_11_rolling_12m_walk_forward.png | 2026-08-05 00:09:02.615050+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_12_desempenho_modelos_finais.png | outputs/graficos/06_12_desempenho_modelos_finais.png | graficos_pipeline/06_12_desempenho_modelos_finais.png | 2026-08-05 00:09:03.578705+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_12_drawdown_modelos_finais.png | outputs/graficos/06_12_drawdown_modelos_finais.png | graficos_pipeline/06_12_drawdown_modelos_finais.png | 2026-08-05 00:09:04.217175+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_12_pesos_oficiais_por_regime.png | outputs/graficos/06_12_pesos_oficiais_por_regime.png | graficos_pipeline/06_12_pesos_oficiais_por_regime.png | 2026-08-05 00:09:04.728958+00:00 | Atual ou posterior às bases centrais |
| Etapa 06 — Otimização e walk-forward | 06_12_risco_retorno_modelos_finais.png | outputs/graficos/06_12_risco_retorno_modelos_finais.png | graficos_pipeline/06_12_risco_retorno_modelos_finais.png | 2026-08-05 00:09:05.113267+00:00 | Atual ou posterior às bases centrais |
| Etapa 07 — Análise final | 07_02_desempenho_acumulado.png | outputs/graficos/07_02_desempenho_acumulado.png | graficos_pipeline/07_02_desempenho_acumulado.png | 2026-08-05 00:10:10.890647+00:00 | Atual ou posterior às bases centrais |
| Etapa 07 — Análise final | 07_02_drawdown_comparativo.png | outputs/graficos/07_02_drawdown_comparativo.png | graficos_pipeline/07_02_drawdown_comparativo.png | 2026-08-05 00:10:13.001571+00:00 | Atual ou posterior às bases centrais |
| Etapa 07 — Análise final | 07_02_retornos_anuais.png | outputs/graficos/07_02_retornos_anuais.png | graficos_pipeline/07_02_retornos_anuais.png | 2026-08-05 00:10:11.348080+00:00 | Atual ou posterior às bases centrais |
| Etapa 07 — Análise final | 07_02_risco_retorno.png | outputs/graficos/07_02_risco_retorno.png | graficos_pipeline/07_02_risco_retorno.png | 2026-08-05 00:10:12.133954+00:00 | Atual ou posterior às bases centrais |

### Etapa 01 — Coleta e qualidade

#### 01_atualizacao_series_macro

![01_atualizacao_series_macro](graficos_pipeline/01_atualizacao_series_macro.png)

#### 01_cobertura_dados_ativos

![01_cobertura_dados_ativos](graficos_pipeline/01_cobertura_dados_ativos.png)

### Etapa 02 — Análise exploratória

#### 02_08_precos_normalizados_commodities

![02_08_precos_normalizados_commodities](graficos_pipeline/02_08_precos_normalizados_commodities.png)

#### 02_08_precos_normalizados_moedas

![02_08_precos_normalizados_moedas](graficos_pipeline/02_08_precos_normalizados_moedas.png)

#### 02_08_precos_normalizados_renda_fixa

![02_08_precos_normalizados_renda_fixa](graficos_pipeline/02_08_precos_normalizados_renda_fixa.png)

#### 02_08_precos_normalizados_renda_variavel

![02_08_precos_normalizados_renda_variavel](graficos_pipeline/02_08_precos_normalizados_renda_variavel.png)

#### 02_09_retorno_acumulado_commodities

![02_09_retorno_acumulado_commodities](graficos_pipeline/02_09_retorno_acumulado_commodities.png)

#### 02_09_retorno_acumulado_moedas

![02_09_retorno_acumulado_moedas](graficos_pipeline/02_09_retorno_acumulado_moedas.png)

#### 02_09_retorno_acumulado_renda_fixa

![02_09_retorno_acumulado_renda_fixa](graficos_pipeline/02_09_retorno_acumulado_renda_fixa.png)

#### 02_09_retorno_acumulado_renda_variavel

![02_09_retorno_acumulado_renda_variavel](graficos_pipeline/02_09_retorno_acumulado_renda_variavel.png)

#### 02_10_volatilidade_movel_commodities

![02_10_volatilidade_movel_commodities](graficos_pipeline/02_10_volatilidade_movel_commodities.png)

#### 02_10_volatilidade_movel_moedas

![02_10_volatilidade_movel_moedas](graficos_pipeline/02_10_volatilidade_movel_moedas.png)

#### 02_10_volatilidade_movel_renda_fixa

![02_10_volatilidade_movel_renda_fixa](graficos_pipeline/02_10_volatilidade_movel_renda_fixa.png)

#### 02_10_volatilidade_movel_renda_variavel

![02_10_volatilidade_movel_renda_variavel](graficos_pipeline/02_10_volatilidade_movel_renda_variavel.png)

#### 02_11_drawdown_ativos_commodities

![02_11_drawdown_ativos_commodities](graficos_pipeline/02_11_drawdown_ativos_commodities.png)

#### 02_11_drawdown_ativos_moedas

![02_11_drawdown_ativos_moedas](graficos_pipeline/02_11_drawdown_ativos_moedas.png)

#### 02_11_drawdown_ativos_renda_fixa

![02_11_drawdown_ativos_renda_fixa](graficos_pipeline/02_11_drawdown_ativos_renda_fixa.png)

#### 02_11_drawdown_ativos_renda_variavel

![02_11_drawdown_ativos_renda_variavel](graficos_pipeline/02_11_drawdown_ativos_renda_variavel.png)

#### 02_12_correlacao_retornos_commodities

![02_12_correlacao_retornos_commodities](graficos_pipeline/02_12_correlacao_retornos_commodities.png)

#### 02_12_correlacao_retornos_consolidada

![02_12_correlacao_retornos_consolidada](graficos_pipeline/02_12_correlacao_retornos_consolidada.png)

#### 02_12_correlacao_retornos_moedas

![02_12_correlacao_retornos_moedas](graficos_pipeline/02_12_correlacao_retornos_moedas.png)

#### 02_12_correlacao_retornos_renda_fixa

![02_12_correlacao_retornos_renda_fixa](graficos_pipeline/02_12_correlacao_retornos_renda_fixa.png)

#### 02_12_correlacao_retornos_renda_variavel

![02_12_correlacao_retornos_renda_variavel](graficos_pipeline/02_12_correlacao_retornos_renda_variavel.png)

#### 02_13_ipca_12_meses

![02_13_ipca_12_meses](graficos_pipeline/02_13_ipca_12_meses.png)

#### 02_14_ibc_br_dessazonalizado

![02_14_ibc_br_dessazonalizado](graficos_pipeline/02_14_ibc_br_dessazonalizado.png)

#### 02_15_tendencias_inflacao_crescimento

![02_15_tendencias_inflacao_crescimento](graficos_pipeline/02_15_tendencias_inflacao_crescimento.png)

### Etapa 04 — Alocação

#### 04_desempenho_acumulado_bruto

![04_desempenho_acumulado_bruto](graficos_pipeline/04_desempenho_acumulado_bruto.png)

#### 04_diferenca_carteiras

![04_diferenca_carteiras](graficos_pipeline/04_diferenca_carteiras.png)

#### 04_drawdown_carteiras

![04_drawdown_carteiras](graficos_pipeline/04_drawdown_carteiras.png)

### Etapa 05 — Backtest

#### 05_contribuicao_media_por_regime

![05_contribuicao_media_por_regime](graficos_pipeline/05_contribuicao_media_por_regime.png)

#### 05_desempenho_bruto_liquido

![05_desempenho_bruto_liquido](graficos_pipeline/05_desempenho_bruto_liquido.png)

#### 05_drawdown_liquido

![05_drawdown_liquido](graficos_pipeline/05_drawdown_liquido.png)

#### 05_impacto_acumulado_custos

![05_impacto_acumulado_custos](graficos_pipeline/05_impacto_acumulado_custos.png)

#### 05_indice_final_por_custo

![05_indice_final_por_custo](graficos_pipeline/05_indice_final_por_custo.png)

#### 05_retorno_liquido_medio_por_regime

![05_retorno_liquido_medio_por_regime](graficos_pipeline/05_retorno_liquido_medio_por_regime.png)

#### 05_retorno_movel_12m

![05_retorno_movel_12m](graficos_pipeline/05_retorno_movel_12m.png)

#### 05_retornos_liquidos_anuais

![05_retornos_liquidos_anuais](graficos_pipeline/05_retornos_liquidos_anuais.png)

#### 05_turnover_mensal

![05_turnover_mensal](graficos_pipeline/05_turnover_mensal.png)

#### 05_vantagem_liquida_por_custo

![05_vantagem_liquida_por_custo](graficos_pipeline/05_vantagem_liquida_por_custo.png)

#### 05_volatilidade_movel_12m

![05_volatilidade_movel_12m](graficos_pipeline/05_volatilidade_movel_12m.png)

### Etapa 06 — Otimização e walk-forward

#### 06_02_mudancas_regime_por_confirmacao

![06_02_mudancas_regime_por_confirmacao](graficos_pipeline/06_02_mudancas_regime_por_confirmacao.png)

#### 06_02_series_regimes_suavizados

![06_02_series_regimes_suavizados](graficos_pipeline/06_02_series_regimes_suavizados.png)

#### 06_03_desempenho_liquido_regimes_suavizados

![06_03_desempenho_liquido_regimes_suavizados](graficos_pipeline/06_03_desempenho_liquido_regimes_suavizados.png)

#### 06_03_diferenca_liquida_vs_benchmark

![06_03_diferenca_liquida_vs_benchmark](graficos_pipeline/06_03_diferenca_liquida_vs_benchmark.png)

#### 06_03_turnover_regimes_suavizados

![06_03_turnover_regimes_suavizados](graficos_pipeline/06_03_turnover_regimes_suavizados.png)

#### 06_04_desempenho_fora_amostra

![06_04_desempenho_fora_amostra](graficos_pipeline/06_04_desempenho_fora_amostra.png)

#### 06_04_diferenca_fora_amostra

![06_04_diferenca_fora_amostra](graficos_pipeline/06_04_diferenca_fora_amostra.png)

#### 06_05_desempenho_teste_pesos_otimizados

![06_05_desempenho_teste_pesos_otimizados](graficos_pipeline/06_05_desempenho_teste_pesos_otimizados.png)

#### 06_05_diferenca_teste_pesos_otimizados

![06_05_diferenca_teste_pesos_otimizados](graficos_pipeline/06_05_diferenca_teste_pesos_otimizados.png)

#### 06_05_retorno_volatilidade_treino

![06_05_retorno_volatilidade_treino](graficos_pipeline/06_05_retorno_volatilidade_treino.png)

#### 06_06_contribuicao_ativos_teste

![06_06_contribuicao_ativos_teste](graficos_pipeline/06_06_contribuicao_ativos_teste.png)

#### 06_06_excesso_retorno_por_regime

![06_06_excesso_retorno_por_regime](graficos_pipeline/06_06_excesso_retorno_por_regime.png)

#### 06_06_turnover_por_regime

![06_06_turnover_por_regime](graficos_pipeline/06_06_turnover_por_regime.png)

#### 06_07_comparacao_pesos_por_regime

![06_07_comparacao_pesos_por_regime](graficos_pipeline/06_07_comparacao_pesos_por_regime.png)

#### 06_07_desempenho_periodo_avaliacao

![06_07_desempenho_periodo_avaliacao](graficos_pipeline/06_07_desempenho_periodo_avaliacao.png)

#### 06_07_diferenca_vs_benchmark_avaliacao

![06_07_diferenca_vs_benchmark_avaliacao](graficos_pipeline/06_07_diferenca_vs_benchmark_avaliacao.png)

#### 06_08_cdi_acumulado

![06_08_cdi_acumulado](graficos_pipeline/06_08_cdi_acumulado.png)

#### 06_09_desempenho_avaliacao_cdi

![06_09_desempenho_avaliacao_cdi](graficos_pipeline/06_09_desempenho_avaliacao_cdi.png)

#### 06_09_diferenca_vs_benchmark_5_ativos

![06_09_diferenca_vs_benchmark_5_ativos](graficos_pipeline/06_09_diferenca_vs_benchmark_5_ativos.png)

#### 06_09_excesso_rolling_12m_treino

![06_09_excesso_rolling_12m_treino](graficos_pipeline/06_09_excesso_rolling_12m_treino.png)

#### 06_09_pesos_cdi_por_regime

![06_09_pesos_cdi_por_regime](graficos_pipeline/06_09_pesos_cdi_por_regime.png)

#### 06_10_desempenho_comparadores_avaliacao

![06_10_desempenho_comparadores_avaliacao](graficos_pipeline/06_10_desempenho_comparadores_avaliacao.png)

#### 06_10_diferenca_modelo_vs_referencias

![06_10_diferenca_modelo_vs_referencias](graficos_pipeline/06_10_diferenca_modelo_vs_referencias.png)

#### 06_10_distribuicao_sensibilidade_vs_benchmark

![06_10_distribuicao_sensibilidade_vs_benchmark](graficos_pipeline/06_10_distribuicao_sensibilidade_vs_benchmark.png)

#### 06_10_risco_retorno_avaliacao

![06_10_risco_retorno_avaliacao](graficos_pipeline/06_10_risco_retorno_avaliacao.png)

#### 06_10_rolling_12m_avaliacao

![06_10_rolling_12m_avaliacao](graficos_pipeline/06_10_rolling_12m_avaliacao.png)

#### 06_11_confirmacao_por_recalibracao

![06_11_confirmacao_por_recalibracao](graficos_pipeline/06_11_confirmacao_por_recalibracao.png)

#### 06_11_desempenho_walk_forward

![06_11_desempenho_walk_forward](graficos_pipeline/06_11_desempenho_walk_forward.png)

#### 06_11_diferenca_walk_forward

![06_11_diferenca_walk_forward](graficos_pipeline/06_11_diferenca_walk_forward.png)

#### 06_11_pesos_cdi_por_recalibracao

![06_11_pesos_cdi_por_recalibracao](graficos_pipeline/06_11_pesos_cdi_por_recalibracao.png)

#### 06_11_rolling_12m_walk_forward

![06_11_rolling_12m_walk_forward](graficos_pipeline/06_11_rolling_12m_walk_forward.png)

#### 06_12_desempenho_modelos_finais

![06_12_desempenho_modelos_finais](graficos_pipeline/06_12_desempenho_modelos_finais.png)

#### 06_12_drawdown_modelos_finais

![06_12_drawdown_modelos_finais](graficos_pipeline/06_12_drawdown_modelos_finais.png)

#### 06_12_pesos_oficiais_por_regime

![06_12_pesos_oficiais_por_regime](graficos_pipeline/06_12_pesos_oficiais_por_regime.png)

#### 06_12_risco_retorno_modelos_finais

![06_12_risco_retorno_modelos_finais](graficos_pipeline/06_12_risco_retorno_modelos_finais.png)

### Etapa 07 — Análise final

#### 07_02_desempenho_acumulado

![07_02_desempenho_acumulado](graficos_pipeline/07_02_desempenho_acumulado.png)

#### 07_02_drawdown_comparativo

![07_02_drawdown_comparativo](graficos_pipeline/07_02_drawdown_comparativo.png)

#### 07_02_retornos_anuais

![07_02_retornos_anuais](graficos_pipeline/07_02_retornos_anuais.png)

#### 07_02_risco_retorno

![07_02_risco_retorno](graficos_pipeline/07_02_risco_retorno.png)

---

## 20. Gráficos adicionais deste relatório

![01_desempenho_acumulado](graficos/01_desempenho_acumulado.png)

![02_drawdown](graficos/02_drawdown.png)

![03_sinais_macro](graficos/03_sinais_macro.png)

![04_regimes](graficos/04_regimes.png)

![05_rolling_12m](graficos/05_rolling_12m.png)

![06_ativos_commodities](graficos/06_ativos_commodities.png)

![07_ativos_moedas](graficos/07_ativos_moedas.png)

![08_ativos_renda_fixa](graficos/08_ativos_renda_fixa.png)

![09_ativos_renda_variavel](graficos/09_ativos_renda_variavel.png)

![01_desenvolvimento_calibracao](graficos_periodos/01_desenvolvimento_calibracao.png)

![02_validacao](graficos_periodos/02_validacao.png)

![03_teste_final_fora_amostra](graficos_periodos/03_teste_final_fora_amostra.png)

---

## 21. Tabelas oficiais do pipeline

Foram selecionadas tabelas relacionadas a métricas, pesos, custos, regimes, otimização, walk-forward, validação e auditoria.

### 01_validacao_ativos.csv

Caminho: `outputs/tabelas/01_validacao_ativos.csv`

| ticker | classe | status | data_inicial | data_final | registros | cobertura | cobertura_pct | nulos_pct | duplicidades | datas_invalidas | precos_nao_positivos | maior_periodo_congelado | maior_intervalo_dias | dias_desatualizado | erros | alertas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B5MB11.SA | RENDA_FIXA_INFLACAO_IMAB5 | ATENCAO | 2020-01-02 | 2026-08-04 | 1640 | 0.954043048283886 | 95.4043048283886 | 0.0 | 0 | 0 | 0 | 913 | 5 | 0 | nan | Sequência elevada de preço congelado |
| IMAB11.SA | RENDA_FIXA_INFLACAO_IMAB | ATENCAO | 2020-01-02 | 2026-08-04 | 1640 | 0.954043048283886 | 95.4043048283886 | 0.0 | 0 | 0 | 0 | 910 | 5 | 0 | nan | Sequência elevada de preço congelado |
| IMBB11.SA | RENDA_FIXA_INFLACAO_IMAB | ATENCAO | 2020-01-02 | 2026-08-04 | 1640 | 0.954043048283886 | 95.4043048283886 | 0.0 | 0 | 0 | 0 | 910 | 5 | 0 | nan | Sequência elevada de preço congelado |
| AUDBRL=X | MOEDA_DOLAR_AUSTRALIANO | OK | 2020-01-01 | 2026-08-04 | 1715 | 0.997093023255814 | 99.7093023255814 | 0.0 | 0 | 0 | 0 | 2 | 5 | 0 | nan | nan |
| BOVA11.SA | RENDA_VARIAVEL_BRASIL_IBOVESPA | OK | 2020-01-02 | 2026-08-04 | 1639 | 0.9534613147178592 | 95.34613147178592 | 0.0 | 0 | 0 | 0 | 2 | 5 | 0 | nan | nan |
| BOVB11.SA | RENDA_VARIAVEL_BRASIL_IBOVESPA | OK | 2020-01-02 | 2026-08-04 | 1639 | 0.9534613147178592 | 95.34613147178592 | 0.0 | 0 | 0 | 0 | 2 | 5 | 0 | nan | nan |
| BOVV11.SA | RENDA_VARIAVEL_BRASIL_IBOVESPA | OK | 2020-01-02 | 2026-08-04 | 1640 | 0.954043048283886 | 95.4043048283886 | 0.0 | 0 | 0 | 0 | 2 | 5 | 0 | nan | nan |
| BRAX11.SA | RENDA_VARIAVEL_BRASIL_IBRX100 | OK | 2020-01-02 | 2026-08-04 | 1639 | 0.9534613147178592 | 95.34613147178592 | 0.0 | 0 | 0 | 0 | 2 | 5 | 0 | nan | nan |
| BZ=F | COMMODITY_PETROLEO_BRENT | OK | 2020-01-02 | 2026-08-04 | 1658 | 0.9645142524723676 | 96.45142524723676 | 0.0 | 0 | 0 | 0 | 2 | 4 | 0 | nan | nan |
| CADBRL=X | MOEDA_DOLAR_CANADENSE | OK | 2020-01-01 | 2026-08-04 | 1715 | 0.997093023255814 | 99.7093023255814 | 0.0 | 0 | 0 | 0 | 3 | 5 | 0 | nan | nan |
| CC=F | COMMODITY_CACAU | OK | 2020-01-02 | 2026-08-04 | 1657 | 0.9639325189063408 | 96.39325189063408 | 0.0 | 0 | 0 | 0 | 3 | 4 | 0 | nan | nan |
| CHFBRL=X | MOEDA_FRANCO_SUICO | OK | 2020-01-01 | 2026-08-04 | 1715 | 0.997093023255814 | 99.7093023255814 | 0.0 | 0 | 0 | 0 | 3 | 5 | 0 | nan | nan |
| CT=F | COMMODITY_ALGODAO | OK | 2020-01-02 | 2026-08-04 | 1658 | 0.9645142524723676 | 96.45142524723676 | 0.0 | 0 | 0 | 0 | 2 | 4 | 0 | nan | nan |
| DIVO11.SA | RENDA_VARIAVEL_DIVIDENDOS | OK | 2020-01-02 | 2026-08-04 | 1640 | 0.954043048283886 | 95.4043048283886 | 0.0 | 0 | 0 | 0 | 3 | 5 | 0 | nan | nan |
| ECOO11.SA | RENDA_VARIAVEL_ESG | OK | 2020-01-02 | 2026-08-04 | 1639 | 0.9534613147178592 | 95.34613147178592 | 0.0 | 0 | 0 | 0 | 4 | 5 | 0 | nan | nan |
| EURBRL=X | MOEDA_EURO | OK | 2020-01-01 | 2026-08-04 | 1715 | 0.997093023255814 | 99.7093023255814 | 0.0 | 0 | 0 | 0 | 3 | 5 | 0 | nan | nan |
| FIND11.SA | RENDA_VARIAVEL_FINANCEIRO | OK | 2020-01-02 | 2026-08-04 | 1640 | 0.954043048283886 | 95.4043048283886 | 0.0 | 0 | 0 | 0 | 2 | 5 | 0 | nan | nan |
| GBPBRL=X | MOEDA_LIBRA | OK | 2020-01-01 | 2026-08-04 | 1715 | 0.997093023255814 | 99.7093023255814 | 0.0 | 0 | 0 | 0 | 2 | 5 | 0 | nan | nan |
| GC=F | COMMODITY_OURO | OK | 2020-01-02 | 2026-08-04 | 1657 | 0.9639325189063408 | 96.39325189063408 | 0.0 | 0 | 0 | 0 | 2 | 4 | 0 | nan | nan |
| GOVE11.SA | RENDA_VARIAVEL_GOVERNANCA | OK | 2020-01-02 | 2026-08-04 | 1630 | 0.9482257126236184 | 94.82257126236183 | 0.0 | 0 | 0 | 0 | 3 | 6 | 0 | nan | nan |
| HE=F | COMMODITY_SUINOS | OK | 2020-01-02 | 2026-08-04 | 1656 | 0.9633507853403142 | 96.3350785340314 | 0.0 | 0 | 0 | 0 | 2 | 4 | 0 | nan | nan |
| HG=F | COMMODITY_COBRE | OK | 2020-01-02 | 2026-08-04 | 1658 | 0.9645142524723676 | 96.45142524723676 | 0.0 | 0 | 0 | 0 | 2 | 4 | 0 | nan | nan |
| HKDBRL=X | MOEDA_DOLAR_HONG_KONG | OK | 2020-01-01 | 2026-08-04 | 1715 | 0.997093023255814 | 99.7093023255814 | 0.0 | 0 | 0 | 0 | 3 | 5 | 0 | nan | nan |
| HO=F | COMMODITY_OLEO_AQUECIMENTO | OK | 2020-01-02 | 2026-08-04 | 1658 | 0.9645142524723676 | 96.45142524723676 | 0.0 | 0 | 0 | 0 | 1 | 4 | 0 | nan | nan |
| IB5M11.SA | RENDA_FIXA_INFLACAO_IMAB5_MAIS | OK | 2020-01-02 | 2026-08-04 | 1640 | 0.954043048283886 | 95.4043048283886 | 0.0 | 0 | 0 | 0 | 6 | 5 | 0 | nan | nan |

### 01_validacao_series_macro.csv

Caminho: `outputs/tabelas/01_validacao_series_macro.csv`

| codigo_sgs | serie | status | frequencia | data_inicial | data_final | registros | duplicidades | datas_invalidas | valores_nulos | valores_infinitos | intervalo_mediano_dias | maior_intervalo_dias | dias_desatualizado | tolerancia_atualizacao_dias | erros | alertas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 24363 | IBC_BR | ATENCAO | mensal | 2004-01-01 | 2026-05-01 | 269 | 0 | 0 | 0 | 0 | 31.0 | 31 | 95 | 90 | nan | Série possivelmente desatualizada |
| 24364 | IBC_BR_DESSAZONALIZADO | ATENCAO | mensal | 2004-01-01 | 2026-05-01 | 269 | 0 | 0 | 0 | 0 | 31.0 | 31 | 95 | 90 | nan | Série possivelmente desatualizada |
| 12 | CDI | OK | diaria | 2004-01-02 | 2026-08-03 | 5671 | 0 | 0 | 0 | 0 | 1.0 | 5 | 1 | 15 | nan | nan |
| 433 | IPCA | OK | mensal | 2004-01-01 | 2026-06-01 | 270 | 0 | 0 | 0 | 0 | 31.0 | 31 | 64 | 90 | nan | nan |

### 02_06_resumo_desempenho_ativos.csv

Caminho: `outputs/tabelas/02_06_resumo_desempenho_ativos.csv`

| ticker | retorno_total | retorno_anualizado | volatilidade_anualizada | drawdown_maximo | media_retorno_diario | desvio_retorno_diario | melhor_dia | pior_dia | percentual_dias_positivos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B5MB11.SA | 28.543154895056038 | 4.041708292387325 | 19.65077584658938 | -20.97908447263559 | 0.0229140128159444 | 1.2378825228464343 | 28.602279747438253 | -20.820305381709737 | 18.4721352536005 |
| BOVV11.SA | 54.84439036618891 | 7.143226716259421 | 24.32006376080184 | -46.8299588903836 | 0.0392625464766435 | 1.5320200138170452 | 13.97967639087938 | -15.019258233050437 | 51.40889167188478 |
| EURBRL=X | 31.147656976831307 | 4.371548267065428 | 16.065726675729866 | -28.6545628461542 | 0.0220862165501833 | 1.0120456527504202 | 4.953169386566514 | -4.323152835841615 | 47.71446462116468 |
| FIND11.SA | 40.38241151186044 | 5.498269283671475 | 27.37956925106032 | -49.010652121656896 | 0.0360901623645259 | 1.7247507438661092 | 14.104473057077891 | -9.448080757675248 | 50.28177833437696 |
| GC=F | 171.53164972122127 | 17.072549313424744 | 19.05095129001069 | -25.06016525948246 | 0.0698093361225086 | 1.2000971274422247 | 6.083292489183334 | -11.366200569716556 | 55.35378835316218 |
| IB5M11.SA | 27.528550017373576 | 3.911691568492404 | 13.824655657530007 | -18.894292485301488 | 0.0190378714125433 | 0.8708714483553934 | 10.000002857451197 | -10.00000311403858 | 48.52849092047589 |
| IMAB11.SA | 48.56695901745032 | 6.445821501297311 | 23.13100909447016 | -24.9759056876689 | 0.0344194636976691 | 1.4571166104271762 | 36.16352201257862 | -24.975905687668888 | 21.35253600500939 |
| JPYBRL=X | -12.504395790247456 | -2.0858027793107525 | 19.110429492963533 | -43.83447488753773 | -0.0011384963894295 | 1.2038439020479923 | 10.118027077921443 | -8.564888169528718 | 48.21540388227928 |
| MATB11.SA | 72.83783989983606 | 9.018053941585949 | 28.15048942619358 | -49.18518537356532 | 0.0501635721106332 | 1.7733141501538467 | 11.91489037047042 | -18.96551724137932 | 50.97056981840952 |
| NG=F | 25.683321474199804 | 3.6729849209727 | 80.13511954544946 | -83.7293388633306 | 0.1428614548708013 | 5.048038038087872 | 46.481176972812 | -47.4798932600666 | 50.84533500313086 |
| USDBRL=X | 27.271360850416304 | 3.878595652016004 | 16.319021419167083 | -22.12063404505201 | 0.020378198986566 | 1.028001721786963 | 6.209600088872613 | -6.034240013874658 | 50.03130870381967 |
| ZC=F | 18.77394636015335 | 2.752097131554976 | 27.796296519287857 | -55.75924228536508 | 0.0263307017783949 | 1.7510020942534752 | 12.054586808188027 | -17.386530014641288 | 50.53224796493425 |

### 02_06_resumo_desempenho_ativos_formatado.csv

Caminho: `outputs/tabelas/02_06_resumo_desempenho_ativos_formatado.csv`

| ticker | retorno_total | retorno_anualizado | volatilidade_anualizada | drawdown_maximo | media_retorno_diario | desvio_retorno_diario | melhor_dia | pior_dia | percentual_dias_positivos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B5MB11.SA | 28.54% | 4.04% | 19.65% | -20.98% | 0.02% | 1.24% | 28.60% | -20.82% | 18.47% |
| BOVV11.SA | 54.84% | 7.14% | 24.32% | -46.83% | 0.04% | 1.53% | 13.98% | -15.02% | 51.41% |
| EURBRL=X | 31.15% | 4.37% | 16.07% | -28.65% | 0.02% | 1.01% | 4.95% | -4.32% | 47.71% |
| FIND11.SA | 40.38% | 5.50% | 27.38% | -49.01% | 0.04% | 1.72% | 14.10% | -9.45% | 50.28% |
| GC=F | 171.53% | 17.07% | 19.05% | -25.06% | 0.07% | 1.20% | 6.08% | -11.37% | 55.35% |
| IB5M11.SA | 27.53% | 3.91% | 13.82% | -18.89% | 0.02% | 0.87% | 10.00% | -10.00% | 48.53% |
| IMAB11.SA | 48.57% | 6.45% | 23.13% | -24.98% | 0.03% | 1.46% | 36.16% | -24.98% | 21.35% |
| JPYBRL=X | -12.50% | -2.09% | 19.11% | -43.83% | -0.00% | 1.20% | 10.12% | -8.56% | 48.22% |
| MATB11.SA | 72.84% | 9.02% | 28.15% | -49.19% | 0.05% | 1.77% | 11.91% | -18.97% | 50.97% |
| NG=F | 25.68% | 3.67% | 80.14% | -83.73% | 0.14% | 5.05% | 46.48% | -47.48% | 50.85% |
| USDBRL=X | 27.27% | 3.88% | 16.32% | -22.12% | 0.02% | 1.03% | 6.21% | -6.03% | 50.03% |
| ZC=F | 18.77% | 2.75% | 27.80% | -55.76% | 0.03% | 1.75% | 12.05% | -17.39% | 50.53% |

### 02_segmento_commodities_desempenho.csv

Caminho: `outputs/tabelas/02_segmento_commodities_desempenho.csv`

| ticker | retorno_total | retorno_anualizado | volatilidade_anualizada | drawdown_maximo | media_retorno_diario | desvio_retorno_diario | melhor_dia | pior_dia | percentual_dias_positivos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GC=F | 171.53164972122127 | 17.072549313424744 | 19.05095129001069 | -25.06016525948246 | 0.0698093361225086 | 1.2000971274422247 | 6.083292489183334 | -11.366200569716556 | 55.35378835316218 |
| NG=F | 25.683321474199804 | 3.6729849209727 | 80.13511954544946 | -83.7293388633306 | 0.1428614548708013 | 5.048038038087872 | 46.481176972812 | -47.4798932600666 | 50.84533500313086 |
| ZC=F | 18.77394636015335 | 2.752097131554976 | 27.796296519287857 | -55.75924228536508 | 0.0263307017783949 | 1.7510020942534752 | 12.054586808188027 | -17.386530014641288 | 50.53224796493425 |

### 02_segmento_moedas_desempenho.csv

Caminho: `outputs/tabelas/02_segmento_moedas_desempenho.csv`

| ticker | retorno_total | retorno_anualizado | volatilidade_anualizada | drawdown_maximo | media_retorno_diario | desvio_retorno_diario | melhor_dia | pior_dia | percentual_dias_positivos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EURBRL=X | 31.147656976831307 | 4.371548267065428 | 16.065726675729866 | -28.6545628461542 | 0.0220862165501833 | 1.0120456527504202 | 4.953169386566514 | -4.323152835841615 | 47.71446462116468 |
| JPYBRL=X | -12.504395790247456 | -2.0858027793107525 | 19.110429492963533 | -43.83447488753773 | -0.0011384963894295 | 1.2038439020479923 | 10.118027077921443 | -8.564888169528718 | 48.21540388227928 |
| USDBRL=X | 27.271360850416304 | 3.878595652016004 | 16.319021419167083 | -22.12063404505201 | 0.020378198986566 | 1.028001721786963 | 6.209600088872613 | -6.034240013874658 | 50.03130870381967 |

### 02_segmento_renda_fixa_desempenho.csv

Caminho: `outputs/tabelas/02_segmento_renda_fixa_desempenho.csv`

| ticker | retorno_total | retorno_anualizado | volatilidade_anualizada | drawdown_maximo | media_retorno_diario | desvio_retorno_diario | melhor_dia | pior_dia | percentual_dias_positivos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B5MB11.SA | 28.543154895056038 | 4.041708292387325 | 19.65077584658938 | -20.97908447263559 | 0.0229140128159444 | 1.2378825228464343 | 28.602279747438253 | -20.820305381709737 | 18.4721352536005 |
| IB5M11.SA | 27.528550017373576 | 3.911691568492404 | 13.824655657530007 | -18.894292485301488 | 0.0190378714125433 | 0.8708714483553934 | 10.000002857451197 | -10.00000311403858 | 48.52849092047589 |
| IMAB11.SA | 48.56695901745032 | 6.445821501297311 | 23.13100909447016 | -24.9759056876689 | 0.0344194636976691 | 1.4571166104271762 | 36.16352201257862 | -24.975905687668888 | 21.35253600500939 |

### 02_segmento_renda_variavel_desempenho.csv

Caminho: `outputs/tabelas/02_segmento_renda_variavel_desempenho.csv`

| ticker | retorno_total | retorno_anualizado | volatilidade_anualizada | drawdown_maximo | media_retorno_diario | desvio_retorno_diario | melhor_dia | pior_dia | percentual_dias_positivos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOVV11.SA | 54.84439036618891 | 7.143226716259421 | 24.32006376080184 | -46.8299588903836 | 0.0392625464766435 | 1.5320200138170452 | 13.97967639087938 | -15.019258233050437 | 51.40889167188478 |
| FIND11.SA | 40.38241151186044 | 5.498269283671475 | 27.37956925106032 | -49.010652121656896 | 0.0360901623645259 | 1.7247507438661092 | 14.104473057077891 | -9.448080757675248 | 50.28177833437696 |
| MATB11.SA | 72.83783989983606 | 9.018053941585949 | 28.15048942619358 | -49.18518537356532 | 0.0501635721106332 | 1.7733141501538467 | 11.91489037047042 | -18.96551724137932 | 50.97056981840952 |

### 03_validacoes_regimes_macroeconomicos.csv

Caminho: `outputs/tabelas/03_validacoes_regimes_macroeconomicos.csv`

| validacao_tecnica | status | detalhe |
| --- | --- | --- |
| Base classificada não vazia | OK | 255 meses |
| Nenhum regime detectado não classificado | OK | 0 meses não classificados |
| Regimes detectados pertencem à configuração | OK | ['ESTAGFLACAO', 'EXPANSAO_DESINFLACIONARIA', 'EXPANSAO_INFLACIONARIA', 'RECESSAO_DESINFLACIONARIA'] |
| Regimes confirmados pertencem à configuração | OK | ['ESTAGFLACAO', 'EXPANSAO_DESINFLACIONARIA', 'EXPANSAO_INFLACIONARIA', 'RECESSAO_DESINFLACIONARIA'] |
| Códigos detectados preenchidos | OK | 0 códigos ausentes |
| Códigos confirmados preenchidos | OK | 0 códigos ausentes |
| Datas sem duplicidade | OK | 0 duplicidades |
| Datas ordenadas | OK | Ordem cronológica verificada |
| Confirmação mensal válida | OK | 3 mês(es) |

### 04_metricas_portfolio.csv

Caminho: `outputs/tabelas/04_metricas_portfolio.csv`

| metrica | portfolio_regimes_bruto | benchmark_estatico |
| --- | --- | --- |
| retorno_total | 0.7269339144807867 | 0.7269339144807867 |
| retorno_anualizado | 0.0888750183150519 | 0.0888750183150519 |
| volatilidade_anualizada | 0.0832876742031146 | 0.0832876742031146 |
| retorno_sobre_volatilidade | 1.0670848857936817 | 1.0670848857936817 |
| maximo_drawdown | -0.0831222795683922 | -0.0831222795683922 |
| meses_positivos | 0.6103896103896104 | 0.6103896103896104 |
| melhor_mes | 0.086845861271291 | 0.086845861271291 |
| pior_mes | -0.0635990150083059 | -0.0635990150083059 |
| quantidade_meses | 77.0 | 77.0 |

### 04_pesos_por_regime.csv

Caminho: `outputs/tabelas/04_pesos_por_regime.csv`

| regime_sinal | peso_NG=F | peso_ZC=F | peso_GC=F | peso_USDBRL=X | peso_EURBRL=X | peso_JPYBRL=X | peso_IMAB11.SA | peso_B5MB11.SA | peso_IB5M11.SA | peso_BOVV11.SA | peso_FIND11.SA | peso_MATB11.SA | soma_pesos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESTAGFLACAO | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 |
| EXPANSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 |
| EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 |
| RECESSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 |

### 05_contribuicao_media_por_regime.csv

Caminho: `outputs/tabelas/05_contribuicao_media_por_regime.csv`

| regime_sinal | contribuicao_media_NG=F | contribuicao_media_ZC=F | contribuicao_media_GC=F | contribuicao_media_USDBRL=X | contribuicao_media_EURBRL=X | contribuicao_media_JPYBRL=X | contribuicao_media_IMAB11.SA | contribuicao_media_B5MB11.SA | contribuicao_media_IB5M11.SA | contribuicao_media_BOVV11.SA | contribuicao_media_FIND11.SA | contribuicao_media_MATB11.SA | soma_contribuicoes_medias | retorno_bruto_medio_portfolio | retorno_liquido_medio_portfolio | custo_medio_portfolio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | -0.0017609904126402 | -0.0011308503824713 | 0.001143181100174 | 0.0002142417080441 | 0.0002508756610349 | -0.0002609138766075 | 0.0010217649933162 | 0.0008141018454069 | 0.0006464484035218 | 0.0002076108191446 | 0.0003311751924919 | -0.0002292979044991 | 0.0012473471469162 | 0.0012473471469162 | 0.0011971677320585 | 5.035314568601911e-05 |
| EXPANSAO_INFLACIONARIA | 0.0026142209471565 | 0.0018100058018873 | 0.0015502050835422 | 2.1040786860180625e-05 | 1.697732772777997e-05 | -0.0003428209368506 | 8.873951297359061e-05 | 9.436213067226e-05 | -1.1629811018947028e-05 | 0.0013911748158428 | 0.001320590775582 | 0.001581267405681 | 0.0101341338400563 | 0.0101341338400563 | 0.0101083589771069 | 2.543321498131129e-05 |
| ESTAGFLACAO | 0.011304046294819 | -0.0017316641141554 | -0.0010234546204219 | 0.0013109174117167 | 0.0006210828819483 | 0.000740882904683 | -0.0007236495030382 | -0.0013066881016464 | -0.0012032475846503 | -0.0031065912487757 | -0.0035137796138058 | -0.0040894231719952 | -0.0027215684653222 | -0.0027215684653222 | -0.0027445686467171 | 2.3127329587836543e-05 |
| RECESSAO_DESINFLACIONARIA | 0.0100834408441834 | 0.0028515293224099 | 0.0022445384568739 | 0.0012152102389802 | 0.0017875183703522 | 0.0009994459011006 | 0.0005795834968604 | 0.0003797232820516 | 0.0010186743738259 | 0.0019113418787819 | 0.0015471421071802 | 0.0050380210080554 | 0.029656169280656 | 0.0296561692806561 | 0.029633903505703 | 2.1713971404356503e-05 |

### 05_custo_break_even.csv

Caminho: `outputs/tabelas/05_custo_break_even.csv`

| custo_base | custo_base_bps | custo_break_even | custo_break_even_bps | indice_final_portfolio_custo_base | indice_final_benchmark_custo_base | diferenca_final_custo_base | limite_inferior_testado | limite_superior_testado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.001 | 10.0 | 0.0 | 0.0 | 172.21657497546323 | 172.21657497546323 | 0.0 | 0.0 | 0.05 |

### 05_desempenho_por_regime.csv

Caminho: `outputs/tabelas/05_desempenho_por_regime.csv`

| regime_sinal | quantidade_meses | retorno_bruto_medio_portfolio | retorno_liquido_medio_portfolio | retorno_condicional_portfolio | volatilidade_anualizada_portfolio | meses_positivos_portfolio | melhor_mes_portfolio | pior_mes_portfolio | retorno_bruto_medio_benchmark | retorno_liquido_medio_benchmark | retorno_condicional_benchmark | volatilidade_anualizada_benchmark | meses_positivos_benchmark | melhor_mes_benchmark | pior_mes_benchmark | diferenca_retorno_liquido_medio | diferenca_retorno_condicional |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | 34 | 0.0012473471469162 | 0.0011971677320585 | 0.0318157069204021 | 0.0832053422239016 | 0.5294117647058824 | 0.0868246670042187 | -0.050864032842775 | 0.0012473471469162 | 0.0011971677320585 | 0.0318157069204021 | 0.0832053422239016 | 0.5294117647058824 | 0.0868246670042187 | -0.050864032842775 | 0.0 | 0.0 |
| EXPANSAO_INFLACIONARIA | 30 | 0.0101341338400563 | 0.0101083589771069 | 0.341682339708617 | 0.080626129126475 | 0.6666666666666666 | 0.0497684275477665 | -0.0636215268498781 | 0.0101341338400563 | 0.0101083589771069 | 0.341682339708617 | 0.080626129126475 | 0.6666666666666666 | 0.0497684275477665 | -0.0636215268498781 | 0.0 | 0.0 |
| ESTAGFLACAO | 5 | -0.0027215684653222 | -0.0027445686467171 | -0.0139582134821897 | 0.0433406415661266 | 0.4 | 0.012748599853589 | -0.0174395341842622 | -0.0027215684653222 | -0.0027445686467171 | -0.0139582134821897 | 0.0433406415661266 | 0.4 | 0.012748599853589 | -0.0174395341842622 | 0.0 | 0.0 |
| RECESSAO_DESINFLACIONARIA | 8 | 0.0296561692806561 | 0.029633903505703 | 0.261617748200361 | 0.0665654786124064 | 0.875 | 0.0515055517844937 | -0.005470982310879 | 0.0296561692806561 | 0.029633903505703 | 0.261617748200361 | 0.0665654786124064 | 0.875 | 0.0515055517844937 | -0.005470982310879 | 0.0 | 0.0 |

### 05_metricas_backtest.csv

Caminho: `outputs/tabelas/05_metricas_backtest.csv`

| metrica | portfolio_regimes_bruto | portfolio_regimes_liquido | benchmark_estatico_bruto | benchmark_estatico_liquido |
| --- | --- | --- | --- | --- |
| quantidade_meses | 77.0 | 77.0 | 77.0 | 77.0 |
| retorno_total | 0.726933914480786 | 0.7221657497546323 | 0.726933914480786 | 0.7221657497546323 |
| retorno_anualizado | 0.0888750183150519 | 0.0884059341519305 | 0.0888750183150519 | 0.0884059341519305 |
| retorno_medio_mensal | 0.0074035757157854 | 0.0073675695716264 | 0.0074035757157854 | 0.0073675695716264 |
| retorno_mediano_mensal | 0.005369418196494 | 0.0053534349727804 | 0.005369418196494 | 0.0053534349727804 |
| volatilidade_anualizada | 0.0832876742031145 | 0.0833098056373953 | 0.0832876742031145 | 0.0833098056373953 |
| desvio_negativo_anualizado | 0.044287481529581 | 0.0443445397325071 | 0.044287481529581 | 0.0443445397325071 |
| retorno_sobre_volatilidade | 1.0670848857936834 | 1.061170812673793 | 1.0670848857936832 | 1.061170812673793 |
| sharpe_excesso_cdi | -0.1008544776135841 | -0.1058224318297662 | -0.1008544776135841 | -0.1058224318297662 |
| sortino_alvo_zero | 2.006775170895404 | 1.993614877619844 | 2.006775170895404 | 1.993614877619844 |
| maximo_drawdown | -0.0883773969742375 | -0.0893304663312881 | -0.0883773969742375 | -0.0893304663312881 |
| calmar | 1.0056306403882826 | 0.9896504270342782 | 1.0056306403882826 | 0.9896504270342782 |
| meses_positivos | 0.6103896103896104 | 0.6103896103896104 | 0.6103896103896104 | 0.6103896103896104 |
| melhor_mes | 0.086845861271291 | 0.0868246670042187 | 0.086845861271291 | 0.0868246670042187 |
| pior_mes | -0.0635990150083059 | -0.0636215268498781 | -0.0635990150083059 | -0.0636215268498781 |
| var_historico_95% | -0.0244871161372276 | -0.0245005708369238 | -0.0244871161372276 | -0.0245005708369238 |
| cvar_historico_95% | -0.0442041405912169 | -0.0442262919368448 | -0.0442041405912169 | -0.0442262919368448 |

### 05_metricas_backtest_formatadas.csv

Caminho: `outputs/tabelas/05_metricas_backtest_formatadas.csv`

| metrica | portfolio_regimes_bruto | portfolio_regimes_liquido | benchmark_estatico_bruto | benchmark_estatico_liquido |
| --- | --- | --- | --- | --- |
| quantidade_meses | 77 | 77 | 77 | 77 |
| retorno_total | 72.69% | 72.22% | 72.69% | 72.22% |
| retorno_anualizado | 8.89% | 8.84% | 8.89% | 8.84% |
| retorno_medio_mensal | 0.74% | 0.74% | 0.74% | 0.74% |
| retorno_mediano_mensal | 0.54% | 0.54% | 0.54% | 0.54% |
| volatilidade_anualizada | 8.33% | 8.33% | 8.33% | 8.33% |
| desvio_negativo_anualizado | 4.43% | 4.43% | 4.43% | 4.43% |
| retorno_sobre_volatilidade | 1.0671 | 1.0612 | 1.0671 | 1.0612 |
| sharpe_excesso_cdi | -0.1009 | -0.1058 | -0.1009 | -0.1058 |
| sortino_alvo_zero | 2.0068 | 1.9936 | 2.0068 | 1.9936 |
| maximo_drawdown | -8.84% | -8.93% | -8.84% | -8.93% |
| calmar | 1.0056 | 0.9897 | 1.0056 | 0.9897 |
| meses_positivos | 61.04% | 61.04% | 61.04% | 61.04% |
| melhor_mes | 8.68% | 8.68% | 8.68% | 8.68% |
| pior_mes | -6.36% | -6.36% | -6.36% | -6.36% |
| var_historico_95% | -2.45% | -2.45% | -2.45% | -2.45% |
| cvar_historico_95% | -4.42% | -4.42% | -4.42% | -4.42% |

### 05_metricas_moveis_12m.csv

Caminho: `outputs/tabelas/05_metricas_moveis_12m.csv`

| data | retorno_portfolio_liquido | retorno_estatica_liquido | retorno_movel_portfolio | retorno_movel_benchmark | volatilidade_movel_portfolio | volatilidade_movel_benchmark | diferenca_retorno_movel | diferenca_volatilidade_movel | portfolio_superou_janela |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-01-31 | -0.0067258041846283 | -0.0067258041846283 | nan | nan | nan | nan | nan | nan | False |
| 2020-02-29 | -0.0208702791480732 | -0.0208702791480732 | nan | nan | nan | nan | nan | nan | False |
| 2020-03-31 | -0.0636215268498781 | -0.0636215268498781 | nan | nan | nan | nan | nan | nan | False |
| 2020-04-30 | 0.0497684275477665 | 0.0497684275477665 | nan | nan | nan | nan | nan | nan | False |
| 2020-05-31 | 0.0310950836815959 | 0.0310950836815959 | nan | nan | nan | nan | nan | nan | False |
| 2020-06-30 | 0.0314123751162691 | 0.0314123751162691 | nan | nan | nan | nan | nan | nan | False |
| 2020-07-31 | 0.0398343004827213 | 0.0398343004827213 | nan | nan | nan | nan | nan | nan | False |
| 2020-08-31 | 0.0515055517844937 | 0.0515055517844937 | nan | nan | nan | nan | nan | nan | False |
| 2020-09-30 | -0.005470982310879 | -0.005470982310879 | nan | nan | nan | nan | nan | nan | False |
| 2020-10-31 | 0.0444458025638641 | 0.0444458025638641 | nan | nan | nan | nan | nan | nan | False |
| 2020-11-30 | 0.0142819881018703 | 0.0142819881018703 | nan | nan | nan | nan | nan | nan | False |
| 2020-12-31 | 0.0404366032137544 | 0.0404366032137544 | 0.2185371705940615 | 0.2185371705940615 | 0.1213722139406958 | 0.1213722139406958 | 0.0 | 0.0 | False |
| 2021-01-31 | 0.0154887323408328 | 0.0154887323408328 | 0.2457897042829819 | 0.2457897042829819 | 0.1186014672674262 | 0.1186014672674262 | 0.0 | 0.0 | False |
| 2021-02-28 | -0.0005959625459094 | -0.0005959625459094 | 0.2715856068548832 | 0.2715856068548832 | 0.1127500375265055 | 0.1127500375265055 | 0.0 | 0.0 | False |
| 2021-03-31 | 0.0124408247763787 | 0.0124408247763787 | 0.3748769514605559 | 0.3748769514605559 | 0.0670972740400866 | 0.0670972740400866 | 0.0 | 0.0 | False |
| 2021-04-30 | 0.0399611773621255 | 0.0399611773621255 | 0.362032440344002 | 0.362032440344002 | 0.0641262964696715 | 0.0641262964696715 | 0.0 | 0.0 | False |
| 2021-05-31 | 0.0033232594001511 | 0.0033232594001511 | 0.325347050026942 | 0.325347050026942 | 0.0677425048628469 | 0.0677425048628469 | 0.0 | 0.0 | False |
| 2021-06-30 | 0.0051637889163169 | 0.0051637889163169 | 0.2916180710784752 | 0.2916180710784752 | 0.069635210655625 | 0.069635210655625 | 0.0 | 0.0 | False |
| 2021-07-31 | -0.0130017700933071 | -0.0130017700933071 | 0.2259883611053619 | 0.2259883611053619 | 0.0745265179084237 | 0.0745265179084237 | 0.0 | 0.0 | False |
| 2021-08-31 | -0.0011939277259223 | -0.0011939277259223 | 0.1645441315371647 | 0.1645441315371647 | 0.0663482548609351 | 0.0663482548609351 | 0.0 | 0.0 | False |
| 2021-09-30 | 0.012748599853589 | 0.012748599853589 | 0.1858783582025576 | 0.1858783582025576 | 0.0632627510200055 | 0.0632627510200055 | 0.0 | 0.0 | False |
| 2021-10-31 | -0.0174395341842622 | -0.0174395341842622 | 0.1156128821390514 | 0.1156128821390514 | 0.0615059019571517 | 0.0615059019571517 | 0.0 | 0.0 | False |
| 2021-11-30 | -0.0092118206022645 | -0.0092118206022645 | 0.0897719464344819 | 0.0897719464344819 | 0.0638719113855165 | 0.0638719113855165 | 0.0 | 0.0 | False |
| 2021-12-31 | -0.0043080584569618 | -0.0043080584569618 | 0.0429055858212241 | 0.0429055858212241 | 0.0533946110378076 | 0.0533946110378076 | 0.0 | 0.0 | False |
| 2022-01-31 | 0.0386555044225127 | 0.0386555044225127 | 0.0666978301268184 | 0.0666978301268184 | 0.063149580400634 | 0.063149580400634 | 0.0 | 0.0 | False |

### 05_resultados_anuais.csv

Caminho: `outputs/tabelas/05_resultados_anuais.csv`

| ano | quantidade_meses | retorno_portfolio_bruto | retorno_portfolio_liquido | retorno_benchmark_bruto | retorno_benchmark_liquido | diferenca_liquida | portfolio_superou_benchmark | ano_completo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020 | 12 | 0.22014399857551 | 0.2185371705940615 | 0.22014399857551 | 0.2185371705940615 | 0.0 | False | True |
| 2021 | 12 | 0.0431941748919906 | 0.0429055858212241 | 0.0431941748919906 | 0.0429055858212241 | 0.0 | False | True |
| 2022 | 12 | 0.0556988178925603 | 0.0553330080490521 | 0.0556988178925603 | 0.0553330080490521 | 0.0 | False | True |
| 2023 | 12 | 0.0010802410813095 | 0.0008235792167194 | 0.0010802410813095 | 0.0008235792167194 | 0.0 | False | True |
| 2024 | 12 | 0.083315828987734 | 0.0830729421157692 | 0.083315828987734 | 0.0830729421157692 | 0.0 | False | True |
| 2025 | 12 | 0.1280132926557466 | 0.1277697913547486 | 0.1280132926557466 | 0.1277697913547486 | 0.0 | False | True |
| 2026 | 5 | 0.0505609308546541 | 0.0504271989134106 | 0.0505609308546541 | 0.0504271989134106 | 0.0 | False | False |

### 05_resumo_turnover_custos.csv

Caminho: `outputs/tabelas/05_resumo_turnover_custos.csv`

| metrica | portfolio_regimes | benchmark_estatico |
| --- | --- | --- |
| custo_por_unidade_turnover | 0.001 | 0.001 |
| turnover_total | 2.7643518219380234 | 2.7643518219380248 |
| turnover_medio_mensal | 0.0359006730121821 | 0.0359006730121821 |
| custo_acumulado_simples | 0.002764351821938 | 0.002764351821938 |
| indice_final_bruto | 172.6933914480786 | 172.6933914480786 |
| indice_final_liquido | 172.21657497546323 | 172.21657497546323 |
| impacto_final_custos | 0.4768164726153827 | 0.4768164726153827 |

### 05_sensibilidade_custos.csv

Caminho: `outputs/tabelas/05_sensibilidade_custos.csv`

| taxa_custo | custo_bps | indice_final_portfolio | indice_final_benchmark | diferenca_indice_final | retorno_total_portfolio | retorno_total_benchmark | retorno_anualizado_portfolio | retorno_anualizado_benchmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 0.0 | 172.6933914480786 | 172.6933914480786 | 0.0 | 0.726933914480786 | 0.726933914480786 | 0.0888750183150519 | 0.0888750183150519 |
| 0.0005 | 5.0 | 172.45484105896574 | 172.45484105896574 | 0.0 | 0.7245484105896574 | 0.7245484105896574 | 0.0886404732404269 | 0.0886404732404269 |
| 0.001 | 10.0 | 172.21657497546323 | 172.21657497546323 | 0.0 | 0.7221657497546323 | 0.7221657497546323 | 0.0884059341519305 | 0.0884059341519305 |
| 0.0015 | 15.0 | 171.97859288663665 | 171.97859288663665 | 0.0 | 0.7197859288663664 | 0.7197859288663664 | 0.0881714010249019 | 0.0881714010249019 |
| 0.002 | 20.0 | 171.74089448187274 | 171.74089448187274 | 0.0 | 0.7174089448187275 | 0.7174089448187275 | 0.0879368738346491 | 0.0879368738346491 |
| 0.003 | 30.0 | 171.26634748367545 | 171.26634748367545 | 0.0 | 0.7126634748367544 | 0.7126634748367544 | 0.0874678371655399 | 0.0874678371655399 |
| 0.005 | 50.0 | 170.3206440645035 | 170.3206440645035 | 0.0 | 0.7032064406450351 | 0.7032064406450351 | 0.0865298339786133 | 0.0865298339786133 |

### 05_turnover_custos_mensal.csv

Caminho: `outputs/tabelas/05_turnover_custos_mensal.csv`

| data | regime_sinal | turnover_portfolio | turnover_estatica | custo_portfolio | custo_estatica | retorno_portfolio | retorno_portfolio_liquido | retorno_carteira_estatica | retorno_estatica_liquido | indice_portfolio_bruto | indice_portfolio_liquido | indice_estatica_bruto | indice_estatica_liquido |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-01-31 | EXPANSAO_DESINFLACIONARIA | 1.0 | 1.0 | 0.001 | 0.001 | -0.0057315357203487 | -0.0067258041846283 | -0.0057315357203487 | -0.0067258041846283 | 99.42684642796512 | 99.32741958153716 | 99.42684642796512 | 99.32741958153716 |
| 2020-02-29 | EXPANSAO_DESINFLACIONARIA | 0.0214700289719183 | 0.0214700289719183 | 2.147002897191834e-05 | 2.1470028971918343e-05 | -0.0208492567532479 | -0.0208702791480732 | -0.0208492567532479 | -0.0208702791480732 | 97.35387057862272 | 97.2544286078127 | 97.35387057862272 | 97.2544286078127 |
| 2020-03-31 | EXPANSAO_INFLACIONARIA | 0.0240408136397085 | 0.0240408136397085 | 2.404081363970857e-05 | 2.404081363970856e-05 | -0.0635990150083059 | -0.0636215268498781 | -0.0635990150083059 | -0.0636215268498781 | 91.16226030257624 | 91.0669533668712 | 91.16226030257624 | 91.0669533668712 |
| 2020-04-30 | EXPANSAO_INFLACIONARIA | 0.0710417699576211 | 0.0710417699576211 | 7.104176995762115e-05 | 7.104176995762118e-05 | 0.0498430102533927 | 0.0497684275477665 | 0.0498430102533927 | 0.0497684275477665 | 95.70606177756 | 95.59921243750615 | 95.70606177756 | 95.59921243750615 |
| 2020-05-31 | EXPANSAO_INFLACIONARIA | 0.0214663560793516 | 0.0214663560793515 | 2.14663560793516e-05 | 2.1466356079351583e-05 | 0.0311172180109573 | 0.0310950836815959 | 0.0311172180109573 | 0.0310950836815959 | 98.68416816686248 | 98.57187794814509 | 98.68416816686248 | 98.57187794814509 |
| 2020-06-30 | RECESSAO_DESINFLACIONARIA | 0.0148516578012435 | 0.0148516578012435 | 1.4851657801243555e-05 | 1.4851657801243506e-05 | 0.0314276935274202 | 0.0314123751162691 | 0.0314276935274203 | 0.0314123751162691 | 101.78558396001904 | 101.66825475416732 | 101.78558396001904 | 101.66825475416732 |
| 2020-07-31 | RECESSAO_DESINFLACIONARIA | 0.0143657636582816 | 0.0143657636582816 | 1.4365763658281627e-05 | 1.4365763658281676e-05 | 0.0398492387111249 | 0.0398343004827213 | 0.0398492387111249 | 0.0398343004827213 | 105.84166199259306 | 105.71813856359869 | 105.84166199259306 | 105.71813856359869 |
| 2020-08-31 | RECESSAO_DESINFLACIONARIA | 0.0237844737872176 | 0.0237844737872176 | 2.3784473787217624e-05 | 2.3784473787217603e-05 | 0.0515305618855795 | 0.0515055517844937 | 0.0515305618855795 | 0.0515055517844937 | 111.29574230597495 | 111.1632096239464 | 111.29574230597495 | 111.1632096239464 |
| 2020-09-30 | RECESSAO_DESINFLACIONARIA | 0.0410681547138152 | 0.0410681547138153 | 4.106815471381529e-05 | 4.106815471381536e-05 | -0.0054301371618784 | -0.005470982310879 | -0.0054301371618784 | -0.005470982310879 | 110.69139115972048 | 110.55503767047324 | 110.69139115972048 | 110.55503767047324 |
| 2020-10-31 | RECESSAO_DESINFLACIONARIA | 0.0201777511637806 | 0.0201777511637806 | 2.017775116378064e-05 | 2.0177751163780672e-05 | 0.0444668775566183 | 0.0444458025638641 | 0.0444668775566183 | 0.0444458025638641 | 115.61349169699152 | 115.46874504721568 | 115.61349169699152 | 115.46874504721568 |
| 2020-11-30 | EXPANSAO_INFLACIONARIA | 0.0243661503870029 | 0.024366150387003 | 2.4366150387002967e-05 | 2.436615038700308e-05 | 0.0143067028515305 | 0.0142819881018703 | 0.0143067028515305 | 0.0142819881018703 | 117.26753956832825 | 117.1178682901179 | 117.26753956832825 | 117.1178682901179 |
| 2020-12-31 | EXPANSAO_INFLACIONARIA | 0.0406453816174108 | 0.0406453816174109 | 4.06453816174109e-05 | 4.064538161741092e-05 | 0.0404788938754607 | 0.0404366032137544 | 0.0404788938754607 | 0.0404366032137544 | 122.014399857551 | 121.85371705940616 | 122.014399857551 | 121.85371705940616 |
| 2021-01-31 | EXPANSAO_INFLACIONARIA | 0.0294704585998917 | 0.0294704585998917 | 2.9470458599891783e-05 | 2.947045859989174e-05 | 0.0155186601414639 | 0.0154887323408328 | 0.0155186601414639 | 0.0154887323408328 | 123.907899861305 | 123.74107666767486 | 123.907899861305 | 123.74107666767486 |
| 2021-02-28 | EXPANSAO_INFLACIONARIA | 0.0202664901565263 | 0.0202664901565263 | 2.0266490156526324e-05 | 2.026649015652635e-05 | -0.0005757077233278 | -0.0005959625459094 | -0.0005757077233278 | -0.0005959625459094 | 123.83656512637351 | 123.66733162059045 | 123.83656512637351 | 123.66733162059045 |
| 2021-03-31 | EXPANSAO_INFLACIONARIA | 0.0197544418505292 | 0.0197544418505292 | 1.975444185052921e-05 | 1.975444185052923e-05 | 0.0124608253748795 | 0.0124408247763787 | 0.0124608253748795 | 0.0124408247763787 | 125.37967093943816 | 125.20585522384452 | 125.37967093943816 | 125.20585522384452 |
| 2021-04-30 | EXPANSAO_INFLACIONARIA | 0.0146724861011076 | 0.0146724861011077 | 1.4672486101107655e-05 | 1.4672486101107704e-05 | 0.0399764364019342 | 0.0399611773621255 | 0.0399764364019342 | 0.0399611773621255 | 130.39190338084404 | 130.20922861122116 | 130.39190338084404 | 130.20922861122116 |
| 2021-05-31 | EXPANSAO_INFLACIONARIA | 0.0355895655419145 | 0.0355895655419146 | 3.558956554191451e-05 | 3.558956554191461e-05 | 0.003358968509923 | 0.0033232594001511 | 0.003358968509923 | 0.0033232594001511 | 130.8298856782492 | 130.64194765418983 | 130.8298856782492 | 130.64194765418983 |
| 2021-06-30 | ESTAGFLACAO | 0.0194029561472565 | 0.0194029561472565 | 1.9402956147256542e-05 | 1.940295614725654e-05 | 0.0051832924436601 | 0.0051637889163169 | 0.0051832924436601 | 0.0051637889163169 | 131.5080152360902 | 131.31655509549262 | 131.5080152360902 | 131.31655509549262 |
| 2021-07-31 | ESTAGFLACAO | 0.0260232298113362 | 0.0260232298113362 | 2.60232298113362e-05 | 2.6023229811336256e-05 | -0.0129760845431259 | -0.0130017700933071 | -0.0129760845431259 | -0.0130017700933071 | 129.80155611228798 | 129.6092074366959 | 129.80155611228798 | 129.6092074366959 |
| 2021-08-31 | ESTAGFLACAO | 0.0239200607402751 | 0.0239200607402751 | 2.392006074027514e-05 | 2.392006074027513e-05 | -0.001170035652506 | -0.0011939277259223 | -0.001170035652506 | -0.0011939277259223 | 129.64968366388584 | 129.4544634104024 | 129.64968366388584 | 129.4544634104024 |
| 2021-09-30 | ESTAGFLACAO | 0.0144238569392235 | 0.0144238569392236 | 1.4423856939223589e-05 | 1.442385693922363e-05 | 0.0127632078052116 | 0.012748599853589 | 0.0127632078052116 | 0.012748599853589 | 131.30442951836795 | 131.1048265636827 | 131.30442951836795 | 131.1048265636827 |
| 2021-10-31 | ESTAGFLACAO | 0.0318665443010912 | 0.0318665443010913 | 3.186654430109128e-05 | 3.186654430109131e-05 | -0.0174082223798508 | -0.0174395341842622 | -0.0174082223798508 | -0.0174395341842622 | 129.01865280985277 | 128.8184194591036 | 129.01865280985277 | 128.8184194591036 |
| 2021-11-30 | EXPANSAO_INFLACIONARIA | 0.0239060807151442 | 0.0239060807151443 | 2.3906080715144293e-05 | 2.3906080715144324e-05 | -0.0091881341738266 | -0.0092118206022645 | -0.0091881341738266 | -0.0092118206022645 | 127.83321211690948 | 127.63176728877907 | 127.83321211690948 | 127.63176728877907 |
| 2021-12-31 | EXPANSAO_INFLACIONARIA | 0.0173785048503699 | 0.0173785048503699 | 1.7378504850369936e-05 | 1.737850485036993e-05 | -0.0042907545190096 | -0.0043080584569618 | -0.0042907545190096 | -0.0043080584569618 | 127.28471118433932 | 127.08192217433368 | 127.28471118433932 | 127.08192217433368 |
| 2022-01-31 | EXPANSAO_INFLACIONARIA | 0.024658637621061 | 0.024658637621061 | 2.465863762106105e-05 | 2.465863762106105e-05 | 0.0386811168837778 | 0.0386555044225127 | 0.0386811168837778 | 0.0386555044225127 | 132.20822597517866 | 131.99433797896504 | 132.20822597517866 | 131.99433797896504 |

### 05_validacao_final_backtest.csv

Caminho: `outputs/tabelas/05_validacao_final_backtest.csv`

| validacao | status | detalhe | resultado |
| --- | --- | --- | --- |
| Base possui registros | APROVADO | 77 meses | True |
| Datas válidas | APROVADO | Nenhuma data inválida | True |
| Datas sem duplicidade | APROVADO | 0 duplicidades | True |
| Datas em ordem crescente | APROVADO | Ordenação temporal validada | True |
| Sem nulos nas colunas principais | APROVADO | 0 valores nulos | True |
| Pesos somam 100% | APROVADO | Mínimo 1.000000000000 \| Máximo 1.000000000000 | True |
| Turnover não negativo | APROVADO | Turnovers mensais verificados | True |
| Custos não negativos | APROVADO | Custos mensais verificados | True |
| Retorno líquido do portfólio consistente | APROVADO | Fórmula de custos validada | True |
| Retorno líquido do benchmark consistente | APROVADO | Fórmula de custos validada | True |
| Índices finais positivos | APROVADO | Patrimônios finais maiores que zero | True |

### 06_01_resumo_modelo_original.csv

Caminho: `outputs/tabelas/06_01_resumo_modelo_original.csv`

| metrica | valor |
| --- | --- |
| Quantidade de meses | 77 |
| Data inicial | 31/01/2020 |
| Data final | 31/05/2026 |
| Quantidade de ativos | 12 |
| Ativos originais | NG=F, ZC=F, GC=F, USDBRL=X, EURBRL=X, JPYBRL=X, IMAB11.SA, B5MB11.SA, IB5M11.SA, BOVV11.SA, FIND11.SA, MATB11.SA |
| Quantidade de regimes encontrados | 4 |
| Regimes encontrados | ESTAGFLACAO, EXPANSAO_DESINFLACIONARIA, EXPANSAO_INFLACIONARIA, RECESSAO_DESINFLACIONARIA |
| Regimes ausentes | Nenhum |
| Peso mínimo total | 0.9999999999999994 |
| Peso máximo total | 0.9999999999999994 |
| CDI disponível | Não |
| IMAB_OFICIAL_PARCIAL disponível | Não |

### 06_02_regimes_suavizados.csv

Caminho: `outputs/tabelas/06_02_regimes_suavizados.csv`

| data | regime_sinal | regime_confirmacao_1m | regime_confirmacao_2m | regime_confirmacao_3m |
| --- | --- | --- | --- | --- |
| 2020-01-31 | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA |
| 2020-02-29 | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA |
| 2020-03-31 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA |
| 2020-04-30 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_DESINFLACIONARIA |
| 2020-05-31 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA |
| 2020-06-30 | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA |
| 2020-07-31 | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | EXPANSAO_INFLACIONARIA |
| 2020-08-31 | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA |
| 2020-09-30 | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA |
| 2020-10-31 | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA |
| 2020-11-30 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA |
| 2020-12-31 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | RECESSAO_DESINFLACIONARIA |
| 2021-01-31 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA |
| 2021-02-28 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA |
| 2021-03-31 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA |
| 2021-04-30 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA |
| 2021-05-31 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA |
| 2021-06-30 | ESTAGFLACAO | ESTAGFLACAO | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA |
| 2021-07-31 | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO | EXPANSAO_INFLACIONARIA |
| 2021-08-31 | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO |
| 2021-09-30 | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO |
| 2021-10-31 | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO |
| 2021-11-30 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | ESTAGFLACAO | ESTAGFLACAO |
| 2021-12-31 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | ESTAGFLACAO |
| 2022-01-31 | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA |

### 06_02_resumo_suavizacao_regimes.csv

Caminho: `outputs/tabelas/06_02_resumo_suavizacao_regimes.csv`

| meses_confirmacao | quantidade_mudancas | reducao_absoluta_mudancas | reducao_percentual_mudancas | duracao_media_regime_meses | duracao_mediana_regime_meses | meses_diferentes_original | proporcao_meses_diferentes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 11.0 | 0.0 | 0.0 | 6.416666666666667 | 4.5 | 0.0 | 0.0 |
| 2.0 | 11.0 | 0.0 | 0.0 | 6.416666666666667 | 4.0 | 11.0 | 0.1428571428571428 |
| 3.0 | 11.0 | 0.0 | 0.0 | 6.416666666666667 | 4.0 | 22.0 | 0.2857142857142857 |

### 06_02_resumo_suavizacao_regimes_formatado.csv

Caminho: `outputs/tabelas/06_02_resumo_suavizacao_regimes_formatado.csv`

| meses_confirmacao | quantidade_mudancas | reducao_absoluta_mudancas | reducao_percentual_mudancas | duracao_media_regime_meses | duracao_mediana_regime_meses | meses_diferentes_original | proporcao_meses_diferentes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 | 0 | 0.00% | 6.42 | 4.5 | 0 | 0.00% |
| 2 | 11 | 0 | 0.00% | 6.42 | 4.0 | 11 | 14.29% |
| 3 | 11 | 0 | 0.00% | 6.42 | 4.0 | 22 | 28.57% |

### 06_03_comparacao_regimes_suavizados.csv

Caminho: `outputs/tabelas/06_03_comparacao_regimes_suavizados.csv`

| cenario | rotulo | meses_confirmacao | quantidade_mudancas_regime | turnover_total | turnover_medio_mensal | custo_acumulado_simples | retorno_total_bruto | retorno_total_liquido | retorno_anualizado_liquido | volatilidade_anualizada_liquida | retorno_volatilidade_liquido | maximo_drawdown_liquido | meses_positivos | indice_final_bruto | indice_final_liquido | impacto_final_custos | diferenca_liquida_vs_benchmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Original_1m | Regime original | 1.0 | 11 | 2.7643518219380234 | 0.0359006730121821 | 0.002764351821938 | 0.7269339144807869 | 0.7221657497546328 | 0.0884059341519305 | 0.0833098056373953 | 1.0611708126737924 | -0.0893304663312883 | 0.6103896103896104 | 172.6933914480787 | 172.2165749754633 | 0.4768164726154111 | 2.8421709430404014e-14 |
| Confirmacao_2m | Confirmação de 2 meses | 2.0 | 11 | 2.7643518219380234 | 0.0359006730121821 | 0.002764351821938 | 0.7269339144807869 | 0.7221657497546328 | 0.0884059341519305 | 0.0833098056373953 | 1.0611708126737924 | -0.0893304663312883 | 0.6103896103896104 | 172.6933914480787 | 172.2165749754633 | 0.4768164726154111 | 2.8421709430404014e-14 |
| Confirmacao_3m | Confirmação de 3 meses | 3.0 | 11 | 2.7643518219380234 | 0.0359006730121821 | 0.002764351821938 | 0.7269339144807869 | 0.7221657497546328 | 0.0884059341519305 | 0.0833098056373953 | 1.0611708126737924 | -0.0893304663312883 | 0.6103896103896104 | 172.6933914480787 | 172.2165749754633 | 0.4768164726154111 | 2.8421709430404014e-14 |
| Benchmark_Estatico | Benchmark de pesos iguais rebalanceado | nan | 0 | 2.764351821938024 | 0.0359006730121821 | 0.002764351821938 | 0.7269339144807867 | 0.7221657497546325 | 0.0884059341519305 | 0.0833098056373954 | 1.061170812673792 | -0.0893304663312883 | 0.6103896103896104 | 172.69339144807867 | 172.21657497546326 | 0.4768164726154111 | 0.0 |

### 06_03_comparacao_regimes_suavizados_formatada.csv

Caminho: `outputs/tabelas/06_03_comparacao_regimes_suavizados_formatada.csv`

| cenario | rotulo | meses_confirmacao | quantidade_mudancas_regime | turnover_total | turnover_medio_mensal | custo_acumulado_simples | retorno_total_bruto | retorno_total_liquido | retorno_anualizado_liquido | volatilidade_anualizada_liquida | retorno_volatilidade_liquido | maximo_drawdown_liquido | meses_positivos | indice_final_bruto | indice_final_liquido | impacto_final_custos | diferenca_liquida_vs_benchmark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Original_1m | Regime original | 1 | 11 | 2.76 | 3.59% | 0.28% | 72.69% | 72.22% | 8.84% | 8.33% | 1.06 | -8.93% | 61.04% | 172.69 | 172.22 | 0.48 | 0.0 |
| Confirmacao_2m | Confirmação de 2 meses | 2 | 11 | 2.76 | 3.59% | 0.28% | 72.69% | 72.22% | 8.84% | 8.33% | 1.06 | -8.93% | 61.04% | 172.69 | 172.22 | 0.48 | 0.0 |
| Confirmacao_3m | Confirmação de 3 meses | 3 | 11 | 2.76 | 3.59% | 0.28% | 72.69% | 72.22% | 8.84% | 8.33% | 1.06 | -8.93% | 61.04% | 172.69 | 172.22 | 0.48 | 0.0 |
| Benchmark_Estatico | Benchmark de pesos iguais rebalanceado | - | 0 | 2.76 | 3.59% | 0.28% | 72.69% | 72.22% | 8.84% | 8.33% | 1.06 | -8.93% | 61.04% | 172.69 | 172.22 | 0.48 | 0.0 |

### 06_03_pesos_originais_por_regime.csv

Caminho: `outputs/tabelas/06_03_pesos_originais_por_regime.csv`

| regime | peso_NG=F | peso_ZC=F | peso_GC=F | peso_USDBRL=X | peso_EURBRL=X | peso_JPYBRL=X | peso_IMAB11.SA | peso_B5MB11.SA | peso_IB5M11.SA | peso_BOVV11.SA | peso_FIND11.SA | peso_MATB11.SA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 |
| EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 |
| ESTAGFLACAO | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 |
| RECESSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 |

### 06_03_series_mensais_regimes_suavizados.csv

Caminho: `outputs/tabelas/06_03_series_mensais_regimes_suavizados.csv`

| data | NG=F | ZC=F | GC=F | USDBRL=X | EURBRL=X | JPYBRL=X | IMAB11.SA | B5MB11.SA | IB5M11.SA | BOVV11.SA | FIND11.SA | MATB11.SA | regime_macro | codigo_regime | regime_sinal | codigo_regime_sinal | peso_NG=F | peso_ZC=F | peso_GC=F | peso_USDBRL=X | peso_EURBRL=X | peso_JPYBRL=X | peso_IMAB11.SA | peso_B5MB11.SA | peso_IB5M11.SA | peso_BOVV11.SA | peso_FIND11.SA | peso_MATB11.SA | soma_pesos | contribuicao_NG=F | contribuicao_ZC=F | contribuicao_GC=F | contribuicao_USDBRL=X | contribuicao_EURBRL=X | contribuicao_JPYBRL=X | contribuicao_IMAB11.SA | contribuicao_B5MB11.SA | contribuicao_IB5M11.SA | contribuicao_BOVV11.SA | contribuicao_FIND11.SA | contribuicao_MATB11.SA | retorno_portfolio_bruto | retorno_benchmark_estatico | indice_portfolio_bruto | indice_benchmark_estatico | retorno_acumulado_portfolio_bruto | retorno_acumulado_benchmark | drawdown_portfolio_bruto | drawdown_benchmark_estatico | diferenca_indice | retorno_portfolio | indice_portfolio | retorno_carteira_estatica | indice_carteira_estatica | drawdown_portfolio | drawdown_estatica | soma_pesos_validacao | turnover_portfolio | peso_estatica_NG=F | peso_estatica_ZC=F | peso_estatica_GC=F | peso_estatica_USDBRL=X | peso_estatica_EURBRL=X | peso_estatica_JPYBRL=X | peso_estatica_IMAB11.SA | peso_estatica_B5MB11.SA | peso_estatica_IB5M11.SA | peso_estatica_BOVV11.SA | peso_estatica_FIND11.SA | peso_estatica_MATB11.SA | turnover_estatica | custo_portfolio | custo_estatica | retorno_portfolio_liquido | retorno_estatica_liquido | pico_portfolio_bruto | indice_portfolio_liquido | pico_portfolio_liquido | drawdown_portfolio_liquido | indice_estatica_bruta | pico_estatica_bruta | drawdown_estatica_bruta | indice_estatica_liquida | pico_estatica_liquida | drawdown_estatica_liquida | indice_estatica_bruto | indice_estatica_liquido | retorno_cdi | cdi_disponivel | regime_confirmacao_1m | regime_confirmacao_2m | regime_confirmacao_3m | peso_Original_1m_NG=F | peso_Original_1m_ZC=F | peso_Original_1m_GC=F | peso_Original_1m_USDBRL=X | peso_Original_1m_EURBRL=X | peso_Original_1m_JPYBRL=X | peso_Original_1m_IMAB11.SA | peso_Original_1m_B5MB11.SA | peso_Original_1m_IB5M11.SA | peso_Original_1m_BOVV11.SA | peso_Original_1m_FIND11.SA | peso_Original_1m_MATB11.SA | retorno_bruto_Original_1m | turnover_Original_1m | custo_Original_1m | retorno_liquido_Original_1m | indice_bruto_Original_1m | indice_liquido_Original_1m | drawdown_liquido_Original_1m | peso_Confirmacao_2m_NG=F | peso_Confirmacao_2m_ZC=F | peso_Confirmacao_2m_GC=F | peso_Confirmacao_2m_USDBRL=X | peso_Confirmacao_2m_EURBRL=X | peso_Confirmacao_2m_JPYBRL=X | peso_Confirmacao_2m_IMAB11.SA | peso_Confirmacao_2m_B5MB11.SA | peso_Confirmacao_2m_IB5M11.SA | peso_Confirmacao_2m_BOVV11.SA | peso_Confirmacao_2m_FIND11.SA | peso_Confirmacao_2m_MATB11.SA | retorno_bruto_Confirmacao_2m | turnover_Confirmacao_2m | custo_Confirmacao_2m | retorno_liquido_Confirmacao_2m | indice_bruto_Confirmacao_2m | indice_liquido_Confirmacao_2m | drawdown_liquido_Confirmacao_2m | peso_Confirmacao_3m_NG=F | peso_Confirmacao_3m_ZC=F | peso_Confirmacao_3m_GC=F | peso_Confirmacao_3m_USDBRL=X | peso_Confirmacao_3m_EURBRL=X | peso_Confirmacao_3m_JPYBRL=X | peso_Confirmacao_3m_IMAB11.SA | peso_Confirmacao_3m_B5MB11.SA | peso_Confirmacao_3m_IB5M11.SA | peso_Confirmacao_3m_BOVV11.SA | peso_Confirmacao_3m_FIND11.SA | peso_Confirmacao_3m_MATB11.SA | retorno_bruto_Confirmacao_3m | turnover_Confirmacao_3m | custo_Confirmacao_3m | retorno_liquido_Confirmacao_3m | indice_bruto_Confirmacao_3m | indice_liquido_Confirmacao_3m | drawdown_liquido_Confirmacao_3m | peso_Benchmark_Estatico_NG=F | peso_Benchmark_Estatico_ZC=F | peso_Benchmark_Estatico_GC=F | peso_Benchmark_Estatico_USDBRL=X | peso_Benchmark_Estatico_EURBRL=X | peso_Benchmark_Estatico_JPYBRL=X | peso_Benchmark_Estatico_IMAB11.SA | peso_Benchmark_Estatico_B5MB11.SA | peso_Benchmark_Estatico_IB5M11.SA | peso_Benchmark_Estatico_BOVV11.SA | peso_Benchmark_Estatico_FIND11.SA | peso_Benchmark_Estatico_MATB11.SA | retorno_bruto_Benchmark_Estatico | turnover_Benchmark_Estatico | custo_Benchmark_Estatico | retorno_liquido_Benchmark_Estatico | indice_bruto_Benchmark_Estatico | indice_liquido_Benchmark_Estatico | diferenca_vs_benchmark_Original_1m | diferenca_vs_benchmark_Confirmacao_2m | diferenca_vs_benchmark_Confirmacao_3m |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-01-31 | -0.1324222530151464 | -0.0261813537675597 | 0.0383076578642589 | 0.0562457199465453 | 0.0420650004191165 | 0.0544411373557007 | 0.0028660919043843 | 0.025336476003539 | -0.0032191607285998 | -0.0407683973464987 | -0.0554493307839379 | -0.0300000164959873 | EXPANSAO_DESINFLACIONARIA | 1 | EXPANSAO_DESINFLACIONARIA | 1 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0110351877512622 | -0.0021817794806299 | 0.0031923048220215 | 0.0046871433288787 | 0.003505416701593 | 0.0045367614463083 | 0.000238840992032 | 0.0021113730002949 | -0.0002682633940499 | -0.0033973664455415 | -0.0046207775653281 | -0.0025000013746656 | -0.0057315357203487 | -0.0057315357203487 | 99.42684642796512 | 99.42684642796512 | -0.0057315357203487 | -0.0057315357203487 | 0.0 | 0.0 | 0.0 | -0.0057315357203487 | 99.42684642796512 | -0.0057315357203487 | 99.42684642796512 | 0.0 | 0.0 | 0.9999999999999994 | 1.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.001 | 0.001 | -0.0067258041846283 | -0.0067258041846283 | 99.42684642796512 | 99.32741958153716 | 99.32741958153716 | 0.0 | 99.42684642796512 | 99.42684642796512 | 0.0 | 99.32741958153716 | 99.32741958153716 | 0.0 | 99.42684642796512 | 99.32741958153716 | 0.0037663336752904 | True | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0057315357203487 | 1.0 | 0.001 | -0.0067258041846284 | 99.42684642796512 | 99.32741958153716 | -0.0067258041846284 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0057315357203487 | 1.0 | 0.001 | -0.0067258041846284 | 99.42684642796512 | 99.32741958153716 | -0.0067258041846284 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0057315357203487 | 1.0 | 0.001 | -0.0067258041846284 | 99.42684642796512 | 99.32741958153716 | -0.0067258041846284 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0057315357203487 | 1.0 | 0.001 | -0.0067258041846284 | 99.42684642796512 | 99.32741958153716 | 0.0 | 0.0 | 0.0 |
| 2020-02-29 | -0.0852797115562489 | -0.0386885245901633 | -0.0118769654041066 | 0.0571873013974646 | 0.0542429645851239 | 0.050012811364211 | 4.440892098500626e-16 | -0.0294401106880816 | 0.0078133140607463 | -0.0841276366030269 | -0.0538461662014483 | -0.1161883574034464 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_DESINFLACIONARIA | 1 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0071066426296874 | -0.0032240437158469 | -0.0009897471170088 | 0.0047656084497887 | 0.0045202470487603 | 0.0041677342803509 | 3.7007434154171876e-17 | -0.0024533425573401 | 0.0006511095050621 | -0.0070106363835855 | -0.0044871805167873 | -0.0096823631169538 | -0.0208492567532479 | -0.0208492567532479 | 97.35387057862272 | 97.35387057862272 | -0.0264612942137728 | -0.0264612942137728 | -0.020849256753248 | -0.020849256753248 | 0.0 | -0.0208492567532479 | 97.35387057862272 | -0.0208492567532479 | 97.35387057862272 | -0.020849256753248 | -0.020849256753248 | 0.9999999999999994 | 0.0214700289719183 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0214700289719183 | 2.147002897191834e-05 | 2.1470028971918343e-05 | -0.0208702791480732 | -0.0208702791480732 | 99.42684642796512 | 97.2544286078127 | 99.32741958153716 | -0.0208702791480731 | 97.35387057862272 | 99.42684642796512 | -0.020849256753248 | 97.2544286078127 | 99.32741958153716 | -0.0208702791480731 | 97.35387057862272 | 97.2544286078127 | 0.002937286315555 | True | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0208492567532479 | 0.0214700289719183 | 2.147002897191832e-05 | -0.0208702791480733 | 97.35387057862272 | 97.25442860781268 | -0.0274557139218732 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0208492567532479 | 0.0214700289719183 | 2.147002897191832e-05 | -0.0208702791480733 | 97.35387057862272 | 97.25442860781268 | -0.0274557139218732 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0208492567532479 | 0.0214700289719183 | 2.147002897191832e-05 | -0.0208702791480733 | 97.35387057862272 | 97.25442860781268 | -0.0274557139218732 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0208492567532479 | 0.0214700289719183 | 2.147002897191833e-05 | -0.0208702791480733 | 97.35387057862272 | 97.25442860781268 | 0.0 | 0.0 | 0.0 |
| 2020-03-31 | -0.0261282833522666 | -0.0702592087312405 | 0.0123393959013997 | 0.1578442893995921 | 0.161089495743832 | 0.1751430276323506 | -0.0750845174933443 | -0.1452014486364589 | -0.1230101487353408 | -0.3010599197751664 | -0.3311938164621636 | -0.1976670455908648 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0021773569460222 | -0.0058549340609367 | 0.0010282829917833 | 0.0131536907832993 | 0.0134241246453193 | 0.0145952523026958 | -0.0062570431244453 | -0.0121001207197049 | -0.010250845727945 | -0.0250883266479305 | -0.0275994847051803 | -0.0164722537992387 | -0.0635990150083059 | -0.0635990150083059 | 91.16226030257624 | 91.1622603025762 | -0.0883773969742379 | -0.0883773969742379 | -0.0831222795683919 | -0.0831222795683922 | 0.0 | -0.0635990150083059 | 91.1622603025762 | -0.0635990150083059 | 91.1622603025762 | -0.0831222795683922 | -0.0831222795683922 | 0.9999999999999994 | 0.0240408136397085 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0240408136397085 | 2.404081363970857e-05 | 2.404081363970856e-05 | -0.0636215268498781 | -0.0636215268498781 | 99.42684642796512 | 91.0669533668712 | 99.32741958153716 | -0.0831640069727677 | 91.16226030257624 | 99.42684642796512 | -0.0831222795683919 | 91.0669533668712 | 99.32741958153716 | -0.0831640069727677 | 91.16226030257624 | 91.0669533668712 | 0.0033836914846629 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_DESINFLACIONARIA | EXPANSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0635990150083059 | 0.0240408136397085 | 2.404081363970856e-05 | -0.0636215268498781 | 91.1622603025762 | 91.06695336687116 | -0.0893304663312883 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0635990150083059 | 0.0240408136397085 | 2.404081363970856e-05 | -0.0636215268498781 | 91.1622603025762 | 91.06695336687116 | -0.0893304663312883 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0635990150083059 | 0.0240408136397085 | 2.404081363970856e-05 | -0.0636215268498781 | 91.1622603025762 | 91.06695336687116 | -0.0893304663312883 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0635990150083059 | 0.0240408136397085 | 2.404081363970856e-05 | -0.0636215268498781 | 91.1622603025762 | 91.06695336687116 | 0.0 | 0.0 | 0.0 |
| 2020-04-30 | 0.1884146450939532 | -0.0858400586940567 | 0.0636604302157408 | 0.0273653128073669 | 0.0132224425213043 | 0.0411768572348962 | -0.007865134587025 | 0.0610820266016003 | 0.053630401321997 | 0.1036885831108966 | 0.0405629956116582 | 0.0990176218023806 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.0157012204244961 | -0.0071533382245047 | 0.0053050358513117 | 0.0022804427339472 | 0.0011018702101086 | 0.0034314047695746 | -0.000655427882252 | 0.0050901688834666 | 0.0044692001101664 | 0.0086407152592413 | 0.0033802496343048 | 0.0082514684835317 | 0.0498430102533927 | 0.0498430102533927 | 95.70606177756 | 95.70606177755997 | -0.0429393822244005 | -0.0429393822244005 | -0.037422333947812 | -0.0374223339478123 | 0.0 | 0.0498430102533927 | 95.70606177755997 | 0.0498430102533927 | 95.70606177755997 | -0.0374223339478123 | -0.0374223339478123 | 0.9999999999999994 | 0.0710417699576211 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0710417699576211 | 7.104176995762115e-05 | 7.104176995762118e-05 | 0.0497684275477665 | 0.0497684275477665 | 99.42684642796512 | 95.59921243750615 | 99.32741958153716 | -0.0375345212806073 | 95.70606177756 | 99.42684642796512 | -0.037422333947812 | 95.59921243750615 | 99.32741958153716 | -0.0375345212806073 | 95.70606177756 | 95.59921243750615 | 0.0028492490278402 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0498430102533926 | 0.0710417699576211 | 7.104176995762115e-05 | 0.0497684275477665 | 95.70606177755997 | 95.59921243750613 | -0.0440078756249388 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0498430102533926 | 0.0710417699576211 | 7.104176995762115e-05 | 0.0497684275477665 | 95.70606177755997 | 95.59921243750613 | -0.0440078756249388 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0498430102533926 | 0.0710417699576211 | 7.104176995762115e-05 | 0.0497684275477665 | 95.70606177755997 | 95.59921243750613 | -0.0440078756249388 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0498430102533926 | 0.0710417699576211 | 7.104176995762118e-05 | 0.0497684275477665 | 95.70606177755997 | 95.59921243750613 | 0.0 | 0.0 | 0.0 |
| 2020-05-31 | -0.0513083754709727 | 0.0457463884430187 | 0.0312908649626313 | 0.0128965382736307 | 0.0315473887353219 | 0.0031375372138198 | 0.0389297851608276 | 0.0142544199041538 | -0.0071596307642725 | 0.0856541414844245 | 0.0393506758515871 | 0.1290668823373175 | RECESSAO_DESINFLACIONARIA | 4 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0042756979559143 | 0.0038121990369182 | 0.0026075720802192 | 0.0010747115228025 | 0.0026289490612768 | 0.0002614614344849 | 0.0032441487634023 | 0.0011878683253461 | -0.0005966358970227 | 0.007137845123702 | 0.0032792229876322 | 0.0107555735281097 | 0.0311172180109573 | 0.0311172180109573 | 98.68416816686248 | 98.68416816686243 | -0.0131583183313757 | -0.0131583183313757 | -0.0074695948607876 | -0.0074695948607879 | 0.0 | 0.0311172180109573 | 98.68416816686243 | 0.0311172180109573 | 98.68416816686243 | -0.0074695948607879 | -0.0074695948607879 | 0.9999999999999994 | 0.0214663560793516 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0214663560793515 | 2.14663560793516e-05 | 2.1466356079351583e-05 | 0.0310950836815959 | 0.0310950836815959 | 99.42684642796512 | 98.57187794814509 | 99.32741958153716 | -0.0076065766791804 | 98.68416816686248 | 99.42684642796512 | -0.0074695948607876 | 98.57187794814509 | 99.32741958153716 | -0.0076065766791804 | 98.68416816686248 | 98.57187794814509 | 0.0023580961930711 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0311172180109573 | 0.0214663560793515 | 2.146635607935158e-05 | 0.0310950836815959 | 98.68416816686243 | 98.57187794814504 | -0.0142812205185495 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0311172180109573 | 0.0214663560793515 | 2.146635607935158e-05 | 0.0310950836815959 | 98.68416816686243 | 98.57187794814504 | -0.0142812205185495 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0311172180109573 | 0.0214663560793515 | 2.146635607935158e-05 | 0.0310950836815959 | 98.68416816686243 | 98.57187794814504 | -0.0142812205185495 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0311172180109573 | 0.0214663560793515 | 2.1466356079351583e-05 | 0.0310950836815959 | 98.68416816686243 | 98.57187794814504 | 0.0 | 0.0 | 0.0 |
| 2020-06-30 | -0.0530015855029117 | 0.0391404451266315 | 0.0322989088591116 | -0.0002776167073367 | 0.015040635311132 | 0.0003386357572798 | 0.0279330027089084 | 0.0270270270270274 | 0.0251267983879845 | 0.0902975516088846 | 0.1310932592419071 | 0.0421152605104246 | RECESSAO_DESINFLACIONARIA | 4 | RECESSAO_DESINFLACIONARIA | 4 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0044167987919093 | 0.0032617037605526 | 0.0026915757382593 | -2.313472561139377e-05 | 0.0012533862759276 | 2.821964643999012e-05 | 0.0023277502257423 | 0.0022522522522522 | 0.0020938998656653 | 0.007524795967407 | 0.0109244382701589 | 0.0035096050425353 | 0.0314276935274202 | 0.0314276935274203 | 101.78558396001904 | 101.785583960019 | 0.0178558396001899 | 0.0178558396001899 | 0.0 | 0.0 | 0.0 | 0.0314276935274202 | 101.785583960019 | 0.0314276935274203 | 101.785583960019 | 0.0 | 0.0 | 0.9999999999999994 | 0.0148516578012435 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0148516578012435 | 1.4851657801243555e-05 | 1.4851657801243506e-05 | 0.0314123751162691 | 0.0314123751162691 | 101.78558396001904 | 101.66825475416732 | 101.66825475416732 | 0.0 | 101.78558396001904 | 101.78558396001904 | 0.0 | 101.66825475416732 | 101.66825475416732 | 0.0 | 101.78558396001904 | 101.66825475416732 | 0.0021233217736713 | True | RECESSAO_DESINFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0314276935274202 | 0.0148516578012435 | 1.4851657801243506e-05 | 0.0314123751162691 | 101.785583960019 | 101.66825475416728 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0314276935274202 | 0.0148516578012435 | 1.4851657801243506e-05 | 0.0314123751162691 | 101.785583960019 | 101.66825475416728 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0314276935274202 | 0.0148516578012435 | 1.4851657801243506e-05 | 0.0314123751162691 | 101.785583960019 | 101.66825475416728 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0314276935274202 | 0.0148516578012435 | 1.4851657801243506e-05 | 0.0314123751162691 | 101.785583960019 | 101.66825475416728 | 0.0 | 0.0 | 0.0 |
| 2020-07-31 | 0.0274128936519058 | -0.0664697193500737 | 0.0947016446336452 | -0.0459450835354313 | 0.0069972699899409 | -0.0195363707301123 | 0.0503710935761791 | 0.0727368806537831 | 0.08078696639838 | 0.0824009736393767 | 0.0978033328803054 | 0.0969309827255997 | RECESSAO_DESINFLACIONARIA | 4 | RECESSAO_DESINFLACIONARIA | 4 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.0022844078043254 | -0.0055391432791728 | 0.0078918037194704 | -0.0038287569612859 | 0.000583105832495 | -0.001628030894176 | 0.0041975911313482 | 0.0060614067211485 | 0.006732247199865 | 0.0068667478032813 | 0.0081502777400254 | 0.0080775818937999 | 0.0398492387111249 | 0.0398492387111249 | 105.84166199259306 | 105.84166199259305 | 0.0584166199259303 | 0.0584166199259303 | 0.0 | 0.0 | 0.0 | 0.0398492387111249 | 105.84166199259305 | 0.0398492387111249 | 105.84166199259305 | 0.0 | 0.0 | 0.9999999999999994 | 0.0143657636582816 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0143657636582816 | 1.4365763658281627e-05 | 1.4365763658281676e-05 | 0.0398343004827213 | 0.0398343004827213 | 105.84166199259306 | 105.71813856359869 | 105.71813856359869 | 0.0 | 105.84166199259306 | 105.84166199259306 | 0.0 | 105.71813856359869 | 105.71813856359869 | 0.0 | 105.84166199259306 | 105.71813856359869 | 0.0019434641302638 | True | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0398492387111248 | 0.0143657636582816 | 1.4365763658281665e-05 | 0.0398343004827213 | 105.84166199259305 | 105.71813856359864 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0398492387111248 | 0.0143657636582816 | 1.4365763658281665e-05 | 0.0398343004827213 | 105.84166199259305 | 105.71813856359864 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0398492387111248 | 0.0143657636582816 | 1.4365763658281665e-05 | 0.0398343004827213 | 105.84166199259305 | 105.71813856359864 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0398492387111248 | 0.0143657636582816 | 1.4365763658281676e-05 | 0.0398343004827213 | 105.84166199259305 | 105.71813856359864 | 0.0 | 0.0 | 0.0 |
| 2020-08-31 | 0.4619233341810744 | 0.1028481012658228 | 0.0024454486643601 | 0.0458099135200109 | 0.0482480797448408 | 0.0370889330663726 | -0.0106006607841498 | -0.0305171278441224 | -0.0283738519635227 | -0.0351656778526355 | -0.0833730372028046 | 0.1080332878317076 | RECESSAO_DESINFLACIONARIA | 4 | RECESSAO_DESINFLACIONARIA | 4 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.0384936111817562 | 0.0085706751054852 | 0.0002037873886966 | 0.0038174927933342 | 0.00402067331207 | 0.0030907444221977 | -0.0008833883986791 | -0.0025430939870102 | -0.0023644876636268 | -0.0029304731543862 | -0.0069477531002337 | 0.0090027739859756 | 0.0515305618855795 | 0.0515305618855795 | 111.29574230597495 | 111.29574230597494 | 0.1129574230597494 | 0.1129574230597494 | 0.0 | 0.0 | 0.0 | 0.0515305618855795 | 111.29574230597494 | 0.0515305618855795 | 111.29574230597494 | 0.0 | 0.0 | 0.9999999999999994 | 0.0237844737872176 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0237844737872176 | 2.3784473787217624e-05 | 2.3784473787217603e-05 | 0.0515055517844937 | 0.0515055517844937 | 111.29574230597495 | 111.1632096239464 | 111.1632096239464 | 0.0 | 111.29574230597495 | 111.29574230597495 | 0.0 | 111.1632096239464 | 111.1632096239464 | 0.0 | 111.29574230597495 | 111.1632096239464 | 0.0015988959789294 | True | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0515305618855794 | 0.0237844737872175 | 2.378447378721759e-05 | 0.0515055517844937 | 111.29574230597494 | 111.16320962394636 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0515305618855794 | 0.0237844737872175 | 2.378447378721759e-05 | 0.0515055517844937 | 111.29574230597494 | 111.16320962394636 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0515305618855794 | 0.0237844737872175 | 2.378447378721759e-05 | 0.0515055517844937 | 111.29574230597494 | 111.16320962394636 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0515305618855795 | 0.0237844737872176 | 2.3784473787217603e-05 | 0.0515055517844937 | 111.29574230597494 | 111.16320962394636 | 0.0 | 0.0 | 0.0 |
| 2020-09-30 | -0.0391635587642843 | 0.0875179340028695 | -0.040709481896636 | 0.0446196621993484 | 0.0309137209869638 | 0.0436162260071208 | -0.0246173503522019 | -0.0293522412581268 | -0.0370525526649014 | -0.048162662017678 | -0.0597713116674375 | 0.0069999694824223 | RECESSAO_DESINFLACIONARIA | 4 | RECESSAO_DESINFLACIONARIA | 4 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0032636298970236 | 0.0072931611669057 | -0.0033924568247196 | 0.003718305183279 | 0.0025761434155803 | 0.0036346855005934 | -0.0020514458626834 | -0.0024460201048439 | -0.0030877127220751 | -0.0040135551681398 | -0.0049809426389531 | 0.0005833307902018 | -0.0054301371618784 | -0.0054301371618784 | 110.69139115972048 | 110.69139115972042 | 0.1069139115972042 | 0.1069139115972042 | -0.0054301371618782 | -0.0054301371618783 | 0.0 | -0.0054301371618784 | 110.69139115972042 | -0.0054301371618784 | 110.69139115972042 | -0.0054301371618783 | -0.0054301371618783 | 0.9999999999999994 | 0.0410681547138152 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0410681547138153 | 4.106815471381529e-05 | 4.106815471381536e-05 | -0.005470982310879 | -0.005470982310879 | 111.29574230597495 | 110.55503767047324 | 111.1632096239464 | -0.0054709823108791 | 110.69139115972048 | 111.29574230597495 | -0.0054301371618782 | 110.55503767047324 | 111.1632096239464 | -0.0054709823108791 | 110.69139115972048 | 110.55503767047324 | 0.0015696620595304 | True | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0054301371618784 | 0.0410681547138153 | 4.106815471381533e-05 | -0.0054709823108791 | 110.69139115972042 | 110.5550376704732 | -0.0054709823108791 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0054301371618784 | 0.0410681547138153 | 4.106815471381533e-05 | -0.0054709823108791 | 110.69139115972042 | 110.5550376704732 | -0.0054709823108791 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0054301371618784 | 0.0410681547138153 | 4.106815471381533e-05 | -0.0054709823108791 | 110.69139115972042 | 110.5550376704732 | -0.0054709823108791 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0054301371618784 | 0.0410681547138153 | 4.106815471381536e-05 | -0.0054709823108791 | 110.69139115972042 | 110.5550376704732 | 0.0 | 0.0 | 0.0 |
| 2020-10-31 | 0.3272655945283924 | 0.0514511873350929 | -0.0053509804428802 | 0.0261611309065188 | 0.0203643429464523 | 0.037176698975913 | 0.0125539305498638 | -0.0034411035016052 | 0.0244565217391308 | -0.0069429418226945 | -0.0101713454945908 | 0.0600794949598271 | EXPANSAO_INFLACIONARIA | 2 | RECESSAO_DESINFLACIONARIA | 4 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.027272132877366 | 0.004287598944591 | -0.0004459150369066 | 0.0021800942422099 | 0.001697028578871 | 0.0030980582479927 | 0.0010461608791553 | -0.0002867586251337 | 0.0020380434782609 | -0.0005785784852245 | -0.0008476121245492 | 0.0050066245799855 | 0.0444668775566183 | 0.0444668775566183 | 115.61349169699152 | 115.61349169699146 | 0.1561349169699146 | 0.1561349169699146 | 0.0 | 0.0 | 0.0 | 0.0444668775566183 | 115.61349169699146 | 0.0444668775566183 | 115.61349169699146 | 0.0 | 0.0 | 0.9999999999999994 | 0.0201777511637806 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0201777511637806 | 2.017775116378064e-05 | 2.0177751163780672e-05 | 0.0444458025638641 | 0.0444458025638641 | 115.61349169699152 | 115.46874504721568 | 115.46874504721568 | 0.0 | 115.61349169699152 | 115.61349169699152 | 0.0 | 115.46874504721568 | 115.46874504721568 | 0.0 | 115.61349169699152 | 115.46874504721568 | 0.0015696620595304 | True | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0444668775566183 | 0.0201777511637806 | 2.0177751163780666e-05 | 0.0444458025638641 | 115.61349169699146 | 115.46874504721562 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0444668775566183 | 0.0201777511637806 | 2.0177751163780666e-05 | 0.0444458025638641 | 115.61349169699146 | 115.46874504721562 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0444668775566183 | 0.0201777511637806 | 2.0177751163780666e-05 | 0.0444458025638641 | 115.61349169699146 | 115.46874504721562 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0444668775566183 | 0.0201777511637806 | 2.0177751163780672e-05 | 0.0444458025638641 | 115.61349169699146 | 115.46874504721562 | 0.0 | 0.0 | 0.0 |
| 2020-11-30 | -0.1407275221187603 | 0.0533249686323715 | -0.0541706998613292 | -0.0753400718416592 | -0.052608198485068 | -0.0712721718037842 | 0.0021955077912345 | 0.0280422759624732 | -0.0026525198938988 | 0.1611228690531638 | 0.1792695551278085 | 0.1444964416558152 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0117272935098966 | 0.0044437473860309 | -0.0045142249884441 | -0.0062783393201382 | -0.0043840165404223 | -0.0059393476503153 | 0.0001829589826028 | 0.0023368563302061 | -0.0002210433244915 | 0.0134269057544303 | 0.014939129593984 | 0.0120413701379846 | 0.0143067028515305 | 0.0143067028515305 | 117.26753956832825 | 117.26753956832825 | 0.1726753956832822 | 0.1726753956832822 | 0.0 | 0.0 | 0.0 | 0.0143067028515305 | 117.26753956832825 | 0.0143067028515305 | 117.26753956832825 | 0.0 | 0.0 | 0.9999999999999994 | 0.0243661503870029 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.024366150387003 | 2.4366150387002967e-05 | 2.436615038700308e-05 | 0.0142819881018703 | 0.0142819881018703 | 117.26753956832825 | 117.1178682901179 | 117.1178682901179 | 0.0 | 117.26753956832825 | 117.26753956832825 | 0.0 | 117.1178682901179 | 117.1178682901179 | 0.0 | 117.26753956832825 | 117.1178682901179 | 0.0014948604084066 | True | EXPANSAO_INFLACIONARIA | RECESSAO_DESINFLACIONARIA | RECESSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0143067028515305 | 0.024366150387003 | 2.436615038700308e-05 | 0.0142819881018705 | 117.26753956832825 | 117.11786829011788 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0143067028515305 | 0.024366150387003 | 2.436615038700308e-05 | 0.0142819881018705 | 117.26753956832825 | 117.11786829011788 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0143067028515305 | 0.024366150387003 | 2.436615038700308e-05 | 0.0142819881018705 | 117.26753956832825 | 117.11786829011788 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0143067028515305 | 0.024366150387003 | 2.436615038700308e-05 | 0.0142819881018705 | 117.26753956832825 | 117.11786829011788 | 0.0 | 0.0 | 0.0 |
| 2020-12-31 | -0.1596113959118407 | 0.1304347826086962 | 0.0649321687214288 | -0.0250632026765348 | -0.0014398998533002 | -0.0199306080486962 | 0.0463917338261508 | 0.071246819338423 | 0.0509574565481636 | 0.0907763606681577 | 0.1212350369423691 | 0.1158174743425113 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.01330094965932 | 0.0108695652173913 | 0.005411014060119 | -0.0020886002230445 | -0.0001199916544416 | -0.001660884004058 | 0.0038659778188459 | 0.0059372349448685 | 0.0042464547123469 | 0.0075646967223464 | 0.0101029197451974 | 0.0096514561952092 | 0.0404788938754607 | 0.0404788938754607 | 122.014399857551 | 122.01439985755098 | 0.2201439985755098 | 0.2201439985755098 | 0.0 | 0.0 | 0.0 | 0.0404788938754607 | 122.01439985755098 | 0.0404788938754607 | 122.01439985755098 | 0.0 | 0.0 | 0.9999999999999994 | 0.0406453816174108 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0406453816174109 | 4.06453816174109e-05 | 4.064538161741092e-05 | 0.0404366032137544 | 0.0404366032137544 | 122.014399857551 | 121.85371705940616 | 121.85371705940616 | 0.0 | 122.014399857551 | 122.014399857551 | 0.0 | 121.85371705940616 | 121.85371705940616 | 0.0 | 122.014399857551 | 121.85371705940616 | 0.0016444692975896 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | RECESSAO_DESINFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0404788938754607 | 0.0406453816174108 | 4.06453816174109e-05 | 0.0404366032137544 | 122.01439985755098 | 121.85371705940614 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0404788938754607 | 0.0406453816174108 | 4.06453816174109e-05 | 0.0404366032137544 | 122.01439985755098 | 121.85371705940614 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0404788938754607 | 0.0406453816174108 | 4.06453816174109e-05 | 0.0404366032137544 | 122.01439985755098 | 121.85371705940614 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0404788938754607 | 0.0406453816174109 | 4.064538161741092e-05 | 0.0404366032137544 | 122.01439985755098 | 121.85371705940614 | 0.0 | 0.0 | 0.0 |
| 2021-01-31 | 0.0586292171640903 | 0.1527924130663862 | -0.0231094400697375 | 0.0440404693631728 | 0.0328046211995005 | 0.0362985670684796 | 2.220446049250313e-16 | -0.0137766930949376 | -0.0049599945260498 | -0.034376051307104 | -0.0606521411704832 | -0.00146704599575 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.0048857680970075 | 0.0127327010888655 | -0.0019257866724781 | 0.0036700391135977 | 0.0027337184332917 | 0.0030248805890399 | 1.8503717077085938e-17 | -0.0011480577579114 | -0.0004133328771708 | -0.0028646709422586 | -0.0050543450975402 | -0.0001222538329791 | 0.0155186601414639 | 0.0155186601414639 | 123.907899861305 | 123.907899861305 | 0.2390789986130499 | 0.2390789986130499 | 0.0 | 0.0 | 0.0 | 0.0155186601414639 | 123.907899861305 | 0.0155186601414639 | 123.907899861305 | 0.0 | 0.0 | 0.9999999999999994 | 0.0294704585998917 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0294704585998917 | 2.9470458599891783e-05 | 2.947045859989174e-05 | 0.0154887323408328 | 0.0154887323408328 | 123.907899861305 | 123.74107666767486 | 123.74107666767486 | 0.0 | 123.907899861305 | 123.907899861305 | 0.0 | 123.74107666767486 | 123.74107666767486 | 0.0 | 123.907899861305 | 123.74107666767486 | 0.0014948604084066 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0155186601414639 | 0.0294704585998917 | 2.9470458599891705e-05 | 0.0154887323408328 | 123.907899861305 | 123.74107666767485 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0155186601414639 | 0.0294704585998917 | 2.9470458599891705e-05 | 0.0154887323408328 | 123.907899861305 | 123.74107666767485 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0155186601414639 | 0.0294704585998917 | 2.9470458599891705e-05 | 0.0154887323408328 | 123.907899861305 | 123.74107666767485 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0155186601414639 | 0.0294704585998917 | 2.947045859989174e-05 | 0.0154887323408328 | 123.907899861305 | 123.74107666767485 | 0.0 | 0.0 | 0.0 |
| 2021-02-28 | 0.0807332394474913 | 0.0155393053016454 | -0.064526644341185 | 0.0165568395752833 | 0.0201988062535969 | -0.0031267398318779 | -0.0169950407054518 | -0.0183044457612536 | -0.019125176240559 | -0.0451277541982815 | -0.0737409817741164 | 0.101010099594774 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.0067277699539576 | 0.0012949421084704 | -0.0053772203617654 | 0.0013797366312736 | 0.0016832338544664 | -0.0002605616526564 | -0.0014162533921209 | -0.0015253704801044 | -0.0015937646867132 | -0.0037606461831901 | -0.0061450818145097 | 0.0084175082995645 | -0.0005757077233278 | -0.0005757077233278 | 123.83656512637351 | 123.83656512637349 | 0.2383656512637348 | 0.2383656512637348 | -0.0005757077233278 | -0.000575707723328 | 0.0 | -0.0005757077233278 | 123.83656512637349 | -0.0005757077233278 | 123.83656512637349 | -0.000575707723328 | -0.000575707723328 | 0.9999999999999994 | 0.0202664901565263 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0202664901565263 | 2.0266490156526324e-05 | 2.026649015652635e-05 | -0.0005959625459094 | -0.0005959625459094 | 123.907899861305 | 123.66733162059045 | 123.74107666767486 | -0.0005959625459093 | 123.83656512637351 | 123.907899861305 | -0.0005757077233278 | 123.66733162059045 | 123.74107666767486 | -0.0005959625459093 | 123.83656512637351 | 123.66733162059045 | 0.0013452738652959 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0005757077233278 | 0.0202664901565263 | 2.026649015652635e-05 | -0.0005959625459094 | 123.83656512637351 | 123.6673316205904 | -0.0005959625459094 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0005757077233278 | 0.0202664901565263 | 2.026649015652635e-05 | -0.0005959625459094 | 123.83656512637351 | 123.6673316205904 | -0.0005959625459094 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0005757077233278 | 0.0202664901565263 | 2.026649015652635e-05 | -0.0005959625459094 | 123.83656512637351 | 123.6673316205904 | -0.0005959625459094 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0005757077233278 | 0.0202664901565263 | 2.026649015652636e-05 | -0.0005959625459094 | 123.83656512637351 | 123.6673316205904 | 0.0 | 0.0 | 0.0 |
| 2021-03-31 | -0.0588234838608421 | 0.0157515751575165 | -0.0082749418204015 | 0.0440617784237178 | 0.0060690945030739 | 0.0064654946855386 | -0.004760677209606 | -0.0186457458040012 | -0.0130677715283523 | 0.0618650202012183 | 0.0630096879977628 | 0.0558798737529293 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0049019569884035 | 0.0013126312631263 | -0.0006895784850334 | 0.0036718148686431 | 0.0005057578752561 | 0.0005387912237948 | -0.0003967231008005 | -0.0015538121503334 | -0.001088980960696 | 0.0051554183501015 | 0.0052508073331469 | 0.0046566561460774 | 0.0124608253748795 | 0.0124608253748795 | 125.37967093943816 | 125.37967093943811 | 0.2537967093943811 | 0.2537967093943811 | 0.0 | 0.0 | 0.0 | 0.0124608253748795 | 125.37967093943811 | 0.0124608253748795 | 125.37967093943811 | 0.0 | 0.0 | 0.9999999999999994 | 0.0197544418505292 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0197544418505292 | 1.975444185052921e-05 | 1.975444185052923e-05 | 0.0124408247763787 | 0.0124408247763787 | 125.37967093943816 | 125.20585522384452 | 125.20585522384452 | 0.0 | 125.37967093943816 | 125.37967093943816 | 0.0 | 125.20585522384452 | 125.20585522384452 | 0.0 | 125.37967093943816 | 125.20585522384452 | 0.0020107988327939 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0124608253748795 | 0.0197544418505292 | 1.975444185052923e-05 | 0.0124408247763787 | 125.37967093943814 | 125.20585522384448 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0124608253748795 | 0.0197544418505292 | 1.975444185052923e-05 | 0.0124408247763787 | 125.37967093943814 | 125.20585522384448 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0124608253748795 | 0.0197544418505292 | 1.975444185052923e-05 | 0.0124408247763787 | 125.37967093943814 | 125.20585522384448 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0124608253748795 | 0.0197544418505292 | 1.975444185052924e-05 | 0.0124408247763787 | 125.37967093943814 | 125.20585522384448 | 0.0 | 0.0 | 0.0 |
| 2021-04-30 | 0.1238496737971313 | 0.3114754098360659 | 0.0312171773110774 | -0.0754036584174941 | -0.0436910836373519 | -0.0629779473980781 | 0.0187562665908598 | 0.0069999694824225 | 0.0101932908152553 | 0.0192209127535121 | 0.0113252855727241 | 0.1287519401170866 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.0103208061497609 | 0.0259562841530054 | 0.0026014314425897 | -0.0062836382014578 | -0.0036409236364459 | -0.0052481622831731 | 0.0015630222159049 | 0.0005833307902018 | 0.0008494409012712 | 0.0016017427294593 | 0.000943773797727 | 0.0107293283430905 | 0.0399764364019342 | 0.0399764364019342 | 130.39190338084404 | 130.39190338084398 | 0.3039190338084399 | 0.3039190338084399 | 0.0 | 0.0 | 0.0 | 0.0399764364019342 | 130.39190338084398 | 0.0399764364019342 | 130.39190338084398 | 0.0 | 0.0 | 0.9999999999999994 | 0.0146724861011076 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0146724861011077 | 1.4672486101107655e-05 | 1.4672486101107704e-05 | 0.0399611773621255 | 0.0399611773621255 | 130.39190338084404 | 130.20922861122116 | 130.20922861122116 | 0.0 | 130.39190338084404 | 130.39190338084404 | 0.0 | 130.20922861122116 | 130.20922861122116 | 0.0 | 130.39190338084404 | 130.20922861122116 | 0.002077848024335 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0399764364019342 | 0.0146724861011076 | 1.4672486101107698e-05 | 0.0399611773621255 | 130.391903380844 | 130.20922861122116 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0399764364019342 | 0.0146724861011076 | 1.4672486101107698e-05 | 0.0399611773621255 | 130.391903380844 | 130.20922861122116 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0399764364019342 | 0.0146724861011076 | 1.4672486101107698e-05 | 0.0399611773621255 | 130.391903380844 | 130.20922861122116 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0399764364019342 | 0.0146724861011077 | 1.4672486101107704e-05 | 0.0399611773621255 | 130.391903380844 | 130.20922861122116 | 0.0 | 0.0 | 0.0 |
| 2021-05-31 | 0.0187649494590842 | -0.1124999999999996 | 0.076500847301806 | -0.0184018896204722 | -0.0129871575619555 | -0.0267904690338767 | 0.002842003658301 | 0.0105263676277287 | 0.0195569014514425 | 0.058251653003543 | 0.0701706530073891 | -0.0456262371739136 | ESTAGFLACAO | 3 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.001563745788257 | -0.0093749999999999 | 0.0063750706084838 | -0.001533490801706 | -0.0010822631301629 | -0.0022325390861563 | 0.0002368336381917 | 0.0008771973023107 | 0.0016297417876202 | 0.0048543044169619 | 0.0058475544172824 | -0.0038021864311594 | 0.003358968509923 | 0.003358968509923 | 130.8298856782492 | 130.82988567824918 | 0.3082988567824918 | 0.3082988567824918 | 0.0 | 0.0 | 0.0 | 0.003358968509923 | 130.82988567824918 | 0.003358968509923 | 130.82988567824918 | 0.0 | 0.0 | 0.9999999999999994 | 0.0355895655419145 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0355895655419146 | 3.558956554191451e-05 | 3.558956554191461e-05 | 0.0033232594001511 | 0.0033232594001511 | 130.8298856782492 | 130.64194765418983 | 130.64194765418983 | 0.0 | 130.8298856782492 | 130.8298856782492 | 0.0 | 130.64194765418983 | 130.64194765418983 | 0.0 | 130.8298856782492 | 130.64194765418983 | 0.0027032626398217 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.003358968509923 | 0.0355895655419145 | 3.558956554191455e-05 | 0.0033232594001513 | 130.8298856782492 | 130.64194765418983 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.003358968509923 | 0.0355895655419145 | 3.558956554191455e-05 | 0.0033232594001513 | 130.8298856782492 | 130.64194765418983 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.003358968509923 | 0.0355895655419145 | 3.558956554191455e-05 | 0.0033232594001513 | 130.8298856782492 | 130.64194765418983 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.003358968509923 | 0.0355895655419145 | 3.558956554191457e-05 | 0.0033232594001513 | 130.8298856782492 | 130.64194765418983 | 0.0 | 0.0 | 0.0 |
| 2021-06-30 | 0.2223710719222447 | 0.0963075751808146 | -0.0692246786711557 | -0.0540453052633409 | -0.0765833067485982 | -0.0601924495097703 | -0.012444579727169 | 0.0062893020461189 | 0.0029588910234308 | 0.009662610486786 | -0.0042194092827 | 0.0013197878672603 | ESTAGFLACAO | 3 | ESTAGFLACAO | 3 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.018530922660187 | 0.0080256312650678 | -0.0057687232225963 | -0.0045037754386117 | -0.0063819422290498 | -0.0050160374591475 | -0.0010370483105974 | 0.0005241085038432 | 0.0002465742519525 | 0.0008052175405655 | -0.000351617440225 | 0.0001099823222716 | 0.0051832924436601 | 0.0051832924436601 | 131.5080152360902 | 131.50801523609016 | 0.3150801523609017 | 0.3150801523609017 | 0.0 | 0.0 | 0.0 | 0.0051832924436601 | 131.50801523609016 | 0.0051832924436601 | 131.50801523609016 | 0.0 | 0.0 | 0.9999999999999994 | 0.0194029561472565 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0194029561472565 | 1.9402956147256542e-05 | 1.940295614725654e-05 | 0.0051637889163169 | 0.0051637889163169 | 131.5080152360902 | 131.31655509549262 | 131.31655509549262 | 0.0 | 131.5080152360902 | 131.5080152360902 | 0.0 | 131.31655509549262 | 131.31655509549262 | 0.0 | 131.5080152360902 | 131.31655509549262 | 0.0030777896833165 | True | ESTAGFLACAO | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0051832924436601 | 0.0194029561472565 | 1.940295614725653e-05 | 0.0051637889163169 | 131.5080152360902 | 131.31655509549262 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0051832924436601 | 0.0194029561472565 | 1.940295614725653e-05 | 0.0051637889163169 | 131.5080152360902 | 131.31655509549262 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0051832924436601 | 0.0194029561472565 | 1.940295614725653e-05 | 0.0051637889163169 | 131.5080152360902 | 131.31655509549262 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0051832924436601 | 0.0194029561472565 | 1.940295614725654e-05 | 0.0051637889163169 | 131.5080152360902 | 131.31655509549262 | 0.0 | 0.0 | 0.0 |
| 2021-07-31 | 0.0723287485115169 | -0.2402777777777772 | 0.0236051082026313 | 0.0252870636450719 | 0.024376611246514 | 0.0358273923932506 | 0.0063630957769329 | -0.0039062648429535 | -0.0043743671599811 | -0.0393787585524713 | -0.0381355932203383 | -0.0174282727399082 | ESTAGFLACAO | 3 | ESTAGFLACAO | 3 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.006027395709293 | -0.0200231481481481 | 0.0019670923502192 | 0.0021072553037559 | 0.0020313842705428 | 0.0029856160327708 | 0.000530257981411 | -0.0003255220702461 | -0.000364530596665 | -0.0032815632127059 | -0.0031779661016948 | -0.001452356061659 | -0.0129760845431259 | -0.0129760845431259 | 129.80155611228798 | 129.80155611228795 | 0.2980155611228796 | 0.2980155611228796 | -0.0129760845431259 | -0.0129760845431259 | 0.0 | -0.0129760845431259 | 129.80155611228795 | -0.0129760845431259 | 129.80155611228795 | -0.0129760845431259 | -0.0129760845431259 | 0.9999999999999994 | 0.0260232298113362 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0260232298113362 | 2.60232298113362e-05 | 2.6023229811336256e-05 | -0.0130017700933071 | -0.0130017700933071 | 131.5080152360902 | 129.6092074366959 | 131.31655509549262 | -0.0130017700933073 | 129.80155611228798 | 131.5080152360902 | -0.0129760845431259 | 129.6092074366959 | 131.31655509549262 | -0.0130017700933073 | 129.80155611228798 | 129.6092074366959 | 0.0035561617801918 | True | ESTAGFLACAO | ESTAGFLACAO | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0129760845431259 | 0.0260232298113362 | 2.602322981133625e-05 | -0.0130017700933072 | 129.80155611228798 | 129.6092074366959 | -0.0130017700933073 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0129760845431259 | 0.0260232298113362 | 2.602322981133625e-05 | -0.0130017700933072 | 129.80155611228798 | 129.6092074366959 | -0.0130017700933073 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0129760845431259 | 0.0260232298113362 | 2.602322981133625e-05 | -0.0130017700933072 | 129.80155611228798 | 129.6092074366959 | -0.0130017700933073 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.012976084543126 | 0.0260232298113362 | 2.6023229811336256e-05 | -0.0130017700933072 | 129.80155611228798 | 129.6092074366959 | 0.0 | 0.0 | 0.0 |
| 2021-08-31 | 0.1182932592355527 | -0.0237659963436922 | 0.0013240783660981 | 0.0201755692569745 | 0.0121217725230882 | 0.0151189085040535 | -0.0112819690155405 | -0.0232353210449215 | -0.0242158238486897 | -0.0263759248055441 | -0.0298678360321443 | -0.0423311446253067 | ESTAGFLACAO | 3 | ESTAGFLACAO | 3 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.0098577716029627 | -0.0019804996953076 | 0.0001103398638415 | 0.0016812974380812 | 0.0010101477102573 | 0.0012599090420044 | -0.0009401640846283 | -0.0019362767537434 | -0.0020179853207241 | -0.0021979937337953 | -0.002488986336012 | -0.0035275953854422 | -0.001170035652506 | -0.001170035652506 | 129.64968366388584 | 129.64968366388584 | 0.2964968366388583 | 0.2964968366388583 | -0.0141309377140866 | -0.0141309377140864 | 0.0 | -0.001170035652506 | 129.64968366388584 | -0.001170035652506 | 129.64968366388584 | -0.0141309377140864 | -0.0141309377140864 | 0.9999999999999994 | 0.0239200607402751 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0239200607402751 | 2.392006074027514e-05 | 2.392006074027513e-05 | -0.0011939277259223 | -0.0011939277259223 | 131.5080152360902 | 129.4544634104024 | 131.31655509549262 | -0.0141801746454292 | 129.64968366388584 | 131.5080152360902 | -0.0141309377140866 | 129.4544634104024 | 131.31655509549262 | -0.0141801746454292 | 129.64968366388584 | 129.4544634104024 | 0.0042795247734248 | True | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0011700356525059 | 0.0239200607402751 | 2.392006074027512e-05 | -0.0011939277259223 | 129.64968366388584 | 129.45446341040238 | -0.0141801746454294 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0011700356525059 | 0.0239200607402751 | 2.392006074027512e-05 | -0.0011939277259223 | 129.64968366388584 | 129.45446341040238 | -0.0141801746454294 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0011700356525059 | 0.0239200607402751 | 2.392006074027512e-05 | -0.0011939277259223 | 129.64968366388584 | 129.45446341040238 | -0.0141801746454294 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.001170035652506 | 0.0239200607402751 | 2.392006074027513e-05 | -0.0011939277259223 | 129.64968366388584 | 129.45446341040238 | 0.0 | 0.0 | 0.0 |
| 2021-09-30 | 0.3404158778390447 | 0.0051498127340829 | -0.0328925350809224 | 0.0446468222647424 | 0.027258337238776 | 0.0260109574147651 | 0.0048902744783503 | -0.0066244710519872 | -0.0071204220437246 | -0.0656714049366781 | -0.0850059082596315 | -0.0978988469342776 | ESTAGFLACAO | 3 | ESTAGFLACAO | 3 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.0283679898199203 | 0.0004291510611735 | -0.0027410445900768 | 0.0037205685220618 | 0.0022715281032313 | 0.0021675797845637 | 0.0004075228731958 | -0.0005520392543322 | -0.0005933685036437 | -0.0054726170780565 | -0.0070838256883026 | -0.0081582372445231 | 0.0127632078052116 | 0.0127632078052116 | 131.30442951836795 | 131.30442951836793 | 0.3130442951836791 | 0.3130442951836791 | -0.0015480860034025 | -0.0015480860034025 | 0.0 | 0.0127632078052116 | 131.30442951836793 | 0.0127632078052116 | 131.30442951836793 | -0.0015480860034025 | -0.0015480860034025 | 0.9999999999999994 | 0.0144238569392235 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0144238569392236 | 1.4423856939223589e-05 | 1.442385693922363e-05 | 0.012748599853589 | 0.012748599853589 | 131.5080152360902 | 131.1048265636827 | 131.31655509549262 | -0.0016123521642488 | 131.30442951836795 | 131.5080152360902 | -0.0015480860034025 | 131.1048265636827 | 131.31655509549262 | -0.0016123521642488 | 131.30442951836795 | 131.1048265636827 | 0.004419993322352 | True | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0127632078052116 | 0.0144238569392236 | 1.442385693922362e-05 | 0.012748599853589 | 131.30442951836795 | 131.1048265636827 | -0.0016123521642488 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0127632078052116 | 0.0144238569392236 | 1.442385693922362e-05 | 0.012748599853589 | 131.30442951836795 | 131.1048265636827 | -0.0016123521642488 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0127632078052116 | 0.0144238569392236 | 1.442385693922362e-05 | 0.012748599853589 | 131.30442951836795 | 131.1048265636827 | -0.0016123521642488 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0127632078052116 | 0.0144238569392236 | 1.442385693922363e-05 | 0.012748599853589 | 131.30442951836795 | 131.1048265636827 | 0.0 | 0.0 | 0.0 |
| 2021-10-31 | -0.075166179819214 | 0.0586865393572433 | 0.0157807499580302 | 0.0425908947995574 | 0.0500915586571215 | 0.0276881654786864 | -0.0309457916948697 | -0.0509245312050475 | -0.0394431330500597 | -0.0646319971186365 | -0.0535980300335366 | -0.0890269138874849 | EXPANSAO_INFLACIONARIA | 2 | ESTAGFLACAO | 3 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0062638483182678 | 0.0048905449464369 | 0.0013150624965025 | 0.0035492412332964 | 0.0041742965547601 | 0.0023073471232238 | -0.0025788159745724 | -0.0042437109337539 | -0.0032869277541716 | -0.0053859997598863 | -0.0044665025027947 | -0.0074189094906237 | -0.0174082223798508 | -0.0174082223798508 | 129.01865280985277 | 129.01865280985274 | 0.2901865280985274 | 0.2901865280985274 | -0.0189293589578428 | -0.0189293589578428 | 0.0 | -0.0174082223798508 | 129.01865280985274 | -0.0174082223798508 | 129.01865280985274 | -0.0189293589578428 | -0.0189293589578428 | 0.9999999999999994 | 0.0318665443010912 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0318665443010913 | 3.186654430109128e-05 | 3.186654430109131e-05 | -0.0174395341842622 | -0.0174395341842622 | 131.5080152360902 | 128.8184194591036 | 131.31655509549262 | -0.0190237676778254 | 129.01865280985277 | 131.5080152360902 | -0.0189293589578428 | 128.8184194591036 | 131.31655509549262 | -0.0190237676778254 | 129.01865280985277 | 128.8184194591036 | 0.0048599610251687 | True | ESTAGFLACAO | ESTAGFLACAO | ESTAGFLACAO | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0174082223798508 | 0.0318665443010913 | 3.18665443010913e-05 | -0.0174395341842622 | 129.01865280985277 | 128.81841945910358 | -0.0190237676778256 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0174082223798508 | 0.0318665443010913 | 3.18665443010913e-05 | -0.0174395341842622 | 129.01865280985277 | 128.81841945910358 | -0.0190237676778256 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0174082223798508 | 0.0318665443010913 | 3.18665443010913e-05 | -0.0174395341842622 | 129.01865280985277 | 128.81841945910358 | -0.0190237676778256 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0174082223798508 | 0.0318665443010913 | 3.186654430109131e-05 | -0.0174395341842622 | 129.01865280985277 | 128.81841945910358 | 0.0 | 0.0 | 0.0 |
| 2021-11-30 | -0.1583118664342765 | -0.0021997360316761 | -0.0052720271531471 | -0.0078300669197282 | -0.0410586956677391 | -0.0097587327581931 | 0.0267833389592666 | 0.0522729268259603 | 0.0423803308382841 | -0.0144913104708247 | -0.0289460113308702 | 0.0361742400570248 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0131926555361897 | -0.000183311335973 | -0.0004393355960955 | -0.000652505576644 | -0.0034215579723115 | -0.0008132277298494 | 0.0022319449132722 | 0.0043560772354966 | 0.0035316942365236 | -0.001207609205902 | -0.0024121676109058 | 0.003014520004752 | -0.0091881341738266 | -0.0091881341738266 | 127.83321211690948 | 127.83321211690944 | 0.2783321211690945 | 0.2783321211690945 | -0.0279435676417403 | -0.0279435676417403 | 0.0 | -0.0091881341738266 | 127.83321211690944 | -0.0091881341738266 | 127.83321211690944 | -0.0279435676417403 | -0.0279435676417403 | 0.9999999999999994 | 0.0239060807151442 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0239060807151443 | 2.3906080715144293e-05 | 2.3906080715144324e-05 | -0.0092118206022645 | -0.0092118206022645 | 131.5080152360902 | 127.63176728877907 | 131.31655509549262 | -0.0280603447450626 | 127.83321211690948 | 131.5080152360902 | -0.0279435676417403 | 127.63176728877907 | 131.31655509549262 | -0.0280603447450626 | 127.83321211690948 | 127.63176728877907 | 0.0058674909390046 | True | EXPANSAO_INFLACIONARIA | ESTAGFLACAO | ESTAGFLACAO | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0091881341738265 | 0.0239060807151443 | 2.3906080715144344e-05 | -0.0092118206022645 | 127.83321211690948 | 127.63176728877906 | -0.0280603447450628 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0091881341738265 | 0.0239060807151443 | 2.3906080715144344e-05 | -0.0092118206022645 | 127.83321211690948 | 127.63176728877906 | -0.0280603447450628 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0091881341738265 | 0.0239060807151443 | 2.3906080715144344e-05 | -0.0092118206022645 | 127.83321211690948 | 127.63176728877906 | -0.0280603447450628 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0091881341738266 | 0.0239060807151443 | 2.3906080715144344e-05 | -0.0092118206022645 | 127.83321211690948 | 127.63176728877906 | 0.0 | 0.0 | 0.0 |
| 2021-12-31 | -0.2202758534858027 | 0.0511463844797175 | 0.0220455435972921 | 0.0182120517620383 | 0.0240735528279136 | 0.0079651599757581 | -0.0117882472685491 | -0.0036421792219248 | -0.0414999193183911 | 0.0259031645678715 | -0.0382329995263654 | 0.1146042873823256 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | -0.0183563211238168 | 0.0042621987066431 | 0.0018371286331076 | 0.0015176709801698 | 0.0020061294023261 | 0.0006637633313131 | -0.0009823539390457 | -0.0003035149351604 | -0.0034583266098659 | 0.0021585970473226 | -0.0031860832938637 | 0.0095503572818604 | -0.0042907545190096 | -0.0042907545190096 | 127.28471118433932 | 127.2847111843393 | 0.272847111843393 | 0.272847111843393 | -0.0321144231716139 | -0.0321144231716139 | 0.0 | -0.0042907545190096 | 127.2847111843393 | -0.0042907545190096 | 127.2847111843393 | -0.0321144231716139 | -0.0321144231716139 | 0.9999999999999994 | 0.0173785048503699 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0173785048503699 | 1.7378504850369936e-05 | 1.737850485036993e-05 | -0.0043080584569618 | -0.0043080584569618 | 131.5080152360902 | 127.08192217433368 | 131.31655509549262 | -0.0322475175965403 | 127.28471118433932 | 131.5080152360902 | -0.0321144231716139 | 127.08192217433368 | 131.31655509549262 | -0.0322475175965403 | 127.28471118433932 | 127.08192217433368 | 0.0076908308186334 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | ESTAGFLACAO | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0042907545190097 | 0.0173785048503699 | 1.7378504850369902e-05 | -0.0043080584569619 | 127.28471118433932 | 127.08192217433364 | -0.0322475175965405 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0042907545190097 | 0.0173785048503699 | 1.7378504850369902e-05 | -0.0043080584569619 | 127.28471118433932 | 127.08192217433364 | -0.0322475175965405 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0042907545190097 | 0.0173785048503699 | 1.7378504850369902e-05 | -0.0043080584569619 | 127.28471118433932 | 127.08192217433364 | -0.0322475175965405 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | -0.0042907545190096 | 0.0173785048503699 | 1.737850485036991e-05 | -0.0043080584569619 | 127.28471118433932 | 127.08192217433364 | 0.0 | 0.0 | 0.0 |
| 2022-01-31 | 0.3687166311917782 | 0.0503355704697989 | -0.0097644131122923 | -0.0596384660170639 | -0.0766545998526579 | -0.0615449418816104 | 0.0104060870947642 | -0.016043884821247 | 0.0126373794052629 | 0.071381152172568 | 0.1723750471428888 | 0.0019678408131444 | EXPANSAO_INFLACIONARIA | 2 | EXPANSAO_INFLACIONARIA | 2 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 1.0 | 0.0307263859326481 | 0.0041946308724832 | -0.000813701092691 | -0.0049698721680886 | -0.0063878833210548 | -0.0051287451568008 | 0.0008671739245636 | -0.0013369904017705 | 0.0010531149504385 | 0.005948429347714 | 0.0143645872619074 | 0.0001639867344287 | 0.0386811168837778 | 0.0386811168837778 | 132.20822597517866 | 132.20822597517864 | 0.3220822597517863 | 0.3220822597517863 | 0.0 | 0.0 | 0.0 | 0.0386811168837778 | 132.20822597517864 | 0.0386811168837778 | 132.20822597517864 | 0.0 | 0.0 | 0.9999999999999994 | 0.024658637621061 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.024658637621061 | 2.465863762106105e-05 | 2.465863762106105e-05 | 0.0386555044225127 | 0.0386555044225127 | 132.20822597517866 | 131.99433797896504 | 131.99433797896504 | 0.0 | 132.20822597517866 | 132.20822597517866 | 0.0 | 131.99433797896504 | 131.99433797896504 | 0.0 | 132.20822597517866 | 131.99433797896504 | 0.0073227032460896 | True | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | EXPANSAO_INFLACIONARIA | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0386811168837778 | 0.024658637621061 | 2.4658637621061e-05 | 0.0386555044225127 | 132.20822597517866 | 131.994337978965 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0386811168837778 | 0.024658637621061 | 2.4658637621061e-05 | 0.0386555044225127 | 132.20822597517866 | 131.994337978965 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0386811168837778 | 0.024658637621061 | 2.4658637621061e-05 | 0.0386555044225127 | 132.20822597517866 | 131.994337978965 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0386811168837778 | 0.024658637621061 | 2.465863762106101e-05 | 0.0386555044225127 | 132.20822597517866 | 131.994337978965 | 0.0 | 0.0 | 0.0 |

### 06_04_validacao_treino_teste.csv

Caminho: `outputs/tabelas/06_04_validacao_treino_teste.csv`

| periodo | cenario | rotulo | data_inicial | data_final | quantidade_meses | quantidade_mudancas_regime | retorno_total_liquido | retorno_anualizado_liquido | volatilidade_anualizada_liquida | retorno_volatilidade_liquido | maximo_drawdown_liquido | meses_positivos | melhor_mes | pior_mes | turnover_total | turnover_medio_mensal | custo_acumulado_simples | indice_final_liquido |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TREINO | Original_1m | Regime original | 2020-01-31 | 2023-12-31 | 48 | 8 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060984 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.19693179883929 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 |
| TREINO | Confirmacao_2m | Confirmação de 2 meses | 2020-01-31 | 2023-12-31 | 48 | 8 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060984 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.19693179883929 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 |
| TREINO | Confirmacao_3m | Confirmação de 3 meses | 2020-01-31 | 2023-12-31 | 48 | 8 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060984 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.19693179883929 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 |
| TREINO | Benchmark_Estatico | Benchmark de pesos iguais rebalanceado | 2020-01-31 | 2023-12-31 | 48 | 0 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060983 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.1969317988392905 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 |
| TESTE | Original_1m | Regime original | 2024-01-31 | 2026-05-31 | 29 | 3 | 0.2830515983295578 | 0.1086403246834308 | 0.0814442627155637 | 1.333922379073487 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295578 |
| TESTE | Confirmacao_2m | Confirmação de 2 meses | 2024-01-31 | 2026-05-31 | 29 | 3 | 0.2830515983295578 | 0.1086403246834308 | 0.0814442627155637 | 1.333922379073487 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295578 |
| TESTE | Confirmacao_3m | Confirmação de 3 meses | 2024-01-31 | 2026-05-31 | 29 | 3 | 0.2830515983295578 | 0.1086403246834308 | 0.0814442627155637 | 1.333922379073487 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295578 |
| TESTE | Benchmark_Estatico | Benchmark de pesos iguais rebalanceado | 2024-01-31 | 2026-05-31 | 29 | 0 | 0.2830515983295576 | 0.1086403246834308 | 0.0814442627155637 | 1.3339223790734869 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.5674200230987332 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295575 |

### 06_04_validacao_treino_teste_formatada.csv

Caminho: `outputs/tabelas/06_04_validacao_treino_teste_formatada.csv`

| periodo | cenario | rotulo | data_inicial | data_final | quantidade_meses | quantidade_mudancas_regime | retorno_total_liquido | retorno_anualizado_liquido | volatilidade_anualizada_liquida | retorno_volatilidade_liquido | maximo_drawdown_liquido | meses_positivos | melhor_mes | pior_mes | turnover_total | turnover_medio_mensal | custo_acumulado_simples | indice_final_liquido |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TREINO | Original_1m | Regime original | 31/01/2020 | 31/12/2023 | 48 | 8 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 |
| TREINO | Confirmacao_2m | Confirmação de 2 meses | 31/01/2020 | 31/12/2023 | 48 | 8 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 |
| TREINO | Confirmacao_3m | Confirmação de 3 meses | 31/01/2020 | 31/12/2023 | 48 | 8 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 |
| TREINO | Benchmark_Estatico | Benchmark de pesos iguais rebalanceado | 31/01/2020 | 31/12/2023 | 48 | 0 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 |
| TESTE | Original_1m | Regime original | 31/01/2024 | 31/05/2026 | 29 | 3 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 |
| TESTE | Confirmacao_2m | Confirmação de 2 meses | 31/01/2024 | 31/05/2026 | 29 | 3 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 |
| TESTE | Confirmacao_3m | Confirmação de 3 meses | 31/01/2024 | 31/05/2026 | 29 | 3 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 |
| TESTE | Benchmark_Estatico | Benchmark de pesos iguais rebalanceado | 31/01/2024 | 31/05/2026 | 29 | 0 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 |

### 06_05_grade_otimizacao_pesos.csv

Caminho: `outputs/tabelas/06_05_grade_otimizacao_pesos.csv`

| periodo | quantidade_meses | retorno_total_liquido | retorno_anualizado_liquido | volatilidade_anualizada_liquida | retorno_volatilidade_liquido | maximo_drawdown_liquido | meses_positivos | melhor_mes | pior_mes | turnover_total | turnover_medio_mensal | custo_acumulado_simples | indice_final_liquido | tipo | candidato | confirmacao | rotulo_confirmacao | meses_confirmacao | alpha_encolhimento |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060984 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.19693179883929 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_1m_alpha_00 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 0.0 |
| TESTE | 29 | 0.2830515983295578 | 0.1086403246834308 | 0.0814442627155637 | 1.333922379073487 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295578 | ESTRATEGIA | confirmacao_1m_alpha_00 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 0.0 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060984 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.19693179883929 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_1m_alpha_25 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 0.25 |
| TESTE | 29 | 0.2830515983295578 | 0.1086403246834308 | 0.0814442627155637 | 1.333922379073487 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295578 | ESTRATEGIA | confirmacao_1m_alpha_25 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 0.25 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060983 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.1969317988392905 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_1m_alpha_50 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 0.5 |
| TESTE | 29 | 0.2830515983295576 | 0.1086403246834308 | 0.0814442627155637 | 1.3339223790734869 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295575 | ESTRATEGIA | confirmacao_1m_alpha_50 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 0.5 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060983 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.1969317988392905 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_1m_alpha_75 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 0.75 |
| TESTE | 29 | 0.2830515983295576 | 0.1086403246834308 | 0.0814442627155637 | 1.3339223790734869 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.5674200230987332 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295575 | ESTRATEGIA | confirmacao_1m_alpha_75 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 0.75 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060983 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.1969317988392905 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_1m_alpha_100 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 1.0 |
| TESTE | 29 | 0.2830515983295576 | 0.1086403246834308 | 0.0814442627155637 | 1.3339223790734869 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.5674200230987332 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295575 | ESTRATEGIA | confirmacao_1m_alpha_100 | Original_1m | Confirmação de 1 mês(es) | 1.0 | 1.0 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060984 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.19693179883929 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_2m_alpha_00 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 0.0 |
| TESTE | 29 | 0.2830515983295578 | 0.1086403246834308 | 0.0814442627155637 | 1.333922379073487 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295578 | ESTRATEGIA | confirmacao_2m_alpha_00 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 0.0 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060984 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.19693179883929 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_2m_alpha_25 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 0.25 |
| TESTE | 29 | 0.2830515983295578 | 0.1086403246834308 | 0.0814442627155637 | 1.333922379073487 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295578 | ESTRATEGIA | confirmacao_2m_alpha_25 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 0.25 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060983 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.1969317988392905 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_2m_alpha_50 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 0.5 |
| TESTE | 29 | 0.2830515983295576 | 0.1086403246834308 | 0.0814442627155637 | 1.3339223790734869 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295575 | ESTRATEGIA | confirmacao_2m_alpha_50 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 0.5 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060983 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.1969317988392905 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_2m_alpha_75 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 0.75 |
| TESTE | 29 | 0.2830515983295576 | 0.1086403246834308 | 0.0814442627155637 | 1.3339223790734869 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.5674200230987332 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295575 | ESTRATEGIA | confirmacao_2m_alpha_75 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 0.75 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060983 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.1969317988392905 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_2m_alpha_100 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 1.0 |
| TESTE | 29 | 0.2830515983295576 | 0.1086403246834308 | 0.0814442627155637 | 1.3339223790734869 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.5674200230987332 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295575 | ESTRATEGIA | confirmacao_2m_alpha_100 | Confirmacao_2m | Confirmação de 2 mês(es) | 2.0 | 1.0 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060984 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.19693179883929 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_3m_alpha_00 | Confirmacao_3m | Confirmação de 3 mês(es) | 3.0 | 0.0 |
| TESTE | 29 | 0.2830515983295578 | 0.1086403246834308 | 0.0814442627155637 | 1.333922379073487 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295578 | ESTRATEGIA | confirmacao_3m_alpha_00 | Confirmacao_3m | Confirmação de 3 mês(es) | 3.0 | 0.0 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060984 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.19693179883929 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_3m_alpha_25 | Confirmacao_3m | Confirmação de 3 mês(es) | 3.0 | 0.25 |
| TESTE | 29 | 0.2830515983295578 | 0.1086403246834308 | 0.0814442627155637 | 1.333922379073487 | -0.0492658973681908 | 0.6551724137931034 | 0.0868246670042187 | -0.0363619028298027 | 0.567420023098733 | 0.0195662076930597 | 0.0005674200230987 | 128.30515983295578 | ESTRATEGIA | confirmacao_3m_alpha_25 | Confirmacao_3m | Confirmação de 3 mês(es) | 3.0 | 0.25 |
| TREINO | 48 | 0.3422420049176287 | 0.0763603876864695 | 0.0851098743421385 | 0.8971977491060983 | -0.0893304663312883 | 0.5833333333333334 | 0.0515055517844937 | -0.0636215268498781 | 2.1969317988392905 | 0.0457694124758185 | 0.0021969317988392 | 134.22420049176287 | ESTRATEGIA | confirmacao_3m_alpha_50 | Confirmacao_3m | Confirmação de 3 mês(es) | 3.0 | 0.5 |

### 06_05_grade_otimizacao_pesos_formatada.csv

Caminho: `outputs/tabelas/06_05_grade_otimizacao_pesos_formatada.csv`

| periodo | quantidade_meses | retorno_total_liquido | retorno_anualizado_liquido | volatilidade_anualizada_liquida | retorno_volatilidade_liquido | maximo_drawdown_liquido | meses_positivos | melhor_mes | pior_mes | turnover_total | turnover_medio_mensal | custo_acumulado_simples | indice_final_liquido | tipo | candidato | confirmacao | rotulo_confirmacao | meses_confirmacao | alpha_encolhimento |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_1m_alpha_00 | Original_1m | Confirmação de 1 mês(es) | 1 | 0% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_1m_alpha_00 | Original_1m | Confirmação de 1 mês(es) | 1 | 0% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_1m_alpha_25 | Original_1m | Confirmação de 1 mês(es) | 1 | 25% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_1m_alpha_25 | Original_1m | Confirmação de 1 mês(es) | 1 | 25% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_1m_alpha_50 | Original_1m | Confirmação de 1 mês(es) | 1 | 50% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_1m_alpha_50 | Original_1m | Confirmação de 1 mês(es) | 1 | 50% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_1m_alpha_75 | Original_1m | Confirmação de 1 mês(es) | 1 | 75% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_1m_alpha_75 | Original_1m | Confirmação de 1 mês(es) | 1 | 75% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_1m_alpha_100 | Original_1m | Confirmação de 1 mês(es) | 1 | 100% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_1m_alpha_100 | Original_1m | Confirmação de 1 mês(es) | 1 | 100% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_2m_alpha_00 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 0% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_2m_alpha_00 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 0% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_2m_alpha_25 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 25% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_2m_alpha_25 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 25% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_2m_alpha_50 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 50% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_2m_alpha_50 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 50% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_2m_alpha_75 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 75% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_2m_alpha_75 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 75% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_2m_alpha_100 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 100% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_2m_alpha_100 | Confirmacao_2m | Confirmação de 2 mês(es) | 2 | 100% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_3m_alpha_00 | Confirmacao_3m | Confirmação de 3 mês(es) | 3 | 0% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_3m_alpha_00 | Confirmacao_3m | Confirmação de 3 mês(es) | 3 | 0% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_3m_alpha_25 | Confirmacao_3m | Confirmação de 3 mês(es) | 3 | 25% |
| TESTE | 29 | 28.31% | 10.86% | 8.14% | 1.33 | -4.93% | 65.52% | 8.68% | -3.64% | 0.57 | 1.96% | 0.06% | 128.31 | ESTRATEGIA | confirmacao_3m_alpha_25 | Confirmacao_3m | Confirmação de 3 mês(es) | 3 | 25% |
| TREINO | 48 | 34.22% | 7.64% | 8.51% | 0.9 | -8.93% | 58.33% | 5.15% | -6.36% | 2.2 | 4.58% | 0.22% | 134.22 | ESTRATEGIA | confirmacao_3m_alpha_50 | Confirmacao_3m | Confirmação de 3 mês(es) | 3 | 50% |

### 06_05_pesos_selecionados_por_regime.csv

Caminho: `outputs/tabelas/06_05_pesos_selecionados_por_regime.csv`

| regime | meses_confirmacao | alpha_encolhimento | peso_NG=F | peso_ZC=F | peso_GC=F | peso_USDBRL=X | peso_EURBRL=X | peso_JPYBRL=X | peso_IMAB11.SA | peso_B5MB11.SA | peso_IB5M11.SA | peso_BOVV11.SA | peso_FIND11.SA | peso_MATB11.SA | soma_pesos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPANSAO_DESINFLACIONARIA | 1 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.9999999999999996 |
| EXPANSAO_INFLACIONARIA | 1 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.9999999999999996 |
| ESTAGFLACAO | 1 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.9999999999999996 |
| RECESSAO_DESINFLACIONARIA | 1 | 0.0 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.0833333333333333 | 0.9999999999999996 |

### 06_06_contribuicao_ativos_por_regime.csv

Caminho: `outputs/tabelas/06_06_contribuicao_ativos_por_regime.csv`

| periodo | regime | nome_regime | ativo | quantidade_meses | peso_medio_estrategia | peso_benchmark | retorno_medio_ativo | contribuicao_estrategia_acumulada_simples | contribuicao_benchmark_acumulada_simples | diferenca_contribuicao_acumulada | contribuicao_media_mensal_estrategia | contribuicao_media_mensal_benchmark | diferenca_contribuicao_media_mensal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | NG=F | 21 | 0.0833333333333332 | 0.0833333333333333 | -0.025946560508559 | -0.0454064808899782 | -0.0454064808899782 | 9.107298248878237e-18 | -0.0021622133757132 | -0.0021622133757132 | 4.336808689942019e-19 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | ZC=F | 21 | 0.0833333333333332 | 0.0833333333333333 | -0.0126076707529935 | -0.0220634238177386 | -0.0220634238177386 | 8.063753657860939e-18 | -0.0010506392294161 | -0.0010506392294161 | 3.839882694219495e-19 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | GC=F | 21 | 0.0833333333333332 | 0.0833333333333333 | 0.0104160767149708 | 0.0182281342511989 | 0.0182281342511989 | -7.047314121155779e-18 | 0.0008680063929142 | 0.0008680063929142 | -3.3558638672170376e-19 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | USDBRL=X | 21 | 0.0833333333333332 | 0.0833333333333333 | 0.0011773787619185 | 0.0020604128333574 | 0.0020604128333574 | 4.675621868843738e-19 | 9.811489682654326e-05 | 9.811489682654332e-05 | 2.226486604211304e-20 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | EURBRL=X | 21 | 0.0833333333333332 | 0.0833333333333333 | 0.0026446797410708 | 0.004628189546874 | 0.004628189546874 | -2.371692252312041e-18 | 0.0002203899784225 | 0.0002203899784225 | -1.129377263005734e-19 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | JPYBRL=X | 21 | 0.0833333333333332 | 0.0833333333333333 | -0.0060018368335451 | -0.0105032144587039 | -0.0105032144587039 | 1.6779722685107692e-18 | -0.000500153069462 | -0.000500153069462 | 7.990344135765566e-20 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | IMAB11.SA | 21 | 0.0833333333333332 | 0.0833333333333333 | -3.659334273236457e-05 | -6.403834978163799e-05 | -6.403834978163802e-05 | 2.7105054312125282e-20 | -3.049445227697048e-06 | -3.0494452276970486e-06 | 1.290716872005966e-21 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | B5MB11.SA | 21 | 0.0833333333333332 | 0.0833333333333333 | -0.0002785236064127 | -0.0004874163112222 | -0.0004874163112222 | 2.710505431213761e-20 | -2.3210300534392057e-05 | -2.3210300534392057e-05 | 1.2907168720065528e-21 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | IB5M11.SA | 21 | 0.0833333333333332 | 0.0833333333333333 | 0.0112721815653087 | 0.0197263177392903 | 0.0197263177392903 | -6.42389787197662e-18 | 0.0009393484637757 | 0.0009393484637757 | -3.0589989866555335e-19 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | BOVV11.SA | 21 | 0.0833333333333332 | 0.0833333333333333 | -0.0010807419792419 | -0.0018912984636733 | -0.0018912984636733 | 1.734723475976807e-18 | -9.006183160349465e-05 | -9.006183160349473e-05 | 8.260587980841938e-20 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | FIND11.SA | 21 | 0.0833333333333332 | 0.0833333333333333 | 0.0025236426619449 | 0.0044163746584036 | 0.0044163746584036 | -2.737610485525899e-18 | 0.000210303555162 | 0.000210303555162 | -1.3036240407266184e-19 |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | MATB11.SA | 21 | 0.0833333333333332 | 0.0833333333333333 | -0.0009371072839145 | -0.0016399377468504 | -0.0016399377468504 | 3.686287386450715e-18 | -7.809227365954287e-05 | -7.809227365954304e-05 | 1.7553749459289122e-19 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | NG=F | 17 | 0.0833333333333333 | 0.0833333333333333 | 0.018154235712918 | 0.0257185005933005 | 0.0257185005933005 | -1.1275702593849246e-17 | 0.0015128529760765 | 0.0015128529760765 | -6.632766231676028e-19 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | ZC=F | 17 | 0.0833333333333333 | 0.0833333333333333 | 0.0315709265204502 | 0.0447254792373045 | 0.0447254792373045 | -1.5260145577733478e-17 | 0.0026309105433708 | 0.0026309105433708 | -8.976556222196162e-19 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | GC=F | 17 | 0.0833333333333333 | 0.0833333333333333 | 0.006303633160738 | 0.0089301469777122 | 0.0089301469777122 | -2.5478751053409358e-18 | 0.0005253027633948 | 0.0005253027633948 | -1.498750061965256e-19 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | USDBRL=X | 17 | 0.0833333333333333 | 0.0833333333333333 | 0.0033318474220407 | 0.0047201171812243 | 0.0047201171812243 | 4.2351647362715017e-19 | 0.0002776539518367 | 0.0002776539518367 | 2.4912733742773535e-20 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | EURBRL=X | 17 | 0.0833333333333333 | 0.0833333333333333 | 1.959111294462809e-05 | 2.7754076671558485e-05 | 2.7754076671557618e-05 | 1.4501204056993624e-18 | 1.6325927453857931e-06 | 1.6325927453857425e-06 | 8.530120033525661e-20 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | JPYBRL=X | 17 | 0.0833333333333333 | 0.0833333333333333 | -0.0027873881336185 | -0.0039487998559596 | -0.0039487998559596 | -1.626303258728257e-19 | -0.0002322823444682 | -0.0002322823444682 | -9.56648975722504e-21 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | IMAB11.SA | 17 | 0.0833333333333333 | 0.0833333333333333 | 0.0018791896864996 | 0.0026621853892078 | 0.0026621853892078 | -1.2468324983583365e-18 | 0.0001565991405416 | 0.0001565991405416 | -7.334308813872568e-20 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | B5MB11.SA | 17 | 0.0833333333333333 | 0.0833333333333333 | 0.0019982568848244 | 0.0028308639201679 | 0.0028308639201679 | -1.7889335846010823e-18 | 0.0001665214070687 | 0.0001665214070687 | -1.0523138732947544e-19 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | IB5M11.SA | 17 | 0.0833333333333333 | 0.0833333333333333 | -0.0014081880615568 | -0.0019949330872055 | -0.0019949330872055 | 1.0028870095490916e-18 | -0.0001173490051297 | -0.0001173490051297 | 5.899335350288774e-20 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | BOVV11.SA | 17 | 0.0833333333333333 | 0.0833333333333333 | 0.0242255888215835 | 0.0343195841639099 | 0.03431958416391 | -1.0245710529988017e-17 | 0.0020187990684652 | 0.0020187990684652 | -6.026888547051774e-19 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | FIND11.SA | 17 | 0.0833333333333333 | 0.0833333333333333 | 0.0186369229570574 | 0.026402307522498 | 0.026402307522498 | -8.565197162635485e-18 | 0.0015530769130881 | 0.0015530769130881 | -5.038351272138521e-19 |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | MATB11.SA | 17 | 0.0833333333333333 | 0.0833333333333333 | 0.0367034329857 | 0.0519965300630751 | 0.0519965300630751 | -1.691355389077387e-17 | 0.003058619415475 | 0.003058619415475 | -9.94914934751404e-19 |
| TREINO | ESTAGFLACAO | Estagflação | NG=F | 5 | 0.0833333333333333 | 0.0833333333333333 | 0.135648555537829 | 0.0565202314740953 | 0.0565202314740954 | -1.7347234759768068e-17 | 0.011304046294819 | 0.011304046294819 | -3.469446951953614e-18 |

### 06_06_contribuicao_ativos_por_regime_formatado.csv

Caminho: `outputs/tabelas/06_06_contribuicao_ativos_por_regime_formatado.csv`

| periodo | regime | nome_regime | ativo | quantidade_meses | peso_medio_estrategia | peso_benchmark | retorno_medio_ativo | contribuicao_estrategia_acumulada_simples | contribuicao_benchmark_acumulada_simples | diferenca_contribuicao_acumulada | contribuicao_media_mensal_estrategia | contribuicao_media_mensal_benchmark | diferenca_contribuicao_media_mensal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | NG=F | 21 | 8.33% | 8.33% | -2.59% | -4.54% | -4.54% | 0.00% | -0.22% | -0.22% | 0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | ZC=F | 21 | 8.33% | 8.33% | -1.26% | -2.21% | -2.21% | 0.00% | -0.11% | -0.11% | 0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | GC=F | 21 | 8.33% | 8.33% | 1.04% | 1.82% | 1.82% | -0.00% | 0.09% | 0.09% | -0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | USDBRL=X | 21 | 8.33% | 8.33% | 0.12% | 0.21% | 0.21% | 0.00% | 0.01% | 0.01% | 0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | EURBRL=X | 21 | 8.33% | 8.33% | 0.26% | 0.46% | 0.46% | -0.00% | 0.02% | 0.02% | -0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | JPYBRL=X | 21 | 8.33% | 8.33% | -0.60% | -1.05% | -1.05% | 0.00% | -0.05% | -0.05% | 0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | IMAB11.SA | 21 | 8.33% | 8.33% | -0.00% | -0.01% | -0.01% | 0.00% | -0.00% | -0.00% | 0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | B5MB11.SA | 21 | 8.33% | 8.33% | -0.03% | -0.05% | -0.05% | 0.00% | -0.00% | -0.00% | 0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | IB5M11.SA | 21 | 8.33% | 8.33% | 1.13% | 1.97% | 1.97% | -0.00% | 0.09% | 0.09% | -0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | BOVV11.SA | 21 | 8.33% | 8.33% | -0.11% | -0.19% | -0.19% | 0.00% | -0.01% | -0.01% | 0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | FIND11.SA | 21 | 8.33% | 8.33% | 0.25% | 0.44% | 0.44% | -0.00% | 0.02% | 0.02% | -0.00% |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | MATB11.SA | 21 | 8.33% | 8.33% | -0.09% | -0.16% | -0.16% | 0.00% | -0.01% | -0.01% | 0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | NG=F | 17 | 8.33% | 8.33% | 1.82% | 2.57% | 2.57% | -0.00% | 0.15% | 0.15% | -0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | ZC=F | 17 | 8.33% | 8.33% | 3.16% | 4.47% | 4.47% | -0.00% | 0.26% | 0.26% | -0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | GC=F | 17 | 8.33% | 8.33% | 0.63% | 0.89% | 0.89% | -0.00% | 0.05% | 0.05% | -0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | USDBRL=X | 17 | 8.33% | 8.33% | 0.33% | 0.47% | 0.47% | 0.00% | 0.03% | 0.03% | 0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | EURBRL=X | 17 | 8.33% | 8.33% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | JPYBRL=X | 17 | 8.33% | 8.33% | -0.28% | -0.39% | -0.39% | -0.00% | -0.02% | -0.02% | -0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | IMAB11.SA | 17 | 8.33% | 8.33% | 0.19% | 0.27% | 0.27% | -0.00% | 0.02% | 0.02% | -0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | B5MB11.SA | 17 | 8.33% | 8.33% | 0.20% | 0.28% | 0.28% | -0.00% | 0.02% | 0.02% | -0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | IB5M11.SA | 17 | 8.33% | 8.33% | -0.14% | -0.20% | -0.20% | 0.00% | -0.01% | -0.01% | 0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | BOVV11.SA | 17 | 8.33% | 8.33% | 2.42% | 3.43% | 3.43% | -0.00% | 0.20% | 0.20% | -0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | FIND11.SA | 17 | 8.33% | 8.33% | 1.86% | 2.64% | 2.64% | -0.00% | 0.16% | 0.16% | -0.00% |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | MATB11.SA | 17 | 8.33% | 8.33% | 3.67% | 5.20% | 5.20% | -0.00% | 0.31% | 0.31% | -0.00% |
| TREINO | ESTAGFLACAO | Estagflação | NG=F | 5 | 8.33% | 8.33% | 13.56% | 5.65% | 5.65% | -0.00% | 1.13% | 1.13% | -0.00% |

### 06_06_diagnostico_por_regime.csv

Caminho: `outputs/tabelas/06_06_diagnostico_por_regime.csv`

| periodo | regime | nome_regime | quantidade_meses | proporcao_periodo | retorno_total_estrategia | retorno_total_benchmark | diferenca_retorno_composto | excesso_acumulado_simples | retorno_medio_mensal_estrategia | retorno_medio_mensal_benchmark | excesso_medio_mensal | volatilidade_mensal_estrategia | volatilidade_mensal_benchmark | maximo_drawdown_estrategia | maximo_drawdown_benchmark | taxa_vitoria_mensal | turnover_total_estrategia | turnover_total_benchmark | diferenca_turnover | custo_total_estrategia | custo_total_benchmark | diferenca_custo | classificacao |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 21 | 0.4375 | -0.0377049927580971 | -0.0377049927580972 | 1.1102230246251563e-16 | 1.1102230246251563e-16 | -0.0016398920747973 | -0.0016398920747973 | 5.2867763077388396e-18 | 0.019821069215824 | 0.019821069215824 | -0.112163224842779 | -0.1121632248427793 | 0.0476190476190476 | 1.4483416067966777 | 1.4483416067966777 | -2.0469737016526324e-16 | 0.0014483416067966 | 0.0014483416067966 | -2.1345230270808369e-19 | - |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | 17 | 0.3541666666666667 | 0.207579851529948 | 0.207579851529948 | 0.0 | 0.0 | 0.0115213426548531 | 0.0115213426548531 | 0.0 | 0.0277260886290393 | 0.0277260886290393 | -0.0636215268498781 | -0.0636215268498781 | 0.0 | 0.5187057429790911 | 0.5187057429790912 | -1.9428902930940242e-16 | 0.000518705742979 | 0.000518705742979 | -1.9651164376299768e-19 | - |
| TREINO | ESTAGFLACAO | Estagflação | 5 | 0.1041666666666666 | -0.0139582134821899 | -0.0139582134821899 | 0.0 | 0.0 | -0.0027445686467171 | -0.0027445686467171 | 0.0 | 0.0125113655375271 | 0.0125113655375271 | -0.0190237676778256 | -0.0190237676778256 | 0.0 | 0.1156366479391828 | 0.1156366479391828 | -3.4694469519536136e-17 | 0.0001156366479391 | 0.0001156366479391 | -3.557538378468061e-20 | - |
| TREINO | RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | 5 | 0.1041666666666666 | 0.1714167108387583 | 0.1714167108387583 | 0.0 | 0.0 | 0.0323454095272938 | 0.0323454095272938 | 0.0 | 0.0223638329427688 | 0.0223638329427688 | -0.005470982310879 | -0.005470982310879 | 0.0 | 0.1142478011243387 | 0.1142478011243388 | -6.938893903907227e-17 | 0.0001142478011243 | 0.0001142478011243 | -7.115076756936123e-20 | - |
| TESTE | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 13 | 0.4482758620689655 | 0.072244685003362 | 0.072244685003362 | 0.0 | 1.1102230246251563e-16 | 0.0057801104969796 | 0.0057801104969796 | 8.540177112501206e-18 | 0.02991521097291 | 0.02991521097291 | -0.0492658973681908 | -0.0492658973681908 | 0.0769230769230769 | 0.2636653465279716 | 0.2636653465279717 | -1.1449174941446927e-16 | 0.0002636653465279 | 0.0002636653465279 | -1.0842021724855044e-19 | POSITIVO |
| TESTE | EXPANSAO_INFLACIONARIA | Expansão inflacionária | 13 | 0.4482758620689655 | 0.1110506174881664 | 0.1110506174881664 | 0.0 | 0.0 | 0.0082606110908233 | 0.0082606110908233 | 0.0 | 0.0166623737168046 | 0.0166623737168046 | -0.0298389106335186 | -0.0298389106335186 | 0.0 | 0.2442907064602478 | 0.2442907064602479 | -6.938893903907227e-17 | 0.0002442907064602 | 0.0002442907064602 | -6.776263578034403e-20 | POSITIVO |
| TESTE | ESTAGFLACAO | Estagflação | 0 | 0.0 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | AMOSTRA INSUFICIENTE |
| TESTE | RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | 3 | 0.1034482758620689 | 0.0770016651862655 | 0.0770016651862655 | 0.0 | 0.0 | 0.0251147268030518 | 0.0251147268030518 | 0.0 | 0.0155906075740225 | 0.0155906075740225 | 0.0 | 0.0 | 0.0 | 0.0594639701105133 | 0.0594639701105134 | -6.938893903907228e-18 | 5.94639701105134e-05 | 5.94639701105134e-05 | -6.776263578034403e-21 | AMOSTRA INSUFICIENTE |

### 06_06_diagnostico_por_regime_formatado.csv

Caminho: `outputs/tabelas/06_06_diagnostico_por_regime_formatado.csv`

| periodo | regime | nome_regime | quantidade_meses | proporcao_periodo | retorno_total_estrategia | retorno_total_benchmark | diferenca_retorno_composto | excesso_acumulado_simples | retorno_medio_mensal_estrategia | retorno_medio_mensal_benchmark | excesso_medio_mensal | volatilidade_mensal_estrategia | volatilidade_mensal_benchmark | maximo_drawdown_estrategia | maximo_drawdown_benchmark | taxa_vitoria_mensal | turnover_total_estrategia | turnover_total_benchmark | diferenca_turnover | custo_total_estrategia | custo_total_benchmark | diferenca_custo | classificacao |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TREINO | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 21 | 43.75% | -3.77% | -3.77% | 0.00% | 0.00% | -0.16% | -0.16% | 0.00% | 1.98% | 1.98% | -11.22% | -11.22% | 4.76% | 1.4483 | 1.4483 | -0.0000 | 0.14% | 0.14% | -0.00% | - |
| TREINO | EXPANSAO_INFLACIONARIA | Expansão inflacionária | 17 | 35.42% | 20.76% | 20.76% | 0.00% | 0.00% | 1.15% | 1.15% | 0.00% | 2.77% | 2.77% | -6.36% | -6.36% | 0.00% | 0.5187 | 0.5187 | -0.0000 | 0.05% | 0.05% | -0.00% | - |
| TREINO | ESTAGFLACAO | Estagflação | 5 | 10.42% | -1.40% | -1.40% | 0.00% | 0.00% | -0.27% | -0.27% | 0.00% | 1.25% | 1.25% | -1.90% | -1.90% | 0.00% | 0.1156 | 0.1156 | -0.0000 | 0.01% | 0.01% | -0.00% | - |
| TREINO | RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | 5 | 10.42% | 17.14% | 17.14% | 0.00% | 0.00% | 3.23% | 3.23% | 0.00% | 2.24% | 2.24% | -0.55% | -0.55% | 0.00% | 0.1142 | 0.1142 | -0.0000 | 0.01% | 0.01% | -0.00% | - |
| TESTE | EXPANSAO_DESINFLACIONARIA | Expansão desinflacionária | 13 | 44.83% | 7.22% | 7.22% | 0.00% | 0.00% | 0.58% | 0.58% | 0.00% | 2.99% | 2.99% | -4.93% | -4.93% | 7.69% | 0.2637 | 0.2637 | -0.0000 | 0.03% | 0.03% | -0.00% | POSITIVO |
| TESTE | EXPANSAO_INFLACIONARIA | Expansão inflacionária | 13 | 44.83% | 11.11% | 11.11% | 0.00% | 0.00% | 0.83% | 0.83% | 0.00% | 1.67% | 1.67% | -2.98% | -2.98% | 0.00% | 0.2443 | 0.2443 | -0.0000 | 0.02% | 0.02% | -0.00% | POSITIVO |
| TESTE | ESTAGFLACAO | Estagflação | 0 | 0.00% | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | AMOSTRA INSUFICIENTE |
| TESTE | RECESSAO_DESINFLACIONARIA | Recessão desinflacionária | 3 | 10.34% | 7.70% | 7.70% | 0.00% | 0.00% | 2.51% | 2.51% | 0.00% | 1.56% | 1.56% | 0.00% | 0.00% | 0.00% | 0.0595 | 0.0595 | -0.0000 | 0.01% | 0.01% | -0.00% | AMOSTRA INSUFICIENTE |

### 06_06_regimes_problematicos_teste.csv

Caminho: `outputs/tabelas/06_06_regimes_problematicos_teste.csv`

_Nenhum dado disponível._

---

## 22. Conclusão técnica

- A estratégia acumulou **72,22%**, com volatilidade anualizada de **8,33%** e drawdown máximo de **-8,32%**.
- A diferença acumulada contra o benchmark foi de **0,00%**.
- O melhor ativo no período foi **GC=F**, com **171,53%**.
- O pior ativo no período foi **JPYBRL=X**, com **-12,50%**.
- O melhor regime para a estratégia foi **Expansão inflacionária**.
- O pior regime para a estratégia foi **Estagflação**.
- A estratégia superou o benchmark em **0,00%** das janelas móveis de 12 meses.
- O teste final de 2026 está parcialmente coberto pela base mensal disponível; a conclusão final deve ser atualizada quando os meses restantes estiverem disponíveis.
- O período de desenvolvimento não deve ser usado sozinho para defender a robustez da estratégia.
- A evidência principal deve vir da validação de 2024–2025 e do teste final de 2026.
- Resultados históricos não garantem desempenho futuro.
- O relatório não constitui recomendação de investimento.
