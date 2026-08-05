from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml


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
) -> None:
    """Salva um CSV e verifica sua existência e estrutura básica."""

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
        low_memory=False,
    )

    if list(validacao.columns) != list(tabela.columns):
        raise ValueError(
            "As colunas do CSV salvo não correspondem ao DataFrame: "
            f"{caminho}"
        )

    if len(validacao) != len(tabela):
        raise ValueError(
            "A quantidade de registros do CSV salvo não corresponde "
            f"ao DataFrame: {caminho}"
        )


# ============================================================
# CARREGAMENTO E PREPARAÇÃO DA BASE MACROECONÔMICA
# ============================================================

def carregar_dados_macro(
    configuracao: dict[str, Any],
) -> tuple[pd.DataFrame, Path]:
    """Carrega a base macroeconômica mensal produzida pela etapa 02."""

    caminho_config = obter_valor(
        configuracao,
        (
            "processamento",
            "arquivos_saida",
            "macro_mensal",
        ),
        obrigatorio=False,
        padrao="data/processed/dados_macro_mensais.csv",
    )

    caminho = resolver_caminho(caminho_config)

    if not caminho.is_file():
        raise FileNotFoundError(
            "A base macroeconômica mensal não foi encontrada.\n"
            "Execute primeiro 02_analise_exploratoria.py.\n"
            f"Arquivo esperado: {caminho}"
        )

    dados = pd.read_csv(
        caminho,
        encoding="utf-8-sig",
        low_memory=False,
    )

    if dados.empty:
        raise ValueError(
            f"A base macroeconômica mensal está vazia: {caminho}"
        )

    if "data" not in dados.columns:
        raise ValueError(
            "A base macroeconômica mensal não possui a coluna 'data'."
        )

    dados["data"] = pd.to_datetime(
        dados["data"],
        errors="coerce",
    )

    quantidade_datas_invalidas = int(
        dados["data"].isna().sum()
    )

    if quantidade_datas_invalidas > 0:
        raise ValueError(
            "A base macroeconômica mensal possui "
            f"{quantidade_datas_invalidas} datas inválidas."
        )

    dados = (
        dados.drop_duplicates(
            subset=["data"],
            keep="last",
        )
        .sort_values("data")
        .reset_index(drop=True)
    )

    return dados, caminho


# ============================================================
# PARÂMETROS DO MODELO DE REGIMES
# ============================================================

def carregar_parametros_regime(
    configuracao: dict[str, Any],
) -> dict[str, Any]:
    """Carrega sinais, limites, regras e confirmação do modelo."""

    config_macro = obter_valor(
        configuracao,
        ("macro",),
    )
    config_regimes = obter_valor(
        configuracao,
        ("regimes",),
    )

    crescimento = config_macro.get("crescimento")
    inflacao = config_macro.get("inflacao")

    if not isinstance(crescimento, dict):
        raise KeyError("A seção macro.crescimento não foi encontrada.")

    if not isinstance(inflacao, dict):
        raise KeyError("A seção macro.inflacao não foi encontrada.")

    coluna_crescimento = str(
        crescimento.get("variavel_modelo", "")
    ).strip()
    coluna_inflacao = str(
        inflacao.get("variavel_modelo", "")
    ).strip()

    if not coluna_crescimento:
        raise ValueError(
            "macro.crescimento.variavel_modelo não pode estar vazio."
        )

    if not coluna_inflacao:
        raise ValueError(
            "macro.inflacao.variavel_modelo não pode estar vazio."
        )

    classificacao_crescimento = crescimento.get(
        "classificacao",
        {},
    )
    classificacao_inflacao = inflacao.get(
        "classificacao",
        {},
    )

    crescimento_alta = str(
        classificacao_crescimento.get(
            "acima_limite",
            "ALTA",
        )
    ).strip().upper()
    crescimento_queda = str(
        classificacao_crescimento.get(
            "abaixo_ou_igual_limite",
            "QUEDA",
        )
    ).strip().upper()

    inflacao_alta = str(
        classificacao_inflacao.get(
            "acima_limite",
            "ALTA",
        )
    ).strip().upper()
    inflacao_queda = str(
        classificacao_inflacao.get(
            "abaixo_ou_igual_limite",
            "QUEDA",
        )
    ).strip().upper()

    lista_regimes = config_regimes.get("lista")
    regras_regimes = config_regimes.get("regras")

    if not isinstance(lista_regimes, list) or not lista_regimes:
        raise ValueError(
            "regimes.lista deve possuir ao menos um regime."
        )

    if not isinstance(regras_regimes, dict) or not regras_regimes:
        raise ValueError(
            "regimes.regras deve possuir as regras de classificação."
        )

    lista_regimes = [
        str(regime).strip().upper()
        for regime in lista_regimes
    ]

    mapa_combinacoes: dict[tuple[str, str], str] = {}

    for regime in lista_regimes:
        regra = regras_regimes.get(regime)

        if not isinstance(regra, dict):
            raise KeyError(
                f"A regra do regime {regime} não foi encontrada."
            )

        combinacao = (
            str(regra.get("crescimento", "")).strip().upper(),
            str(regra.get("inflacao", "")).strip().upper(),
        )

        if not all(combinacao):
            raise ValueError(
                f"A regra do regime {regime} está incompleta."
            )

        if combinacao in mapa_combinacoes:
            raise ValueError(
                "Duas regras de regime utilizam a mesma combinação: "
                f"{combinacao}"
            )

        mapa_combinacoes[combinacao] = regime

    combinacoes_esperadas = {
        (crescimento_alta, inflacao_queda),
        (crescimento_alta, inflacao_alta),
        (crescimento_queda, inflacao_alta),
        (crescimento_queda, inflacao_queda),
    }

    combinacoes_ausentes = (
        combinacoes_esperadas - set(mapa_combinacoes)
    )

    if combinacoes_ausentes:
        raise ValueError(
            "As regras não cobrem todas as combinações necessárias: "
            f"{sorted(combinacoes_ausentes)}"
        )

    confirmacao_meses = int(
        obter_valor(
            configuracao,
            (
                "sinal",
                "modelo_oficial",
                "confirmacao_meses",
            ),
            obrigatorio=False,
            padrao=1,
        )
    )

    if confirmacao_meses <= 0:
        raise ValueError(
            "sinal.modelo_oficial.confirmacao_meses deve ser positivo."
        )

    return {
        "coluna_crescimento": coluna_crescimento,
        "coluna_inflacao": coluna_inflacao,
        "limite_crescimento": float(
            crescimento.get("limite_classificacao", 0.0)
        ),
        "limite_inflacao": float(
            inflacao.get("limite_classificacao", 0.0)
        ),
        "crescimento_alta": crescimento_alta,
        "crescimento_queda": crescimento_queda,
        "inflacao_alta": inflacao_alta,
        "inflacao_queda": inflacao_queda,
        "lista_regimes": lista_regimes,
        "mapa_combinacoes": mapa_combinacoes,
        "confirmacao_meses": confirmacao_meses,
    }


# ============================================================
# CLASSIFICAÇÃO E CONFIRMAÇÃO
# ============================================================

def preparar_base_regimes(
    dados_macro: pd.DataFrame,
    parametros: dict[str, Any],
) -> pd.DataFrame:
    """Seleciona e valida as colunas utilizadas na classificação."""

    coluna_inflacao = parametros["coluna_inflacao"]
    coluna_crescimento = parametros["coluna_crescimento"]

    colunas_contexto = [
        "IPCA_MENSAL_PCT",
        "IPCA_12M_PCT",
        coluna_inflacao,
        "IBC_BR_DESSAZONALIZADO",
        "IBC_BR_MEDIA_MOVEL_3M",
        coluna_crescimento,
    ]

    colunas_obrigatorias = [
        "data",
        coluna_inflacao,
        coluna_crescimento,
    ]

    colunas_ausentes = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in dados_macro.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            "Colunas obrigatórias ausentes na base macroeconômica: "
            f"{colunas_ausentes}"
        )

    colunas_saida = [
        "data",
        *[
            coluna
            for coluna in colunas_contexto
            if coluna in dados_macro.columns
        ],
    ]

    # Remove repetições quando uma coluna de sinal também aparece
    # na lista de contexto.
    colunas_saida = list(dict.fromkeys(colunas_saida))

    dados_regimes = dados_macro[colunas_saida].copy()

    for coluna in {
        coluna_inflacao,
        coluna_crescimento,
        *[
            coluna
            for coluna in colunas_contexto
            if coluna in dados_regimes.columns
        ],
    }:
        if coluna == "data":
            continue

        dados_regimes[coluna] = pd.to_numeric(
            dados_regimes[coluna],
            errors="coerce",
        )

    dados_regimes = (
        dados_regimes.dropna(
            subset=[
                coluna_inflacao,
                coluna_crescimento,
            ]
        )
        .sort_values("data")
        .reset_index(drop=True)
    )

    if dados_regimes.empty:
        raise ValueError(
            "Nenhum mês válido permaneceu para classificar os regimes."
        )

    return dados_regimes


def classificar_regimes_detectados(
    dados_regimes: pd.DataFrame,
    parametros: dict[str, Any],
) -> pd.DataFrame:
    """Classifica o regime detectado de cada mês."""

    dados = dados_regimes.copy()

    coluna_crescimento = parametros["coluna_crescimento"]
    coluna_inflacao = parametros["coluna_inflacao"]

    dados["tendencia_crescimento"] = np.where(
        dados[coluna_crescimento]
        > parametros["limite_crescimento"],
        parametros["crescimento_alta"],
        parametros["crescimento_queda"],
    )

    dados["tendencia_inflacao"] = np.where(
        dados[coluna_inflacao]
        > parametros["limite_inflacao"],
        parametros["inflacao_alta"],
        parametros["inflacao_queda"],
    )

    combinacoes = list(
        zip(
            dados["tendencia_crescimento"],
            dados["tendencia_inflacao"],
        )
    )

    dados["regime_detectado"] = [
        parametros["mapa_combinacoes"].get(
            combinacao,
            "NAO_CLASSIFICADO",
        )
        for combinacao in combinacoes
    ]

    if dados["regime_detectado"].eq("NAO_CLASSIFICADO").any():
        linhas = dados.loc[
            dados["regime_detectado"].eq("NAO_CLASSIFICADO"),
            [
                "data",
                "tendencia_crescimento",
                "tendencia_inflacao",
            ],
        ]

        raise ValueError(
            "Existem meses sem classificação de regime:\n"
            + linhas.to_string(index=False)
        )

    mapa_codigos = {
        regime: indice
        for indice, regime in enumerate(
            parametros["lista_regimes"],
            start=1,
        )
    }

    dados["codigo_regime_detectado"] = (
        dados["regime_detectado"]
        .map(mapa_codigos)
        .astype("Int64")
    )

    return dados


def confirmar_regimes(
    regimes_detectados: pd.Series,
    confirmacao_meses: int,
) -> pd.DataFrame:
    """
    Confirma uma mudança somente após o mesmo regime candidato
    aparecer pelo número configurado de meses consecutivos.
    """

    if regimes_detectados.empty:
        raise ValueError(
            "A série de regimes detectados está vazia."
        )

    regime_confirmado_atual: str | None = None
    regime_candidato_atual: str | None = None
    meses_candidato = 0

    registros: list[dict[str, Any]] = []

    for regime_detectado in regimes_detectados.astype(str):
        mudanca_confirmada = False

        if regime_confirmado_atual is None:
            regime_confirmado_atual = regime_detectado
            regime_candidato_atual = None
            meses_candidato = 0

        elif regime_detectado == regime_confirmado_atual:
            regime_candidato_atual = None
            meses_candidato = 0

        else:
            if regime_detectado == regime_candidato_atual:
                meses_candidato += 1
            else:
                regime_candidato_atual = regime_detectado
                meses_candidato = 1

            if meses_candidato >= confirmacao_meses:
                regime_confirmado_atual = regime_candidato_atual
                regime_candidato_atual = None
                meses_candidato = 0
                mudanca_confirmada = True

        registros.append(
            {
                "regime_candidato": (
                    regime_candidato_atual
                    if regime_candidato_atual is not None
                    else ""
                ),
                "meses_regime_candidato": meses_candidato,
                "regime_confirmado": regime_confirmado_atual,
                "mudanca_regime_confirmada": mudanca_confirmada,
            }
        )

    return pd.DataFrame(registros)


def classificar_e_confirmar_regimes(
    dados_regimes: pd.DataFrame,
    parametros: dict[str, Any],
) -> pd.DataFrame:
    """Executa a classificação detectada e a confirmação oficial."""

    dados = classificar_regimes_detectados(
        dados_regimes=dados_regimes,
        parametros=parametros,
    )

    confirmacao = confirmar_regimes(
        regimes_detectados=dados["regime_detectado"],
        confirmacao_meses=parametros["confirmacao_meses"],
    )

    dados = pd.concat(
        [
            dados.reset_index(drop=True),
            confirmacao.reset_index(drop=True),
        ],
        axis=1,
    )

    mapa_codigos = {
        regime: indice
        for indice, regime in enumerate(
            parametros["lista_regimes"],
            start=1,
        )
    }

    dados["codigo_regime_confirmado"] = (
        dados["regime_confirmado"]
        .map(mapa_codigos)
        .astype("Int64")
    )

    dados["regime_detectado_anterior"] = (
        dados["regime_detectado"].shift(1)
    )
    dados["mudanca_regime_detectada"] = (
        dados["regime_detectado"]
        != dados["regime_detectado_anterior"]
    )

    dados.loc[
        dados.index[0],
        "mudanca_regime_detectada",
    ] = False

    dados["regime_confirmado_anterior"] = (
        dados["regime_confirmado"].shift(1)
    )

    # Colunas oficiais usadas pelas próximas etapas.
    dados["regime_macro"] = dados["regime_confirmado"]
    dados["codigo_regime"] = dados["codigo_regime_confirmado"]
    dados["regime_anterior"] = dados["regime_confirmado_anterior"]
    dados["mudanca_regime"] = (
        dados["mudanca_regime_confirmada"].astype(bool)
    )

    return dados


# ============================================================
# RESUMOS E VALIDAÇÕES
# ============================================================

def criar_resumo_regimes(
    dados: pd.DataFrame,
) -> pd.DataFrame:
    """Cria o resumo dos regimes detectados e confirmados."""

    resumos: list[pd.DataFrame] = []

    for tipo, coluna in [
        ("DETECTADO", "regime_detectado"),
        ("CONFIRMADO", "regime_confirmado"),
    ]:
        resumo = (
            dados[coluna]
            .value_counts(dropna=False)
            .rename_axis("regime_macro")
            .reset_index(name="quantidade_meses")
        )

        resumo["percentual"] = (
            resumo["quantidade_meses"]
            / len(dados)
            * 100.0
        ).round(2)

        resumo.insert(0, "tipo_classificacao", tipo)
        resumos.append(resumo)

    return pd.concat(
        resumos,
        ignore_index=True,
    )


def criar_transicoes_regime(
    dados: pd.DataFrame,
) -> pd.DataFrame:
    """Seleciona somente as mudanças confirmadas de regime."""

    colunas = [
        "data",
        "regime_anterior",
        "regime_macro",
        "regime_detectado",
        "tendencia_inflacao",
        "tendencia_crescimento",
    ]

    return (
        dados.loc[
            dados["mudanca_regime"].astype(bool),
            colunas,
        ]
        .copy()
        .reset_index(drop=True)
    )


def criar_validacoes(
    dados: pd.DataFrame,
    parametros: dict[str, Any],
) -> pd.DataFrame:
    """Cria verificações técnicas da classificação."""

    validacoes: list[dict[str, Any]] = []

    def adicionar(
        nome: str,
        correto: bool,
        detalhe: str,
    ) -> None:
        validacoes.append(
            {
                "validacao_tecnica": nome,
                "status": "OK" if correto else "ERRO",
                "detalhe": detalhe,
            }
        )

    adicionar(
        "Base classificada não vazia",
        not dados.empty,
        f"{len(dados)} meses",
    )

    adicionar(
        "Nenhum regime detectado não classificado",
        not dados["regime_detectado"].eq(
            "NAO_CLASSIFICADO"
        ).any(),
        (
            f"{int(dados['regime_detectado'].eq('NAO_CLASSIFICADO').sum())} "
            "meses não classificados"
        ),
    )

    adicionar(
        "Regimes detectados pertencem à configuração",
        set(dados["regime_detectado"]).issubset(
            set(parametros["lista_regimes"])
        ),
        str(sorted(dados["regime_detectado"].unique())),
    )

    adicionar(
        "Regimes confirmados pertencem à configuração",
        set(dados["regime_confirmado"]).issubset(
            set(parametros["lista_regimes"])
        ),
        str(sorted(dados["regime_confirmado"].unique())),
    )

    adicionar(
        "Códigos detectados preenchidos",
        dados["codigo_regime_detectado"].notna().all(),
        (
            f"{int(dados['codigo_regime_detectado'].isna().sum())} "
            "códigos ausentes"
        ),
    )

    adicionar(
        "Códigos confirmados preenchidos",
        dados["codigo_regime_confirmado"].notna().all(),
        (
            f"{int(dados['codigo_regime_confirmado'].isna().sum())} "
            "códigos ausentes"
        ),
    )

    adicionar(
        "Datas sem duplicidade",
        not dados["data"].duplicated().any(),
        f"{int(dados['data'].duplicated().sum())} duplicidades",
    )

    adicionar(
        "Datas ordenadas",
        dados["data"].is_monotonic_increasing,
        "Ordem cronológica verificada",
    )

    adicionar(
        "Confirmação mensal válida",
        parametros["confirmacao_meses"] >= 1,
        f"{parametros['confirmacao_meses']} mês(es)",
    )

    return pd.DataFrame(validacoes)


# ============================================================
# ESTADO ATUAL DO MODELO
# ============================================================

def salvar_estado_regime(
    configuracao: dict[str, Any],
    dados: pd.DataFrame,
    parametros: dict[str, Any],
) -> Path | None:
    """Salva o último regime confirmado quando habilitado no config."""

    salvar_estado = bool(
        obter_valor(
            configuracao,
            (
                "estado_modelo",
                "salvar_regime_confirmado",
            ),
            obrigatorio=False,
            padrao=False,
        )
    )

    if not salvar_estado:
        return None

    caminho_config = obter_valor(
        configuracao,
        (
            "estado_modelo",
            "arquivo_regime_atual",
        ),
        obrigatorio=False,
        padrao="data/state/regime_atual.json",
    )

    caminho = resolver_caminho(caminho_config)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    ultimo = dados.iloc[-1]

    estado = {
        "data_referencia": pd.Timestamp(
            ultimo["data"]
        ).date().isoformat(),
        "regime_detectado": str(
            ultimo["regime_detectado"]
        ),
        "regime_confirmado": str(
            ultimo["regime_confirmado"]
        ),
        "codigo_regime": int(
            ultimo["codigo_regime"]
        ),
        "regime_candidato": str(
            ultimo["regime_candidato"]
        ),
        "meses_regime_candidato": int(
            ultimo["meses_regime_candidato"]
        ),
        "confirmacao_meses": int(
            parametros["confirmacao_meses"]
        ),
        "atualizado_em_utc": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    caminho.write_text(
        json.dumps(
            estado,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return caminho


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main() -> None:
    """Executa a classificação dos regimes macroeconômicos."""

    inicio_execucao = datetime.now(timezone.utc)

    configuracao = carregar_configuracao()
    parametros = carregar_parametros_regime(configuracao)
    dados_macro, arquivo_entrada = carregar_dados_macro(
        configuracao
    )

    dados_regimes = preparar_base_regimes(
        dados_macro=dados_macro,
        parametros=parametros,
    )

    regimes_macroeconomicos = classificar_e_confirmar_regimes(
        dados_regimes=dados_regimes,
        parametros=parametros,
    )

    resumo_regimes = criar_resumo_regimes(
        regimes_macroeconomicos
    )
    transicoes_regimes = criar_transicoes_regime(
        regimes_macroeconomicos
    )
    validacoes = criar_validacoes(
        dados=regimes_macroeconomicos,
        parametros=parametros,
    )

    config_saidas = obter_valor(
        configuracao,
        ("regimes", "arquivos_saida"),
        obrigatorio=False,
        padrao={},
    )

    arquivo_regimes = resolver_caminho(
        config_saidas.get(
            "classificacao",
            "data/processed/regimes_macroeconomicos.csv",
        )
    )
    arquivo_resumo = resolver_caminho(
        config_saidas.get(
            "resumo",
            "data/processed/resumo_regimes_macroeconomicos.csv",
        )
    )
    arquivo_transicoes = resolver_caminho(
        config_saidas.get(
            "transicoes",
            "data/processed/transicoes_regimes_macroeconomicos.csv",
        )
    )
    arquivo_validacoes = resolver_caminho(
        config_saidas.get(
            "validacoes",
            "outputs/tabelas/03_validacoes_regimes_macroeconomicos.csv",
        )
    )

    salvar_csv_validado(
        regimes_macroeconomicos,
        arquivo_regimes,
    )
    salvar_csv_validado(
        resumo_regimes,
        arquivo_resumo,
    )
    salvar_csv_validado(
        transicoes_regimes,
        arquivo_transicoes,
    )
    salvar_csv_validado(
        validacoes,
        arquivo_validacoes,
    )

    estado_regime = salvar_estado_regime(
        configuracao=configuracao,
        dados=regimes_macroeconomicos,
        parametros=parametros,
    )

    if validacoes["status"].eq("ERRO").any():
        raise RuntimeError(
            "Uma ou mais validações da classificação de regimes falharam."
        )

    ultimo = regimes_macroeconomicos.iloc[-1]
    quantidade_mudancas = int(
        regimes_macroeconomicos["mudanca_regime"].sum()
    )

    fim_execucao = datetime.now(timezone.utc)

    print("=" * 80)
    print("03 — CLASSIFICAÇÃO DOS REGIMES MACROECONÔMICOS")
    print("=" * 80)
    print(f"Arquivo de entrada: {arquivo_entrada}")
    print(
        "Indicador de inflação: "
        f"{parametros['coluna_inflacao']} | "
        f"limite {parametros['limite_inflacao']}"
    )
    print(
        "Indicador de crescimento: "
        f"{parametros['coluna_crescimento']} | "
        f"limite {parametros['limite_crescimento']}"
    )
    print(
        f"Confirmação oficial: "
        f"{parametros['confirmacao_meses']} mês(es)"
    )
    print(
        f"Meses classificados: {len(regimes_macroeconomicos)}"
    )
    print(
        f"Período: "
        f"{regimes_macroeconomicos['data'].min():%d/%m/%Y} a "
        f"{regimes_macroeconomicos['data'].max():%d/%m/%Y}"
    )
    print(
        f"Mudanças confirmadas: {quantidade_mudancas}"
    )
    print(
        f"Último regime detectado: {ultimo['regime_detectado']}"
    )
    print(
        f"Último regime confirmado: {ultimo['regime_confirmado']}"
    )
    print(f"Classificação salva em: {arquivo_regimes}")
    print(f"Resumo salvo em: {arquivo_resumo}")
    print(f"Transições salvas em: {arquivo_transicoes}")
    print(f"Validações salvas em: {arquivo_validacoes}")

    if estado_regime is not None:
        print(f"Estado atual salvo em: {estado_regime}")

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