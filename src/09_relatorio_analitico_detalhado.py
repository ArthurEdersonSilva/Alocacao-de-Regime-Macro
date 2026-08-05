# VERSAO_V3_PERIODOS_OFICIAIS_E_SAIDAS_PIPELINE
r"""
09 — RELATÓRIO ANALÍTICO DETALHADO

Consolida as análises do projeto em um relatório Markdown, com tabelas CSV
separadas e gráficos PNG.

Principais análises:
- inventário e atualização das bases;
- universo dos ativos selecionados;
- indicadores macroeconômicos;
- episódios consecutivos de regimes;
- ativos no período completo, por ano, semestre e regime;
- carteira, benchmark e CDI;
- melhores e piores meses;
- transições entre regimes;
- janelas móveis de 12 meses;
- contribuições dos ativos quando os pesos mensais existem.

Execução:
    python .\src\09_relatorio_analitico_detalhado.py

Período específico:
    python .\src\09_relatorio_analitico_detalhado.py --inicio 2020-01-01 --fim 2026-05-31
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml


VERSAO = "3.0.0"
VALOR_INICIAL = 100.0
PERIODOS_ANO = 12
JANELA_ROLLING = 12
JANELA_TRANSICAO = 3
QUANTIDADE_EXTREMOS = 5

NOMES_REGIMES = {
    "EXPANSAO_DESINFLACIONARIA": "Expansão desinflacionária",
    "EXPANSAO_INFLACIONARIA": "Expansão inflacionária",
    "ESTAGFLACAO": "Estagflação",
    "RECESSAO_DESINFLACIONARIA": "Recessão desinflacionária",
}

ORDEM_REGIMES = list(NOMES_REGIMES)

ARQUIVOS = {
    "selecao": "data/processed/ativos_selecionados_modelo.csv",
    "retornos": "data/processed/retornos_ativos.csv",
    "macro": "data/processed/dados_macro_mensais.csv",
    "regimes": "data/processed/regimes_macroeconomicos.csv",
    "alocacao": "data/processed/alocacao_portfolio_mensal.csv",
    "backtest": "data/processed/backtest_portfolio_mensal.csv",
    "series_finais": "outputs/tabelas/06_12_series_modelos_finais.csv",
    "metricas_finais": "outputs/tabelas/06_12_metricas_finais_modelos.csv",
    "pesos_oficiais": "outputs/tabelas/06_12_pesos_oficiais_atuais.csv",
    "scorecard": "outputs/tabelas/07_05_scorecard_executivo.csv",
    "auditoria": "outputs/auditoria/08_06_diagnostico_final_corrigido.csv",
}


PERIODOS_OFICIAIS = [
    {
        "codigo": "DESENVOLVIMENTO_CALIBRACAO",
        "nome": "Desenvolvimento e calibração",
        "inicio": pd.Timestamp("2020-01-01"),
        "fim": pd.Timestamp("2023-12-31"),
        "funcao": "Construção, testes e escolha dos parâmetros",
        "ajusta_parametros": "Sim",
        "altera_regras": "Sim",
    },
    {
        "codigo": "VALIDACAO",
        "nome": "Validação",
        "inicio": pd.Timestamp("2024-01-01"),
        "fim": pd.Timestamp("2025-12-31"),
        "funcao": "Avaliação das regras e parâmetros congelados",
        "ajusta_parametros": "Não",
        "altera_regras": "Não",
    },
    {
        "codigo": "TESTE_FINAL_FORA_AMOSTRA",
        "nome": "Teste final fora da amostra",
        "inicio": pd.Timestamp("2026-01-01"),
        "fim": pd.Timestamp("2026-08-02"),
        "funcao": "Teste final de generalização sem novos ajustes",
        "ajusta_parametros": "Não",
        "altera_regras": "Não",
    },
]

PASTAS_PIPELINE = {
    "graficos": "outputs/graficos",
    "modelo_final": "outputs/modelo_final",
    "tabelas": "outputs/tabelas",
    "auditoria": "outputs/auditoria",
}

PALAVRAS_TABELAS_RELEVANTES = (
    "metrica",
    "scorecard",
    "desempenho",
    "resultado",
    "validacao",
    "peso",
    "turnover",
    "custo",
    "walk",
    "modelo",
    "regime",
    "auditoria",
    "sensibilidade",
    "manifesto",
)


# ============================================================
# CAMINHOS E LEITURA
# ============================================================


def raiz_projeto() -> Path:
    valor = os.getenv("PROJECT_ROOT", "").strip()
    if valor:
        raiz = Path(valor).expanduser().resolve()
    else:
        raiz = Path(__file__).resolve().parent.parent
    if not raiz.is_dir():
        raise FileNotFoundError(f"Raiz do projeto não encontrada: {raiz}")
    return raiz


def caminho_config(raiz: Path) -> Path:
    valor = os.getenv("PROJECT_CONFIG", "").strip()
    caminho = Path(valor).expanduser().resolve() if valor else raiz / "config" / "config.yaml"
    if not caminho.is_file():
        raise FileNotFoundError(f"Configuração não encontrada: {caminho}")
    return caminho


def resolver(raiz: Path, caminho: str | Path) -> Path:
    objeto = Path(caminho)
    return objeto.resolve() if objeto.is_absolute() else (raiz / objeto).resolve()


def carregar_yaml(caminho: Path) -> dict[str, Any]:
    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = yaml.safe_load(arquivo) or {}
    if not isinstance(dados, dict):
        raise ValueError("config.yaml precisa conter um dicionário YAML.")
    return dados


def ler_csv(
    caminho: Path,
    obrigatorio: bool = False,
) -> pd.DataFrame:
    """
    Lê CSV com detecção automática de separador.

    Aceita vírgula, ponto e vírgula ou tabulação. O parâmetro
    low_memory é utilizado apenas com o engine C, pois não é
    suportado pelo engine Python.
    """

    if not caminho.is_file():
        if obrigatorio:
            raise FileNotFoundError(
                f"Arquivo obrigatório não encontrado: {caminho}"
            )
        return pd.DataFrame()

    erros: list[str] = []

    # Mesma estratégia que funcionou nas etapas 02 e 04.
    for encoding in ("utf-8-sig", "latin1"):
        try:
            dados = pd.read_csv(
                caminho,
                encoding=encoding,
                sep=None,
                engine="python",
            )
            dados.columns = [
                str(coluna).replace("\ufeff", "").strip()
                for coluna in dados.columns
            ]

            if len(dados.columns) > 1 or dados.empty:
                return dados

            erros.append(
                f"{encoding}/automático: apenas uma coluna detectada"
            )
        except Exception as erro:
            erros.append(
                f"{encoding}/automático: {erro}"
            )

    tentativas = [
        ("utf-8-sig", ",", "c"),
        ("utf-8-sig", ";", "python"),
        ("utf-8-sig", "\t", "python"),
        ("latin1", ",", "python"),
        ("latin1", ";", "python"),
        ("latin1", "\t", "python"),
    ]

    for encoding, separador, engine in tentativas:
        try:
            parametros = {
                "filepath_or_buffer": caminho,
                "encoding": encoding,
                "sep": separador,
                "engine": engine,
            }

            if engine == "c":
                parametros["low_memory"] = False

            dados = pd.read_csv(**parametros)
            dados.columns = [
                str(coluna).replace("\ufeff", "").strip()
                for coluna in dados.columns
            ]

            if len(dados.columns) > 1 or dados.empty:
                return dados

            erros.append(
                f"{encoding}/{separador!r}: apenas uma coluna"
            )
        except Exception as erro:
            erros.append(
                f"{encoding}/{separador!r}: {erro}"
            )

    raise ValueError(
        f"Não foi possível interpretar {caminho}\n"
        + "\n".join(erros)
    )


# ============================================================
# UTILITÁRIOS
# ============================================================


def normalizar(valor: Any) -> str:
    texto = unicodedata.normalize("NFKD", str(valor or "").strip())
    texto = "".join(c for c in texto if not unicodedata.combining(c)).upper()
    return re.sub(r"[^A-Z0-9]+", "_", texto).strip("_")


def nome_regime(valor: Any) -> str:
    codigo = normalizar(valor)
    return NOMES_REGIMES.get(codigo, str(valor).replace("_", " ").title() if codigo else "Não informado")


def localizar_coluna(
    dados: pd.DataFrame,
    candidatos: Iterable[str],
    contem: Iterable[str] | None = None,
) -> str | None:
    mapa = {normalizar(coluna): str(coluna) for coluna in dados.columns}
    for candidato in candidatos:
        chave = normalizar(candidato)
        if chave in mapa:
            return mapa[chave]
    if contem:
        termos = [normalizar(termo) for termo in contem]
        for coluna in dados.columns:
            chave = normalizar(coluna)
            if all(termo in chave for termo in termos):
                return str(coluna)
    return None


def preparar_data(dados: pd.DataFrame) -> pd.DataFrame:
    if dados.empty:
        return dados.copy()
    resultado = dados.copy()
    coluna = localizar_coluna(resultado, ["data", "date", "mes", "data_referencia"])
    if coluna is None:
        return resultado
    if coluna != "data":
        resultado = resultado.rename(columns={coluna: "data"})
    resultado["data"] = pd.to_datetime(resultado["data"], errors="coerce")
    return (
        resultado.dropna(subset=["data"])
        .drop_duplicates(subset=["data"], keep="last")
        .sort_values("data")
        .reset_index(drop=True)
    )


def filtrar_periodo(
    dados: pd.DataFrame,
    inicio: pd.Timestamp | None,
    fim: pd.Timestamp | None,
) -> pd.DataFrame:
    if dados.empty or "data" not in dados.columns:
        return dados.copy()
    resultado = dados.copy()
    if inicio is not None:
        resultado = resultado.loc[resultado["data"] >= inicio]
    if fim is not None:
        resultado = resultado.loc[resultado["data"] <= fim]
    return resultado.reset_index(drop=True)


def retorno_composto(serie: pd.Series) -> float:
    valores = pd.to_numeric(serie, errors="coerce").dropna()
    return float((1.0 + valores).prod() - 1.0) if not valores.empty else np.nan


def drawdown(retornos: pd.Series) -> pd.Series:
    serie = pd.to_numeric(retornos, errors="coerce").fillna(0.0)
    indice = (1.0 + serie).cumprod()
    return indice / indice.cummax() - 1.0


def metricas(retornos: pd.Series, cdi: pd.Series | None = None) -> dict[str, float]:
    serie = pd.to_numeric(retornos, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if serie.empty:
        return {chave: np.nan for chave in [
            "meses", "retorno_total", "retorno_anualizado", "volatilidade_anualizada",
            "sharpe", "drawdown_maximo", "meses_positivos", "melhor_mes", "pior_mes",
        ]}

    n = len(serie)
    fator = float((1.0 + serie).prod())
    anualizado = fator ** (PERIODOS_ANO / n) - 1.0 if fator > 0 else np.nan
    volatilidade = float(serie.std(ddof=1) * math.sqrt(PERIODOS_ANO)) if n > 1 else np.nan

    if cdi is not None:
        cdi_alinhado = pd.to_numeric(cdi, errors="coerce").reindex(serie.index)
        excesso = (serie - cdi_alinhado).dropna()
    else:
        excesso = serie

    sharpe = (
        float(excesso.mean() / excesso.std(ddof=1) * math.sqrt(PERIODOS_ANO))
        if len(excesso) > 1 and excesso.std(ddof=1) > 0
        else np.nan
    )

    return {
        "meses": n,
        "retorno_total": fator - 1.0,
        "retorno_anualizado": anualizado,
        "volatilidade_anualizada": volatilidade,
        "sharpe": sharpe,
        "drawdown_maximo": float(drawdown(serie).min()),
        "meses_positivos": float((serie > 0).mean()),
        "melhor_mes": float(serie.max()),
        "pior_mes": float(serie.min()),
    }


def fmt_pct(valor: Any) -> str:
    numero = pd.to_numeric(pd.Series([valor]), errors="coerce").iloc[0]
    return "—" if pd.isna(numero) else f"{numero * 100:.2f}%".replace(".", ",")


def fmt_num(valor: Any, casas: int = 2) -> str:
    numero = pd.to_numeric(pd.Series([valor]), errors="coerce").iloc[0]
    return "—" if pd.isna(numero) else f"{numero:.{casas}f}".replace(".", ",")


def fmt_data(valor: Any) -> str:
    data = pd.to_datetime(valor, errors="coerce")
    return "—" if pd.isna(data) else data.strftime("%d/%m/%Y")


def tabela_md(dados: pd.DataFrame, limite: int | None = None) -> str:
    if dados is None or dados.empty:
        return "_Nenhum dado disponível._"
    tabela = dados.head(limite).copy() if limite else dados.copy()
    colunas = [str(c) for c in tabela.columns]
    linhas = [
        "| " + " | ".join(c.replace("|", "\\|") for c in colunas) + " |",
        "| " + " | ".join("---" for _ in colunas) + " |",
    ]
    for _, linha in tabela.iterrows():
        valores = [str(linha[c]).replace("|", "\\|").replace("\n", "<br>") for c in tabela.columns]
        linhas.append("| " + " | ".join(valores) + " |")
    return "\n".join(linhas)


def salvar_csv(dados: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    dados.to_csv(caminho, index=False, encoding="utf-8-sig")


# ============================================================
# PREPARAÇÃO DAS BASES
# ============================================================


def preparar_universo(selecao: pd.DataFrame) -> pd.DataFrame:
    dados = selecao.copy()
    dados.columns = [str(c).strip().lower() for c in dados.columns]
    ticker = localizar_coluna(dados, ["ticker", "ativo", "codigo"])
    if ticker is None:
        raise ValueError("ativos_selecionados_modelo.csv não possui ticker.")
    if ticker != "ticker":
        dados = dados.rename(columns={ticker: "ticker"})

    classe = localizar_coluna(dados, ["classe", "categoria", "tipo"])
    if classe is None:
        dados["classe"] = ""
    elif classe != "classe":
        dados = dados.rename(columns={classe: "classe"})

    status = localizar_coluna(dados, ["status"])
    if status is None:
        dados["status"] = "SELECIONADO"
    elif status != "status":
        dados = dados.rename(columns={status: "status"})

    dados["ticker"] = dados["ticker"].astype(str).str.strip()
    dados["classe"] = dados["classe"].fillna("").astype(str)

    def segmento(linha: pd.Series) -> str:
        texto = normalizar(f"{linha['ticker']} {linha['classe']}")
        if "COMMODITY" in texto or linha["ticker"] in {"GC=F", "NG=F", "ZC=F"}:
            return "Commodities"
        if "MOEDA" in texto or linha["ticker"].endswith("BRL=X"):
            return "Moedas"
        if "RENDA_FIXA" in texto or "IMAB" in texto or linha["ticker"] in {"B5MB11.SA", "IB5M11.SA"}:
            return "Renda Fixa"
        return "Renda Variável"

    dados["segmento"] = dados.apply(segmento, axis=1)
    return (
        dados[["ticker", "segmento", "classe", "status"]]
        .drop_duplicates(subset=["ticker"])
        .sort_values(["segmento", "ticker"])
        .reset_index(drop=True)
    )


def retornos_mensais(retornos: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    dados = retornos.copy()
    ativos = [ticker for ticker in tickers if ticker in dados.columns]
    if not ativos:
        raise ValueError("Nenhum ativo selecionado existe em retornos_ativos.csv.")
    for ticker in ativos:
        dados[ticker] = pd.to_numeric(dados[ticker], errors="coerce")
    dados["mes"] = dados["data"].dt.to_period("M").dt.to_timestamp("M")
    return (
        dados.groupby("mes", sort=True)[ativos]
        .agg(retorno_composto)
        .reset_index()
        .rename(columns={"mes": "data"})
    )


def preparar_regimes(regimes: pd.DataFrame) -> pd.DataFrame:
    coluna = localizar_coluna(
        regimes,
        ["regime_confirmado", "regime_sinal", "regime_oficial", "regime"],
    )
    if coluna is None:
        raise ValueError("regimes_macroeconomicos.csv não possui coluna de regime.")
    dados = regimes.copy()
    dados["regime"] = dados[coluna].map(normalizar)
    dados["nome_regime"] = dados["regime"].map(nome_regime)
    return dados


def localizar_macro(dados: pd.DataFrame) -> dict[str, str | None]:
    return {
        "ipca": localizar_coluna(dados, ["IPCA_MENSAL_PCT", "IPCA_PCT", "IPCA"]),
        "ipca_12m": localizar_coluna(dados, ["IPCA_12M_PCT", "IPCA_ACUMULADO_12M_PCT"], contem=["IPCA", "12M"]),
        "inflacao": localizar_coluna(dados, ["IPCA_VARIACAO_3M_PP"], contem=["IPCA", "VARIACAO", "3M"]),
        "ibc": localizar_coluna(dados, ["IBC_BR", "IBC_BR_VALOR"]),
        "ibc_dessaz": localizar_coluna(dados, ["IBC_BR_DESSAZONALIZADO"], contem=["IBC", "DESSAZ"]),
        "atividade": localizar_coluna(dados, ["IBC_BR_TENDENCIA_3M_PCT"], contem=["IBC", "TENDENCIA", "3M"]),
        "cdi": localizar_coluna(dados, ["CDI_MENSAL_PCT", "RETORNO_CDI"], contem=["CDI", "MENSAL"]),
    }


def localizar_carteira(dados: pd.DataFrame) -> dict[str, str | None]:
    return {
        "estrategia": localizar_coluna(
            dados,
            ["retorno_portfolio_liquido", "retorno_modelo_oficial", "retorno_walk_forward", "retorno_portfolio"],
        ),
        "benchmark": localizar_coluna(
            dados,
            ["retorno_estatica_liquido", "retorno_carteira_estatica", "retorno_benchmark"],
        ),
        "cdi": localizar_coluna(dados, ["retorno_cdi", "CDI_MENSAL_PCT"], contem=["CDI"]),
        "turnover": localizar_coluna(dados, ["turnover_portfolio"], contem=["TURNOVER", "PORTFOLIO"]),
        "custo": localizar_coluna(dados, ["custo_portfolio"], contem=["CUSTO", "PORTFOLIO"]),
    }


def cdi_decimal(serie: pd.Series, nome: str | None) -> pd.Series:
    valores = pd.to_numeric(serie, errors="coerce")
    if nome and "PCT" in normalizar(nome):
        return valores / 100.0
    if valores.abs().median(skipna=True) > 0.20:
        return valores / 100.0
    return valores


def consolidar_base(
    mensal: pd.DataFrame,
    macro: pd.DataFrame,
    regimes: pd.DataFrame,
    carteira: pd.DataFrame,
) -> pd.DataFrame:
    base = mensal.copy()
    base = pd.merge(base, macro, on="data", how="left", validate="one_to_one")
    base = pd.merge(
        base,
        regimes[["data", "regime", "nome_regime"]],
        on="data",
        how="left",
        validate="one_to_one",
    )
    if not carteira.empty:
        extras = [c for c in carteira.columns if c != "data" and c not in base.columns]
        base = pd.merge(base, carteira[["data", *extras]], on="data", how="left", validate="one_to_one")
    return base.sort_values("data").reset_index(drop=True)


# ============================================================
# ANÁLISES
# ============================================================


def serie_cdi(base: pd.DataFrame) -> pd.Series | None:
    macro = localizar_macro(base)
    coluna = macro["cdi"]
    if coluna and coluna in base.columns:
        return cdi_decimal(base[coluna], coluna)
    carteira = localizar_carteira(base)
    coluna = carteira["cdi"]
    return cdi_decimal(base[coluna], coluna) if coluna and coluna in base.columns else None


def analise_ativos(base: pd.DataFrame, universo: pd.DataFrame) -> pd.DataFrame:
    cdi = serie_cdi(base)
    linhas: list[dict[str, Any]] = []
    for _, ativo in universo.iterrows():
        ticker = ativo["ticker"]
        if ticker not in base.columns:
            continue
        linhas.append({"ticker": ticker, "segmento": ativo["segmento"], **metricas(base[ticker], cdi)})
    return pd.DataFrame(linhas).sort_values("retorno_total", ascending=False).reset_index(drop=True)


def analise_periodica_ativos(
    base: pd.DataFrame,
    universo: pd.DataFrame,
    tipo: str,
) -> pd.DataFrame:
    dados = base.copy()
    if tipo == "ano":
        dados["periodo"] = dados["data"].dt.year.astype(str)
    else:
        dados["periodo"] = dados["data"].dt.year.astype(str) + " — " + np.where(
            dados["data"].dt.month <= 6, "1º semestre", "2º semestre"
        )
    linhas = []
    for periodo, grupo in dados.groupby("periodo", sort=True):
        for _, ativo in universo.iterrows():
            ticker = ativo["ticker"]
            if ticker in grupo.columns:
                linhas.append({
                    "periodo": periodo,
                    "ticker": ticker,
                    "segmento": ativo["segmento"],
                    "retorno": retorno_composto(grupo[ticker]),
                    "meses": int(grupo[ticker].notna().sum()),
                })
    return pd.DataFrame(linhas)


def analise_ativos_regime(base: pd.DataFrame, universo: pd.DataFrame) -> pd.DataFrame:
    if "regime" not in base.columns:
        return pd.DataFrame()
    linhas = []
    for regime, grupo in base.dropna(subset=["regime"]).groupby("regime", sort=False):
        for _, ativo in universo.iterrows():
            ticker = ativo["ticker"]
            if ticker in grupo.columns:
                linhas.append({
                    "regime": regime,
                    "nome_regime": nome_regime(regime),
                    "ticker": ticker,
                    "segmento": ativo["segmento"],
                    **metricas(grupo[ticker], serie_cdi(grupo)),
                })
    return pd.DataFrame(linhas)


def analise_segmentos(base: pd.DataFrame, universo: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    retornos = base[["data"]].copy()
    linhas = []
    cdi = serie_cdi(base)
    for segmento, grupo in universo.groupby("segmento"):
        tickers = [ticker for ticker in grupo["ticker"] if ticker in base.columns]
        if not tickers:
            continue
        retornos[segmento] = base[tickers].apply(pd.to_numeric, errors="coerce").mean(axis=1)
        linhas.append({"segmento": segmento, **metricas(retornos[segmento], cdi)})
    return pd.DataFrame(linhas), retornos


def analise_carteira(base: pd.DataFrame) -> pd.DataFrame:
    colunas = localizar_carteira(base)
    cdi = serie_cdi(base)
    linhas = []
    for nome, chave in [("Estratégia", "estrategia"), ("Benchmark estático", "benchmark"), ("CDI", "cdi")]:
        coluna = colunas[chave]
        if not coluna or coluna not in base.columns:
            continue
        serie = cdi_decimal(base[coluna], coluna) if chave == "cdi" else base[coluna]
        linhas.append({"serie": nome, **metricas(serie, None if chave == "cdi" else cdi)})
    return pd.DataFrame(linhas)


def analise_periodica_carteira(base: pd.DataFrame, tipo: str) -> pd.DataFrame:
    colunas = localizar_carteira(base)
    dados = base.copy()
    if tipo == "ano":
        dados["periodo"] = dados["data"].dt.year.astype(str)
    else:
        dados["periodo"] = dados["data"].dt.year.astype(str) + " — " + np.where(
            dados["data"].dt.month <= 6, "1º semestre", "2º semestre"
        )

    linhas = []
    for periodo, grupo in dados.groupby("periodo", sort=True):
        linha: dict[str, Any] = {"periodo": periodo, "meses": len(grupo)}
        for chave in ["estrategia", "benchmark", "cdi"]:
            coluna = colunas[chave]
            if coluna and coluna in grupo.columns:
                serie = cdi_decimal(grupo[coluna], coluna) if chave == "cdi" else grupo[coluna]
                linha[f"retorno_{chave}"] = retorno_composto(serie)
            else:
                linha[f"retorno_{chave}"] = np.nan
        linha["excesso_vs_benchmark"] = linha["retorno_estrategia"] - linha["retorno_benchmark"]
        linha["excesso_vs_cdi"] = linha["retorno_estrategia"] - linha["retorno_cdi"]
        linhas.append(linha)
    return pd.DataFrame(linhas)


def analise_carteira_regime(base: pd.DataFrame) -> pd.DataFrame:
    colunas = localizar_carteira(base)
    linhas = []
    validos = base.dropna(subset=["regime"]) if "regime" in base.columns else pd.DataFrame()
    for regime, grupo in validos.groupby("regime", sort=False):
        linha: dict[str, Any] = {
            "regime": regime,
            "nome_regime": nome_regime(regime),
            "meses": len(grupo),
            "frequencia": len(grupo) / len(validos),
        }
        for chave in ["estrategia", "benchmark", "cdi"]:
            coluna = colunas[chave]
            if coluna and coluna in grupo.columns:
                serie = cdi_decimal(grupo[coluna], coluna) if chave == "cdi" else grupo[coluna]
                m = metricas(serie, serie_cdi(grupo))
                linha[f"retorno_{chave}"] = m["retorno_total"]
                linha[f"volatilidade_{chave}"] = m["volatilidade_anualizada"]
                linha[f"drawdown_{chave}"] = m["drawdown_maximo"]
            else:
                linha[f"retorno_{chave}"] = np.nan
                linha[f"volatilidade_{chave}"] = np.nan
                linha[f"drawdown_{chave}"] = np.nan
        linha["excesso_vs_benchmark"] = linha["retorno_estrategia"] - linha["retorno_benchmark"]
        linhas.append(linha)
    resultado = pd.DataFrame(linhas)
    if not resultado.empty:
        ordem = {regime: i for i, regime in enumerate(ORDEM_REGIMES)}
        resultado["ordem"] = resultado["regime"].map(ordem).fillna(999)
        resultado = resultado.sort_values("ordem").drop(columns="ordem").reset_index(drop=True)
    return resultado


def episodios_regime(base: pd.DataFrame, universo: pd.DataFrame) -> pd.DataFrame:
    dados = base.dropna(subset=["regime"]).copy() if "regime" in base.columns else pd.DataFrame()
    if dados.empty:
        return pd.DataFrame()
    dados["episodio"] = dados["regime"].ne(dados["regime"].shift()).cumsum()
    carteira = localizar_carteira(dados)
    linhas = []
    for episodio, grupo in dados.groupby("episodio"):
        linha: dict[str, Any] = {
            "episodio": int(episodio),
            "regime": grupo["regime"].iloc[0],
            "nome_regime": nome_regime(grupo["regime"].iloc[0]),
            "inicio": grupo["data"].min(),
            "fim": grupo["data"].max(),
            "meses": len(grupo),
        }
        for chave in ["estrategia", "benchmark", "cdi"]:
            coluna = carteira[chave]
            if coluna and coluna in grupo.columns:
                serie = cdi_decimal(grupo[coluna], coluna) if chave == "cdi" else grupo[coluna]
                linha[f"retorno_{chave}"] = retorno_composto(serie)
            else:
                linha[f"retorno_{chave}"] = np.nan
        linha["excesso_vs_benchmark"] = linha["retorno_estrategia"] - linha["retorno_benchmark"]

        ativos = {
            ticker: retorno_composto(grupo[ticker])
            for ticker in universo["ticker"]
            if ticker in grupo.columns
        }
        ativos = {k: v for k, v in ativos.items() if pd.notna(v)}
        if ativos:
            melhor = max(ativos, key=ativos.get)
            pior = min(ativos, key=ativos.get)
            linha.update({
                "melhor_ativo": melhor,
                "retorno_melhor_ativo": ativos[melhor],
                "pior_ativo": pior,
                "retorno_pior_ativo": ativos[pior],
            })
        linhas.append(linha)
    return pd.DataFrame(linhas)


def analise_rolling(base: pd.DataFrame) -> pd.DataFrame:
    colunas = localizar_carteira(base)
    resultado = base[["data"]].copy()
    for chave in ["estrategia", "benchmark", "cdi"]:
        coluna = colunas[chave]
        if not coluna or coluna not in base.columns:
            continue
        serie = cdi_decimal(base[coluna], coluna) if chave == "cdi" else pd.to_numeric(base[coluna], errors="coerce")
        resultado[f"retorno_{chave}_{JANELA_ROLLING}m"] = (
            (1.0 + serie).rolling(JANELA_ROLLING).apply(np.prod, raw=True) - 1.0
        )
    estrategia = f"retorno_estrategia_{JANELA_ROLLING}m"
    benchmark = f"retorno_benchmark_{JANELA_ROLLING}m"
    cdi = f"retorno_cdi_{JANELA_ROLLING}m"
    if estrategia in resultado and benchmark in resultado:
        resultado["excesso_vs_benchmark"] = resultado[estrategia] - resultado[benchmark]
    if estrategia in resultado and cdi in resultado:
        resultado["excesso_vs_cdi"] = resultado[estrategia] - resultado[cdi]
    return resultado.dropna(how="all", subset=[c for c in resultado.columns if c != "data"]).reset_index(drop=True)


def meses_extremos(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    colunas = localizar_carteira(base)
    estrategia = colunas["estrategia"]
    if not estrategia or estrategia not in base.columns:
        return pd.DataFrame(), pd.DataFrame()
    dados = base.copy()
    dados["retorno_estrategia"] = pd.to_numeric(dados[estrategia], errors="coerce")
    benchmark = colunas["benchmark"]
    cdi = colunas["cdi"]
    if benchmark and benchmark in dados.columns:
        dados["retorno_benchmark"] = pd.to_numeric(dados[benchmark], errors="coerce")
    if cdi and cdi in dados.columns:
        dados["retorno_cdi"] = cdi_decimal(dados[cdi], cdi)
    colunas_saida = [c for c in ["data", "regime", "nome_regime", "retorno_estrategia", "retorno_benchmark", "retorno_cdi"] if c in dados.columns]
    dados = dados.dropna(subset=["retorno_estrategia"])
    return (
        dados.nlargest(QUANTIDADE_EXTREMOS, "retorno_estrategia")[colunas_saida].reset_index(drop=True),
        dados.nsmallest(QUANTIDADE_EXTREMOS, "retorno_estrategia")[colunas_saida].reset_index(drop=True),
    )


def transicoes_regime(base: pd.DataFrame) -> pd.DataFrame:
    dados = base.dropna(subset=["regime"]).reset_index(drop=True) if "regime" in base.columns else pd.DataFrame()
    if dados.empty:
        return pd.DataFrame()
    carteira = localizar_carteira(dados)
    indices = dados.index[dados["regime"].ne(dados["regime"].shift())].tolist()
    linhas = []
    transicao_id = 0
    for indice in indices:
        if indice == 0:
            continue
        transicao_id += 1
        inicio = max(0, indice - JANELA_TRANSICAO)
        fim = min(len(dados) - 1, indice + JANELA_TRANSICAO)
        for posicao in range(inicio, fim + 1):
            linha: dict[str, Any] = {
                "transicao": transicao_id,
                "data_transicao": dados.loc[indice, "data"],
                "regime_anterior": dados.loc[indice - 1, "regime"],
                "novo_regime": dados.loc[indice, "regime"],
                "mes_relativo": posicao - indice,
                "data": dados.loc[posicao, "data"],
            }
            for chave in ["estrategia", "benchmark", "cdi"]:
                coluna = carteira[chave]
                valor = dados.loc[posicao, coluna] if coluna and coluna in dados.columns else np.nan
                if chave == "cdi" and coluna:
                    valor = cdi_decimal(pd.Series([valor]), coluna).iloc[0]
                linha[f"retorno_{chave}"] = valor
            linhas.append(linha)
    return pd.DataFrame(linhas)


def resumo_transicoes(transicoes: pd.DataFrame) -> pd.DataFrame:
    if transicoes.empty:
        return pd.DataFrame()
    linhas = []
    for transicao, grupo in transicoes.groupby("transicao"):
        pre = grupo.loc[grupo["mes_relativo"] < 0, "retorno_estrategia"]
        pos = grupo.loc[grupo["mes_relativo"] >= 0, "retorno_estrategia"]
        linhas.append({
            "transicao": transicao,
            "data": grupo["data_transicao"].iloc[0],
            "regime_anterior": nome_regime(grupo["regime_anterior"].iloc[0]),
            "novo_regime": nome_regime(grupo["novo_regime"].iloc[0]),
            "retorno_3m_antes": retorno_composto(pre),
            "retorno_mes_0_a_3": retorno_composto(pos),
        })
    return pd.DataFrame(linhas)


def contribuicoes(base: pd.DataFrame, universo: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for _, ativo in universo.iterrows():
        ticker = ativo["ticker"]
        if ticker not in base.columns:
            continue
        coluna_peso = localizar_coluna(base, [f"peso_{ticker}", f"weight_{ticker}"])
        if coluna_peso is None:
            continue
        peso = pd.to_numeric(base[coluna_peso], errors="coerce")
        retorno = pd.to_numeric(base[ticker], errors="coerce")
        for indice in base.index:
            valor = peso.loc[indice] * retorno.loc[indice]
            if pd.isna(valor):
                continue
            linhas.append({
                "data": base.loc[indice, "data"],
                "regime": base.loc[indice, "regime"] if "regime" in base.columns else "",
                "ticker": ticker,
                "segmento": ativo["segmento"],
                "peso": peso.loc[indice],
                "retorno_ativo": retorno.loc[indice],
                "contribuicao": valor,
            })
    return pd.DataFrame(linhas)



# ============================================================
# PERÍODOS OFICIAIS E SAÍDAS DO PIPELINE
# ============================================================


def meses_planejados(inicio: pd.Timestamp, fim: pd.Timestamp) -> int:
    """Quantidade de meses-calendário tocados pelo intervalo oficial."""

    return (fim.year - inicio.year) * 12 + fim.month - inicio.month + 1


def recortar_periodo_oficial(
    base: pd.DataFrame,
    periodo: dict[str, Any],
) -> pd.DataFrame:
    """Recorta a base no intervalo oficial informado."""

    if base.empty or "data" not in base.columns:
        return pd.DataFrame(columns=base.columns)

    mascara = (
        base["data"].ge(periodo["inicio"])
        & base["data"].le(periodo["fim"])
    )
    return base.loc[mascara].copy().reset_index(drop=True)


def linha_serie_metricas(
    dados: pd.DataFrame,
    nome_serie: str,
) -> pd.Series | None:
    """Obtém uma linha da tabela produzida por analise_carteira."""

    if dados.empty or "serie" not in dados.columns:
        return None

    linhas = dados.loc[dados["serie"].eq(nome_serie)]
    return linhas.iloc[0] if not linhas.empty else None


def resumo_periodos_oficiais(base: pd.DataFrame) -> pd.DataFrame:
    """Compara desenvolvimento, validação e teste final fora da amostra."""

    registros: list[dict[str, Any]] = []
    colunas_carteira = localizar_carteira(base)

    for periodo in PERIODOS_OFICIAIS:
        amostra = recortar_periodo_oficial(base, periodo)
        tabela_metricas = analise_carteira(amostra)
        estrategia = linha_serie_metricas(tabela_metricas, "Estratégia")
        benchmark = linha_serie_metricas(tabela_metricas, "Benchmark estático")
        cdi = linha_serie_metricas(tabela_metricas, "CDI")

        retorno_estrategia = (
            estrategia.get("retorno_total", np.nan)
            if estrategia is not None
            else np.nan
        )
        retorno_benchmark = (
            benchmark.get("retorno_total", np.nan)
            if benchmark is not None
            else np.nan
        )
        retorno_cdi = (
            cdi.get("retorno_total", np.nan)
            if cdi is not None
            else np.nan
        )

        coluna_turnover = colunas_carteira.get("turnover")
        coluna_custo = colunas_carteira.get("custo")
        turnover = (
            pd.to_numeric(amostra[coluna_turnover], errors="coerce").sum()
            if coluna_turnover and coluna_turnover in amostra.columns
            else np.nan
        )
        custo = (
            pd.to_numeric(amostra[coluna_custo], errors="coerce").sum()
            if coluna_custo and coluna_custo in amostra.columns
            else np.nan
        )

        meses_disponiveis = int(amostra["data"].nunique()) if not amostra.empty else 0
        meses_esperados = meses_planejados(periodo["inicio"], periodo["fim"])
        cobertura = meses_disponiveis / meses_esperados if meses_esperados else np.nan

        registros.append(
            {
                "codigo_periodo": periodo["codigo"],
                "periodo": periodo["nome"],
                "funcao": periodo["funcao"],
                "inicio_oficial": periodo["inicio"],
                "fim_oficial": periodo["fim"],
                "inicio_disponivel": (
                    amostra["data"].min() if not amostra.empty else pd.NaT
                ),
                "fim_disponivel": (
                    amostra["data"].max() if not amostra.empty else pd.NaT
                ),
                "meses_esperados": meses_esperados,
                "meses_disponiveis": meses_disponiveis,
                "cobertura_temporal": cobertura,
                "ajusta_parametros": periodo["ajusta_parametros"],
                "altera_regras": periodo["altera_regras"],
                "retorno_estrategia": retorno_estrategia,
                "retorno_benchmark": retorno_benchmark,
                "retorno_cdi": retorno_cdi,
                "excesso_vs_benchmark": (
                    retorno_estrategia - retorno_benchmark
                    if pd.notna(retorno_estrategia)
                    and pd.notna(retorno_benchmark)
                    else np.nan
                ),
                "excesso_vs_cdi": (
                    retorno_estrategia - retorno_cdi
                    if pd.notna(retorno_estrategia)
                    and pd.notna(retorno_cdi)
                    else np.nan
                ),
                "retorno_anualizado": (
                    estrategia.get("retorno_anualizado", np.nan)
                    if estrategia is not None
                    else np.nan
                ),
                "volatilidade_anualizada": (
                    estrategia.get("volatilidade_anualizada", np.nan)
                    if estrategia is not None
                    else np.nan
                ),
                "sharpe": (
                    estrategia.get("sharpe", np.nan)
                    if estrategia is not None
                    else np.nan
                ),
                "drawdown_maximo": (
                    estrategia.get("drawdown_maximo", np.nan)
                    if estrategia is not None
                    else np.nan
                ),
                "meses_positivos": (
                    estrategia.get("meses_positivos", np.nan)
                    if estrategia is not None
                    else np.nan
                ),
                "turnover_total": turnover,
                "custo_total": custo,
            }
        )

    return pd.DataFrame(registros)


def analises_detalhadas_periodos(
    base: pd.DataFrame,
    universo: pd.DataFrame,
) -> dict[str, dict[str, pd.DataFrame]]:
    """Calcula ativos, segmentos, regimes e carteira em cada bloco oficial."""

    resultado: dict[str, dict[str, pd.DataFrame]] = {}

    for periodo in PERIODOS_OFICIAIS:
        amostra = recortar_periodo_oficial(base, periodo)
        segmentos, retornos_segmentos = analise_segmentos(amostra, universo)
        resultado[periodo["codigo"]] = {
            "base": amostra,
            "carteira": analise_carteira(amostra),
            "ativos": analise_ativos(amostra, universo),
            "segmentos": segmentos,
            "retornos_segmentos": retornos_segmentos,
            "regimes": analise_carteira_regime(amostra),
            "episodios": episodios_regime(amostra, universo),
            "melhores": meses_extremos(amostra)[0],
            "piores": meses_extremos(amostra)[1],
            "contribuicoes": contribuicoes(amostra, universo),
        }

    return resultado


def formatar_resumo_periodos(dados: pd.DataFrame) -> pd.DataFrame:
    """Formata a tabela comparativa dos três blocos oficiais."""

    if dados.empty:
        return dados

    tabela = dados.copy()
    for coluna in [
        "inicio_oficial",
        "fim_oficial",
        "inicio_disponivel",
        "fim_disponivel",
    ]:
        tabela[coluna] = tabela[coluna].map(fmt_data)

    for coluna in [
        "cobertura_temporal",
        "retorno_estrategia",
        "retorno_benchmark",
        "retorno_cdi",
        "excesso_vs_benchmark",
        "excesso_vs_cdi",
        "retorno_anualizado",
        "volatilidade_anualizada",
        "drawdown_maximo",
        "meses_positivos",
        "turnover_total",
        "custo_total",
    ]:
        if coluna in tabela.columns:
            tabela[coluna] = tabela[coluna].map(fmt_pct)

    if "sharpe" in tabela.columns:
        tabela["sharpe"] = tabela["sharpe"].map(fmt_num)

    colunas = [
        "periodo",
        "funcao",
        "inicio_oficial",
        "fim_oficial",
        "inicio_disponivel",
        "fim_disponivel",
        "meses_disponiveis",
        "meses_esperados",
        "cobertura_temporal",
        "ajusta_parametros",
        "altera_regras",
        "retorno_estrategia",
        "retorno_benchmark",
        "retorno_cdi",
        "excesso_vs_benchmark",
        "excesso_vs_cdi",
        "volatilidade_anualizada",
        "sharpe",
        "drawdown_maximo",
        "turnover_total",
        "custo_total",
    ]
    tabela = tabela[[c for c in colunas if c in tabela.columns]]
    return tabela.rename(
        columns={
            "periodo": "Período",
            "funcao": "Função",
            "inicio_oficial": "Início oficial",
            "fim_oficial": "Fim oficial",
            "inicio_disponivel": "Início disponível",
            "fim_disponivel": "Fim disponível",
            "meses_disponiveis": "Meses disponíveis",
            "meses_esperados": "Meses esperados",
            "cobertura_temporal": "Cobertura",
            "ajusta_parametros": "Ajusta parâmetros?",
            "altera_regras": "Altera regras?",
            "retorno_estrategia": "Estratégia",
            "retorno_benchmark": "Benchmark",
            "retorno_cdi": "CDI",
            "excesso_vs_benchmark": "Excesso vs benchmark",
            "excesso_vs_cdi": "Excesso vs CDI",
            "volatilidade_anualizada": "Volatilidade anualizada",
            "sharpe": "Sharpe",
            "drawdown_maximo": "Drawdown máximo",
            "turnover_total": "Turnover total",
            "custo_total": "Custo total",
        }
    )


def classificar_etapa_grafico(caminho: Path) -> str:
    """Classifica gráfico pelo prefixo numérico do pipeline."""

    correspondencia = re.match(r"^(0[1-9]|1[0-9])[_-]", caminho.name)
    if not correspondencia:
        return "Outros gráficos"

    numero = correspondencia.group(1)
    nomes = {
        "01": "Etapa 01 — Coleta e qualidade",
        "02": "Etapa 02 — Análise exploratória",
        "03": "Etapa 03 — Regimes macroeconômicos",
        "04": "Etapa 04 — Alocação",
        "05": "Etapa 05 — Backtest",
        "06": "Etapa 06 — Otimização e walk-forward",
        "07": "Etapa 07 — Análise final",
        "08": "Etapa 08 — Auditoria",
        "09": "Etapa 09 — Relatório analítico",
    }
    return nomes.get(numero, f"Etapa {numero}")


def referencia_atualizacao(raiz: Path) -> datetime | None:
    """Obtém a modificação mais recente das bases centrais."""

    datas: list[datetime] = []
    for chave in ["selecao", "retornos", "macro", "regimes", "backtest"]:
        caminho = resolver(raiz, ARQUIVOS[chave])
        if caminho.is_file():
            datas.append(
                datetime.fromtimestamp(caminho.stat().st_mtime, tz=timezone.utc)
            )
    return max(datas) if datas else None


def status_atualizacao_arquivo(
    modificado: datetime,
    referencia: datetime | None,
) -> str:
    """Classifica a proximidade temporal com as bases centrais."""

    if referencia is None or modificado >= referencia:
        return "Atual ou posterior às bases centrais"

    diferenca_horas = (referencia - modificado).total_seconds() / 3600.0
    if diferenca_horas <= 24.0:
        return "Mesma execução provável"
    return "Verificar atualização"


def inventariar_saidas_pipeline(raiz: Path) -> pd.DataFrame:
    """Inventaria gráficos, tabelas, modelo final e auditoria."""

    referencia = referencia_atualizacao(raiz)
    registros: list[dict[str, Any]] = []

    for origem, relativo in PASTAS_PIPELINE.items():
        pasta = resolver(raiz, relativo)
        if not pasta.is_dir():
            continue

        for caminho in sorted(pasta.rglob("*")):
            if not caminho.is_file():
                continue
            modificado = datetime.fromtimestamp(
                caminho.stat().st_mtime,
                tz=timezone.utc,
            )
            registros.append(
                {
                    "origem": origem,
                    "arquivo": caminho.name,
                    "caminho": caminho.relative_to(raiz).as_posix(),
                    "extensao": caminho.suffix.lower(),
                    "modificacao_utc": modificado,
                    "tamanho_bytes": caminho.stat().st_size,
                    "status_atualizacao": status_atualizacao_arquivo(
                        modificado,
                        referencia,
                    ),
                }
            )

    return pd.DataFrame(registros)


def copiar_graficos_pipeline(
    raiz: Path,
    saida: Path,
) -> tuple[list[Path], pd.DataFrame]:
    """Copia para o relatório todos os gráficos já gerados pelo pipeline."""

    origem = resolver(raiz, PASTAS_PIPELINE["graficos"])
    destino = saida / "graficos_pipeline"
    destino.mkdir(parents=True, exist_ok=True)

    extensoes = {".png", ".jpg", ".jpeg", ".svg", ".webp"}
    copiados: list[Path] = []
    registros: list[dict[str, Any]] = []
    referencia = referencia_atualizacao(raiz)

    if not origem.is_dir():
        return copiados, pd.DataFrame()

    for arquivo in sorted(origem.rglob("*")):
        if not arquivo.is_file() or arquivo.suffix.lower() not in extensoes:
            continue

        relativo = arquivo.relative_to(origem)
        destino_arquivo = destino / relativo
        destino_arquivo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(arquivo, destino_arquivo)
        copiados.append(destino_arquivo)

        modificado = datetime.fromtimestamp(
            arquivo.stat().st_mtime,
            tz=timezone.utc,
        )
        registros.append(
            {
                "etapa": classificar_etapa_grafico(arquivo),
                "arquivo": arquivo.name,
                "origem": arquivo.relative_to(raiz).as_posix(),
                "copia_relatorio": destino_arquivo.relative_to(saida).as_posix(),
                "modificacao_utc": modificado,
                "status_atualizacao": status_atualizacao_arquivo(
                    modificado,
                    referencia,
                ),
            }
        )

    return copiados, pd.DataFrame(registros)


def ler_texto_limitado(caminho: Path, limite: int = 12000) -> str:
    """Lê arquivo textual sem permitir um anexo Markdown excessivo."""

    try:
        texto = caminho.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        texto = caminho.read_text(encoding="latin1")

    if len(texto) > limite:
        return texto[:limite] + "\n\n[conteúdo truncado no relatório]"
    return texto


def carregar_artefatos_modelo_final(
    raiz: Path,
) -> list[dict[str, Any]]:
    """Carrega previews dos arquivos em outputs/modelo_final."""

    pasta = resolver(raiz, PASTAS_PIPELINE["modelo_final"])
    artefatos: list[dict[str, Any]] = []

    if not pasta.is_dir():
        return artefatos

    for caminho in sorted(pasta.rglob("*")):
        if not caminho.is_file():
            continue

        extensao = caminho.suffix.lower()
        item: dict[str, Any] = {
            "nome": caminho.name,
            "caminho": caminho.relative_to(raiz).as_posix(),
            "extensao": extensao,
            "tabela": pd.DataFrame(),
            "texto": "",
        }

        try:
            if extensao == ".csv":
                item["tabela"] = ler_csv(caminho, obrigatorio=False)
            elif extensao == ".json":
                conteudo = json.loads(ler_texto_limitado(caminho, 50000))
                item["texto"] = json.dumps(
                    conteudo,
                    ensure_ascii=False,
                    indent=2,
                )
            elif extensao in {".txt", ".md", ".yaml", ".yml"}:
                item["texto"] = ler_texto_limitado(caminho)
            else:
                item["texto"] = "Arquivo binário ou formato não exibido."
        except Exception as erro:
            item["texto"] = f"Falha ao interpretar o arquivo: {erro}"

        artefatos.append(item)

    return artefatos


def carregar_tabelas_pipeline(
    raiz: Path,
    limite_arquivos: int = 40,
) -> list[dict[str, Any]]:
    """Carrega as tabelas mais relevantes de outputs/tabelas e auditoria."""

    candidatos: list[Path] = []
    for chave in ["tabelas", "auditoria"]:
        pasta = resolver(raiz, PASTAS_PIPELINE[chave])
        if pasta.is_dir():
            candidatos.extend(sorted(pasta.rglob("*.csv")))

    relevantes = [
        caminho
        for caminho in candidatos
        if any(
            palavra in normalizar(caminho.stem).lower()
            for palavra in PALAVRAS_TABELAS_RELEVANTES
        )
    ]
    selecionados = relevantes[:limite_arquivos]

    tabelas: list[dict[str, Any]] = []
    for caminho in selecionados:
        try:
            dados = ler_csv(caminho, obrigatorio=False)
            erro = ""
        except Exception as excecao:
            dados = pd.DataFrame()
            erro = str(excecao)

        tabelas.append(
            {
                "nome": caminho.name,
                "caminho": caminho.relative_to(raiz).as_posix(),
                "dados": dados,
                "erro": erro,
            }
        )

    return tabelas


def gerar_graficos_periodos_oficiais(
    saida: Path,
    analises_periodos: dict[str, dict[str, pd.DataFrame]],
) -> list[Path]:
    """Gera um gráfico acumulado separado para cada bloco oficial."""

    pasta = saida / "graficos_periodos"
    pasta.mkdir(parents=True, exist_ok=True)
    gerados: list[Path] = []

    for indice, periodo in enumerate(PERIODOS_OFICIAIS, start=1):
        base_periodo = analises_periodos[periodo["codigo"]]["base"]
        colunas = localizar_carteira(base_periodo)
        if base_periodo.empty or colunas["estrategia"] is None:
            continue

        figura, eixo = plt.subplots(figsize=(12, 6))
        adicionou = False
        for rotulo, chave in [
            ("Estratégia", "estrategia"),
            ("Benchmark", "benchmark"),
            ("CDI", "cdi"),
        ]:
            coluna = colunas[chave]
            if coluna is None or coluna not in base_periodo.columns:
                continue
            serie = (
                cdi_decimal(base_periodo[coluna], coluna)
                if chave == "cdi"
                else pd.to_numeric(base_periodo[coluna], errors="coerce")
            )
            indice_acumulado = VALOR_INICIAL * (1.0 + serie.fillna(0.0)).cumprod()
            eixo.plot(base_periodo["data"], indice_acumulado, label=rotulo)
            adicionou = True

        if not adicionou:
            plt.close(figura)
            continue

        eixo.set_title(periodo["nome"])
        eixo.set_xlabel("Data")
        eixo.set_ylabel("Índice base 100")
        eixo.grid(alpha=0.25)
        eixo.legend()
        caminho = pasta / f"{indice:02d}_{normalizar(periodo['codigo']).lower()}.png"
        salvar_figura(figura, caminho)
        gerados.append(caminho)

    return gerados


def formatar_inventario_saidas(dados: pd.DataFrame) -> pd.DataFrame:
    """Formata o inventário das saídas do pipeline."""

    if dados.empty:
        return dados

    tabela = dados.copy()
    tabela["modificacao_utc"] = tabela["modificacao_utc"].map(
        lambda valor: (
            pd.to_datetime(valor).strftime("%d/%m/%Y %H:%M")
            if pd.notna(valor)
            else "—"
        )
    )
    tabela["tamanho_bytes"] = tabela["tamanho_bytes"].map(
        lambda valor: f"{int(valor):,}".replace(",", ".")
    )
    return tabela.rename(
        columns={
            "origem": "Origem",
            "arquivo": "Arquivo",
            "caminho": "Caminho",
            "extensao": "Extensão",
            "modificacao_utc": "Modificação UTC",
            "tamanho_bytes": "Bytes",
            "status_atualizacao": "Situação temporal",
        }
    )


def observacao_cobertura_periodo(linha: pd.Series) -> str:
    """Explica se o bloco oficial está completo na base disponível."""

    disponiveis = int(linha.get("meses_disponiveis", 0))
    esperados = int(linha.get("meses_esperados", 0))
    if disponiveis == 0:
        return "Não há observações disponíveis para este bloco."
    if disponiveis < esperados:
        return (
            f"A base disponível cobre {disponiveis} de {esperados} meses "
            "do intervalo oficial. As conclusões deste bloco são parciais."
        )
    return "A cobertura mensal disponível contempla todo o intervalo oficial."


# ============================================================
# INVENTÁRIO E QUALIDADE
# ============================================================


def inventario(raiz: Path) -> pd.DataFrame:
    linhas = []
    for chave, relativo in ARQUIVOS.items():
        caminho = resolver(raiz, relativo)
        existe = caminho.is_file()
        linhas.append({
            "arquivo": chave,
            "caminho": relativo,
            "existe": existe,
            "modificacao_utc": datetime.fromtimestamp(caminho.stat().st_mtime, tz=timezone.utc) if existe else pd.NaT,
            "tamanho_bytes": caminho.stat().st_size if existe else 0,
        })
    dados = pd.DataFrame(linhas)
    centrais = dados.loc[
        dados["caminho"].isin([
            ARQUIVOS["selecao"], ARQUIVOS["retornos"], ARQUIVOS["macro"], ARQUIVOS["regimes"],
        ]) & dados["existe"],
        "modificacao_utc",
    ]
    referencia = centrais.max() if not centrais.empty else pd.NaT
    dados["possivelmente_desatualizado"] = False
    if pd.notna(referencia):
        limite = referencia - pd.Timedelta(hours=24)
        dados.loc[
            dados["existe"]
            & dados["modificacao_utc"].notna()
            & (dados["modificacao_utc"] < limite),
            "possivelmente_desatualizado",
        ] = True
    return dados


def cobertura(bases: dict[str, pd.DataFrame]) -> pd.DataFrame:
    linhas = []
    for nome, dados in bases.items():
        linhas.append({
            "base": nome,
            "registros": len(dados),
            "inicio": dados["data"].min() if not dados.empty and "data" in dados else pd.NaT,
            "fim": dados["data"].max() if not dados.empty and "data" in dados else pd.NaT,
            "colunas": len(dados.columns),
            "ausentes": int(dados.isna().sum().sum()) if not dados.empty else 0,
        })
    return pd.DataFrame(linhas)


# ============================================================
# GRÁFICOS
# ============================================================


def salvar_figura(figura: plt.Figure, caminho: Path) -> None:
    figura.tight_layout()
    figura.savefig(caminho, dpi=160, bbox_inches="tight")
    plt.close(figura)


def grafico_acumulado(base: pd.DataFrame, caminho: Path) -> bool:
    colunas = localizar_carteira(base)
    figura, eixo = plt.subplots(figsize=(12, 6))
    adicionou = False
    for rotulo, chave in [("Estratégia", "estrategia"), ("Benchmark", "benchmark"), ("CDI", "cdi")]:
        coluna = colunas[chave]
        if not coluna or coluna not in base.columns:
            continue
        serie = cdi_decimal(base[coluna], coluna) if chave == "cdi" else pd.to_numeric(base[coluna], errors="coerce")
        eixo.plot(base["data"], VALOR_INICIAL * (1.0 + serie.fillna(0.0)).cumprod(), label=rotulo)
        adicionou = True
    if not adicionou:
        plt.close(figura)
        return False
    eixo.set_title("Desempenho acumulado")
    eixo.set_xlabel("Data")
    eixo.set_ylabel("Índice base 100")
    eixo.grid(alpha=0.25)
    eixo.legend()
    salvar_figura(figura, caminho)
    return True


def grafico_drawdown(base: pd.DataFrame, caminho: Path) -> bool:
    colunas = localizar_carteira(base)
    figura, eixo = plt.subplots(figsize=(12, 5))
    adicionou = False
    for rotulo, chave in [("Estratégia", "estrategia"), ("Benchmark", "benchmark")]:
        coluna = colunas[chave]
        if coluna and coluna in base.columns:
            eixo.plot(base["data"], drawdown(base[coluna]) * 100.0, label=rotulo)
            adicionou = True
    if not adicionou:
        plt.close(figura)
        return False
    eixo.set_title("Drawdown")
    eixo.set_ylabel("Drawdown (%)")
    eixo.grid(alpha=0.25)
    eixo.legend()
    salvar_figura(figura, caminho)
    return True


def grafico_macro(base: pd.DataFrame, caminho: Path) -> bool:
    colunas = localizar_macro(base)
    figura, eixo = plt.subplots(figsize=(12, 5))
    adicionou = False
    for rotulo, chave in [("Inflação", "inflacao"), ("Atividade", "atividade")]:
        coluna = colunas[chave]
        if coluna and coluna in base.columns:
            eixo.plot(base["data"], pd.to_numeric(base[coluna], errors="coerce"), label=rotulo)
            adicionou = True
    if not adicionou:
        plt.close(figura)
        return False
    eixo.axhline(0.0, linewidth=1.0)
    eixo.set_title("Sinais macroeconômicos")
    eixo.grid(alpha=0.25)
    eixo.legend()
    salvar_figura(figura, caminho)
    return True


def grafico_regimes(base: pd.DataFrame, caminho: Path) -> bool:
    dados = base.dropna(subset=["regime"]) if "regime" in base.columns else pd.DataFrame()
    if dados.empty:
        return False
    mapa = {regime: i + 1 for i, regime in enumerate(ORDEM_REGIMES)}
    figura, eixo = plt.subplots(figsize=(12, 4))
    eixo.step(dados["data"], dados["regime"].map(mapa), where="post")
    eixo.set_yticks(list(mapa.values()), [NOMES_REGIMES[r] for r in ORDEM_REGIMES])
    eixo.set_title("Linha temporal dos regimes")
    eixo.grid(alpha=0.25)
    salvar_figura(figura, caminho)
    return True


def grafico_segmento(base: pd.DataFrame, universo: pd.DataFrame, segmento: str, caminho: Path) -> bool:
    tickers = [t for t in universo.loc[universo["segmento"] == segmento, "ticker"] if t in base.columns]
    if not tickers:
        return False
    figura, eixo = plt.subplots(figsize=(12, 6))
    for ticker in tickers:
        serie = pd.to_numeric(base[ticker], errors="coerce").fillna(0.0)
        eixo.plot(base["data"], VALOR_INICIAL * (1.0 + serie).cumprod(), label=ticker)
    eixo.set_title(f"Retorno acumulado — {segmento}")
    eixo.set_ylabel("Índice base 100")
    eixo.grid(alpha=0.25)
    eixo.legend()
    salvar_figura(figura, caminho)
    return True


def grafico_rolling(rolling: pd.DataFrame, caminho: Path) -> bool:
    if rolling.empty:
        return False
    figura, eixo = plt.subplots(figsize=(12, 5))
    adicionou = False
    for coluna, rotulo in [("excesso_vs_benchmark", "Excesso vs benchmark"), ("excesso_vs_cdi", "Excesso vs CDI")]:
        if coluna in rolling:
            eixo.plot(rolling["data"], rolling[coluna] * 100.0, label=rotulo)
            adicionou = True
    if not adicionou:
        plt.close(figura)
        return False
    eixo.axhline(0.0, linewidth=1.0)
    eixo.set_title(f"Excesso móvel de {JANELA_ROLLING} meses")
    eixo.set_ylabel("Excesso (%)")
    eixo.grid(alpha=0.25)
    eixo.legend()
    salvar_figura(figura, caminho)
    return True


def gerar_graficos(saida: Path, base: pd.DataFrame, universo: pd.DataFrame, rolling: pd.DataFrame) -> list[Path]:
    pasta = saida / "graficos"
    pasta.mkdir(parents=True, exist_ok=True)
    graficos: list[Path] = []
    tarefas = [
        (grafico_acumulado, (base, pasta / "01_desempenho_acumulado.png")),
        (grafico_drawdown, (base, pasta / "02_drawdown.png")),
        (grafico_macro, (base, pasta / "03_sinais_macro.png")),
        (grafico_regimes, (base, pasta / "04_regimes.png")),
        (grafico_rolling, (rolling, pasta / "05_rolling_12m.png")),
    ]
    for funcao, parametros in tarefas:
        try:
            if funcao(*parametros):
                graficos.append(parametros[-1])
        except Exception as erro:
            print(f"ATENÇÃO: gráfico {parametros[-1].name} não gerado: {erro}")
    for indice, segmento in enumerate(sorted(universo["segmento"].unique()), start=6):
        nome = normalizar(segmento).lower()
        caminho = pasta / f"{indice:02d}_ativos_{nome}.png"
        try:
            if grafico_segmento(base, universo, segmento, caminho):
                graficos.append(caminho)
        except Exception as erro:
            print(f"ATENÇÃO: gráfico {caminho.name} não gerado: {erro}")
    return graficos


# ============================================================
# FORMATAÇÃO DE RESULTADOS
# ============================================================


def formatar_metricas(dados: pd.DataFrame) -> pd.DataFrame:
    if dados.empty:
        return dados
    tabela = dados.copy()
    percentuais = [
        "retorno_total", "retorno_anualizado", "volatilidade_anualizada",
        "drawdown_maximo", "meses_positivos", "melhor_mes", "pior_mes",
    ]
    for coluna in percentuais:
        if coluna in tabela:
            tabela[coluna] = tabela[coluna].map(fmt_pct)
    if "sharpe" in tabela:
        tabela["sharpe"] = tabela["sharpe"].map(fmt_num)
    return tabela


def formatar_periodos(dados: pd.DataFrame) -> pd.DataFrame:
    if dados.empty:
        return dados
    tabela = dados.copy()
    termos_percentuais = (
        "retorno_",
        "volatilidade_",
        "drawdown_",
        "excesso_",
        "frequencia",
        "custo_",
        "turnover_",
    )
    for coluna in tabela.columns:
        if coluna.startswith(termos_percentuais) or coluna in {
            "frequencia",
            "cobertura_temporal",
        }:
            tabela[coluna] = tabela[coluna].map(fmt_pct)
    return tabela


def formatar_episodios(dados: pd.DataFrame) -> pd.DataFrame:
    if dados.empty:
        return dados
    tabela = dados.copy()
    tabela["inicio"] = tabela["inicio"].map(fmt_data)
    tabela["fim"] = tabela["fim"].map(fmt_data)
    for coluna in ["retorno_estrategia", "retorno_benchmark", "retorno_cdi", "excesso_vs_benchmark", "retorno_melhor_ativo", "retorno_pior_ativo"]:
        if coluna in tabela:
            tabela[coluna] = tabela[coluna].map(fmt_pct)
    return tabela


def formatar_extremos(dados: pd.DataFrame) -> pd.DataFrame:
    if dados.empty:
        return dados
    tabela = dados.copy()
    tabela["data"] = tabela["data"].map(fmt_data)
    if "regime" in tabela:
        tabela["regime"] = tabela["regime"].map(nome_regime)
    for coluna in ["retorno_estrategia", "retorno_benchmark", "retorno_cdi"]:
        if coluna in tabela:
            tabela[coluna] = tabela[coluna].map(fmt_pct)
    return tabela


# ============================================================
# RELATÓRIO
# ============================================================


def conclusoes(
    ativos: pd.DataFrame,
    carteira: pd.DataFrame,
    regimes: pd.DataFrame,
    rolling: pd.DataFrame,
) -> list[str]:
    linhas: list[str] = []
    if not carteira.empty:
        estrategia = carteira.loc[carteira["serie"] == "Estratégia"]
        benchmark = carteira.loc[carteira["serie"] == "Benchmark estático"]
        if not estrategia.empty:
            e = estrategia.iloc[0]
            linhas.append(
                f"A estratégia acumulou **{fmt_pct(e['retorno_total'])}**, com volatilidade anualizada de "
                f"**{fmt_pct(e['volatilidade_anualizada'])}** e drawdown máximo de **{fmt_pct(e['drawdown_maximo'])}**."
            )
        if not estrategia.empty and not benchmark.empty:
            diferenca = estrategia.iloc[0]["retorno_total"] - benchmark.iloc[0]["retorno_total"]
            linhas.append(f"A diferença acumulada contra o benchmark foi de **{fmt_pct(diferenca)}**.")
    if not ativos.empty:
        melhor = ativos.loc[ativos["retorno_total"].idxmax()]
        pior = ativos.loc[ativos["retorno_total"].idxmin()]
        linhas.append(f"O melhor ativo no período foi **{melhor['ticker']}**, com **{fmt_pct(melhor['retorno_total'])}**.")
        linhas.append(f"O pior ativo no período foi **{pior['ticker']}**, com **{fmt_pct(pior['retorno_total'])}**.")
    if not regimes.empty:
        validos = regimes.dropna(subset=["retorno_estrategia"])
        if not validos.empty:
            melhor = validos.loc[validos["retorno_estrategia"].idxmax()]
            pior = validos.loc[validos["retorno_estrategia"].idxmin()]
            linhas.append(f"O melhor regime para a estratégia foi **{melhor['nome_regime']}**.")
            linhas.append(f"O pior regime para a estratégia foi **{pior['nome_regime']}**.")
    if not rolling.empty and "excesso_vs_benchmark" in rolling:
        serie = rolling["excesso_vs_benchmark"].dropna()
        if not serie.empty:
            linhas.append(
                f"A estratégia superou o benchmark em **{fmt_pct((serie > 0).mean())}** das janelas móveis de {JANELA_ROLLING} meses."
            )
    return linhas


def caminho_md(relatorio: Path, arquivo: Path) -> str:
    return Path(os.path.relpath(arquivo, start=relatorio.parent)).as_posix()


def construir_relatorio(
    relatorio: Path,
    base: pd.DataFrame,
    universo: pd.DataFrame,
    inventario_df: pd.DataFrame,
    cobertura_df: pd.DataFrame,
    ativos: pd.DataFrame,
    segmentos: pd.DataFrame,
    ativos_ano: pd.DataFrame,
    ativos_semestre: pd.DataFrame,
    ativos_regime: pd.DataFrame,
    carteira: pd.DataFrame,
    carteira_ano: pd.DataFrame,
    carteira_semestre: pd.DataFrame,
    carteira_regime: pd.DataFrame,
    episodios: pd.DataFrame,
    rolling: pd.DataFrame,
    melhores: pd.DataFrame,
    piores: pd.DataFrame,
    transicoes_resumo: pd.DataFrame,
    contribuicoes_df: pd.DataFrame,
    metricas_finais: pd.DataFrame,
    pesos_oficiais: pd.DataFrame,
    scorecard: pd.DataFrame,
    auditoria: pd.DataFrame,
    graficos: list[Path],
    resumo_periodos: pd.DataFrame,
    analises_periodos: dict[str, dict[str, pd.DataFrame]],
    graficos_periodos: list[Path],
    graficos_pipeline: list[Path],
    inventario_graficos: pd.DataFrame,
    inventario_saidas: pd.DataFrame,
    artefatos_modelo: list[dict[str, Any]],
    tabelas_pipeline: list[dict[str, Any]],
) -> str:
    """Constrói o Markdown detalhado com os três blocos temporais oficiais."""

    partes: list[str] = [
        "# Relatório Analítico Detalhado",
        "",
        "## Alocação Quantitativa por Regimes Macroeconômicos",
        "",
        f"**Versão do gerador:** {VERSAO}  ",
        f"**Gerado em:** {datetime.now().astimezone().strftime('%d/%m/%Y %H:%M:%S %Z')}  ",
        f"**Período disponível na base consolidada:** {fmt_data(base['data'].min())} a {fmt_data(base['data'].max())}  ",
        f"**Universo:** {len(universo)} ativos selecionados  ",
        "",
        "> O relatório separa desenvolvimento, validação e teste final fora da amostra. "
        "Resultados desses blocos não devem ser misturados, pois cumprem funções diferentes.",
        "",
        "---",
        "",
        "## 1. Resumo executivo",
        "",
        "A estratégia utiliza inflação e atividade econômica para classificar o cenário "
        "brasileiro e ajustar uma carteira multimercado. A avaliação temporal oficial é:",
        "",
        tabela_md(formatar_resumo_periodos(resumo_periodos)),
        "",
    ]

    for linha in conclusoes(ativos, carteira, carteira_regime, rolling):
        partes.append(f"- {linha}")

    partes += [
        "",
        "### Regra de interpretação dos resultados",
        "",
        "- **2020–2023:** resultados de desenvolvimento podem refletir calibração e não são prova de generalização.",
        "- **2024–2025:** validação com parâmetros e regras congelados.",
        "- **2026:** teste final fora da amostra, também sem alteração de regras ou parâmetros.",
        "",
        "---",
        "",
        "## 2. Metodologia temporal oficial",
        "",
        "| Período | Função | Ajusta parâmetros? | Altera regras? |",
        "| --- | --- | ---: | ---: |",
        "| 01/01/2020 a 31/12/2023 | Desenvolvimento e calibração | Sim | Sim |",
        "| 01/01/2024 a 31/12/2025 | Validação | Não | Não |",
        "| 01/01/2026 a 02/08/2026 | Teste final fora da amostra | Não | Não |",
        "",
        "```text",
        "Dados e retornos: mensais",
        "Rebalanceamento: mensal",
        "Confirmação do regime: 3 meses",
        "Defasagem do sinal: 1 mês",
        "Recalibração walk-forward: anual",
        "Treino inicial: 48 meses",
        "Janela de treino: expansiva",
        "Focus: consulta semanal, mas sinal oficial mensal",
        "```",
        "",
        "---",
        "",
        "## 3. Fontes, qualidade e atualização",
        "",
        "### Arquivos centrais",
        "",
    ]

    inv = inventario_df.copy()
    inv["existe"] = inv["existe"].map(lambda valor: "Sim" if valor else "Não")
    inv["possivelmente_desatualizado"] = inv["possivelmente_desatualizado"].map(
        lambda valor: "Sim" if valor else "Não"
    )
    inv["modificacao_utc"] = inv["modificacao_utc"].map(
        lambda valor: pd.to_datetime(valor).strftime("%d/%m/%Y %H:%M")
        if pd.notna(valor)
        else "—"
    )
    partes += [tabela_md(inv), "", "### Cobertura das bases", ""]

    cob = cobertura_df.copy()
    cob["inicio"] = cob["inicio"].map(fmt_data)
    cob["fim"] = cob["fim"].map(fmt_data)
    partes += [tabela_md(cob), "", "### Inventário das saídas do pipeline", ""]
    partes += [tabela_md(formatar_inventario_saidas(inventario_saidas), limite=200), ""]

    partes += [
        "---",
        "",
        "## 4. Universo de investimento",
        "",
        tabela_md(universo),
        "",
        "### Distribuição por segmento",
        "",
        tabela_md(
            universo.groupby("segmento", as_index=False).agg(
                quantidade=("ticker", "size")
            )
        ),
        "",
        "---",
        "",
        "## 5. Indicadores e regimes macroeconômicos",
        "",
    ]

    macro = localizar_macro(base)
    linhas_macro: list[dict[str, Any]] = []
    for chave, nome in [
        ("ipca", "IPCA mensal"),
        ("ipca_12m", "IPCA em 12 meses"),
        ("inflacao", "Tendência da inflação"),
        ("ibc", "IBC-Br"),
        ("ibc_dessaz", "IBC-Br dessazonalizado"),
        ("atividade", "Tendência da atividade"),
        ("cdi", "CDI mensal"),
    ]:
        coluna = macro[chave]
        if coluna and coluna in base.columns:
            serie = pd.to_numeric(base[coluna], errors="coerce").dropna()
            if not serie.empty:
                linhas_macro.append(
                    {
                        "indicador": nome,
                        "coluna": coluna,
                        "primeiro": fmt_num(serie.iloc[0], 4),
                        "último": fmt_num(serie.iloc[-1], 4),
                        "mínimo": fmt_num(serie.min(), 4),
                        "máximo": fmt_num(serie.max(), 4),
                        "observações": len(serie),
                    }
                )
    partes += [tabela_md(pd.DataFrame(linhas_macro)), ""]
    partes += [
        "```text",
        "Atividade alta + inflação em queda = Expansão desinflacionária",
        "Atividade alta + inflação em alta = Expansão inflacionária",
        "Atividade em queda + inflação em alta = Estagflação",
        "Atividade em queda + inflação em queda = Recessão desinflacionária",
        "```",
        "",
        "### Desempenho consolidado por regime",
        "",
        tabela_md(formatar_periodos(carteira_regime)),
        "",
    ]

    # Blocos oficiais detalhados
    for numero_secao, periodo in enumerate(PERIODOS_OFICIAIS, start=6):
        detalhe = analises_periodos[periodo["codigo"]]
        linha_resumo = resumo_periodos.loc[
            resumo_periodos["codigo_periodo"].eq(periodo["codigo"])
        ].iloc[0]
        partes += [
            "---",
            "",
            f"## {numero_secao}. {periodo['nome']}",
            "",
            f"**Intervalo oficial:** {fmt_data(periodo['inicio'])} a {fmt_data(periodo['fim'])}  ",
            f"**Função:** {periodo['funcao']}  ",
            f"**Ajusta parâmetros:** {periodo['ajusta_parametros']}  ",
            f"**Altera regras:** {periodo['altera_regras']}  ",
            "",
            f"> {observacao_cobertura_periodo(linha_resumo)}",
            "",
            "### Métricas da carteira",
            "",
            tabela_md(formatar_metricas(detalhe["carteira"])),
            "",
            "### Resultado por regime dentro do período",
            "",
            tabela_md(formatar_periodos(detalhe["regimes"])),
            "",
            "### Segmentos",
            "",
            tabela_md(formatar_metricas(detalhe["segmentos"])),
            "",
            "### Ativos",
            "",
            tabela_md(formatar_metricas(detalhe["ativos"])),
            "",
            f"### {QUANTIDADE_EXTREMOS} melhores meses",
            "",
            tabela_md(formatar_extremos(detalhe["melhores"])),
            "",
            f"### {QUANTIDADE_EXTREMOS} piores meses",
            "",
            tabela_md(formatar_extremos(detalhe["piores"])),
            "",
        ]

        grafico_periodo = [
            caminho
            for caminho in graficos_periodos
            if normalizar(periodo["codigo"]).lower() in caminho.stem
        ]
        if grafico_periodo:
            partes += [
                f"![Desempenho — {periodo['nome']}]({caminho_md(relatorio, grafico_periodo[0])})",
                "",
            ]

        if periodo["codigo"] == "DESENVOLVIMENTO_CALIBRACAO":
            partes.append(
                "**Interpretação:** este bloco foi usado para construir e calibrar o modelo. "
                "Resultados fortes aqui não devem ser tratados isoladamente como evidência fora da amostra."
            )
        elif periodo["codigo"] == "VALIDACAO":
            partes.append(
                "**Interpretação:** o objetivo é verificar se as regras definidas no desenvolvimento "
                "continuaram funcionando sem novos ajustes."
            )
        else:
            partes.append(
                "**Interpretação:** este é o principal teste de generalização. Qualquer cobertura inferior "
                "ao intervalo oficial deve ser tratada como resultado parcial."
            )
        partes.append("")

    partes += [
        "---",
        "",
        "## 9. Comparação entre desenvolvimento, validação e teste final",
        "",
        tabela_md(formatar_resumo_periodos(resumo_periodos)),
        "",
        "A comparação deve priorizar validação e teste final. O bloco de desenvolvimento "
        "explica como o modelo foi escolhido; os outros dois blocos avaliam sua capacidade de generalização.",
        "",
        "---",
        "",
        "## 10. Análise individual dos ativos no período completo",
        "",
        tabela_md(formatar_metricas(ativos)),
        "",
        "### Ativos por ano",
        "",
    ]

    ativos_ano_fmt = ativos_ano.copy()
    if not ativos_ano_fmt.empty:
        ativos_ano_fmt["retorno"] = ativos_ano_fmt["retorno"].map(fmt_pct)
    partes += [tabela_md(ativos_ano_fmt), "", "### Ativos por semestre", ""]
    ativos_semestre_fmt = ativos_semestre.copy()
    if not ativos_semestre_fmt.empty:
        ativos_semestre_fmt["retorno"] = ativos_semestre_fmt["retorno"].map(fmt_pct)
    partes += [tabela_md(ativos_semestre_fmt), "", "### Ativos por regime", ""]
    partes += [tabela_md(formatar_metricas(ativos_regime)), ""]

    partes += [
        "---",
        "",
        "## 11. Análise por segmento",
        "",
        tabela_md(formatar_metricas(segmentos)),
        "",
        "---",
        "",
        "## 12. Episódios macroeconômicos",
        "",
        "Cada episódio representa uma sequência contínua de meses no mesmo regime.",
        "",
        tabela_md(formatar_episodios(episodios)),
        "",
    ]
    if not episodios.empty:
        for _, episodio in episodios.iterrows():
            partes += [
                f"### Episódio {int(episodio['episodio'])} — {episodio['nome_regime']}",
                "",
                f"- Período: **{fmt_data(episodio['inicio'])} a {fmt_data(episodio['fim'])}**.",
                f"- Duração: **{int(episodio['meses'])} meses**.",
                f"- Estratégia: **{fmt_pct(episodio['retorno_estrategia'])}**.",
                f"- Benchmark: **{fmt_pct(episodio['retorno_benchmark'])}**.",
                f"- Excesso: **{fmt_pct(episodio['excesso_vs_benchmark'])}**.",
                f"- Melhor ativo: **{episodio.get('melhor_ativo', '—')}** "
                f"({fmt_pct(episodio.get('retorno_melhor_ativo'))}).",
                f"- Pior ativo: **{episodio.get('pior_ativo', '—')}** "
                f"({fmt_pct(episodio.get('retorno_pior_ativo'))}).",
                "",
            ]

    trans = transicoes_resumo.copy()
    if not trans.empty:
        trans["data"] = trans["data"].map(fmt_data)
        trans["retorno_3m_antes"] = trans["retorno_3m_antes"].map(fmt_pct)
        trans["retorno_mes_0_a_3"] = trans["retorno_mes_0_a_3"].map(fmt_pct)
    partes += [
        "---",
        "",
        "## 13. Transições de regime",
        "",
        tabela_md(trans),
        "",
        "---",
        "",
        "## 14. Contribuições, turnover e custos",
        "",
    ]

    if contribuicoes_df.empty:
        partes.append(
            "_As colunas de peso por ativo não foram encontradas na base consolidada; "
            "a contribuição peso × retorno não foi calculada._"
        )
    else:
        resumo_contribuicoes = contribuicoes_df.groupby(
            ["ticker", "segmento"], as_index=False
        ).agg(
            contribuicao=("contribuicao", "sum"),
            peso_medio=("peso", "mean"),
        ).sort_values("contribuicao", ascending=False)
        resumo_contribuicoes["contribuicao"] = resumo_contribuicoes["contribuicao"].map(fmt_pct)
        resumo_contribuicoes["peso_medio"] = resumo_contribuicoes["peso_medio"].map(fmt_pct)
        partes.append(tabela_md(resumo_contribuicoes))
    partes += ["", "### Comparação de turnover e custos por bloco", "", tabela_md(formatar_resumo_periodos(resumo_periodos)[[
        coluna for coluna in ["Período", "Turnover total", "Custo total"]
        if coluna in formatar_resumo_periodos(resumo_periodos).columns
    ]]), ""]

    partes += [
        "---",
        "",
        "## 15. Otimização e walk-forward",
        "",
        "### Métricas finais já produzidas pelo pipeline",
        "",
        tabela_md(metricas_finais, 50),
        "",
        "### Pesos oficiais já produzidos pelo pipeline",
        "",
        tabela_md(pesos_oficiais, 80),
        "",
        "### Scorecard existente",
        "",
        tabela_md(scorecard, 50),
        "",
        "> A recalibração walk-forward é anual, com treino inicial de 48 meses e janela expansiva. "
        "Arquivos anteriores às bases centrais atuais devem ser tratados como resultados de uma execução anterior.",
        "",
        "---",
        "",
        "## 16. Modelo final",
        "",
    ]

    if not artefatos_modelo:
        partes.append("_Nenhum arquivo foi encontrado em `outputs/modelo_final`._")
    else:
        for artefato in artefatos_modelo:
            partes += [
                f"### {artefato['nome']}",
                "",
                f"Caminho: `{artefato['caminho']}`",
                "",
            ]
            if isinstance(artefato["tabela"], pd.DataFrame) and not artefato["tabela"].empty:
                partes += [tabela_md(artefato["tabela"], 80), ""]
            elif artefato["texto"]:
                linguagem = "json" if artefato["extensao"] == ".json" else "text"
                partes += [f"```{linguagem}", artefato["texto"], "```", ""]

    partes += [
        "---",
        "",
        "## 17. Auditoria e controles",
        "",
        tabela_md(auditoria, 80),
        "",
        "---",
        "",
        "## 18. Janelas móveis e estabilidade",
        "",
    ]
    if rolling.empty:
        partes.append("_Não há histórico suficiente ou as séries finais não estão disponíveis._")
    else:
        resumo_rolling: list[dict[str, Any]] = []
        for coluna, nome in [
            ("excesso_vs_benchmark", "Benchmark"),
            ("excesso_vs_cdi", "CDI"),
        ]:
            if coluna in rolling.columns:
                serie = rolling[coluna].dropna()
                if not serie.empty:
                    resumo_rolling.append(
                        {
                            "comparação": nome,
                            "janelas": len(serie),
                            "proporção positiva": fmt_pct((serie > 0).mean()),
                            "melhor excesso": fmt_pct(serie.max()),
                            "pior excesso": fmt_pct(serie.min()),
                        }
                    )
        partes.append(tabela_md(pd.DataFrame(resumo_rolling)))
    partes.append("")

    partes += [
        "---",
        "",
        "## 19. Gráficos oficiais do pipeline",
        "",
        "Os gráficos abaixo foram copiados de `outputs/graficos` para a pasta desta execução. "
        "A situação temporal informa se o arquivo parece pertencer à mesma execução das bases centrais.",
        "",
        tabela_md(inventario_graficos),
        "",
    ]

    if not graficos_pipeline:
        partes.append("_Nenhum gráfico foi encontrado em `outputs/graficos`._")
    else:
        grupos: dict[str, list[Path]] = {}
        for grafico in graficos_pipeline:
            grupos.setdefault(classificar_etapa_grafico(grafico), []).append(grafico)
        for etapa, arquivos in grupos.items():
            partes += [f"### {etapa}", ""]
            for grafico in arquivos:
                partes += [
                    f"#### {grafico.stem}",
                    "",
                    f"![{grafico.stem}]({caminho_md(relatorio, grafico)})",
                    "",
                ]

    partes += [
        "---",
        "",
        "## 20. Gráficos adicionais deste relatório",
        "",
    ]
    for grafico in [*graficos, *graficos_periodos]:
        partes += [
            f"![{grafico.stem}]({caminho_md(relatorio, grafico)})",
            "",
        ]

    partes += [
        "---",
        "",
        "## 21. Tabelas oficiais do pipeline",
        "",
        "Foram selecionadas tabelas relacionadas a métricas, pesos, custos, regimes, "
        "otimização, walk-forward, validação e auditoria.",
        "",
    ]
    if not tabelas_pipeline:
        partes.append("_Nenhuma tabela relevante foi encontrada._")
    else:
        for item in tabelas_pipeline:
            partes += [
                f"### {item['nome']}",
                "",
                f"Caminho: `{item['caminho']}`",
                "",
            ]
            if item["erro"]:
                partes += [f"Erro de leitura: `{item['erro']}`", ""]
            else:
                partes += [tabela_md(item["dados"], 25), ""]

    partes += [
        "---",
        "",
        "## 22. Conclusão técnica",
        "",
    ]
    for linha in conclusoes(ativos, carteira, carteira_regime, rolling):
        partes.append(f"- {linha}")

    verificacao = resumo_periodos.loc[
        resumo_periodos["codigo_periodo"].eq("TESTE_FINAL_FORA_AMOSTRA")
    ]
    if not verificacao.empty:
        linha = verificacao.iloc[0]
        if int(linha["meses_disponiveis"]) < int(linha["meses_esperados"]):
            partes.append(
                "- O teste final de 2026 está parcialmente coberto pela base mensal disponível; "
                "a conclusão final deve ser atualizada quando os meses restantes estiverem disponíveis."
            )

    stale = inventario_saidas.loc[
        inventario_saidas["status_atualizacao"].eq("Verificar atualização")
    ] if not inventario_saidas.empty else pd.DataFrame()
    if not stale.empty:
        partes.append(
            "- Existem saídas do pipeline que parecem anteriores às bases centrais atuais. "
            "Esses resultados foram mantidos para auditoria, mas devem ser regenerados antes da entrega final."
        )

    partes += [
        "- O período de desenvolvimento não deve ser usado sozinho para defender a robustez da estratégia.",
        "- A evidência principal deve vir da validação de 2024–2025 e do teste final de 2026.",
        "- Resultados históricos não garantem desempenho futuro.",
        "- O relatório não constitui recomendação de investimento.",
        "",
    ]

    return "\n".join(partes)


# ============================================================
# EXECUÇÃO
# ============================================================


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera relatório analítico detalhado do projeto.")
    parser.add_argument("--inicio", default=None, help="Data inicial AAAA-MM-DD.")
    parser.add_argument("--fim", default=None, help="Data final AAAA-MM-DD.")
    parser.add_argument("--nome", default=None, help="Nome opcional da execução.")
    parser.add_argument("--sem-graficos", action="store_true")
    return parser.parse_args()


def main() -> None:
    inicio_execucao = datetime.now()
    args = argumentos()
    raiz = raiz_projeto()
    config = caminho_config(raiz)
    carregar_yaml(config)

    data_inicio = pd.to_datetime(args.inicio, errors="raise") if args.inicio else None
    data_fim = pd.to_datetime(args.fim, errors="raise") if args.fim else None
    if data_inicio is not None and data_fim is not None and data_inicio > data_fim:
        raise ValueError("A data inicial não pode ser maior que a data final.")

    identificador = datetime.now().strftime("%Y%m%d_%H%M%S")
    sufixo = "_" + normalizar(args.nome).lower() if args.nome else ""
    saida = raiz / "outputs" / "relatorios" / f"analise_detalhada_{identificador}{sufixo}"
    pasta_tabelas = saida / "tabelas"
    pasta_tabelas.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("09 — RELATÓRIO ANALÍTICO DETALHADO")
    print("=" * 80)
    print(f"Raiz: {raiz}")
    print(f"Configuração: {config}")
    print(f"Saída: {saida}")
    print()

    selecao = ler_csv(resolver(raiz, ARQUIVOS["selecao"]), obrigatorio=True)
    retornos = filtrar_periodo(
        preparar_data(ler_csv(resolver(raiz, ARQUIVOS["retornos"]), obrigatorio=True)),
        data_inicio,
        data_fim,
    )
    macro = filtrar_periodo(
        preparar_data(ler_csv(resolver(raiz, ARQUIVOS["macro"]), obrigatorio=True)),
        data_inicio,
        data_fim,
    )
    regimes = filtrar_periodo(
        preparar_regimes(
            preparar_data(ler_csv(resolver(raiz, ARQUIVOS["regimes"]), obrigatorio=True))
        ),
        data_inicio,
        data_fim,
    )
    alocacao = filtrar_periodo(
        preparar_data(ler_csv(resolver(raiz, ARQUIVOS["alocacao"]), obrigatorio=False)),
        data_inicio,
        data_fim,
    )
    backtest = filtrar_periodo(
        preparar_data(ler_csv(resolver(raiz, ARQUIVOS["backtest"]), obrigatorio=False)),
        data_inicio,
        data_fim,
    )
    series_finais = filtrar_periodo(
        preparar_data(ler_csv(resolver(raiz, ARQUIVOS["series_finais"]), obrigatorio=False)),
        data_inicio,
        data_fim,
    )

    metricas_finais = ler_csv(resolver(raiz, ARQUIVOS["metricas_finais"]), obrigatorio=False)
    pesos_oficiais = ler_csv(resolver(raiz, ARQUIVOS["pesos_oficiais"]), obrigatorio=False)
    scorecard = ler_csv(resolver(raiz, ARQUIVOS["scorecard"]), obrigatorio=False)
    auditoria = ler_csv(resolver(raiz, ARQUIVOS["auditoria"]), obrigatorio=False)

    universo = preparar_universo(selecao)
    mensal = filtrar_periodo(
        retornos_mensais(retornos, universo["ticker"].tolist()),
        data_inicio,
        data_fim,
    )

    carteira_fonte = (
        backtest
        if not backtest.empty
        else series_finais
        if not series_finais.empty
        else alocacao
    )
    base = consolidar_base(mensal, macro, regimes, carteira_fonte)
    if base.empty:
        raise ValueError("A base consolidada ficou vazia.")

    inv = inventario(raiz)
    cob = cobertura(
        {
            "retornos_diarios": retornos,
            "retornos_mensais": mensal,
            "macro": macro,
            "regimes": regimes,
            "alocacao": alocacao,
            "backtest": backtest,
            "series_finais": series_finais,
        }
    )

    ativos = analise_ativos(base, universo)
    ativos_ano = analise_periodica_ativos(base, universo, "ano")
    ativos_semestre = analise_periodica_ativos(base, universo, "semestre")
    ativos_regime = analise_ativos_regime(base, universo)
    segmentos, retornos_segmentos = analise_segmentos(base, universo)
    carteira = analise_carteira(base)
    carteira_ano = analise_periodica_carteira(base, "ano")
    carteira_semestre = analise_periodica_carteira(base, "semestre")
    carteira_regime = analise_carteira_regime(base)
    episodios = episodios_regime(base, universo)
    rolling = analise_rolling(base)
    melhores, piores = meses_extremos(base)
    transicoes = transicoes_regime(base)
    transicoes_resumo = resumo_transicoes(transicoes)
    contribuicoes_df = contribuicoes(base, universo)

    resumo_periodos = resumo_periodos_oficiais(base)
    analises_periodos = analises_detalhadas_periodos(base, universo)
    inventario_saidas = inventariar_saidas_pipeline(raiz)
    artefatos_modelo = carregar_artefatos_modelo_final(raiz)
    tabelas_pipeline = carregar_tabelas_pipeline(raiz)

    tabelas = {
        "00_inventario.csv": inv,
        "01_cobertura.csv": cob,
        "02_universo.csv": universo,
        "03_base_mensal_consolidada.csv": base,
        "04_metricas_ativos.csv": ativos,
        "05_metricas_segmentos.csv": segmentos,
        "06_retornos_segmentos.csv": retornos_segmentos,
        "07_ativos_por_ano.csv": ativos_ano,
        "08_ativos_por_semestre.csv": ativos_semestre,
        "09_ativos_por_regime.csv": ativos_regime,
        "10_metricas_carteira.csv": carteira,
        "11_carteira_por_ano.csv": carteira_ano,
        "12_carteira_por_semestre.csv": carteira_semestre,
        "13_carteira_por_regime.csv": carteira_regime,
        "14_episodios_regimes.csv": episodios,
        "15_rolling_12m.csv": rolling,
        "16_melhores_meses.csv": melhores,
        "17_piores_meses.csv": piores,
        "18_transicoes_detalhadas.csv": transicoes,
        "19_transicoes_resumo.csv": transicoes_resumo,
        "20_contribuicoes_ativos.csv": contribuicoes_df,
        "21_comparacao_periodos_oficiais.csv": resumo_periodos,
        "22_inventario_saidas_pipeline.csv": inventario_saidas,
    }

    for periodo in PERIODOS_OFICIAIS:
        codigo_periodo = periodo["codigo"].lower()
        detalhe = analises_periodos[periodo["codigo"]]
        tabelas[f"periodo_{codigo_periodo}_carteira.csv"] = detalhe["carteira"]
        tabelas[f"periodo_{codigo_periodo}_ativos.csv"] = detalhe["ativos"]
        tabelas[f"periodo_{codigo_periodo}_segmentos.csv"] = detalhe["segmentos"]
        tabelas[f"periodo_{codigo_periodo}_regimes.csv"] = detalhe["regimes"]
        tabelas[f"periodo_{codigo_periodo}_episodios.csv"] = detalhe["episodios"]
        tabelas[f"periodo_{codigo_periodo}_contribuicoes.csv"] = detalhe["contribuicoes"]

    caminhos_tabelas: list[Path] = []
    for nome, dados in tabelas.items():
        caminho = pasta_tabelas / nome
        salvar_csv(dados, caminho)
        caminhos_tabelas.append(caminho)

    graficos = [] if args.sem_graficos else gerar_graficos(saida, base, universo, rolling)
    graficos_periodos = (
        []
        if args.sem_graficos
        else gerar_graficos_periodos_oficiais(saida, analises_periodos)
    )
    graficos_pipeline, inventario_graficos = copiar_graficos_pipeline(raiz, saida)
    if not inventario_graficos.empty:
        salvar_csv(inventario_graficos, pasta_tabelas / "23_inventario_graficos_pipeline.csv")

    caminho_relatorio = saida / "relatorio_analitico_detalhado.md"
    texto = construir_relatorio(
        relatorio=caminho_relatorio,
        base=base,
        universo=universo,
        inventario_df=inv,
        cobertura_df=cob,
        ativos=ativos,
        segmentos=segmentos,
        ativos_ano=ativos_ano,
        ativos_semestre=ativos_semestre,
        ativos_regime=ativos_regime,
        carteira=carteira,
        carteira_ano=carteira_ano,
        carteira_semestre=carteira_semestre,
        carteira_regime=carteira_regime,
        episodios=episodios,
        rolling=rolling,
        melhores=melhores,
        piores=piores,
        transicoes_resumo=transicoes_resumo,
        contribuicoes_df=contribuicoes_df,
        metricas_finais=metricas_finais,
        pesos_oficiais=pesos_oficiais,
        scorecard=scorecard,
        auditoria=auditoria,
        graficos=graficos,
        resumo_periodos=resumo_periodos,
        analises_periodos=analises_periodos,
        graficos_periodos=graficos_periodos,
        graficos_pipeline=graficos_pipeline,
        inventario_graficos=inventario_graficos,
        inventario_saidas=inventario_saidas,
        artefatos_modelo=artefatos_modelo,
        tabelas_pipeline=tabelas_pipeline,
    )
    caminho_relatorio.write_text(texto, encoding="utf-8")

    manifesto = {
        "versao": VERSAO,
        "gerado_em_utc": datetime.now(timezone.utc).isoformat(),
        "periodo_disponivel_inicial": base["data"].min().isoformat(),
        "periodo_disponivel_final": base["data"].max().isoformat(),
        "periodos_oficiais": [
            {
                "codigo": periodo["codigo"],
                "nome": periodo["nome"],
                "inicio": periodo["inicio"].date().isoformat(),
                "fim": periodo["fim"].date().isoformat(),
                "ajusta_parametros": periodo["ajusta_parametros"],
                "altera_regras": periodo["altera_regras"],
            }
            for periodo in PERIODOS_OFICIAIS
        ],
        "ativos": len(universo),
        "meses": len(base),
        "episodios_regime": len(episodios),
        "transicoes": int(transicoes["transicao"].nunique()) if not transicoes.empty else 0,
        "tabelas_geradas": [str(c.relative_to(raiz)) for c in caminhos_tabelas],
        "graficos_gerados_relatorio": [
            str(c.relative_to(raiz)) for c in [*graficos, *graficos_periodos]
        ],
        "graficos_pipeline_copiados": [
            str(c.relative_to(raiz)) for c in graficos_pipeline
        ],
        "artefatos_modelo_final": len(artefatos_modelo),
        "tabelas_pipeline_incorporadas": len(tabelas_pipeline),
        "relatorio": str(caminho_relatorio.relative_to(raiz)),
    }
    caminho_manifesto = saida / "manifesto.json"
    caminho_manifesto.write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    duracao = (datetime.now() - inicio_execucao).total_seconds()
    print("=" * 80)
    print("RELATÓRIO CONCLUÍDO")
    print("=" * 80)
    print(f"Período disponível: {fmt_data(base['data'].min())} a {fmt_data(base['data'].max())}")
    print(f"Ativos: {len(universo)}")
    print(f"Meses: {len(base)}")
    print(f"Episódios: {len(episodios)}")
    print(f"Tabelas geradas: {len(caminhos_tabelas)}")
    print(f"Gráficos novos: {len(graficos) + len(graficos_periodos)}")
    print(f"Gráficos do pipeline copiados: {len(graficos_pipeline)}")
    print(f"Arquivos do modelo final incorporados: {len(artefatos_modelo)}")
    print(f"Tabelas do pipeline incorporadas: {len(tabelas_pipeline)}")
    print(f"Relatório Markdown: {caminho_relatorio}")
    print(f"Duração: {duracao:.2f}s")


if __name__ == "__main__":
    try:
        main()
    except Exception as erro:
        print()
        print(f"ERRO: {erro}")
        sys.exit(1)
