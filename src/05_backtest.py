from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

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

RAIZ_PROJETO = Path(
    os.getenv(
        "PROJECT_ROOT",
        Path(__file__).resolve().parent,
    )
).resolve()

ARQUIVO_CONFIG = Path(
    os.getenv(
        "PROJECT_CONFIG",
        RAIZ_PROJETO / "config" / "config.yaml",
    )
).resolve()


# ============================================================
# CONFIGURAÇÃO E I/O
# ============================================================

def carregar_configuracao() -> dict[str, Any]:
    """Carrega e valida o config.yaml do projeto."""

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
                    "Parâmetro obrigatório ausente no config.yaml: "
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


def salvar_csv_validado(
    tabela: pd.DataFrame,
    caminho: Path,
    *,
    index: bool = False,
    index_label: str | None = None,
) -> None:
    """Salva um CSV e valida existência, colunas e quantidade de linhas."""

    caminho.parent.mkdir(parents=True, exist_ok=True)

    tabela.to_csv(
        caminho,
        index=index,
        index_label=index_label,
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

    quantidade_esperada = len(tabela)

    if len(validacao) != quantidade_esperada:
        raise ValueError(
            "A quantidade de registros do CSV salvo não corresponde "
            f"ao DataFrame original: {caminho}"
        )


def salvar_figura(
    figura: plt.Figure,
    caminho: Path,
    dpi: int,
) -> None:
    """Salva e fecha uma figura do Matplotlib."""

    caminho.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(
        caminho,
        dpi=dpi,
        bbox_inches="tight",
    )
    plt.close(figura)

    if not caminho.is_file() or caminho.stat().st_size == 0:
        raise FileNotFoundError(
            f"O gráfico não foi salvo corretamente: {caminho}"
        )


# ============================================================
# CARREGAMENTO E VALIDAÇÃO DA BASE
# ============================================================

def carregar_base_alocacao(
    configuracao: dict[str, Any],
) -> tuple[pd.DataFrame, list[str], list[str], Path]:
    """Carrega a base mensal produzida por 04_alocacao_portfolio.py."""

    caminho_config = obter_valor(
        configuracao,
        ("backtest", "arquivo_entrada"),
        obrigatorio=False,
        padrao=obter_valor(
            configuracao,
            ("alocacao", "arquivos_saida", "base_mensal"),
            obrigatorio=False,
            padrao="data/processed/alocacao_portfolio_mensal.csv",
        ),
    )

    caminho = resolver_caminho(caminho_config)

    if not caminho.is_file():
        raise FileNotFoundError(
            "A base mensal da alocação não foi encontrada.\n"
            "Execute primeiro 04_alocacao_portfolio.py.\n"
            f"Arquivo esperado: {caminho}"
        )

    dados = pd.read_csv(
        caminho,
        encoding="utf-8-sig",
        low_memory=False,
    )

    if dados.empty:
        raise ValueError(
            f"A base mensal da alocação está vazia: {caminho}"
        )

    if "data" not in dados.columns:
        raise ValueError(
            "A base da alocação não possui a coluna 'data'."
        )

    dados["data"] = pd.to_datetime(
        dados["data"],
        errors="coerce",
    )

    if dados["data"].isna().any():
        raise ValueError(
            "A base da alocação possui datas inválidas."
        )

    dados = (
        dados.drop_duplicates(
            subset=["data"],
            keep="last",
        )
        .sort_values("data")
        .reset_index(drop=True)
    )

    colunas_pesos = [
        coluna
        for coluna in dados.columns
        if coluna.startswith("peso_")
        and not coluna.startswith("peso_estatica_")
    ]

    ativos = [
        coluna.removeprefix("peso_")
        for coluna in colunas_pesos
    ]

    if not ativos:
        raise ValueError(
            "Nenhuma coluna de peso foi encontrada na base da alocação."
        )

    coluna_retorno_portfolio = (
        "retorno_portfolio_bruto"
        if "retorno_portfolio_bruto" in dados.columns
        else "retorno_portfolio"
    )
    coluna_retorno_benchmark = (
        "retorno_benchmark_estatico"
        if "retorno_benchmark_estatico" in dados.columns
        else "retorno_carteira_estatica"
    )

    colunas_obrigatorias = [
        "data",
        "regime_sinal",
        coluna_retorno_portfolio,
        coluna_retorno_benchmark,
        *ativos,
        *colunas_pesos,
    ]

    colunas_ausentes = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in dados.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            "Colunas obrigatórias ausentes na base da alocação:\n"
            f"{colunas_ausentes}"
        )

    dados["retorno_portfolio"] = pd.to_numeric(
        dados[coluna_retorno_portfolio],
        errors="coerce",
    )
    dados["retorno_carteira_estatica"] = pd.to_numeric(
        dados[coluna_retorno_benchmark],
        errors="coerce",
    )

    colunas_numericas = [
        *ativos,
        *colunas_pesos,
        "retorno_portfolio",
        "retorno_carteira_estatica",
    ]

    for coluna in colunas_numericas:
        dados[coluna] = pd.to_numeric(
            dados[coluna],
            errors="coerce",
        )

    nulos = (
        dados[
            [
                "data",
                "regime_sinal",
                *colunas_numericas,
            ]
        ]
        .isna()
        .sum()
    )
    nulos = nulos[nulos.gt(0)]

    if not nulos.empty:
        raise ValueError(
            "Existem valores nulos nas colunas obrigatórias:\n"
            f"{nulos.to_string()}"
        )

    soma_pesos = dados[colunas_pesos].sum(axis=1)

    tolerancia = float(
        obter_valor(
            configuracao,
            ("portfolio", "tolerancia_soma_pesos"),
            obrigatorio=False,
            padrao=1e-6,
        )
    )

    if not np.allclose(
        soma_pesos,
        1.0,
        atol=tolerancia,
        rtol=0.0,
    ):
        raise ValueError(
            "Existem meses em que os pesos não somam 100%.\n"
            f"Mínimo: {soma_pesos.min():.12f}\n"
            f"Máximo: {soma_pesos.max():.12f}"
        )

    dados["soma_pesos_validacao"] = soma_pesos

    return dados, ativos, colunas_pesos, caminho


# ============================================================
# TURNOVER, CUSTOS E RETORNOS LÍQUIDOS
# ============================================================

def calcular_turnover(
    dados: pd.DataFrame,
    colunas_retornos: list[str],
    colunas_pesos_alvo: list[str],
    cobrar_custo_inicial: bool,
) -> np.ndarray:
    """
    Calcula o turnover como metade da soma absoluta das negociações.

    Antes do rebalanceamento, os pesos do mês anterior são atualizados
    pelos retornos realizados. O turnover mede a distância entre esses
    pesos pós-mercado e os novos pesos-alvo.
    """

    quantidade_meses = len(dados)
    turnover = np.zeros(
        quantidade_meses,
        dtype=float,
    )

    if quantidade_meses == 0:
        return turnover

    if len(colunas_retornos) != len(colunas_pesos_alvo):
        raise ValueError(
            "A quantidade de retornos deve corresponder "
            "à quantidade de pesos."
        )

    if cobrar_custo_inicial:
        turnover[0] = 1.0

    for indice in range(1, quantidade_meses):
        pesos_anteriores = (
            dados.loc[
                indice - 1,
                colunas_pesos_alvo,
            ]
            .astype(float)
            .to_numpy()
        )
        retornos_anteriores = (
            dados.loc[
                indice - 1,
                colunas_retornos,
            ]
            .astype(float)
            .to_numpy()
        )

        fatores_ativos = 1.0 + retornos_anteriores

        if (fatores_ativos <= 0).any():
            raise ValueError(
                "Um ativo apresentou retorno menor ou igual a -100% "
                f"no índice mensal {indice - 1}."
            )

        patrimonio_relativo = float(
            np.dot(
                pesos_anteriores,
                fatores_ativos,
            )
        )

        if patrimonio_relativo <= 0:
            raise ValueError(
                "O patrimônio relativo da carteira ficou menor "
                f"ou igual a zero no índice {indice - 1}."
            )

        pesos_pos_mercado = (
            pesos_anteriores
            * fatores_ativos
            / patrimonio_relativo
        )

        pesos_alvo_atuais = (
            dados.loc[
                indice,
                colunas_pesos_alvo,
            ]
            .astype(float)
            .to_numpy()
        )

        turnover[indice] = float(
            np.abs(
                pesos_alvo_atuais
                - pesos_pos_mercado
            ).sum()
            / 2.0
        )

    return turnover


def aplicar_custos(
    base: pd.DataFrame,
    ativos: list[str],
    colunas_pesos: list[str],
    custo_por_turnover: float,
    cobrar_custo_inicial: bool,
    valor_inicial: float,
) -> pd.DataFrame:
    """Calcula turnover, custos, retornos líquidos, índices e drawdowns."""

    if custo_por_turnover < 0:
        raise ValueError(
            "O custo por unidade de turnover não pode ser negativo."
        )

    if valor_inicial <= 0:
        raise ValueError(
            "O valor inicial do índice deve ser positivo."
        )

    dados = (
        base.copy()
        .sort_values("data")
        .reset_index(drop=True)
    )

    dados["turnover_portfolio"] = calcular_turnover(
        dados=dados,
        colunas_retornos=ativos,
        colunas_pesos_alvo=colunas_pesos,
        cobrar_custo_inicial=cobrar_custo_inicial,
    )

    peso_estatico = 1.0 / len(ativos)
    colunas_pesos_estatica: list[str] = []

    for ativo in ativos:
        coluna = f"peso_estatica_{ativo}"
        dados[coluna] = peso_estatico
        colunas_pesos_estatica.append(coluna)

    dados["turnover_estatica"] = calcular_turnover(
        dados=dados,
        colunas_retornos=ativos,
        colunas_pesos_alvo=colunas_pesos_estatica,
        cobrar_custo_inicial=cobrar_custo_inicial,
    )

    dados["custo_portfolio"] = (
        dados["turnover_portfolio"]
        * custo_por_turnover
    )
    dados["custo_estatica"] = (
        dados["turnover_estatica"]
        * custo_por_turnover
    )

    fatores_custo_portfolio = (
        1.0 - dados["custo_portfolio"]
    )
    fatores_custo_estatica = (
        1.0 - dados["custo_estatica"]
    )

    if (
        fatores_custo_portfolio.le(0).any()
        or fatores_custo_estatica.le(0).any()
    ):
        raise ValueError(
            "Os custos geraram fator patrimonial menor ou igual a zero."
        )

    dados["retorno_portfolio_liquido"] = (
        (
            1.0
            + dados["retorno_portfolio"]
        )
        * fatores_custo_portfolio
        - 1.0
    )
    dados["retorno_estatica_liquido"] = (
        (
            1.0
            + dados["retorno_carteira_estatica"]
        )
        * fatores_custo_estatica
        - 1.0
    )

    series_retorno = {
        "portfolio_bruto": "retorno_portfolio",
        "portfolio_liquido": "retorno_portfolio_liquido",
        "estatica_bruta": "retorno_carteira_estatica",
        "estatica_liquida": "retorno_estatica_liquido",
    }

    for nome, coluna_retorno in series_retorno.items():
        indice = (
            valor_inicial
            * (
                1.0
                + dados[coluna_retorno]
            )
            .cumprod()
        )
        pico = indice.cummax()
        drawdown = indice / pico - 1.0

        dados[f"indice_{nome}"] = indice
        dados[f"pico_{nome}"] = pico
        dados[f"drawdown_{nome}"] = drawdown

    # Compatibilidade com nomes históricos.
    dados["indice_portfolio_bruto"] = dados[
        "indice_portfolio_bruto"
    ]
    dados["indice_portfolio_liquido"] = dados[
        "indice_portfolio_liquido"
    ]
    dados["indice_estatica_bruto"] = dados[
        "indice_estatica_bruta"
    ]
    dados["indice_estatica_liquido"] = dados[
        "indice_estatica_liquida"
    ]

    return dados


# ============================================================
# CDI E TAXA LIVRE DE RISCO
# ============================================================

def carregar_cdi_mensal(
    configuracao: dict[str, Any],
) -> tuple[pd.DataFrame | None, Path | None]:
    """Carrega o CDI mensal quando disponível."""

    usar_cdi = bool(
        obter_valor(
            configuracao,
            ("backtest", "usar_cdi_taxa_livre_risco"),
            obrigatorio=False,
            padrao=True,
        )
    )

    if not usar_cdi:
        return None, None

    caminho = resolver_caminho(
        obter_valor(
            configuracao,
            ("processamento", "arquivos_saida", "macro_mensal"),
            obrigatorio=False,
            padrao="data/processed/dados_macro_mensais.csv",
        )
    )

    if not caminho.is_file():
        return None, None

    dados = pd.read_csv(
        caminho,
        encoding="utf-8-sig",
        low_memory=False,
    )

    if not {
        "data",
        "CDI_MENSAL_PCT",
    }.issubset(dados.columns):
        return None, caminho

    dados["data"] = pd.to_datetime(
        dados["data"],
        errors="coerce",
    )
    dados["retorno_cdi"] = (
        pd.to_numeric(
            dados["CDI_MENSAL_PCT"],
            errors="coerce",
        )
        / 100.0
    )

    dados = (
        dados[
            [
                "data",
                "retorno_cdi",
            ]
        ]
        .dropna()
        .drop_duplicates(
            subset=["data"],
            keep="last",
        )
        .sort_values("data")
        .reset_index(drop=True)
    )

    if dados.empty:
        return None, caminho

    return dados, caminho


def adicionar_cdi(
    backtest: pd.DataFrame,
    cdi_mensal: pd.DataFrame | None,
) -> pd.DataFrame:
    """Alinha o CDI à base mensal do backtest."""

    dados = backtest.copy()

    if cdi_mensal is None:
        dados["retorno_cdi"] = 0.0
        dados["cdi_disponivel"] = False
        return dados

    dados = pd.merge(
        dados,
        cdi_mensal,
        on="data",
        how="left",
        validate="one_to_one",
    )

    dados["cdi_disponivel"] = (
        dados["retorno_cdi"].notna()
    )

    return dados


# ============================================================
# MÉTRICAS DE RISCO E RETORNO
# ============================================================

def calcular_indice_drawdown(
    retornos: pd.Series,
    valor_inicial: float,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Calcula índice, pico e drawdown incluindo o patrimônio inicial."""

    retornos = (
        pd.to_numeric(
            pd.Series(retornos),
            errors="coerce",
        )
        .replace(
            [
                np.inf,
                -np.inf,
            ],
            np.nan,
        )
        .dropna()
        .reset_index(drop=True)
    )

    indice = (
        valor_inicial
        * (
            1.0
            + retornos
        )
        .cumprod()
    )

    indice_com_inicio = pd.concat(
        [
            pd.Series(
                [valor_inicial],
                dtype=float,
            ),
            indice,
        ],
        ignore_index=True,
    )
    pico_com_inicio = indice_com_inicio.cummax()
    drawdown_com_inicio = (
        indice_com_inicio
        / pico_com_inicio
        - 1.0
    )

    return (
        indice,
        pico_com_inicio.iloc[1:].reset_index(drop=True),
        drawdown_com_inicio.iloc[1:].reset_index(drop=True),
    )


def calcular_metricas_backtest(
    retornos: pd.Series,
    *,
    periodos_por_ano: int,
    nivel_var: float,
    valor_inicial: float,
    retorno_livre_risco: pd.Series | None = None,
) -> dict[str, float]:
    """Calcula métricas completas de retorno e risco."""

    retornos = (
        pd.to_numeric(
            pd.Series(retornos),
            errors="coerce",
        )
        .replace(
            [
                np.inf,
                -np.inf,
            ],
            np.nan,
        )
    )

    if retorno_livre_risco is not None:
        retorno_livre_risco = pd.to_numeric(
            pd.Series(retorno_livre_risco),
            errors="coerce",
        )
        base = pd.concat(
            [
                retornos.rename("retorno"),
                retorno_livre_risco.rename("livre_risco"),
            ],
            axis=1,
        ).dropna()
        retornos_validos = base["retorno"]
        excesso = (
            (
                1.0 + base["retorno"]
            )
            / (
                1.0 + base["livre_risco"]
            )
            - 1.0
        )
    else:
        retornos_validos = retornos.dropna()
        excesso = retornos_validos.copy()

    retornos_validos = (
        retornos_validos.astype(float).reset_index(drop=True)
    )
    excesso = (
        excesso.astype(float).reset_index(drop=True)
    )

    quantidade_periodos = len(retornos_validos)

    if quantidade_periodos == 0:
        raise ValueError(
            "A série de retornos está vazia."
        )

    retorno_total = float(
        (
            1.0
            + retornos_validos
        ).prod()
        - 1.0
    )
    retorno_anualizado = float(
        (
            1.0
            + retorno_total
        )
        ** (
            periodos_por_ano
            / quantidade_periodos
        )
        - 1.0
    )
    volatilidade_anualizada = float(
        retornos_validos.std(ddof=1)
        * np.sqrt(periodos_por_ano)
    )

    retorno_volatilidade = (
        retorno_anualizado
        / volatilidade_anualizada
        if np.isfinite(volatilidade_anualizada)
        and volatilidade_anualizada > 0
        else np.nan
    )

    volatilidade_excesso = float(
        excesso.std(ddof=1)
        * np.sqrt(periodos_por_ano)
    )
    excesso_total = float(
        (
            1.0
            + excesso
        ).prod()
        - 1.0
    )
    excesso_anualizado = float(
        (
            1.0
            + excesso_total
        )
        ** (
            periodos_por_ano
            / len(excesso)
        )
        - 1.0
    )

    sharpe_excesso = (
        excesso_anualizado
        / volatilidade_excesso
        if np.isfinite(volatilidade_excesso)
        and volatilidade_excesso > 0
        else np.nan
    )

    _, _, drawdown = calcular_indice_drawdown(
        retornos_validos,
        valor_inicial,
    )
    maximo_drawdown = float(drawdown.min())

    calmar = (
        retorno_anualizado
        / abs(maximo_drawdown)
        if maximo_drawdown < 0
        else np.nan
    )

    retornos_negativos = np.minimum(
        retornos_validos.to_numpy(dtype=float),
        0.0,
    )
    desvio_negativo_anualizado = float(
        np.sqrt(
            np.mean(
                retornos_negativos ** 2
            )
        )
        * np.sqrt(periodos_por_ano)
    )
    sortino = (
        retorno_anualizado
        / desvio_negativo_anualizado
        if desvio_negativo_anualizado > 0
        else np.nan
    )

    quantil_var = 1.0 - nivel_var
    var_historico = float(
        retornos_validos.quantile(
            quantil_var
        )
    )
    cauda = retornos_validos.loc[
        retornos_validos.le(var_historico)
    ]
    cvar_historico = (
        float(cauda.mean())
        if not cauda.empty
        else np.nan
    )

    return {
        "quantidade_meses": float(quantidade_periodos),
        "retorno_total": retorno_total,
        "retorno_anualizado": retorno_anualizado,
        "retorno_medio_mensal": float(
            retornos_validos.mean()
        ),
        "retorno_mediano_mensal": float(
            retornos_validos.median()
        ),
        "volatilidade_anualizada": volatilidade_anualizada,
        "desvio_negativo_anualizado": (
            desvio_negativo_anualizado
        ),
        "retorno_sobre_volatilidade": retorno_volatilidade,
        "sharpe_excesso_cdi": sharpe_excesso,
        "sortino_alvo_zero": sortino,
        "maximo_drawdown": maximo_drawdown,
        "calmar": calmar,
        "meses_positivos": float(
            retornos_validos.gt(0).mean()
        ),
        "melhor_mes": float(
            retornos_validos.max()
        ),
        "pior_mes": float(
            retornos_validos.min()
        ),
        f"var_historico_{nivel_var:.0%}": var_historico,
        f"cvar_historico_{nivel_var:.0%}": cvar_historico,
    }


def criar_tabela_metricas(
    backtest: pd.DataFrame,
    *,
    periodos_por_ano: int,
    nivel_var: float,
    valor_inicial: float,
) -> pd.DataFrame:
    """Compara quatro séries: carteira e benchmark, bruto e líquido."""

    cdi = (
        backtest["retorno_cdi"]
        if backtest["cdi_disponivel"].all()
        else None
    )

    series = {
        "portfolio_regimes_bruto": "retorno_portfolio",
        "portfolio_regimes_liquido": "retorno_portfolio_liquido",
        "benchmark_estatico_bruto": "retorno_carteira_estatica",
        "benchmark_estatico_liquido": "retorno_estatica_liquido",
    }

    resultados: dict[str, dict[str, float]] = {}

    for nome, coluna in series.items():
        resultados[nome] = calcular_metricas_backtest(
            backtest[coluna],
            periodos_por_ano=periodos_por_ano,
            nivel_var=nivel_var,
            valor_inicial=valor_inicial,
            retorno_livre_risco=cdi,
        )

    metricas = list(
        next(iter(resultados.values())).keys()
    )

    return pd.DataFrame(
        [
            {
                "metrica": metrica,
                **{
                    nome: valores.get(metrica)
                    for nome, valores in resultados.items()
                },
            }
            for metrica in metricas
        ]
    )


def formatar_metricas(
    metricas: pd.DataFrame,
) -> pd.DataFrame:
    """Cria uma versão textual das métricas para leitura humana."""

    resultado = metricas.copy().astype(object)

    metricas_percentuais = {
        "retorno_total",
        "retorno_anualizado",
        "retorno_medio_mensal",
        "retorno_mediano_mensal",
        "volatilidade_anualizada",
        "desvio_negativo_anualizado",
        "maximo_drawdown",
        "meses_positivos",
        "melhor_mes",
        "pior_mes",
    }

    for indice, linha in metricas.iterrows():
        metrica = str(linha["metrica"])

        for coluna in metricas.columns:
            if coluna == "metrica":
                continue

            valor = linha[coluna]

            if pd.isna(valor):
                texto = "-"
            elif metrica == "quantidade_meses":
                texto = f"{int(valor)}"
            elif (
                metrica in metricas_percentuais
                or metrica.startswith("var_historico_")
                or metrica.startswith("cvar_historico_")
            ):
                texto = f"{valor:.2%}"
            else:
                texto = f"{valor:.4f}"

            resultado.loc[indice, coluna] = texto

    return resultado


# ============================================================
# DESEMPENHO E CONTRIBUIÇÃO POR REGIME
# ============================================================

def calcular_desempenho_por_regime(
    backtest: pd.DataFrame,
    ativos: list[str],
    periodos_por_ano: int,
    ordem_regimes: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula desempenho condicional e contribuição média por regime."""

    colunas_contribuicao = [
        f"contribuicao_{ativo}"
        for ativo in ativos
    ]

    colunas_ausentes = [
        coluna
        for coluna in colunas_contribuicao
        if coluna not in backtest.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            "Colunas de contribuição ausentes na base:\n"
            f"{colunas_ausentes}"
        )

    registros_desempenho: list[dict[str, Any]] = []
    registros_contribuicao: list[dict[str, Any]] = []

    regimes_presentes = (
        backtest["regime_sinal"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    ordem_final = [
        regime
        for regime in ordem_regimes
        if regime in regimes_presentes
    ] + [
        regime
        for regime in regimes_presentes
        if regime not in ordem_regimes
    ]

    for regime in ordem_final:
        grupo = (
            backtest.loc[
                backtest["regime_sinal"].eq(regime)
            ]
            .sort_values("data")
            .copy()
        )

        if grupo.empty:
            continue

        retorno_portfolio = grupo[
            "retorno_portfolio_liquido"
        ].astype(float)
        retorno_benchmark = grupo[
            "retorno_estatica_liquido"
        ].astype(float)

        quantidade = len(grupo)

        volatilidade_portfolio = (
            float(
                retorno_portfolio.std(ddof=1)
                * np.sqrt(periodos_por_ano)
            )
            if quantidade > 1
            else np.nan
        )
        volatilidade_benchmark = (
            float(
                retorno_benchmark.std(ddof=1)
                * np.sqrt(periodos_por_ano)
            )
            if quantidade > 1
            else np.nan
        )

        retorno_condicional_portfolio = float(
            (
                1.0
                + retorno_portfolio
            ).prod()
            - 1.0
        )
        retorno_condicional_benchmark = float(
            (
                1.0
                + retorno_benchmark
            ).prod()
            - 1.0
        )

        registros_desempenho.append(
            {
                "regime_sinal": regime,
                "quantidade_meses": quantidade,
                "retorno_bruto_medio_portfolio": float(
                    grupo["retorno_portfolio"].mean()
                ),
                "retorno_liquido_medio_portfolio": float(
                    retorno_portfolio.mean()
                ),
                "retorno_condicional_portfolio": (
                    retorno_condicional_portfolio
                ),
                "volatilidade_anualizada_portfolio": (
                    volatilidade_portfolio
                ),
                "meses_positivos_portfolio": float(
                    retorno_portfolio.gt(0).mean()
                ),
                "melhor_mes_portfolio": float(
                    retorno_portfolio.max()
                ),
                "pior_mes_portfolio": float(
                    retorno_portfolio.min()
                ),
                "retorno_bruto_medio_benchmark": float(
                    grupo["retorno_carteira_estatica"].mean()
                ),
                "retorno_liquido_medio_benchmark": float(
                    retorno_benchmark.mean()
                ),
                "retorno_condicional_benchmark": (
                    retorno_condicional_benchmark
                ),
                "volatilidade_anualizada_benchmark": (
                    volatilidade_benchmark
                ),
                "meses_positivos_benchmark": float(
                    retorno_benchmark.gt(0).mean()
                ),
                "melhor_mes_benchmark": float(
                    retorno_benchmark.max()
                ),
                "pior_mes_benchmark": float(
                    retorno_benchmark.min()
                ),
                "diferenca_retorno_liquido_medio": float(
                    retorno_portfolio.mean()
                    - retorno_benchmark.mean()
                ),
                "diferenca_retorno_condicional": float(
                    retorno_condicional_portfolio
                    - retorno_condicional_benchmark
                ),
            }
        )

        registro_contribuicao: dict[str, Any] = {
            "regime_sinal": regime,
        }

        for ativo, coluna in zip(
            ativos,
            colunas_contribuicao,
        ):
            registro_contribuicao[
                f"contribuicao_media_{ativo}"
            ] = float(
                grupo[coluna].mean()
            )

        registro_contribuicao[
            "soma_contribuicoes_medias"
        ] = float(
            grupo[colunas_contribuicao]
            .sum(axis=1)
            .mean()
        )
        registro_contribuicao[
            "retorno_bruto_medio_portfolio"
        ] = float(
            grupo["retorno_portfolio"].mean()
        )
        registro_contribuicao[
            "retorno_liquido_medio_portfolio"
        ] = float(
            retorno_portfolio.mean()
        )
        registro_contribuicao[
            "custo_medio_portfolio"
        ] = float(
            grupo["custo_portfolio"].mean()
        )

        registros_contribuicao.append(
            registro_contribuicao
        )

    desempenho = pd.DataFrame(
        registros_desempenho
    )
    contribuicao = pd.DataFrame(
        registros_contribuicao
    )

    if desempenho.empty or contribuicao.empty:
        raise ValueError(
            "Não foi possível calcular resultados por regime."
        )

    if not np.allclose(
        contribuicao["soma_contribuicoes_medias"],
        contribuicao["retorno_bruto_medio_portfolio"],
        atol=1e-10,
        rtol=1e-8,
    ):
        raise ValueError(
            "A soma das contribuições médias não coincide "
            "com o retorno bruto médio do portfólio."
        )

    return desempenho, contribuicao


# ============================================================
# SENSIBILIDADE AOS CUSTOS E BREAK-EVEN
# ============================================================

def simular_custo_transacao(
    dados: pd.DataFrame,
    taxa_custo: float,
    valor_inicial: float,
    periodos_por_ano: int,
) -> dict[str, float]:
    """Simula o índice final para uma taxa de custo por turnover."""

    taxa_custo = float(taxa_custo)

    if taxa_custo < 0:
        raise ValueError(
            "A taxa de custo não pode ser negativa."
        )

    fator_portfolio = (
        1.0
        - dados["turnover_portfolio"]
        * taxa_custo
    )
    fator_benchmark = (
        1.0
        - dados["turnover_estatica"]
        * taxa_custo
    )

    if (
        fator_portfolio.le(0).any()
        or fator_benchmark.le(0).any()
    ):
        raise ValueError(
            "O custo informado gerou fator patrimonial "
            "menor ou igual a zero."
        )

    retorno_liquido_portfolio = (
        (
            1.0
            + dados["retorno_portfolio"]
        )
        * fator_portfolio
        - 1.0
    )
    retorno_liquido_benchmark = (
        (
            1.0
            + dados["retorno_carteira_estatica"]
        )
        * fator_benchmark
        - 1.0
    )

    indice_final_portfolio = float(
        valor_inicial
        * (
            1.0
            + retorno_liquido_portfolio
        ).prod()
    )
    indice_final_benchmark = float(
        valor_inicial
        * (
            1.0
            + retorno_liquido_benchmark
        ).prod()
    )

    quantidade_meses = len(dados)

    retorno_total_portfolio = (
        indice_final_portfolio
        / valor_inicial
        - 1.0
    )
    retorno_total_benchmark = (
        indice_final_benchmark
        / valor_inicial
        - 1.0
    )

    return {
        "taxa_custo": taxa_custo,
        "custo_bps": taxa_custo * 10000.0,
        "indice_final_portfolio": indice_final_portfolio,
        "indice_final_benchmark": indice_final_benchmark,
        "diferenca_indice_final": (
            indice_final_portfolio
            - indice_final_benchmark
        ),
        "retorno_total_portfolio": (
            retorno_total_portfolio
        ),
        "retorno_total_benchmark": (
            retorno_total_benchmark
        ),
        "retorno_anualizado_portfolio": (
            (
                1.0
                + retorno_total_portfolio
            )
            ** (
                periodos_por_ano
                / quantidade_meses
            )
            - 1.0
        ),
        "retorno_anualizado_benchmark": (
            (
                1.0
                + retorno_total_benchmark
            )
            ** (
                periodos_por_ano
                / quantidade_meses
            )
            - 1.0
        ),
    }


def calcular_sensibilidade_custos(
    backtest: pd.DataFrame,
    *,
    cenarios: list[float],
    custo_base: float,
    limite_inferior: float,
    limite_superior: float,
    maximo_iteracoes: int,
    tolerancia: float,
    valor_inicial: float,
    periodos_por_ano: int,
) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    """Executa cenários de custo e estima o break-even por bisseção."""

    cenarios_array = np.asarray(
        cenarios,
        dtype=float,
    )

    if cenarios_array.size == 0:
        raise ValueError(
            "A lista de cenários de custo está vazia."
        )

    if (cenarios_array < 0).any():
        raise ValueError(
            "A lista de cenários possui custos negativos."
        )

    resultados = [
        simular_custo_transacao(
            dados=backtest,
            taxa_custo=float(custo),
            valor_inicial=valor_inicial,
            periodos_por_ano=periodos_por_ano,
        )
        for custo in sorted(
            set(cenarios_array.tolist())
        )
    ]

    sensibilidade = pd.DataFrame(
        resultados
    )

    def diferenca(custo: float) -> float:
        return float(
            simular_custo_transacao(
                dados=backtest,
                taxa_custo=custo,
                valor_inicial=valor_inicial,
                periodos_por_ano=periodos_por_ano,
            )["diferenca_indice_final"]
        )

    inferior = float(limite_inferior)
    superior = float(limite_superior)

    if inferior < 0 or superior <= inferior:
        raise ValueError(
            "Os limites do break-even são inválidos."
        )

    diferenca_inferior = diferenca(inferior)
    diferenca_superior = diferenca(superior)

    if np.isclose(
        diferenca_inferior,
        0.0,
        atol=tolerancia,
    ):
        break_even = inferior

    elif (
        diferenca_inferior
        * diferenca_superior
        < 0
    ):
        for _ in range(maximo_iteracoes):
            meio = (
                inferior
                + superior
            ) / 2.0
            diferenca_meio = diferenca(meio)

            if np.isclose(
                diferenca_meio,
                0.0,
                atol=tolerancia,
            ):
                inferior = meio
                superior = meio
                break

            if (
                diferenca_inferior
                * diferenca_meio
                <= 0
            ):
                superior = meio
                diferenca_superior = diferenca_meio
            else:
                inferior = meio
                diferenca_inferior = diferenca_meio

        break_even = (
            inferior
            + superior
        ) / 2.0

    else:
        break_even = np.nan

    resultado_base = simular_custo_transacao(
        dados=backtest,
        taxa_custo=custo_base,
        valor_inicial=valor_inicial,
        periodos_por_ano=periodos_por_ano,
    )

    resumo = pd.DataFrame(
        [
            {
                "custo_base": custo_base,
                "custo_base_bps": custo_base * 10000.0,
                "custo_break_even": break_even,
                "custo_break_even_bps": (
                    break_even * 10000.0
                    if pd.notna(break_even)
                    else np.nan
                ),
                "indice_final_portfolio_custo_base": (
                    resultado_base[
                        "indice_final_portfolio"
                    ]
                ),
                "indice_final_benchmark_custo_base": (
                    resultado_base[
                        "indice_final_benchmark"
                    ]
                ),
                "diferenca_final_custo_base": (
                    resultado_base[
                        "diferenca_indice_final"
                    ]
                ),
                "limite_inferior_testado": limite_inferior,
                "limite_superior_testado": limite_superior,
            }
        ]
    )

    return sensibilidade, resumo, float(break_even)


# ============================================================
# ROBUSTEZ TEMPORAL
# ============================================================

def retorno_composto(
    serie: pd.Series,
) -> float:
    """Calcula retorno composto de uma série."""

    valores = (
        pd.to_numeric(
            serie,
            errors="coerce",
        )
        .dropna()
    )

    if valores.empty:
        return np.nan

    return float(
        (
            1.0
            + valores
        ).prod()
        - 1.0
    )


def calcular_robustez_temporal(
    backtest: pd.DataFrame,
    periodos_por_ano: int,
    periodos_janela: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula resultados anuais e métricas em janelas móveis."""

    dados = (
        backtest[
            [
                "data",
                "retorno_portfolio",
                "retorno_portfolio_liquido",
                "retorno_carteira_estatica",
                "retorno_estatica_liquido",
            ]
        ]
        .copy()
        .sort_values("data")
        .reset_index(drop=True)
    )

    dados["ano"] = dados["data"].dt.year

    resultados_anuais = (
        dados.groupby(
            "ano",
            as_index=False,
        )
        .agg(
            quantidade_meses=(
                "data",
                "count",
            ),
            retorno_portfolio_bruto=(
                "retorno_portfolio",
                retorno_composto,
            ),
            retorno_portfolio_liquido=(
                "retorno_portfolio_liquido",
                retorno_composto,
            ),
            retorno_benchmark_bruto=(
                "retorno_carteira_estatica",
                retorno_composto,
            ),
            retorno_benchmark_liquido=(
                "retorno_estatica_liquido",
                retorno_composto,
            ),
        )
    )

    resultados_anuais["diferenca_liquida"] = (
        resultados_anuais[
            "retorno_portfolio_liquido"
        ]
        - resultados_anuais[
            "retorno_benchmark_liquido"
        ]
    )
    resultados_anuais[
        "portfolio_superou_benchmark"
    ] = (
        resultados_anuais[
            "diferenca_liquida"
        ]
        > 0
    )
    resultados_anuais["ano_completo"] = (
        resultados_anuais[
            "quantidade_meses"
        ]
        == periodos_por_ano
    )

    metricas_moveis = dados[
        [
            "data",
            "retorno_portfolio_liquido",
            "retorno_estatica_liquido",
        ]
    ].copy()

    metricas_moveis[
        "retorno_movel_portfolio"
    ] = (
        metricas_moveis[
            "retorno_portfolio_liquido"
        ]
        .rolling(
            window=periodos_janela,
            min_periods=periodos_janela,
        )
        .apply(
            lambda valores: (
                np.prod(
                    1.0
                    + valores
                )
                - 1.0
            ),
            raw=True,
        )
    )
    metricas_moveis[
        "retorno_movel_benchmark"
    ] = (
        metricas_moveis[
            "retorno_estatica_liquido"
        ]
        .rolling(
            window=periodos_janela,
            min_periods=periodos_janela,
        )
        .apply(
            lambda valores: (
                np.prod(
                    1.0
                    + valores
                )
                - 1.0
            ),
            raw=True,
        )
    )
    metricas_moveis[
        "volatilidade_movel_portfolio"
    ] = (
        metricas_moveis[
            "retorno_portfolio_liquido"
        ]
        .rolling(
            window=periodos_janela,
            min_periods=periodos_janela,
        )
        .std(ddof=1)
        * np.sqrt(periodos_por_ano)
    )
    metricas_moveis[
        "volatilidade_movel_benchmark"
    ] = (
        metricas_moveis[
            "retorno_estatica_liquido"
        ]
        .rolling(
            window=periodos_janela,
            min_periods=periodos_janela,
        )
        .std(ddof=1)
        * np.sqrt(periodos_por_ano)
    )
    metricas_moveis[
        "diferenca_retorno_movel"
    ] = (
        metricas_moveis[
            "retorno_movel_portfolio"
        ]
        - metricas_moveis[
            "retorno_movel_benchmark"
        ]
    )
    metricas_moveis[
        "diferenca_volatilidade_movel"
    ] = (
        metricas_moveis[
            "volatilidade_movel_portfolio"
        ]
        - metricas_moveis[
            "volatilidade_movel_benchmark"
        ]
    )
    metricas_moveis[
        "portfolio_superou_janela"
    ] = (
        metricas_moveis[
            "diferenca_retorno_movel"
        ]
        > 0
    )

    return resultados_anuais, metricas_moveis


# ============================================================
# RESUMOS E VALIDAÇÕES FINAIS
# ============================================================

def criar_resumo_turnover_custos(
    backtest: pd.DataFrame,
    custo_por_turnover: float,
) -> pd.DataFrame:
    """Cria o resumo comparativo de turnover e custos."""

    return pd.DataFrame(
        [
            {
                "metrica": "custo_por_unidade_turnover",
                "portfolio_regimes": custo_por_turnover,
                "benchmark_estatico": custo_por_turnover,
            },
            {
                "metrica": "turnover_total",
                "portfolio_regimes": (
                    backtest["turnover_portfolio"].sum()
                ),
                "benchmark_estatico": (
                    backtest["turnover_estatica"].sum()
                ),
            },
            {
                "metrica": "turnover_medio_mensal",
                "portfolio_regimes": (
                    backtest["turnover_portfolio"].mean()
                ),
                "benchmark_estatico": (
                    backtest["turnover_estatica"].mean()
                ),
            },
            {
                "metrica": "custo_acumulado_simples",
                "portfolio_regimes": (
                    backtest["custo_portfolio"].sum()
                ),
                "benchmark_estatico": (
                    backtest["custo_estatica"].sum()
                ),
            },
            {
                "metrica": "indice_final_bruto",
                "portfolio_regimes": (
                    backtest["indice_portfolio_bruto"].iloc[-1]
                ),
                "benchmark_estatico": (
                    backtest["indice_estatica_bruto"].iloc[-1]
                ),
            },
            {
                "metrica": "indice_final_liquido",
                "portfolio_regimes": (
                    backtest["indice_portfolio_liquido"].iloc[-1]
                ),
                "benchmark_estatico": (
                    backtest["indice_estatica_liquido"].iloc[-1]
                ),
            },
            {
                "metrica": "impacto_final_custos",
                "portfolio_regimes": (
                    backtest["indice_portfolio_bruto"].iloc[-1]
                    - backtest["indice_portfolio_liquido"].iloc[-1]
                ),
                "benchmark_estatico": (
                    backtest["indice_estatica_bruto"].iloc[-1]
                    - backtest["indice_estatica_liquido"].iloc[-1]
                ),
            },
        ]
    )


def criar_resumo_final(
    metricas: pd.DataFrame,
    backtest: pd.DataFrame,
    custo_break_even: float,
    resultados_anuais: pd.DataFrame,
    metricas_moveis: pd.DataFrame,
    periodos_janela: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cria o resumo final e o diagnóstico da estratégia."""

    coluna_portfolio = "portfolio_regimes_liquido"
    coluna_benchmark = "benchmark_estatico_liquido"

    metricas_resumo = [
        "quantidade_meses",
        "retorno_total",
        "retorno_anualizado",
        "volatilidade_anualizada",
        "retorno_sobre_volatilidade",
        "sharpe_excesso_cdi",
        "sortino_alvo_zero",
        "maximo_drawdown",
        "calmar",
        "meses_positivos",
        "melhor_mes",
        "pior_mes",
    ]

    resumo = metricas.loc[
        metricas["metrica"].isin(
            metricas_resumo
        ),
        [
            "metrica",
            coluna_portfolio,
            coluna_benchmark,
        ],
    ].copy()

    resumo = resumo.rename(
        columns={
            coluna_portfolio: "portfolio_regimes",
            coluna_benchmark: "benchmark_estatico",
        }
    )

    adicionais = pd.DataFrame(
        [
            {
                "metrica": "turnover_total",
                "portfolio_regimes": (
                    backtest["turnover_portfolio"].sum()
                ),
                "benchmark_estatico": (
                    backtest["turnover_estatica"].sum()
                ),
            },
            {
                "metrica": "turnover_medio_mensal",
                "portfolio_regimes": (
                    backtest["turnover_portfolio"].mean()
                ),
                "benchmark_estatico": (
                    backtest["turnover_estatica"].mean()
                ),
            },
            {
                "metrica": "custo_acumulado_simples",
                "portfolio_regimes": (
                    backtest["custo_portfolio"].sum()
                ),
                "benchmark_estatico": (
                    backtest["custo_estatica"].sum()
                ),
            },
            {
                "metrica": "indice_final_bruto",
                "portfolio_regimes": (
                    backtest["indice_portfolio_bruto"].iloc[-1]
                ),
                "benchmark_estatico": (
                    backtest["indice_estatica_bruto"].iloc[-1]
                ),
            },
            {
                "metrica": "indice_final_liquido",
                "portfolio_regimes": (
                    backtest["indice_portfolio_liquido"].iloc[-1]
                ),
                "benchmark_estatico": (
                    backtest["indice_estatica_liquido"].iloc[-1]
                ),
            },
        ]
    )

    resumo = pd.concat(
        [
            resumo,
            adicionais,
        ],
        ignore_index=True,
    )

    diferenca_bruta = float(
        backtest["indice_portfolio_bruto"].iloc[-1]
        - backtest["indice_estatica_bruto"].iloc[-1]
    )
    diferenca_liquida = float(
        backtest["indice_portfolio_liquido"].iloc[-1]
        - backtest["indice_estatica_liquido"].iloc[-1]
    )

    anos_completos = resultados_anuais.loc[
        resultados_anuais["ano_completo"]
    ]
    quantidade_anos = len(anos_completos)
    quantidade_anos_superiores = int(
        anos_completos[
            "portfolio_superou_benchmark"
        ].sum()
    )
    proporcao_anos = (
        quantidade_anos_superiores
        / quantidade_anos
        if quantidade_anos > 0
        else np.nan
    )

    janelas = (
        metricas_moveis[
            "diferenca_retorno_movel"
        ]
        .dropna()
    )

    proporcao_janelas = (
        float(janelas.gt(0).mean())
        if not janelas.empty
        else np.nan
    )
    maior_vantagem = (
        float(janelas.max())
        if not janelas.empty
        else np.nan
    )
    pior_desvantagem = (
        float(janelas.min())
        if not janelas.empty
        else np.nan
    )

    if diferenca_liquida > 0:
        conclusao = (
            "O portfólio por regimes superou o benchmark "
            "após os custos."
        )
    elif diferenca_liquida < 0:
        conclusao = (
            "O portfólio por regimes ficou abaixo do benchmark "
            "após os custos."
        )
    else:
        conclusao = (
            "O portfólio por regimes empatou com o benchmark "
            "após os custos."
        )

    diagnostico = pd.DataFrame(
        [
            {
                "diferenca_final_bruta_pontos": diferenca_bruta,
                "diferenca_final_liquida_pontos": diferenca_liquida,
                "custo_break_even": custo_break_even,
                "custo_break_even_bps": (
                    custo_break_even * 10000.0
                    if pd.notna(custo_break_even)
                    else np.nan
                ),
                "quantidade_anos_completos": quantidade_anos,
                "quantidade_anos_superiores": (
                    quantidade_anos_superiores
                ),
                "proporcao_anos_superiores": proporcao_anos,
                f"proporcao_janelas_{periodos_janela}m_superiores": (
                    proporcao_janelas
                ),
                f"maior_vantagem_{periodos_janela}m": (
                    maior_vantagem
                ),
                f"pior_desvantagem_{periodos_janela}m": (
                    pior_desvantagem
                ),
                "conclusao": conclusao,
            }
        ]
    )

    return resumo, diagnostico


def criar_validacoes_finais(
    backtest: pd.DataFrame,
    colunas_pesos: list[str],
    tolerancia: float,
) -> pd.DataFrame:
    """Executa as verificações finais do backtest."""

    retorno_portfolio_recalculado = (
        (
            1.0
            + backtest["retorno_portfolio"]
        )
        * (
            1.0
            - backtest["custo_portfolio"]
        )
        - 1.0
    )
    retorno_benchmark_recalculado = (
        (
            1.0
            + backtest["retorno_carteira_estatica"]
        )
        * (
            1.0
            - backtest["custo_estatica"]
        )
        - 1.0
    )

    colunas_principais = [
        "data",
        "regime_sinal",
        "retorno_portfolio",
        "retorno_portfolio_liquido",
        "retorno_carteira_estatica",
        "retorno_estatica_liquido",
        "turnover_portfolio",
        "turnover_estatica",
        "custo_portfolio",
        "custo_estatica",
        "indice_portfolio_bruto",
        "indice_portfolio_liquido",
        "indice_estatica_bruto",
        "indice_estatica_liquido",
        *colunas_pesos,
    ]

    validacoes = [
        {
            "validacao": "Base possui registros",
            "resultado": not backtest.empty,
            "detalhe": f"{len(backtest)} meses",
        },
        {
            "validacao": "Datas válidas",
            "resultado": not backtest["data"].isna().any(),
            "detalhe": "Nenhuma data inválida",
        },
        {
            "validacao": "Datas sem duplicidade",
            "resultado": not backtest["data"].duplicated().any(),
            "detalhe": (
                f"{int(backtest['data'].duplicated().sum())} "
                "duplicidades"
            ),
        },
        {
            "validacao": "Datas em ordem crescente",
            "resultado": backtest["data"].is_monotonic_increasing,
            "detalhe": "Ordenação temporal validada",
        },
        {
            "validacao": "Sem nulos nas colunas principais",
            "resultado": not backtest[
                colunas_principais
            ].isna().any().any(),
            "detalhe": (
                f"{int(backtest[colunas_principais].isna().sum().sum())} "
                "valores nulos"
            ),
        },
        {
            "validacao": "Pesos somam 100%",
            "resultado": np.allclose(
                backtest[colunas_pesos].sum(axis=1),
                1.0,
                atol=tolerancia,
                rtol=0.0,
            ),
            "detalhe": (
                f"Mínimo {backtest[colunas_pesos].sum(axis=1).min():.12f} | "
                f"Máximo {backtest[colunas_pesos].sum(axis=1).max():.12f}"
            ),
        },
        {
            "validacao": "Turnover não negativo",
            "resultado": backtest[
                [
                    "turnover_portfolio",
                    "turnover_estatica",
                ]
            ].ge(0).all().all(),
            "detalhe": "Turnovers mensais verificados",
        },
        {
            "validacao": "Custos não negativos",
            "resultado": backtest[
                [
                    "custo_portfolio",
                    "custo_estatica",
                ]
            ].ge(0).all().all(),
            "detalhe": "Custos mensais verificados",
        },
        {
            "validacao": "Retorno líquido do portfólio consistente",
            "resultado": np.allclose(
                backtest["retorno_portfolio_liquido"],
                retorno_portfolio_recalculado,
                atol=1e-12,
                rtol=1e-10,
            ),
            "detalhe": "Fórmula de custos validada",
        },
        {
            "validacao": "Retorno líquido do benchmark consistente",
            "resultado": np.allclose(
                backtest["retorno_estatica_liquido"],
                retorno_benchmark_recalculado,
                atol=1e-12,
                rtol=1e-10,
            ),
            "detalhe": "Fórmula de custos validada",
        },
        {
            "validacao": "Índices finais positivos",
            "resultado": backtest[
                [
                    "indice_portfolio_bruto",
                    "indice_portfolio_liquido",
                    "indice_estatica_bruto",
                    "indice_estatica_liquido",
                ]
            ].iloc[-1].gt(0).all(),
            "detalhe": "Patrimônios finais maiores que zero",
        },
    ]

    resultado = pd.DataFrame(
        validacoes
    )
    resultado["status"] = np.where(
        resultado["resultado"],
        "APROVADO",
        "REPROVADO",
    )

    return resultado[
        [
            "validacao",
            "status",
            "detalhe",
            "resultado",
        ]
    ]


# ============================================================
# GRÁFICOS
# ============================================================

def gerar_graficos_backtest(
    backtest: pd.DataFrame,
    desempenho_regimes: pd.DataFrame,
    contribuicao_regimes: pd.DataFrame,
    sensibilidade: pd.DataFrame,
    custo_base: float,
    custo_break_even: float,
    resultados_anuais: pd.DataFrame,
    metricas_moveis: pd.DataFrame,
    ativos: list[str],
    valor_inicial: float,
    periodos_janela: int,
    pasta_graficos: Path,
    dpi: int,
) -> list[Path]:
    """Gera todos os gráficos do backtest."""

    pasta_graficos.mkdir(
        parents=True,
        exist_ok=True,
    )
    arquivos: list[Path] = []

    data_inicial = (
        backtest["data"].iloc[0]
        - pd.offsets.MonthEnd(1)
    )
    linha_inicial = pd.DataFrame(
        [
            {
                "data": data_inicial,
                "indice_portfolio_bruto": valor_inicial,
                "indice_portfolio_liquido": valor_inicial,
                "indice_estatica_bruto": valor_inicial,
                "indice_estatica_liquido": valor_inicial,
                "drawdown_portfolio_liquido": 0.0,
                "drawdown_estatica_liquida": 0.0,
                "turnover_portfolio": 0.0,
                "turnover_estatica": 0.0,
            }
        ]
    )
    series_inicio = pd.concat(
        [
            linha_inicial,
            backtest[
                [
                    "data",
                    "indice_portfolio_bruto",
                    "indice_portfolio_liquido",
                    "indice_estatica_bruto",
                    "indice_estatica_liquido",
                    "drawdown_portfolio_liquido",
                    "drawdown_estatica_liquida",
                    "turnover_portfolio",
                    "turnover_estatica",
                ]
            ],
        ],
        ignore_index=True,
    )

    arquivo = (
        pasta_graficos
        / "05_desempenho_bruto_liquido.png"
    )
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.plot(
        series_inicio["data"],
        series_inicio["indice_portfolio_bruto"],
        label="Portfólio por regimes — bruto",
    )
    ax.plot(
        series_inicio["data"],
        series_inicio["indice_portfolio_liquido"],
        label="Portfólio por regimes — líquido",
        linestyle="--",
    )
    ax.plot(
        series_inicio["data"],
        series_inicio["indice_estatica_bruto"],
        label="Benchmark estático — bruto",
    )
    ax.plot(
        series_inicio["data"],
        series_inicio["indice_estatica_liquido"],
        label="Benchmark estático — líquido",
        linestyle="--",
    )
    ax.axhline(y=valor_inicial, linewidth=1)
    ax.set_title("Desempenho Bruto e Líquido")
    ax.set_xlabel("Data")
    ax.set_ylabel("Índice acumulado")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    arquivo = (
        pasta_graficos
        / "05_drawdown_liquido.png"
    )
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(
        series_inicio["data"],
        series_inicio["drawdown_portfolio_liquido"],
        label="Portfólio por regimes — líquido",
    )
    ax.plot(
        series_inicio["data"],
        series_inicio["drawdown_estatica_liquida"],
        label="Benchmark estático — líquido",
    )
    ax.axhline(y=0.0, linewidth=1)
    ax.yaxis.set_major_formatter(
        PercentFormatter(xmax=1.0)
    )
    ax.set_title("Drawdown Líquido")
    ax.set_xlabel("Data")
    ax.set_ylabel("Drawdown")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    impacto = backtest[
        [
            "data",
            "indice_portfolio_bruto",
            "indice_portfolio_liquido",
            "indice_estatica_bruto",
            "indice_estatica_liquido",
        ]
    ].copy()
    impacto["portfolio"] = (
        impacto["indice_portfolio_bruto"]
        - impacto["indice_portfolio_liquido"]
    )
    impacto["benchmark"] = (
        impacto["indice_estatica_bruto"]
        - impacto["indice_estatica_liquido"]
    )

    arquivo = (
        pasta_graficos
        / "05_impacto_acumulado_custos.png"
    )
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(
        impacto["data"],
        impacto["portfolio"],
        label="Portfólio por regimes",
    )
    ax.plot(
        impacto["data"],
        impacto["benchmark"],
        label="Benchmark estático",
    )
    ax.axhline(y=0.0, linewidth=1)
    ax.set_title("Impacto Acumulado dos Custos")
    ax.set_xlabel("Data")
    ax.set_ylabel("Redução do índice em pontos")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    arquivo = (
        pasta_graficos
        / "05_turnover_mensal.png"
    )
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(
        backtest["data"],
        backtest["turnover_portfolio"],
        label="Portfólio por regimes",
    )
    ax.plot(
        backtest["data"],
        backtest["turnover_estatica"],
        label="Benchmark estático",
    )
    ax.yaxis.set_major_formatter(
        PercentFormatter(xmax=1.0)
    )
    ax.set_title("Turnover Mensal")
    ax.set_xlabel("Data")
    ax.set_ylabel("Turnover")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    posicoes = np.arange(
        len(desempenho_regimes)
    )
    largura = 0.36

    arquivo = (
        pasta_graficos
        / "05_retorno_liquido_medio_por_regime.png"
    )
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.bar(
        posicoes - largura / 2,
        desempenho_regimes[
            "retorno_liquido_medio_portfolio"
        ],
        width=largura,
        label="Portfólio por regimes",
    )
    ax.bar(
        posicoes + largura / 2,
        desempenho_regimes[
            "retorno_liquido_medio_benchmark"
        ],
        width=largura,
        label="Benchmark estático",
    )
    ax.axhline(y=0.0, linewidth=1)
    ax.set_xticks(posicoes)
    ax.set_xticklabels(
        desempenho_regimes[
            "regime_sinal"
        ].str.replace(
            "_",
            " ",
            regex=False,
        ),
        rotation=15,
        ha="right",
    )
    ax.yaxis.set_major_formatter(
        PercentFormatter(xmax=1.0)
    )
    ax.set_title(
        "Retorno Líquido Médio Mensal por Regime"
    )
    ax.set_xlabel("Regime utilizado na alocação")
    ax.set_ylabel("Retorno líquido médio mensal")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    arquivo = (
        pasta_graficos
        / "05_contribuicao_media_por_regime.png"
    )
    fig, ax = plt.subplots(figsize=(14, 7))
    posicoes = np.arange(
        len(contribuicao_regimes)
    )
    largura_total = 0.80
    largura_ativo = largura_total / len(ativos)

    for indice, ativo in enumerate(ativos):
        deslocamento = (
            indice
            - (
                len(ativos)
                - 1
            )
            / 2
        ) * largura_ativo
        ax.bar(
            posicoes + deslocamento,
            contribuicao_regimes[
                f"contribuicao_media_{ativo}"
            ],
            width=largura_ativo,
            label=ativo,
        )

    ax.axhline(y=0.0, linewidth=1)
    ax.set_xticks(posicoes)
    ax.set_xticklabels(
        contribuicao_regimes[
            "regime_sinal"
        ].str.replace(
            "_",
            " ",
            regex=False,
        ),
        rotation=15,
        ha="right",
    )
    ax.yaxis.set_major_formatter(
        PercentFormatter(xmax=1.0)
    )
    ax.set_title(
        "Contribuição Média Mensal dos Ativos por Regime"
    )
    ax.set_xlabel("Regime utilizado na alocação")
    ax.set_ylabel("Contribuição média mensal")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    arquivo = (
        pasta_graficos
        / "05_indice_final_por_custo.png"
    )
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(
        sensibilidade["custo_bps"],
        sensibilidade["indice_final_portfolio"],
        marker="o",
        label="Portfólio por regimes",
    )
    ax.plot(
        sensibilidade["custo_bps"],
        sensibilidade["indice_final_benchmark"],
        marker="o",
        label="Benchmark estático",
    )
    ax.axvline(
        x=custo_base * 10000.0,
        linestyle="--",
        linewidth=1,
        label="Custo-base",
    )
    if pd.notna(custo_break_even):
        ax.axvline(
            x=custo_break_even * 10000.0,
            linestyle=":",
            linewidth=1,
            label="Break-even",
        )
    ax.set_title(
        "Sensibilidade do Índice Final aos Custos"
    )
    ax.set_xlabel(
        "Custo por unidade de turnover (bps)"
    )
    ax.set_ylabel("Índice final")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    arquivo = (
        pasta_graficos
        / "05_vantagem_liquida_por_custo.png"
    )
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(
        sensibilidade["custo_bps"],
        sensibilidade["diferenca_indice_final"],
        marker="o",
    )
    ax.axhline(y=0.0, linewidth=1)
    ax.axvline(
        x=custo_base * 10000.0,
        linestyle="--",
        linewidth=1,
        label="Custo-base",
    )
    if pd.notna(custo_break_even):
        ax.axvline(
            x=custo_break_even * 10000.0,
            linestyle=":",
            linewidth=1,
            label="Break-even",
        )
    ax.set_title(
        "Vantagem Líquida do Portfólio por Regimes"
    )
    ax.set_xlabel(
        "Custo por unidade de turnover (bps)"
    )
    ax.set_ylabel("Diferença do índice final")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    arquivo = (
        pasta_graficos
        / "05_retornos_liquidos_anuais.png"
    )
    posicoes = np.arange(
        len(resultados_anuais)
    )
    largura = 0.36
    rotulos = [
        (
            str(int(ano))
            if completo
            else f"{int(ano)}*"
        )
        for ano, completo in zip(
            resultados_anuais["ano"],
            resultados_anuais["ano_completo"],
        )
    ]
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.bar(
        posicoes - largura / 2,
        resultados_anuais[
            "retorno_portfolio_liquido"
        ],
        width=largura,
        label="Portfólio por regimes",
    )
    ax.bar(
        posicoes + largura / 2,
        resultados_anuais[
            "retorno_benchmark_liquido"
        ],
        width=largura,
        label="Benchmark estático",
    )
    ax.axhline(y=0.0, linewidth=1)
    ax.set_xticks(posicoes)
    ax.set_xticklabels(rotulos)
    ax.yaxis.set_major_formatter(
        PercentFormatter(xmax=1.0)
    )
    ax.set_title("Retornos Líquidos por Ano")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Retorno acumulado no ano")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    arquivo = (
        pasta_graficos
        / f"05_retorno_movel_{periodos_janela}m.png"
    )
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.plot(
        metricas_moveis["data"],
        metricas_moveis["retorno_movel_portfolio"],
        label="Portfólio por regimes",
    )
    ax.plot(
        metricas_moveis["data"],
        metricas_moveis["retorno_movel_benchmark"],
        label="Benchmark estático",
    )
    ax.axhline(y=0.0, linewidth=1)
    ax.yaxis.set_major_formatter(
        PercentFormatter(xmax=1.0)
    )
    ax.set_title(
        f"Retorno Líquido Móvel de {periodos_janela} Meses"
    )
    ax.set_xlabel("Data")
    ax.set_ylabel("Retorno acumulado")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    arquivo = (
        pasta_graficos
        / f"05_volatilidade_movel_{periodos_janela}m.png"
    )
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.plot(
        metricas_moveis["data"],
        metricas_moveis["volatilidade_movel_portfolio"],
        label="Portfólio por regimes",
    )
    ax.plot(
        metricas_moveis["data"],
        metricas_moveis["volatilidade_movel_benchmark"],
        label="Benchmark estático",
    )
    ax.yaxis.set_major_formatter(
        PercentFormatter(xmax=1.0)
    )
    ax.set_title(
        "Volatilidade Móvel Anualizada — "
        f"{periodos_janela} Meses"
    )
    ax.set_xlabel("Data")
    ax.set_ylabel("Volatilidade anualizada")
    ax.legend()
    ax.grid(alpha=0.3)
    salvar_figura(fig, arquivo, dpi)
    arquivos.append(arquivo)

    return arquivos


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main() -> None:
    """Executa o backtest completo, líquido e auditável."""

    inicio_execucao = datetime.now(timezone.utc)
    configuracao = carregar_configuracao()

    backtest_config = obter_valor(
        configuracao,
        ("backtest",),
    )

    base, ativos, colunas_pesos, arquivo_entrada = (
        carregar_base_alocacao(
            configuracao
        )
    )

    custo_por_turnover = float(
        backtest_config["custo_por_turnover"]
    )
    cobrar_custo_inicial = bool(
        backtest_config["cobrar_custo_inicial"]
    )
    periodos_por_ano = int(
        backtest_config["periodos_por_ano"]
    )
    nivel_var = float(
        backtest_config["nivel_var"]
    )
    valor_inicial = float(
        backtest_config["valor_inicial"]
    )
    periodos_janela = int(
        backtest_config["periodos_janela"]
    )

    if periodos_por_ano <= 0:
        raise ValueError(
            "backtest.periodos_por_ano deve ser positivo."
        )
    if not 0 < nivel_var < 1:
        raise ValueError(
            "backtest.nivel_var deve estar entre 0 e 1."
        )
    if periodos_janela <= 0:
        raise ValueError(
            "backtest.periodos_janela deve ser positivo."
        )

    backtest = aplicar_custos(
        base=base,
        ativos=ativos,
        colunas_pesos=colunas_pesos,
        custo_por_turnover=custo_por_turnover,
        cobrar_custo_inicial=cobrar_custo_inicial,
        valor_inicial=valor_inicial,
    )

    cdi_mensal, arquivo_cdi = carregar_cdi_mensal(
        configuracao
    )
    backtest = adicionar_cdi(
        backtest,
        cdi_mensal,
    )

    metricas = criar_tabela_metricas(
        backtest,
        periodos_por_ano=periodos_por_ano,
        nivel_var=nivel_var,
        valor_inicial=valor_inicial,
    )
    metricas_formatadas = formatar_metricas(
        metricas
    )

    ordem_regimes = [
        str(regime).strip().upper()
        for regime in obter_valor(
            configuracao,
            ("regimes", "lista"),
            obrigatorio=False,
            padrao=[],
        )
    ]

    desempenho_regimes, contribuicao_regimes = (
        calcular_desempenho_por_regime(
            backtest=backtest,
            ativos=ativos,
            periodos_por_ano=periodos_por_ano,
            ordem_regimes=ordem_regimes,
        )
    )

    sensibilidade, resumo_break_even, custo_break_even = (
        calcular_sensibilidade_custos(
            backtest=backtest,
            cenarios=list(
                backtest_config["cenarios_custo"]
            ),
            custo_base=custo_por_turnover,
            limite_inferior=float(
                backtest_config[
                    "limite_inferior_break_even"
                ]
            ),
            limite_superior=float(
                backtest_config[
                    "limite_superior_break_even"
                ]
            ),
            maximo_iteracoes=int(
                backtest_config[
                    "maximo_iteracoes_break_even"
                ]
            ),
            tolerancia=float(
                backtest_config[
                    "tolerancia_break_even"
                ]
            ),
            valor_inicial=valor_inicial,
            periodos_por_ano=periodos_por_ano,
        )
    )

    resultados_anuais, metricas_moveis = (
        calcular_robustez_temporal(
            backtest=backtest,
            periodos_por_ano=periodos_por_ano,
            periodos_janela=periodos_janela,
        )
    )

    resumo_turnover = criar_resumo_turnover_custos(
        backtest=backtest,
        custo_por_turnover=custo_por_turnover,
    )

    resumo_final, diagnostico_final = criar_resumo_final(
        metricas=metricas,
        backtest=backtest,
        custo_break_even=custo_break_even,
        resultados_anuais=resultados_anuais,
        metricas_moveis=metricas_moveis,
        periodos_janela=periodos_janela,
    )

    tolerancia_pesos = float(
        obter_valor(
            configuracao,
            ("portfolio", "tolerancia_soma_pesos"),
            obrigatorio=False,
            padrao=1e-6,
        )
    )
    validacao_final = criar_validacoes_finais(
        backtest=backtest,
        colunas_pesos=colunas_pesos,
        tolerancia=tolerancia_pesos,
    )

    configuracoes_backtest = pd.DataFrame(
        [
            {
                "frequencia": "MENSAL",
                "periodo_inicial": backtest["data"].min(),
                "periodo_final": backtest["data"].max(),
                "quantidade_meses": len(backtest),
                "periodos_por_ano": periodos_por_ano,
                "janela_movel_meses": periodos_janela,
                "valor_inicial_indice": valor_inicial,
                "custo_por_turnover": custo_por_turnover,
                "custo_bps": custo_por_turnover * 10000.0,
                "cobrar_custo_inicial": cobrar_custo_inicial,
                "benchmark": (
                    "Pesos iguais entre os ativos selecionados, "
                    "com rebalanceamento mensal"
                ),
                "quantidade_ativos": len(ativos),
                "ativos": ", ".join(ativos),
                "cdi_disponivel_em_todos_os_meses": bool(
                    backtest["cdi_disponivel"].all()
                ),
                "arquivo_cdi": (
                    str(arquivo_cdi)
                    if arquivo_cdi is not None
                    else ""
                ),
                "gerado_em_utc": datetime.now(
                    timezone.utc
                ).isoformat(),
            }
        ]
    )

    config_saidas = backtest_config.get(
        "arquivos_saida",
        {},
    )

    arquivos = {
        "backtest_completo": resolver_caminho(
            config_saidas.get(
                "backtest_completo",
                "data/processed/backtest_portfolio_mensal.csv",
            )
        ),
        "resumo_turnover": resolver_caminho(
            config_saidas.get(
                "resumo_turnover",
                "outputs/tabelas/05_resumo_turnover_custos.csv",
            )
        ),
        "custos_mensais": resolver_caminho(
            config_saidas.get(
                "custos_mensais",
                "outputs/tabelas/05_turnover_custos_mensal.csv",
            )
        ),
        "metricas": resolver_caminho(
            config_saidas.get(
                "metricas",
                "outputs/tabelas/05_metricas_backtest.csv",
            )
        ),
        "metricas_formatadas": resolver_caminho(
            config_saidas.get(
                "metricas_formatadas",
                "outputs/tabelas/05_metricas_backtest_formatadas.csv",
            )
        ),
        "desempenho_regimes": resolver_caminho(
            config_saidas.get(
                "desempenho_regimes",
                "outputs/tabelas/05_desempenho_por_regime.csv",
            )
        ),
        "contribuicao_regimes": resolver_caminho(
            config_saidas.get(
                "contribuicao_regimes",
                "outputs/tabelas/05_contribuicao_media_por_regime.csv",
            )
        ),
        "sensibilidade": resolver_caminho(
            config_saidas.get(
                "sensibilidade",
                "outputs/tabelas/05_sensibilidade_custos.csv",
            )
        ),
        "break_even": resolver_caminho(
            config_saidas.get(
                "break_even",
                "outputs/tabelas/05_custo_break_even.csv",
            )
        ),
        "resultados_anuais": resolver_caminho(
            config_saidas.get(
                "resultados_anuais",
                "outputs/tabelas/05_resultados_anuais.csv",
            )
        ),
        "metricas_moveis": resolver_caminho(
            config_saidas.get(
                "metricas_moveis",
                f"outputs/tabelas/05_metricas_moveis_{periodos_janela}m.csv",
            )
        ),
        "resumo_final": resolver_caminho(
            config_saidas.get(
                "resumo_final",
                "outputs/tabelas/05_resumo_final_backtest.csv",
            )
        ),
        "diagnostico": resolver_caminho(
            config_saidas.get(
                "diagnostico",
                "outputs/tabelas/05_diagnostico_estrategia.csv",
            )
        ),
        "configuracoes": resolver_caminho(
            config_saidas.get(
                "configuracoes",
                "outputs/tabelas/05_configuracoes_backtest.csv",
            )
        ),
        "validacoes": resolver_caminho(
            config_saidas.get(
                "validacoes",
                "outputs/tabelas/05_validacao_final_backtest.csv",
            )
        ),
    }

    custos_mensais = backtest[
        [
            "data",
            "regime_sinal",
            "turnover_portfolio",
            "turnover_estatica",
            "custo_portfolio",
            "custo_estatica",
            "retorno_portfolio",
            "retorno_portfolio_liquido",
            "retorno_carteira_estatica",
            "retorno_estatica_liquido",
            "indice_portfolio_bruto",
            "indice_portfolio_liquido",
            "indice_estatica_bruto",
            "indice_estatica_liquido",
        ]
    ].copy()

    salvar_csv_validado(
        backtest,
        arquivos["backtest_completo"],
    )
    salvar_csv_validado(
        resumo_turnover,
        arquivos["resumo_turnover"],
    )
    salvar_csv_validado(
        custos_mensais,
        arquivos["custos_mensais"],
    )
    salvar_csv_validado(
        metricas,
        arquivos["metricas"],
    )
    salvar_csv_validado(
        metricas_formatadas,
        arquivos["metricas_formatadas"],
    )
    salvar_csv_validado(
        desempenho_regimes,
        arquivos["desempenho_regimes"],
    )
    salvar_csv_validado(
        contribuicao_regimes,
        arquivos["contribuicao_regimes"],
    )
    salvar_csv_validado(
        sensibilidade,
        arquivos["sensibilidade"],
    )
    salvar_csv_validado(
        resumo_break_even,
        arquivos["break_even"],
    )
    salvar_csv_validado(
        resultados_anuais,
        arquivos["resultados_anuais"],
    )
    salvar_csv_validado(
        metricas_moveis,
        arquivos["metricas_moveis"],
    )
    salvar_csv_validado(
        resumo_final,
        arquivos["resumo_final"],
    )
    salvar_csv_validado(
        diagnostico_final,
        arquivos["diagnostico"],
    )
    salvar_csv_validado(
        configuracoes_backtest,
        arquivos["configuracoes"],
    )
    salvar_csv_validado(
        validacao_final,
        arquivos["validacoes"],
    )

    config_graficos = obter_valor(
        configuracao,
        ("graficos",),
        obrigatorio=False,
        padrao={},
    )
    graficos: list[Path] = []

    if bool(config_graficos.get("ativo", True)):
        pasta_graficos = resolver_caminho(
            obter_valor(
                configuracao,
                ("caminhos", "graficos"),
                obrigatorio=False,
                padrao="outputs/graficos",
            )
        )
        graficos = gerar_graficos_backtest(
            backtest=backtest,
            desempenho_regimes=desempenho_regimes,
            contribuicao_regimes=contribuicao_regimes,
            sensibilidade=sensibilidade,
            custo_base=custo_por_turnover,
            custo_break_even=custo_break_even,
            resultados_anuais=resultados_anuais,
            metricas_moveis=metricas_moveis,
            ativos=ativos,
            valor_inicial=valor_inicial,
            periodos_janela=periodos_janela,
            pasta_graficos=pasta_graficos,
            dpi=int(
                config_graficos.get(
                    "dpi",
                    150,
                )
            ),
        )

    if not validacao_final["resultado"].all():
        reprovadas = validacao_final.loc[
            ~validacao_final["resultado"]
        ]

        raise RuntimeError(
            "O backtest possui validações reprovadas:\n"
            + reprovadas.to_string(index=False)
        )

    fim_execucao = datetime.now(timezone.utc)
    ultimo = backtest.iloc[-1]

    print("=" * 80)
    print("05 — BACKTEST COMPLETO")
    print("=" * 80)
    print(f"Arquivo de entrada: {arquivo_entrada}")
    print(f"Ativos: {ativos}")
    print(f"Meses processados: {len(backtest)}")
    print(
        f"Período: "
        f"{backtest['data'].min():%d/%m/%Y} a "
        f"{backtest['data'].max():%d/%m/%Y}"
    )
    print(
        f"Custo por turnover: "
        f"{custo_por_turnover:.4%} "
        f"({custo_por_turnover * 10000:.2f} bps)"
    )
    print(
        f"Turnover total do portfólio: "
        f"{backtest['turnover_portfolio'].sum():.4f}"
    )
    print(
        f"Índice final bruto do portfólio: "
        f"{ultimo['indice_portfolio_bruto']:.2f}"
    )
    print(
        f"Índice final líquido do portfólio: "
        f"{ultimo['indice_portfolio_liquido']:.2f}"
    )
    print(
        f"Índice final líquido do benchmark: "
        f"{ultimo['indice_estatica_liquido']:.2f}"
    )
    print(
        f"Diferença líquida final: "
        f"{ultimo['indice_portfolio_liquido'] - ultimo['indice_estatica_liquido']:.2f} "
        "pontos"
    )

    if pd.notna(custo_break_even):
        print(
            f"Custo de break-even: "
            f"{custo_break_even * 10000:.2f} bps"
        )
    else:
        print(
            "Custo de break-even não encontrado "
            "no intervalo configurado."
        )

    print(
        "CDI utilizado como taxa livre de risco: "
        f"{bool(backtest['cdi_disponivel'].all())}"
    )
    print(
        f"Backtest completo salvo em: "
        f"{arquivos['backtest_completo']}"
    )
    print(
        f"Resumo final salvo em: "
        f"{arquivos['resumo_final']}"
    )
    print(
        f"Diagnóstico salvo em: "
        f"{arquivos['diagnostico']}"
    )
    print(
        f"Validações salvas em: "
        f"{arquivos['validacoes']}"
    )

    for grafico in graficos:
        print(f"Gráfico salvo em: {grafico}")

    print(
        f"Duração: "
        f"{(fim_execucao - inicio_execucao).total_seconds():.2f}s"
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