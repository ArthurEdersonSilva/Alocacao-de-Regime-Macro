# VERSAO_V6_LEITURA_FLEXIVEL_DA_SELECAO_FINAL
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

RAIZ_PROJETO = Path(
    os.getenv("PROJECT_ROOT", Path(__file__).resolve().parent.parent)
).resolve()
ARQUIVO_CONFIG = Path(
    os.getenv("PROJECT_CONFIG", RAIZ_PROJETO / "config" / "config.yaml")
).resolve()


def carregar_configuracao() -> dict[str, Any]:
    if not ARQUIVO_CONFIG.is_file():
        raise FileNotFoundError(f"Configuração não encontrada: {ARQUIVO_CONFIG}")
    with ARQUIVO_CONFIG.open("r", encoding="utf-8") as arquivo:
        config = yaml.safe_load(arquivo) or {}
    if not isinstance(config, dict):
        raise TypeError("O config.yaml deve possuir um dicionário na raiz.")
    return config


def obter(config: dict[str, Any], caminho: tuple[str, ...], padrao: Any = None) -> Any:
    valor: Any = config
    for chave in caminho:
        if not isinstance(valor, dict) or chave not in valor:
            return padrao
        valor = valor[chave]
    return valor


def resolver(caminho: str | Path) -> Path:
    caminho = Path(caminho)
    return caminho.resolve() if caminho.is_absolute() else (RAIZ_PROJETO / caminho).resolve()


def salvar_csv(tabela: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(caminho, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")
    if not caminho.is_file() or caminho.stat().st_size == 0:
        raise FileNotFoundError(f"Arquivo não salvo corretamente: {caminho}")
    validacao = pd.read_csv(caminho, encoding="utf-8-sig", low_memory=False)
    if list(validacao.columns) != list(tabela.columns) or len(validacao) != len(tabela):
        raise ValueError(f"Falha na validação do CSV salvo: {caminho}")


def identificar_segmento(classe: str) -> str:
    """Identifica o segmento principal a partir da classe do ativo."""

    classe_normalizada = str(classe).strip().upper()

    if classe_normalizada.startswith("COMMODITY_"):
        return "COMMODITIES"

    if classe_normalizada.startswith("RENDA_VARIAVEL_"):
        return "RENDA_VARIAVEL"

    if classe_normalizada.startswith("MOEDA_"):
        return "MOEDAS"

    if classe_normalizada.startswith("RENDA_FIXA_"):
        return "RENDA_FIXA"

    raise ValueError(
        f"Classe sem segmento reconhecido: {classe_normalizada}"
    )


def converter_coluna_booleana(serie: pd.Series) -> pd.Series:
    """Converte valores booleanos escritos em diferentes formatos."""

    valores_verdadeiros = {
        "TRUE",
        "VERDADEIRO",
        "1",
        "SIM",
        "YES",
    }

    return (
        serie.astype("string")
        .str.strip()
        .str.upper()
        .isin(valores_verdadeiros)
    )


def carregar_ativos_selecionados(
    config: dict[str, Any],
) -> tuple[pd.DataFrame, list[str], Path]:
    """
    Carrega os ativos escolhidos em ativos_selecionados_modelo.csv.

    A planilha de validação permanece como evidência dos candidatos
    analisados. Esta etapa utiliza somente os tickers registrados na
    seleção final e confirma que todos continuam aprovados e presentes
    na base de preços utilizáveis.
    """

    caminho_selecao = resolver(
        obter(
            config,
            (
                "selecao_ativos",
                "arquivo_selecao_final",
            ),
            obter(
                config,
                (
                    "modelo_selecionado",
                    "arquivo_ativos",
                ),
                "data/processed/ativos_selecionados_modelo.csv",
            ),
        )
    )

    if not caminho_selecao.is_file():
        raise FileNotFoundError(
            "O arquivo de ativos selecionados não foi encontrado.\n"
            f"Arquivo esperado: {caminho_selecao}"
        )

    try:
        selecionados = pd.read_csv(
            caminho_selecao,
            encoding="utf-8-sig",
            sep=None,
            engine="python",
        )
    except UnicodeDecodeError:
        selecionados = pd.read_csv(
            caminho_selecao,
            encoding="latin1",
            sep=None,
            engine="python",
        )

    selecionados.columns = [
        str(coluna)
        .replace("\ufeff", "")
        .strip()
        .lower()
        for coluna in selecionados.columns
    ]

    obrigatorias = {
        "ticker",
        "classe",
    }

    ausentes = sorted(
        obrigatorias - set(selecionados.columns)
    )

    if ausentes:
        raise ValueError(
            "Colunas ausentes no arquivo de seleção final: "
            f"{ausentes}"
        )

    selecionados = selecionados.copy()

    selecionados["ticker"] = (
        selecionados["ticker"]
        .astype("string")
        .str.strip()
    )

    selecionados["classe"] = (
        selecionados["classe"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    selecionados = selecionados.loc[
        selecionados["ticker"].notna()
        & selecionados["classe"].notna()
        & selecionados["ticker"].ne("")
        & selecionados["classe"].ne("")
    ].copy()

    if selecionados.empty:
        raise ValueError(
            "O arquivo de seleção final não possui ativos válidos."
        )

    if selecionados["ticker"].duplicated().any():
        duplicados = (
            selecionados.loc[
                selecionados["ticker"].duplicated(
                    keep=False
                ),
                "ticker",
            ]
            .astype(str)
            .tolist()
        )

        raise ValueError(
            "Existem tickers duplicados no arquivo de seleção: "
            f"{sorted(set(duplicados))}"
        )

    if "aprovado" in selecionados.columns:
        selecionados["aprovado"] = converter_coluna_booleana(
            selecionados["aprovado"]
        )

        nao_aprovados = selecionados.loc[
            ~selecionados["aprovado"],
            "ticker",
        ].astype(str).tolist()

        if nao_aprovados:
            raise ValueError(
                "A seleção final contém ativos marcados como não "
                f"aprovados: {nao_aprovados}"
            )

    else:
        selecionados["aprovado"] = True

    status_permitidos = {
        "APROVADO",
        "APROVADO_COM_RESSALVAS",
    }

    if "status" in selecionados.columns:
        selecionados["status"] = (
            selecionados["status"]
            .astype("string")
            .str.strip()
            .str.upper()
        )

        status_invalidos = selecionados.loc[
            ~selecionados["status"].isin(
                status_permitidos
            ),
            [
                "ticker",
                "status",
            ],
        ]

        if not status_invalidos.empty:
            raise ValueError(
                "A seleção final contém status não permitidos:\n"
                + status_invalidos.to_string(index=False)
            )

    selecionados["segmento"] = selecionados["classe"].map(
        identificar_segmento
    )

    segmentos_esperados = {
        "COMMODITIES",
        "RENDA_VARIAVEL",
        "MOEDAS",
        "RENDA_FIXA",
    }

    segmentos_encontrados = set(
        selecionados["segmento"].tolist()
    )

    segmentos_ausentes = sorted(
        segmentos_esperados - segmentos_encontrados
    )

    if segmentos_ausentes:
        raise ValueError(
            "A seleção final não possui todos os segmentos exigidos: "
            f"{segmentos_ausentes}"
        )

    quantidade_por_segmento = int(
        obter(
            config,
            (
                "selecao_ativos",
                "quantidade_por_segmento",
            ),
            3,
        )
    )

    contagem_segmentos = (
        selecionados.groupby(
            "segmento"
        )["ticker"]
        .nunique()
        .to_dict()
    )

    contagens_invalidas = {
        segmento: quantidade
        for segmento, quantidade in contagem_segmentos.items()
        if quantidade != quantidade_por_segmento
    }

    if contagens_invalidas:
        raise ValueError(
            "A seleção final deve possuir exatamente "
            f"{quantidade_por_segmento} ativos por segmento. "
            f"Contagem encontrada: {contagem_segmentos}"
        )

    caminho_precos = resolver(
        obter(
            config,
            (
                "selecao_ativos",
                "arquivo_precos_utilizaveis",
            ),
            obter(
                config,
                (
                    "coleta_yfinance",
                    "saidas",
                    "precos_utilizaveis",
                ),
                "data/processed/precos_ativos_utilizaveis.csv",
            ),
        )
    )

    if not caminho_precos.is_file():
        raise FileNotFoundError(
            "O arquivo de preços utilizáveis não foi encontrado:\n"
            f"{caminho_precos}"
        )

    precos = pd.read_csv(
        caminho_precos,
        encoding="utf-8-sig",
        low_memory=False,
        usecols=lambda coluna: coluna in {
            "ticker",
            "classe",
        },
    )

    if not {
        "ticker",
        "classe",
    }.issubset(precos.columns):
        raise ValueError(
            "O arquivo de preços utilizáveis não possui ticker e classe."
        )

    precos["ticker"] = (
        precos["ticker"]
        .astype("string")
        .str.strip()
    )

    precos["classe"] = (
        precos["classe"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    universo_precos = (
        precos[
            [
                "ticker",
                "classe",
            ]
        ]
        .dropna()
        .drop_duplicates(
            subset=["ticker"],
            keep="last",
        )
    )

    tickers_selecionados = selecionados[
        "ticker"
    ].astype(str).tolist()

    tickers_disponiveis = set(
        universo_precos["ticker"].astype(str)
    )

    ausentes_precos = sorted(
        set(tickers_selecionados) - tickers_disponiveis
    )

    if ausentes_precos:
        raise ValueError(
            "Ativos selecionados ausentes na base de preços "
            f"utilizáveis: {ausentes_precos}"
        )

    classes_precos = universo_precos.set_index(
        "ticker"
    )["classe"].to_dict()

    divergencias_classe = []

    for linha in selecionados.itertuples(
        index=False
    ):
        classe_precos = classes_precos.get(
            str(linha.ticker)
        )

        if classe_precos != str(linha.classe):
            divergencias_classe.append(
                {
                    "ticker": str(linha.ticker),
                    "classe_selecao": str(linha.classe),
                    "classe_precos": classe_precos,
                }
            )

    if divergencias_classe:
        raise ValueError(
            "Existem divergências de classe entre a seleção e a "
            "base de preços:\n"
            + pd.DataFrame(
                divergencias_classe
            ).to_string(index=False)
        )

    caminho_validacao = resolver(
        obter(
            config,
            (
                "selecao_ativos",
                "arquivo_validacao_ativos",
            ),
            obter(
                config,
                (
                    "coleta_yfinance",
                    "saidas",
                    "validacao_ativos",
                ),
                "data/processed/validacao_ativos_yfinance.csv",
            ),
        )
    )

    if caminho_validacao.is_file():
        validacao = pd.read_csv(
            caminho_validacao,
            encoding="utf-8-sig",
            low_memory=False,
        )

        if {
            "ticker",
            "aprovado",
        }.issubset(validacao.columns):
            validacao["ticker"] = (
                validacao["ticker"]
                .astype("string")
                .str.strip()
            )

            validacao["aprovado_validacao"] = (
                converter_coluna_booleana(
                    validacao["aprovado"]
                )
            )

            mapa_aprovacao = (
                validacao.drop_duplicates(
                    "ticker",
                    keep="last",
                )
                .set_index("ticker")[
                    "aprovado_validacao"
                ]
                .to_dict()
            )

            invalidos = [
                ticker
                for ticker in tickers_selecionados
                if not bool(
                    mapa_aprovacao.get(
                        ticker,
                        False,
                    )
                )
            ]

            if invalidos:
                raise ValueError(
                    "Ativos selecionados não aprovados na validação "
                    f"técnica: {invalidos}"
                )

    selecionados["fonte"] = str(
        caminho_selecao.relative_to(
            RAIZ_PROJETO
        )
    )

    selecionados = (
        selecionados.sort_values(
            [
                "segmento",
                "classe",
                "ticker",
            ]
        )
        .reset_index(drop=True)
    )

    tickers = selecionados[
        "ticker"
    ].astype(str).tolist()

    return (
        selecionados,
        tickers,
        caminho_selecao,
    )


def retorno_mensal(serie: pd.Series) -> float:
    valores = pd.to_numeric(serie, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if valores.empty or (1.0 + valores).le(0).any():
        return np.nan
    return float((1.0 + valores).prod() - 1.0)


def ler_csv_retornos(caminho: Path) -> pd.DataFrame:
    """
    Lê um CSV de retornos aceitando vírgula, ponto e vírgula ou tabulação.

    A leitura padrão por vírgula é priorizada porque os arquivos produzidos
    pela etapa 02 utilizam esse formato.
    """

    tentativas = [
        {
            "encoding": "utf-8-sig",
            "sep": ",",
            "engine": "c",
        },
        {
            "encoding": "utf-8-sig",
            "sep": ";",
            "engine": "python",
        },
        {
            "encoding": "utf-8-sig",
            "sep": "\t",
            "engine": "python",
        },
        {
            "encoding": "latin1",
            "sep": ",",
            "engine": "python",
        },
        {
            "encoding": "latin1",
            "sep": ";",
            "engine": "python",
        },
    ]

    erros: list[str] = []

    for parametros in tentativas:
        try:
            dados = pd.read_csv(
                caminho,
                low_memory=False,
                **parametros,
            )

            dados.columns = [
                str(coluna)
                .replace("\ufeff", "")
                .strip()
                for coluna in dados.columns
            ]

            if "data" in dados.columns:
                return dados

            erros.append(
                f"separador {parametros['sep']!r}: coluna data ausente"
            )

        except Exception as erro:
            erros.append(
                f"separador {parametros['sep']!r}: {erro}"
            )

    raise ValueError(
        "Não foi possível interpretar o arquivo de retornos:\n"
        f"{caminho}\n"
        + "\n".join(erros)
    )


def carregar_retornos_mensais(
    config: dict[str, Any],
    tickers_selecionados: list[str],
) -> tuple[pd.DataFrame, Path]:
    """
    Carrega prioritariamente retornos_ativos.csv, produzido pela etapa 02.

    Arquivos antigos de retornos mensais ou diários são utilizados apenas
    como alternativas e somente quando contêm todos os ativos selecionados.
    """

    candidatos_brutos = [
        "data/processed/retornos_ativos.csv",
        obter(
            config,
            (
                "processamento",
                "arquivos_saida",
                "retornos_diarios",
            ),
            "data/processed/retornos_ativos_diarios.csv",
        ),
        obter(
            config,
            (
                "processamento",
                "arquivos_saida",
                "retornos_mensais",
            ),
            "data/processed/retornos_ativos_mensais.csv",
        ),
    ]

    caminhos: list[Path] = []

    for item in candidatos_brutos:
        caminho_item = resolver(item)

        if caminho_item not in caminhos:
            caminhos.append(caminho_item)

    problemas: list[str] = []
    dados_escolhidos: pd.DataFrame | None = None
    caminho_escolhido: Path | None = None

    for caminho in caminhos:
        if not caminho.is_file():
            problemas.append(
                f"{caminho}: arquivo não encontrado"
            )
            continue

        try:
            dados_candidato = ler_csv_retornos(
                caminho
            )
        except Exception as erro:
            problemas.append(
                f"{caminho}: {erro}"
            )
            continue

        ausentes = [
            ticker
            for ticker in tickers_selecionados
            if ticker not in dados_candidato.columns
        ]

        if ausentes:
            problemas.append(
                f"{caminho}: ativos selecionados ausentes {ausentes}"
            )
            continue

        dados_escolhidos = dados_candidato
        caminho_escolhido = caminho
        break

    if dados_escolhidos is None or caminho_escolhido is None:
        raise FileNotFoundError(
            "Nenhum arquivo de retornos válido foi encontrado.\n"
            + "\n".join(problemas)
        )

    dados = dados_escolhidos.copy()
    caminho = caminho_escolhido

    if dados.empty:
        raise ValueError(
            f"O arquivo de retornos está vazio: {caminho}"
        )

    dados["data"] = pd.to_datetime(
        dados["data"],
        errors="coerce",
    )

    if dados["data"].isna().any():
        raise ValueError(
            f"A base de retornos possui datas inválidas: {caminho}"
        )

    for ticker in tickers_selecionados:
        dados[ticker] = pd.to_numeric(
            dados[ticker],
            errors="coerce",
        )

    ativos_sem_dados = [
        ticker
        for ticker in tickers_selecionados
        if not dados[ticker].notna().any()
    ]

    if ativos_sem_dados:
        raise ValueError(
            "Ativos selecionados sem retornos numéricos: "
            f"{ativos_sem_dados}"
        )

    dados = (
        dados[
            [
                "data",
                *tickers_selecionados,
            ]
        ]
        .drop_duplicates(
            subset=["data"],
            keep="last",
        )
        .sort_values("data")
        .reset_index(drop=True)
    )

    dados["mes"] = (
        dados["data"]
        .dt.to_period("M")
        .dt.to_timestamp("M")
    )

    mensal = (
        dados.groupby(
            "mes",
            sort=True,
        )[tickers_selecionados]
        .agg(retorno_mensal)
        .reset_index()
        .rename(
            columns={
                "mes": "data",
            }
        )
        .sort_values("data")
        .reset_index(drop=True)
    )

    mensal = mensal.dropna(
        subset=tickers_selecionados,
        how="any",
    )

    if mensal.empty:
        raise ValueError(
            "A base mensal de retornos ficou vazia após o alinhamento."
        )

    return mensal, caminho


def adicionar_cdi(
    retornos: pd.DataFrame,
    tickers: list[str],
    config: dict[str, Any],
) -> tuple[pd.DataFrame, Path | None]:
    aliases = {"CDI", "CDI_SGS_12", "RENDA_FIXA_CDI"}
    ticker_cdi = next((ticker for ticker in tickers if ticker.upper() in aliases), None)
    if ticker_cdi is None or ticker_cdi in retornos.columns:
        return retornos, None

    caminho = resolver(
        obter(
            config,
            ("processamento", "arquivos_saida", "macro_mensal"),
            "data/processed/dados_macro_mensais.csv",
        )
    )
    if not caminho.is_file():
        raise FileNotFoundError(f"Base macro mensal não encontrada para o CDI: {caminho}")

    macro = pd.read_csv(caminho, encoding="utf-8-sig", low_memory=False)
    if not {"data", "CDI_MENSAL_PCT"}.issubset(macro.columns):
        raise ValueError("A base macro mensal não possui CDI_MENSAL_PCT.")
    macro["data"] = pd.to_datetime(macro["data"], errors="coerce")
    macro[ticker_cdi] = pd.to_numeric(macro["CDI_MENSAL_PCT"], errors="coerce") / 100.0
    cdi = macro[["data", ticker_cdi]].dropna().drop_duplicates("data", keep="last")
    return pd.merge(retornos, cdi, on="data", how="left"), caminho


def carregar_regimes(config: dict[str, Any]) -> tuple[pd.DataFrame, Path]:
    caminho = resolver(
        obter(
            config,
            ("regimes", "arquivos_saida", "classificacao"),
            "data/processed/regimes_macroeconomicos.csv",
        )
    )
    if not caminho.is_file():
        raise FileNotFoundError(f"Arquivo de regimes não encontrado: {caminho}")

    dados = pd.read_csv(caminho, encoding="utf-8-sig", low_memory=False)
    obrigatorias = {"data", "regime_macro", "codigo_regime"}
    ausentes = sorted(obrigatorias - set(dados.columns))
    if ausentes:
        raise ValueError(f"Colunas ausentes no arquivo de regimes: {ausentes}")

    dados["data"] = pd.to_datetime(dados["data"], errors="coerce")
    dados["regime_macro"] = dados["regime_macro"].astype("string").str.strip().str.upper()
    dados["codigo_regime"] = pd.to_numeric(dados["codigo_regime"], errors="coerce").astype("Int64")
    dados = (
        dados.dropna(subset=["data", "regime_macro", "codigo_regime"])
        .drop_duplicates("data", keep="last")
        .sort_values("data")
        .reset_index(drop=True)
    )
    if dados.empty:
        raise ValueError("A base de regimes ficou vazia.")
    return dados, caminho


def extrair_pesos(conteudo: Any) -> dict[str, dict[str, float]]:
    """
    Extrai pesos por regime de diferentes formatos aceitos.

    Formatos suportados:
    1. {"EXPANSAO_...": {"ATIVO": 0.25}}
    2. {"pesos_por_regime": {...}}
    3. {"configuracao_atual": {"pesos_por_regime": {...}}}
    4. {"alocacao": {"pesos_por_regime": {...}}}
    """

    if not isinstance(conteudo, dict):
        raise TypeError(
            "O conteúdo dos pesos deve ser um dicionário."
        )

    candidatos = [
        conteudo.get("pesos_por_regime"),
        (
            conteudo.get("configuracao_atual", {})
            .get("pesos_por_regime")
            if isinstance(
                conteudo.get("configuracao_atual"),
                dict,
            )
            else None
        ),
        (
            conteudo.get("alocacao", {})
            .get("pesos_por_regime")
            if isinstance(
                conteudo.get("alocacao"),
                dict,
            )
            else None
        ),
    ]

    pesos_encontrados = next(
        (
            candidato
            for candidato in candidatos
            if isinstance(candidato, dict)
            and candidato
        ),
        None,
    )

    if pesos_encontrados is not None:
        conteudo = pesos_encontrados

    if not conteudo:
        raise ValueError(
            "Nenhum peso por regime foi encontrado."
        )

    resultado: dict[str, dict[str, float]] = {}

    for regime, pesos in conteudo.items():

        if not isinstance(pesos, dict):
            raise TypeError(
                "Estrutura inválida de pesos. "
                f"A chave '{regime}' possui valor do tipo "
                f"{type(pesos).__name__}, mas deveria conter "
                "um dicionário de ativos e pesos."
            )

        pesos_convertidos: dict[str, float] = {}

        for ativo, peso in pesos.items():

            try:
                pesos_convertidos[
                    str(ativo).strip()
                ] = float(
                    peso
                )

            except (
                TypeError,
                ValueError,
            ) as erro:

                raise ValueError(
                    "Peso inválido encontrado. "
                    f"Regime: {regime} | "
                    f"Ativo: {ativo} | "
                    f"Valor: {peso!r}"
                ) from erro

        resultado[
            str(regime).strip().upper()
        ] = pesos_convertidos

    return resultado


def criar_pesos_iguais_automaticos(
    config: dict[str, Any],
    tickers: list[str],
) -> tuple[dict[str, dict[str, float]], Path]:
    """
    Cria pesos iniciais iguais para os ativos da seleção final.

    Esses pesos apenas inicializam a alocação e o backtest.
    Os pesos finais serão definidos pela etapa de otimização.
    """

    if not tickers:
        raise ValueError(
            "Não existem ativos selecionados para criar os pesos iniciais."
        )

    regimes = [
        str(item).strip().upper()
        for item in obter(
            config,
            (
                "regimes",
                "lista",
            ),
            [],
        )
    ]

    if not regimes:
        regras = obter(
            config,
            (
                "regimes",
                "regras",
            ),
            {},
        )

        if isinstance(
            regras,
            dict,
        ):
            regimes = [
                str(item).strip().upper()
                for item in regras
            ]

    if not regimes:
        raise ValueError(
            "Nenhum regime foi encontrado no config.yaml."
        )

    peso_individual = 1.0 / len(
        tickers
    )

    pesos = {
        regime: {
            ticker: peso_individual
            for ticker in tickers
        }
        for regime in regimes
    }

    caminho_saida = resolver(
        obter(
            config,
            (
                "alocacao",
                "pesos_iniciais",
                "arquivo_saida",
            ),
            "outputs/modelo_final/"
            "alocacoes_iniciais_automaticas.json",
        )
    )

    caminho_saida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    conteudo = {
        "metodo": "PESOS_IGUAIS_ENTRE_ATIVOS_SELECIONADOS",
        "provisorio": True,
        "quantidade_ativos": len(
            tickers
        ),
        "peso_individual": peso_individual,
        "ativos_selecionados": tickers,
        "pesos_por_regime": pesos,
        "observacao": (
            "Pesos iniciais gerados automaticamente. "
            "A etapa 06 deve otimizar os pesos finais."
        ),
    }

    caminho_saida.write_text(
        json.dumps(
            conteudo,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return (
        pesos,
        caminho_saida,
    )


def carregar_pesos(
    config: dict[str, Any],
    tickers: list[str],
) -> tuple[dict[str, dict[str, float]], str]:
    pesos_config = obter(
        config,
        (
            "alocacao",
            "pesos_por_regime",
        ),
        None,
    )

    if (
        isinstance(
            pesos_config,
            dict,
        )
        and pesos_config
    ):
        return (
            extrair_pesos(
                pesos_config
            ),
            "config.yaml: alocacao.pesos_por_regime",
        )

    selecionado = (
        obter(
            config,
            (
                "alocacao",
                "modelo_selecionado",
            ),
            {},
        )
        or {}
    )

    if bool(
        selecionado.get(
            "pesos_definidos",
            False,
        )
    ):

        caminho = resolver(
            selecionado.get(
                "fonte_pesos",
                "outputs/modelo_final/"
                "alocacoes_modelo_selecionado.json",
            )
        )

        if not caminho.is_file():
            raise FileNotFoundError(
                "Arquivo de pesos selecionados não encontrado: "
                f"{caminho}"
            )

        return (
            extrair_pesos(
                json.loads(
                    caminho.read_text(
                        encoding="utf-8"
                    )
                )
            ),
            str(
                caminho
            ),
        )

    oficial = (
        obter(
            config,
            (
                "alocacao",
                "modelo_oficial",
            ),
            {},
        )
        or {}
    )

    if bool(
        oficial.get(
            "usar_pesos_do_arquivo",
            False,
        )
    ):

        caminho = resolver(
            oficial.get(
                "fonte_pesos",
                "outputs/modelo_final/"
                "modelo_oficial.json",
            )
        )

        if caminho.is_file():
            return (
                extrair_pesos(
                    json.loads(
                        caminho.read_text(
                            encoding="utf-8"
                        )
                    )
                ),
                str(
                    caminho
                ),
            )

    pesos_automaticos, arquivo_automatico = (
        criar_pesos_iguais_automaticos(
            config=config,
            tickers=tickers,
        )
    )

    return (
        pesos_automaticos,
        str(
            arquivo_automatico
        ),
    )


def preparar_universo_com_ativos_auxiliares(
    ativos_selecionados: pd.DataFrame,
    tickers: list[str],
    pesos: dict[str, dict[str, float]],
    config: dict[str, Any],
) -> tuple[
    pd.DataFrame,
    list[str],
    dict[str, dict[str, float]],
]:
    """
    Acrescenta ao universo ativos auxiliares que não vêm do Yahoo
    Finance, mas que aparecem na configuração oficial de pesos.

    Atualmente, o único ativo auxiliar permitido é o CDI, cuja série
    mensal é carregada da base macroeconômica oficial.
    """

    if not pesos:
        raise ValueError(
            "Nenhum peso por regime foi encontrado."
        )

    conjuntos_chaves = {
        frozenset(
            str(chave).strip()
            for chave in pesos_regime
        )
        for pesos_regime in pesos.values()
    }

    if len(conjuntos_chaves) != 1:
        raise ValueError(
            "Os regimes possuem conjuntos diferentes de ativos "
            "ou classes nos pesos."
        )

    chaves_originais = set(
        next(
            iter(
                conjuntos_chaves
            )
        )
    )

    classes_aprovadas = set(
        ativos_selecionados[
            "classe"
        ]
        .astype(str)
        .str.strip()
        .str.upper()
        .tolist()
    )

    # Quando os pesos são definidos por classe, não há ativo
    # auxiliar a incluir nesta etapa.
    if chaves_originais == classes_aprovadas:
        return (
            ativos_selecionados,
            tickers,
            pesos,
        )

    aliases_cdi = {
        "CDI",
        "CDI_SGS_12",
        "RENDA_FIXA_CDI",
    }

    pesos_normalizados: dict[
        str,
        dict[str, float],
    ] = {}

    for regime, pesos_regime in pesos.items():

        pesos_regime_normalizados: dict[
            str,
            float,
        ] = {}

        for chave, valor in pesos_regime.items():

            chave_limpa = str(
                chave
            ).strip()

            chave_normalizada = (
                "CDI"
                if chave_limpa.upper()
                in aliases_cdi
                else chave_limpa
            )

            if (
                chave_normalizada
                in pesos_regime_normalizados
            ):

                raise ValueError(
                    "Foram encontradas chaves duplicadas após "
                    "a normalização dos aliases do CDI. "
                    f"Regime: {regime}"
                )

            pesos_regime_normalizados[
                chave_normalizada
            ] = float(
                valor
            )

        pesos_normalizados[
            regime
        ] = pesos_regime_normalizados

    chaves_normalizadas = set(
        next(
            iter(
                pesos_normalizados.values()
            )
        )
    )

    tickers_yahoo = set(
        tickers
    )

    ativos_extras = (
        chaves_normalizadas
        - tickers_yahoo
    )

    extras_nao_permitidos = (
        ativos_extras
        - {
            "CDI",
        }
    )

    if extras_nao_permitidos:
        raise ValueError(
            "Os pesos contêm ativos que não foram aprovados "
            "pela coleta e não são ativos auxiliares permitidos.\n"
            f"Ativos extras: {sorted(extras_nao_permitidos)}"
        )

    if "CDI" not in ativos_extras:
        return (
            ativos_selecionados,
            tickers,
            pesos_normalizados,
        )

    ativos_atualizados = (
        ativos_selecionados.copy()
    )

    linha_cdi = pd.DataFrame(
        [
            {
                "ticker": "CDI",
                "classe": "RENDA_FIXA_CDI",
                "aprovado": True,
                "fonte": str(
                    resolver(
                        obter(
                            config,
                            (
                                "processamento",
                                "arquivos_saida",
                                "macro_mensal",
                            ),
                            "data/processed/"
                            "dados_macro_mensais.csv",
                        )
                    ).relative_to(
                        RAIZ_PROJETO
                    )
                ),
            }
        ]
    )

    ativos_atualizados = pd.concat(
        [
            ativos_atualizados,
            linha_cdi,
        ],
        ignore_index=True,
    )

    ativos_atualizados = (
        ativos_atualizados
        .drop_duplicates(
            subset=[
                "ticker",
            ],
            keep="last",
        )
        .sort_values(
            [
                "classe",
                "ticker",
            ]
        )
        .reset_index(
            drop=True
        )
    )

    tickers_atualizados = (
        ativos_atualizados[
            "ticker"
        ]
        .astype(str)
        .tolist()
    )

    return (
        ativos_atualizados,
        tickers_atualizados,
        pesos_normalizados,
    )



def converter_pesos_para_tickers(
    pesos: dict[str, dict[str, float]],
    ativos_selecionados: pd.DataFrame,
) -> dict[str, dict[str, float]]:
    """
    Aceita pesos definidos diretamente por ticker.

    Também aceita pesos definidos pela classe de origem. Quando uma
    classe possui mais de um ativo aprovado, o peso da classe é
    dividido igualmente entre seus tickers.
    """

    tickers = (
        ativos_selecionados[
            "ticker"
        ]
        .astype(str)
        .tolist()
    )

    classes_tickers = {
        str(classe): grupo[
            "ticker"
        ]
        .astype(str)
        .tolist()
        for classe, grupo in ativos_selecionados.groupby(
            "classe",
            sort=True,
        )
    }

    conjunto_tickers = set(
        tickers
    )
    conjunto_classes = set(
        classes_tickers
    )

    resultado: dict[str, dict[str, float]] = {}

    for regime, pesos_regime in pesos.items():

        pesos_normalizados = {
            str(chave).strip(): float(
                valor
            )
            for chave, valor in pesos_regime.items()
        }

        chaves = set(
            pesos_normalizados
        )

        if chaves == conjunto_tickers:

            resultado[
                regime
            ] = {
                ticker: pesos_normalizados[
                    ticker
                ]
                for ticker in tickers
            }

            continue

        if chaves == conjunto_classes:

            pesos_tickers: dict[str, float] = {}

            for classe, tickers_classe in classes_tickers.items():

                peso_classe = pesos_normalizados[
                    classe
                ]

                peso_individual = (
                    peso_classe
                    / len(
                        tickers_classe
                    )
                )

                for ticker in tickers_classe:
                    pesos_tickers[
                        ticker
                    ] = peso_individual

            resultado[
                regime
            ] = pesos_tickers

            continue

        raise ValueError(
            f"Pesos do regime {regime} incompatíveis com "
            "os ativos selecionados automaticamente.\n"
            f"Encontrados: {sorted(chaves)}\n"
            f"Tickers esperados: {sorted(conjunto_tickers)}\n"
            f"Classes de origem esperadas: {sorted(conjunto_classes)}"
        )

    return resultado


def validar_pesos(
    pesos: dict[str, dict[str, float]],
    regimes: list[str],
    tickers: list[str],
    tolerancia: float,
    permitir_vendidos: bool,
    exposicao_maxima: float,
) -> None:
    ausentes = sorted(set(regimes) - set(pesos))
    if ausentes:
        raise ValueError(f"Regimes sem pesos definidos: {ausentes}")

    for regime in regimes:
        pesos_regime = pesos[regime]
        if set(pesos_regime) != set(tickers):
            raise ValueError(f"Ativos dos pesos do regime {regime} não correspondem à seleção final.")
        vetor = np.asarray([pesos_regime[ticker] for ticker in tickers], dtype=float)
        if not np.isfinite(vetor).all():
            raise ValueError(f"O regime {regime} possui pesos nulos ou infinitos.")
        if not permitir_vendidos and (vetor < 0).any():
            raise ValueError(f"O regime {regime} possui peso negativo.")
        if not np.isclose(vetor.sum(), 1.0, atol=tolerancia, rtol=0.0):
            raise ValueError(f"Os pesos do regime {regime} somam {vetor.sum():.12f}, e não 1.0.")
        if np.abs(vetor).sum() > exposicao_maxima + tolerancia:
            raise ValueError(f"A exposição bruta do regime {regime} excede o limite.")


def preparar_base(
    retornos: pd.DataFrame,
    regimes: pd.DataFrame,
    tickers: list[str],
    defasagem: int,
) -> pd.DataFrame:
    ausentes = [ticker for ticker in tickers if ticker not in retornos.columns]
    if ausentes:
        raise ValueError(f"Ativos selecionados ausentes nos retornos: {ausentes}")

    base_retornos = retornos[["data", *tickers]].copy()
    for ticker in tickers:
        base_retornos[ticker] = pd.to_numeric(base_retornos[ticker], errors="coerce")

    base_regimes = regimes[["data", "regime_macro", "codigo_regime"]].copy()
    base_regimes["regime_sinal"] = base_regimes["regime_macro"].shift(defasagem)
    base_regimes["codigo_regime_sinal"] = base_regimes["codigo_regime"].shift(defasagem)

    base = pd.merge(base_retornos, base_regimes, on="data", how="inner", validate="one_to_one")
    base = (
        base.dropna(subset=["regime_sinal", *tickers])
        .sort_values("data")
        .reset_index(drop=True)
    )
    if base.empty:
        raise ValueError("A base de alocação ficou vazia após o alinhamento.")
    return base


def aplicar_pesos(
    base: pd.DataFrame,
    pesos: dict[str, dict[str, float]],
    tickers: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    registros = []
    for regime, pesos_regime in pesos.items():
        registro = {"regime_sinal": regime}
        registro.update({f"peso_{ticker}": pesos_regime[ticker] for ticker in tickers})
        registro["soma_pesos"] = sum(pesos_regime.values())
        registros.append(registro)

    tabela = pd.DataFrame(registros).sort_values("regime_sinal").reset_index(drop=True)
    resultado = pd.merge(base, tabela, on="regime_sinal", how="left", validate="many_to_one")
    colunas = [f"peso_{ticker}" for ticker in tickers]
    if resultado[colunas].isna().any().any():
        raise ValueError("Existem meses sem pesos atribuídos.")
    resultado["soma_pesos"] = resultado[colunas].sum(axis=1)
    return resultado, tabela


def calcular_carteiras(base: pd.DataFrame, tickers: list[str], indice_inicial: float) -> pd.DataFrame:
    resultado = base.copy()
    contribuicoes = []
    for ticker in tickers:
        coluna = f"contribuicao_{ticker}"
        resultado[coluna] = resultado[ticker] * resultado[f"peso_{ticker}"]
        contribuicoes.append(coluna)

    resultado["retorno_portfolio_bruto"] = resultado[contribuicoes].sum(axis=1)
    resultado["retorno_benchmark_estatico"] = resultado[tickers].mean(axis=1)
    resultado["indice_portfolio_bruto"] = indice_inicial * (1.0 + resultado["retorno_portfolio_bruto"]).cumprod()
    resultado["indice_benchmark_estatico"] = indice_inicial * (1.0 + resultado["retorno_benchmark_estatico"]).cumprod()
    resultado["retorno_acumulado_portfolio_bruto"] = resultado["indice_portfolio_bruto"] / indice_inicial - 1.0
    resultado["retorno_acumulado_benchmark"] = resultado["indice_benchmark_estatico"] / indice_inicial - 1.0
    resultado["drawdown_portfolio_bruto"] = resultado["indice_portfolio_bruto"] / resultado["indice_portfolio_bruto"].cummax() - 1.0
    resultado["drawdown_benchmark_estatico"] = resultado["indice_benchmark_estatico"] / resultado["indice_benchmark_estatico"].cummax() - 1.0
    resultado["diferenca_indice"] = resultado["indice_portfolio_bruto"] - resultado["indice_benchmark_estatico"]

    # Compatibilidade com as etapas antigas.
    resultado["retorno_portfolio"] = resultado["retorno_portfolio_bruto"]
    resultado["indice_portfolio"] = resultado["indice_portfolio_bruto"]
    resultado["retorno_carteira_estatica"] = resultado["retorno_benchmark_estatico"]
    resultado["indice_carteira_estatica"] = resultado["indice_benchmark_estatico"]
    resultado["drawdown_portfolio"] = resultado["drawdown_portfolio_bruto"]
    resultado["drawdown_estatica"] = resultado["drawdown_benchmark_estatico"]
    return resultado


def calcular_metricas(retornos: pd.Series, drawdown: pd.Series) -> dict[str, float]:
    retornos = pd.to_numeric(retornos, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    drawdown = pd.to_numeric(drawdown, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    quantidade = len(retornos)
    if quantidade == 0:
        raise ValueError("Não existem retornos suficientes para calcular métricas.")

    retorno_total = float((1.0 + retornos).prod() - 1.0)
    retorno_anualizado = float((1.0 + retorno_total) ** (12.0 / quantidade) - 1.0)
    volatilidade = float(retornos.std(ddof=1) * np.sqrt(12.0))
    retorno_vol = retorno_anualizado / volatilidade if np.isfinite(volatilidade) and volatilidade > 0 else np.nan

    return {
        "retorno_total": retorno_total,
        "retorno_anualizado": retorno_anualizado,
        "volatilidade_anualizada": volatilidade,
        "retorno_sobre_volatilidade": retorno_vol,
        "maximo_drawdown": float(drawdown.min()) if not drawdown.empty else np.nan,
        "meses_positivos": float(retornos.gt(0).mean()),
        "melhor_mes": float(retornos.max()),
        "pior_mes": float(retornos.min()),
        "quantidade_meses": float(quantidade),
    }


def tabela_metricas(base: pd.DataFrame) -> pd.DataFrame:
    portfolio = calcular_metricas(base["retorno_portfolio_bruto"], base["drawdown_portfolio_bruto"])
    benchmark = calcular_metricas(base["retorno_benchmark_estatico"], base["drawdown_benchmark_estatico"])
    return pd.DataFrame(
        [
            {
                "metrica": metrica,
                "portfolio_regimes_bruto": portfolio[metrica],
                "benchmark_estatico": benchmark[metrica],
            }
            for metrica in portfolio
        ]
    )


def criar_validacoes(
    base: pd.DataFrame,
    tabela_pesos: pd.DataFrame,
    tickers: list[str],
    tolerancia: float,
) -> pd.DataFrame:
    colunas_pesos = [f"peso_{ticker}" for ticker in tickers]
    registros = []

    def adicionar(nome: str, correto: bool, detalhe: str) -> None:
        registros.append({"validacao_tecnica": nome, "status": "OK" if correto else "ERRO", "detalhe": detalhe})

    adicionar("Base de alocação não vazia", not base.empty, f"{len(base)} meses")
    adicionar("Retornos selecionados preenchidos", not base[tickers].isna().any().any(), f"{int(base[tickers].isna().sum().sum())} ausências")
    adicionar("Pesos mensais preenchidos", not base[colunas_pesos].isna().any().any(), f"{int(base[colunas_pesos].isna().sum().sum())} ausências")
    adicionar(
        "Pesos mensais somam 100%",
        np.allclose(base[colunas_pesos].sum(axis=1), 1.0, atol=tolerancia, rtol=0.0),
        f"Mínimo {base[colunas_pesos].sum(axis=1).min():.12f} | Máximo {base[colunas_pesos].sum(axis=1).max():.12f}",
    )
    adicionar("Tabela de pesos possui todos os ativos", all(coluna in tabela_pesos.columns for coluna in colunas_pesos), str(colunas_pesos))
    adicionar("Datas sem duplicidade", not base["data"].duplicated().any(), f"{int(base['data'].duplicated().sum())} duplicidades")
    adicionar("Datas ordenadas", base["data"].is_monotonic_increasing, "Ordem cronológica verificada")
    adicionar("Retornos da carteira são finitos", np.isfinite(base["retorno_portfolio_bruto"].to_numpy(dtype=float)).all(), "Sem nulos ou infinitos")
    return pd.DataFrame(registros)


def gerar_graficos(base: pd.DataFrame, pasta: Path, dpi: int) -> list[Path]:
    pasta.mkdir(parents=True, exist_ok=True)
    arquivos = []

    desempenho = pasta / "04_desempenho_acumulado_bruto.png"
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(base["data"], base["indice_portfolio_bruto"], label="Portfólio por regimes — bruto")
    ax.plot(base["data"], base["indice_benchmark_estatico"], label="Benchmark estático")
    ax.set_title("Desempenho Acumulado das Carteiras")
    ax.set_xlabel("Data")
    ax.set_ylabel("Índice acumulado")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(desempenho, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    arquivos.append(desempenho)

    drawdown = pasta / "04_drawdown_carteiras.png"
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(base["data"], base["drawdown_portfolio_bruto"], label="Portfólio por regimes — bruto")
    ax.plot(base["data"], base["drawdown_benchmark_estatico"], label="Benchmark estático")
    ax.axhline(0.0, linewidth=1.0)
    ax.set_title("Drawdown das Carteiras")
    ax.set_xlabel("Data")
    ax.set_ylabel("Drawdown")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(drawdown, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    arquivos.append(drawdown)

    diferenca = pasta / "04_diferenca_carteiras.png"
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(base["data"], base["diferenca_indice"])
    ax.axhline(0.0, linewidth=1.0)
    ax.set_title("Diferença entre o Portfólio por Regimes e o Benchmark Estático")
    ax.set_xlabel("Data")
    ax.set_ylabel("Diferença no índice")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(diferenca, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    arquivos.append(diferenca)
    return arquivos


def main() -> None:
    inicio = datetime.now(timezone.utc)
    config = carregar_configuracao()

    ativos_selecionados, tickers, arquivo_universo = carregar_ativos_selecionados(config)

    retornos, arquivo_retornos = carregar_retornos_mensais(config, tickers)
    regimes, arquivo_regimes = carregar_regimes(config)

    pesos_origem, fonte_pesos = carregar_pesos(config, tickers)

    (
        ativos_selecionados,
        tickers,
        pesos_origem,
    ) = preparar_universo_com_ativos_auxiliares(
        ativos_selecionados=ativos_selecionados,
        tickers=tickers,
        pesos=pesos_origem,
        config=config,
    )

    retornos, arquivo_cdi = adicionar_cdi(
        retornos,
        tickers,
        config,
    )

    pesos = converter_pesos_para_tickers(
        pesos_origem,
        ativos_selecionados,
    )

    regimes_esperados = [str(item).strip().upper() for item in obter(config, ("regimes", "lista"), [])]
    tolerancia = float(obter(config, ("portfolio", "tolerancia_soma_pesos"), 1e-6))
    permitir_vendidos = bool(obter(config, ("portfolio", "permitir_posicao_vendida"), False))
    exposicao_maxima = float(obter(config, ("portfolio", "exposicao_maxima"), 1.0))
    validar_pesos(pesos, regimes_esperados, tickers, tolerancia, permitir_vendidos, exposicao_maxima)

    defasagem = int(obter(config, ("sinal", "modelo_oficial", "defasagem_meses"), 1))
    if defasagem < 0:
        raise ValueError("A defasagem do sinal não pode ser negativa.")

    base = preparar_base(retornos, regimes, tickers, defasagem)
    base, pesos_tabela = aplicar_pesos(base, pesos, tickers)
    indice_inicial = float(obter(config, ("portfolio", "indice_inicial_backtest"), 100.0))
    base = calcular_carteiras(base, tickers, indice_inicial)
    metricas = tabela_metricas(base)
    validacoes = criar_validacoes(base, pesos_tabela, tickers, tolerancia)

    saidas = obter(config, ("alocacao", "arquivos_saida"), {}) or {}
    arquivo_alocacao = resolver(saidas.get("base_mensal", "data/processed/alocacao_portfolio_mensal.csv"))
    arquivo_metricas = resolver(saidas.get("metricas", "outputs/tabelas/04_metricas_portfolio.csv"))
    arquivo_pesos = resolver(saidas.get("pesos", "outputs/tabelas/04_pesos_por_regime.csv"))
    arquivo_ativos = resolver(saidas.get("ativos_utilizados", "outputs/tabelas/04_ativos_selecionados_utilizados.csv"))
    arquivo_validacoes = resolver(saidas.get("validacoes", "outputs/tabelas/04_validacoes_alocacao.csv"))

    salvar_csv(base, arquivo_alocacao)
    salvar_csv(metricas, arquivo_metricas)
    salvar_csv(pesos_tabela, arquivo_pesos)
    salvar_csv(ativos_selecionados, arquivo_ativos)
    salvar_csv(validacoes, arquivo_validacoes)

    graficos_config = obter(config, ("graficos",), {}) or {}
    arquivos_graficos = []
    if bool(graficos_config.get("ativo", True)):
        pasta = resolver(obter(config, ("caminhos", "graficos"), "outputs/graficos"))
        arquivos_graficos = gerar_graficos(base, pasta, int(graficos_config.get("dpi", 150)))

    if validacoes["status"].eq("ERRO").any():
        raise RuntimeError("Uma ou mais validações da alocação falharam.")

    ultimo = base.iloc[-1]
    fim = datetime.now(timezone.utc)
    print("=" * 80)
    print("04 — ALOCAÇÃO DO PORTFÓLIO POR REGIMES")
    print("=" * 80)
    print(f"Arquivo de seleção final: {arquivo_universo}")
    print(f"Retornos utilizados: {arquivo_retornos}")
    print(f"Regimes utilizados: {arquivo_regimes}")
    print(f"Fonte dos pesos: {fonte_pesos}")
    if arquivo_cdi is not None:
        print(f"CDI mensal carregado de: {arquivo_cdi}")
    print(f"Defasagem do sinal: {defasagem} mês(es)")
    print(f"Ativos selecionados utilizados: {tickers}")
    print(f"Meses processados: {len(base)}")
    print(f"Período: {base['data'].min():%d/%m/%Y} a {base['data'].max():%d/%m/%Y}")
    print(f"Índice final do portfólio bruto: {ultimo['indice_portfolio_bruto']:.2f}")
    print(f"Índice final do benchmark estático: {ultimo['indice_benchmark_estatico']:.2f}")
    print(f"Diferença final: {ultimo['diferenca_indice']:.2f} pontos")
    print(f"Base mensal salva em: {arquivo_alocacao}")
    print(f"Métricas salvas em: {arquivo_metricas}")
    print(f"Pesos salvos em: {arquivo_pesos}")
    print(f"Validações salvas em: {arquivo_validacoes}")
    for arquivo in arquivos_graficos:
        print(f"Gráfico salvo em: {arquivo}")
    print(f"Duração: {(fim - inicio).total_seconds():.2f}s")
    print("Observação: esta etapa calcula resultados brutos. Custos e turnover pertencem ao backtest.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
        sys.exit(130)
    except Exception as erro:
        print(f"\nERRO: {erro}")
        sys.exit(1)
