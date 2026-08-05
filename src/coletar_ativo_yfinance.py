from __future__ import annotations

import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yfinance as yf
import yaml


# ============================================================
# CAMINHOS
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
# CONFIGURAÇÃO
# ============================================================

def carregar_configuracao() -> dict[str, Any]:
    """Carrega o config.yaml do projeto."""

    if not ARQUIVO_CONFIG.is_file():
        raise FileNotFoundError(
            f"Configuração não encontrada: {ARQUIVO_CONFIG}"
        )

    with ARQUIVO_CONFIG.open("r", encoding="utf-8") as arquivo:
        configuracao = yaml.safe_load(arquivo) or {}

    if not isinstance(configuracao, dict):
        raise TypeError("O config.yaml deve possuir um dicionário na raiz.")

    return configuracao


def obter_secao(
    configuracao: dict[str, Any],
    caminho: tuple[str, ...],
) -> Any:
    """Obtém uma seção obrigatória do YAML."""

    valor: Any = configuracao

    for chave in caminho:
        if not isinstance(valor, dict) or chave not in valor:
            raise KeyError(
                "Parâmetro obrigatório ausente no config.yaml: "
                + ".".join(caminho)
            )
        valor = valor[chave]

    return valor


def resolver_caminho(caminho: str | Path) -> Path:
    """Resolve um caminho relativo a partir da raiz do projeto."""

    caminho = Path(caminho)

    if not caminho.is_absolute():
        caminho = RAIZ_PROJETO / caminho

    return caminho.resolve()


def normalizar_proporcao(valor: Any, nome: str) -> float:
    """Aceita proporção decimal ou percentual."""

    proporcao = float(valor)

    if proporcao > 1:
        proporcao /= 100

    if not 0 <= proporcao <= 1:
        raise ValueError(
            f"{nome} deve estar entre 0 e 1 ou entre 0 e 100."
        )

    return proporcao


def normalizar_candidatos(secao: Any) -> dict[str, str]:
    """Converte universo_candidatos_yfinance para {ticker: classe}."""

    candidatos: dict[str, str] = {}

    def percorrer(valor: Any) -> None:
        if isinstance(valor, list):
            for item in valor:
                percorrer(item)
            return

        if not isinstance(valor, dict):
            return

        ticker = valor.get("ticker") or valor.get("ativo")
        classe = valor.get("classe")

        if ticker is not None:
            if classe is None:
                raise ValueError(
                    f"O ativo {ticker} está sem classe no config.yaml."
                )

            ticker_texto = str(ticker).strip()
            classe_texto = str(classe).strip()

            if not ticker_texto or not classe_texto:
                raise ValueError("Ticker e classe não podem estar vazios.")

            candidatos[ticker_texto] = classe_texto
            return

        for item in valor.values():
            percorrer(item)

    percorrer(secao)

    if not candidatos:
        raise ValueError(
            "Nenhum candidato foi encontrado em "
            "universo_candidatos_yfinance."
        )

    return candidatos


# ============================================================
# COLETA
# ============================================================

def coletar_ativo(
    ticker: str,
    classe: str,
    data_inicial: str,
    data_final_yfinance: str,
    requisicao: dict[str, Any],
    tentativas: dict[str, Any],
    campos_obrigatorios: list[str],
) -> pd.DataFrame:
    """Coleta e padroniza o histórico diário de um ativo."""

    quantidade_maxima = int(tentativas["quantidade_maxima"])
    timeout = int(tentativas["timeout_segundos"])
    espera_progressiva = bool(
        tentativas.get("usar_espera_progressiva", True)
    )
    multiplicador_espera = float(
        tentativas.get("multiplicador_espera_segundos", 2)
    )

    ultimo_erro: Exception | None = None

    for tentativa in range(1, quantidade_maxima + 1):
        try:
            dados = yf.download(
                tickers=ticker,
                start=data_inicial,
                end=data_final_yfinance,
                interval=str(requisicao["intervalo"]),
                auto_adjust=bool(requisicao["auto_adjust"]),
                actions=bool(requisicao["actions"]),
                progress=bool(requisicao["progress"]),
                threads=bool(requisicao["threads"]),
                timeout=timeout,
                multi_level_index=bool(
                    requisicao["multi_level_index"]
                ),
            )

            if dados is None or dados.empty:
                raise RuntimeError(
                    f"Nenhum dado retornado para {ticker}."
                )

            break

        except Exception as erro:
            ultimo_erro = erro

            if tentativa >= quantidade_maxima:
                continue

            espera = (
                tentativa * multiplicador_espera
                if espera_progressiva
                else multiplicador_espera
            )

            print(
                f"Tentativa {tentativa} falhou para {ticker}: "
                f"{erro}. Nova tentativa em {espera:.1f}s.",
                flush=True,
            )
            time.sleep(espera)

    else:
        raise RuntimeError(
            f"Falha na coleta de {ticker} após "
            f"{quantidade_maxima} tentativas: {ultimo_erro}"
        )

    if isinstance(dados.columns, pd.MultiIndex):
        dados.columns = dados.columns.get_level_values(0)

    dados = dados.reset_index()

    dados.columns = [
        str(coluna).strip().lower().replace(" ", "_")
        for coluna in dados.columns
    ]

    if "date" in dados.columns:
        dados.rename(columns={"date": "data"}, inplace=True)

    if "datetime" in dados.columns:
        dados.rename(columns={"datetime": "data"}, inplace=True)

    if "data" not in dados.columns:
        raise RuntimeError(
            f"Coluna de data não encontrada para {ticker}."
        )

    dados["data"] = pd.to_datetime(
        dados["data"],
        errors="coerce",
        utc=True,
    ).dt.tz_convert(None)

    if "adj_close" not in dados.columns and "close" in dados.columns:
        dados["adj_close"] = dados["close"]

    for coluna in [
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]:
        if coluna not in dados.columns:
            dados[coluna] = pd.NA

        dados[coluna] = pd.to_numeric(
            dados[coluna],
            errors="coerce",
        )

    dados.insert(1, "ticker", ticker)
    dados.insert(2, "classe", classe)

    colunas_ausentes = [
        coluna
        for coluna in campos_obrigatorios
        if coluna not in dados.columns
    ]

    if colunas_ausentes:
        raise RuntimeError(
            f"Campos obrigatórios ausentes em {ticker}: "
            f"{colunas_ausentes}"
        )

    dados = dados[campos_obrigatorios]

    dados = (
        dados.dropna(subset=["data"])
        .drop_duplicates(
            subset=["data", "ticker"],
            keep="last",
        )
        .sort_values("data")
        .reset_index(drop=True)
    )

    if dados.empty:
        raise RuntimeError(
            f"Os dados de {ticker} ficaram vazios após a limpeza."
        )

    return dados


# ============================================================
# VALIDAÇÃO
# ============================================================

def maior_sequencia_verdadeira(serie: pd.Series) -> int:
    """Retorna a maior sequência consecutiva de valores True."""

    serie = serie.fillna(False).astype(bool)

    if not serie.any():
        return 0

    grupos = serie.ne(serie.shift(fill_value=False)).cumsum()
    tamanhos = serie.groupby(grupos).sum()

    return int(tamanhos.max())


def maior_periodo_congelado(preco: pd.Series) -> int:
    """Retorna a maior sequência consecutiva do mesmo preço."""

    preco = preco.dropna().round(8).reset_index(drop=True)

    if preco.empty:
        return 0

    grupos = preco.ne(preco.shift()).cumsum()
    return int(preco.groupby(grupos).size().max())


def validar_ativo(
    dados: pd.DataFrame,
    data_inicial: str,
    data_final: str,
    criterios: dict[str, Any],
    preco_principal: str,
    preco_alternativo: str,
) -> dict[str, Any]:
    """Valida a cobertura e a integridade do ativo."""

    ticker = str(dados["ticker"].iloc[0])
    classe = str(dados["classe"].iloc[0])
    eh_moeda = classe.startswith("MOEDA")

    data_limite_inicio = pd.Timestamp(
        criterios["data_limite_inicio"]
    )
    tolerancia_final = int(criterios["tolerancia_final_dias"])
    cobertura_minima = normalizar_proporcao(
        criterios["cobertura_minima"],
        "cobertura_minima",
    )
    percentual_maximo_nulos = normalizar_proporcao(
        criterios["percentual_maximo_nulos"],
        "percentual_maximo_nulos",
    )
    maximo_dias_congelado = int(
        criterios["maximo_dias_preco_congelado"]
    )
    maximo_linhas_suspeitas = int(
        criterios["maximo_linhas_suspeitas_consecutivas"]
    )
    maximo_intervalo = int(
        criterios["maximo_intervalo_dias"]
    )
    maximo_retorno = normalizar_proporcao(
        criterios["maximo_retorno_diario_absoluto"],
        "maximo_retorno_diario_absoluto",
    )
    percentual_maximo_ohlc = normalizar_proporcao(
        criterios["percentual_maximo_ohlc_invalido"],
        "percentual_maximo_ohlc_invalido",
    )

    duplicidades = int(
        dados.duplicated(subset=["data", "ticker"]).sum()
    )

    preco = dados[preco_principal].copy()

    if preco.isna().all():
        preco = dados[preco_alternativo].copy()

    percentual_nulos = float(preco.isna().mean())

    filtro_valido = dados["data"].notna() & preco.notna()
    dados_validos = dados.loc[filtro_valido].copy()
    preco_valido = preco.loc[filtro_valido].copy()

    if dados_validos.empty:
        return {
            "ticker": ticker,
            "classe": classe,
            "aprovado": False,
            "status": "REPROVADO",
            "motivos_reprovacao": "Nenhum registro válido",
            "ressalvas": "",
            "erro_coleta": "",
        }

    primeira_data = dados_validos["data"].min()
    ultima_data = dados_validos["data"].max()

    dias_desatualizado = max(
        0,
        int((pd.Timestamp(data_final) - ultima_data).days),
    )

    quantidade_esperada = len(
        pd.bdate_range(
            start=data_inicial,
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

    congelado = maior_periodo_congelado(preco_valido)

    ohlc_completo = dados[
        ["open", "high", "low", "close"]
    ].notna().all(axis=1)

    open_high_iguais = pd.Series(
        np.isclose(
            dados["open"],
            dados["high"],
            rtol=0,
            atol=1e-8,
            equal_nan=False,
        ),
        index=dados.index,
    )
    high_low_iguais = pd.Series(
        np.isclose(
            dados["high"],
            dados["low"],
            rtol=0,
            atol=1e-8,
            equal_nan=False,
        ),
        index=dados.index,
    )
    low_close_iguais = pd.Series(
        np.isclose(
            dados["low"],
            dados["close"],
            rtol=0,
            atol=1e-8,
            equal_nan=False,
        ),
        index=dados.index,
    )

    volume_zero = dados["volume"].fillna(0).eq(0)

    if (
        eh_moeda
        and bool(
            criterios.get(
                "volume_zero_permitido_para_moedas",
                True,
            )
        )
    ):
        linhas_suspeitas = pd.Series(False, index=dados.index)
    else:
        linhas_suspeitas = (
            ohlc_completo
            & volume_zero
            & open_high_iguais
            & high_low_iguais
            & low_close_iguais
        )

    maior_sequencia_suspeita = maior_sequencia_verdadeira(
        linhas_suspeitas
    )
    percentual_linhas_suspeitas = float(
        linhas_suspeitas.mean()
    )

    maior_open_close = dados[["open", "close"]].max(axis=1)
    menor_open_close = dados[["open", "close"]].min(axis=1)

    ohlc_invalido = (
        ohlc_completo
        & (
            (dados["high"] < maior_open_close)
            | (dados["low"] > menor_open_close)
            | (dados["high"] < dados["low"])
        )
    )
    percentual_ohlc_invalido = float(ohlc_invalido.mean())

    precos_nao_positivos = int(preco_valido.le(0).sum())

    retornos = (
        preco_valido.pct_change(fill_method=None)
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
    )
    maior_retorno_absoluto = (
        float(retornos.abs().max())
        if not retornos.empty
        else np.nan
    )

    criterios_obrigatorios = {
        "inicio_ok": primeira_data <= data_limite_inicio,
        "final_ok": dias_desatualizado <= tolerancia_final,
        "cobertura_ok": cobertura >= cobertura_minima,
        "nulos_ok": percentual_nulos <= percentual_maximo_nulos,
        "precos_positivos_ok": (
            precos_nao_positivos == 0
            if bool(criterios["exigir_precos_positivos"])
            else True
        ),
        "retorno_ok": (
            pd.notna(maior_retorno_absoluto)
            and maior_retorno_absoluto <= maximo_retorno
            if bool(criterios["exigir_retorno_calculavel"])
            else (
                pd.isna(maior_retorno_absoluto)
                or maior_retorno_absoluto <= maximo_retorno
            )
        ),
    }

    criterios_alerta = {
        "preco_congelado": congelado <= maximo_dias_congelado,
        "linhas_suspeitas": (
            maior_sequencia_suspeita
            <= maximo_linhas_suspeitas
        ),
        "intervalo_elevado": maior_intervalo <= maximo_intervalo,
        "duplicidades": (
            duplicidades == 0
            if bool(criterios["exigir_sem_duplicados"])
            else True
        ),
        "ohlc_invalido": (
            percentual_ohlc_invalido
            <= percentual_maximo_ohlc
        ),
    }

    aprovado = all(criterios_obrigatorios.values())

    motivos = [
        nome
        for nome, correto in criterios_obrigatorios.items()
        if not correto
    ]
    ressalvas = [
        nome
        for nome, correto in criterios_alerta.items()
        if not correto
    ]

    if not aprovado:
        status = "REPROVADO"
    elif ressalvas:
        status = "APROVADO_COM_RESSALVAS"
    else:
        status = "APROVADO"

    return {
        "ticker": ticker,
        "classe": classe,
        "aprovado": aprovado,
        "status": status,
        "motivos_reprovacao": ", ".join(motivos),
        "ressalvas": ", ".join(ressalvas),
        "data_inicial": primeira_data,
        "data_final": ultima_data,
        "registros": len(dados_validos),
        "cobertura_pct": round(cobertura * 100, 2),
        "nulos_pct": round(percentual_nulos * 100, 2),
        "maior_periodo_congelado": congelado,
        "maior_sequencia_suspeita": maior_sequencia_suspeita,
        "linhas_suspeitas_pct": round(
            percentual_linhas_suspeitas * 100,
            2,
        ),
        "maior_intervalo_dias": maior_intervalo,
        "maior_retorno_diario_pct": (
            round(maior_retorno_absoluto * 100, 2)
            if pd.notna(maior_retorno_absoluto)
            else np.nan
        ),
        "ohlc_invalido_pct": round(
            percentual_ohlc_invalido * 100,
            4,
        ),
        "precos_nao_positivos": precos_nao_positivos,
        "dias_desatualizado": dias_desatualizado,
        "erro_coleta": "",
    }


# ============================================================
# EXECUÇÃO
# ============================================================

def main() -> None:
    """Executa a coleta e a validação dos candidatos."""

    configuracao = carregar_configuracao()

    coleta_config = obter_secao(
        configuracao,
        ("coleta_yfinance",),
    )
    candidatos_config = obter_secao(
        configuracao,
        ("universo_candidatos_yfinance",),
    )

    periodo = obter_secao(
        configuracao,
        ("coleta_yfinance", "periodo"),
    )
    requisicao = obter_secao(
        configuracao,
        ("coleta_yfinance", "requisicao"),
    )
    tentativas = obter_secao(
        configuracao,
        ("coleta_yfinance", "tentativas"),
    )
    criterios = obter_secao(
        configuracao,
        ("coleta_yfinance", "validacao"),
    )
    saidas = obter_secao(
        configuracao,
        ("coleta_yfinance", "saidas"),
    )

    data_inicial = pd.Timestamp(
        periodo["data_inicial"]
    ).date().isoformat()

    data_final_config = periodo.get("data_final")
    usar_data_atual = bool(
        periodo.get("usar_data_atual", True)
    )

    if data_final_config is None and usar_data_atual:
        data_final = date.today().isoformat()
    elif data_final_config is not None:
        data_final = pd.Timestamp(
            data_final_config
        ).date().isoformat()
    else:
        raise ValueError(
            "data_final está vazia e usar_data_atual está desabilitado."
        )

    if pd.Timestamp(data_inicial) > pd.Timestamp(data_final):
        raise ValueError(
            "A data inicial não pode ser posterior à data final."
        )

    data_final_yfinance = (
        pd.Timestamp(data_final).date()
        + timedelta(
            days=int(
                periodo.get(
                    "adicionar_dias_data_final_yfinance",
                    1,
                )
            )
        )
    ).isoformat()

    campos_obrigatorios = list(
        coleta_config["campos_obrigatorios"]
    )
    preco_principal = str(
        coleta_config["preco_principal"]
    )
    preco_alternativo = str(
        coleta_config["preco_alternativo"]
    )

    candidatos = normalizar_candidatos(candidatos_config)

    arquivo_validacao = resolver_caminho(
        saidas["validacao_ativos"]
    )
    arquivo_precos = resolver_caminho(
        saidas["precos_utilizaveis"]
    )

    arquivo_validacao.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    arquivo_precos.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    resultados: list[dict[str, Any]] = []
    precos_utilizaveis: list[pd.DataFrame] = []

    total = len(candidatos)

    print("=" * 70)
    print("COLETA E VALIDAÇÃO DOS CANDIDATOS DO YAHOO FINANCE")
    print("=" * 70)
    print(f"Configuração: {ARQUIVO_CONFIG}")
    print(f"Período: {data_inicial} até {data_final}")
    print(f"Candidatos: {total}")

    for numero, (ticker, classe) in enumerate(
        candidatos.items(),
        start=1,
    ):
        inicio = time.perf_counter()

        print(
            f"\n[{numero}/{total}] {ticker}",
            flush=True,
        )

        try:
            dados = coletar_ativo(
                ticker=ticker,
                classe=classe,
                data_inicial=data_inicial,
                data_final_yfinance=data_final_yfinance,
                requisicao=requisicao,
                tentativas=tentativas,
                campos_obrigatorios=campos_obrigatorios,
            )

            resultado = validar_ativo(
                dados=dados,
                data_inicial=data_inicial,
                data_final=data_final,
                criterios=criterios,
                preco_principal=preco_principal,
                preco_alternativo=preco_alternativo,
            )
            resultados.append(resultado)

            if bool(resultado["aprovado"]):
                precos_utilizaveis.append(dados)

            print(
                f"Status: {resultado['status']} | "
                f"{time.perf_counter() - inicio:.2f}s",
                flush=True,
            )

        except Exception as erro:
            resultados.append(
                {
                    "ticker": ticker,
                    "classe": classe,
                    "aprovado": False,
                    "status": "ERRO_COLETA",
                    "motivos_reprovacao": "",
                    "ressalvas": "",
                    "data_inicial": pd.NaT,
                    "data_final": pd.NaT,
                    "registros": 0,
                    "cobertura_pct": np.nan,
                    "nulos_pct": np.nan,
                    "maior_periodo_congelado": np.nan,
                    "maior_sequencia_suspeita": np.nan,
                    "linhas_suspeitas_pct": np.nan,
                    "maior_intervalo_dias": np.nan,
                    "maior_retorno_diario_pct": np.nan,
                    "ohlc_invalido_pct": np.nan,
                    "precos_nao_positivos": np.nan,
                    "dias_desatualizado": np.nan,
                    "erro_coleta": str(erro),
                }
            )

            print(
                f"Status: ERRO_COLETA | {erro}",
                flush=True,
            )

        time.sleep(
            float(
                tentativas.get(
                    "intervalo_entre_ativos_segundos",
                    0,
                )
            )
        )

    validacao = pd.DataFrame(resultados)

    validacao = validacao.sort_values(
        ["status", "classe", "ticker"]
    ).reset_index(drop=True)

    if precos_utilizaveis:
        precos = pd.concat(
            precos_utilizaveis,
            ignore_index=True,
        )

        precos = (
            precos.drop_duplicates(
                subset=["ticker", "data"],
                keep="last",
            )
            .sort_values(["ticker", "data"])
            .reset_index(drop=True)
        )
    else:
        precos = pd.DataFrame(
            columns=campos_obrigatorios
        )

    validacao.to_csv(
        arquivo_validacao,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )
    precos.to_csv(
        arquivo_precos,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )

    quantidade_aprovados = int(
        validacao["aprovado"].fillna(False).astype(bool).sum()
    )
    quantidade_reprovados = int(
        validacao["status"].eq("REPROVADO").sum()
    )
    quantidade_erros = int(
        validacao["status"].eq("ERRO_COLETA").sum()
    )

    print("\n" + "=" * 70)
    print("RESUMO")
    print("=" * 70)
    print(f"Analisados: {len(validacao)}")
    print(f"Aprovados: {quantidade_aprovados}")
    print(f"Reprovados: {quantidade_reprovados}")
    print(f"Erros de coleta: {quantidade_erros}")
    print(f"Validação: {arquivo_validacao}")
    print(f"Preços utilizáveis: {arquivo_precos}")

    if quantidade_aprovados == 0:
        raise RuntimeError(
            "Nenhum ativo foi aprovado. "
            "O arquivo de validação foi salvo para diagnóstico."
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