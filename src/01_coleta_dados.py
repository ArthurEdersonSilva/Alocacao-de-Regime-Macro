from __future__ import annotations

import os
import re
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import yaml
from matplotlib.ticker import PercentFormatter
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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
# FUNÇÕES DE CONFIGURAÇÃO
# ============================================================

def carregar_configuracao() -> dict[str, Any]:
    """Carrega o config.yaml utilizado pelo projeto."""

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


def resolver_data_final(valor: Any, usar_data_atual: bool = True) -> str:
    """Resolve uma data final nula para a data atual."""

    if valor in (None, "", "hoje", "HOJE"):
        if not usar_data_atual:
            raise ValueError(
                "A data final está vazia e o uso da data atual "
                "está desabilitado."
            )

        return date.today().isoformat()

    return pd.Timestamp(valor).date().isoformat()


def salvar_csv_validado(
    tabela: pd.DataFrame,
    caminho: Path,
    colunas_esperadas: list[str] | None = None,
) -> None:
    """Salva um CSV e verifica estrutura e quantidade de linhas."""

    caminho.parent.mkdir(parents=True, exist_ok=True)

    tabela.to_csv(
        caminho,
        index=False,
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
    )

    if len(validacao) != len(tabela):
        raise ValueError(
            "O CSV salvo possui quantidade de linhas diferente "
            f"do DataFrame original: {caminho}"
        )

    if (
        colunas_esperadas is not None
        and list(validacao.columns) != list(colunas_esperadas)
    ):
        raise ValueError(
            "As colunas do arquivo salvo não correspondem "
            f"ao esperado: {caminho}"
        )


# ============================================================
# PREÇOS APROVADOS PELO YAHOO FINANCE
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


def carregar_precos_utilizaveis(
    configuracao: dict[str, Any],
) -> tuple[pd.DataFrame, Path]:
    """
    Carrega os preços aprovados previamente por
    coletar_ativo_yfinance.py.

    Esta etapa não realiza nova coleta no Yahoo Finance.
    """

    caminho_config = obter_valor(
        configuracao,
        (
            "coleta_yfinance",
            "saidas",
            "precos_utilizaveis",
        ),
    )

    caminho = resolver_caminho(caminho_config)

    if not caminho.is_file():
        raise FileNotFoundError(
            "O arquivo de preços utilizáveis não foi encontrado.\n"
            "Execute primeiro coletar_ativo_yfinance.py.\n"
            f"Arquivo esperado: {caminho}"
        )

    dados = pd.read_csv(
        caminho,
        encoding="utf-8-sig",
    )

    colunas_ausentes = [
        coluna
        for coluna in COLUNAS_PRECOS
        if coluna not in dados.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            "Colunas ausentes no arquivo de preços utilizáveis: "
            f"{colunas_ausentes}"
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

    dados = (
        dados.dropna(
            subset=[
                "data",
                "ticker",
                "classe",
                "close",
            ]
        )
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
        .reset_index(drop=True)
    )

    if dados.empty:
        raise ValueError(
            "O arquivo de preços utilizáveis ficou vazio após a limpeza."
        )

    return dados, caminho


# ============================================================
# SÉRIES DO BANCO CENTRAL
# ============================================================

COLUNAS_MACRO = [
    "data",
    "codigo_sgs",
    "serie",
    "valor",
]

URL_BCB = (
    "https://api.bcb.gov.br/dados/serie/"
    "bcdata.sgs.{codigo}/dados"
)


def montar_series_bcb(
    configuracao: dict[str, Any],
) -> dict[int, dict[str, Any]]:
    """Carrega os indicadores principais ativos do config.yaml."""

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

    series: dict[int, dict[str, Any]] = {}

    for chave, indicador in indicadores.items():
        if not isinstance(indicador, dict):
            continue

        if not bool(indicador.get("ativo", True)):
            continue

        codigo = indicador.get("codigo_sgs")
        nome = indicador.get("nome_modelo")
        arquivo_saida = indicador.get("arquivo_saida")

        if codigo is None or nome is None or arquivo_saida is None:
            raise ValueError(
                f"O indicador '{chave}' deve possuir codigo_sgs, "
                "nome_modelo e arquivo_saida."
            )

        series[int(codigo)] = {
            "chave": str(chave),
            "nome": str(nome).strip().upper(),
            "frequencia": str(
                indicador.get(
                    "frequencia_origem",
                    "desconhecida",
                )
            ).strip().lower(),
            "arquivo_saida": resolver_caminho(arquivo_saida),
        }

    if not series:
        raise ValueError(
            "Nenhuma série principal ativa foi encontrada no config.yaml."
        )

    return series


def criar_sessao_bcb(
    tentativas: int,
    backoff: float,
) -> requests.Session:
    """Cria uma sessão HTTP com política de novas tentativas."""

    politica = Retry(
        total=tentativas,
        connect=tentativas,
        read=tentativas,
        status=tentativas,
        backoff_factor=backoff,
        status_forcelist=[
            429,
            500,
            502,
            503,
            504,
        ],
        allowed_methods=frozenset(["GET"]),
        raise_on_status=False,
    )

    adaptador = HTTPAdapter(max_retries=politica)
    sessao = requests.Session()

    sessao.mount("https://", adaptador)
    sessao.mount("http://", adaptador)

    sessao.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 projeto-quant-regimes-macroeconomicos"
            ),
            "Accept": "application/json",
        }
    )

    return sessao


def coletar_serie_bcb(
    codigo: int,
    nome: str,
    data_inicial: str,
    data_final: str,
    anos_por_bloco: int,
    timeout: int,
    tentativas: int,
    backoff: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Coleta uma série SGS em blocos de anos."""

    inicio_total = pd.Timestamp(data_inicial).normalize()
    fim_total = pd.Timestamp(data_final).normalize()

    if inicio_total > fim_total:
        raise ValueError(
            f"Período inválido para a série SGS {codigo}."
        )

    sessao = criar_sessao_bcb(
        tentativas=tentativas,
        backoff=backoff,
    )

    partes: list[pd.DataFrame] = []
    registros_blocos: list[dict[str, Any]] = []

    inicio_bloco = inicio_total
    numero_bloco = 0

    try:
        while inicio_bloco <= fim_total:
            numero_bloco += 1

            fim_bloco = min(
                inicio_bloco
                + pd.DateOffset(years=anos_por_bloco)
                - pd.Timedelta(days=1),
                fim_total,
            )

            inicio_requisicao = time.perf_counter()

            registro = {
                "numero_bloco": numero_bloco,
                "codigo_sgs": codigo,
                "serie": nome,
                "data_inicial": inicio_bloco,
                "data_final": fim_bloco,
                "status_http": pd.NA,
                "status": "INICIADO",
                "registros": 0,
                "duracao_segundos": 0.0,
                "erro": "",
            }

            try:
                resposta = sessao.get(
                    URL_BCB.format(codigo=codigo),
                    params={
                        "formato": "json",
                        "dataInicial": inicio_bloco.strftime("%d/%m/%Y"),
                        "dataFinal": fim_bloco.strftime("%d/%m/%Y"),
                    },
                    timeout=timeout,
                )

                registro["status_http"] = resposta.status_code
                registro["duracao_segundos"] = (
                    time.perf_counter() - inicio_requisicao
                )

                if resposta.status_code != 200:
                    raise RuntimeError(
                        f"HTTP {resposta.status_code}: "
                        f"{resposta.text[:300]}"
                    )

                conteudo = resposta.json()

                if not isinstance(conteudo, list):
                    raise RuntimeError(
                        "A API retornou uma estrutura diferente de lista."
                    )

                if conteudo:
                    bloco = pd.DataFrame(conteudo)

                    if not {"data", "valor"}.issubset(bloco.columns):
                        raise RuntimeError(
                            "A API não retornou as colunas data e valor."
                        )

                    partes.append(bloco)
                    registro["registros"] = len(bloco)
                    registro["status"] = "SUCESSO"
                else:
                    registro["status"] = "SEM_DADOS"

            except Exception as erro:
                registro["duracao_segundos"] = (
                    time.perf_counter() - inicio_requisicao
                )
                registro["status"] = "ERRO"
                registro["erro"] = str(erro)
                registros_blocos.append(registro)
                raise RuntimeError(
                    f"Erro na série SGS {codigo}, período "
                    f"{inicio_bloco:%Y-%m-%d} a {fim_bloco:%Y-%m-%d}: "
                    f"{erro}"
                ) from erro

            registros_blocos.append(registro)

            inicio_bloco = fim_bloco + pd.Timedelta(days=1)
            time.sleep(0.2)

    finally:
        sessao.close()

    status_blocos = pd.DataFrame(registros_blocos)

    if not partes:
        raise RuntimeError(
            f"Nenhum dado foi retornado para a série SGS {codigo}."
        )

    dados = pd.concat(
        partes,
        ignore_index=True,
    )

    dados["data"] = pd.to_datetime(
        dados["data"],
        format="%d/%m/%Y",
        errors="coerce",
    )

    dados["valor"] = pd.to_numeric(
        dados["valor"]
        .astype(str)
        .str.strip()
        .str.replace(",", ".", regex=False),
        errors="coerce",
    )

    dados["codigo_sgs"] = int(codigo)
    dados["serie"] = str(nome).upper()

    dados = (
        dados[
            [
                "data",
                "codigo_sgs",
                "serie",
                "valor",
            ]
        ]
        .dropna(
            subset=[
                "data",
                "valor",
            ]
        )
        .loc[
            lambda tabela: (
                tabela["data"].between(
                    inicio_total,
                    fim_total,
                )
            )
        ]
        .drop_duplicates(
            subset=[
                "codigo_sgs",
                "data",
            ],
            keep="last",
        )
        .sort_values("data")
        .reset_index(drop=True)
    )

    if dados.empty:
        raise RuntimeError(
            f"A série SGS {codigo} ficou vazia após a limpeza."
        )

    return dados, status_blocos


def combinar_com_historico(
    novos_dados: pd.DataFrame,
    arquivo_existente: Path,
    acrescentar: bool,
) -> pd.DataFrame:
    """Combina novos registros com o arquivo histórico existente."""

    if not acrescentar or not arquivo_existente.is_file():
        return novos_dados

    historico = pd.read_csv(
        arquivo_existente,
        encoding="utf-8-sig",
    )

    colunas_ausentes = [
        coluna
        for coluna in COLUNAS_MACRO
        if coluna not in historico.columns
    ]

    if colunas_ausentes:
        return novos_dados

    historico = historico[COLUNAS_MACRO].copy()
    historico["data"] = pd.to_datetime(
        historico["data"],
        errors="coerce",
    )
    historico["codigo_sgs"] = pd.to_numeric(
        historico["codigo_sgs"],
        errors="coerce",
    )
    historico["valor"] = pd.to_numeric(
        historico["valor"],
        errors="coerce",
    )

    combinado = pd.concat(
        [
            historico,
            novos_dados,
        ],
        ignore_index=True,
    )

    combinado = (
        combinado.dropna(
            subset=[
                "data",
                "codigo_sgs",
                "serie",
                "valor",
            ]
        )
        .drop_duplicates(
            subset=[
                "codigo_sgs",
                "data",
            ],
            keep="last",
        )
        .sort_values(
            [
                "codigo_sgs",
                "data",
            ]
        )
        .reset_index(drop=True)
    )

    combinado["codigo_sgs"] = combinado["codigo_sgs"].astype(int)

    return combinado[COLUNAS_MACRO]


def coletar_series_macro(
    configuracao: dict[str, Any],
    series_bcb: dict[int, dict[str, Any]],
    data_inicial: str,
    data_final: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Coleta, salva e consolida as séries macroeconômicas."""

    resiliencia = obter_valor(
        configuracao,
        ("resiliencia_coleta",),
        obrigatorio=False,
        padrao={},
    )
    atualizacao = obter_valor(
        configuracao,
        ("coleta_macro", "atualizacao"),
        obrigatorio=False,
        padrao={},
    )

    tentativas = int(
        resiliencia.get(
            "tentativas_maximas",
            3,
        )
    )
    timeout = int(
        resiliencia.get(
            "timeout_segundos",
            60,
        )
    )
    backoff = 2.0 if bool(
        resiliencia.get(
            "usar_backoff_exponencial",
            True,
        )
    ) else 0.0

    acrescentar = bool(
        atualizacao.get(
            "acrescentar_novos_registros",
            True,
        )
    )

    usar_cache = bool(
        resiliencia.get(
            "comportamento_falha",
            {},
        ).get(
            "usar_cache_existente",
            True,
        )
    )

    lista_series: list[pd.DataFrame] = []
    status_series: list[dict[str, Any]] = []
    status_blocos_lista: list[pd.DataFrame] = []

    for codigo, metadados in series_bcb.items():
        nome = metadados["nome"]
        arquivo_saida = metadados["arquivo_saida"]
        inicio = time.perf_counter()

        print(
            f"Coletando {nome} — SGS {codigo}...",
            flush=True,
        )

        try:
            serie, status_blocos = coletar_serie_bcb(
                codigo=codigo,
                nome=nome,
                data_inicial=data_inicial,
                data_final=data_final,
                anos_por_bloco=5,
                timeout=timeout,
                tentativas=tentativas,
                backoff=backoff,
            )

            serie = combinar_com_historico(
                novos_dados=serie,
                arquivo_existente=arquivo_saida,
                acrescentar=acrescentar,
            )

            salvar_csv_validado(
                tabela=serie,
                caminho=arquivo_saida,
                colunas_esperadas=COLUNAS_MACRO,
            )

            lista_series.append(serie)
            status_blocos_lista.append(status_blocos)

            status_series.append(
                {
                    "codigo_sgs": codigo,
                    "serie": nome,
                    "status": "SUCESSO",
                    "registros": len(serie),
                    "data_inicial": serie["data"].min(),
                    "data_final": serie["data"].max(),
                    "arquivo": str(
                        arquivo_saida.relative_to(RAIZ_PROJETO)
                    ),
                    "duracao_segundos": (
                        time.perf_counter() - inicio
                    ),
                    "erro": "",
                }
            )

        except Exception as erro:
            if usar_cache and arquivo_saida.is_file():
                serie = pd.read_csv(
                    arquivo_saida,
                    encoding="utf-8-sig",
                )

                serie["data"] = pd.to_datetime(
                    serie["data"],
                    errors="coerce",
                )
                serie["codigo_sgs"] = pd.to_numeric(
                    serie["codigo_sgs"],
                    errors="coerce",
                )
                serie["valor"] = pd.to_numeric(
                    serie["valor"],
                    errors="coerce",
                )

                serie = (
                    serie[COLUNAS_MACRO]
                    .dropna(
                        subset=[
                            "data",
                            "codigo_sgs",
                            "serie",
                            "valor",
                        ]
                    )
                    .sort_values("data")
                    .reset_index(drop=True)
                )

                serie["codigo_sgs"] = serie["codigo_sgs"].astype(int)
                lista_series.append(serie)

                status_series.append(
                    {
                        "codigo_sgs": codigo,
                        "serie": nome,
                        "status": "CACHE_UTILIZADO",
                        "registros": len(serie),
                        "data_inicial": serie["data"].min(),
                        "data_final": serie["data"].max(),
                        "arquivo": str(
                            arquivo_saida.relative_to(RAIZ_PROJETO)
                        ),
                        "duracao_segundos": (
                            time.perf_counter() - inicio
                        ),
                        "erro": str(erro),
                    }
                )
            else:
                status_series.append(
                    {
                        "codigo_sgs": codigo,
                        "serie": nome,
                        "status": "ERRO",
                        "registros": 0,
                        "data_inicial": pd.NaT,
                        "data_final": pd.NaT,
                        "arquivo": "",
                        "duracao_segundos": (
                            time.perf_counter() - inicio
                        ),
                        "erro": str(erro),
                    }
                )

                raise

    dados_macro = pd.concat(
        lista_series,
        ignore_index=True,
    )

    dados_macro = (
        dados_macro.drop_duplicates(
            subset=[
                "codigo_sgs",
                "data",
            ],
            keep="last",
        )
        .sort_values(
            [
                "codigo_sgs",
                "data",
            ]
        )
        .reset_index(drop=True)
    )

    status = pd.DataFrame(status_series)

    if status_blocos_lista:
        status_blocos_consolidado = pd.concat(
            status_blocos_lista,
            ignore_index=True,
        )
    else:
        status_blocos_consolidado = pd.DataFrame(
            columns=[
                "numero_bloco",
                "codigo_sgs",
                "serie",
                "data_inicial",
                "data_final",
                "status_http",
                "status",
                "registros",
                "duracao_segundos",
                "erro",
            ]
        )

    return dados_macro[COLUNAS_MACRO], status, status_blocos_consolidado


# ============================================================
# QUALIDADE DOS DADOS
# ============================================================

def maior_periodo_preco_congelado(
    serie: pd.Series,
) -> int:
    """Calcula a maior sequência consecutiva do mesmo preço."""

    serie = serie.dropna().round(8).reset_index(drop=True)

    if serie.empty:
        return 0

    grupos = serie.ne(serie.shift()).cumsum()
    return int(serie.groupby(grupos).size().max())


def validar_precos(
    precos: pd.DataFrame,
    configuracao: dict[str, Any],
) -> pd.DataFrame:
    """Valida integridade e cobertura dos preços aprovados."""

    criterios = obter_valor(
        configuracao,
        ("coleta_yfinance", "validacao"),
    )

    data_referencia = pd.Timestamp(date.today()).normalize()
    data_inicial_referencia = pd.Timestamp(
        obter_valor(
            configuracao,
            ("coleta_yfinance", "periodo", "data_inicial"),
        )
    )

    cobertura_minima = float(
        criterios.get(
            "cobertura_minima",
            0.94,
        )
    )

    if cobertura_minima > 1:
        cobertura_minima /= 100

    resultados: list[dict[str, Any]] = []

    for ticker, grupo in precos.groupby("ticker", sort=True):
        grupo = (
            grupo.copy()
            .sort_values("data")
            .reset_index(drop=True)
        )

        classe = str(grupo["classe"].iloc[0])
        preco = grupo["adj_close"].copy()

        if preco.isna().all():
            preco = grupo["close"].copy()

        dados_validos = grupo.loc[
            grupo["data"].notna() & preco.notna()
        ].copy()
        preco_valido = preco.loc[
            grupo["data"].notna() & preco.notna()
        ]

        erros: list[str] = []
        alertas: list[str] = []

        duplicidades = int(
            grupo.duplicated(
                subset=[
                    "ticker",
                    "data",
                ]
            ).sum()
        )
        datas_invalidas = int(grupo["data"].isna().sum())
        precos_nao_positivos = int(preco_valido.le(0).sum())
        nulos_pct = float(preco.isna().mean() * 100)

        primeira_data = dados_validos["data"].min()
        ultima_data = dados_validos["data"].max()

        quantidade_esperada = len(
            pd.bdate_range(
                start=max(
                    data_inicial_referencia,
                    primeira_data,
                ),
                end=ultima_data,
            )
        )
        quantidade_observada = int(
            dados_validos["data"].dt.normalize().nunique()
        )
        cobertura = (
            quantidade_observada / quantidade_esperada
            if quantidade_esperada > 0
            else 0.0
        )

        dias_desatualizado = max(
            int(
                (
                    data_referencia
                    - ultima_data.normalize()
                ).days
            ),
            0,
        )

        periodo_congelado = maior_periodo_preco_congelado(
            preco_valido
        )

        intervalos = (
            dados_validos["data"]
            .sort_values()
            .diff()
            .dt.days
            .dropna()
        )
        maior_intervalo = (
            int(intervalos.max())
            if not intervalos.empty
            else 0
        )

        if duplicidades > 0:
            erros.append(f"{duplicidades} duplicidades")

        if datas_invalidas > 0:
            erros.append(f"{datas_invalidas} datas inválidas")

        if precos_nao_positivos > 0:
            erros.append(
                f"{precos_nao_positivos} preços não positivos"
            )

        if cobertura < cobertura_minima:
            alertas.append(
                f"Cobertura inferior a {cobertura_minima:.0%}"
            )

        if dias_desatualizado > int(
            criterios.get(
                "tolerancia_final_dias",
                10,
            )
        ):
            alertas.append("Série possivelmente desatualizada")

        if periodo_congelado > int(
            criterios.get(
                "maximo_dias_preco_congelado",
                10,
            )
        ):
            alertas.append("Sequência elevada de preço congelado")

        if maior_intervalo > int(
            criterios.get(
                "maximo_intervalo_dias",
                10,
            )
        ):
            alertas.append("Intervalo elevado entre observações")

        status = (
            "ERRO"
            if erros
            else "ATENCAO"
            if alertas
            else "OK"
        )

        resultados.append(
            {
                "ticker": ticker,
                "classe": classe,
                "status": status,
                "data_inicial": primeira_data,
                "data_final": ultima_data,
                "registros": len(dados_validos),
                "cobertura": cobertura,
                "cobertura_pct": cobertura * 100,
                "nulos_pct": nulos_pct,
                "duplicidades": duplicidades,
                "datas_invalidas": datas_invalidas,
                "precos_nao_positivos": precos_nao_positivos,
                "maior_periodo_congelado": periodo_congelado,
                "maior_intervalo_dias": maior_intervalo,
                "dias_desatualizado": dias_desatualizado,
                "erros": " | ".join(erros),
                "alertas": " | ".join(alertas),
            }
        )

    return (
        pd.DataFrame(resultados)
        .sort_values(
            [
                "status",
                "ticker",
            ]
        )
        .reset_index(drop=True)
    )


def tolerancia_macro_dias(frequencia: str) -> int:
    """Define tolerância de atualização conforme a frequência."""

    frequencia = frequencia.lower()

    if frequencia == "diaria":
        return 15

    if frequencia == "mensal":
        return 90

    if frequencia == "trimestral":
        return 150

    if frequencia == "por_reuniao":
        return 90

    return 90


def validar_macro(
    dados_macro: pd.DataFrame,
    series_bcb: dict[int, dict[str, Any]],
) -> pd.DataFrame:
    """Valida integridade e atualização das séries macro."""

    data_referencia = pd.Timestamp(date.today()).normalize()
    resultados: list[dict[str, Any]] = []

    for codigo, grupo in dados_macro.groupby(
        "codigo_sgs",
        sort=True,
    ):
        codigo = int(codigo)

        grupo = (
            grupo.copy()
            .sort_values("data")
            .reset_index(drop=True)
        )

        metadados = series_bcb.get(
            codigo,
            {
                "nome": str(grupo["serie"].iloc[0]),
                "frequencia": "desconhecida",
            },
        )

        nome_esperado = str(metadados["nome"])
        frequencia = str(metadados["frequencia"])

        erros: list[str] = []
        alertas: list[str] = []

        nomes = (
            grupo["serie"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        duplicidades = int(
            grupo.duplicated(
                subset=[
                    "codigo_sgs",
                    "data",
                ]
            ).sum()
        )
        datas_invalidas = int(grupo["data"].isna().sum())
        valores_nulos = int(grupo["valor"].isna().sum())

        valores_validos = (
            grupo["valor"]
            .dropna()
            .to_numpy(dtype=float)
        )
        valores_infinitos = int(
            np.isinf(valores_validos).sum()
        )

        dados_validos = grupo.dropna(
            subset=[
                "data",
                "valor",
            ]
        )

        primeira_data = dados_validos["data"].min()
        ultima_data = dados_validos["data"].max()

        tolerancia = tolerancia_macro_dias(frequencia)
        dias_desatualizado = max(
            int(
                (
                    data_referencia
                    - ultima_data.normalize()
                ).days
            ),
            0,
        )

        intervalos = (
            dados_validos["data"]
            .sort_values()
            .diff()
            .dt.days
            .dropna()
        )

        intervalo_mediano = (
            float(intervalos.median())
            if not intervalos.empty
            else 0.0
        )
        maior_intervalo = (
            int(intervalos.max())
            if not intervalos.empty
            else 0
        )

        if duplicidades > 0:
            erros.append(f"{duplicidades} duplicidades")

        if datas_invalidas > 0:
            erros.append(f"{datas_invalidas} datas inválidas")

        if valores_nulos > 0:
            erros.append(f"{valores_nulos} valores nulos")

        if valores_infinitos > 0:
            erros.append(f"{valores_infinitos} valores infinitos")

        if len(nomes) != 1 or nomes[0] != nome_esperado:
            erros.append("Nome da série diferente da configuração")

        if dias_desatualizado > tolerancia:
            alertas.append("Série possivelmente desatualizada")

        status = (
            "ERRO"
            if erros
            else "ATENCAO"
            if alertas
            else "OK"
        )

        resultados.append(
            {
                "codigo_sgs": codigo,
                "serie": nomes[0] if nomes else "",
                "status": status,
                "frequencia": frequencia,
                "data_inicial": primeira_data,
                "data_final": ultima_data,
                "registros": len(dados_validos),
                "duplicidades": duplicidades,
                "datas_invalidas": datas_invalidas,
                "valores_nulos": valores_nulos,
                "valores_infinitos": valores_infinitos,
                "intervalo_mediano_dias": intervalo_mediano,
                "maior_intervalo_dias": maior_intervalo,
                "dias_desatualizado": dias_desatualizado,
                "tolerancia_atualizacao_dias": tolerancia,
                "erros": " | ".join(erros),
                "alertas": " | ".join(alertas),
            }
        )

    return (
        pd.DataFrame(resultados)
        .sort_values(
            [
                "status",
                "codigo_sgs",
            ]
        )
        .reset_index(drop=True)
    )


def montar_resumo_qualidade(
    validacao_ativos: pd.DataFrame,
    validacao_macro: pd.DataFrame,
) -> pd.DataFrame:
    """Cria o resumo consolidado de qualidade."""

    quantidade_ativos_erro = int(
        validacao_ativos["status"].eq("ERRO").sum()
    )
    quantidade_macro_erro = int(
        validacao_macro["status"].eq("ERRO").sum()
    )

    quantidade_ativos_atencao = int(
        validacao_ativos["status"].eq("ATENCAO").sum()
    )
    quantidade_macro_atencao = int(
        validacao_macro["status"].eq("ATENCAO").sum()
    )

    if quantidade_ativos_erro or quantidade_macro_erro:
        status_final = "ERROS_ESTRUTURAIS"
    elif quantidade_ativos_atencao or quantidade_macro_atencao:
        status_final = "APROVADO_COM_ATENCAO"
    else:
        status_final = "APROVADO"

    return pd.DataFrame(
        [
            {
                "status_final": status_final,
                "ativos_analisados": len(validacao_ativos),
                "ativos_ok": int(
                    validacao_ativos["status"].eq("OK").sum()
                ),
                "ativos_atencao": quantidade_ativos_atencao,
                "ativos_erro": quantidade_ativos_erro,
                "series_macro_analisadas": len(validacao_macro),
                "series_macro_ok": int(
                    validacao_macro["status"].eq("OK").sum()
                ),
                "series_macro_atencao": quantidade_macro_atencao,
                "series_macro_erro": quantidade_macro_erro,
                "data_validacao_utc": datetime.now(
                    timezone.utc
                ).isoformat(),
            }
        ]
    )


# ============================================================
# GRÁFICOS
# ============================================================

def gerar_graficos(
    validacao_ativos: pd.DataFrame,
    validacao_macro: pd.DataFrame,
    pasta_graficos: Path,
    dpi: int,
) -> list[Path]:
    """Gera os gráficos de cobertura e atualização."""

    pasta_graficos.mkdir(
        parents=True,
        exist_ok=True,
    )

    arquivos: list[Path] = []

    arquivo_cobertura = (
        pasta_graficos
        / "01_cobertura_dados_ativos.png"
    )

    dados_cobertura = (
        validacao_ativos
        .sort_values(
            "cobertura",
            ascending=True,
        )
        .set_index("ticker")["cobertura"]
    )

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )
    dados_cobertura.plot(
        kind="barh",
        ax=ax,
    )
    ax.xaxis.set_major_formatter(
        PercentFormatter(xmax=1.0)
    )
    ax.set_title(
        "Cobertura dos Dados Diários por Ativo"
    )
    ax.set_xlabel(
        "Cobertura aproximada dos dias úteis"
    )
    ax.set_ylabel("Ativo")
    ax.grid(
        axis="x",
        alpha=0.3,
    )
    fig.tight_layout()
    fig.savefig(
        arquivo_cobertura,
        dpi=dpi,
        bbox_inches="tight",
    )
    plt.close(fig)

    arquivos.append(arquivo_cobertura)

    arquivo_atualizacao = (
        pasta_graficos
        / "01_atualizacao_series_macro.png"
    )

    dados_atualizacao = validacao_macro.copy()
    dados_atualizacao["proporcao_tolerancia"] = (
        dados_atualizacao["dias_desatualizado"]
        / dados_atualizacao["tolerancia_atualizacao_dias"]
    )

    dados_atualizacao = (
        dados_atualizacao
        .sort_values(
            "proporcao_tolerancia",
            ascending=True,
        )
        .set_index("serie")
    )

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )
    dados_atualizacao["proporcao_tolerancia"].plot(
        kind="barh",
        ax=ax,
    )
    ax.axvline(
        x=1.0,
        linewidth=1.5,
        linestyle="--",
        label="Limite de atualização",
    )
    ax.set_title(
        "Atualização das Séries Macroeconômicas"
    )
    ax.set_xlabel(
        "Dias sem atualização ÷ tolerância da série"
    )
    ax.set_ylabel("Série")
    ax.legend()
    ax.grid(
        axis="x",
        alpha=0.3,
    )
    fig.tight_layout()
    fig.savefig(
        arquivo_atualizacao,
        dpi=dpi,
        bbox_inches="tight",
    )
    plt.close(fig)

    arquivos.append(arquivo_atualizacao)

    return arquivos


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main() -> None:
    """Executa a etapa 01 de coleta, consolidação e qualidade."""

    inicio_execucao = datetime.now(timezone.utc)
    configuracao = carregar_configuracao()

    pasta_macro = resolver_caminho(
        obter_valor(
            configuracao,
            ("caminhos", "macro_bruto"),
            obrigatorio=False,
            padrao="data/raw/macro",
        )
    )
    pasta_tabelas = resolver_caminho(
        obter_valor(
            configuracao,
            ("caminhos", "tabelas"),
            obrigatorio=False,
            padrao="outputs/tabelas",
        )
    )
    pasta_graficos = resolver_caminho(
        obter_valor(
            configuracao,
            ("caminhos", "graficos"),
            obrigatorio=False,
            padrao="outputs/graficos",
        )
    )

    pasta_macro.mkdir(
        parents=True,
        exist_ok=True,
    )
    pasta_tabelas.mkdir(
        parents=True,
        exist_ok=True,
    )
    pasta_graficos.mkdir(
        parents=True,
        exist_ok=True,
    )

    data_inicial_macro = str(
        obter_valor(
            configuracao,
            (
                "coleta_macro",
                "periodo_operacional",
                "inicio",
            ),
        )
    )
    data_final_macro = resolver_data_final(
        obter_valor(
            configuracao,
            (
                "coleta_macro",
                "periodo_operacional",
                "fim",
            ),
            obrigatorio=False,
            padrao=None,
        ),
        usar_data_atual=bool(
            obter_valor(
                configuracao,
                (
                    "coleta_macro",
                    "periodo_operacional",
                    "usar_ultima_data_disponivel",
                ),
                obrigatorio=False,
                padrao=True,
            )
        ),
    )

    print("=" * 80)
    print("01 — COLETA E ORGANIZAÇÃO DOS DADOS")
    print("=" * 80)
    print(f"Raiz do projeto: {RAIZ_PROJETO}")
    print(f"Configuração: {ARQUIVO_CONFIG}")

    # --------------------------------------------------------
    # 1. PREÇOS JÁ APROVADOS
    # --------------------------------------------------------

    precos_ativos, arquivo_precos = carregar_precos_utilizaveis(
        configuracao
    )

    print(
        "\nPreços utilizáveis carregados:"
    )
    print(f"- Arquivo: {arquivo_precos}")
    print(
        f"- Ativos: {precos_ativos['ticker'].nunique()}"
    )
    print(
        f"- Registros: {len(precos_ativos):,}"
    )

    # --------------------------------------------------------
    # 2. COLETA MACROECONÔMICA
    # --------------------------------------------------------

    series_bcb = montar_series_bcb(
        configuracao
    )

    dados_macro, status_macro, status_blocos = coletar_series_macro(
        configuracao=configuracao,
        series_bcb=series_bcb,
        data_inicial=data_inicial_macro,
        data_final=data_final_macro,
    )

    arquivo_macro_consolidado = (
        pasta_macro
        / "series_macroeconomicas.csv"
    )

    salvar_csv_validado(
        tabela=dados_macro,
        caminho=arquivo_macro_consolidado,
        colunas_esperadas=COLUNAS_MACRO,
    )

    # --------------------------------------------------------
    # 3. QUALIDADE
    # --------------------------------------------------------

    validacao_ativos = validar_precos(
        precos=precos_ativos,
        configuracao=configuracao,
    )

    validacao_macro = validar_macro(
        dados_macro=dados_macro,
        series_bcb=series_bcb,
    )

    resumo_qualidade = montar_resumo_qualidade(
        validacao_ativos=validacao_ativos,
        validacao_macro=validacao_macro,
    )

    arquivo_validacao_ativos = (
        pasta_tabelas
        / "01_validacao_ativos.csv"
    )
    arquivo_validacao_macro = (
        pasta_tabelas
        / "01_validacao_series_macro.csv"
    )
    arquivo_status_macro = (
        pasta_tabelas
        / "01_status_coleta_macro.csv"
    )
    arquivo_status_blocos = (
        pasta_tabelas
        / "01_status_blocos_bcb.csv"
    )

    arquivo_resumo_qualidade = resolver_caminho(
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

    salvar_csv_validado(
        tabela=validacao_ativos,
        caminho=arquivo_validacao_ativos,
    )
    salvar_csv_validado(
        tabela=validacao_macro,
        caminho=arquivo_validacao_macro,
    )
    salvar_csv_validado(
        tabela=status_macro,
        caminho=arquivo_status_macro,
    )
    salvar_csv_validado(
        tabela=status_blocos,
        caminho=arquivo_status_blocos,
    )
    salvar_csv_validado(
        tabela=resumo_qualidade,
        caminho=arquivo_resumo_qualidade,
    )

    # --------------------------------------------------------
    # 4. GRÁFICOS
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
            validacao_ativos=validacao_ativos,
            validacao_macro=validacao_macro,
            pasta_graficos=pasta_graficos,
            dpi=int(config_graficos.get("dpi", 150)),
        )

    # --------------------------------------------------------
    # 5. RESULTADO
    # --------------------------------------------------------

    fim_execucao = datetime.now(timezone.utc)

    print("\n" + "=" * 80)
    print("ETAPA 01 CONCLUÍDA")
    print("=" * 80)
    print(
        f"Ativos analisados: {len(validacao_ativos)}"
    )
    print(
        f"Séries macroeconômicas: {len(validacao_macro)}"
    )
    print(
        f"Status final: "
        f"{resumo_qualidade['status_final'].iloc[0]}"
    )
    print(
        f"Macro consolidado: {arquivo_macro_consolidado}"
    )
    print(
        f"Resumo de qualidade: {arquivo_resumo_qualidade}"
    )

    for arquivo in arquivos_graficos:
        print(f"Gráfico: {arquivo}")

    print(
        f"Duração: "
        f"{(fim_execucao - inicio_execucao).total_seconds():.2f}s"
    )

    interromper_erro_critico = bool(
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
        interromper_erro_critico
        and resumo_qualidade[
            "status_final"
        ].iloc[0] == "ERROS_ESTRUTURAIS"
    ):
        raise RuntimeError(
            "Foram encontrados erros estruturais na qualidade dos dados."
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