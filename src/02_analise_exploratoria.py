from __future__ import annotations

# VERSAO_V4_SELECAO_FINAL_E_GRAFICOS_SEGMENTADOS

import os
import sys
import time
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from matplotlib.ticker import PercentFormatter


# ============================================================
# CAMINHOS PRINCIPAIS
# ============================================================

CAMINHO_SCRIPT = Path(__file__).resolve()
RAIZ_PADRAO = (
    CAMINHO_SCRIPT.parent.parent
    if CAMINHO_SCRIPT.parent.name.lower() == "src"
    else CAMINHO_SCRIPT.parent
)

RAIZ_PROJETO = Path(
    os.getenv(
        "PROJECT_ROOT",
        RAIZ_PADRAO,
    )
).resolve()

ARQUIVO_CONFIG = Path(
    os.getenv(
        "PROJECT_CONFIG",
        RAIZ_PROJETO / "config" / "config.yaml",
    )
).resolve()


# ============================================================
# CONSTANTES
# ============================================================

COLUNAS_PRECOS = [
    "data",
    "ticker",
    "classe",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
]

COLUNAS_MACRO = [
    "data",
    "codigo_sgs",
    "serie",
    "valor",
]

DIAS_UTEIS_ANO = 252
VALOR_INICIAL = 1.0
BASE_NORMALIZACAO = 100.0
JANELA_VOLATILIDADE = 63
JANELA_IPCA_12M = 12
DEFASAGEM_IPCA_MESES = 3
JANELA_IBC_BR_12M = 12
JANELA_MEDIA_MOVEL_IBC_BR = 3
DEFASAGEM_TENDENCIA_IBC_BR = 3

COLUNAS_SELECAO_OBRIGATORIAS = [
    "ticker",
    "classe",
]

STATUS_SELECAO_PERMITIDOS = {
    "APROVADO",
    "APROVADO_COM_RESSALVAS",
}

ORDEM_SEGMENTOS = [
    "commodities",
    "renda_variavel",
    "moedas",
    "renda_fixa",
]

TITULOS_SEGMENTOS = {
    "commodities": "Commodities",
    "renda_variavel": "Renda Variável",
    "moedas": "Moedas",
    "renda_fixa": "Renda Fixa",
}


# ============================================================
# CONFIGURAÇÃO E ARQUIVOS
# ============================================================

def carregar_configuracao() -> dict[str, Any]:
    """Carrega o config.yaml do projeto."""

    if not ARQUIVO_CONFIG.is_file():
        raise FileNotFoundError(
            f"Arquivo de configuração não encontrado: {ARQUIVO_CONFIG}"
        )

    with ARQUIVO_CONFIG.open("r", encoding="utf-8") as arquivo:
        configuracao = yaml.safe_load(arquivo) or {}

    if not isinstance(configuracao, dict):
        raise TypeError("O config.yaml deve possuir um dicionário na raiz.")

    return configuracao


def obter_valor(
    configuracao: dict[str, Any],
    caminho: tuple[str, ...],
    obrigatorio: bool = True,
    padrao: Any = None,
) -> Any:
    """Obtém um valor aninhado do config.yaml."""

    valor: Any = configuracao

    for chave in caminho:
        if not isinstance(valor, dict) or chave not in valor:
            if obrigatorio:
                raise KeyError(
                    "Parâmetro obrigatório ausente: "
                    + ".".join(caminho)
                )
            return padrao

        valor = valor[chave]

    return valor


def resolver_caminho(caminho: str | Path) -> Path:
    """Resolve caminhos relativos a partir da raiz do projeto."""

    caminho_resolvido = Path(caminho)

    if not caminho_resolvido.is_absolute():
        caminho_resolvido = RAIZ_PROJETO / caminho_resolvido

    return caminho_resolvido.resolve()


def criar_diretorios(
    configuracao: dict[str, Any],
) -> dict[str, Path]:
    """Cria e retorna os diretórios usados pela etapa."""

    diretorios = {
        "processed": resolver_caminho(
            obter_valor(
                configuracao,
                ("caminhos", "dados_processados"),
                obrigatorio=False,
                padrao="data/processed",
            )
        ),
        "macro": resolver_caminho(
            obter_valor(
                configuracao,
                ("caminhos", "macro_bruto"),
                obrigatorio=False,
                padrao="data/raw/macro",
            )
        ),
        "tabelas": resolver_caminho(
            obter_valor(
                configuracao,
                ("caminhos", "tabelas"),
                obrigatorio=False,
                padrao="outputs/tabelas",
            )
        ),
        "graficos": resolver_caminho(
            obter_valor(
                configuracao,
                ("caminhos", "graficos"),
                obrigatorio=False,
                padrao="outputs/graficos",
            )
        ),
    }

    for diretorio in diretorios.values():
        diretorio.mkdir(parents=True, exist_ok=True)

    return diretorios


def salvar_csv(
    tabela: pd.DataFrame,
    caminho: Path,
    incluir_indice: bool = False,
) -> None:
    """Salva um CSV e confere sua integridade básica."""

    caminho.parent.mkdir(parents=True, exist_ok=True)

    tabela.to_csv(
        caminho,
        index=incluir_indice,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )

    if not caminho.is_file() or caminho.stat().st_size == 0:
        raise FileNotFoundError(
            f"O arquivo não foi salvo corretamente: {caminho}"
        )

    validacao = pd.read_csv(
        caminho,
        encoding="utf-8-sig",
        low_memory=False,
    )

    if len(validacao) != len(tabela):
        raise ValueError(
            "O arquivo salvo possui quantidade de linhas diferente "
            f"do DataFrame original: {caminho}"
        )


def salvar_temporal(
    tabela: pd.DataFrame,
    caminho: Path,
) -> None:
    """Salva uma tabela temporal com a data como primeira coluna."""

    tabela_salvar = tabela.copy()

    if isinstance(tabela_salvar.index, pd.DatetimeIndex):
        tabela_salvar.index.name = "data"
        tabela_salvar = tabela_salvar.reset_index()

    salvar_csv(
        tabela=tabela_salvar,
        caminho=caminho,
        incluir_indice=False,
    )



def converter_booleano(valor: Any) -> bool:
    """Converte valores usuais de CSV para booleano."""

    if isinstance(valor, bool):
        return valor

    if pd.isna(valor):
        return False

    normalizado = str(valor).strip().upper()

    return normalizado in {
        "TRUE",
        "1",
        "SIM",
        "YES",
        "Y",
    }


def identificar_segmento(classe: str) -> str:
    """Converte a classe detalhada no segmento principal."""

    classe_normalizada = str(classe).strip().upper()

    if classe_normalizada.startswith("COMMODITY"):
        return "commodities"

    if classe_normalizada.startswith("RENDA_VARIAVEL"):
        return "renda_variavel"

    if classe_normalizada.startswith("MOEDA"):
        return "moedas"

    if classe_normalizada.startswith("RENDA_FIXA"):
        return "renda_fixa"

    raise ValueError(
        "Não foi possível identificar o segmento da classe: "
        f"{classe}"
    )


def carregar_ativos_selecionados(
    configuracao: dict[str, Any],
) -> tuple[pd.DataFrame, Path]:
    """Carrega e valida o arquivo oficial de ativos selecionados."""

    caminho_configurado = obter_valor(
        configuracao,
        (
            "selecao_ativos",
            "arquivo_selecao_final",
        ),
        obrigatorio=False,
        padrao=(
            "data/processed/"
            "ativos_selecionados_modelo.csv"
        ),
    )

    if caminho_configurado in {
        None,
        "",
    }:
        raise ValueError(
            "selecao_ativos.arquivo_selecao_final "
            "não foi definido no config.yaml."
        )

    caminho = resolver_caminho(caminho_configurado)

    if not caminho.is_file():
        raise FileNotFoundError(
            "O arquivo de ativos selecionados não foi encontrado.\n"
            f"Arquivo esperado: {caminho}"
        )

    try:
        dados = pd.read_csv(
            caminho,
            encoding="utf-8-sig",
            sep=None,
            engine="python",
        )
    except UnicodeDecodeError:
        dados = pd.read_csv(
            caminho,
            encoding="latin1",
            sep=None,
            engine="python",
        )

    dados.columns = [
        str(coluna).strip().lower()
        for coluna in dados.columns
    ]

    ausentes = [
        coluna
        for coluna in COLUNAS_SELECAO_OBRIGATORIAS
        if coluna not in dados.columns
    ]

    if ausentes:
        raise ValueError(
            "Colunas ausentes em ativos_selecionados_modelo.csv: "
            f"{ausentes}"
        )

    dados["ticker"] = (
        dados["ticker"]
        .astype("string")
        .str.strip()
        .str.upper()
    )
    dados["classe"] = (
        dados["classe"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    dados = dados.dropna(
        subset=[
            "ticker",
            "classe",
        ]
    ).copy()

    if dados.empty:
        raise ValueError(
            "O arquivo de ativos selecionados está vazio."
        )

    if dados["ticker"].duplicated().any():
        duplicados = (
            dados.loc[
                dados["ticker"].duplicated(
                    keep=False
                ),
                "ticker",
            ]
            .drop_duplicates()
            .tolist()
        )
        raise ValueError(
            "Existem tickers duplicados no arquivo de seleção: "
            f"{duplicados}"
        )

    if "aprovado" in dados.columns:
        aprovados = dados["aprovado"].map(
            converter_booleano
        )

        if not aprovados.all():
            invalidos = dados.loc[
                ~aprovados,
                "ticker",
            ].tolist()
            raise ValueError(
                "O arquivo de seleção contém ativos não aprovados: "
                f"{invalidos}"
            )

        dados["aprovado"] = aprovados

    if "status" in dados.columns:
        dados["status"] = (
            dados["status"]
            .astype("string")
            .str.strip()
            .str.upper()
        )

        status_invalidos = sorted(
            set(dados["status"].dropna())
            - STATUS_SELECAO_PERMITIDOS
        )

        if status_invalidos:
            raise ValueError(
                "O arquivo de seleção possui status não permitidos: "
                f"{status_invalidos}"
            )

    dados["segmento"] = dados["classe"].map(
        identificar_segmento
    )

    segmentos_ausentes = [
        segmento
        for segmento in ORDEM_SEGMENTOS
        if segmento not in set(dados["segmento"])
    ]

    if segmentos_ausentes:
        raise ValueError(
            "O arquivo de seleção não possui ativos nos segmentos: "
            f"{segmentos_ausentes}"
        )

    ordem = {
        segmento: indice
        for indice, segmento in enumerate(
            ORDEM_SEGMENTOS
        )
    }

    dados["_ordem_segmento"] = dados["segmento"].map(
        ordem
    )

    dados = (
        dados.sort_values(
            [
                "_ordem_segmento",
                "ticker",
            ]
        )
        .drop(columns="_ordem_segmento")
        .reset_index(drop=True)
    )

    return dados, caminho


def criar_mapa_segmentos(
    ativos_selecionados: pd.DataFrame,
) -> dict[str, list[str]]:
    """Organiza os tickers selecionados por segmento."""

    segmentos: dict[str, list[str]] = {}

    for segmento in ORDEM_SEGMENTOS:
        tickers = (
            ativos_selecionados.loc[
                ativos_selecionados["segmento"].eq(
                    segmento
                ),
                "ticker",
            ]
            .tolist()
        )

        if tickers:
            segmentos[segmento] = tickers

    return segmentos


def filtrar_precos_selecionados(
    precos_aprovados: pd.DataFrame,
    ativos_selecionados: pd.DataFrame,
) -> pd.DataFrame:
    """Mantém somente os ativos definidos na seleção final."""

    tickers_selecionados = (
        ativos_selecionados["ticker"]
        .astype(str)
        .str.strip()
        .str.upper()
        .tolist()
    )

    tickers_disponiveis = set(
        precos_aprovados["ticker"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    ausentes = [
        ticker
        for ticker in tickers_selecionados
        if ticker not in tickers_disponiveis
    ]

    if ausentes:
        raise ValueError(
            "Ativos selecionados sem preços na base aprovada: "
            f"{ausentes}"
        )

    classes_precos = (
        precos_aprovados[
            [
                "ticker",
                "classe",
            ]
        ]
        .drop_duplicates()
        .assign(
            ticker=lambda tabela: (
                tabela["ticker"]
                .astype(str)
                .str.strip()
                .str.upper()
            ),
            classe=lambda tabela: (
                tabela["classe"]
                .astype(str)
                .str.strip()
                .str.upper()
            ),
        )
    )

    validacao_classes = ativos_selecionados[
        [
            "ticker",
            "classe",
        ]
    ].merge(
        classes_precos,
        on="ticker",
        how="left",
        suffixes=(
            "_selecao",
            "_precos",
        ),
    )

    divergencias = validacao_classes.loc[
        validacao_classes["classe_selecao"].ne(
            validacao_classes["classe_precos"]
        )
    ]

    if not divergencias.empty:
        raise ValueError(
            "Existem divergências de classe entre a seleção e "
            "a base de preços:\n"
            + divergencias.to_string(index=False)
        )

    filtrados = (
        precos_aprovados.loc[
            precos_aprovados["ticker"].isin(
                tickers_selecionados
            )
        ]
        .copy()
        .sort_values(
            [
                "ticker",
                "data",
            ]
        )
        .reset_index(drop=True)
    )

    encontrados = set(
        filtrados["ticker"].unique().tolist()
    )

    if encontrados != set(tickers_selecionados):
        raise RuntimeError(
            "A filtragem não preservou exatamente os ativos "
            "selecionados."
        )

    return filtrados


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

def carregar_precos(
    configuracao: dict[str, Any],
) -> tuple[pd.DataFrame, Path]:
    """Carrega os preços já aprovados na etapa de seleção técnica."""

    caminho = resolver_caminho(
        obter_valor(
            configuracao,
            (
                "coleta_yfinance",
                "saidas",
                "precos_utilizaveis",
            ),
        )
    )

    if not caminho.is_file():
        raise FileNotFoundError(
            "O arquivo de preços utilizáveis não foi encontrado.\n"
            "Execute primeiro coletar_ativo_yfinance.py.\n"
            f"Arquivo esperado: {caminho}"
        )

    dados = pd.read_csv(
        caminho,
        encoding="utf-8-sig",
        low_memory=False,
    )

    ausentes = [
        coluna
        for coluna in COLUNAS_PRECOS
        if coluna not in dados.columns
    ]

    if ausentes:
        raise ValueError(
            f"Colunas ausentes na base de preços: {ausentes}"
        )

    dados = dados[COLUNAS_PRECOS].copy()

    dados["data"] = pd.to_datetime(
        dados["data"],
        errors="coerce",
    )

    for coluna in [
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]:
        dados[coluna] = pd.to_numeric(
            dados[coluna],
            errors="coerce",
        )

    dados["ticker"] = (
        dados["ticker"]
        .astype("string")
        .str.strip()
    )
    dados["classe"] = (
        dados["classe"]
        .astype("string")
        .str.strip()
    )

    if dados["data"].isna().any():
        raise ValueError("A base de preços possui datas inválidas.")

    if dados[["ticker", "data"]].duplicated().any():
        raise ValueError(
            "A base de preços possui duplicidades de ticker e data."
        )

    dados = (
        dados.sort_values(
            [
                "ticker",
                "data",
            ]
        )
        .reset_index(drop=True)
    )

    if dados.empty:
        raise ValueError("A base de preços está vazia.")

    return dados, caminho


def carregar_macro(
    diretorio_macro: Path,
) -> tuple[pd.DataFrame, Path]:
    """Carrega o consolidado macroeconômico produzido pela etapa 01."""

    candidatos = [
        diretorio_macro / "series_macroeconomicas.csv",
        diretorio_macro / "01_05_series_macroeconomicas.csv",
    ]

    caminho = next(
        (
            candidato
            for candidato in candidatos
            if candidato.is_file()
        ),
        None,
    )

    if caminho is None:
        raise FileNotFoundError(
            "O consolidado macroeconômico não foi encontrado.\n"
            "Execute primeiro 01_coleta_dados.py.\n"
            + "\n".join(str(item) for item in candidatos)
        )

    dados = pd.read_csv(
        caminho,
        encoding="utf-8-sig",
        low_memory=False,
    )

    ausentes = [
        coluna
        for coluna in COLUNAS_MACRO
        if coluna not in dados.columns
    ]

    if ausentes:
        raise ValueError(
            f"Colunas ausentes na base macroeconômica: {ausentes}"
        )

    dados = dados[COLUNAS_MACRO].copy()
    dados["data"] = pd.to_datetime(
        dados["data"],
        errors="coerce",
    )
    dados["codigo_sgs"] = pd.to_numeric(
        dados["codigo_sgs"],
        errors="coerce",
    )
    dados["valor"] = pd.to_numeric(
        dados["valor"],
        errors="coerce",
    )
    dados["serie"] = (
        dados["serie"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    if dados["data"].isna().any():
        raise ValueError(
            "A base macroeconômica possui datas inválidas."
        )

    if dados["codigo_sgs"].isna().any():
        raise ValueError(
            "A base macroeconômica possui códigos SGS inválidos."
        )

    if dados["valor"].isna().any():
        raise ValueError(
            "A base macroeconômica possui valores inválidos."
        )

    dados["codigo_sgs"] = dados["codigo_sgs"].astype(int)

    if dados[["codigo_sgs", "data"]].duplicated().any():
        raise ValueError(
            "A base macroeconômica possui duplicidades de código e data."
        )

    dados = (
        dados.sort_values(
            [
                "codigo_sgs",
                "data",
            ]
        )
        .reset_index(drop=True)
    )

    if dados.empty:
        raise ValueError("A base macroeconômica está vazia.")

    return dados, caminho


def mapa_indicadores(
    configuracao: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Obtém os indicadores macroeconômicos ativos do config.yaml."""

    indicadores = obter_valor(
        configuracao,
        (
            "coleta_macro",
            "indicadores_principais",
        ),
    )

    if not isinstance(indicadores, dict):
        raise TypeError(
            "coleta_macro.indicadores_principais deve ser um dicionário."
        )

    resultado: dict[str, dict[str, Any]] = {}

    for chave, dados in indicadores.items():
        if not isinstance(dados, dict):
            continue

        if not bool(dados.get("ativo", True)):
            continue

        codigo = dados.get("codigo_sgs")
        nome = dados.get("nome_modelo")

        if codigo is None or nome is None:
            continue

        resultado[str(chave)] = {
            "codigo_sgs": int(codigo),
            "nome_modelo": str(nome).strip().upper(),
            "frequencia": str(
                dados.get(
                    "frequencia_origem",
                    "desconhecida",
                )
            ).strip().lower(),
        }

    return resultado


def separar_series_macro(
    dados_macro: pd.DataFrame,
    configuracao: dict[str, Any],
) -> dict[str, pd.DataFrame]:
    """
    Separa CDI, IPCA, IBC-Br e IBC-Br dessazonalizado.

    Quando a configuração possui somente o IBC-Br dessazonalizado,
    a mesma série é utilizada como indicador de atividade geral.
    """

    indicadores = mapa_indicadores(configuracao)

    codigos_padrao = {
        "cdi": 12,
        "ipca": 433,
        "ibc_br": 24363,
        "ibc_br_dessazonalizado": 24364,
    }

    codigos_disponiveis = set(
        dados_macro["codigo_sgs"].unique().tolist()
    )

    def localizar_codigo(
        chave: str,
        padrao: int,
    ) -> int | None:
        if chave in indicadores:
            codigo = int(indicadores[chave]["codigo_sgs"])
            if codigo in codigos_disponiveis:
                return codigo

        if padrao in codigos_disponiveis:
            return padrao

        return None

    codigo_cdi = localizar_codigo("cdi", codigos_padrao["cdi"])
    codigo_ipca = localizar_codigo("ipca", codigos_padrao["ipca"])
    codigo_ibc = localizar_codigo(
        "ibc_br",
        codigos_padrao["ibc_br"],
    )
    codigo_ibc_dessaz = localizar_codigo(
        "ibc_br_dessazonalizado",
        codigos_padrao["ibc_br_dessazonalizado"],
    )

    if codigo_ibc_dessaz is None:
        candidatos_dessaz = [
            int(dados["codigo_sgs"])
            for chave, dados in indicadores.items()
            if bool(
                obter_valor(
                    configuracao,
                    (
                        "coleta_macro",
                        "indicadores_principais",
                        chave,
                        "dessazonalizado",
                    ),
                    obrigatorio=False,
                    padrao=False,
                )
            )
            and int(dados["codigo_sgs"]) in codigos_disponiveis
        ]

        if candidatos_dessaz:
            codigo_ibc_dessaz = candidatos_dessaz[0]

    if codigo_ibc is None and codigo_ibc_dessaz is not None:
        codigo_ibc = codigo_ibc_dessaz

    if codigo_ibc_dessaz is None and codigo_ibc is not None:
        codigo_ibc_dessaz = codigo_ibc

    codigos_obrigatorios = {
        "CDI": codigo_cdi,
        "IPCA": codigo_ipca,
        "IBC_BR": codigo_ibc,
        "IBC_BR_DESSAZONALIZADO": codigo_ibc_dessaz,
    }

    ausentes = [
        nome
        for nome, codigo in codigos_obrigatorios.items()
        if codigo is None
    ]

    if ausentes:
        raise ValueError(
            "Séries macroeconômicas obrigatórias ausentes: "
            f"{ausentes}. Códigos disponíveis: "
            f"{sorted(codigos_disponiveis)}"
        )

    resultado: dict[str, pd.DataFrame] = {}

    for nome, codigo in codigos_obrigatorios.items():
        serie = (
            dados_macro.loc[
                dados_macro["codigo_sgs"].eq(int(codigo)),
                COLUNAS_MACRO,
            ]
            .copy()
            .sort_values("data")
            .reset_index(drop=True)
        )

        if serie.empty:
            raise ValueError(
                f"A série {nome} — SGS {codigo} está vazia."
            )

        resultado[nome] = serie

    return resultado


# ============================================================
# QUALIDADE DOS DADOS
# ============================================================

def contar_dias_sem_registro(datas: pd.Series) -> int:
    """Estima lacunas de segunda a sexta em uma série diária."""

    datas_validas = pd.to_datetime(
        datas,
        errors="coerce",
    ).dropna()

    if datas_validas.empty:
        return 0

    esperados = pd.bdate_range(
        start=datas_validas.min(),
        end=datas_validas.max(),
    )
    observados = pd.DatetimeIndex(
        datas_validas.dt.normalize().unique()
    )

    return int(len(esperados.difference(observados)))


def contar_meses_sem_registro(datas: pd.Series) -> int:
    """Conta competências mensais ausentes."""

    datas_validas = pd.to_datetime(
        datas,
        errors="coerce",
    ).dropna()

    if datas_validas.empty:
        return 0

    observados = pd.PeriodIndex(
        datas_validas.dt.to_period("M").unique()
    )
    esperados = pd.period_range(
        start=datas_validas.min().to_period("M"),
        end=datas_validas.max().to_period("M"),
        freq="M",
    )

    return int(len(esperados.difference(observados)))


def analisar_qualidade(
    precos: pd.DataFrame,
    dados_macro: pd.DataFrame,
    configuracao: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Analisa qualidade das séries de mercado e macroeconomia."""

    qualidade_config = obter_valor(
        configuracao,
        ("qualidade_dados",),
        obrigatorio=False,
        padrao={},
    )

    limite_alerta = float(
        qualidade_config.get(
            "limite_percentual_nulos_alerta",
            0.05,
        )
    )
    limite_critico = float(
        qualidade_config.get(
            "limite_percentual_nulos_critico",
            0.20,
        )
    )

    precos = precos.copy()
    precos["preco_referencia"] = (
        precos["adj_close"]
        .combine_first(precos["close"])
    )

    registros_ativos: list[dict[str, Any]] = []

    for (ticker, classe), grupo in precos.groupby(
        [
            "ticker",
            "classe",
        ],
        sort=True,
    ):
        grupo = grupo.sort_values("data").copy()
        total = len(grupo)
        duplicidades = int(
            grupo.duplicated(subset=["data"]).sum()
        )
        nulos = int(grupo["preco_referencia"].isna().sum())
        percentual_nulos = (
            nulos / total
            if total
            else 1.0
        )
        nao_positivos = int(
            grupo["preco_referencia"]
            .le(0)
            .fillna(False)
            .sum()
        )
        lacunas = contar_dias_sem_registro(
            grupo["data"]
        )

        if (
            duplicidades > 0
            or nao_positivos > 0
            or percentual_nulos > limite_critico
        ):
            status = "ERRO"
        elif percentual_nulos > limite_alerta or lacunas > 0:
            status = "ATENCAO"
        else:
            status = "OK"

        registros_ativos.append(
            {
                "ticker": ticker,
                "classe": classe,
                "status": status,
                "data_inicial": grupo["data"].min(),
                "data_final": grupo["data"].max(),
                "registros": total,
                "duplicidades": duplicidades,
                "precos_nulos": nulos,
                "percentual_nulos": percentual_nulos,
                "precos_nao_positivos": nao_positivos,
                "lacunas_dias_uteis_estimadas": lacunas,
            }
        )

    qualidade_ativos = pd.DataFrame(registros_ativos)

    registros_macro: list[dict[str, Any]] = []

    for codigo, grupo in dados_macro.groupby(
        "codigo_sgs",
        sort=True,
    ):
        grupo = grupo.sort_values("data").copy()
        total = len(grupo)
        duplicidades = int(
            grupo.duplicated(subset=["data"]).sum()
        )
        nulos = int(grupo["valor"].isna().sum())
        infinitos = int(
            np.isinf(
                grupo["valor"]
                .dropna()
                .to_numpy(dtype=float)
            ).sum()
        )

        intervalo_mediano = (
            grupo["data"]
            .sort_values()
            .diff()
            .dt.days
            .dropna()
            .median()
        )

        if pd.isna(intervalo_mediano):
            intervalo_mediano = 0.0

        if float(intervalo_mediano) <= 3:
            lacunas = contar_dias_sem_registro(
                grupo["data"]
            )
            frequencia_estimativa = "DIARIA"
        else:
            lacunas = contar_meses_sem_registro(
                grupo["data"]
            )
            frequencia_estimativa = "MENSAL"

        status = (
            "ERRO"
            if duplicidades > 0 or nulos > 0 or infinitos > 0
            else "ATENCAO"
            if lacunas > 0
            else "OK"
        )

        registros_macro.append(
            {
                "codigo_sgs": int(codigo),
                "serie": str(grupo["serie"].iloc[0]),
                "status": status,
                "frequencia_estimada": frequencia_estimativa,
                "data_inicial": grupo["data"].min(),
                "data_final": grupo["data"].max(),
                "registros": total,
                "duplicidades": duplicidades,
                "valores_nulos": nulos,
                "valores_infinitos": infinitos,
                "lacunas_estimadas": lacunas,
            }
        )

    qualidade_macro = pd.DataFrame(registros_macro)

    problemas_ativos = (
        qualidade_ativos.loc[
            qualidade_ativos["status"].ne("OK")
        ]
        .assign(tipo="ATIVO")
        .rename(columns={"ticker": "identificador"})
    )

    problemas_macro = (
        qualidade_macro.loc[
            qualidade_macro["status"].ne("OK")
        ]
        .assign(tipo="SERIE_MACRO")
        .rename(columns={"serie": "identificador"})
    )

    problemas = pd.concat(
        [
            problemas_ativos[
                [
                    "tipo",
                    "identificador",
                    "status",
                ]
            ],
            problemas_macro[
                [
                    "tipo",
                    "identificador",
                    "status",
                ]
            ],
        ],
        ignore_index=True,
    )

    ativos_erro = int(
        qualidade_ativos["status"].eq("ERRO").sum()
    )
    macro_erro = int(
        qualidade_macro["status"].eq("ERRO").sum()
    )
    ativos_atencao = int(
        qualidade_ativos["status"].eq("ATENCAO").sum()
    )
    macro_atencao = int(
        qualidade_macro["status"].eq("ATENCAO").sum()
    )

    if ativos_erro or macro_erro:
        status_final = "ERROS_ESTRUTURAIS"
    elif ativos_atencao or macro_atencao:
        status_final = "APROVADO_COM_ATENCAO"
    else:
        status_final = "APROVADO"

    resumo = pd.DataFrame(
        [
            {
                "status_final": status_final,
                "ativos_analisados": len(qualidade_ativos),
                "ativos_ok": int(
                    qualidade_ativos["status"].eq("OK").sum()
                ),
                "ativos_atencao": ativos_atencao,
                "ativos_erro": ativos_erro,
                "series_macro_analisadas": len(qualidade_macro),
                "series_macro_ok": int(
                    qualidade_macro["status"].eq("OK").sum()
                ),
                "series_macro_atencao": macro_atencao,
                "series_macro_erro": macro_erro,
                "data_analise_utc": datetime.now(
                    timezone.utc
                ).isoformat(),
            }
        ]
    )

    return qualidade_ativos, qualidade_macro, problemas, resumo


# ============================================================
# TRATAMENTO DOS PREÇOS
# ============================================================

def alinhar_precos(
    precos: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Converte preços para formato largo e mantém período comum."""

    dados = precos.copy()
    dados["preco_referencia"] = (
        dados["adj_close"]
        .combine_first(dados["close"])
    )

    dados = (
        dados.dropna(
            subset=[
                "data",
                "ticker",
                "preco_referencia",
            ]
        )
        .loc[
            lambda tabela: tabela["preco_referencia"].gt(0)
        ]
        .drop_duplicates(
            subset=[
                "ticker",
                "data",
            ],
            keep="last",
        )
        .sort_values(
            [
                "ticker",
                "data",
            ]
        )
    )

    if dados.empty:
        raise ValueError(
            "A base de preços ficou vazia após o tratamento."
        )

    pivot = (
        dados.pivot(
            index="data",
            columns="ticker",
            values="preco_referencia",
        )
        .sort_index()
    )

    pivot.columns.name = None
    pivot.index.name = "data"

    periodos = pd.DataFrame(
        {
            "ticker": pivot.columns,
            "data_inicial": [
                pivot[coluna].first_valid_index()
                for coluna in pivot.columns
            ],
            "data_final": [
                pivot[coluna].last_valid_index()
                for coluna in pivot.columns
            ],
            "quantidade_observacoes": [
                int(pivot[coluna].notna().sum())
                for coluna in pivot.columns
            ],
            "quantidade_ausencias": [
                int(pivot[coluna].isna().sum())
                for coluna in pivot.columns
            ],
        }
    )

    if periodos[
        [
            "data_inicial",
            "data_final",
        ]
    ].isna().any().any():
        raise ValueError(
            "Um ou mais ativos não possuem período válido."
        )

    inicio_comum = periodos["data_inicial"].max()
    fim_comum = periodos["data_final"].min()

    if inicio_comum > fim_comum:
        raise ValueError(
            "Não existe interseção temporal entre todos os ativos."
        )

    alinhados = (
        pivot.loc[
            inicio_comum:fim_comum
        ]
        .dropna(how="any")
        .copy()
    )

    if alinhados.empty:
        raise ValueError(
            "A base ficou vazia após o alinhamento dos ativos."
        )

    if not alinhados.index.is_monotonic_increasing:
        raise ValueError(
            "As datas dos preços alinhados não estão ordenadas."
        )

    if alinhados.isna().any().any():
        raise ValueError(
            "Existem preços ausentes após o alinhamento."
        )

    return alinhados, periodos


# ============================================================
# RETORNOS, PATRIMÔNIO E MÉTRICAS
# ============================================================

def calcular_desempenho(
    precos_alinhados: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Calcula retornos, patrimônio, drawdown e métricas."""

    if len(precos_alinhados) < 2:
        raise ValueError(
            "São necessários pelo menos dois preços para calcular retornos."
        )

    retornos = (
        precos_alinhados
        .pct_change(fill_method=None)
        .replace(
            [
                np.inf,
                -np.inf,
            ],
            np.nan,
        )
        .dropna(how="any")
    )

    if retornos.empty:
        raise ValueError(
            "Nenhum retorno válido permaneceu após a limpeza."
        )

    patrimonio = (
        VALOR_INICIAL
        * (1.0 + retornos).cumprod()
    )
    maximo_historico = patrimonio.cummax()
    drawdown = patrimonio / maximo_historico - 1.0

    quantidade_dias = len(retornos)

    resumo_decimal = pd.DataFrame(
        {
            "retorno_total": patrimonio.iloc[-1] - VALOR_INICIAL,
            "retorno_anualizado": (
                patrimonio.iloc[-1]
                ** (DIAS_UTEIS_ANO / quantidade_dias)
                - 1.0
            ),
            "volatilidade_anualizada": (
                retornos.std(ddof=1)
                * np.sqrt(DIAS_UTEIS_ANO)
            ),
            "drawdown_maximo": drawdown.min(),
            "media_retorno_diario": retornos.mean(),
            "desvio_retorno_diario": retornos.std(ddof=1),
            "melhor_dia": retornos.max(),
            "pior_dia": retornos.min(),
            "percentual_dias_positivos": retornos.gt(0).mean(),
        }
    )

    resumo_decimal.index.name = "ticker"
    resumo_decimal = resumo_decimal.sort_index()

    resumo_percentual = resumo_decimal * 100.0

    resumo_formatado = resumo_decimal.copy().astype(object)

    for coluna in resumo_formatado.columns:
        resumo_formatado[coluna] = resumo_decimal[coluna].map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )

    return {
        "retornos": retornos,
        "patrimonio": patrimonio,
        "drawdown": drawdown,
        "resumo_decimal": resumo_decimal,
        "resumo_percentual": resumo_percentual,
        "resumo_formatado": resumo_formatado,
    }


# ============================================================
# DADOS MACROECONÔMICOS MENSAIS
# ============================================================

def preparar_serie_mensal(
    dados: pd.DataFrame,
    nome_coluna: str,
) -> pd.DataFrame:
    """Converte uma série para frequência mensal pelo último valor."""

    serie = dados[
        [
            "data",
            "valor",
        ]
    ].copy()

    serie["data"] = pd.to_datetime(
        serie["data"],
        errors="coerce",
    )
    serie["valor"] = pd.to_numeric(
        serie["valor"],
        errors="coerce",
    )

    serie = (
        serie.dropna(
            subset=[
                "data",
                "valor",
            ]
        )
        .drop_duplicates(
            subset=["data"],
            keep="last",
        )
        .sort_values("data")
    )

    serie["mes"] = serie["data"].dt.to_period("M")

    mensal = (
        serie.groupby("mes")["valor"]
        .last()
        .to_frame(nome_coluna)
    )

    mensal.index = (
        mensal.index
        .to_timestamp(how="end")
        .normalize()
    )
    mensal.index.name = "data"

    return mensal


def preparar_macro_mensal(
    series_macro: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Calcula os indicadores mensais usados nos regimes."""

    ipca_mensal = preparar_serie_mensal(
        series_macro["IPCA"],
        "IPCA_MENSAL_PCT",
    )

    ipca_mensal["IPCA_12M_PCT"] = (
        (
            1.0
            + ipca_mensal["IPCA_MENSAL_PCT"] / 100.0
        )
        .rolling(
            window=JANELA_IPCA_12M,
            min_periods=JANELA_IPCA_12M,
        )
        .apply(np.prod, raw=True)
        .sub(1.0)
        .mul(100.0)
    )

    ipca_mensal["IPCA_VARIACAO_3M_PP"] = (
        ipca_mensal["IPCA_12M_PCT"]
        - ipca_mensal["IPCA_12M_PCT"].shift(
            DEFASAGEM_IPCA_MESES
        )
    )

    ibc_br_mensal = preparar_serie_mensal(
        series_macro["IBC_BR"],
        "IBC_BR",
    )

    ibc_br_mensal["IBC_BR_VARIACAO_12M_PCT"] = (
        ibc_br_mensal["IBC_BR"]
        .pct_change(
            periods=JANELA_IBC_BR_12M,
            fill_method=None,
        )
        .mul(100.0)
    )

    ibc_dessaz = preparar_serie_mensal(
        series_macro["IBC_BR_DESSAZONALIZADO"],
        "IBC_BR_DESSAZONALIZADO",
    )

    ibc_dessaz["IBC_BR_VARIACAO_MENSAL_PCT"] = (
        ibc_dessaz["IBC_BR_DESSAZONALIZADO"]
        .pct_change(
            periods=1,
            fill_method=None,
        )
        .mul(100.0)
    )

    ibc_dessaz[
        "IBC_BR_DESSAZONALIZADO_VARIACAO_12M_PCT"
    ] = (
        ibc_dessaz["IBC_BR_DESSAZONALIZADO"]
        .pct_change(
            periods=JANELA_IBC_BR_12M,
            fill_method=None,
        )
        .mul(100.0)
    )

    ibc_dessaz["IBC_BR_MEDIA_MOVEL_3M"] = (
        ibc_dessaz["IBC_BR_DESSAZONALIZADO"]
        .rolling(
            window=JANELA_MEDIA_MOVEL_IBC_BR,
            min_periods=JANELA_MEDIA_MOVEL_IBC_BR,
        )
        .mean()
    )

    ibc_dessaz["IBC_BR_TENDENCIA_3M_PCT"] = (
        ibc_dessaz["IBC_BR_MEDIA_MOVEL_3M"]
        .pct_change(
            periods=DEFASAGEM_TENDENCIA_IBC_BR,
            fill_method=None,
        )
        .mul(100.0)
    )

    cdi = series_macro["CDI"][
        [
            "data",
            "valor",
        ]
    ].copy()

    cdi["data"] = pd.to_datetime(
        cdi["data"],
        errors="coerce",
    )
    cdi["valor"] = pd.to_numeric(
        cdi["valor"],
        errors="coerce",
    )

    cdi = (
        cdi.dropna(
            subset=[
                "data",
                "valor",
            ]
        )
        .drop_duplicates(
            subset=["data"],
            keep="last",
        )
        .sort_values("data")
    )

    cdi["mes"] = cdi["data"].dt.to_period("M")
    cdi["CDI_RETORNO_DIARIO"] = cdi["valor"] / 100.0

    if (1.0 + cdi["CDI_RETORNO_DIARIO"]).le(0).any():
        raise ValueError(
            "A série do CDI possui fatores de capitalização inválidos."
        )

    cdi_mensal = (
        cdi.groupby("mes")["CDI_RETORNO_DIARIO"]
        .apply(
            lambda valores: (
                (1.0 + valores).prod() - 1.0
            )
            * 100.0
        )
        .to_frame("CDI_MENSAL_PCT")
    )

    cdi_mensal.index = (
        cdi_mensal.index
        .to_timestamp(how="end")
        .normalize()
    )
    cdi_mensal.index.name = "data"

    dados_macro_mensais = pd.concat(
        [
            cdi_mensal,
            ipca_mensal,
            ibc_br_mensal,
            ibc_dessaz,
        ],
        axis=1,
    ).sort_index()

    if dados_macro_mensais.empty:
        raise ValueError(
            "A base macroeconômica mensal ficou vazia."
        )

    if dados_macro_mensais.columns.duplicated().any():
        raise ValueError(
            "A base macroeconômica mensal possui colunas duplicadas."
        )

    return dados_macro_mensais


# ============================================================
# ANÁLISES COMPLEMENTARES
# ============================================================

def calcular_precos_normalizados(
    precos_alinhados: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Normaliza cada ativo para base 100."""

    primeiros_precos = precos_alinhados.iloc[0]

    if primeiros_precos.isna().any():
        raise ValueError(
            "Existem ativos sem preço na primeira data comum."
        )

    if primeiros_precos.le(0).any():
        raise ValueError(
            "Existem ativos com primeiro preço não positivo."
        )

    normalizados = (
        precos_alinhados
        .divide(
            primeiros_precos,
            axis="columns",
        )
        * BASE_NORMALIZACAO
    )

    resumo = pd.DataFrame(
        {
            "ticker": normalizados.columns,
            "data_inicial": normalizados.index.min(),
            "data_final": normalizados.index.max(),
            "quantidade_registros": [
                int(normalizados[coluna].notna().sum())
                for coluna in normalizados.columns
            ],
            "valor_inicial": [
                float(normalizados[coluna].iloc[0])
                for coluna in normalizados.columns
            ],
            "valor_final": [
                float(normalizados[coluna].iloc[-1])
                for coluna in normalizados.columns
            ],
            "valor_minimo": [
                float(normalizados[coluna].min())
                for coluna in normalizados.columns
            ],
            "valor_maximo": [
                float(normalizados[coluna].max())
                for coluna in normalizados.columns
            ],
            "variacao_periodo": [
                float(
                    normalizados[coluna].iloc[-1]
                    / BASE_NORMALIZACAO
                    - 1.0
                )
                for coluna in normalizados.columns
            ],
        }
    )

    return normalizados, resumo


def calcular_volatilidade_movel(
    retornos: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula volatilidade móvel anualizada de 63 dias."""

    if len(retornos) < JANELA_VOLATILIDADE:
        raise ValueError(
            "A quantidade de retornos é inferior à janela "
            f"de {JANELA_VOLATILIDADE} dias."
        )

    volatilidade = (
        retornos.rolling(
            window=JANELA_VOLATILIDADE,
            min_periods=JANELA_VOLATILIDADE,
        )
        .std(ddof=1)
        * np.sqrt(DIAS_UTEIS_ANO)
        * 100.0
    )

    registros: list[dict[str, Any]] = []

    for ticker in volatilidade.columns:
        serie = volatilidade[ticker].dropna()

        registros.append(
            {
                "ticker": ticker,
                "data_inicial_valida": (
                    serie.index.min()
                    if not serie.empty
                    else pd.NaT
                ),
                "data_final_valida": (
                    serie.index.max()
                    if not serie.empty
                    else pd.NaT
                ),
                "observacoes_validas": len(serie),
                "volatilidade_media_pct": (
                    float(serie.mean())
                    if not serie.empty
                    else np.nan
                ),
                "volatilidade_mediana_pct": (
                    float(serie.median())
                    if not serie.empty
                    else np.nan
                ),
                "volatilidade_minima_pct": (
                    float(serie.min())
                    if not serie.empty
                    else np.nan
                ),
                "volatilidade_maxima_pct": (
                    float(serie.max())
                    if not serie.empty
                    else np.nan
                ),
                "volatilidade_atual_pct": (
                    float(serie.iloc[-1])
                    if not serie.empty
                    else np.nan
                ),
            }
        )

    return volatilidade, pd.DataFrame(registros)


def resumir_drawdown(
    drawdown: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Converte drawdown para percentual e cria resumo."""

    percentual = drawdown * 100.0
    registros: list[dict[str, Any]] = []

    for ticker in percentual.columns:
        serie = percentual[ticker].dropna()

        registros.append(
            {
                "ticker": ticker,
                "data_inicial": serie.index.min(),
                "data_final": serie.index.max(),
                "observacoes_validas": len(serie),
                "drawdown_maximo_pct": float(serie.min()),
                "data_drawdown_maximo": serie.idxmin(),
                "drawdown_medio_pct": float(serie.mean()),
                "drawdown_mediano_pct": float(serie.median()),
                "drawdown_atual_pct": float(serie.iloc[-1]),
                "dias_em_drawdown": int(serie.lt(-1e-10).sum()),
                "percentual_dias_em_drawdown": float(
                    serie.lt(-1e-10).mean() * 100.0
                ),
            }
        )

    return percentual, pd.DataFrame(registros)


def calcular_correlacao(
    retornos: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Calcula matriz, pares e resumo de correlação."""

    if retornos.shape[1] < 2:
        raise ValueError(
            "São necessários pelo menos dois ativos "
            "para calcular correlações."
        )

    matriz = retornos.corr()
    ativos = matriz.columns.tolist()
    registros_pares: list[dict[str, Any]] = []

    for ativo_1, ativo_2 in combinations(ativos, 2):
        base_par = retornos[
            [
                ativo_1,
                ativo_2,
            ]
        ].dropna()

        correlacao = matriz.loc[
            ativo_1,
            ativo_2,
        ]

        registros_pares.append(
            {
                "ativo_1": ativo_1,
                "ativo_2": ativo_2,
                "correlacao": correlacao,
                "correlacao_absoluta": (
                    abs(correlacao)
                    if pd.notna(correlacao)
                    else np.nan
                ),
                "observacoes_utilizadas": len(base_par),
            }
        )

    pares = (
        pd.DataFrame(registros_pares)
        .sort_values(
            [
                "correlacao_absoluta",
                "correlacao",
            ],
            ascending=[
                False,
                False,
            ],
            na_position="last",
        )
        .reset_index(drop=True)
    )

    validos = pares.dropna(subset=["correlacao"])

    if validos.empty:
        resumo = pd.DataFrame(
            [
                {
                    "quantidade_ativos": len(ativos),
                    "quantidade_pares": len(pares),
                    "correlacao_media": np.nan,
                    "correlacao_mediana": np.nan,
                    "correlacao_media_absoluta": np.nan,
                    "maior_correlacao": np.nan,
                    "menor_correlacao": np.nan,
                }
            ]
        )
    else:
        resumo = pd.DataFrame(
            [
                {
                    "quantidade_ativos": len(ativos),
                    "quantidade_pares": len(pares),
                    "correlacao_media": float(
                        validos["correlacao"].mean()
                    ),
                    "correlacao_mediana": float(
                        validos["correlacao"].median()
                    ),
                    "correlacao_media_absoluta": float(
                        validos["correlacao_absoluta"].mean()
                    ),
                    "maior_correlacao": float(
                        validos["correlacao"].max()
                    ),
                    "menor_correlacao": float(
                        validos["correlacao"].min()
                    ),
                }
            ]
        )

    return matriz, pares, resumo


def diagnosticar_imab(
    precos: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cria diagnóstico auxiliar do IMAB11 quando disponível."""

    dados = (
        precos.loc[
            precos["ticker"].eq("IMAB11.SA")
        ]
        .copy()
        .sort_values("data")
    )

    if dados.empty:
        return (
            pd.DataFrame(),
            pd.DataFrame(),
        )

    dados["ano"] = dados["data"].dt.year

    resumo = (
        dados.groupby("ano", as_index=False)
        .agg(
            close_minimo=("close", "min"),
            close_maximo=("close", "max"),
            close_valores_unicos=("close", "nunique"),
            adj_close_minimo=("adj_close", "min"),
            adj_close_maximo=("adj_close", "max"),
            adj_close_valores_unicos=("adj_close", "nunique"),
            registros=("data", "count"),
        )
    )

    ultimos = dados[
        [
            "data",
            "close",
            "adj_close",
            "volume",
        ]
    ].tail(30)

    return resumo, ultimos



def salvar_tabelas_segmentadas(
    segmentos: dict[str, list[str]],
    diretorio: Path,
    resumo_desempenho: pd.DataFrame,
    resumo_normalizado: pd.DataFrame,
    resumo_retorno_acumulado: pd.DataFrame,
    resumo_volatilidade: pd.DataFrame,
    resumo_drawdown: pd.DataFrame,
    retornos: pd.DataFrame,
) -> list[Path]:
    """Salva resumos e correlações separados por segmento."""

    arquivos: list[Path] = []

    tabelas_por_ticker = {
        "desempenho": resumo_desempenho,
        "precos_normalizados": resumo_normalizado,
        "retorno_acumulado": resumo_retorno_acumulado,
        "volatilidade_movel": resumo_volatilidade,
        "drawdown": resumo_drawdown,
    }

    for segmento, tickers in segmentos.items():
        titulo = TITULOS_SEGMENTOS[segmento]

        for nome, tabela in tabelas_por_ticker.items():
            if "ticker" not in tabela.columns:
                raise ValueError(
                    f"A tabela {nome} não possui a coluna ticker."
                )

            filtrada = (
                tabela.loc[
                    tabela["ticker"].isin(tickers)
                ]
                .copy()
                .sort_values("ticker")
                .reset_index(drop=True)
            )

            if len(filtrada) != len(tickers):
                encontrados = set(
                    filtrada["ticker"].tolist()
                )
                ausentes = [
                    ticker
                    for ticker in tickers
                    if ticker not in encontrados
                ]
                raise ValueError(
                    f"Ativos ausentes na tabela {nome} "
                    f"do segmento {titulo}: {ausentes}"
                )

            caminho = (
                diretorio
                / f"02_segmento_{segmento}_{nome}.csv"
            )
            salvar_csv(
                filtrada,
                caminho,
            )
            arquivos.append(caminho)

        retornos_segmento = retornos[
            tickers
        ].copy()

        matriz = retornos_segmento.corr()
        caminho_matriz = (
            diretorio
            / f"02_segmento_{segmento}_correlacao.csv"
        )
        salvar_csv(
            matriz.reset_index(
                names="ticker"
            ),
            caminho_matriz,
        )
        arquivos.append(caminho_matriz)

        if len(tickers) >= 2:
            _, pares, resumo = calcular_correlacao(
                retornos_segmento
            )

            caminho_pares = (
                diretorio
                / (
                    f"02_segmento_{segmento}_"
                    "pares_correlacao.csv"
                )
            )
            caminho_resumo = (
                diretorio
                / (
                    f"02_segmento_{segmento}_"
                    "resumo_correlacao.csv"
                )
            )

            salvar_csv(
                pares,
                caminho_pares,
            )
            salvar_csv(
                resumo,
                caminho_resumo,
            )

            arquivos.extend(
                [
                    caminho_pares,
                    caminho_resumo,
                ]
            )

    return arquivos


# ============================================================
# GRÁFICOS
# ============================================================

def salvar_figura(
    figura: plt.Figure,
    caminho: Path,
    dpi: int,
) -> None:
    """Salva e fecha uma figura."""

    caminho.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(
        caminho,
        dpi=dpi,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(figura)

    if not caminho.is_file() or caminho.stat().st_size == 0:
        raise FileNotFoundError(
            f"O gráfico não foi salvo corretamente: {caminho}"
        )


def gerar_graficos(
    precos_normalizados: pd.DataFrame,
    patrimonio: pd.DataFrame,
    drawdown_percentual: pd.DataFrame,
    volatilidade: pd.DataFrame,
    matriz_correlacao: pd.DataFrame,
    dados_macro_mensais: pd.DataFrame,
    segmentos: dict[str, list[str]],
    diretorio: Path,
    dpi: int,
) -> list[Path]:
    """Gera gráficos dos ativos por segmento e gráficos macro."""

    arquivos: list[Path] = []

    arquivos_antigos_consolidados = [
        "02_08_precos_normalizados.png",
        "02_09_retorno_acumulado.png",
        "02_10_volatilidade_movel.png",
        "02_11_drawdown_ativos.png",
        "02_12_correlacao_retornos.png",
    ]

    for nome_arquivo in arquivos_antigos_consolidados:
        caminho_antigo = diretorio / nome_arquivo

        if caminho_antigo.is_file():
            caminho_antigo.unlink()

    retorno_acumulado = (
        patrimonio - VALOR_INICIAL
    ) * 100.0

    for segmento, tickers in segmentos.items():
        titulo_segmento = TITULOS_SEGMENTOS[
            segmento
        ]

        estruturas = [
            {
                "dados": precos_normalizados,
                "arquivo": (
                    f"02_08_precos_normalizados_"
                    f"{segmento}.png"
                ),
                "titulo": (
                    "Preços Normalizados — "
                    f"{titulo_segmento}"
                ),
                "eixo_y": "Índice normalizado",
                "linha_referencia": BASE_NORMALIZACAO,
                "referencia_tracejada": True,
            },
            {
                "dados": retorno_acumulado,
                "arquivo": (
                    f"02_09_retorno_acumulado_"
                    f"{segmento}.png"
                ),
                "titulo": (
                    "Retorno Acumulado — "
                    f"{titulo_segmento}"
                ),
                "eixo_y": "Retorno acumulado (%)",
                "linha_referencia": 0.0,
                "referencia_tracejada": True,
            },
            {
                "dados": volatilidade,
                "arquivo": (
                    f"02_10_volatilidade_movel_"
                    f"{segmento}.png"
                ),
                "titulo": (
                    "Volatilidade Móvel Anualizada "
                    f"— {titulo_segmento} — "
                    f"{JANELA_VOLATILIDADE} Dias"
                ),
                "eixo_y": "Volatilidade anualizada (%)",
                "linha_referencia": None,
                "referencia_tracejada": False,
            },
            {
                "dados": drawdown_percentual,
                "arquivo": (
                    f"02_11_drawdown_ativos_"
                    f"{segmento}.png"
                ),
                "titulo": (
                    "Drawdown — "
                    f"{titulo_segmento}"
                ),
                "eixo_y": "Drawdown (%)",
                "linha_referencia": 0.0,
                "referencia_tracejada": False,
            },
        ]

        for estrutura in estruturas:
            dados = estrutura["dados"]
            ausentes = [
                ticker
                for ticker in tickers
                if ticker not in dados.columns
            ]

            if ausentes:
                raise ValueError(
                    "Ativos ausentes no gráfico "
                    f"{estrutura['arquivo']}: {ausentes}"
                )

            caminho = (
                diretorio
                / str(estrutura["arquivo"])
            )
            fig, ax = plt.subplots(
                figsize=(14, 7)
            )

            for ticker in tickers:
                ax.plot(
                    dados.index,
                    dados[ticker],
                    linewidth=1.8,
                    label=ticker,
                )

            linha_referencia = estrutura[
                "linha_referencia"
            ]

            if linha_referencia is not None:
                ax.axhline(
                    y=float(linha_referencia),
                    linewidth=1,
                    linestyle=(
                        "--"
                        if estrutura[
                            "referencia_tracejada"
                        ]
                        else "-"
                    ),
                )

            ax.set_title(
                str(estrutura["titulo"])
            )
            ax.set_xlabel("Data")
            ax.set_ylabel(
                str(estrutura["eixo_y"])
            )
            ax.legend(
                title="Ativo",
                loc="best",
            )
            ax.grid(alpha=0.3)

            salvar_figura(
                fig,
                caminho,
                dpi,
            )
            arquivos.append(caminho)

        matriz_segmento = matriz_correlacao.loc[
            tickers,
            tickers,
        ]

        caminho_correlacao = (
            diretorio
            / (
                "02_12_correlacao_retornos_"
                f"{segmento}.png"
            )
        )
        fig, ax = plt.subplots(
            figsize=(8, 7)
        )
        imagem = ax.imshow(
            matriz_segmento.to_numpy(
                dtype=float
            ),
            vmin=-1,
            vmax=1,
            aspect="auto",
        )
        ax.set_xticks(
            range(len(matriz_segmento.columns))
        )
        ax.set_xticklabels(
            matriz_segmento.columns,
            rotation=45,
            ha="right",
        )
        ax.set_yticks(
            range(len(matriz_segmento.index))
        )
        ax.set_yticklabels(
            matriz_segmento.index
        )
        ax.set_title(
            "Correlação dos Retornos — "
            f"{titulo_segmento}"
        )

        for linha in range(
            len(matriz_segmento.index)
        ):
            for coluna in range(
                len(matriz_segmento.columns)
            ):
                valor = matriz_segmento.iloc[
                    linha,
                    coluna,
                ]

                if pd.notna(valor):
                    ax.text(
                        coluna,
                        linha,
                        f"{valor:.2f}",
                        ha="center",
                        va="center",
                        fontsize=9,
                    )

        fig.colorbar(
            imagem,
            ax=ax,
            label="Correlação",
        )
        salvar_figura(
            fig,
            caminho_correlacao,
            dpi,
        )
        arquivos.append(caminho_correlacao)

    # Correlação consolidada dos 12 ativos selecionados
    caminho = (
        diretorio
        / "02_12_correlacao_retornos_consolidada.png"
    )
    fig, ax = plt.subplots(figsize=(13, 11))
    imagem = ax.imshow(
        matriz_correlacao.to_numpy(dtype=float),
        vmin=-1,
        vmax=1,
        aspect="auto",
    )
    ax.set_xticks(
        range(len(matriz_correlacao.columns))
    )
    ax.set_xticklabels(
        matriz_correlacao.columns,
        rotation=45,
        ha="right",
    )
    ax.set_yticks(
        range(len(matriz_correlacao.index))
    )
    ax.set_yticklabels(
        matriz_correlacao.index
    )
    ax.set_title(
        "Correlação dos Retornos — "
        "Ativos Selecionados"
    )

    for linha in range(
        len(matriz_correlacao.index)
    ):
        for coluna in range(
            len(matriz_correlacao.columns)
        ):
            valor = matriz_correlacao.iloc[
                linha,
                coluna,
            ]

            if pd.notna(valor):
                ax.text(
                    coluna,
                    linha,
                    f"{valor:.2f}",
                    ha="center",
                    va="center",
                    fontsize=7,
                )

    fig.colorbar(
        imagem,
        ax=ax,
        label="Correlação",
    )
    salvar_figura(
        fig,
        caminho,
        dpi,
    )
    arquivos.append(caminho)

    # IPCA 12 meses
    caminho = diretorio / "02_13_ipca_12_meses.png"
    serie_ipca = dados_macro_mensais[
        "IPCA_12M_PCT"
    ].dropna()
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(
        serie_ipca.index,
        serie_ipca,
        linewidth=1.8,
        label="IPCA acumulado em 12 meses",
    )
    ax.axhline(
        y=0.0,
        linewidth=1,
        linestyle="--",
        alpha=0.6,
    )
    ax.set_title("IPCA Acumulado em 12 Meses")
    ax.set_xlabel("Data")
    ax.set_ylabel("Inflação (%)")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, caminho, dpi)
    arquivos.append(caminho)

    # IBC-Br dessazonalizado
    caminho = (
        diretorio
        / "02_14_ibc_br_dessazonalizado.png"
    )
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(
        dados_macro_mensais.index,
        dados_macro_mensais[
            "IBC_BR_DESSAZONALIZADO"
        ],
        linewidth=1.8,
        label="IBC-Br dessazonalizado",
    )
    ax.plot(
        dados_macro_mensais.index,
        dados_macro_mensais[
            "IBC_BR_MEDIA_MOVEL_3M"
        ],
        linewidth=2,
        label="Média móvel de 3 meses",
    )
    ax.set_title("IBC-Br Dessazonalizado")
    ax.set_xlabel("Data")
    ax.set_ylabel("Índice")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, caminho, dpi)
    arquivos.append(caminho)

    # Tendências macroeconômicas
    caminho = (
        diretorio
        / "02_15_tendencias_inflacao_crescimento.png"
    )
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(
        dados_macro_mensais.index,
        dados_macro_mensais[
            "IPCA_VARIACAO_3M_PP"
        ],
        linewidth=1.8,
        label="Variação do IPCA em 3 meses",
    )
    ax.plot(
        dados_macro_mensais.index,
        dados_macro_mensais[
            "IBC_BR_TENDENCIA_3M_PCT"
        ],
        linewidth=1.8,
        label="Tendência do IBC-Br em 3 meses",
    )
    ax.axhline(
        y=0.0,
        linewidth=1,
        linestyle="--",
    )
    ax.set_title(
        "Variações de Inflação e Crescimento"
    )
    ax.set_xlabel("Data")
    ax.set_ylabel("Variação")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, caminho, dpi)
    arquivos.append(caminho)

    return arquivos


# ============================================================
# CONFERÊNCIA FINAL
# ============================================================

def conferir_arquivos(
    arquivos: dict[str, Path],
) -> pd.DataFrame:
    """Confere existência, tamanho e leitura dos arquivos finais."""

    registros: list[dict[str, Any]] = []

    for base, caminho in arquivos.items():
        registro = {
            "base": base,
            "arquivo": caminho.name,
            "caminho": str(caminho),
            "arquivo_existe": caminho.is_file(),
            "arquivo_nao_vazio": False,
            "csv_legivel": False,
            "quantidade_registros": 0,
            "quantidade_colunas": 0,
            "tamanho_bytes": 0,
            "status": "NAO_ENCONTRADO",
            "erro": "",
        }

        if not caminho.is_file():
            registro["erro"] = "O arquivo não foi localizado."
            registros.append(registro)
            continue

        registro["tamanho_bytes"] = caminho.stat().st_size
        registro["arquivo_nao_vazio"] = caminho.stat().st_size > 0

        if caminho.stat().st_size == 0:
            registro["status"] = "ARQUIVO_VAZIO"
            registro["erro"] = "O arquivo possui tamanho zero."
            registros.append(registro)
            continue

        try:
            dados = pd.read_csv(
                caminho,
                encoding="utf-8-sig",
                low_memory=False,
            )
            registro["csv_legivel"] = True
            registro["quantidade_registros"] = len(dados)
            registro["quantidade_colunas"] = len(dados.columns)

            if dados.empty:
                registro["status"] = "SEM_REGISTROS"
                registro["erro"] = (
                    "O CSV possui cabeçalho, mas não possui registros."
                )
            else:
                registro["status"] = "OK"

        except Exception as erro:
            registro["status"] = "ERRO_LEITURA"
            registro["erro"] = str(erro)

        registros.append(registro)

    return pd.DataFrame(registros)


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main() -> None:
    """Executa toda a análise exploratória em um único arquivo Python."""

    inicio = time.perf_counter()
    inicio_utc = datetime.now(timezone.utc)

    configuracao = carregar_configuracao()
    diretorios = criar_diretorios(configuracao)

    print("=" * 80)
    print("02 — ANÁLISE EXPLORATÓRIA DOS DADOS")
    print("=" * 80)
    print(f"Raiz do projeto: {RAIZ_PROJETO}")
    print(f"Configuração: {ARQUIVO_CONFIG}")

    # --------------------------------------------------------
    # 1. CARREGAMENTO
    # --------------------------------------------------------

    precos_aprovados, arquivo_precos = carregar_precos(
        configuracao
    )
    (
        ativos_selecionados,
        arquivo_selecao,
    ) = carregar_ativos_selecionados(
        configuracao
    )
    segmentos = criar_mapa_segmentos(
        ativos_selecionados
    )
    precos = filtrar_precos_selecionados(
        precos_aprovados=precos_aprovados,
        ativos_selecionados=ativos_selecionados,
    )

    salvar_csv(
        ativos_selecionados,
        diretorios["tabelas"]
        / "02_01_ativos_selecionados_utilizados.csv",
    )

    dados_macro, arquivo_macro = carregar_macro(
        diretorios["macro"]
    )
    series_macro = separar_series_macro(
        dados_macro,
        configuracao,
    )

    print(
        f"\nPreços aprovados carregados: {arquivo_precos}"
    )
    print(
        f"Arquivo de seleção: {arquivo_selecao}"
    )
    print(
        f"Ativos selecionados: "
        f"{precos['ticker'].nunique()} | "
        f"Registros: {len(precos):,}"
    )

    for segmento in ORDEM_SEGMENTOS:
        tickers = segmentos.get(
            segmento,
            [],
        )
        print(
            f"  - {TITULOS_SEGMENTOS[segmento]}: "
            f"{len(tickers)} — {', '.join(tickers)}"
        )
    print(
        f"Macro carregado: {arquivo_macro}"
    )
    print(
        f"Séries: {dados_macro['codigo_sgs'].nunique()} | "
        f"Registros: {len(dados_macro):,}"
    )

    # --------------------------------------------------------
    # 2. QUALIDADE
    # --------------------------------------------------------

    (
        qualidade_ativos,
        qualidade_macro,
        problemas_qualidade,
        resumo_qualidade,
    ) = analisar_qualidade(
        precos=precos,
        dados_macro=dados_macro,
        configuracao=configuracao,
    )

    caminho_resumo_qualidade = resolver_caminho(
        obter_valor(
            configuracao,
            (
                "qualidade_dados",
                "arquivo_saida",
            ),
            obrigatorio=False,
            padrao="data/processed/resumo_qualidade.csv",
        )
    )

    salvar_csv(
        qualidade_ativos,
        diretorios["tabelas"]
        / "02_04_qualidade_ativos.csv",
    )
    salvar_csv(
        qualidade_macro,
        diretorios["tabelas"]
        / "02_04_qualidade_series_macro.csv",
    )
    salvar_csv(
        problemas_qualidade,
        diretorios["tabelas"]
        / "02_04_pontos_atencao_qualidade.csv",
    )
    salvar_csv(
        resumo_qualidade,
        caminho_resumo_qualidade,
    )

    # --------------------------------------------------------
    # 3. ALINHAMENTO DOS PREÇOS
    # --------------------------------------------------------

    precos_alinhados, periodos_ativos = alinhar_precos(
        precos
    )

    arquivo_precos_tratados = (
        diretorios["processed"]
        / "precos_ativos_tratados.csv"
    )
    arquivo_precos_periodo_comum = (
        diretorios["processed"]
        / "precos_periodo_comum.csv"
    )

    salvar_temporal(
        precos_alinhados,
        arquivo_precos_tratados,
    )
    salvar_temporal(
        precos_alinhados,
        arquivo_precos_periodo_comum,
    )
    salvar_temporal(
        precos_alinhados,
        diretorios["tabelas"]
        / "02_05_precos_periodo_comum.csv",
    )
    salvar_csv(
        periodos_ativos,
        diretorios["tabelas"]
        / "02_05_periodos_disponiveis_ativos.csv",
    )

    # --------------------------------------------------------
    # 4. RETORNOS E MÉTRICAS
    # --------------------------------------------------------

    desempenho = calcular_desempenho(
        precos_alinhados
    )

    arquivo_retornos = (
        diretorios["processed"]
        / "retornos_ativos.csv"
    )
    arquivo_patrimonio = (
        diretorios["processed"]
        / "patrimonio_acumulado_ativos.csv"
    )
    arquivo_drawdown = (
        diretorios["processed"]
        / "drawdown_ativos.csv"
    )

    salvar_temporal(
        desempenho["retornos"],
        arquivo_retornos,
    )
    salvar_temporal(
        desempenho["patrimonio"],
        arquivo_patrimonio,
    )
    salvar_temporal(
        desempenho["drawdown"],
        arquivo_drawdown,
    )
    salvar_csv(
        desempenho["resumo_percentual"].reset_index(),
        diretorios["tabelas"]
        / "02_06_resumo_desempenho_ativos.csv",
    )
    salvar_csv(
        desempenho["resumo_formatado"].reset_index(),
        diretorios["tabelas"]
        / "02_06_resumo_desempenho_ativos_formatado.csv",
    )

    # --------------------------------------------------------
    # 5. MACRO MENSAL
    # --------------------------------------------------------

    dados_macro_mensais = preparar_macro_mensal(
        series_macro
    )

    arquivo_macro_mensal = (
        diretorios["processed"]
        / "dados_macro_mensais.csv"
    )

    salvar_temporal(
        dados_macro_mensais,
        arquivo_macro_mensal,
    )

    resumo_macro = (
        dados_macro_mensais
        .agg(
            [
                "count",
                "min",
                "max",
                "mean",
                "median",
                "std",
            ]
        )
        .T
        .reset_index()
        .rename(columns={"index": "indicador"})
    )

    salvar_csv(
        resumo_macro,
        diretorios["tabelas"]
        / "02_07_resumo_dados_macro_mensais.csv",
    )

    # --------------------------------------------------------
    # 6. ANÁLISES COMPLEMENTARES
    # --------------------------------------------------------

    precos_normalizados, resumo_normalizado = (
        calcular_precos_normalizados(
            precos_alinhados
        )
    )

    salvar_temporal(
        precos_normalizados,
        diretorios["processed"]
        / "precos_normalizados.csv",
    )
    salvar_csv(
        resumo_normalizado,
        diretorios["tabelas"]
        / "02_08_resumo_precos_normalizados.csv",
    )

    retorno_acumulado = (
        desempenho["patrimonio"] - 1.0
    ) * 100.0

    resumo_retorno_acumulado = pd.DataFrame(
        {
            "ticker": retorno_acumulado.columns,
            "retorno_final_pct": [
                float(retorno_acumulado[coluna].iloc[-1])
                for coluna in retorno_acumulado.columns
            ],
            "retorno_maximo_pct": [
                float(retorno_acumulado[coluna].max())
                for coluna in retorno_acumulado.columns
            ],
            "retorno_minimo_pct": [
                float(retorno_acumulado[coluna].min())
                for coluna in retorno_acumulado.columns
            ],
        }
    )

    salvar_temporal(
        retorno_acumulado,
        diretorios["processed"]
        / "retorno_acumulado_ativos.csv",
    )
    salvar_csv(
        resumo_retorno_acumulado,
        diretorios["tabelas"]
        / "02_09_resumo_retorno_acumulado.csv",
    )

    volatilidade, resumo_volatilidade = (
        calcular_volatilidade_movel(
            desempenho["retornos"]
        )
    )
    salvar_temporal(
        volatilidade,
        diretorios["processed"]
        / "volatilidade_movel_63d.csv",
    )
    salvar_csv(
        resumo_volatilidade,
        diretorios["tabelas"]
        / "02_10_resumo_volatilidade_movel.csv",
    )

    drawdown_percentual, resumo_drawdown = (
        resumir_drawdown(
            desempenho["drawdown"]
        )
    )
    salvar_temporal(
        drawdown_percentual,
        diretorios["processed"]
        / "drawdown_percentual_ativos.csv",
    )
    salvar_csv(
        resumo_drawdown,
        diretorios["tabelas"]
        / "02_11_resumo_drawdown_ativos.csv",
    )

    matriz_correlacao, pares_correlacao, resumo_correlacao = (
        calcular_correlacao(
            desempenho["retornos"]
        )
    )
    salvar_csv(
        matriz_correlacao.reset_index(
            names="ticker"
        ),
        diretorios["processed"]
        / "matriz_correlacao_retornos.csv",
    )
    salvar_csv(
        pares_correlacao,
        diretorios["tabelas"]
        / "02_12_pares_correlacao_retornos.csv",
    )
    salvar_csv(
        resumo_correlacao,
        diretorios["tabelas"]
        / "02_12_resumo_correlacao_retornos.csv",
    )

    arquivos_tabelas_segmentadas = (
        salvar_tabelas_segmentadas(
            segmentos=segmentos,
            diretorio=diretorios["tabelas"],
            resumo_desempenho=(
                desempenho[
                    "resumo_percentual"
                ]
                .reset_index()
            ),
            resumo_normalizado=resumo_normalizado,
            resumo_retorno_acumulado=(
                resumo_retorno_acumulado
            ),
            resumo_volatilidade=resumo_volatilidade,
            resumo_drawdown=resumo_drawdown,
            retornos=desempenho["retornos"],
        )
    )

    resumo_imab, ultimos_imab = diagnosticar_imab(
        precos
    )

    if not resumo_imab.empty:
        salvar_csv(
            resumo_imab,
            diretorios["tabelas"]
            / "02_diagnostico_imab11_por_ano.csv",
        )
        salvar_csv(
            ultimos_imab,
            diretorios["tabelas"]
            / "02_diagnostico_imab11_ultimos_registros.csv",
        )

    tendencias = dados_macro_mensais[
        [
            "IPCA_VARIACAO_3M_PP",
            "IBC_BR_TENDENCIA_3M_PCT",
        ]
    ].dropna(how="all")

    salvar_temporal(
        tendencias,
        diretorios["processed"]
        / "tendencias_inflacao_crescimento.csv",
    )

    # --------------------------------------------------------
    # 7. GRÁFICOS
    # --------------------------------------------------------

    config_graficos = obter_valor(
        configuracao,
        ("graficos",),
        obrigatorio=False,
        padrao={},
    )

    arquivos_graficos: list[Path] = []

    if bool(config_graficos.get("ativo", True)):
        arquivos_graficos = gerar_graficos(
            precos_normalizados=precos_normalizados,
            patrimonio=desempenho["patrimonio"],
            drawdown_percentual=drawdown_percentual,
            volatilidade=volatilidade,
            matriz_correlacao=matriz_correlacao,
            dados_macro_mensais=dados_macro_mensais,
            segmentos=segmentos,
            diretorio=diretorios["graficos"],
            dpi=int(config_graficos.get("dpi", 150)),
        )

    # --------------------------------------------------------
    # 8. CONFERÊNCIA FINAL
    # --------------------------------------------------------

    arquivos_finais = {
        "Preços dos ativos tratados": arquivo_precos_tratados,
        "Retornos dos ativos": arquivo_retornos,
        "Dados macroeconômicos mensais": arquivo_macro_mensal,
        "Resumo de qualidade": caminho_resumo_qualidade,
    }

    conferencia = conferir_arquivos(
        arquivos_finais
    )

    arquivo_conferencia = (
        diretorios["tabelas"]
        / "02_16_conferencia_final_arquivos.csv"
    )

    salvar_csv(
        conferencia,
        arquivo_conferencia,
    )

    if conferencia["status"].ne("OK").any():
        problematicos = conferencia.loc[
            conferencia["status"].ne("OK"),
            [
                "base",
                "caminho",
                "status",
                "erro",
            ],
        ]

        raise RuntimeError(
            "A conferência final encontrou arquivos problemáticos:\n"
            + problematicos.to_string(index=False)
        )

    fim_utc = datetime.now(timezone.utc)

    print("\n" + "=" * 80)
    print("ETAPA 02 CONCLUÍDA")
    print("=" * 80)
    print(
        f"Ativos analisados: {precos_alinhados.shape[1]}"
    )
    print(
        f"Período comum: "
        f"{precos_alinhados.index.min():%Y-%m-%d} até "
        f"{precos_alinhados.index.max():%Y-%m-%d}"
    )
    print(
        f"Retornos calculados: {len(desempenho['retornos']):,}"
    )
    print(
        f"Meses macroeconômicos: {len(dados_macro_mensais):,}"
    )
    print(
        f"Status de qualidade: "
        f"{resumo_qualidade['status_final'].iloc[0]}"
    )
    print(
        f"Tabelas segmentadas geradas: "
        f"{len(arquivos_tabelas_segmentadas)}"
    )
    print(
        f"Gráficos gerados: {len(arquivos_graficos)}"
    )
    print(
        f"Início UTC: {inicio_utc.isoformat()}"
    )
    print(
        f"Fim UTC: {fim_utc.isoformat()}"
    )
    print(
        f"Duração: {time.perf_counter() - inicio:.2f}s"
    )

    interromper = bool(
        obter_valor(
            configuracao,
            (
                "qualidade_dados",
                "interromper_execucao_em_erro_critico",
            ),
            obrigatorio=False,
            padrao=True,
        )
    )

    if (
        interromper
        and resumo_qualidade["status_final"].iloc[0]
        == "ERROS_ESTRUTURAIS"
    ):
        raise RuntimeError(
            "A análise exploratória encontrou erros estruturais."
        )


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
        sys.exit(130)

    except Exception as erro:
        print(f"\nERRO: {erro}")
        sys.exit(1)