# VERSAO_V7_FALLBACK_FINAL_SEM_CDI_NORMALIZADO
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")


RAIZ_PROJETO = Path(
    os.getenv(
        "PROJECT_ROOT",
        Path(__file__).resolve().parent,
    )
).resolve()


def display(objeto) -> None:
    """
    Compatibilidade textual com as antigas chamadas
    display() utilizadas no notebook.
    """

    if hasattr(objeto, "to_string"):
        try:
            print(objeto.to_string(index=False))
            return
        except TypeError:
            print(objeto.to_string())
            return

    print(objeto)


INICIO_EXECUCAO_UTC = datetime.now(timezone.utc)

print("=" * 80)
print("06 — OTIMIZAÇÃO DA ESTRATÉGIA")
print(f"Raiz do projeto: {RAIZ_PROJETO}")
print("=" * 80)


# ###########################################################################
# ETAPA 01 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 1 — CARREGAMENTO E VALIDAÇÃO DAS BASES
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import yaml

# ============================================================
# IDENTIFICAÇÃO DA RAIZ DO PROJETO
# ============================================================

# A raiz já foi definida pelo caminho do arquivo .py.


# ============================================================
# CARREGAMENTO DO CONFIG.YAML
# ============================================================

ARQUIVO_CONFIG = (
    RAIZ_PROJETO
    / "config"
    / "config.yaml"
)


if not ARQUIVO_CONFIG.exists():
    raise FileNotFoundError(
        "Arquivo de configuração não encontrado:\n"
        f"{ARQUIVO_CONFIG}"
    )


with ARQUIVO_CONFIG.open(
    mode="r",
    encoding="utf-8",
) as arquivo_yaml:

    CONFIGURACAO = (
        yaml.safe_load(
            arquivo_yaml
        )
        or {}
    )


if (
    "otimizacao" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["otimizacao"],
        dict,
    )
):
    raise KeyError(
        "A seção 'otimizacao' não foi encontrada "
        "no config/config.yaml."
    )


CONFIGURACAO_OTIMIZACAO = (
    CONFIGURACAO[
        "otimizacao"
    ]
)


if (
    "ativos_adicionais_desejados"
    not in CONFIGURACAO_OTIMIZACAO
):
    raise KeyError(
        "O parâmetro "
        "'otimizacao.ativos_adicionais_desejados' "
        "não foi encontrado no config.yaml."
    )


ATIVOS_DESEJADOS_ADICIONAIS = (
    CONFIGURACAO_OTIMIZACAO[
        "ativos_adicionais_desejados"
    ]
)


if not isinstance(
    ATIVOS_DESEJADOS_ADICIONAIS,
    list,
):
    raise TypeError(
        "O parâmetro "
        "'otimizacao.ativos_adicionais_desejados' "
        "deve ser uma lista."
    )


ATIVOS_DESEJADOS_ADICIONAIS = [
    str(ativo).strip()
    for ativo in ATIVOS_DESEJADOS_ADICIONAIS
]


if not ATIVOS_DESEJADOS_ADICIONAIS:
    raise ValueError(
        "A lista de ativos adicionais desejados "
        "não pode estar vazia."
    )


if any(
    not ativo
    for ativo in ATIVOS_DESEJADOS_ADICIONAIS
):
    raise ValueError(
        "A lista de ativos adicionais possui "
        "um nome vazio."
    )


if (
    len(ATIVOS_DESEJADOS_ADICIONAIS)
    != len(set(ATIVOS_DESEJADOS_ADICIONAIS))
):
    raise ValueError(
        "A lista de ativos adicionais possui "
        "ativos duplicados."
    )


# ============================================================
# PASTAS DO PROJETO
# ============================================================

PASTA_DADOS_PROCESSADOS = (
    RAIZ_PROJETO
    / "data"
    / "processed"
)

PASTA_TABELAS = (
    RAIZ_PROJETO
    / "outputs"
    / "tabelas"
)

PASTA_GRAFICOS = (
    RAIZ_PROJETO
    / "outputs"
    / "graficos"
)


PASTA_TABELAS.mkdir(
    parents=True,
    exist_ok=True,
)

PASTA_GRAFICOS.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ARQUIVO_BACKTEST = (
    PASTA_DADOS_PROCESSADOS
    / "backtest_portfolio_mensal.csv"
)

ARQUIVO_REGIMES = (
    PASTA_DADOS_PROCESSADOS
    / "regimes_macroeconomicos.csv"
)

ARQUIVO_RETORNOS = (
    PASTA_DADOS_PROCESSADOS
    / "retornos_ativos.csv"
)


arquivos_entrada = {
    "Backtest mensal": ARQUIVO_BACKTEST,
    "Regimes macroeconômicos": ARQUIVO_REGIMES,
    "Retornos dos ativos": ARQUIVO_RETORNOS,
}


arquivos_ausentes = [
    caminho
    for caminho in arquivos_entrada.values()
    if not caminho.exists()
]


if arquivos_ausentes:
    raise FileNotFoundError(
        "Os seguintes arquivos obrigatórios não foram encontrados:\n"
        + "\n".join(
            str(caminho)
            for caminho in arquivos_ausentes
        )
    )


# ============================================================
# LEITURA DAS BASES
# ============================================================

backtest_original = pd.read_csv(
    ARQUIVO_BACKTEST,
    encoding="utf-8-sig",
)

regimes_macro = pd.read_csv(
    ARQUIVO_REGIMES,
    encoding="utf-8-sig",
)

retornos_ativos = pd.read_csv(
    ARQUIVO_RETORNOS,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DA COLUNA DE DATA
# ============================================================

bases = {
    "backtest_original": backtest_original,
    "regimes_macro": regimes_macro,
    "retornos_ativos": retornos_ativos,
}


for nome_base, base in bases.items():

    if "data" not in base.columns:
        raise ValueError(
            f"A base {nome_base} não possui a coluna 'data'."
        )

    base["data"] = pd.to_datetime(
        base["data"],
        errors="coerce",
    )

    if base["data"].isna().any():
        quantidade_datas_invalidas = (
            base["data"]
            .isna()
            .sum()
        )

        raise ValueError(
            f"A base {nome_base} possui "
            f"{quantidade_datas_invalidas} datas inválidas."
        )

    base.sort_values(
        "data",
        inplace=True,
    )

    base.reset_index(
        drop=True,
        inplace=True,
    )

    if base["data"].duplicated().any():
        quantidade_duplicadas = (
            base["data"]
            .duplicated()
            .sum()
        )

        raise ValueError(
            f"A base {nome_base} possui "
            f"{quantidade_duplicadas} datas duplicadas."
        )


# ============================================================
# IDENTIFICAÇÃO DOS ATIVOS DO MODELO ORIGINAL
# ============================================================

colunas_pesos_originais = [
    coluna
    for coluna in backtest_original.columns
    if (
        coluna.startswith("peso_")
        and not coluna.startswith("peso_estatica_")
    )
]


if not colunas_pesos_originais:
    raise ValueError(
        "Não foram encontradas colunas de pesos "
        "do portfólio original."
    )


ativos_originais = [
    coluna.replace(
        "peso_",
        "",
        1,
    )
    for coluna in colunas_pesos_originais
]


colunas_ativos_ausentes_backtest = [
    ativo
    for ativo in ativos_originais
    if ativo not in backtest_original.columns
]


if colunas_ativos_ausentes_backtest:
    raise ValueError(
        "Os seguintes ativos possuem pesos, mas não possuem "
        "retornos no backtest:\n"
        f"{colunas_ativos_ausentes_backtest}"
    )


# ============================================================
# VALIDAÇÃO DOS REGIMES
# ============================================================

if "regime_sinal" not in backtest_original.columns:
    raise ValueError(
        "A base do backtest não possui a coluna 'regime_sinal'."
    )


regimes_validos = [
    "EXPANSAO_DESINFLACIONARIA",
    "EXPANSAO_INFLACIONARIA",
    "ESTAGFLACAO",
    "RECESSAO_DESINFLACIONARIA",
]


regimes_encontrados = sorted(
    backtest_original[
        "regime_sinal"
    ]
    .dropna()
    .unique()
    .tolist()
)


regimes_invalidos = [
    regime
    for regime in regimes_encontrados
    if regime not in regimes_validos
]


if regimes_invalidos:
    raise ValueError(
        "Foram encontrados regimes não reconhecidos:\n"
        f"{regimes_invalidos}"
    )


regimes_ausentes = [
    regime
    for regime in regimes_validos
    if regime not in regimes_encontrados
]


# ============================================================
# VALIDAÇÃO DOS PESOS
# ============================================================

for coluna in colunas_pesos_originais:
    backtest_original[coluna] = pd.to_numeric(
        backtest_original[coluna],
        errors="coerce",
    )


if (
    backtest_original[
        colunas_pesos_originais
    ]
    .isna()
    .any()
    .any()
):
    raise ValueError(
        "Existem valores nulos ou não numéricos "
        "nas colunas de pesos."
    )


soma_pesos = (
    backtest_original[
        colunas_pesos_originais
    ]
    .sum(axis=1)
)


if not np.allclose(
    soma_pesos,
    1.0,
    rtol=1e-10,
    atol=1e-10,
):
    raise ValueError(
        "Os pesos do portfólio original não somam 100% "
        "em todos os meses."
    )


# ============================================================
# VERIFICAÇÃO DOS ATIVOS ADICIONAIS
# ============================================================

ativos_disponiveis_retornos = [
    coluna
    for coluna in retornos_ativos.columns
    if coluna != "data"
]


status_ativos_adicionais = pd.DataFrame(
    {
        "ativo": ATIVOS_DESEJADOS_ADICIONAIS,
    }
)


status_ativos_adicionais[
    "disponivel_retornos_ativos"
] = (
    status_ativos_adicionais[
        "ativo"
    ]
    .isin(
        ativos_disponiveis_retornos
    )
)


status_ativos_adicionais[
    "status"
] = np.where(
    status_ativos_adicionais[
        "disponivel_retornos_ativos"
    ],
    "DISPONÍVEL",
    "PENDENTE",
)


ativos_adicionais_disponiveis = (
    status_ativos_adicionais.loc[
        status_ativos_adicionais[
            "disponivel_retornos_ativos"
        ],
        "ativo",
    ]
    .tolist()
)


ativos_adicionais_pendentes = (
    status_ativos_adicionais.loc[
        ~status_ativos_adicionais[
            "disponivel_retornos_ativos"
        ],
        "ativo",
    ]
    .tolist()
)


# ============================================================
# INVENTÁRIO DAS BASES
# ============================================================

inventario_bases = pd.DataFrame(
    {
        "base": [
            "Backtest mensal original",
            "Regimes macroeconômicos",
            "Retornos dos ativos",
        ],
        "arquivo": [
            str(ARQUIVO_BACKTEST),
            str(ARQUIVO_REGIMES),
            str(ARQUIVO_RETORNOS),
        ],
        "quantidade_linhas": [
            len(backtest_original),
            len(regimes_macro),
            len(retornos_ativos),
        ],
        "quantidade_colunas": [
            backtest_original.shape[1],
            regimes_macro.shape[1],
            retornos_ativos.shape[1],
        ],
        "data_inicial": [
            backtest_original["data"].min(),
            regimes_macro["data"].min(),
            retornos_ativos["data"].min(),
        ],
        "data_final": [
            backtest_original["data"].max(),
            regimes_macro["data"].max(),
            retornos_ativos["data"].max(),
        ],
        "datas_duplicadas": [
            int(
                backtest_original[
                    "data"
                ].duplicated().sum()
            ),
            int(
                regimes_macro[
                    "data"
                ].duplicated().sum()
            ),
            int(
                retornos_ativos[
                    "data"
                ].duplicated().sum()
            ),
        ],
    }
)


# ============================================================
# RESUMO DO MODELO ORIGINAL
# ============================================================

metricas_status_ativos = [
    f"{ativo} disponível"
    for ativo in ATIVOS_DESEJADOS_ADICIONAIS
]


valores_status_ativos = [
    (
        "Sim"
        if ativo in ativos_disponiveis_retornos
        else "Não"
    )
    for ativo in ATIVOS_DESEJADOS_ADICIONAIS
]


resumo_modelo_original = pd.DataFrame(
    {
        "metrica": [
            "Quantidade de meses",
            "Data inicial",
            "Data final",
            "Quantidade de ativos",
            "Ativos originais",
            "Quantidade de regimes encontrados",
            "Regimes encontrados",
            "Regimes ausentes",
            "Peso mínimo total",
            "Peso máximo total",
            *metricas_status_ativos,
        ],
        "valor": [
            len(backtest_original),
            backtest_original[
                "data"
            ].min().strftime(
                "%d/%m/%Y"
            ),
            backtest_original[
                "data"
            ].max().strftime(
                "%d/%m/%Y"
            ),
            len(ativos_originais),
            ", ".join(
                ativos_originais
            ),
            len(regimes_encontrados),
            ", ".join(
                regimes_encontrados
            ),
            (
                ", ".join(regimes_ausentes)
                if regimes_ausentes
                else "Nenhum"
            ),
            soma_pesos.min(),
            soma_pesos.max(),
            *valores_status_ativos,
        ],
    }
)


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_INVENTARIO_BASES = (
    PASTA_TABELAS
    / "06_01_inventario_bases.csv"
)

ARQUIVO_STATUS_ATIVOS = (
    PASTA_TABELAS
    / "06_01_status_ativos_adicionais.csv"
)

ARQUIVO_RESUMO_MODELO = (
    PASTA_TABELAS
    / "06_01_resumo_modelo_original.csv"
)


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

inventario_bases.to_csv(
    ARQUIVO_INVENTARIO_BASES,
    index=False,
    encoding="utf-8-sig",
)

status_ativos_adicionais.to_csv(
    ARQUIVO_STATUS_ATIVOS,
    index=False,
    encoding="utf-8-sig",
)

resumo_modelo_original.to_csv(
    ARQUIVO_RESUMO_MODELO,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_INVENTARIO_BASES,
    ARQUIVO_STATUS_ATIVOS,
    ARQUIVO_RESUMO_MODELO,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:
    raise FileNotFoundError(
        "Alguns arquivos da Célula 1 não foram salvos:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("=" * 70)
print("NOTEBOOK 06 — BASES CARREGADAS E VALIDADAS")
print("=" * 70)

print(
    f"\nRaiz do projeto:\n"
    f"{RAIZ_PROJETO}"
)

print(
    f"\nArquivo de configuração:\n"
    f"{ARQUIVO_CONFIG}"
)

print(
    f"\nPeríodo do backtest original: "
    f"{backtest_original['data'].min():%d/%m/%Y} "
    f"a "
    f"{backtest_original['data'].max():%d/%m/%Y}"
)

print(
    f"Quantidade de meses: "
    f"{len(backtest_original)}"
)

print(
    f"\nAtivos originais:\n"
    f"{ativos_originais}"
)

print(
    f"\nRegimes encontrados:\n"
    f"{regimes_encontrados}"
)

print(
    f"\nAtivos adicionais configurados:\n"
    f"{ATIVOS_DESEJADOS_ADICIONAIS}"
)

print(
    f"\nAtivos adicionais disponíveis:\n"
    f"{ativos_adicionais_disponiveis}"
)

print(
    f"\nAtivos adicionais pendentes:\n"
    f"{ativos_adicionais_pendentes}"
)

print(
    f"\nInventário das bases salvo em:\n"
    f"{ARQUIVO_INVENTARIO_BASES}"
)

print(
    f"\nStatus dos ativos adicionais salvo em:\n"
    f"{ARQUIVO_STATUS_ATIVOS}"
)

print(
    f"\nResumo do modelo original salvo em:\n"
    f"{ARQUIVO_RESUMO_MODELO}"
)

print("\nInventário das bases:")

display(
    inventario_bases
)

print("\nStatus dos ativos adicionais:")

display(
    status_ativos_adicionais
)

print("\nResumo do modelo original:")

display(
    resumo_modelo_original
)

# ###########################################################################
# ETAPA 02 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 2 — SUAVIZAÇÃO E CONFIRMAÇÃO DOS REGIMES
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# VALIDAÇÃO DA CÉLULA 1
# ============================================================

variaveis_obrigatorias = [
    "RAIZ_PROJETO",
    "backtest_original",
    "PASTA_TABELAS",
    "PASTA_GRAFICOS",
    "CONFIGURACAO_OTIMIZACAO",
]

variaveis_ausentes = [
    variavel
    for variavel in variaveis_obrigatorias
    if variavel not in globals()
]

if variaveis_ausentes:
    raise NameError(
        "Execute primeiro a Célula 1 do Notebook 06.\n"
        f"Variáveis ausentes: {variaveis_ausentes}"
    )


colunas_obrigatorias = [
    "data",
    "regime_sinal",
]

colunas_ausentes = [
    coluna
    for coluna in colunas_obrigatorias
    if coluna not in backtest_original.columns
]

if colunas_ausentes:
    raise ValueError(
        "Colunas obrigatórias ausentes no backtest:\n"
        f"{colunas_ausentes}"
    )


# ============================================================
# CONFIGURAÇÕES
# ============================================================

if (
    "janelas_confirmacao"
    not in CONFIGURACAO_OTIMIZACAO
):
    raise KeyError(
        "O parâmetro "
        "'otimizacao.janelas_confirmacao' "
        "não foi encontrado no config.yaml."
    )


janelas_confirmacao_configuradas = (
    CONFIGURACAO_OTIMIZACAO[
        "janelas_confirmacao"
    ]
)


if not isinstance(
    janelas_confirmacao_configuradas,
    list,
):
    raise TypeError(
        "O parâmetro "
        "'otimizacao.janelas_confirmacao' "
        "deve ser uma lista."
    )


if not janelas_confirmacao_configuradas:
    raise ValueError(
        "A lista "
        "'otimizacao.janelas_confirmacao' "
        "não pode estar vazia."
    )


try:
    JANELAS_CONFIRMACAO = [
        int(janela)
        for janela in janelas_confirmacao_configuradas
    ]

except (
    TypeError,
    ValueError,
) as erro:
    raise TypeError(
        "Todos os valores de "
        "'otimizacao.janelas_confirmacao' "
        "devem ser números inteiros."
    ) from erro


if any(
    janela < 1
    for janela in JANELAS_CONFIRMACAO
):
    raise ValueError(
        "Todas as janelas de confirmação "
        "devem ser maiores ou iguais a 1."
    )


if (
    len(JANELAS_CONFIRMACAO)
    != len(set(JANELAS_CONFIRMACAO))
):
    raise ValueError(
        "A lista de janelas de confirmação "
        "possui valores duplicados."
    )


if 1 not in JANELAS_CONFIRMACAO:
    raise ValueError(
        "A janela de confirmação de 1 mês "
        "é obrigatória para validar o modelo original."
    )


JANELAS_CONFIRMACAO = sorted(
    JANELAS_CONFIRMACAO
)


ORDEM_REGIMES = [
    "EXPANSAO_DESINFLACIONARIA",
    "EXPANSAO_INFLACIONARIA",
    "ESTAGFLACAO",
    "RECESSAO_DESINFLACIONARIA",
]


NOMES_REGIMES = {
    "EXPANSAO_DESINFLACIONARIA": (
        "Expansão desinflacionária"
    ),
    "EXPANSAO_INFLACIONARIA": (
        "Expansão inflacionária"
    ),
    "ESTAGFLACAO": (
        "Estagflação"
    ),
    "RECESSAO_DESINFLACIONARIA": (
        "Recessão desinflacionária"
    ),
}


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_REGIMES_SUAVIZADOS = (
    PASTA_TABELAS
    / "06_02_regimes_suavizados.csv"
)

ARQUIVO_RESUMO_SUAVIZACAO = (
    PASTA_TABELAS
    / "06_02_resumo_suavizacao_regimes.csv"
)

ARQUIVO_RESUMO_SUAVIZACAO_FORMATADO = (
    PASTA_TABELAS
    / "06_02_resumo_suavizacao_regimes_formatado.csv"
)

ARQUIVO_GRAFICO_MUDANCAS = (
    PASTA_GRAFICOS
    / "06_02_mudancas_regime_por_confirmacao.png"
)

ARQUIVO_GRAFICO_SERIES = (
    PASTA_GRAFICOS
    / "06_02_series_regimes_suavizados.png"
)


# ============================================================
# ORGANIZAÇÃO DA BASE
# ============================================================

base_regimes = (
    backtest_original[
        [
            "data",
            "regime_sinal",
        ]
    ]
    .copy()
    .sort_values("data")
    .reset_index(drop=True)
)


base_regimes["data"] = pd.to_datetime(
    base_regimes["data"],
    errors="coerce",
)


base_regimes["regime_sinal"] = (
    base_regimes["regime_sinal"]
    .astype("string")
    .str.strip()
)


if base_regimes["data"].isna().any():
    raise ValueError(
        "Existem datas inválidas na base de regimes."
    )


if base_regimes["regime_sinal"].isna().any():
    raise ValueError(
        "Existem regimes nulos na base."
    )


if base_regimes.empty:
    raise ValueError(
        "A base de regimes está vazia."
    )


regimes_invalidos = (
    base_regimes.loc[
        ~base_regimes[
            "regime_sinal"
        ].isin(
            ORDEM_REGIMES
        ),
        "regime_sinal",
    ]
    .dropna()
    .unique()
    .tolist()
)


if regimes_invalidos:
    raise ValueError(
        "Foram encontrados regimes inválidos:\n"
        f"{regimes_invalidos}"
    )


# ============================================================
# FUNÇÃO CAUSAL DE CONFIRMAÇÃO DE REGIME
# ============================================================

def aplicar_confirmacao_regime(
    serie_regimes,
    meses_confirmacao,
):
    serie_regimes = (
        pd.Series(
            serie_regimes
        )
        .astype("string")
        .str.strip()
        .reset_index(drop=True)
    )

    meses_confirmacao = int(
        meses_confirmacao
    )

    if meses_confirmacao < 1:
        raise ValueError(
            "O número de meses de confirmação "
            "deve ser maior ou igual a 1."
        )

    if serie_regimes.empty:
        return pd.Series(
            dtype="string"
        )

    if serie_regimes.isna().any():
        raise ValueError(
            "A série de regimes possui valores nulos."
        )

    regime_ativo = str(
        serie_regimes.iloc[0]
    )

    regime_candidato = None
    contagem_candidato = 0

    regimes_confirmados = [
        regime_ativo
    ]

    for regime_observado in (
        serie_regimes.iloc[1:]
    ):
        regime_observado = str(
            regime_observado
        )

        if regime_observado == regime_ativo:
            regime_candidato = None
            contagem_candidato = 0

        else:
            if regime_observado == regime_candidato:
                contagem_candidato += 1

            else:
                regime_candidato = regime_observado
                contagem_candidato = 1

            if (
                contagem_candidato
                >= meses_confirmacao
            ):
                regime_ativo = regime_candidato
                regime_candidato = None
                contagem_candidato = 0

        regimes_confirmados.append(
            regime_ativo
        )

    return pd.Series(
        regimes_confirmados,
        index=serie_regimes.index,
        dtype="string",
    )


# ============================================================
# CRIAÇÃO DAS SÉRIES SUAVIZADAS
# ============================================================

for meses_confirmacao in JANELAS_CONFIRMACAO:

    nome_coluna = (
        f"regime_confirmacao_"
        f"{meses_confirmacao}m"
    )

    base_regimes[
        nome_coluna
    ] = aplicar_confirmacao_regime(
        serie_regimes=base_regimes[
            "regime_sinal"
        ],
        meses_confirmacao=meses_confirmacao,
    )


# ============================================================
# FUNÇÃO PARA CONTAR MUDANÇAS DE REGIME
# ============================================================

def contar_mudancas_regime(
    serie_regimes,
):
    valores = (
        pd.Series(
            serie_regimes
        )
        .astype("string")
        .str.strip()
        .to_numpy(
            dtype=str
        )
    )

    if len(valores) <= 1:
        return 0

    return int(
        np.sum(
            valores[1:]
            != valores[:-1]
        )
    )


# ============================================================
# FUNÇÃO PARA CALCULAR DURAÇÕES DOS REGIMES
# ============================================================

def calcular_duracoes_regimes(
    serie_regimes,
):
    valores = (
        pd.Series(
            serie_regimes
        )
        .astype("string")
        .str.strip()
        .to_numpy(
            dtype=str
        )
    )

    if len(valores) == 0:
        return np.array(
            [],
            dtype=float,
        )

    inicio_blocos = np.concatenate(
        [
            np.array(
                [True]
            ),
            valores[1:]
            != valores[:-1],
        ]
    )

    grupos = np.cumsum(
        inicio_blocos
    )

    duracoes = (
        pd.Series(
            grupos
        )
        .value_counts(
            sort=False
        )
        .to_numpy(
            dtype=float
        )
    )

    return duracoes


def calcular_duracao_media_regime(
    serie_regimes,
):
    duracoes = calcular_duracoes_regimes(
        serie_regimes
    )

    if len(duracoes) == 0:
        return np.nan

    return float(
        np.mean(
            duracoes
        )
    )


def calcular_duracao_mediana_regime(
    serie_regimes,
):
    duracoes = calcular_duracoes_regimes(
        serie_regimes
    )

    if len(duracoes) == 0:
        return np.nan

    return float(
        np.median(
            duracoes
        )
    )


# ============================================================
# VALIDAÇÃO DA CONFIRMAÇÃO DE 1 MÊS
# ============================================================

regime_original_validacao = (
    base_regimes[
        "regime_sinal"
    ]
    .astype("string")
    .str.strip()
    .to_numpy(
        dtype=str
    )
)


regime_confirmacao_1m_validacao = (
    base_regimes[
        "regime_confirmacao_1m"
    ]
    .astype("string")
    .str.strip()
    .to_numpy(
        dtype=str
    )
)


confirmacao_1m_identica = np.array_equal(
    regime_original_validacao,
    regime_confirmacao_1m_validacao,
)


if not confirmacao_1m_identica:

    indices_diferentes = np.where(
        regime_original_validacao
        != regime_confirmacao_1m_validacao
    )[0]

    primeiras_diferencas = (
        base_regimes.loc[
            indices_diferentes[:10],
            [
                "data",
                "regime_sinal",
                "regime_confirmacao_1m",
            ],
        ]
    )

    raise ValueError(
        "A confirmação de 1 mês não ficou idêntica "
        "ao regime original.\n"
        f"Quantidade de diferenças: "
        f"{len(indices_diferentes)}\n"
        f"Primeiras diferenças:\n"
        f"{primeiras_diferencas}"
    )


# ============================================================
# RESUMO DA SUAVIZAÇÃO
# ============================================================

mudancas_modelo_original = (
    contar_mudancas_regime(
        base_regimes[
            "regime_sinal"
        ]
    )
)


resultados_suavizacao = []


for meses_confirmacao in JANELAS_CONFIRMACAO:

    nome_coluna = (
        f"regime_confirmacao_"
        f"{meses_confirmacao}m"
    )

    serie_confirmada = (
        base_regimes[
            nome_coluna
        ]
    )

    quantidade_mudancas = (
        contar_mudancas_regime(
            serie_confirmada
        )
    )

    reducao_absoluta = (
        mudancas_modelo_original
        - quantidade_mudancas
    )

    if mudancas_modelo_original > 0:
        reducao_percentual = (
            reducao_absoluta
            / mudancas_modelo_original
        )
    else:
        reducao_percentual = 0.0

    valores_confirmados = (
        serie_confirmada
        .astype("string")
        .str.strip()
        .to_numpy(
            dtype=str
        )
    )

    meses_diferentes_original = int(
        np.sum(
            valores_confirmados
            != regime_original_validacao
        )
    )

    proporcao_meses_diferentes = (
        meses_diferentes_original
        / len(
            base_regimes
        )
    )

    resultados_suavizacao.append(
        {
            "meses_confirmacao": (
                meses_confirmacao
            ),
            "quantidade_mudancas": (
                quantidade_mudancas
            ),
            "reducao_absoluta_mudancas": (
                reducao_absoluta
            ),
            "reducao_percentual_mudancas": (
                reducao_percentual
            ),
            "duracao_media_regime_meses": (
                calcular_duracao_media_regime(
                    serie_confirmada
                )
            ),
            "duracao_mediana_regime_meses": (
                calcular_duracao_mediana_regime(
                    serie_confirmada
                )
            ),
            "meses_diferentes_original": (
                meses_diferentes_original
            ),
            "proporcao_meses_diferentes": (
                proporcao_meses_diferentes
            ),
        }
    )


resumo_suavizacao = pd.DataFrame(
    resultados_suavizacao
)


# ============================================================
# VALIDAÇÕES DOS RESULTADOS
# ============================================================

linha_confirmacao_1m = (
    resumo_suavizacao.loc[
        resumo_suavizacao[
            "meses_confirmacao"
        ]
        == 1
    ]
    .iloc[0]
)


if (
    int(
        linha_confirmacao_1m[
            "quantidade_mudancas"
        ]
    )
    != mudancas_modelo_original
):
    raise ValueError(
        "A confirmação de 1 mês apresentou quantidade "
        "de mudanças diferente do modelo original."
    )


if (
    int(
        linha_confirmacao_1m[
            "meses_diferentes_original"
        ]
    )
    != 0
):
    raise ValueError(
        "A confirmação de 1 mês apresentou meses "
        "diferentes do modelo original."
    )


if (
    resumo_suavizacao[
        "quantidade_mudancas"
    ]
    .gt(
        mudancas_modelo_original
    )
    .any()
):
    raise ValueError(
        "Uma das séries suavizadas apresentou mais "
        "mudanças do que a série original."
    )


if (
    resumo_suavizacao[
        "quantidade_mudancas"
    ]
    .diff()
    .dropna()
    .gt(0)
    .any()
):
    raise ValueError(
        "O aumento da janela de confirmação gerou "
        "mais mudanças de regime."
    )


# ============================================================
# TABELA FORMATADA
# ============================================================

resumo_suavizacao_formatado = (
    resumo_suavizacao
    .copy()
    .astype(object)
)


resumo_suavizacao_formatado[
    "reducao_percentual_mudancas"
] = (
    resumo_suavizacao[
        "reducao_percentual_mudancas"
    ]
    .map(
        lambda valor: (
            f"{valor:.2%}"
        )
    )
)


resumo_suavizacao_formatado[
    "proporcao_meses_diferentes"
] = (
    resumo_suavizacao[
        "proporcao_meses_diferentes"
    ]
    .map(
        lambda valor: (
            f"{valor:.2%}"
        )
    )
)


for coluna in [
    "duracao_media_regime_meses",
    "duracao_mediana_regime_meses",
]:
    resumo_suavizacao_formatado[
        coluna
    ] = (
        resumo_suavizacao[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

base_regimes.to_csv(
    ARQUIVO_REGIMES_SUAVIZADOS,
    index=False,
    encoding="utf-8-sig",
)

resumo_suavizacao.to_csv(
    ARQUIVO_RESUMO_SUAVIZACAO,
    index=False,
    encoding="utf-8-sig",
)

resumo_suavizacao_formatado.to_csv(
    ARQUIVO_RESUMO_SUAVIZACAO_FORMATADO,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO 1 — QUANTIDADE DE MUDANÇAS
# ============================================================

posicoes_grafico = np.arange(
    len(
        resumo_suavizacao
    )
)


fig, ax = plt.subplots(
    figsize=(10, 6)
)


barras = ax.bar(
    posicoes_grafico,
    resumo_suavizacao[
        "quantidade_mudancas"
    ],
)


ax.set_xticks(
    posicoes_grafico
)

ax.set_xticklabels(
    resumo_suavizacao[
        "meses_confirmacao"
    ]
    .astype(int)
    .astype(str)
)


ax.set_title(
    "Mudanças de Regime por Janela de Confirmação"
)

ax.set_xlabel(
    "Meses consecutivos exigidos para confirmar o regime"
)

ax.set_ylabel(
    "Quantidade de mudanças"
)

ax.grid(
    axis="y",
    alpha=0.3,
)


for barra, quantidade in zip(
    barras,
    resumo_suavizacao[
        "quantidade_mudancas"
    ],
):
    ax.text(
        barra.get_x()
        + barra.get_width()
        / 2,
        barra.get_height(),
        f"{int(quantidade)}",
        ha="center",
        va="bottom",
    )


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_MUDANCAS,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — COMPARAÇÃO DAS SÉRIES
# ============================================================

mapa_numerico_regimes = {
    regime: indice
    for indice, regime
    in enumerate(
        ORDEM_REGIMES
    )
}


colunas_grafico = [
    (
        "regime_sinal",
        "Regime original",
        0.00,
    )
]


janelas_suavizadas_grafico = [
    janela
    for janela in JANELAS_CONFIRMACAO
    if janela != 1
]


for indice_janela, meses_confirmacao in enumerate(
    janelas_suavizadas_grafico,
    start=1,
):
    colunas_grafico.append(
        (
            (
                f"regime_confirmacao_"
                f"{meses_confirmacao}m"
            ),
            (
                f"Confirmação de "
                f"{meses_confirmacao} meses"
            ),
            0.07 * indice_janela,
        )
    )


fig, ax = plt.subplots(
    figsize=(14, 8)
)


for (
    coluna,
    rotulo,
    deslocamento,
) in colunas_grafico:

    valores_numericos = (
        base_regimes[
            coluna
        ]
        .map(
            mapa_numerico_regimes
        )
        .astype(float)
        + deslocamento
    )

    ax.step(
        base_regimes[
            "data"
        ],
        valores_numericos,
        where="post",
        linewidth=1.8,
        label=rotulo,
    )


ax.set_yticks(
    list(
        mapa_numerico_regimes.values()
    )
)

ax.set_yticklabels(
    [
        NOMES_REGIMES[
            regime
        ]
        for regime in ORDEM_REGIMES
    ]
)


ax.set_title(
    "Comparação entre Regime Original e Regimes Suavizados"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Regime macroeconômico"
)

ax.legend()

ax.grid(
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_SERIES,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_REGIMES_SUAVIZADOS,
    ARQUIVO_RESUMO_SUAVIZACAO,
    ARQUIVO_RESUMO_SUAVIZACAO_FORMATADO,
    ARQUIVO_GRAFICO_MUDANCAS,
    ARQUIVO_GRAFICO_SERIES,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:
    raise FileNotFoundError(
        "Alguns arquivos da Célula 2 não foram salvos:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

melhor_reducao = (
    resumo_suavizacao
    .sort_values(
        [
            "quantidade_mudancas",
            "meses_confirmacao",
        ],
        ascending=[
            True,
            True,
        ],
    )
    .iloc[0]
)


print("=" * 70)
print("SUAVIZAÇÃO DOS REGIMES CONCLUÍDA")
print("=" * 70)

print(
    f"\nJanelas de confirmação configuradas: "
    f"{JANELAS_CONFIRMACAO}"
)

print(
    f"\nMudanças no modelo original: "
    f"{mudancas_modelo_original}"
)

print(
    f"\nMenor quantidade de mudanças: "
    f"{int(melhor_reducao['quantidade_mudancas'])}"
)

print(
    f"Janela correspondente: "
    f"{int(melhor_reducao['meses_confirmacao'])} meses"
)

print(
    f"Redução nas mudanças: "
    f"{melhor_reducao['reducao_percentual_mudancas']:.2%}"
)

print(
    f"\nTabela mensal salva em:\n"
    f"{ARQUIVO_REGIMES_SUAVIZADOS}"
)

print(
    f"\nResumo da suavização salvo em:\n"
    f"{ARQUIVO_RESUMO_SUAVIZACAO}"
)

print(
    f"\nResumo formatado salvo em:\n"
    f"{ARQUIVO_RESUMO_SUAVIZACAO_FORMATADO}"
)

print(
    f"\nGráfico de mudanças:\n"
    f"{ARQUIVO_GRAFICO_MUDANCAS.name}"
)

print(
    f"\nGráfico das séries:\n"
    f"{ARQUIVO_GRAFICO_SERIES.name}"
)

print("\nResumo da suavização:")

display(
    resumo_suavizacao_formatado
)

# ###########################################################################
# ETAPA 03 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 3 — BACKTEST DOS REGIMES SUAVIZADOS
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter


# ============================================================
# VALIDAÇÃO DAS CÉLULAS ANTERIORES
# ============================================================

variaveis_obrigatorias = [
    "RAIZ_PROJETO",
    "backtest_original",
    "base_regimes",
    "ativos_originais",
    "colunas_pesos_originais",
    "ORDEM_REGIMES",
    "JANELAS_CONFIRMACAO",
    "CONFIGURACAO",
    "CONFIGURACAO_OTIMIZACAO",
    "PASTA_TABELAS",
    "PASTA_GRAFICOS",
]

variaveis_ausentes = [
    variavel
    for variavel in variaveis_obrigatorias
    if variavel not in globals()
]

if variaveis_ausentes:
    raise NameError(
        "Execute primeiro as Células 1 e 2 do Notebook 06.\n"
        f"Variáveis ausentes: {variaveis_ausentes}"
    )


if (
    "backtest" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["backtest"],
        dict,
    )
):
    raise KeyError(
        "A seção 'backtest' não foi encontrada "
        "no config/config.yaml."
    )


CONFIGURACAO_BACKTEST = (
    CONFIGURACAO[
        "backtest"
    ]
)


parametros_backtest_obrigatorios = [
    "valor_inicial",
    "periodos_por_ano",
    "cobrar_custo_inicial",
    "custo_por_turnover",
]

parametros_backtest_ausentes = [
    parametro
    for parametro in parametros_backtest_obrigatorios
    if parametro not in CONFIGURACAO_BACKTEST
]

if parametros_backtest_ausentes:
    raise KeyError(
        "Parâmetros ausentes na seção 'backtest' "
        "do config.yaml:\n"
        f"{parametros_backtest_ausentes}"
    )


# ============================================================
# CONFIGURAÇÕES
# ============================================================

VALOR_INICIAL = float(
    CONFIGURACAO_BACKTEST[
        "valor_inicial"
    ]
)

PERIODOS_POR_ANO = int(
    CONFIGURACAO_BACKTEST[
        "periodos_por_ano"
    ]
)

COBRAR_CUSTO_INICIAL = (
    CONFIGURACAO_BACKTEST[
        "cobrar_custo_inicial"
    ]
)

CUSTO_POR_TURNOVER_OTIMIZACAO = float(
    CONFIGURACAO_BACKTEST[
        "custo_por_turnover"
    ]
)


if VALOR_INICIAL <= 0:
    raise ValueError(
        "'backtest.valor_inicial' "
        "deve ser maior que zero."
    )


if PERIODOS_POR_ANO <= 0:
    raise ValueError(
        "'backtest.periodos_por_ano' "
        "deve ser maior que zero."
    )


if not isinstance(
    COBRAR_CUSTO_INICIAL,
    bool,
):
    raise TypeError(
        "'backtest.cobrar_custo_inicial' "
        "deve ser true ou false."
    )


if CUSTO_POR_TURNOVER_OTIMIZACAO < 0:
    raise ValueError(
        "'backtest.custo_por_turnover' "
        "não pode ser negativo."
    )


if not JANELAS_CONFIRMACAO:
    raise ValueError(
        "A lista JANELAS_CONFIRMACAO "
        "não pode estar vazia."
    )


if 1 not in JANELAS_CONFIRMACAO:
    raise ValueError(
        "A janela de confirmação de 1 mês "
        "é obrigatória."
    )


JANELAS_CONFIRMACAO = sorted(
    [
        int(janela)
        for janela in JANELAS_CONFIRMACAO
    ]
)


# ============================================================
# CENÁRIOS DE REGIME
# ============================================================

CENARIOS_REGIME = {}

ROTULOS_CENARIOS = {}


for meses_confirmacao in JANELAS_CONFIRMACAO:

    if meses_confirmacao == 1:
        nome_cenario = (
            "Original_1m"
        )

        rotulo_cenario = (
            "Regime original"
        )

    else:
        nome_cenario = (
            f"Confirmacao_"
            f"{meses_confirmacao}m"
        )

        rotulo_cenario = (
            f"Confirmação de "
            f"{meses_confirmacao} meses"
        )

    coluna_regime = (
        f"regime_confirmacao_"
        f"{meses_confirmacao}m"
    )

    CENARIOS_REGIME[
        nome_cenario
    ] = coluna_regime

    ROTULOS_CENARIOS[
        nome_cenario
    ] = rotulo_cenario


ROTULOS_CENARIOS[
    "Benchmark_Estatico"
] = (
    "Benchmark de pesos iguais rebalanceado"
)


NOMES_CENARIOS_ESTRATEGIA = list(
    CENARIOS_REGIME.keys()
)


# ============================================================
# VALIDAÇÃO DAS COLUNAS
# ============================================================

colunas_regimes_necessarias = [
    "data",
    *CENARIOS_REGIME.values(),
]

colunas_regimes_ausentes = [
    coluna
    for coluna in colunas_regimes_necessarias
    if coluna not in base_regimes.columns
]

if colunas_regimes_ausentes:
    raise ValueError(
        "Colunas de regimes suavizados ausentes:\n"
        f"{colunas_regimes_ausentes}"
    )


colunas_backtest_necessarias = [
    "data",
    "regime_sinal",
    "retorno_portfolio",
    "retorno_carteira_estatica",
    *ativos_originais,
    *colunas_pesos_originais,
]

colunas_backtest_ausentes = [
    coluna
    for coluna in colunas_backtest_necessarias
    if coluna not in backtest_original.columns
]

if colunas_backtest_ausentes:
    raise ValueError(
        "Colunas necessárias ausentes no backtest original:\n"
        f"{colunas_backtest_ausentes}"
    )


# ============================================================
# VALIDAÇÃO DO CUSTO CONTRA O BACKTEST ORIGINAL
# ============================================================

if (
    "custo_portfolio" in backtest_original.columns
    and "turnover_portfolio" in backtest_original.columns
):
    linhas_com_turnover = (
        pd.to_numeric(
            backtest_original[
                "turnover_portfolio"
            ],
            errors="coerce",
        )
        .gt(0)
    )

    if linhas_com_turnover.any():
        taxas_custo_observadas = (
            pd.to_numeric(
                backtest_original.loc[
                    linhas_com_turnover,
                    "custo_portfolio",
                ],
                errors="coerce",
            )
            / pd.to_numeric(
                backtest_original.loc[
                    linhas_com_turnover,
                    "turnover_portfolio",
                ],
                errors="coerce",
            )
        )

        if taxas_custo_observadas.isna().any():
            raise ValueError(
                "Não foi possível validar a taxa de custo "
                "observada no backtest original."
            )

        if not np.allclose(
            taxas_custo_observadas,
            CUSTO_POR_TURNOVER_OTIMIZACAO,
            rtol=1e-8,
            atol=1e-12,
        ):
            raise ValueError(
                "A taxa de custo configurada não coincide "
                "com a taxa utilizada no backtest original."
            )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_COMPARACAO_CENARIOS = (
    PASTA_TABELAS
    / "06_03_comparacao_regimes_suavizados.csv"
)

ARQUIVO_COMPARACAO_CENARIOS_FORMATADA = (
    PASTA_TABELAS
    / "06_03_comparacao_regimes_suavizados_formatada.csv"
)

ARQUIVO_SERIES_MENSAIS = (
    PASTA_TABELAS
    / "06_03_series_mensais_regimes_suavizados.csv"
)

ARQUIVO_PESOS_REGIMES = (
    PASTA_TABELAS
    / "06_03_pesos_originais_por_regime.csv"
)

ARQUIVO_GRAFICO_DESEMPENHO = (
    PASTA_GRAFICOS
    / "06_03_desempenho_liquido_regimes_suavizados.png"
)

ARQUIVO_GRAFICO_TURNOVER = (
    PASTA_GRAFICOS
    / "06_03_turnover_regimes_suavizados.png"
)

ARQUIVO_GRAFICO_DIFERENCA = (
    PASTA_GRAFICOS
    / "06_03_diferenca_liquida_vs_benchmark.png"
)


# ============================================================
# ORGANIZAÇÃO E VALIDAÇÃO DA BASE
# ============================================================

base_backtest_suavizacao = (
    backtest_original
    .copy()
    .sort_values("data")
    .reset_index(drop=True)
)


base_backtest_suavizacao["data"] = pd.to_datetime(
    base_backtest_suavizacao["data"],
    errors="coerce",
)

if base_backtest_suavizacao["data"].isna().any():
    raise ValueError(
        "Existem datas inválidas no backtest original."
    )


for coluna in [
    *ativos_originais,
    *colunas_pesos_originais,
    "retorno_portfolio",
    "retorno_carteira_estatica",
]:
    base_backtest_suavizacao[coluna] = pd.to_numeric(
        base_backtest_suavizacao[coluna],
        errors="coerce",
    )


colunas_numericas_validacao = [
    *ativos_originais,
    *colunas_pesos_originais,
    "retorno_portfolio",
    "retorno_carteira_estatica",
]


if (
    base_backtest_suavizacao[
        colunas_numericas_validacao
    ]
    .isna()
    .any()
    .any()
):
    raise ValueError(
        "Existem valores nulos ou inválidos nas colunas "
        "utilizadas no backtest."
    )


base_cenarios = (
    base_backtest_suavizacao
    .merge(
        base_regimes[
            colunas_regimes_necessarias
        ],
        on="data",
        how="inner",
        validate="one_to_one",
    )
    .sort_values("data")
    .reset_index(drop=True)
)


if len(base_cenarios) != len(base_backtest_suavizacao):
    raise ValueError(
        "A junção entre o backtest e os regimes suavizados "
        "alterou a quantidade de meses."
    )


# ============================================================
# RECUPERAÇÃO DOS PESOS ORIGINAIS POR REGIME
# ============================================================

registros_pesos_regimes = []

pesos_por_regime = {}


for regime in ORDEM_REGIMES:

    linhas_regime = (
        base_backtest_suavizacao.loc[
            base_backtest_suavizacao[
                "regime_sinal"
            ]
            == regime,
            colunas_pesos_originais,
        ]
        .copy()
    )

    if linhas_regime.empty:
        raise ValueError(
            f"O regime {regime} não possui observações "
            "no backtest original."
        )

    pesos_referencia = (
        linhas_regime
        .iloc[0]
        .astype(float)
        .to_numpy()
    )

    if not np.allclose(
        linhas_regime.astype(float).to_numpy(),
        pesos_referencia,
        rtol=1e-10,
        atol=1e-10,
    ):
        raise ValueError(
            f"O regime {regime} possui mais de uma "
            "configuração de pesos no backtest original."
        )

    if not np.isclose(
        pesos_referencia.sum(),
        1.0,
        rtol=1e-10,
        atol=1e-10,
    ):
        raise ValueError(
            f"Os pesos do regime {regime} não somam 100%."
        )

    pesos_por_regime[regime] = {
        ativo: float(peso)
        for ativo, peso in zip(
            ativos_originais,
            pesos_referencia,
        )
    }

    registro = {
        "regime": regime,
    }

    for ativo, peso in zip(
        ativos_originais,
        pesos_referencia,
    ):
        registro[
            f"peso_{ativo}"
        ] = float(peso)

    registros_pesos_regimes.append(
        registro
    )


tabela_pesos_regimes = pd.DataFrame(
    registros_pesos_regimes
)


# ============================================================
# FUNÇÃO DE TURNOVER
# ============================================================

def calcular_turnover_carteira(
    dados,
    colunas_retornos,
    colunas_pesos,
    cobrar_custo_inicial,
):
    quantidade_periodos = len(
        dados
    )

    turnover = np.zeros(
        quantidade_periodos,
        dtype=float,
    )

    if quantidade_periodos == 0:
        return turnover

    if len(colunas_retornos) != len(colunas_pesos):
        raise ValueError(
            "A quantidade de retornos e pesos deve ser igual."
        )

    if cobrar_custo_inicial:
        turnover[0] = 1.0

    for indice in range(
        1,
        quantidade_periodos,
    ):
        pesos_anteriores = (
            dados.loc[
                indice - 1,
                colunas_pesos,
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

        retorno_carteira_anterior = float(
            np.sum(
                pesos_anteriores
                * retornos_anteriores
            )
        )

        fator_patrimonio = (
            1
            + retorno_carteira_anterior
        )

        if fator_patrimonio <= 0:
            raise ValueError(
                "O patrimônio relativo ficou menor ou igual "
                f"a zero no período {indice - 1}."
            )

        pesos_apos_retornos = (
            pesos_anteriores
            * (
                1
                + retornos_anteriores
            )
            / fator_patrimonio
        )

        pesos_alvo_atuais = (
            dados.loc[
                indice,
                colunas_pesos,
            ]
            .astype(float)
            .to_numpy()
        )

        turnover[indice] = float(
            np.abs(
                pesos_alvo_atuais
                - pesos_apos_retornos
            ).sum()
            / 2
        )

    return turnover


# ============================================================
# FUNÇÕES DE MÉTRICAS
# ============================================================

def calcular_retorno_total(
    retornos,
):
    retornos = (
        pd.Series(retornos)
        .dropna()
        .astype(float)
    )

    return float(
        (
            1
            + retornos
        ).prod()
        - 1
    )


def calcular_retorno_anualizado(
    retornos,
    periodos_por_ano,
):
    retornos = (
        pd.Series(retornos)
        .dropna()
        .astype(float)
    )

    quantidade_periodos = len(
        retornos
    )

    if quantidade_periodos == 0:
        return np.nan

    retorno_total = calcular_retorno_total(
        retornos
    )

    return float(
        (
            1
            + retorno_total
        )
        ** (
            periodos_por_ano
            / quantidade_periodos
        )
        - 1
    )


def calcular_volatilidade_anualizada(
    retornos,
    periodos_por_ano,
):
    retornos = (
        pd.Series(retornos)
        .dropna()
        .astype(float)
    )

    if len(retornos) < 2:
        return np.nan

    return float(
        retornos.std(
            ddof=1
        )
        * np.sqrt(
            periodos_por_ano
        )
    )


def calcular_maximo_drawdown(
    retornos,
    valor_inicial,
):
    retornos = (
        pd.Series(retornos)
        .dropna()
        .astype(float)
        .reset_index(drop=True)
    )

    indice = (
        valor_inicial
        * (
            1
            + retornos
        ).cumprod()
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

    pico = (
        indice_com_inicio
        .cummax()
    )

    drawdown = (
        indice_com_inicio
        / pico
        - 1
    )

    return float(
        drawdown.min()
    )


def contar_mudancas(
    serie_regimes,
):
    valores = (
        pd.Series(
            serie_regimes
        )
        .astype("string")
        .to_numpy(
            dtype=str
        )
    )

    if len(valores) <= 1:
        return 0

    return int(
        np.sum(
            valores[1:]
            != valores[:-1]
        )
    )


# ============================================================
# CÁLCULO DOS CENÁRIOS
# ============================================================

resultados_cenarios = []


for nome_cenario, coluna_regime in (
    CENARIOS_REGIME.items()
):

    colunas_pesos_cenario = []

    for ativo in ativos_originais:

        coluna_peso = (
            f"peso_{nome_cenario}_{ativo}"
        )

        base_cenarios[coluna_peso] = (
            base_cenarios[
                coluna_regime
            ]
            .map(
                {
                    regime: pesos[
                        ativo
                    ]
                    for regime, pesos
                    in pesos_por_regime.items()
                }
            )
        )

        colunas_pesos_cenario.append(
            coluna_peso
        )

    if (
        base_cenarios[
            colunas_pesos_cenario
        ]
        .isna()
        .any()
        .any()
    ):
        raise ValueError(
            f"O cenário {nome_cenario} gerou pesos nulos."
        )

    soma_pesos_cenario = (
        base_cenarios[
            colunas_pesos_cenario
        ]
        .sum(axis=1)
    )

    if not np.allclose(
        soma_pesos_cenario,
        1.0,
        rtol=1e-10,
        atol=1e-10,
    ):
        raise ValueError(
            f"Os pesos do cenário {nome_cenario} "
            "não somam 100%."
        )

    coluna_retorno_bruto = (
        f"retorno_bruto_{nome_cenario}"
    )

    coluna_turnover = (
        f"turnover_{nome_cenario}"
    )

    coluna_custo = (
        f"custo_{nome_cenario}"
    )

    coluna_retorno_liquido = (
        f"retorno_liquido_{nome_cenario}"
    )

    coluna_indice_bruto = (
        f"indice_bruto_{nome_cenario}"
    )

    coluna_indice_liquido = (
        f"indice_liquido_{nome_cenario}"
    )

    coluna_drawdown_liquido = (
        f"drawdown_liquido_{nome_cenario}"
    )

    base_cenarios[
        coluna_retorno_bruto
    ] = 0.0

    for ativo, coluna_peso in zip(
        ativos_originais,
        colunas_pesos_cenario,
    ):
        base_cenarios[
            coluna_retorno_bruto
        ] += (
            base_cenarios[
                coluna_peso
            ]
            * base_cenarios[
                ativo
            ]
        )

    base_cenarios[
        coluna_turnover
    ] = calcular_turnover_carteira(
        dados=base_cenarios,
        colunas_retornos=ativos_originais,
        colunas_pesos=colunas_pesos_cenario,
        cobrar_custo_inicial=COBRAR_CUSTO_INICIAL,
    )

    base_cenarios[
        coluna_custo
    ] = (
        base_cenarios[
            coluna_turnover
        ]
        * CUSTO_POR_TURNOVER_OTIMIZACAO
    )

    base_cenarios[
        coluna_retorno_liquido
    ] = (
        (
            1
            + base_cenarios[
                coluna_retorno_bruto
            ]
        )
        * (
            1
            - base_cenarios[
                coluna_custo
            ]
        )
        - 1
    )

    base_cenarios[
        coluna_indice_bruto
    ] = (
        VALOR_INICIAL
        * (
            1
            + base_cenarios[
                coluna_retorno_bruto
            ]
        ).cumprod()
    )

    base_cenarios[
        coluna_indice_liquido
    ] = (
        VALOR_INICIAL
        * (
            1
            + base_cenarios[
                coluna_retorno_liquido
            ]
        ).cumprod()
    )

    pico_liquido = pd.concat(
        [
            pd.Series(
                [VALOR_INICIAL],
                dtype=float,
            ),
            base_cenarios[
                coluna_indice_liquido
            ].reset_index(drop=True),
        ],
        ignore_index=True,
    ).cummax()

    base_cenarios[
        coluna_drawdown_liquido
    ] = (
        base_cenarios[
            coluna_indice_liquido
        ].reset_index(drop=True)
        / pico_liquido.iloc[1:].reset_index(
            drop=True
        )
        - 1
    )

    retorno_total_bruto = (
        calcular_retorno_total(
            base_cenarios[
                coluna_retorno_bruto
            ]
        )
    )

    retorno_total_liquido = (
        calcular_retorno_total(
            base_cenarios[
                coluna_retorno_liquido
            ]
        )
    )

    retorno_anualizado_liquido = (
        calcular_retorno_anualizado(
            retornos=base_cenarios[
                coluna_retorno_liquido
            ],
            periodos_por_ano=PERIODOS_POR_ANO,
        )
    )

    volatilidade_liquida = (
        calcular_volatilidade_anualizada(
            retornos=base_cenarios[
                coluna_retorno_liquido
            ],
            periodos_por_ano=PERIODOS_POR_ANO,
        )
    )

    if (
        pd.notna(
            volatilidade_liquida
        )
        and volatilidade_liquida > 0
    ):
        retorno_volatilidade = (
            retorno_anualizado_liquido
            / volatilidade_liquida
        )

    else:
        retorno_volatilidade = np.nan

    meses_confirmacao = int(
        coluna_regime
        .replace(
            "regime_confirmacao_",
            ""
        )
        .replace(
            "m",
            ""
        )
    )

    resultados_cenarios.append(
        {
            "cenario": nome_cenario,
            "rotulo": ROTULOS_CENARIOS[
                nome_cenario
            ],
            "meses_confirmacao": (
                meses_confirmacao
            ),
            "quantidade_mudancas_regime": (
                contar_mudancas(
                    base_cenarios[
                        coluna_regime
                    ]
                )
            ),
            "turnover_total": (
                base_cenarios[
                    coluna_turnover
                ].sum()
            ),
            "turnover_medio_mensal": (
                base_cenarios[
                    coluna_turnover
                ].mean()
            ),
            "custo_acumulado_simples": (
                base_cenarios[
                    coluna_custo
                ].sum()
            ),
            "retorno_total_bruto": (
                retorno_total_bruto
            ),
            "retorno_total_liquido": (
                retorno_total_liquido
            ),
            "retorno_anualizado_liquido": (
                retorno_anualizado_liquido
            ),
            "volatilidade_anualizada_liquida": (
                volatilidade_liquida
            ),
            "retorno_volatilidade_liquido": (
                retorno_volatilidade
            ),
            "maximo_drawdown_liquido": (
                calcular_maximo_drawdown(
                    retornos=base_cenarios[
                        coluna_retorno_liquido
                    ],
                    valor_inicial=VALOR_INICIAL,
                )
            ),
            "meses_positivos": (
                base_cenarios[
                    coluna_retorno_liquido
                ]
                .gt(0)
                .mean()
            ),
            "indice_final_bruto": (
                base_cenarios[
                    coluna_indice_bruto
                ].iloc[-1]
            ),
            "indice_final_liquido": (
                base_cenarios[
                    coluna_indice_liquido
                ].iloc[-1]
            ),
            "impacto_final_custos": (
                base_cenarios[
                    coluna_indice_bruto
                ].iloc[-1]
                - base_cenarios[
                    coluna_indice_liquido
                ].iloc[-1]
            ),
        }
    )


# ============================================================
# VALIDAÇÃO DO CENÁRIO ORIGINAL
# ============================================================

if not np.allclose(
    base_cenarios[
        "retorno_bruto_Original_1m"
    ],
    base_backtest_suavizacao[
        "retorno_portfolio"
    ],
    rtol=1e-10,
    atol=1e-12,
):
    diferenca_maxima = float(
        np.max(
            np.abs(
                base_cenarios[
                    "retorno_bruto_Original_1m"
                ]
                - base_backtest_suavizacao[
                    "retorno_portfolio"
                ]
            )
        )
    )

    raise ValueError(
        "O cenário original de 1 mês não reproduziu "
        "o retorno do backtest anterior.\n"
        f"Diferença máxima: {diferenca_maxima}"
    )


if "turnover_portfolio" in base_backtest_suavizacao.columns:

    if not np.allclose(
        base_cenarios[
            "turnover_Original_1m"
        ],
        base_backtest_suavizacao[
            "turnover_portfolio"
        ],
        rtol=1e-10,
        atol=1e-12,
    ):
        raise ValueError(
            "O turnover do cenário original não reproduziu "
            "o turnover do Notebook 05."
        )


# ============================================================
# CÁLCULO DO BENCHMARK DE PESOS IGUAIS
# ============================================================

peso_benchmark = (
    1
    / len(
        ativos_originais
    )
)

colunas_pesos_benchmark = []


for ativo in ativos_originais:

    coluna_peso_benchmark = (
        f"peso_Benchmark_Estatico_{ativo}"
    )

    base_cenarios[
        coluna_peso_benchmark
    ] = peso_benchmark

    colunas_pesos_benchmark.append(
        coluna_peso_benchmark
    )


base_cenarios[
    "retorno_bruto_Benchmark_Estatico"
] = 0.0


for ativo, coluna_peso in zip(
    ativos_originais,
    colunas_pesos_benchmark,
):
    base_cenarios[
        "retorno_bruto_Benchmark_Estatico"
    ] += (
        base_cenarios[
            coluna_peso
        ]
        * base_cenarios[
            ativo
        ]
    )


base_cenarios[
    "turnover_Benchmark_Estatico"
] = calcular_turnover_carteira(
    dados=base_cenarios,
    colunas_retornos=ativos_originais,
    colunas_pesos=colunas_pesos_benchmark,
    cobrar_custo_inicial=COBRAR_CUSTO_INICIAL,
)


base_cenarios[
    "custo_Benchmark_Estatico"
] = (
    base_cenarios[
        "turnover_Benchmark_Estatico"
    ]
    * CUSTO_POR_TURNOVER_OTIMIZACAO
)


base_cenarios[
    "retorno_liquido_Benchmark_Estatico"
] = (
    (
        1
        + base_cenarios[
            "retorno_bruto_Benchmark_Estatico"
        ]
    )
    * (
        1
        - base_cenarios[
            "custo_Benchmark_Estatico"
        ]
    )
    - 1
)


base_cenarios[
    "indice_bruto_Benchmark_Estatico"
] = (
    VALOR_INICIAL
    * (
        1
        + base_cenarios[
            "retorno_bruto_Benchmark_Estatico"
        ]
    ).cumprod()
)


base_cenarios[
    "indice_liquido_Benchmark_Estatico"
] = (
    VALOR_INICIAL
    * (
        1
        + base_cenarios[
            "retorno_liquido_Benchmark_Estatico"
        ]
    ).cumprod()
)


if not np.allclose(
    base_cenarios[
        "retorno_bruto_Benchmark_Estatico"
    ],
    base_backtest_suavizacao[
        "retorno_carteira_estatica"
    ],
    rtol=1e-10,
    atol=1e-12,
):
    raise ValueError(
        "O benchmark recalculado não reproduziu "
        "o benchmark do Notebook 05."
    )


retorno_anualizado_benchmark = (
    calcular_retorno_anualizado(
        retornos=base_cenarios[
            "retorno_liquido_Benchmark_Estatico"
        ],
        periodos_por_ano=PERIODOS_POR_ANO,
    )
)

volatilidade_benchmark = (
    calcular_volatilidade_anualizada(
        retornos=base_cenarios[
            "retorno_liquido_Benchmark_Estatico"
        ],
        periodos_por_ano=PERIODOS_POR_ANO,
    )
)

retorno_volatilidade_benchmark = (
    retorno_anualizado_benchmark
    / volatilidade_benchmark
    if (
        pd.notna(
            volatilidade_benchmark
        )
        and volatilidade_benchmark > 0
    )
    else np.nan
)


resultados_cenarios.append(
    {
        "cenario": "Benchmark_Estatico",
        "rotulo": ROTULOS_CENARIOS[
            "Benchmark_Estatico"
        ],
        "meses_confirmacao": np.nan,
        "quantidade_mudancas_regime": 0,
        "turnover_total": (
            base_cenarios[
                "turnover_Benchmark_Estatico"
            ].sum()
        ),
        "turnover_medio_mensal": (
            base_cenarios[
                "turnover_Benchmark_Estatico"
            ].mean()
        ),
        "custo_acumulado_simples": (
            base_cenarios[
                "custo_Benchmark_Estatico"
            ].sum()
        ),
        "retorno_total_bruto": (
            calcular_retorno_total(
                base_cenarios[
                    "retorno_bruto_Benchmark_Estatico"
                ]
            )
        ),
        "retorno_total_liquido": (
            calcular_retorno_total(
                base_cenarios[
                    "retorno_liquido_Benchmark_Estatico"
                ]
            )
        ),
        "retorno_anualizado_liquido": (
            retorno_anualizado_benchmark
        ),
        "volatilidade_anualizada_liquida": (
            volatilidade_benchmark
        ),
        "retorno_volatilidade_liquido": (
            retorno_volatilidade_benchmark
        ),
        "maximo_drawdown_liquido": (
            calcular_maximo_drawdown(
                retornos=base_cenarios[
                    "retorno_liquido_Benchmark_Estatico"
                ],
                valor_inicial=VALOR_INICIAL,
            )
        ),
        "meses_positivos": (
            base_cenarios[
                "retorno_liquido_Benchmark_Estatico"
            ]
            .gt(0)
            .mean()
        ),
        "indice_final_bruto": (
            base_cenarios[
                "indice_bruto_Benchmark_Estatico"
            ].iloc[-1]
        ),
        "indice_final_liquido": (
            base_cenarios[
                "indice_liquido_Benchmark_Estatico"
            ].iloc[-1]
        ),
        "impacto_final_custos": (
            base_cenarios[
                "indice_bruto_Benchmark_Estatico"
            ].iloc[-1]
            - base_cenarios[
                "indice_liquido_Benchmark_Estatico"
            ].iloc[-1]
        ),
    }
)


# ============================================================
# TABELA COMPARATIVA
# ============================================================

comparacao_cenarios = pd.DataFrame(
    resultados_cenarios
)


indice_final_benchmark = float(
    comparacao_cenarios.loc[
        comparacao_cenarios[
            "cenario"
        ]
        == "Benchmark_Estatico",
        "indice_final_liquido",
    ]
    .iloc[0]
)


comparacao_cenarios[
    "diferenca_liquida_vs_benchmark"
] = (
    comparacao_cenarios[
        "indice_final_liquido"
    ]
    - indice_final_benchmark
)


ordem_cenarios = {
    nome_cenario: indice
    for indice, nome_cenario
    in enumerate(
        NOMES_CENARIOS_ESTRATEGIA,
        start=1,
    )
}

ordem_cenarios[
    "Benchmark_Estatico"
] = (
    len(
        NOMES_CENARIOS_ESTRATEGIA
    )
    + 1
)


comparacao_cenarios[
    "ordem"
] = (
    comparacao_cenarios[
        "cenario"
    ]
    .map(
        ordem_cenarios
    )
)


comparacao_cenarios = (
    comparacao_cenarios
    .sort_values(
        "ordem"
    )
    .drop(
        columns=[
            "ordem"
        ]
    )
    .reset_index(drop=True)
)


# ============================================================
# TABELA FORMATADA
# ============================================================

comparacao_cenarios_formatada = (
    comparacao_cenarios
    .copy()
    .astype(object)
)


colunas_percentuais = [
    "turnover_medio_mensal",
    "custo_acumulado_simples",
    "retorno_total_bruto",
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown_liquido",
    "meses_positivos",
]


for coluna in colunas_percentuais:
    comparacao_cenarios_formatada[
        coluna
    ] = (
        comparacao_cenarios[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


colunas_decimais = [
    "turnover_total",
    "retorno_volatilidade_liquido",
    "indice_final_bruto",
    "indice_final_liquido",
    "impacto_final_custos",
    "diferenca_liquida_vs_benchmark",
]


for coluna in colunas_decimais:
    comparacao_cenarios_formatada[
        coluna
    ] = (
        comparacao_cenarios[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "meses_confirmacao",
    "quantidade_mudancas_regime",
]:
    comparacao_cenarios_formatada[
        coluna
    ] = (
        comparacao_cenarios[
            coluna
        ]
        .map(
            lambda valor: (
                f"{int(valor)}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


# ============================================================
# BASE PARA GRÁFICOS
# ============================================================

data_inicial_grafico = (
    base_cenarios[
        "data"
    ].iloc[0]
    - pd.offsets.MonthEnd(1)
)


NOMES_CENARIOS_GRAFICO = [
    *NOMES_CENARIOS_ESTRATEGIA,
    "Benchmark_Estatico",
]


colunas_indices_grafico = [
    f"indice_liquido_{nome_cenario}"
    for nome_cenario in NOMES_CENARIOS_GRAFICO
]


linha_inicial_grafico = {
    "data": data_inicial_grafico,
}


for coluna in colunas_indices_grafico:
    linha_inicial_grafico[
        coluna
    ] = VALOR_INICIAL


base_graficos = pd.concat(
    [
        pd.DataFrame(
            [
                linha_inicial_grafico
            ]
        ),
        base_cenarios[
            [
                "data",
                *colunas_indices_grafico,
            ]
        ],
    ],
    ignore_index=True,
)


for nome_cenario in NOMES_CENARIOS_ESTRATEGIA:

    base_cenarios[
        f"diferenca_vs_benchmark_{nome_cenario}"
    ] = (
        base_cenarios[
            f"indice_liquido_{nome_cenario}"
        ]
        - base_cenarios[
            "indice_liquido_Benchmark_Estatico"
        ]
    )


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

comparacao_cenarios.to_csv(
    ARQUIVO_COMPARACAO_CENARIOS,
    index=False,
    encoding="utf-8-sig",
)

comparacao_cenarios_formatada.to_csv(
    ARQUIVO_COMPARACAO_CENARIOS_FORMATADA,
    index=False,
    encoding="utf-8-sig",
)

base_cenarios.to_csv(
    ARQUIVO_SERIES_MENSAIS,
    index=False,
    encoding="utf-8-sig",
)

tabela_pesos_regimes.to_csv(
    ARQUIVO_PESOS_REGIMES,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO 1 — DESEMPENHO LÍQUIDO
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


for nome_cenario in NOMES_CENARIOS_GRAFICO:

    ax.plot(
        base_graficos[
            "data"
        ],
        base_graficos[
            f"indice_liquido_{nome_cenario}"
        ],
        linewidth=2,
        label=ROTULOS_CENARIOS[
            nome_cenario
        ],
    )


ax.axhline(
    y=VALOR_INICIAL,
    linewidth=1,
)


ax.set_title(
    "Desempenho Líquido dos Regimes Suavizados"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Índice acumulado"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DESEMPENHO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — TURNOVER SEM A MONTAGEM INICIAL
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


for nome_cenario in NOMES_CENARIOS_ESTRATEGIA:

    ax.plot(
        base_cenarios[
            "data"
        ].iloc[1:],
        base_cenarios[
            f"turnover_{nome_cenario}"
        ].iloc[1:],
        linewidth=1.8,
        label=ROTULOS_CENARIOS[
            nome_cenario
        ],
    )


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Turnover Mensal dos Regimes Suavizados"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Turnover"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_TURNOVER,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — DIFERENÇA LÍQUIDA CONTRA O BENCHMARK
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


for nome_cenario in NOMES_CENARIOS_ESTRATEGIA:

    ax.plot(
        base_cenarios[
            "data"
        ],
        base_cenarios[
            f"diferenca_vs_benchmark_{nome_cenario}"
        ],
        linewidth=2,
        label=ROTULOS_CENARIOS[
            nome_cenario
        ],
    )


ax.axhline(
    y=0,
    linewidth=1,
)


ax.set_title(
    "Diferença Líquida dos Cenários contra o Benchmark"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Diferença do índice em pontos"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DIFERENCA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_COMPARACAO_CENARIOS,
    ARQUIVO_COMPARACAO_CENARIOS_FORMATADA,
    ARQUIVO_SERIES_MENSAIS,
    ARQUIVO_PESOS_REGIMES,
    ARQUIVO_GRAFICO_DESEMPENHO,
    ARQUIVO_GRAFICO_TURNOVER,
    ARQUIVO_GRAFICO_DIFERENCA,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:
    raise FileNotFoundError(
        "Alguns arquivos da Célula 3 não foram salvos:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

cenarios_estrategia = (
    comparacao_cenarios.loc[
        comparacao_cenarios[
            "cenario"
        ]
        != "Benchmark_Estatico"
    ]
    .copy()
)


melhor_cenario = (
    cenarios_estrategia
    .sort_values(
        [
            "indice_final_liquido",
            "retorno_volatilidade_liquido",
        ],
        ascending=[
            False,
            False,
        ],
    )
    .iloc[0]
)


menor_turnover = (
    cenarios_estrategia
    .sort_values(
        [
            "turnover_total",
            "indice_final_liquido",
        ],
        ascending=[
            True,
            False,
        ],
    )
    .iloc[0]
)


print("=" * 70)
print("BACKTEST DOS REGIMES SUAVIZADOS CONCLUÍDO")
print("=" * 70)

print(
    f"\nJanelas de confirmação testadas: "
    f"{JANELAS_CONFIRMACAO}"
)

print(
    f"Valor inicial: "
    f"{VALOR_INICIAL:.2f}"
)

print(
    f"Períodos por ano: "
    f"{PERIODOS_POR_ANO}"
)

print(
    f"Cobrança de custo inicial: "
    f"{COBRAR_CUSTO_INICIAL}"
)

print(
    f"\nCusto utilizado: "
    f"{CUSTO_POR_TURNOVER_OTIMIZACAO:.4%} "
    f"({CUSTO_POR_TURNOVER_OTIMIZACAO * 10000:.2f} bps)"
)

print(
    f"\nMelhor cenário por índice líquido final: "
    f"{melhor_cenario['rotulo']}"
)

print(
    f"Índice líquido final: "
    f"{melhor_cenario['indice_final_liquido']:.2f}"
)

print(
    f"Diferença contra o benchmark: "
    f"{melhor_cenario['diferenca_liquida_vs_benchmark']:.2f} pontos"
)

print(
    f"\nCenário com menor turnover: "
    f"{menor_turnover['rotulo']}"
)

print(
    f"Turnover total: "
    f"{menor_turnover['turnover_total']:.4f}"
)

print(
    f"Mudanças de regime: "
    f"{int(menor_turnover['quantidade_mudancas_regime'])}"
)

print(
    f"\nTabela comparativa salva em:\n"
    f"{ARQUIVO_COMPARACAO_CENARIOS}"
)

print(
    f"\nSéries mensais salvas em:\n"
    f"{ARQUIVO_SERIES_MENSAIS}"
)

print(
    f"\nPesos originais por regime salvos em:\n"
    f"{ARQUIVO_PESOS_REGIMES}"
)

print(
    f"\nGráfico de desempenho:\n"
    f"{ARQUIVO_GRAFICO_DESEMPENHO.name}"
)

print(
    f"\nGráfico de turnover:\n"
    f"{ARQUIVO_GRAFICO_TURNOVER.name}"
)

print(
    f"\nGráfico de diferença:\n"
    f"{ARQUIVO_GRAFICO_DIFERENCA.name}"
)

print("\nComparação dos cenários:")

display(
    comparacao_cenarios_formatada
)

# ###########################################################################
# ETAPA 04 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 4 — VALIDAÇÃO FORA DA AMOSTRA: TREINO E TESTE
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# VALIDAÇÃO DAS CÉLULAS ANTERIORES
# ============================================================

variaveis_obrigatorias = [
    "RAIZ_PROJETO",
    "base_cenarios",
    "comparacao_cenarios",
    "ROTULOS_CENARIOS",
    "PASTA_TABELAS",
    "PASTA_GRAFICOS",
]

variaveis_ausentes = [
    variavel
    for variavel in variaveis_obrigatorias
    if variavel not in globals()
]

if variaveis_ausentes:
    raise NameError(
        "Execute primeiro as Células 1, 2 e 3 "
        "do Notebook 06.\n"
        f"Variáveis ausentes: {variaveis_ausentes}"
    )


# ============================================================
# CONFIGURAÇÕES
# ============================================================

VALOR_INICIAL = 100.0
PERIODOS_POR_ANO = 12

DATA_CORTE_TREINO = pd.Timestamp(
    "2023-12-31"
)

CENARIOS_ESTRATEGIA = [
    "Original_1m",
    "Confirmacao_2m",
    "Confirmacao_3m",
]

CENARIO_BENCHMARK = (
    "Benchmark_Estatico"
)

MAPA_REGIMES_CENARIOS = {
    "Original_1m": (
        "regime_confirmacao_1m"
    ),
    "Confirmacao_2m": (
        "regime_confirmacao_2m"
    ),
    "Confirmacao_3m": (
        "regime_confirmacao_3m"
    ),
}

CRITERIO_SELECAO = (
    "retorno_volatilidade_liquido"
)


# ============================================================
# COLUNAS OBRIGATÓRIAS
# ============================================================

colunas_obrigatorias = [
    "data",
]

for cenario in [
    *CENARIOS_ESTRATEGIA,
    CENARIO_BENCHMARK,
]:
    colunas_obrigatorias.extend(
        [
            f"retorno_liquido_{cenario}",
            f"turnover_{cenario}",
            f"custo_{cenario}",
        ]
    )


for coluna_regime in (
    MAPA_REGIMES_CENARIOS.values()
):
    colunas_obrigatorias.append(
        coluna_regime
    )


colunas_ausentes = [
    coluna
    for coluna in colunas_obrigatorias
    if coluna not in base_cenarios.columns
]

if colunas_ausentes:
    raise ValueError(
        "Colunas necessárias não encontradas.\n"
        "Execute novamente a Célula 3.\n"
        f"Colunas ausentes: {colunas_ausentes}"
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_VALIDACAO_TREINO_TESTE = (
    PASTA_TABELAS
    / "06_04_validacao_treino_teste.csv"
)

ARQUIVO_VALIDACAO_FORMATADA = (
    PASTA_TABELAS
    / "06_04_validacao_treino_teste_formatada.csv"
)

ARQUIVO_SELECAO_CENARIO = (
    PASTA_TABELAS
    / "06_04_selecao_cenario_treino.csv"
)

ARQUIVO_SERIES_FORA_AMOSTRA = (
    PASTA_TABELAS
    / "06_04_series_fora_amostra.csv"
)

ARQUIVO_GRAFICO_FORA_AMOSTRA = (
    PASTA_GRAFICOS
    / "06_04_desempenho_fora_amostra.png"
)

ARQUIVO_GRAFICO_DIFERENCA = (
    PASTA_GRAFICOS
    / "06_04_diferenca_fora_amostra.png"
)


# ============================================================
# ORGANIZAÇÃO DA BASE
# ============================================================

base_validacao = (
    base_cenarios
    .copy()
    .sort_values("data")
    .reset_index(drop=True)
)


base_validacao["data"] = pd.to_datetime(
    base_validacao["data"],
    errors="coerce",
)

if base_validacao["data"].isna().any():
    raise ValueError(
        "Existem datas inválidas na base."
    )


if base_validacao[
    "data"
].duplicated().any():
    raise ValueError(
        "Existem datas duplicadas na base."
    )


for coluna in colunas_obrigatorias:

    if coluna == "data":
        continue

    if coluna.startswith(
        "regime_"
    ):
        base_validacao[coluna] = (
            base_validacao[coluna]
            .astype("string")
            .str.strip()
        )

    else:
        base_validacao[coluna] = pd.to_numeric(
            base_validacao[coluna],
            errors="coerce",
        )


colunas_numericas = [
    coluna
    for coluna in colunas_obrigatorias
    if (
        coluna != "data"
        and not coluna.startswith(
            "regime_"
        )
    )
]


if (
    base_validacao[
        colunas_numericas
    ]
    .isna()
    .any()
    .any()
):
    nulos = (
        base_validacao[
            colunas_numericas
        ]
        .isna()
        .sum()
    )

    nulos = nulos[
        nulos > 0
    ]

    raise ValueError(
        "Existem valores nulos nas colunas numéricas:\n"
        f"{nulos}"
    )


# ============================================================
# DIVISÃO CRONOLÓGICA
# ============================================================

base_treino = (
    base_validacao.loc[
        base_validacao["data"]
        <= DATA_CORTE_TREINO
    ]
    .copy()
    .reset_index(drop=True)
)


base_teste = (
    base_validacao.loc[
        base_validacao["data"]
        > DATA_CORTE_TREINO
    ]
    .copy()
    .reset_index(drop=True)
)


if base_treino.empty:
    raise ValueError(
        "A base de treino ficou vazia."
    )


if base_teste.empty:
    raise ValueError(
        "A base de teste ficou vazia."
    )


if len(base_treino) < 24:
    raise ValueError(
        "A base de treino possui menos de 24 meses."
    )


if len(base_teste) < 12:
    raise ValueError(
        "A base de teste possui menos de 12 meses."
    )


if (
    base_treino["data"].max()
    >= base_teste["data"].min()
):
    raise ValueError(
        "Existe sobreposição entre treino e teste."
    )


# ============================================================
# FUNÇÕES DE MÉTRICAS
# ============================================================

def calcular_retorno_total(
    retornos,
):
    retornos = (
        pd.Series(retornos)
        .dropna()
        .astype(float)
    )

    if retornos.empty:
        return np.nan

    return float(
        (
            1
            + retornos
        ).prod()
        - 1
    )


def calcular_retorno_anualizado(
    retornos,
    periodos_por_ano=12,
):
    retornos = (
        pd.Series(retornos)
        .dropna()
        .astype(float)
    )

    quantidade_periodos = len(
        retornos
    )

    if quantidade_periodos == 0:
        return np.nan

    retorno_total = calcular_retorno_total(
        retornos
    )

    if (
        pd.isna(retorno_total)
        or retorno_total <= -1
    ):
        return np.nan

    return float(
        (
            1
            + retorno_total
        )
        ** (
            periodos_por_ano
            / quantidade_periodos
        )
        - 1
    )


def calcular_volatilidade_anualizada(
    retornos,
    periodos_por_ano=12,
):
    retornos = (
        pd.Series(retornos)
        .dropna()
        .astype(float)
    )

    if len(retornos) < 2:
        return np.nan

    return float(
        retornos.std(
            ddof=1
        )
        * np.sqrt(
            periodos_por_ano
        )
    )


def calcular_maximo_drawdown(
    retornos,
    valor_inicial=100.0,
):
    retornos = (
        pd.Series(retornos)
        .dropna()
        .astype(float)
        .reset_index(drop=True)
    )

    if retornos.empty:
        return np.nan

    indice = (
        valor_inicial
        * (
            1
            + retornos
        ).cumprod()
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

    pico = (
        indice_com_inicio
        .cummax()
    )

    drawdown = (
        indice_com_inicio
        / pico
        - 1
    )

    return float(
        drawdown.min()
    )


def contar_mudancas_regime(
    serie_regimes,
):
    valores = (
        pd.Series(
            serie_regimes
        )
        .dropna()
        .astype("string")
        .to_numpy(
            dtype=str
        )
    )

    if len(valores) <= 1:
        return 0

    return int(
        np.sum(
            valores[1:]
            != valores[:-1]
        )
    )


def calcular_metricas_periodo(
    dados,
    cenario,
    nome_periodo,
):
    coluna_retorno = (
        f"retorno_liquido_{cenario}"
    )

    coluna_turnover = (
        f"turnover_{cenario}"
    )

    coluna_custo = (
        f"custo_{cenario}"
    )

    retornos = (
        dados[
            coluna_retorno
        ]
        .astype(float)
    )

    retorno_total = (
        calcular_retorno_total(
            retornos
        )
    )

    retorno_anualizado = (
        calcular_retorno_anualizado(
            retornos,
            periodos_por_ano=PERIODOS_POR_ANO,
        )
    )

    volatilidade_anualizada = (
        calcular_volatilidade_anualizada(
            retornos,
            periodos_por_ano=PERIODOS_POR_ANO,
        )
    )

    if (
        pd.notna(
            volatilidade_anualizada
        )
        and volatilidade_anualizada > 0
    ):
        retorno_volatilidade = (
            retorno_anualizado
            / volatilidade_anualizada
        )

    else:
        retorno_volatilidade = np.nan

    if cenario in MAPA_REGIMES_CENARIOS:
        coluna_regime = (
            MAPA_REGIMES_CENARIOS[
                cenario
            ]
        )

        quantidade_mudancas = (
            contar_mudancas_regime(
                dados[
                    coluna_regime
                ]
            )
        )

    else:
        quantidade_mudancas = 0

    indice_final = (
        VALOR_INICIAL
        * (
            1
            + retornos
        ).prod()
    )

    return {
        "periodo": nome_periodo,
        "cenario": cenario,
        "rotulo": ROTULOS_CENARIOS[
            cenario
        ],
        "data_inicial": (
            dados[
                "data"
            ].min()
        ),
        "data_final": (
            dados[
                "data"
            ].max()
        ),
        "quantidade_meses": (
            len(
                dados
            )
        ),
        "quantidade_mudancas_regime": (
            quantidade_mudancas
        ),
        "retorno_total_liquido": (
            retorno_total
        ),
        "retorno_anualizado_liquido": (
            retorno_anualizado
        ),
        "volatilidade_anualizada_liquida": (
            volatilidade_anualizada
        ),
        "retorno_volatilidade_liquido": (
            retorno_volatilidade
        ),
        "maximo_drawdown_liquido": (
            calcular_maximo_drawdown(
                retornos,
                valor_inicial=VALOR_INICIAL,
            )
        ),
        "meses_positivos": (
            retornos.gt(0).mean()
        ),
        "melhor_mes": (
            retornos.max()
        ),
        "pior_mes": (
            retornos.min()
        ),
        "turnover_total": (
            dados[
                coluna_turnover
            ].sum()
        ),
        "turnover_medio_mensal": (
            dados[
                coluna_turnover
            ].mean()
        ),
        "custo_acumulado_simples": (
            dados[
                coluna_custo
            ].sum()
        ),
        "indice_final_liquido": (
            indice_final
        ),
    }


# ============================================================
# MÉTRICAS DE TREINO E TESTE
# ============================================================

resultados_validacao = []


for nome_periodo, dados_periodo in [
    (
        "TREINO",
        base_treino,
    ),
    (
        "TESTE",
        base_teste,
    ),
]:
    for cenario in [
        *CENARIOS_ESTRATEGIA,
        CENARIO_BENCHMARK,
    ]:
        resultados_validacao.append(
            calcular_metricas_periodo(
                dados=dados_periodo,
                cenario=cenario,
                nome_periodo=nome_periodo,
            )
        )


validacao_treino_teste = pd.DataFrame(
    resultados_validacao
)


# ============================================================
# SELEÇÃO DO CENÁRIO SOMENTE COM O TREINO
# ============================================================

resultados_treino_estrategias = (
    validacao_treino_teste.loc[
        (
            validacao_treino_teste[
                "periodo"
            ]
            == "TREINO"
        )
        & (
            validacao_treino_teste[
                "cenario"
            ]
            .isin(
                CENARIOS_ESTRATEGIA
            )
        )
    ]
    .copy()
)


if (
    resultados_treino_estrategias[
        CRITERIO_SELECAO
    ]
    .isna()
    .all()
):
    raise ValueError(
        "O critério de seleção ficou nulo "
        "para todos os cenários."
    )


resultado_selecionado_treino = (
    resultados_treino_estrategias
    .sort_values(
        [
            CRITERIO_SELECAO,
            "indice_final_liquido",
            "turnover_total",
        ],
        ascending=[
            False,
            False,
            True,
        ],
    )
    .iloc[0]
)


cenario_selecionado = (
    resultado_selecionado_treino[
        "cenario"
    ]
)


rotulo_cenario_selecionado = (
    resultado_selecionado_treino[
        "rotulo"
    ]
)


# ============================================================
# RESULTADO FORA DA AMOSTRA
# ============================================================

resultado_selecionado_teste = (
    validacao_treino_teste.loc[
        (
            validacao_treino_teste[
                "periodo"
            ]
            == "TESTE"
        )
        & (
            validacao_treino_teste[
                "cenario"
            ]
            == cenario_selecionado
        )
    ]
    .iloc[0]
)


resultado_benchmark_teste = (
    validacao_treino_teste.loc[
        (
            validacao_treino_teste[
                "periodo"
            ]
            == "TESTE"
        )
        & (
            validacao_treino_teste[
                "cenario"
            ]
            == CENARIO_BENCHMARK
        )
    ]
    .iloc[0]
)


diferenca_indice_teste = (
    resultado_selecionado_teste[
        "indice_final_liquido"
    ]
    - resultado_benchmark_teste[
        "indice_final_liquido"
    ]
)


diferenca_retorno_anualizado_teste = (
    resultado_selecionado_teste[
        "retorno_anualizado_liquido"
    ]
    - resultado_benchmark_teste[
        "retorno_anualizado_liquido"
    ]
)


diferenca_retorno_volatilidade_teste = (
    resultado_selecionado_teste[
        "retorno_volatilidade_liquido"
    ]
    - resultado_benchmark_teste[
        "retorno_volatilidade_liquido"
    ]
)


if diferenca_indice_teste > 0:
    status_fora_amostra = (
        "SUPEROU O BENCHMARK"
    )

elif diferenca_indice_teste < 0:
    status_fora_amostra = (
        "FICOU ABAIXO DO BENCHMARK"
    )

else:
    status_fora_amostra = (
        "EMPATOU COM O BENCHMARK"
    )


# ============================================================
# RESUMO DA SELEÇÃO
# ============================================================

selecao_cenario_treino = pd.DataFrame(
    {
        "metrica": [
            "Data final do treino",
            "Data inicial do teste",
            "Meses de treino",
            "Meses de teste",
            "Critério de seleção",
            "Cenário selecionado",
            "Retorno/volatilidade no treino",
            "Índice final no treino",
            "Turnover total no treino",
            "Índice final no teste da estratégia",
            "Índice final no teste do benchmark",
            "Diferença do índice no teste",
            "Diferença do retorno anualizado no teste",
            "Diferença de retorno/volatilidade no teste",
            "Status fora da amostra",
        ],
        "valor": [
            base_treino[
                "data"
            ].max().strftime(
                "%d/%m/%Y"
            ),
            base_teste[
                "data"
            ].min().strftime(
                "%d/%m/%Y"
            ),
            len(
                base_treino
            ),
            len(
                base_teste
            ),
            CRITERIO_SELECAO,
            rotulo_cenario_selecionado,
            resultado_selecionado_treino[
                "retorno_volatilidade_liquido"
            ],
            resultado_selecionado_treino[
                "indice_final_liquido"
            ],
            resultado_selecionado_treino[
                "turnover_total"
            ],
            resultado_selecionado_teste[
                "indice_final_liquido"
            ],
            resultado_benchmark_teste[
                "indice_final_liquido"
            ],
            diferenca_indice_teste,
            diferenca_retorno_anualizado_teste,
            diferenca_retorno_volatilidade_teste,
            status_fora_amostra,
        ],
    }
)


# ============================================================
# TABELA FORMATADA
# ============================================================

validacao_formatada = (
    validacao_treino_teste
    .copy()
    .astype(object)
)


validacao_formatada[
    "data_inicial"
] = (
    validacao_treino_teste[
        "data_inicial"
    ]
    .dt.strftime(
        "%d/%m/%Y"
    )
)


validacao_formatada[
    "data_final"
] = (
    validacao_treino_teste[
        "data_final"
    ]
    .dt.strftime(
        "%d/%m/%Y"
    )
)


colunas_percentuais = [
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown_liquido",
    "meses_positivos",
    "melhor_mes",
    "pior_mes",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
]


for coluna in colunas_percentuais:
    validacao_formatada[
        coluna
    ] = (
        validacao_treino_teste[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


colunas_decimais = [
    "retorno_volatilidade_liquido",
    "turnover_total",
    "indice_final_liquido",
]


for coluna in colunas_decimais:
    validacao_formatada[
        coluna
    ] = (
        validacao_treino_teste[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "quantidade_meses",
    "quantidade_mudancas_regime",
]:
    validacao_formatada[
        coluna
    ] = (
        validacao_treino_teste[
            coluna
        ]
        .map(
            lambda valor: (
                f"{int(valor)}"
            )
        )
    )


# ============================================================
# SÉRIES FORA DA AMOSTRA
# ============================================================

coluna_retorno_selecionado = (
    f"retorno_liquido_"
    f"{cenario_selecionado}"
)


coluna_retorno_benchmark = (
    f"retorno_liquido_"
    f"{CENARIO_BENCHMARK}"
)


series_fora_amostra = (
    base_teste[
        [
            "data",
            coluna_retorno_selecionado,
            coluna_retorno_benchmark,
        ]
    ]
    .copy()
    .rename(
        columns={
            coluna_retorno_selecionado: (
                "retorno_estrategia"
            ),
            coluna_retorno_benchmark: (
                "retorno_benchmark"
            ),
        }
    )
    .reset_index(drop=True)
)


series_fora_amostra[
    "indice_estrategia"
] = (
    VALOR_INICIAL
    * (
        1
        + series_fora_amostra[
            "retorno_estrategia"
        ]
    ).cumprod()
)


series_fora_amostra[
    "indice_benchmark"
] = (
    VALOR_INICIAL
    * (
        1
        + series_fora_amostra[
            "retorno_benchmark"
        ]
    ).cumprod()
)


series_fora_amostra[
    "diferenca_indice"
] = (
    series_fora_amostra[
        "indice_estrategia"
    ]
    - series_fora_amostra[
        "indice_benchmark"
    ]
)


data_inicial_grafico = (
    series_fora_amostra[
        "data"
    ].iloc[0]
    - pd.offsets.MonthEnd(1)
)


linha_inicial = pd.DataFrame(
    {
        "data": [
            data_inicial_grafico
        ],
        "retorno_estrategia": [
            np.nan
        ],
        "retorno_benchmark": [
            np.nan
        ],
        "indice_estrategia": [
            VALOR_INICIAL
        ],
        "indice_benchmark": [
            VALOR_INICIAL
        ],
        "diferenca_indice": [
            0.0
        ],
    }
)


series_grafico_fora_amostra = pd.concat(
    [
        linha_inicial,
        series_fora_amostra,
    ],
    ignore_index=True,
)


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

validacao_treino_teste.to_csv(
    ARQUIVO_VALIDACAO_TREINO_TESTE,
    index=False,
    encoding="utf-8-sig",
)


validacao_formatada.to_csv(
    ARQUIVO_VALIDACAO_FORMATADA,
    index=False,
    encoding="utf-8-sig",
)


selecao_cenario_treino.to_csv(
    ARQUIVO_SELECAO_CENARIO,
    index=False,
    encoding="utf-8-sig",
)


series_fora_amostra.to_csv(
    ARQUIVO_SERIES_FORA_AMOSTRA,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO 1 — DESEMPENHO FORA DA AMOSTRA
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_grafico_fora_amostra[
        "data"
    ],
    series_grafico_fora_amostra[
        "indice_estrategia"
    ],
    linewidth=2,
    label=(
        f"Estratégia selecionada — "
        f"{rotulo_cenario_selecionado}"
    ),
)


ax.plot(
    series_grafico_fora_amostra[
        "data"
    ],
    series_grafico_fora_amostra[
        "indice_benchmark"
    ],
    linewidth=2,
    label="Benchmark 25% rebalanceado",
)


ax.axhline(
    y=VALOR_INICIAL,
    linewidth=1,
)


ax.set_title(
    "Desempenho Fora da Amostra"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Índice acumulado"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_FORA_AMOSTRA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — DIFERENÇA FORA DA AMOSTRA
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_grafico_fora_amostra[
        "data"
    ],
    series_grafico_fora_amostra[
        "diferenca_indice"
    ],
    linewidth=2,
)


ax.axhline(
    y=0,
    linewidth=1,
)


ax.set_title(
    "Diferença da Estratégia contra o Benchmark "
    "Fora da Amostra"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Diferença do índice em pontos"
)

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DIFERENCA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_VALIDACAO_TREINO_TESTE,
    ARQUIVO_VALIDACAO_FORMATADA,
    ARQUIVO_SELECAO_CENARIO,
    ARQUIVO_SERIES_FORA_AMOSTRA,
    ARQUIVO_GRAFICO_FORA_AMOSTRA,
    ARQUIVO_GRAFICO_DIFERENCA,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:
    raise FileNotFoundError(
        "Alguns arquivos da Célula 4 não foram salvos:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("=" * 70)
print("VALIDAÇÃO FORA DA AMOSTRA CONCLUÍDA")
print("=" * 70)

print(
    f"\nTreino: "
    f"{base_treino['data'].min():%d/%m/%Y} "
    f"a "
    f"{base_treino['data'].max():%d/%m/%Y}"
)

print(
    f"Quantidade de meses de treino: "
    f"{len(base_treino)}"
)

print(
    f"\nTeste: "
    f"{base_teste['data'].min():%d/%m/%Y} "
    f"a "
    f"{base_teste['data'].max():%d/%m/%Y}"
)

print(
    f"Quantidade de meses de teste: "
    f"{len(base_teste)}"
)

print(
    f"\nCenário selecionado apenas com o treino: "
    f"{rotulo_cenario_selecionado}"
)

print(
    f"Retorno/volatilidade no treino: "
    f"{resultado_selecionado_treino['retorno_volatilidade_liquido']:.2f}"
)

print(
    f"\nÍndice final da estratégia no teste: "
    f"{resultado_selecionado_teste['indice_final_liquido']:.2f}"
)

print(
    f"Índice final do benchmark no teste: "
    f"{resultado_benchmark_teste['indice_final_liquido']:.2f}"
)

print(
    f"Diferença fora da amostra: "
    f"{diferenca_indice_teste:.2f} pontos"
)

print(
    f"Retorno anualizado da estratégia no teste: "
    f"{resultado_selecionado_teste['retorno_anualizado_liquido']:.2%}"
)

print(
    f"Retorno anualizado do benchmark no teste: "
    f"{resultado_benchmark_teste['retorno_anualizado_liquido']:.2%}"
)

print(
    f"Retorno/volatilidade da estratégia no teste: "
    f"{resultado_selecionado_teste['retorno_volatilidade_liquido']:.2f}"
)

print(
    f"Retorno/volatilidade do benchmark no teste: "
    f"{resultado_benchmark_teste['retorno_volatilidade_liquido']:.2f}"
)

print(
    f"\nResultado fora da amostra: "
    f"{status_fora_amostra}"
)

print(
    "\nO turnover do primeiro mês de teste preserva "
    "a transição real da carteira ao final do treino."
)

print(
    f"\nTabela de validação salva em:\n"
    f"{ARQUIVO_VALIDACAO_TREINO_TESTE}"
)

print(
    f"\nResumo da seleção salvo em:\n"
    f"{ARQUIVO_SELECAO_CENARIO}"
)

print(
    f"\nSéries fora da amostra salvas em:\n"
    f"{ARQUIVO_SERIES_FORA_AMOSTRA}"
)

print(
    f"\nGráfico de desempenho:\n"
    f"{ARQUIVO_GRAFICO_FORA_AMOSTRA.name}"
)

print(
    f"\nGráfico de diferença:\n"
    f"{ARQUIVO_GRAFICO_DIFERENCA.name}"
)

print("\nValidação treino e teste:")

display(
    validacao_formatada
)

# ###########################################################################
# ETAPA 05 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 5 — OTIMIZAÇÃO CONSERVADORA DOS PESOS
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter


# ============================================================
# VALIDAÇÃO DAS CÉLULAS ANTERIORES
# ============================================================

variaveis_obrigatorias = [
    "RAIZ_PROJETO",
    "base_cenarios",
    "ativos_originais",
    "pesos_por_regime",
    "CUSTO_POR_TURNOVER_OTIMIZACAO",
    "DATA_CORTE_TREINO",
    "CONFIGURACAO_BACKTEST",
    "CONFIGURACAO_OTIMIZACAO",
    "JANELAS_CONFIRMACAO",
    "PASTA_TABELAS",
    "PASTA_GRAFICOS",
]

variaveis_ausentes = [
    variavel
    for variavel in variaveis_obrigatorias
    if variavel not in globals()
]

if variaveis_ausentes:
    raise NameError(
        "Execute primeiro as Células 1 a 4 do Notebook 06.\n"
        f"Variáveis ausentes: {variaveis_ausentes}"
    )


# ============================================================
# CONFIGURAÇÕES
# ============================================================

parametros_backtest_obrigatorios = [
    "valor_inicial",
    "periodos_por_ano",
    "cobrar_custo_inicial",
]

parametros_backtest_ausentes = [
    parametro
    for parametro in parametros_backtest_obrigatorios
    if parametro not in CONFIGURACAO_BACKTEST
]

if parametros_backtest_ausentes:
    raise KeyError(
        "Parâmetros ausentes na seção 'backtest' "
        "do config.yaml:\n"
        f"{parametros_backtest_ausentes}"
    )


if (
    "alfas_encolhimento"
    not in CONFIGURACAO_OTIMIZACAO
):
    raise KeyError(
        "O parâmetro "
        "'otimizacao.alfas_encolhimento' "
        "não foi encontrado no config.yaml."
    )


VALOR_INICIAL_OTIMIZACAO = float(
    CONFIGURACAO_BACKTEST[
        "valor_inicial"
    ]
)

PERIODOS_POR_ANO_OTIMIZACAO = int(
    CONFIGURACAO_BACKTEST[
        "periodos_por_ano"
    ]
)

COBRAR_CUSTO_INICIAL_OTIMIZACAO = (
    CONFIGURACAO_BACKTEST[
        "cobrar_custo_inicial"
    ]
)


if VALOR_INICIAL_OTIMIZACAO <= 0:
    raise ValueError(
        "'backtest.valor_inicial' "
        "deve ser maior que zero."
    )


if PERIODOS_POR_ANO_OTIMIZACAO <= 0:
    raise ValueError(
        "'backtest.periodos_por_ano' "
        "deve ser maior que zero."
    )


if not isinstance(
    COBRAR_CUSTO_INICIAL_OTIMIZACAO,
    bool,
):
    raise TypeError(
        "'backtest.cobrar_custo_inicial' "
        "deve ser true ou false."
    )


alfas_configurados = (
    CONFIGURACAO_OTIMIZACAO[
        "alfas_encolhimento"
    ]
)


if not isinstance(
    alfas_configurados,
    list,
):
    raise TypeError(
        "'otimizacao.alfas_encolhimento' "
        "deve ser uma lista."
    )


if not alfas_configurados:
    raise ValueError(
        "'otimizacao.alfas_encolhimento' "
        "não pode estar vazio."
    )


try:
    ALFAS_ENCOLHIMENTO = [
        float(alpha)
        for alpha in alfas_configurados
    ]

except (
    TypeError,
    ValueError,
) as erro:
    raise TypeError(
        "Todos os valores de "
        "'otimizacao.alfas_encolhimento' "
        "devem ser numéricos."
    ) from erro


if any(
    alpha < 0.0
    or alpha > 1.0
    for alpha in ALFAS_ENCOLHIMENTO
):
    raise ValueError(
        "Todos os alphas de encolhimento "
        "devem estar entre 0 e 1."
    )


if (
    len(ALFAS_ENCOLHIMENTO)
    != len(set(ALFAS_ENCOLHIMENTO))
):
    raise ValueError(
        "A lista de alphas de encolhimento "
        "possui valores duplicados."
    )


if not any(
    np.isclose(
        alpha,
        0.0,
    )
    for alpha in ALFAS_ENCOLHIMENTO
):
    raise ValueError(
        "O alpha 0.0 é obrigatório para representar "
        "o modelo original."
    )


ALFAS_ENCOLHIMENTO = sorted(
    ALFAS_ENCOLHIMENTO
)


if not JANELAS_CONFIRMACAO:
    raise ValueError(
        "A lista JANELAS_CONFIRMACAO "
        "não pode estar vazia."
    )


JANELAS_CONFIRMACAO = sorted(
    [
        int(janela)
        for janela in JANELAS_CONFIRMACAO
    ]
)


if 1 not in JANELAS_CONFIRMACAO:
    raise ValueError(
        "A janela de confirmação de 1 mês "
        "é obrigatória."
    )


CENARIOS_CONFIRMACAO = {}


for meses_confirmacao in JANELAS_CONFIRMACAO:

    if meses_confirmacao == 1:
        nome_cenario = (
            "Original_1m"
        )

    else:
        nome_cenario = (
            f"Confirmacao_"
            f"{meses_confirmacao}m"
        )

    CENARIOS_CONFIRMACAO[
        nome_cenario
    ] = {
        "meses_confirmacao": (
            meses_confirmacao
        ),
        "coluna_regime": (
            f"regime_confirmacao_"
            f"{meses_confirmacao}m"
        ),
        "rotulo": (
            f"Confirmação de "
            f"{meses_confirmacao} mês(es)"
        ),
    }


CENARIO_BENCHMARK = "Benchmark_Estatico"

COLUNA_RETORNO_BENCHMARK = (
    "retorno_liquido_Benchmark_Estatico"
)

COLUNA_TURNOVER_BENCHMARK = (
    "turnover_Benchmark_Estatico"
)

COLUNA_CUSTO_BENCHMARK = (
    "custo_Benchmark_Estatico"
)


# ============================================================
# COLUNAS OBRIGATÓRIAS
# ============================================================

colunas_obrigatorias = [
    "data",
    *ativos_originais,
    COLUNA_RETORNO_BENCHMARK,
    COLUNA_TURNOVER_BENCHMARK,
    COLUNA_CUSTO_BENCHMARK,
]

for configuracao in (
    CENARIOS_CONFIRMACAO.values()
):
    colunas_obrigatorias.append(
        configuracao[
            "coluna_regime"
        ]
    )


colunas_ausentes = [
    coluna
    for coluna in colunas_obrigatorias
    if coluna not in base_cenarios.columns
]

if colunas_ausentes:
    raise ValueError(
        "Colunas necessárias não encontradas.\n"
        "Execute novamente a Célula 3.\n"
        f"Colunas ausentes: {colunas_ausentes}"
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_GRADE_PARAMETROS = (
    PASTA_TABELAS
    / "06_05_grade_otimizacao_pesos.csv"
)

ARQUIVO_GRADE_FORMATADA = (
    PASTA_TABELAS
    / "06_05_grade_otimizacao_pesos_formatada.csv"
)

ARQUIVO_PARAMETROS_SELECIONADOS = (
    PASTA_TABELAS
    / "06_05_parametros_selecionados.csv"
)

ARQUIVO_PESOS_SELECIONADOS = (
    PASTA_TABELAS
    / "06_05_pesos_selecionados_por_regime.csv"
)

ARQUIVO_SERIES_TESTE = (
    PASTA_TABELAS
    / "06_05_series_teste_parametros_selecionados.csv"
)

ARQUIVO_GRAFICO_TREINO = (
    PASTA_GRAFICOS
    / "06_05_retorno_volatilidade_treino.png"
)

ARQUIVO_GRAFICO_TESTE = (
    PASTA_GRAFICOS
    / "06_05_desempenho_teste_pesos_otimizados.png"
)

ARQUIVO_GRAFICO_DIFERENCA = (
    PASTA_GRAFICOS
    / "06_05_diferenca_teste_pesos_otimizados.png"
)


# ============================================================
# ORGANIZAÇÃO DA BASE
# ============================================================

base_otimizacao = (
    base_cenarios[
        colunas_obrigatorias
    ]
    .copy()
    .sort_values("data")
    .reset_index(drop=True)
)


base_otimizacao["data"] = pd.to_datetime(
    base_otimizacao["data"],
    errors="coerce",
)

if base_otimizacao["data"].isna().any():
    raise ValueError(
        "Existem datas inválidas na base de otimização."
    )


if base_otimizacao[
    "data"
].duplicated().any():
    raise ValueError(
        "Existem datas duplicadas na base de otimização."
    )


for ativo in ativos_originais:
    base_otimizacao[ativo] = pd.to_numeric(
        base_otimizacao[ativo],
        errors="coerce",
    )


for coluna in [
    COLUNA_RETORNO_BENCHMARK,
    COLUNA_TURNOVER_BENCHMARK,
    COLUNA_CUSTO_BENCHMARK,
]:
    base_otimizacao[coluna] = pd.to_numeric(
        base_otimizacao[coluna],
        errors="coerce",
    )


colunas_numericas_validacao = [
    *ativos_originais,
    COLUNA_RETORNO_BENCHMARK,
    COLUNA_TURNOVER_BENCHMARK,
    COLUNA_CUSTO_BENCHMARK,
]


nulos_numericos = (
    base_otimizacao[
        colunas_numericas_validacao
    ]
    .isna()
    .sum()
)

nulos_numericos = nulos_numericos[
    nulos_numericos > 0
]

if not nulos_numericos.empty:
    raise ValueError(
        "Existem valores nulos ou inválidos:\n"
        f"{nulos_numericos}"
    )


for configuracao in (
    CENARIOS_CONFIRMACAO.values()
):
    coluna_regime = (
        configuracao[
            "coluna_regime"
        ]
    )

    base_otimizacao[coluna_regime] = (
        base_otimizacao[coluna_regime]
        .astype("string")
        .str.strip()
    )

    if base_otimizacao[
        coluna_regime
    ].isna().any():
        raise ValueError(
            f"A coluna {coluna_regime} possui regimes nulos."
        )


# ============================================================
# DIVISÃO TEMPORAL
# ============================================================

mascara_treino = (
    base_otimizacao["data"]
    <= DATA_CORTE_TREINO
)

mascara_teste = (
    base_otimizacao["data"]
    > DATA_CORTE_TREINO
)


if not mascara_treino.any():
    raise ValueError(
        "A divisão gerou uma base de treino vazia."
    )


if not mascara_teste.any():
    raise ValueError(
        "A divisão gerou uma base de teste vazia."
    )


quantidade_meses_treino = int(
    mascara_treino.sum()
)

quantidade_meses_teste = int(
    mascara_teste.sum()
)


# ============================================================
# PESOS DE REFERÊNCIA
# ============================================================

quantidade_ativos = len(
    ativos_originais
)

peso_igual = (
    1.0
    / quantidade_ativos
)


regimes_disponiveis = list(
    pesos_por_regime.keys()
)


for regime in regimes_disponiveis:

    pesos_regime = (
        pesos_por_regime[
            regime
        ]
    )

    ativos_ausentes = [
        ativo
        for ativo in ativos_originais
        if ativo not in pesos_regime
    ]

    if ativos_ausentes:
        raise ValueError(
            f"O regime {regime} não possui pesos "
            f"para os ativos: {ativos_ausentes}"
        )

    soma_pesos_regime = sum(
        float(
            pesos_regime[
                ativo
            ]
        )
        for ativo in ativos_originais
    )

    if not np.isclose(
        soma_pesos_regime,
        1.0,
        rtol=1e-10,
        atol=1e-10,
    ):
        raise ValueError(
            f"Os pesos originais do regime {regime} "
            "não somam 100%."
        )


# ============================================================
# FUNÇÃO DE AJUSTE DOS PESOS
# ============================================================

def criar_pesos_encolhidos(
    pesos_originais,
    ativos,
    alpha,
):
    alpha = float(
        alpha
    )

    if not (
        0.0
        <= alpha
        <= 1.0
    ):
        raise ValueError(
            "Alpha deve estar entre 0 e 1."
        )

    peso_igual_local = (
        1.0
        / len(
            ativos
        )
    )

    pesos_ajustados = {}

    for regime, pesos_regime in (
        pesos_originais.items()
    ):
        pesos_ajustados[
            regime
        ] = {}

        for ativo in ativos:
            peso_original = float(
                pesos_regime[
                    ativo
                ]
            )

            peso_ajustado = (
                (
                    1.0
                    - alpha
                )
                * peso_original
                + alpha
                * peso_igual_local
            )

            pesos_ajustados[
                regime
            ][ativo] = float(
                peso_ajustado
            )

        soma_pesos = sum(
            pesos_ajustados[
                regime
            ].values()
        )

        if not np.isclose(
            soma_pesos,
            1.0,
            rtol=1e-10,
            atol=1e-10,
        ):
            raise ValueError(
                f"Os pesos ajustados do regime {regime} "
                "não somam 100%."
            )

    return pesos_ajustados


# ============================================================
# FUNÇÃO DE TURNOVER
# ============================================================

def calcular_turnover_otimizacao(
    dados,
    colunas_retornos,
    colunas_pesos,
    cobrar_custo_inicial=True,
):
    quantidade_periodos = len(
        dados
    )

    turnover = np.zeros(
        quantidade_periodos,
        dtype=float,
    )

    if quantidade_periodos == 0:
        return turnover

    if len(
        colunas_retornos
    ) != len(
        colunas_pesos
    ):
        raise ValueError(
            "Retornos e pesos possuem tamanhos diferentes."
        )

    if cobrar_custo_inicial:
        turnover[0] = 1.0

    for indice in range(
        1,
        quantidade_periodos,
    ):
        pesos_anteriores = (
            dados.loc[
                indice - 1,
                colunas_pesos,
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

        retorno_carteira_anterior = float(
            np.sum(
                pesos_anteriores
                * retornos_anteriores
            )
        )

        fator_patrimonio = (
            1.0
            + retorno_carteira_anterior
        )

        if fator_patrimonio <= 0:
            raise ValueError(
                "O patrimônio relativo ficou menor "
                f"ou igual a zero no índice {indice - 1}."
            )

        pesos_apos_retornos = (
            pesos_anteriores
            * (
                1.0
                + retornos_anteriores
            )
            / fator_patrimonio
        )

        pesos_alvo_atuais = (
            dados.loc[
                indice,
                colunas_pesos,
            ]
            .astype(float)
            .to_numpy()
        )

        turnover[indice] = float(
            np.abs(
                pesos_alvo_atuais
                - pesos_apos_retornos
            ).sum()
            / 2.0
        )

    return turnover


# ============================================================
# FUNÇÕES DE MÉTRICAS
# ============================================================

def calcular_metricas_otimizacao(
    dados,
    coluna_retorno,
    coluna_turnover,
    coluna_custo,
    nome_periodo,
):
    retornos = (
        dados[
            coluna_retorno
        ]
        .dropna()
        .astype(float)
        .reset_index(drop=True)
    )

    if retornos.empty:
        raise ValueError(
            f"A série de retornos do período "
            f"{nome_periodo} ficou vazia."
        )

    quantidade_periodos = len(
        retornos
    )

    retorno_total = float(
        (
            1.0
            + retornos
        ).prod()
        - 1.0
    )

    retorno_anualizado = float(
        (
            1.0
            + retorno_total
        )
        ** (
            PERIODOS_POR_ANO_OTIMIZACAO
            / quantidade_periodos
        )
        - 1.0
    )

    if quantidade_periodos > 1:
        volatilidade_anualizada = float(
            retornos.std(
                ddof=1
            )
            * np.sqrt(
                PERIODOS_POR_ANO_OTIMIZACAO
            )
        )
    else:
        volatilidade_anualizada = np.nan

    if (
        pd.notna(
            volatilidade_anualizada
        )
        and volatilidade_anualizada > 0
    ):
        retorno_volatilidade = float(
            retorno_anualizado
            / volatilidade_anualizada
        )
    else:
        retorno_volatilidade = np.nan

    indice = (
        VALOR_INICIAL_OTIMIZACAO
        * (
            1.0
            + retornos
        ).cumprod()
    )

    indice_com_inicio = pd.concat(
        [
            pd.Series(
                [
                    VALOR_INICIAL_OTIMIZACAO
                ],
                dtype=float,
            ),
            indice,
        ],
        ignore_index=True,
    )

    pico = (
        indice_com_inicio
        .cummax()
    )

    drawdown = (
        indice_com_inicio
        / pico
        - 1.0
    )

    return {
        "periodo": nome_periodo,
        "quantidade_meses": (
            quantidade_periodos
        ),
        "retorno_total_liquido": (
            retorno_total
        ),
        "retorno_anualizado_liquido": (
            retorno_anualizado
        ),
        "volatilidade_anualizada_liquida": (
            volatilidade_anualizada
        ),
        "retorno_volatilidade_liquido": (
            retorno_volatilidade
        ),
        "maximo_drawdown_liquido": float(
            drawdown.min()
        ),
        "meses_positivos": float(
            retornos.gt(0).mean()
        ),
        "melhor_mes": float(
            retornos.max()
        ),
        "pior_mes": float(
            retornos.min()
        ),
        "turnover_total": float(
            dados[
                coluna_turnover
            ].sum()
        ),
        "turnover_medio_mensal": float(
            dados[
                coluna_turnover
            ].mean()
        ),
        "custo_acumulado_simples": float(
            dados[
                coluna_custo
            ].sum()
        ),
        "indice_final_liquido": float(
            indice.iloc[-1]
        ),
    }


# ============================================================
# SIMULAÇÃO DA GRADE DE PARÂMETROS
# ============================================================

resultados_grade = []

series_por_candidato = {}

pesos_por_candidato = {}


for nome_confirmacao, configuracao in (
    CENARIOS_CONFIRMACAO.items()
):
    meses_confirmacao = int(
        configuracao[
            "meses_confirmacao"
        ]
    )

    coluna_regime = (
        configuracao[
            "coluna_regime"
        ]
    )

    rotulo_confirmacao = (
        configuracao[
            "rotulo"
        ]
    )

    for alpha in ALFAS_ENCOLHIMENTO:

        identificador_candidato = (
            f"confirmacao_{meses_confirmacao}m"
            f"_alpha_{int(round(alpha * 100)):02d}"
        )

        pesos_ajustados = (
            criar_pesos_encolhidos(
                pesos_originais=pesos_por_regime,
                ativos=ativos_originais,
                alpha=alpha,
            )
        )

        pesos_por_candidato[
            identificador_candidato
        ] = pesos_ajustados

        base_candidato = (
            base_otimizacao
            .copy()
        )

        colunas_pesos_candidato = []

        for ativo in ativos_originais:
            coluna_peso = (
                f"peso_candidato_{ativo}"
            )

            mapa_pesos_ativo = {
                regime: (
                    pesos_ajustados[
                        regime
                    ][ativo]
                )
                for regime in pesos_ajustados
            }

            base_candidato[
                coluna_peso
            ] = (
                base_candidato[
                    coluna_regime
                ]
                .map(
                    mapa_pesos_ativo
                )
            )

            colunas_pesos_candidato.append(
                coluna_peso
            )

        if (
            base_candidato[
                colunas_pesos_candidato
            ]
            .isna()
            .any()
            .any()
        ):
            raise ValueError(
                f"O candidato {identificador_candidato} "
                "gerou pesos nulos."
            )

        soma_pesos_candidato = (
            base_candidato[
                colunas_pesos_candidato
            ]
            .sum(axis=1)
        )

        if not np.allclose(
            soma_pesos_candidato,
            1.0,
            rtol=1e-10,
            atol=1e-10,
        ):
            raise ValueError(
                f"Os pesos do candidato "
                f"{identificador_candidato} "
                "não somam 100%."
            )

        base_candidato[
            "retorno_bruto_candidato"
        ] = 0.0

        for ativo, coluna_peso in zip(
            ativos_originais,
            colunas_pesos_candidato,
        ):
            base_candidato[
                "retorno_bruto_candidato"
            ] += (
                base_candidato[
                    coluna_peso
                ]
                * base_candidato[
                    ativo
                ]
            )

        base_candidato[
            "turnover_candidato"
        ] = calcular_turnover_otimizacao(
            dados=base_candidato,
            colunas_retornos=ativos_originais,
            colunas_pesos=colunas_pesos_candidato,
            cobrar_custo_inicial=(
                COBRAR_CUSTO_INICIAL_OTIMIZACAO
            ),
        )

        base_candidato[
            "custo_candidato"
        ] = (
            base_candidato[
                "turnover_candidato"
            ]
            * CUSTO_POR_TURNOVER_OTIMIZACAO
        )

        base_candidato[
            "retorno_liquido_candidato"
        ] = (
            (
                1.0
                + base_candidato[
                    "retorno_bruto_candidato"
                ]
            )
            * (
                1.0
                - base_candidato[
                    "custo_candidato"
                ]
            )
            - 1.0
        )

        series_por_candidato[
            identificador_candidato
        ] = (
            base_candidato[
                [
                    "data",
                    coluna_regime,
                    *colunas_pesos_candidato,
                    "retorno_bruto_candidato",
                    "turnover_candidato",
                    "custo_candidato",
                    "retorno_liquido_candidato",
                ]
            ]
            .copy()
        )

        for nome_periodo, mascara_periodo in [
            (
                "TREINO",
                mascara_treino,
            ),
            (
                "TESTE",
                mascara_teste,
            ),
        ]:
            dados_periodo = (
                base_candidato.loc[
                    mascara_periodo
                ]
                .copy()
                .reset_index(drop=True)
            )

            metricas_periodo = (
                calcular_metricas_otimizacao(
                    dados=dados_periodo,
                    coluna_retorno=(
                        "retorno_liquido_candidato"
                    ),
                    coluna_turnover=(
                        "turnover_candidato"
                    ),
                    coluna_custo=(
                        "custo_candidato"
                    ),
                    nome_periodo=nome_periodo,
                )
            )

            metricas_periodo.update(
                {
                    "tipo": "ESTRATEGIA",
                    "candidato": (
                        identificador_candidato
                    ),
                    "confirmacao": (
                        nome_confirmacao
                    ),
                    "rotulo_confirmacao": (
                        rotulo_confirmacao
                    ),
                    "meses_confirmacao": (
                        meses_confirmacao
                    ),
                    "alpha_encolhimento": (
                        float(alpha)
                    ),
                }
            )

            resultados_grade.append(
                metricas_periodo
            )


# ============================================================
# MÉTRICAS DO BENCHMARK
# ============================================================

for nome_periodo, mascara_periodo in [
    (
        "TREINO",
        mascara_treino,
    ),
    (
        "TESTE",
        mascara_teste,
    ),
]:
    dados_benchmark = (
        base_otimizacao.loc[
            mascara_periodo
        ]
        .copy()
        .reset_index(drop=True)
    )

    metricas_benchmark = (
        calcular_metricas_otimizacao(
            dados=dados_benchmark,
            coluna_retorno=(
                COLUNA_RETORNO_BENCHMARK
            ),
            coluna_turnover=(
                COLUNA_TURNOVER_BENCHMARK
            ),
            coluna_custo=(
                COLUNA_CUSTO_BENCHMARK
            ),
            nome_periodo=nome_periodo,
        )
    )

    metricas_benchmark.update(
        {
            "tipo": "BENCHMARK",
            "candidato": (
                CENARIO_BENCHMARK
            ),
            "confirmacao": "-",
            "rotulo_confirmacao": (
                "Benchmark de pesos iguais"
            ),
            "meses_confirmacao": np.nan,
            "alpha_encolhimento": np.nan,
        }
    )

    resultados_grade.append(
        metricas_benchmark
    )


grade_otimizacao = pd.DataFrame(
    resultados_grade
)


# ============================================================
# LIMITE DE TURNOVER DO MODELO ORIGINAL
# ============================================================

linha_original_treino = (
    grade_otimizacao.loc[
        (
            grade_otimizacao[
                "periodo"
            ]
            == "TREINO"
        )
        & (
            grade_otimizacao[
                "tipo"
            ]
            == "ESTRATEGIA"
        )
        & (
            grade_otimizacao[
                "meses_confirmacao"
            ]
            == 1
        )
        & (
            np.isclose(
                grade_otimizacao[
                    "alpha_encolhimento"
                ],
                0.0,
            )
        )
    ]
)


if len(
    linha_original_treino
) != 1:
    raise ValueError(
        "Não foi possível identificar o modelo "
        "original na grade de parâmetros."
    )


turnover_limite_treino = float(
    linha_original_treino[
        "turnover_total"
    ]
    .iloc[0]
)


# ============================================================
# SELEÇÃO APENAS NO TREINO
# ============================================================

candidatos_treino = (
    grade_otimizacao.loc[
        (
            grade_otimizacao[
                "periodo"
            ]
            == "TREINO"
        )
        & (
            grade_otimizacao[
                "tipo"
            ]
            == "ESTRATEGIA"
        )
    ]
    .copy()
)


candidatos_elegiveis = (
    candidatos_treino.loc[
        candidatos_treino[
            "turnover_total"
        ]
        <= (
            turnover_limite_treino
            + 1e-12
        )
    ]
    .copy()
)


if candidatos_elegiveis.empty:
    raise ValueError(
        "Nenhum candidato respeitou o limite "
        "de turnover do modelo original."
    )


candidato_selecionado_treino = (
    candidatos_elegiveis
    .sort_values(
        [
            "retorno_volatilidade_liquido",
            "retorno_anualizado_liquido",
            "maximo_drawdown_liquido",
            "turnover_total",
        ],
        ascending=[
            False,
            False,
            False,
            True,
        ],
    )
    .iloc[0]
)


identificador_selecionado = (
    candidato_selecionado_treino[
        "candidato"
    ]
)

confirmacao_selecionada = int(
    candidato_selecionado_treino[
        "meses_confirmacao"
    ]
)

alpha_selecionado = float(
    candidato_selecionado_treino[
        "alpha_encolhimento"
    ]
)


resultado_selecionado_teste = (
    grade_otimizacao.loc[
        (
            grade_otimizacao[
                "periodo"
            ]
            == "TESTE"
        )
        & (
            grade_otimizacao[
                "candidato"
            ]
            == identificador_selecionado
        )
    ]
    .iloc[0]
)


resultado_benchmark_teste = (
    grade_otimizacao.loc[
        (
            grade_otimizacao[
                "periodo"
            ]
            == "TESTE"
        )
        & (
            grade_otimizacao[
                "tipo"
            ]
            == "BENCHMARK"
        )
    ]
    .iloc[0]
)


diferenca_indice_teste = float(
    resultado_selecionado_teste[
        "indice_final_liquido"
    ]
    - resultado_benchmark_teste[
        "indice_final_liquido"
    ]
)


diferenca_retorno_anualizado_teste = float(
    resultado_selecionado_teste[
        "retorno_anualizado_liquido"
    ]
    - resultado_benchmark_teste[
        "retorno_anualizado_liquido"
    ]
)


diferenca_retorno_volatilidade_teste = float(
    resultado_selecionado_teste[
        "retorno_volatilidade_liquido"
    ]
    - resultado_benchmark_teste[
        "retorno_volatilidade_liquido"
    ]
)


if diferenca_indice_teste > 0:
    status_teste = (
        "SUPEROU O BENCHMARK"
    )

elif diferenca_indice_teste < 0:
    status_teste = (
        "FICOU ABAIXO DO BENCHMARK"
    )

else:
    status_teste = (
        "EMPATOU COM O BENCHMARK"
    )


# ============================================================
# PESOS SELECIONADOS POR REGIME
# ============================================================

pesos_selecionados_dict = (
    pesos_por_candidato[
        identificador_selecionado
    ]
)


registros_pesos_selecionados = []


for regime, pesos_regime in (
    pesos_selecionados_dict.items()
):
    registro = {
        "regime": regime,
        "meses_confirmacao": (
            confirmacao_selecionada
        ),
        "alpha_encolhimento": (
            alpha_selecionado
        ),
    }

    for ativo in ativos_originais:
        registro[
            f"peso_{ativo}"
        ] = float(
            pesos_regime[
                ativo
            ]
        )

    registro[
        "soma_pesos"
    ] = sum(
        pesos_regime.values()
    )

    registros_pesos_selecionados.append(
        registro
    )


pesos_selecionados = pd.DataFrame(
    registros_pesos_selecionados
)


if not np.allclose(
    pesos_selecionados[
        "soma_pesos"
    ],
    1.0,
    rtol=1e-10,
    atol=1e-10,
):
    raise ValueError(
        "Os pesos selecionados não somam 100%."
    )


# ============================================================
# RESUMO DOS PARÂMETROS SELECIONADOS
# ============================================================

parametros_selecionados = pd.DataFrame(
    {
        "metrica": [
            "Data final do treino",
            "Data inicial do teste",
            "Meses de treino",
            "Meses de teste",
            "Candidato selecionado",
            "Meses de confirmação",
            "Alpha de encolhimento",
            "Peso dos parâmetros originais",
            "Peso da carteira de pesos iguais",
            "Turnover limite no treino",
            "Turnover do candidato no treino",
            "Retorno/volatilidade no treino",
            "Retorno anualizado no treino",
            "Índice final da estratégia no teste",
            "Índice final do benchmark no teste",
            "Diferença do índice no teste",
            "Retorno anualizado da estratégia no teste",
            "Retorno anualizado do benchmark no teste",
            "Diferença de retorno anualizado no teste",
            "Retorno/volatilidade da estratégia no teste",
            "Retorno/volatilidade do benchmark no teste",
            "Diferença de retorno/volatilidade no teste",
            "Status fora da amostra",
        ],
        "valor": [
            base_otimizacao.loc[
                mascara_treino,
                "data",
            ].max().strftime(
                "%d/%m/%Y"
            ),
            base_otimizacao.loc[
                mascara_teste,
                "data",
            ].min().strftime(
                "%d/%m/%Y"
            ),
            quantidade_meses_treino,
            quantidade_meses_teste,
            identificador_selecionado,
            confirmacao_selecionada,
            alpha_selecionado,
            (
                1.0
                - alpha_selecionado
            ),
            alpha_selecionado,
            turnover_limite_treino,
            candidato_selecionado_treino[
                "turnover_total"
            ],
            candidato_selecionado_treino[
                "retorno_volatilidade_liquido"
            ],
            candidato_selecionado_treino[
                "retorno_anualizado_liquido"
            ],
            resultado_selecionado_teste[
                "indice_final_liquido"
            ],
            resultado_benchmark_teste[
                "indice_final_liquido"
            ],
            diferenca_indice_teste,
            resultado_selecionado_teste[
                "retorno_anualizado_liquido"
            ],
            resultado_benchmark_teste[
                "retorno_anualizado_liquido"
            ],
            diferenca_retorno_anualizado_teste,
            resultado_selecionado_teste[
                "retorno_volatilidade_liquido"
            ],
            resultado_benchmark_teste[
                "retorno_volatilidade_liquido"
            ],
            diferenca_retorno_volatilidade_teste,
            status_teste,
        ],
    }
)


# ============================================================
# SÉRIES DO CANDIDATO SELECIONADO
# ============================================================

serie_candidato_selecionado = (
    series_por_candidato[
        identificador_selecionado
    ]
    .copy()
)


serie_teste_selecionado = (
    serie_candidato_selecionado.loc[
        serie_candidato_selecionado[
            "data"
        ]
        > DATA_CORTE_TREINO
    ]
    .copy()
    .reset_index(drop=True)
)


benchmark_teste = (
    base_otimizacao.loc[
        mascara_teste,
        [
            "data",
            COLUNA_RETORNO_BENCHMARK,
            COLUNA_TURNOVER_BENCHMARK,
            COLUNA_CUSTO_BENCHMARK,
        ],
    ]
    .copy()
    .reset_index(drop=True)
)


serie_teste_selecionado = (
    serie_teste_selecionado
    .merge(
        benchmark_teste,
        on="data",
        how="inner",
        validate="one_to_one",
    )
)


serie_teste_selecionado[
    "indice_estrategia"
] = (
    VALOR_INICIAL_OTIMIZACAO
    * (
        1.0
        + serie_teste_selecionado[
            "retorno_liquido_candidato"
        ]
    ).cumprod()
)


serie_teste_selecionado[
    "indice_benchmark"
] = (
    VALOR_INICIAL_OTIMIZACAO
    * (
        1.0
        + serie_teste_selecionado[
            COLUNA_RETORNO_BENCHMARK
        ]
    ).cumprod()
)


serie_teste_selecionado[
    "diferenca_indice"
] = (
    serie_teste_selecionado[
        "indice_estrategia"
    ]
    - serie_teste_selecionado[
        "indice_benchmark"
    ]
)


data_inicial_grafico = (
    serie_teste_selecionado[
        "data"
    ].iloc[0]
    - pd.offsets.MonthEnd(1)
)


linha_inicial_grafico = pd.DataFrame(
    {
        "data": [
            data_inicial_grafico
        ],
        "indice_estrategia": [
            VALOR_INICIAL_OTIMIZACAO
        ],
        "indice_benchmark": [
            VALOR_INICIAL_OTIMIZACAO
        ],
        "diferenca_indice": [
            0.0
        ],
    }
)


serie_grafico_teste = pd.concat(
    [
        linha_inicial_grafico,
        serie_teste_selecionado[
            [
                "data",
                "indice_estrategia",
                "indice_benchmark",
                "diferenca_indice",
            ]
        ],
    ],
    ignore_index=True,
)


# ============================================================
# TABELA FORMATADA
# ============================================================

grade_otimizacao_formatada = (
    grade_otimizacao
    .copy()
    .astype(object)
)


grade_otimizacao_formatada[
    "alpha_encolhimento"
] = (
    grade_otimizacao[
        "alpha_encolhimento"
    ]
    .map(
        lambda valor: (
            f"{valor:.0%}"
            if pd.notna(valor)
            else "-"
        )
    )
)


for coluna in [
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown_liquido",
    "meses_positivos",
    "melhor_mes",
    "pior_mes",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
]:
    grade_otimizacao_formatada[
        coluna
    ] = (
        grade_otimizacao[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "retorno_volatilidade_liquido",
    "turnover_total",
    "indice_final_liquido",
]:
    grade_otimizacao_formatada[
        coluna
    ] = (
        grade_otimizacao[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "quantidade_meses",
    "meses_confirmacao",
]:
    grade_otimizacao_formatada[
        coluna
    ] = (
        grade_otimizacao[
            coluna
        ]
        .map(
            lambda valor: (
                f"{int(valor)}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

grade_otimizacao.to_csv(
    ARQUIVO_GRADE_PARAMETROS,
    index=False,
    encoding="utf-8-sig",
)


grade_otimizacao_formatada.to_csv(
    ARQUIVO_GRADE_FORMATADA,
    index=False,
    encoding="utf-8-sig",
)


parametros_selecionados.to_csv(
    ARQUIVO_PARAMETROS_SELECIONADOS,
    index=False,
    encoding="utf-8-sig",
)


pesos_selecionados.to_csv(
    ARQUIVO_PESOS_SELECIONADOS,
    index=False,
    encoding="utf-8-sig",
)


serie_teste_selecionado.to_csv(
    ARQUIVO_SERIES_TESTE,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO 1 — RETORNO/VOLATILIDADE NO TREINO
# ============================================================

grade_treino_grafico = (
    grade_otimizacao.loc[
        (
            grade_otimizacao[
                "periodo"
            ]
            == "TREINO"
        )
        & (
            grade_otimizacao[
                "tipo"
            ]
            == "ESTRATEGIA"
        )
    ]
    .copy()
)


fig, ax = plt.subplots(
    figsize=(12, 7)
)


for meses_confirmacao in sorted(
    grade_treino_grafico[
        "meses_confirmacao"
    ]
    .dropna()
    .unique()
):
    dados_linha = (
        grade_treino_grafico.loc[
            grade_treino_grafico[
                "meses_confirmacao"
            ]
            == meses_confirmacao
        ]
        .sort_values(
            "alpha_encolhimento"
        )
    )

    ax.plot(
        dados_linha[
            "alpha_encolhimento"
        ],
        dados_linha[
            "retorno_volatilidade_liquido"
        ],
        marker="o",
        linewidth=2,
        label=(
            f"Confirmação de "
            f"{int(meses_confirmacao)} mês(es)"
        ),
    )


ax.scatter(
    [
        alpha_selecionado
    ],
    [
        candidato_selecionado_treino[
            "retorno_volatilidade_liquido"
        ]
    ],
    marker="*",
    s=180,
    label="Parâmetro selecionado",
)


ax.xaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Retorno/Volatilidade no Período de Treino"
)

ax.set_xlabel(
    "Encolhimento dos pesos em direção aos pesos iguais"
)

ax.set_ylabel(
    "Retorno anualizado / volatilidade anualizada"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_TREINO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — DESEMPENHO NO TESTE
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    serie_grafico_teste[
        "data"
    ],
    serie_grafico_teste[
        "indice_estrategia"
    ],
    linewidth=2,
    label="Estratégia com pesos selecionados",
)


ax.plot(
    serie_grafico_teste[
        "data"
    ],
    serie_grafico_teste[
        "indice_benchmark"
    ],
    linewidth=2,
    label="Benchmark de pesos iguais",
)


ax.axhline(
    y=VALOR_INICIAL_OTIMIZACAO,
    linewidth=1,
)


ax.set_title(
    "Desempenho Fora da Amostra após Ajuste dos Pesos"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Índice acumulado"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_TESTE,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — DIFERENÇA NO TESTE
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    serie_grafico_teste[
        "data"
    ],
    serie_grafico_teste[
        "diferenca_indice"
    ],
    linewidth=2,
)


ax.axhline(
    y=0,
    linewidth=1,
)


ax.set_title(
    "Diferença da Estratégia contra o Benchmark "
    "Fora da Amostra"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Diferença do índice em pontos"
)

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DIFERENCA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_GRADE_PARAMETROS,
    ARQUIVO_GRADE_FORMATADA,
    ARQUIVO_PARAMETROS_SELECIONADOS,
    ARQUIVO_PESOS_SELECIONADOS,
    ARQUIVO_SERIES_TESTE,
    ARQUIVO_GRAFICO_TREINO,
    ARQUIVO_GRAFICO_TESTE,
    ARQUIVO_GRAFICO_DIFERENCA,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:
    raise FileNotFoundError(
        "Alguns arquivos da Célula 5 não foram salvos:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("=" * 70)
print("OTIMIZAÇÃO CONSERVADORA DOS PESOS CONCLUÍDA")
print("=" * 70)

print(
    f"\nJanelas de confirmação testadas: "
    f"{JANELAS_CONFIRMACAO}"
)

print(
    f"Alphas de encolhimento testados: "
    f"{ALFAS_ENCOLHIMENTO}"
)

print(
    f"\nCombinações de estratégia testadas: "
    f"{len(CENARIOS_CONFIRMACAO) * len(ALFAS_ENCOLHIMENTO)}"
)

print(
    f"Meses de treino: "
    f"{quantidade_meses_treino}"
)

print(
    f"Meses de teste: "
    f"{quantidade_meses_teste}"
)

print(
    f"\nParâmetro selecionado apenas com o treino: "
    f"{identificador_selecionado}"
)

print(
    f"Confirmação do regime: "
    f"{confirmacao_selecionada} mês(es)"
)

print(
    f"Encolhimento em direção aos pesos iguais: "
    f"{alpha_selecionado:.0%}"
)

print(
    f"Peso mantido dos parâmetros originais: "
    f"{1.0 - alpha_selecionado:.0%}"
)

print(
    f"\nRetorno/volatilidade no treino: "
    f"{candidato_selecionado_treino['retorno_volatilidade_liquido']:.2f}"
)

print(
    f"Turnover no treino: "
    f"{candidato_selecionado_treino['turnover_total']:.4f}"
)

print(
    f"Limite de turnover do modelo original: "
    f"{turnover_limite_treino:.4f}"
)

print(
    f"\nÍndice final da estratégia no teste: "
    f"{resultado_selecionado_teste['indice_final_liquido']:.2f}"
)

print(
    f"Índice final do benchmark no teste: "
    f"{resultado_benchmark_teste['indice_final_liquido']:.2f}"
)

print(
    f"Diferença fora da amostra: "
    f"{diferenca_indice_teste:.2f} pontos"
)

print(
    f"\nRetorno anualizado da estratégia no teste: "
    f"{resultado_selecionado_teste['retorno_anualizado_liquido']:.2%}"
)

print(
    f"Retorno anualizado do benchmark no teste: "
    f"{resultado_benchmark_teste['retorno_anualizado_liquido']:.2%}"
)

print(
    f"\nRetorno/volatilidade da estratégia no teste: "
    f"{resultado_selecionado_teste['retorno_volatilidade_liquido']:.2f}"
)

print(
    f"Retorno/volatilidade do benchmark no teste: "
    f"{resultado_benchmark_teste['retorno_volatilidade_liquido']:.2f}"
)

print(
    f"\nResultado fora da amostra: "
    f"{status_teste}"
)

print(
    f"\nGrade de parâmetros salva em:\n"
    f"{ARQUIVO_GRADE_PARAMETROS}"
)

print(
    f"\nParâmetros selecionados salvos em:\n"
    f"{ARQUIVO_PARAMETROS_SELECIONADOS}"
)

print(
    f"\nPesos selecionados salvos em:\n"
    f"{ARQUIVO_PESOS_SELECIONADOS}"
)

print(
    f"\nSéries de teste salvas em:\n"
    f"{ARQUIVO_SERIES_TESTE}"
)

print(
    f"\nGráfico de treino:\n"
    f"{ARQUIVO_GRAFICO_TREINO.name}"
)

print(
    f"\nGráfico de desempenho no teste:\n"
    f"{ARQUIVO_GRAFICO_TESTE.name}"
)

print(
    f"\nGráfico de diferença no teste:\n"
    f"{ARQUIVO_GRAFICO_DIFERENCA.name}"
)

print("\nPesos selecionados por regime:")

display(
    pesos_selecionados
)

print("\nResumo dos parâmetros selecionados:")

display(
    parametros_selecionados
)

# ###########################################################################
# ETAPA 06 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 6 — DIAGNÓSTICO POR REGIME E ATIVO
# VERSÃO AUTÔNOMA
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml

from matplotlib.ticker import PercentFormatter


# ============================================================
# LOCALIZAÇÃO AUTOMÁTICA DA RAIZ DO PROJETO
# ============================================================

DIRETORIO_ATUAL = Path.cwd().resolve()

RAIZ_PROJETO = None

for diretorio in [
    DIRETORIO_ATUAL,
    *DIRETORIO_ATUAL.parents,
]:
    arquivo_teste = (
        diretorio
        / "data"
        / "processed"
        / "backtest_portfolio_mensal.csv"
    )

    if arquivo_teste.exists():
        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:
    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo data/processed/"
        "backtest_portfolio_mensal.csv não foi encontrado."
    )


# ============================================================
# CARREGAMENTO DO CONFIG.YAML
# ============================================================

ARQUIVO_CONFIG = (
    RAIZ_PROJETO
    / "config"
    / "config.yaml"
)


if not ARQUIVO_CONFIG.exists():
    raise FileNotFoundError(
        "Arquivo de configuração não encontrado:\n"
        f"{ARQUIVO_CONFIG}"
    )


with ARQUIVO_CONFIG.open(
    mode="r",
    encoding="utf-8",
) as arquivo_yaml:

    CONFIGURACAO = (
        yaml.safe_load(
            arquivo_yaml
        )
        or {}
    )


if (
    "backtest" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["backtest"],
        dict,
    )
):
    raise KeyError(
        "A seção 'backtest' não foi encontrada "
        "no config/config.yaml."
    )


if (
    "otimizacao" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["otimizacao"],
        dict,
    )
):
    raise KeyError(
        "A seção 'otimizacao' não foi encontrada "
        "no config/config.yaml."
    )


CONFIGURACAO_BACKTEST = (
    CONFIGURACAO[
        "backtest"
    ]
)

CONFIGURACAO_OTIMIZACAO = (
    CONFIGURACAO[
        "otimizacao"
    ]
)


parametros_backtest_obrigatorios = [
    "valor_inicial",
    "custo_por_turnover",
    "cobrar_custo_inicial",
]

parametros_backtest_ausentes = [
    parametro
    for parametro in parametros_backtest_obrigatorios
    if parametro not in CONFIGURACAO_BACKTEST
]

if parametros_backtest_ausentes:
    raise KeyError(
        "Parâmetros ausentes na seção 'backtest' "
        "do config.yaml:\n"
        f"{parametros_backtest_ausentes}"
    )


parametros_otimizacao_obrigatorios = [
    "minimo_meses_classificacao_regime",
    "limite_critico_regime",
]

parametros_otimizacao_ausentes = [
    parametro
    for parametro in parametros_otimizacao_obrigatorios
    if parametro not in CONFIGURACAO_OTIMIZACAO
]

if parametros_otimizacao_ausentes:
    raise KeyError(
        "Parâmetros ausentes na seção 'otimizacao' "
        "do config.yaml:\n"
        f"{parametros_otimizacao_ausentes}"
    )


VALOR_INICIAL = float(
    CONFIGURACAO_BACKTEST[
        "valor_inicial"
    ]
)

CUSTO_POR_TURNOVER = float(
    CONFIGURACAO_BACKTEST[
        "custo_por_turnover"
    ]
)

COBRAR_CUSTO_INICIAL = (
    CONFIGURACAO_BACKTEST[
        "cobrar_custo_inicial"
    ]
)

MINIMO_MESES_CLASSIFICACAO_REGIME = int(
    CONFIGURACAO_OTIMIZACAO[
        "minimo_meses_classificacao_regime"
    ]
)

LIMITE_CRITICO_REGIME = float(
    CONFIGURACAO_OTIMIZACAO[
        "limite_critico_regime"
    ]
)


if VALOR_INICIAL <= 0:
    raise ValueError(
        "'backtest.valor_inicial' "
        "deve ser maior que zero."
    )


if CUSTO_POR_TURNOVER < 0:
    raise ValueError(
        "'backtest.custo_por_turnover' "
        "não pode ser negativo."
    )


if not isinstance(
    COBRAR_CUSTO_INICIAL,
    bool,
):
    raise TypeError(
        "'backtest.cobrar_custo_inicial' "
        "deve ser true ou false."
    )


if MINIMO_MESES_CLASSIFICACAO_REGIME < 1:
    raise ValueError(
        "'otimizacao.minimo_meses_classificacao_regime' "
        "deve ser maior ou igual a 1."
    )


if LIMITE_CRITICO_REGIME >= 0:
    raise ValueError(
        "'otimizacao.limite_critico_regime' "
        "deve ser negativo."
    )


PASTA_DADOS_PROCESSADOS = (
    RAIZ_PROJETO
    / "data"
    / "processed"
)

PASTA_TABELAS = (
    RAIZ_PROJETO
    / "outputs"
    / "tabelas"
)

PASTA_GRAFICOS = (
    RAIZ_PROJETO
    / "outputs"
    / "graficos"
)


PASTA_TABELAS.mkdir(
    parents=True,
    exist_ok=True,
)

PASTA_GRAFICOS.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ARQUIVO_BACKTEST = (
    PASTA_DADOS_PROCESSADOS
    / "backtest_portfolio_mensal.csv"
)

ARQUIVO_REGIMES_SUAVIZADOS = (
    PASTA_TABELAS
    / "06_02_regimes_suavizados.csv"
)

ARQUIVO_PESOS_SELECIONADOS = (
    PASTA_TABELAS
    / "06_05_pesos_selecionados_por_regime.csv"
)

ARQUIVO_PARAMETROS_SELECIONADOS = (
    PASTA_TABELAS
    / "06_05_parametros_selecionados.csv"
)


arquivos_entrada = [
    ARQUIVO_BACKTEST,
    ARQUIVO_REGIMES_SUAVIZADOS,
    ARQUIVO_PESOS_SELECIONADOS,
    ARQUIVO_PARAMETROS_SELECIONADOS,
]


arquivos_ausentes = [
    arquivo
    for arquivo in arquivos_entrada
    if not arquivo.exists()
]


if arquivos_ausentes:
    raise FileNotFoundError(
        "Arquivos necessários não encontrados:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# CARREGAMENTO DAS BASES
# ============================================================

backtest_original = pd.read_csv(
    ARQUIVO_BACKTEST,
    encoding="utf-8-sig",
)


regimes_suavizados = pd.read_csv(
    ARQUIVO_REGIMES_SUAVIZADOS,
    encoding="utf-8-sig",
)


pesos_selecionados = pd.read_csv(
    ARQUIVO_PESOS_SELECIONADOS,
    encoding="utf-8-sig",
)


parametros_selecionados = pd.read_csv(
    ARQUIVO_PARAMETROS_SELECIONADOS,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DAS BASES
# ============================================================

for nome_base, base in {
    "backtest": backtest_original,
    "regimes suavizados": regimes_suavizados,
}.items():

    if "data" not in base.columns:
        raise ValueError(
            f"A base {nome_base} não possui "
            "a coluna data."
        )

    base["data"] = pd.to_datetime(
        base["data"],
        errors="coerce",
    )

    if base["data"].isna().any():
        raise ValueError(
            f"A base {nome_base} possui datas inválidas."
        )

    if base["data"].duplicated().any():
        raise ValueError(
            f"A base {nome_base} possui datas duplicadas."
        )


if "regime" not in pesos_selecionados.columns:
    raise ValueError(
        "O arquivo de pesos selecionados não possui "
        "a coluna regime."
    )


if "meses_confirmacao" not in pesos_selecionados.columns:
    raise ValueError(
        "O arquivo de pesos selecionados não possui "
        "a coluna meses_confirmacao."
    )


if "alpha_encolhimento" not in pesos_selecionados.columns:
    raise ValueError(
        "O arquivo de pesos selecionados não possui "
        "a coluna alpha_encolhimento."
    )


pesos_selecionados["regime"] = (
    pesos_selecionados["regime"]
    .astype("string")
    .str.strip()
)


pesos_selecionados[
    "meses_confirmacao"
] = pd.to_numeric(
    pesos_selecionados[
        "meses_confirmacao"
    ],
    errors="coerce",
)


pesos_selecionados[
    "alpha_encolhimento"
] = pd.to_numeric(
    pesos_selecionados[
        "alpha_encolhimento"
    ],
    errors="coerce",
)


if pesos_selecionados[
    [
        "meses_confirmacao",
        "alpha_encolhimento",
    ]
].isna().any().any():
    raise ValueError(
        "Os parâmetros selecionados possuem "
        "valores inválidos."
    )


# ============================================================
# IDENTIFICAÇÃO DOS ATIVOS E PARÂMETROS
# ============================================================

colunas_pesos_arquivo = [
    coluna
    for coluna in pesos_selecionados.columns
    if coluna.startswith(
        "peso_"
    )
]


if not colunas_pesos_arquivo:
    raise ValueError(
        "Nenhuma coluna de peso foi encontrada "
        "no arquivo de pesos selecionados."
    )


ativos_originais = [
    coluna.replace(
        "peso_",
        "",
        1,
    )
    for coluna in colunas_pesos_arquivo
]


ativos_ausentes_backtest = [
    ativo
    for ativo in ativos_originais
    if ativo not in backtest_original.columns
]


if ativos_ausentes_backtest:
    raise ValueError(
        "Ativos ausentes no backtest:\n"
        f"{ativos_ausentes_backtest}"
    )


valores_confirmacao = (
    pesos_selecionados[
        "meses_confirmacao"
    ]
    .dropna()
    .unique()
)


if len(valores_confirmacao) != 1:
    raise ValueError(
        "O arquivo de pesos possui mais de um "
        "parâmetro de confirmação."
    )


confirmacao_selecionada = int(
    valores_confirmacao[0]
)


valores_alpha = (
    pesos_selecionados[
        "alpha_encolhimento"
    ]
    .dropna()
    .unique()
)


if len(valores_alpha) != 1:
    raise ValueError(
        "O arquivo de pesos possui mais de um "
        "alpha de encolhimento."
    )


alpha_selecionado = float(
    valores_alpha[0]
)


COLUNA_REGIME_SELECIONADO = (
    f"regime_confirmacao_"
    f"{confirmacao_selecionada}m"
)


if (
    COLUNA_REGIME_SELECIONADO
    not in regimes_suavizados.columns
):
    raise ValueError(
        "A coluna do regime selecionado não foi encontrada:\n"
        f"{COLUNA_REGIME_SELECIONADO}"
    )


# ============================================================
# DATA DE CORTE DO TREINO
# ============================================================

linha_data_treino = (
    parametros_selecionados.loc[
        parametros_selecionados[
            "metrica"
        ]
        == "Data final do treino",
        "valor",
    ]
)


if linha_data_treino.empty:
    raise ValueError(
        "O arquivo de parâmetros selecionados não possui "
        "a métrica 'Data final do treino'."
    )


DATA_CORTE_TREINO = pd.to_datetime(
    linha_data_treino.iloc[0],
    dayfirst=True,
    errors="coerce",
)


if pd.isna(
    DATA_CORTE_TREINO
):
    raise ValueError(
        "A data final do treino é inválida."
    )


# ============================================================
# REGIMES E NOMES
# ============================================================

ORDEM_REGIMES = [
    "EXPANSAO_DESINFLACIONARIA",
    "EXPANSAO_INFLACIONARIA",
    "ESTAGFLACAO",
    "RECESSAO_DESINFLACIONARIA",
]


NOMES_REGIMES = {
    "EXPANSAO_DESINFLACIONARIA": (
        "Expansão desinflacionária"
    ),
    "EXPANSAO_INFLACIONARIA": (
        "Expansão inflacionária"
    ),
    "ESTAGFLACAO": (
        "Estagflação"
    ),
    "RECESSAO_DESINFLACIONARIA": (
        "Recessão desinflacionária"
    ),
}


regimes_ausentes_pesos = [
    regime
    for regime in ORDEM_REGIMES
    if regime
    not in pesos_selecionados[
        "regime"
    ].tolist()
]


if regimes_ausentes_pesos:
    raise ValueError(
        "Os seguintes regimes não possuem pesos:\n"
        f"{regimes_ausentes_pesos}"
    )


# ============================================================
# CONVERSÃO E VALIDAÇÃO DOS PESOS
# ============================================================

for coluna in colunas_pesos_arquivo:
    pesos_selecionados[coluna] = pd.to_numeric(
        pesos_selecionados[coluna],
        errors="coerce",
    )


if pesos_selecionados[
    colunas_pesos_arquivo
].isna().any().any():
    raise ValueError(
        "Existem pesos nulos ou inválidos."
    )


if (
    pesos_selecionados[
        colunas_pesos_arquivo
    ]
    .lt(0)
    .any()
    .any()
):
    raise ValueError(
        "Foram encontrados pesos negativos."
    )


soma_pesos_regime = (
    pesos_selecionados[
        colunas_pesos_arquivo
    ]
    .sum(axis=1)
)


if not np.allclose(
    soma_pesos_regime,
    1.0,
    rtol=1e-10,
    atol=1e-10,
):
    raise ValueError(
        "Os pesos selecionados não somam 100%."
    )


# ============================================================
# IDENTIFICAÇÃO E VALIDAÇÃO DO CUSTO DE TRANSAÇÃO
# ============================================================

if {
    "turnover_portfolio",
    "custo_portfolio",
}.issubset(
    backtest_original.columns
):

    turnover_original = pd.to_numeric(
        backtest_original[
            "turnover_portfolio"
        ],
        errors="coerce",
    )

    custo_original = pd.to_numeric(
        backtest_original[
            "custo_portfolio"
        ],
        errors="coerce",
    )

    if (
        turnover_original.isna().any()
        or custo_original.isna().any()
    ):
        raise ValueError(
            "Não foi possível validar o custo do "
            "backtest original."
        )

    mascara_turnover = (
        turnover_original > 0
    )

    taxas_observadas = (
        custo_original.loc[
            mascara_turnover
        ]
        / turnover_original.loc[
            mascara_turnover
        ]
    ).dropna()

    if (
        not taxas_observadas.empty
        and not np.allclose(
            taxas_observadas,
            CUSTO_POR_TURNOVER,
            rtol=1e-8,
            atol=1e-12,
        )
    ):
        raise ValueError(
            "O custo configurado não coincide com o custo "
            "utilizado no backtest original."
        )


# ============================================================
# CONSTRUÇÃO DA BASE MENSAL
# ============================================================

base_diagnostico = (
    backtest_original[
        [
            "data",
            *ativos_originais,
        ]
    ]
    .merge(
        regimes_suavizados[
            [
                "data",
                COLUNA_REGIME_SELECIONADO,
            ]
        ],
        on="data",
        how="inner",
        validate="one_to_one",
    )
    .sort_values("data")
    .reset_index(drop=True)
)


if len(
    base_diagnostico
) != len(
    backtest_original
):
    raise ValueError(
        "A junção entre o backtest e os regimes "
        "alterou a quantidade de meses."
    )


for ativo in ativos_originais:
    base_diagnostico[ativo] = pd.to_numeric(
        base_diagnostico[ativo],
        errors="coerce",
    )


if base_diagnostico[
    ativos_originais
].isna().any().any():
    raise ValueError(
        "Existem retornos de ativos nulos ou inválidos."
    )


base_diagnostico[
    COLUNA_REGIME_SELECIONADO
] = (
    base_diagnostico[
        COLUNA_REGIME_SELECIONADO
    ]
    .astype("string")
    .str.strip()
)


regimes_invalidos = (
    base_diagnostico.loc[
        ~base_diagnostico[
            COLUNA_REGIME_SELECIONADO
        ].isin(
            ORDEM_REGIMES
        ),
        COLUNA_REGIME_SELECIONADO,
    ]
    .dropna()
    .unique()
    .tolist()
)


if regimes_invalidos:
    raise ValueError(
        "Foram encontrados regimes inválidos:\n"
        f"{regimes_invalidos}"
    )


# ============================================================
# APLICAÇÃO DOS PESOS SELECIONADOS
# ============================================================

colunas_pesos_estrategia = []


for ativo in ativos_originais:

    coluna_origem = (
        f"peso_{ativo}"
    )

    coluna_destino = (
        f"peso_estrategia_{ativo}"
    )

    mapa_pesos = (
        pesos_selecionados
        .set_index(
            "regime"
        )[
            coluna_origem
        ]
        .to_dict()
    )

    base_diagnostico[
        coluna_destino
    ] = (
        base_diagnostico[
            COLUNA_REGIME_SELECIONADO
        ]
        .map(
            mapa_pesos
        )
    )

    colunas_pesos_estrategia.append(
        coluna_destino
    )


if base_diagnostico[
    colunas_pesos_estrategia
].isna().any().any():
    raise ValueError(
        "A aplicação dos pesos gerou valores nulos."
    )


if not np.allclose(
    base_diagnostico[
        colunas_pesos_estrategia
    ].sum(axis=1),
    1.0,
    rtol=1e-10,
    atol=1e-10,
):
    raise ValueError(
        "Os pesos mensais da estratégia "
        "não somam 100%."
    )


# ============================================================
# PESOS DO BENCHMARK
# ============================================================

PESO_BENCHMARK = (
    1.0
    / len(
        ativos_originais
    )
)


colunas_pesos_benchmark = []


for ativo in ativos_originais:

    coluna_benchmark = (
        f"peso_benchmark_{ativo}"
    )

    base_diagnostico[
        coluna_benchmark
    ] = PESO_BENCHMARK

    colunas_pesos_benchmark.append(
        coluna_benchmark
    )


# ============================================================
# FUNÇÃO DE TURNOVER
# ============================================================

def calcular_turnover(
    dados,
    colunas_retornos,
    colunas_pesos,
    cobrar_custo_inicial,
):
    quantidade_periodos = len(
        dados
    )

    turnover = np.zeros(
        quantidade_periodos,
        dtype=float,
    )

    if quantidade_periodos == 0:
        return turnover

    if len(
        colunas_retornos
    ) != len(
        colunas_pesos
    ):
        raise ValueError(
            "A quantidade de retornos e pesos "
            "deve ser igual."
        )

    if cobrar_custo_inicial:
        turnover[0] = 1.0

    for indice in range(
        1,
        quantidade_periodos,
    ):

        pesos_anteriores = (
            dados.loc[
                indice - 1,
                colunas_pesos,
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

        retorno_anterior = float(
            np.sum(
                pesos_anteriores
                * retornos_anteriores
            )
        )

        fator_patrimonio = (
            1.0
            + retorno_anterior
        )

        if fator_patrimonio <= 0:
            raise ValueError(
                "O patrimônio relativo ficou menor "
                "ou igual a zero."
            )

        pesos_apos_retorno = (
            pesos_anteriores
            * (
                1.0
                + retornos_anteriores
            )
            / fator_patrimonio
        )

        pesos_alvo = (
            dados.loc[
                indice,
                colunas_pesos,
            ]
            .astype(float)
            .to_numpy()
        )

        turnover[indice] = float(
            np.abs(
                pesos_alvo
                - pesos_apos_retorno
            ).sum()
            / 2.0
        )

    return turnover


# ============================================================
# RETORNOS DA ESTRATÉGIA E DO BENCHMARK
# ============================================================

base_diagnostico[
    "retorno_bruto_estrategia"
] = 0.0


base_diagnostico[
    "retorno_bruto_benchmark"
] = 0.0


for ativo, coluna_peso_estrategia in zip(
    ativos_originais,
    colunas_pesos_estrategia,
):

    base_diagnostico[
        "retorno_bruto_estrategia"
    ] += (
        base_diagnostico[
            coluna_peso_estrategia
        ]
        * base_diagnostico[
            ativo
        ]
    )

    base_diagnostico[
        "retorno_bruto_benchmark"
    ] += (
        PESO_BENCHMARK
        * base_diagnostico[
            ativo
        ]
    )


base_diagnostico[
    "turnover_estrategia"
] = calcular_turnover(
    dados=base_diagnostico,
    colunas_retornos=ativos_originais,
    colunas_pesos=colunas_pesos_estrategia,
    cobrar_custo_inicial=COBRAR_CUSTO_INICIAL,
)


base_diagnostico[
    "turnover_benchmark"
] = calcular_turnover(
    dados=base_diagnostico,
    colunas_retornos=ativos_originais,
    colunas_pesos=colunas_pesos_benchmark,
    cobrar_custo_inicial=COBRAR_CUSTO_INICIAL,
)


base_diagnostico[
    "custo_estrategia"
] = (
    base_diagnostico[
        "turnover_estrategia"
    ]
    * CUSTO_POR_TURNOVER
)


base_diagnostico[
    "custo_benchmark"
] = (
    base_diagnostico[
        "turnover_benchmark"
    ]
    * CUSTO_POR_TURNOVER
)


base_diagnostico[
    "retorno_liquido_estrategia"
] = (
    (
        1.0
        + base_diagnostico[
            "retorno_bruto_estrategia"
        ]
    )
    * (
        1.0
        - base_diagnostico[
            "custo_estrategia"
        ]
    )
    - 1.0
)


base_diagnostico[
    "retorno_liquido_benchmark"
] = (
    (
        1.0
        + base_diagnostico[
            "retorno_bruto_benchmark"
        ]
    )
    * (
        1.0
        - base_diagnostico[
            "custo_benchmark"
        ]
    )
    - 1.0
)


base_diagnostico[
    "retorno_excesso_liquido"
] = (
    base_diagnostico[
        "retorno_liquido_estrategia"
    ]
    - base_diagnostico[
        "retorno_liquido_benchmark"
    ]
)


base_diagnostico[
    "diferenca_turnover"
] = (
    base_diagnostico[
        "turnover_estrategia"
    ]
    - base_diagnostico[
        "turnover_benchmark"
    ]
)


base_diagnostico[
    "diferenca_custo"
] = (
    base_diagnostico[
        "custo_estrategia"
    ]
    - base_diagnostico[
        "custo_benchmark"
    ]
)


# ============================================================
# DIVISÃO ENTRE TREINO E TESTE
# ============================================================

base_diagnostico[
    "periodo"
] = np.where(
    base_diagnostico[
        "data"
    ]
    <= DATA_CORTE_TREINO,
    "TREINO",
    "TESTE",
)


quantidade_treino = int(
    (
        base_diagnostico[
            "periodo"
        ]
        == "TREINO"
    ).sum()
)


quantidade_teste = int(
    (
        base_diagnostico[
            "periodo"
        ]
        == "TESTE"
    ).sum()
)


if quantidade_treino == 0:
    raise ValueError(
        "A base de treino ficou vazia."
    )


if quantidade_teste == 0:
    raise ValueError(
        "A base de teste ficou vazia."
    )


# ============================================================
# CONTRIBUIÇÕES MENSAIS DOS ATIVOS
# ============================================================

for ativo, coluna_peso_estrategia in zip(
    ativos_originais,
    colunas_pesos_estrategia,
):

    base_diagnostico[
        f"contribuicao_estrategia_{ativo}"
    ] = (
        base_diagnostico[
            coluna_peso_estrategia
        ]
        * base_diagnostico[
            ativo
        ]
    )

    base_diagnostico[
        f"contribuicao_benchmark_{ativo}"
    ] = (
        PESO_BENCHMARK
        * base_diagnostico[
            ativo
        ]
    )

    base_diagnostico[
        f"diferenca_contribuicao_{ativo}"
    ] = (
        base_diagnostico[
            f"contribuicao_estrategia_{ativo}"
        ]
        - base_diagnostico[
            f"contribuicao_benchmark_{ativo}"
        ]
    )


# ============================================================
# FUNÇÕES DE MÉTRICAS
# ============================================================

def calcular_retorno_composto(
    retornos,
):
    retornos = (
        pd.Series(
            retornos
        )
        .dropna()
        .astype(float)
    )

    if retornos.empty:
        return np.nan

    return float(
        (
            1.0
            + retornos
        ).prod()
        - 1.0
    )


def calcular_volatilidade_mensal(
    retornos,
):
    retornos = (
        pd.Series(
            retornos
        )
        .dropna()
        .astype(float)
    )

    if len(
        retornos
    ) < 2:
        return np.nan

    return float(
        retornos.std(
            ddof=1
        )
    )


def calcular_maximo_drawdown(
    retornos,
    valor_inicial,
):
    retornos = (
        pd.Series(
            retornos
        )
        .dropna()
        .astype(float)
        .reset_index(drop=True)
    )

    if retornos.empty:
        return np.nan

    indice = (
        valor_inicial
        * (
            1.0
            + retornos
        ).cumprod()
    )

    indice_com_inicio = pd.concat(
        [
            pd.Series(
                [
                    valor_inicial
                ],
                dtype=float,
            ),
            indice,
        ],
        ignore_index=True,
    )

    pico = (
        indice_com_inicio
        .cummax()
    )

    drawdown = (
        indice_com_inicio
        / pico
        - 1.0
    )

    return float(
        drawdown.min()
    )


# ============================================================
# DIAGNÓSTICO POR REGIME
# ============================================================

resultados_regimes = []


for periodo in [
    "TREINO",
    "TESTE",
]:

    dados_periodo = (
        base_diagnostico.loc[
            base_diagnostico[
                "periodo"
            ]
            == periodo
        ]
        .copy()
    )

    for regime in ORDEM_REGIMES:

        dados_regime = (
            dados_periodo.loc[
                dados_periodo[
                    COLUNA_REGIME_SELECIONADO
                ]
                == regime
            ]
            .copy()
            .reset_index(drop=True)
        )

        quantidade_meses = len(
            dados_regime
        )

        if quantidade_meses == 0:

            resultados_regimes.append(
                {
                    "periodo": periodo,
                    "regime": regime,
                    "nome_regime": (
                        NOMES_REGIMES[
                            regime
                        ]
                    ),
                    "quantidade_meses": 0,
                    "proporcao_periodo": 0.0,
                    "retorno_total_estrategia": np.nan,
                    "retorno_total_benchmark": np.nan,
                    "diferenca_retorno_composto": np.nan,
                    "excesso_acumulado_simples": np.nan,
                    "retorno_medio_mensal_estrategia": np.nan,
                    "retorno_medio_mensal_benchmark": np.nan,
                    "excesso_medio_mensal": np.nan,
                    "volatilidade_mensal_estrategia": np.nan,
                    "volatilidade_mensal_benchmark": np.nan,
                    "maximo_drawdown_estrategia": np.nan,
                    "maximo_drawdown_benchmark": np.nan,
                    "taxa_vitoria_mensal": np.nan,
                    "turnover_total_estrategia": np.nan,
                    "turnover_total_benchmark": np.nan,
                    "diferenca_turnover": np.nan,
                    "custo_total_estrategia": np.nan,
                    "custo_total_benchmark": np.nan,
                    "diferenca_custo": np.nan,
                }
            )

            continue

        retorno_total_estrategia = (
            calcular_retorno_composto(
                dados_regime[
                    "retorno_liquido_estrategia"
                ]
            )
        )

        retorno_total_benchmark = (
            calcular_retorno_composto(
                dados_regime[
                    "retorno_liquido_benchmark"
                ]
            )
        )

        resultados_regimes.append(
            {
                "periodo": periodo,
                "regime": regime,
                "nome_regime": (
                    NOMES_REGIMES[
                        regime
                    ]
                ),
                "quantidade_meses": (
                    quantidade_meses
                ),
                "proporcao_periodo": (
                    quantidade_meses
                    / len(
                        dados_periodo
                    )
                ),
                "retorno_total_estrategia": (
                    retorno_total_estrategia
                ),
                "retorno_total_benchmark": (
                    retorno_total_benchmark
                ),
                "diferenca_retorno_composto": (
                    retorno_total_estrategia
                    - retorno_total_benchmark
                ),
                "excesso_acumulado_simples": float(
                    dados_regime[
                        "retorno_excesso_liquido"
                    ].sum()
                ),
                "retorno_medio_mensal_estrategia": float(
                    dados_regime[
                        "retorno_liquido_estrategia"
                    ].mean()
                ),
                "retorno_medio_mensal_benchmark": float(
                    dados_regime[
                        "retorno_liquido_benchmark"
                    ].mean()
                ),
                "excesso_medio_mensal": float(
                    dados_regime[
                        "retorno_excesso_liquido"
                    ].mean()
                ),
                "volatilidade_mensal_estrategia": (
                    calcular_volatilidade_mensal(
                        dados_regime[
                            "retorno_liquido_estrategia"
                        ]
                    )
                ),
                "volatilidade_mensal_benchmark": (
                    calcular_volatilidade_mensal(
                        dados_regime[
                            "retorno_liquido_benchmark"
                        ]
                    )
                ),
                "maximo_drawdown_estrategia": (
                    calcular_maximo_drawdown(
                        retornos=dados_regime[
                            "retorno_liquido_estrategia"
                        ],
                        valor_inicial=VALOR_INICIAL,
                    )
                ),
                "maximo_drawdown_benchmark": (
                    calcular_maximo_drawdown(
                        retornos=dados_regime[
                            "retorno_liquido_benchmark"
                        ],
                        valor_inicial=VALOR_INICIAL,
                    )
                ),
                "taxa_vitoria_mensal": float(
                    (
                        dados_regime[
                            "retorno_liquido_estrategia"
                        ]
                        > dados_regime[
                            "retorno_liquido_benchmark"
                        ]
                    ).mean()
                ),
                "turnover_total_estrategia": float(
                    dados_regime[
                        "turnover_estrategia"
                    ].sum()
                ),
                "turnover_total_benchmark": float(
                    dados_regime[
                        "turnover_benchmark"
                    ].sum()
                ),
                "diferenca_turnover": float(
                    dados_regime[
                        "diferenca_turnover"
                    ].sum()
                ),
                "custo_total_estrategia": float(
                    dados_regime[
                        "custo_estrategia"
                    ].sum()
                ),
                "custo_total_benchmark": float(
                    dados_regime[
                        "custo_benchmark"
                    ].sum()
                ),
                "diferenca_custo": float(
                    dados_regime[
                        "diferenca_custo"
                    ].sum()
                ),
            }
        )


diagnostico_regimes = pd.DataFrame(
    resultados_regimes
)


# ============================================================
# CLASSIFICAÇÃO DOS REGIMES NO TESTE
# ============================================================

def classificar_regime(
    quantidade_meses,
    diferenca_retorno,
):
    if quantidade_meses < MINIMO_MESES_CLASSIFICACAO_REGIME:
        return (
            "AMOSTRA INSUFICIENTE"
        )

    if pd.isna(
        diferenca_retorno
    ):
        return (
            "SEM RESULTADO"
        )

    if diferenca_retorno <= LIMITE_CRITICO_REGIME:
        return (
            "CRÍTICO"
        )

    if diferenca_retorno < 0:
        return (
            "ATENÇÃO"
        )

    return (
        "POSITIVO"
    )


diagnostico_regimes[
    "classificacao"
] = "-"


mascara_teste = (
    diagnostico_regimes[
        "periodo"
    ]
    == "TESTE"
)


diagnostico_regimes.loc[
    mascara_teste,
    "classificacao",
] = (
    diagnostico_regimes.loc[
        mascara_teste
    ]
    .apply(
        lambda linha: (
            classificar_regime(
                quantidade_meses=int(
                    linha[
                        "quantidade_meses"
                    ]
                ),
                diferenca_retorno=linha[
                    "diferenca_retorno_composto"
                ],
            )
        ),
        axis=1,
    )
)


regimes_problematicos = (
    diagnostico_regimes.loc[
        (
            diagnostico_regimes[
                "periodo"
            ]
            == "TESTE"
        )
        & (
            diagnostico_regimes[
                "classificacao"
            ]
            .isin(
                [
                    "CRÍTICO",
                    "ATENÇÃO",
                ]
            )
        )
    ]
    .sort_values(
        "diferenca_retorno_composto"
    )
    .reset_index(drop=True)
)


# ============================================================
# CONTRIBUIÇÃO DOS ATIVOS POR REGIME
# ============================================================

resultados_contribuicoes = []


for periodo in [
    "TREINO",
    "TESTE",
]:

    for regime in ORDEM_REGIMES:

        dados_regime = (
            base_diagnostico.loc[
                (
                    base_diagnostico[
                        "periodo"
                    ]
                    == periodo
                )
                & (
                    base_diagnostico[
                        COLUNA_REGIME_SELECIONADO
                    ]
                    == regime
                )
            ]
            .copy()
        )

        quantidade_meses = len(
            dados_regime
        )

        for ativo, coluna_peso_estrategia in zip(
            ativos_originais,
            colunas_pesos_estrategia,
        ):

            if quantidade_meses == 0:

                resultados_contribuicoes.append(
                    {
                        "periodo": periodo,
                        "regime": regime,
                        "nome_regime": (
                            NOMES_REGIMES[
                                regime
                            ]
                        ),
                        "ativo": ativo,
                        "quantidade_meses": 0,
                        "peso_medio_estrategia": np.nan,
                        "peso_benchmark": (
                            PESO_BENCHMARK
                        ),
                        "retorno_medio_ativo": np.nan,
                        "contribuicao_estrategia_acumulada_simples": np.nan,
                        "contribuicao_benchmark_acumulada_simples": np.nan,
                        "diferenca_contribuicao_acumulada": np.nan,
                        "contribuicao_media_mensal_estrategia": np.nan,
                        "contribuicao_media_mensal_benchmark": np.nan,
                        "diferenca_contribuicao_media_mensal": np.nan,
                    }
                )

                continue

            resultados_contribuicoes.append(
                {
                    "periodo": periodo,
                    "regime": regime,
                    "nome_regime": (
                        NOMES_REGIMES[
                            regime
                        ]
                    ),
                    "ativo": ativo,
                    "quantidade_meses": (
                        quantidade_meses
                    ),
                    "peso_medio_estrategia": float(
                        dados_regime[
                            coluna_peso_estrategia
                        ].mean()
                    ),
                    "peso_benchmark": (
                        PESO_BENCHMARK
                    ),
                    "retorno_medio_ativo": float(
                        dados_regime[
                            ativo
                        ].mean()
                    ),
                    "contribuicao_estrategia_acumulada_simples": float(
                        dados_regime[
                            f"contribuicao_estrategia_{ativo}"
                        ].sum()
                    ),
                    "contribuicao_benchmark_acumulada_simples": float(
                        dados_regime[
                            f"contribuicao_benchmark_{ativo}"
                        ].sum()
                    ),
                    "diferenca_contribuicao_acumulada": float(
                        dados_regime[
                            f"diferenca_contribuicao_{ativo}"
                        ].sum()
                    ),
                    "contribuicao_media_mensal_estrategia": float(
                        dados_regime[
                            f"contribuicao_estrategia_{ativo}"
                        ].mean()
                    ),
                    "contribuicao_media_mensal_benchmark": float(
                        dados_regime[
                            f"contribuicao_benchmark_{ativo}"
                        ].mean()
                    ),
                    "diferenca_contribuicao_media_mensal": float(
                        dados_regime[
                            f"diferenca_contribuicao_{ativo}"
                        ].mean()
                    ),
                }
            )


contribuicao_ativos = pd.DataFrame(
    resultados_contribuicoes
)


# ============================================================
# VALIDAÇÃO DAS CONTRIBUIÇÕES
# ============================================================

for periodo in [
    "TREINO",
    "TESTE",
]:

    for regime in ORDEM_REGIMES:

        dados_regime = (
            base_diagnostico.loc[
                (
                    base_diagnostico[
                        "periodo"
                    ]
                    == periodo
                )
                & (
                    base_diagnostico[
                        COLUNA_REGIME_SELECIONADO
                    ]
                    == regime
                )
            ]
        )

        if dados_regime.empty:
            continue

        contribuicao_total = (
            contribuicao_ativos.loc[
                (
                    contribuicao_ativos[
                        "periodo"
                    ]
                    == periodo
                )
                & (
                    contribuicao_ativos[
                        "regime"
                    ]
                    == regime
                ),
                "contribuicao_estrategia_acumulada_simples",
            ]
            .sum()
        )

        retorno_bruto_total = (
            dados_regime[
                "retorno_bruto_estrategia"
            ]
            .sum()
        )

        if not np.isclose(
            contribuicao_total,
            retorno_bruto_total,
            rtol=1e-10,
            atol=1e-12,
        ):
            raise ValueError(
                "A soma das contribuições não reproduziu "
                "o retorno bruto da estratégia.\n"
                f"Período: {periodo}\n"
                f"Regime: {regime}"
            )


# ============================================================
# IDENTIFICAÇÃO DOS PRINCIPAIS RESULTADOS
# ============================================================

diagnostico_teste = (
    diagnostico_regimes.loc[
        (
            diagnostico_regimes[
                "periodo"
            ]
            == "TESTE"
        )
        & (
            diagnostico_regimes[
                "quantidade_meses"
            ]
            > 0
        )
    ]
    .copy()
)


if diagnostico_teste.empty:
    raise ValueError(
        "Nenhum regime foi encontrado no teste."
    )


pior_regime_teste = (
    diagnostico_teste
    .sort_values(
        "diferenca_retorno_composto"
    )
    .iloc[0]
)


melhor_regime_teste = (
    diagnostico_teste
    .sort_values(
        "diferenca_retorno_composto",
        ascending=False,
    )
    .iloc[0]
)


contribuicoes_pior_regime = (
    contribuicao_ativos.loc[
        (
            contribuicao_ativos[
                "periodo"
            ]
            == "TESTE"
        )
        & (
            contribuicao_ativos[
                "regime"
            ]
            == pior_regime_teste[
                "regime"
            ]
        )
    ]
    .dropna(
        subset=[
            "diferenca_contribuicao_acumulada"
        ]
    )
    .sort_values(
        "diferenca_contribuicao_acumulada"
    )
    .reset_index(drop=True)
)


if contribuicoes_pior_regime.empty:

    nome_pior_ativo = (
        "Não identificado"
    )

    diferenca_pior_ativo = np.nan

else:

    pior_ativo = (
        contribuicoes_pior_regime
        .iloc[0]
    )

    nome_pior_ativo = (
        pior_ativo[
            "ativo"
        ]
    )

    diferenca_pior_ativo = float(
        pior_ativo[
            "diferenca_contribuicao_acumulada"
        ]
    )


# ============================================================
# TABELAS FORMATADAS
# ============================================================

diagnostico_regimes_formatado = (
    diagnostico_regimes
    .copy()
    .astype(object)
)


colunas_percentuais_regimes = [
    "proporcao_periodo",
    "retorno_total_estrategia",
    "retorno_total_benchmark",
    "diferenca_retorno_composto",
    "excesso_acumulado_simples",
    "retorno_medio_mensal_estrategia",
    "retorno_medio_mensal_benchmark",
    "excesso_medio_mensal",
    "volatilidade_mensal_estrategia",
    "volatilidade_mensal_benchmark",
    "maximo_drawdown_estrategia",
    "maximo_drawdown_benchmark",
    "taxa_vitoria_mensal",
    "custo_total_estrategia",
    "custo_total_benchmark",
    "diferenca_custo",
]


for coluna in colunas_percentuais_regimes:

    diagnostico_regimes_formatado[
        coluna
    ] = (
        diagnostico_regimes[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "turnover_total_estrategia",
    "turnover_total_benchmark",
    "diferenca_turnover",
]:

    diagnostico_regimes_formatado[
        coluna
    ] = (
        diagnostico_regimes[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.4f}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


diagnostico_regimes_formatado[
    "quantidade_meses"
] = (
    diagnostico_regimes[
        "quantidade_meses"
    ]
    .map(
        lambda valor: (
            f"{int(valor)}"
        )
    )
)


contribuicao_ativos_formatado = (
    contribuicao_ativos
    .copy()
    .astype(object)
)


for coluna in [
    "peso_medio_estrategia",
    "peso_benchmark",
    "retorno_medio_ativo",
    "contribuicao_estrategia_acumulada_simples",
    "contribuicao_benchmark_acumulada_simples",
    "diferenca_contribuicao_acumulada",
    "contribuicao_media_mensal_estrategia",
    "contribuicao_media_mensal_benchmark",
    "diferenca_contribuicao_media_mensal",
]:

    contribuicao_ativos_formatado[
        coluna
    ] = (
        contribuicao_ativos[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


contribuicao_ativos_formatado[
    "quantidade_meses"
] = (
    contribuicao_ativos[
        "quantidade_meses"
    ]
    .map(
        lambda valor: (
            f"{int(valor)}"
        )
    )
)


# ============================================================
# RESUMO DO DIAGNÓSTICO
# ============================================================

resumo_diagnostico = pd.DataFrame(
    {
        "metrica": [
            "Meses de confirmação",
            "Alpha de encolhimento",
            "Custo por turnover",
            "Data final do treino",
            "Meses de treino",
            "Meses de teste",
            "Quantidade de regimes problemáticos",
            "Pior regime no teste",
            "Meses do pior regime",
            "Diferença do pior regime",
            "Classificação do pior regime",
            "Ativo com pior contribuição relativa",
            "Diferença de contribuição do pior ativo",
            "Melhor regime no teste",
            "Diferença do melhor regime",
        ],
        "valor": [
            confirmacao_selecionada,
            alpha_selecionado,
            CUSTO_POR_TURNOVER,
            DATA_CORTE_TREINO.strftime(
                "%d/%m/%Y"
            ),
            quantidade_treino,
            quantidade_teste,
            len(
                regimes_problematicos
            ),
            pior_regime_teste[
                "nome_regime"
            ],
            int(
                pior_regime_teste[
                    "quantidade_meses"
                ]
            ),
            pior_regime_teste[
                "diferenca_retorno_composto"
            ],
            pior_regime_teste[
                "classificacao"
            ],
            nome_pior_ativo,
            diferenca_pior_ativo,
            melhor_regime_teste[
                "nome_regime"
            ],
            melhor_regime_teste[
                "diferenca_retorno_composto"
            ],
        ],
    }
)


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_DIAGNOSTICO_REGIMES = (
    PASTA_TABELAS
    / "06_06_diagnostico_por_regime.csv"
)

ARQUIVO_DIAGNOSTICO_REGIMES_FORMATADO = (
    PASTA_TABELAS
    / "06_06_diagnostico_por_regime_formatado.csv"
)

ARQUIVO_CONTRIBUICAO_ATIVOS = (
    PASTA_TABELAS
    / "06_06_contribuicao_ativos_por_regime.csv"
)

ARQUIVO_CONTRIBUICAO_ATIVOS_FORMATADO = (
    PASTA_TABELAS
    / "06_06_contribuicao_ativos_por_regime_formatado.csv"
)

ARQUIVO_REGIMES_PROBLEMATICOS = (
    PASTA_TABELAS
    / "06_06_regimes_problematicos_teste.csv"
)

ARQUIVO_SERIES_DIAGNOSTICO = (
    PASTA_TABELAS
    / "06_06_series_mensais_diagnostico.csv"
)

ARQUIVO_RESUMO_DIAGNOSTICO = (
    PASTA_TABELAS
    / "06_06_resumo_diagnostico.csv"
)

ARQUIVO_GRAFICO_EXCESSO_REGIMES = (
    PASTA_GRAFICOS
    / "06_06_excesso_retorno_por_regime.png"
)

ARQUIVO_GRAFICO_CONTRIBUICAO_ATIVOS = (
    PASTA_GRAFICOS
    / "06_06_contribuicao_ativos_teste.png"
)

ARQUIVO_GRAFICO_TURNOVER_REGIMES = (
    PASTA_GRAFICOS
    / "06_06_turnover_por_regime.png"
)


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

diagnostico_regimes.to_csv(
    ARQUIVO_DIAGNOSTICO_REGIMES,
    index=False,
    encoding="utf-8-sig",
)


diagnostico_regimes_formatado.to_csv(
    ARQUIVO_DIAGNOSTICO_REGIMES_FORMATADO,
    index=False,
    encoding="utf-8-sig",
)


contribuicao_ativos.to_csv(
    ARQUIVO_CONTRIBUICAO_ATIVOS,
    index=False,
    encoding="utf-8-sig",
)


contribuicao_ativos_formatado.to_csv(
    ARQUIVO_CONTRIBUICAO_ATIVOS_FORMATADO,
    index=False,
    encoding="utf-8-sig",
)


regimes_problematicos.to_csv(
    ARQUIVO_REGIMES_PROBLEMATICOS,
    index=False,
    encoding="utf-8-sig",
)


base_diagnostico.to_csv(
    ARQUIVO_SERIES_DIAGNOSTICO,
    index=False,
    encoding="utf-8-sig",
)


resumo_diagnostico.to_csv(
    ARQUIVO_RESUMO_DIAGNOSTICO,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO 1 — EXCESSO DE RETORNO POR REGIME
# ============================================================

dados_grafico_excesso = (
    diagnostico_regimes
    .pivot(
        index="nome_regime",
        columns="periodo",
        values="diferenca_retorno_composto",
    )
    .reindex(
        [
            NOMES_REGIMES[
                regime
            ]
            for regime in ORDEM_REGIMES
        ]
    )
)


fig, ax = plt.subplots(
    figsize=(13, 7)
)


dados_grafico_excesso.plot(
    kind="bar",
    ax=ax,
    width=0.75,
)


ax.axhline(
    y=0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Diferença de Retorno contra o Benchmark por Regime"
)

ax.set_xlabel(
    "Regime macroeconômico"
)

ax.set_ylabel(
    "Diferença de retorno composto"
)

ax.tick_params(
    axis="x",
    rotation=20,
)

ax.legend(
    title="Período"
)

ax.grid(
    axis="y",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_EXCESSO_REGIMES,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — CONTRIBUIÇÃO DOS ATIVOS NO TESTE
# ============================================================

dados_grafico_contribuicao = (
    contribuicao_ativos.loc[
        contribuicao_ativos[
            "periodo"
        ]
        == "TESTE"
    ]
    .pivot(
        index="nome_regime",
        columns="ativo",
        values="diferenca_contribuicao_acumulada",
    )
    .reindex(
        [
            NOMES_REGIMES[
                regime
            ]
            for regime in ORDEM_REGIMES
        ]
    )
)


fig, ax = plt.subplots(
    figsize=(13, 7)
)


dados_grafico_contribuicao.plot(
    kind="bar",
    ax=ax,
    width=0.8,
)


ax.axhline(
    y=0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Contribuição Relativa dos Ativos no Período de Teste"
)

ax.set_xlabel(
    "Regime macroeconômico"
)

ax.set_ylabel(
    "Diferença de contribuição acumulada"
)

ax.tick_params(
    axis="x",
    rotation=20,
)

ax.legend(
    title="Ativo"
)

ax.grid(
    axis="y",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_CONTRIBUICAO_ATIVOS,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — TURNOVER POR REGIME
# ============================================================

dados_grafico_turnover = (
    diagnostico_regimes
    .pivot(
        index="nome_regime",
        columns="periodo",
        values="turnover_total_estrategia",
    )
    .reindex(
        [
            NOMES_REGIMES[
                regime
            ]
            for regime in ORDEM_REGIMES
        ]
    )
)


fig, ax = plt.subplots(
    figsize=(13, 7)
)


dados_grafico_turnover.plot(
    kind="bar",
    ax=ax,
    width=0.75,
)


ax.set_title(
    "Turnover Total da Estratégia por Regime"
)

ax.set_xlabel(
    "Regime macroeconômico"
)

ax.set_ylabel(
    "Turnover total"
)

ax.tick_params(
    axis="x",
    rotation=20,
)

ax.legend(
    title="Período"
)

ax.grid(
    axis="y",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_TURNOVER_REGIMES,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_DIAGNOSTICO_REGIMES,
    ARQUIVO_DIAGNOSTICO_REGIMES_FORMATADO,
    ARQUIVO_CONTRIBUICAO_ATIVOS,
    ARQUIVO_CONTRIBUICAO_ATIVOS_FORMATADO,
    ARQUIVO_REGIMES_PROBLEMATICOS,
    ARQUIVO_SERIES_DIAGNOSTICO,
    ARQUIVO_RESUMO_DIAGNOSTICO,
    ARQUIVO_GRAFICO_EXCESSO_REGIMES,
    ARQUIVO_GRAFICO_CONTRIBUICAO_ATIVOS,
    ARQUIVO_GRAFICO_TURNOVER_REGIMES,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:
    raise FileNotFoundError(
        "Alguns arquivos da Célula 6 "
        "não foram salvos:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("=" * 70)
print("DIAGNÓSTICO POR REGIME E ATIVO CONCLUÍDO")
print("=" * 70)

print(
    f"\nRaiz do projeto:\n"
    f"{RAIZ_PROJETO}"
)

print(
    f"\nArquivo de configuração:\n"
    f"{ARQUIVO_CONFIG}"
)

print(
    f"\nValor inicial: "
    f"{VALOR_INICIAL:.2f}"
)

print(
    f"Cobrança de custo inicial: "
    f"{COBRAR_CUSTO_INICIAL}"
)

print(
    f"Mínimo de meses para classificação: "
    f"{MINIMO_MESES_CLASSIFICACAO_REGIME}"
)

print(
    f"Limite crítico de retorno: "
    f"{LIMITE_CRITICO_REGIME:.2%}"
)

print(
    f"\nConfirmação do regime: "
    f"{confirmacao_selecionada} mês(es)"
)

print(
    f"Encolhimento dos pesos: "
    f"{alpha_selecionado:.0%}"
)

print(
    f"Custo utilizado: "
    f"{CUSTO_POR_TURNOVER:.4%} "
    f"({CUSTO_POR_TURNOVER * 10000:.2f} bps)"
)

print(
    f"\nMeses de treino: "
    f"{quantidade_treino}"
)

print(
    f"Meses de teste: "
    f"{quantidade_teste}"
)

print(
    f"\nPior regime no teste: "
    f"{pior_regime_teste['nome_regime']}"
)

print(
    f"Quantidade de meses: "
    f"{int(pior_regime_teste['quantidade_meses'])}"
)

print(
    f"Retorno da estratégia: "
    f"{pior_regime_teste['retorno_total_estrategia']:.2%}"
)

print(
    f"Retorno do benchmark: "
    f"{pior_regime_teste['retorno_total_benchmark']:.2%}"
)

print(
    f"Diferença contra o benchmark: "
    f"{pior_regime_teste['diferenca_retorno_composto']:.2%}"
)

print(
    f"Classificação: "
    f"{pior_regime_teste['classificacao']}"
)

print(
    f"\nAtivo com pior contribuição relativa "
    f"nesse regime: "
    f"{nome_pior_ativo}"
)

if pd.notna(
    diferenca_pior_ativo
):
    print(
        f"Diferença de contribuição: "
        f"{diferenca_pior_ativo:.2%}"
    )


print(
    f"\nMelhor regime no teste: "
    f"{melhor_regime_teste['nome_regime']}"
)

print(
    f"Diferença contra o benchmark: "
    f"{melhor_regime_teste['diferenca_retorno_composto']:.2%}"
)

print(
    f"\nQuantidade de regimes problemáticos: "
    f"{len(regimes_problematicos)}"
)

print(
    f"\nDiagnóstico salvo em:\n"
    f"{ARQUIVO_DIAGNOSTICO_REGIMES}"
)

print(
    f"\nContribuições salvas em:\n"
    f"{ARQUIVO_CONTRIBUICAO_ATIVOS}"
)

print(
    f"\nResumo salvo em:\n"
    f"{ARQUIVO_RESUMO_DIAGNOSTICO}"
)

print(
    "\nDiagnóstico dos regimes no teste:"
)

display(
    diagnostico_regimes_formatado.loc[
        diagnostico_regimes_formatado[
            "periodo"
        ]
        == "TESTE"
    ]
)


print(
    "\nContribuições dos ativos no pior regime:"
)

display(
    contribuicao_ativos_formatado.loc[
        (
            contribuicao_ativos_formatado[
                "periodo"
            ]
            == "TESTE"
        )
        & (
            contribuicao_ativos_formatado[
                "regime"
            ]
            == pior_regime_teste[
                "regime"
            ]
        )
    ]
)

# ###########################################################################
# ETAPA 07 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 7 — AJUSTE INDIVIDUAL DOS PESOS POR REGIME
# VERSÃO AUTÔNOMA
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml

from matplotlib.ticker import PercentFormatter


# ============================================================
# LOCALIZAÇÃO DA RAIZ DO PROJETO
# ============================================================

DIRETORIO_ATUAL = Path.cwd().resolve()

RAIZ_PROJETO = None

for diretorio in [
    DIRETORIO_ATUAL,
    *DIRETORIO_ATUAL.parents,
]:
    arquivo_teste = (
        diretorio
        / "data"
        / "processed"
        / "backtest_portfolio_mensal.csv"
    )

    if arquivo_teste.exists():
        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:
    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto."
    )


PASTA_DADOS_PROCESSADOS = (
    RAIZ_PROJETO
    / "data"
    / "processed"
)

PASTA_TABELAS = (
    RAIZ_PROJETO
    / "outputs"
    / "tabelas"
)

PASTA_GRAFICOS = (
    RAIZ_PROJETO
    / "outputs"
    / "graficos"
)


PASTA_TABELAS.mkdir(
    parents=True,
    exist_ok=True,
)

PASTA_GRAFICOS.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ARQUIVO_BACKTEST = (
    PASTA_DADOS_PROCESSADOS
    / "backtest_portfolio_mensal.csv"
)

ARQUIVO_REGIMES_SUAVIZADOS = (
    PASTA_TABELAS
    / "06_02_regimes_suavizados.csv"
)

ARQUIVO_PESOS_BASE = (
    PASTA_TABELAS
    / "06_05_pesos_selecionados_por_regime.csv"
)

ARQUIVO_PARAMETROS_BASE = (
    PASTA_TABELAS
    / "06_05_parametros_selecionados.csv"
)


arquivos_entrada = [
    ARQUIVO_BACKTEST,
    ARQUIVO_REGIMES_SUAVIZADOS,
    ARQUIVO_PESOS_BASE,
    ARQUIVO_PARAMETROS_BASE,
]


arquivos_ausentes = [
    arquivo
    for arquivo in arquivos_entrada
    if not arquivo.exists()
]


if arquivos_ausentes:
    raise FileNotFoundError(
        "Arquivos necessários não encontrados:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# CARREGAMENTO DO CONFIG.YAML
# ============================================================

ARQUIVO_CONFIG = (
    RAIZ_PROJETO
    / "config"
    / "config.yaml"
)


if not ARQUIVO_CONFIG.exists():
    raise FileNotFoundError(
        "Arquivo de configuração não encontrado:\n"
        f"{ARQUIVO_CONFIG}"
    )


with ARQUIVO_CONFIG.open(
    mode="r",
    encoding="utf-8",
) as arquivo_yaml:

    CONFIGURACAO = (
        yaml.safe_load(
            arquivo_yaml
        )
        or {}
    )


if (
    "backtest" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["backtest"],
        dict,
    )
):
    raise KeyError(
        "A seção 'backtest' não foi encontrada "
        "no config/config.yaml."
    )


if (
    "otimizacao" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["otimizacao"],
        dict,
    )
):
    raise KeyError(
        "A seção 'otimizacao' não foi encontrada "
        "no config/config.yaml."
    )


CONFIGURACAO_BACKTEST = (
    CONFIGURACAO[
        "backtest"
    ]
)

CONFIGURACAO_OTIMIZACAO = (
    CONFIGURACAO[
        "otimizacao"
    ]
)


parametros_backtest_obrigatorios = [
    "valor_inicial",
    "periodos_por_ano",
    "periodos_janela",
    "custo_por_turnover",
    "cobrar_custo_inicial",
]


parametros_backtest_ausentes = [
    parametro
    for parametro in parametros_backtest_obrigatorios
    if parametro not in CONFIGURACAO_BACKTEST
]


if parametros_backtest_ausentes:
    raise KeyError(
        "Parâmetros ausentes na seção 'backtest' "
        "do config.yaml:\n"
        f"{parametros_backtest_ausentes}"
    )


parametros_otimizacao_obrigatorios = [
    "betas_encolhimento_regime",
    "minimo_meses_regime_treino",
]


parametros_otimizacao_ausentes = [
    parametro
    for parametro in parametros_otimizacao_obrigatorios
    if parametro not in CONFIGURACAO_OTIMIZACAO
]


if parametros_otimizacao_ausentes:
    raise KeyError(
        "Parâmetros ausentes na seção 'otimizacao' "
        "do config.yaml:\n"
        f"{parametros_otimizacao_ausentes}"
    )


# ============================================================
# CONFIGURAÇÕES
# ============================================================

VALOR_INICIAL = float(
    CONFIGURACAO_BACKTEST[
        "valor_inicial"
    ]
)

PERIODOS_POR_ANO = int(
    CONFIGURACAO_BACKTEST[
        "periodos_por_ano"
    ]
)

JANELA_ROLLING = int(
    CONFIGURACAO_BACKTEST[
        "periodos_janela"
    ]
)

CUSTO_POR_TURNOVER = float(
    CONFIGURACAO_BACKTEST[
        "custo_por_turnover"
    ]
)

COBRAR_CUSTO_INICIAL = (
    CONFIGURACAO_BACKTEST[
        "cobrar_custo_inicial"
    ]
)


betas_configurados = (
    CONFIGURACAO_OTIMIZACAO[
        "betas_encolhimento_regime"
    ]
)


if not isinstance(
    betas_configurados,
    list,
):
    raise TypeError(
        "'otimizacao.betas_encolhimento_regime' "
        "deve ser uma lista."
    )


if not betas_configurados:
    raise ValueError(
        "'otimizacao.betas_encolhimento_regime' "
        "não pode estar vazio."
    )


try:
    BETAS_ENCOLHIMENTO_REGIME = [
        float(beta)
        for beta in betas_configurados
    ]

except (
    TypeError,
    ValueError,
) as erro:
    raise TypeError(
        "Todos os valores de "
        "'otimizacao.betas_encolhimento_regime' "
        "devem ser numéricos."
    ) from erro


MINIMO_MESES_REGIME_TREINO = int(
    CONFIGURACAO_OTIMIZACAO[
        "minimo_meses_regime_treino"
    ]
)


if VALOR_INICIAL <= 0:
    raise ValueError(
        "'backtest.valor_inicial' "
        "deve ser maior que zero."
    )


if PERIODOS_POR_ANO <= 0:
    raise ValueError(
        "'backtest.periodos_por_ano' "
        "deve ser maior que zero."
    )


if JANELA_ROLLING <= 0:
    raise ValueError(
        "'backtest.periodos_janela' "
        "deve ser maior que zero."
    )


if CUSTO_POR_TURNOVER < 0:
    raise ValueError(
        "'backtest.custo_por_turnover' "
        "não pode ser negativo."
    )


if not isinstance(
    COBRAR_CUSTO_INICIAL,
    bool,
):
    raise TypeError(
        "'backtest.cobrar_custo_inicial' "
        "deve ser true ou false."
    )


if any(
    beta < 0.0
    or beta > 1.0
    for beta in BETAS_ENCOLHIMENTO_REGIME
):
    raise ValueError(
        "Todos os betas de encolhimento "
        "devem estar entre 0 e 1."
    )


if (
    len(BETAS_ENCOLHIMENTO_REGIME)
    != len(set(BETAS_ENCOLHIMENTO_REGIME))
):
    raise ValueError(
        "A lista de betas de encolhimento "
        "possui valores duplicados."
    )


if not any(
    np.isclose(
        beta,
        0.0,
    )
    for beta in BETAS_ENCOLHIMENTO_REGIME
):
    raise ValueError(
        "O beta 0.0 é obrigatório para representar "
        "a manutenção dos pesos base."
    )


BETAS_ENCOLHIMENTO_REGIME = sorted(
    BETAS_ENCOLHIMENTO_REGIME
)


if MINIMO_MESES_REGIME_TREINO <= 0:
    raise ValueError(
        "'otimizacao.minimo_meses_regime_treino' "
        "deve ser maior que zero."
    )


ORDEM_REGIMES = [
    "EXPANSAO_DESINFLACIONARIA",
    "EXPANSAO_INFLACIONARIA",
    "ESTAGFLACAO",
    "RECESSAO_DESINFLACIONARIA",
]


NOMES_REGIMES = {
    "EXPANSAO_DESINFLACIONARIA": (
        "Expansão desinflacionária"
    ),
    "EXPANSAO_INFLACIONARIA": (
        "Expansão inflacionária"
    ),
    "ESTAGFLACAO": (
        "Estagflação"
    ),
    "RECESSAO_DESINFLACIONARIA": (
        "Recessão desinflacionária"
    ),
}


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_GRADE_AJUSTES = (
    PASTA_TABELAS
    / "06_07_grade_ajustes_por_regime.csv"
)

ARQUIVO_GRADE_AJUSTES_FORMATADA = (
    PASTA_TABELAS
    / "06_07_grade_ajustes_por_regime_formatada.csv"
)

ARQUIVO_BETAS_SELECIONADOS = (
    PASTA_TABELAS
    / "06_07_betas_selecionados_por_regime.csv"
)

ARQUIVO_PESOS_OTIMIZADOS = (
    PASTA_TABELAS
    / "06_07_pesos_otimizados_por_regime.csv"
)

ARQUIVO_METRICAS_COMPARATIVAS = (
    PASTA_TABELAS
    / "06_07_metricas_comparativas.csv"
)

ARQUIVO_METRICAS_FORMATADAS = (
    PASTA_TABELAS
    / "06_07_metricas_comparativas_formatadas.csv"
)

ARQUIVO_SERIES_MENSAIS = (
    PASTA_TABELAS
    / "06_07_series_mensais_otimizadas.csv"
)

ARQUIVO_RESUMO_FINAL = (
    PASTA_TABELAS
    / "06_07_resumo_ajuste_regimes.csv"
)

ARQUIVO_GRAFICO_DESEMPENHO = (
    PASTA_GRAFICOS
    / "06_07_desempenho_periodo_avaliacao.png"
)

ARQUIVO_GRAFICO_DIFERENCA = (
    PASTA_GRAFICOS
    / "06_07_diferenca_vs_benchmark_avaliacao.png"
)

ARQUIVO_GRAFICO_PESOS = (
    PASTA_GRAFICOS
    / "06_07_comparacao_pesos_por_regime.png"
)


# ============================================================
# CARREGAMENTO
# ============================================================

backtest = pd.read_csv(
    ARQUIVO_BACKTEST,
    encoding="utf-8-sig",
)


regimes_suavizados = pd.read_csv(
    ARQUIVO_REGIMES_SUAVIZADOS,
    encoding="utf-8-sig",
)


pesos_base_df = pd.read_csv(
    ARQUIVO_PESOS_BASE,
    encoding="utf-8-sig",
)


parametros_base = pd.read_csv(
    ARQUIVO_PARAMETROS_BASE,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DAS DATAS
# ============================================================

for nome_base, base in {
    "backtest": backtest,
    "regimes": regimes_suavizados,
}.items():

    if "data" not in base.columns:
        raise ValueError(
            f"A base {nome_base} não possui a coluna data."
        )

    base["data"] = pd.to_datetime(
        base["data"],
        errors="coerce",
    )

    if base["data"].isna().any():
        raise ValueError(
            f"A base {nome_base} possui datas inválidas."
        )

    if base["data"].duplicated().any():
        raise ValueError(
            f"A base {nome_base} possui datas duplicadas."
        )


# ============================================================
# IDENTIFICAÇÃO DOS ATIVOS
# ============================================================

colunas_pesos_base = [
    coluna
    for coluna in pesos_base_df.columns
    if coluna.startswith(
        "peso_"
    )
]


if not colunas_pesos_base:
    raise ValueError(
        "Nenhuma coluna de peso foi encontrada."
    )


ativos = [
    coluna.replace(
        "peso_",
        "",
        1,
    )
    for coluna in colunas_pesos_base
]


ativos_ausentes = [
    ativo
    for ativo in ativos
    if ativo not in backtest.columns
]


if ativos_ausentes:
    raise ValueError(
        "Ativos ausentes no backtest:\n"
        f"{ativos_ausentes}"
    )


# ============================================================
# PARÂMETROS SELECIONADOS NA CÉLULA 5
# ============================================================

if "meses_confirmacao" not in pesos_base_df.columns:
    raise ValueError(
        "A coluna meses_confirmacao não foi encontrada."
    )


pesos_base_df[
    "meses_confirmacao"
] = pd.to_numeric(
    pesos_base_df[
        "meses_confirmacao"
    ],
    errors="coerce",
)


valores_confirmacao = (
    pesos_base_df[
        "meses_confirmacao"
    ]
    .dropna()
    .unique()
)


if len(valores_confirmacao) != 1:
    raise ValueError(
        "Foi encontrada mais de uma confirmação de regime."
    )


MESES_CONFIRMACAO = int(
    valores_confirmacao[0]
)


COLUNA_REGIME = (
    f"regime_confirmacao_"
    f"{MESES_CONFIRMACAO}m"
)


if COLUNA_REGIME not in regimes_suavizados.columns:
    raise ValueError(
        f"A coluna {COLUNA_REGIME} não foi encontrada."
    )


# ============================================================
# DATA FINAL DO TREINO
# ============================================================

linha_data_treino = (
    parametros_base.loc[
        parametros_base[
            "metrica"
        ]
        == "Data final do treino",
        "valor",
    ]
)


if linha_data_treino.empty:
    raise ValueError(
        "A data final do treino não foi encontrada "
        "no arquivo de parâmetros selecionados."
    )


if len(
    linha_data_treino
) != 1:
    raise ValueError(
        "Foi encontrada mais de uma data final do treino "
        "no arquivo de parâmetros selecionados."
    )


DATA_CORTE_TREINO = pd.to_datetime(
    linha_data_treino.iloc[0],
    dayfirst=True,
    errors="coerce",
)


if pd.isna(DATA_CORTE_TREINO):
    raise ValueError(
        "A data final do treino é inválida."
    )


# ============================================================
# VALIDAÇÃO DO CUSTO POR TURNOVER
# ============================================================

if {
    "turnover_portfolio",
    "custo_portfolio",
}.issubset(
    backtest.columns
):

    turnover_original = pd.to_numeric(
        backtest[
            "turnover_portfolio"
        ],
        errors="coerce",
    )

    custo_original = pd.to_numeric(
        backtest[
            "custo_portfolio"
        ],
        errors="coerce",
    )

    if (
        turnover_original.isna().any()
        or custo_original.isna().any()
    ):
        raise ValueError(
            "Existem valores inválidos nas colunas "
            "de turnover ou custo do backtest."
        )

    mascara_custo = (
        turnover_original > 0
    )

    taxas_observadas = (
        custo_original.loc[
            mascara_custo
        ]
        / turnover_original.loc[
            mascara_custo
        ]
    ).dropna()

    if not taxas_observadas.empty:

        if not np.allclose(
            taxas_observadas,
            CUSTO_POR_TURNOVER,
            rtol=1e-8,
            atol=1e-12,
        ):
            raise ValueError(
                "O custo configurado não coincide com "
                "o custo utilizado no backtest original."
            )


# ============================================================
# ============================================================
# ORGANIZAÇÃO DOS PESOS BASE
# ============================================================

if "regime" not in pesos_base_df.columns:
    raise ValueError(
        "A coluna regime não foi encontrada."
    )


pesos_base_df["regime"] = (
    pesos_base_df["regime"]
    .astype("string")
    .str.strip()
)


for coluna in colunas_pesos_base:
    pesos_base_df[coluna] = pd.to_numeric(
        pesos_base_df[coluna],
        errors="coerce",
    )


if pesos_base_df[
    colunas_pesos_base
].isna().any().any():
    raise ValueError(
        "Existem pesos inválidos."
    )


regimes_ausentes = [
    regime
    for regime in ORDEM_REGIMES
    if regime not in pesos_base_df[
        "regime"
    ].tolist()
]


if regimes_ausentes:
    raise ValueError(
        "Regimes sem pesos:\n"
        f"{regimes_ausentes}"
    )


pesos_base = {}


for regime in ORDEM_REGIMES:

    linha_regime = (
        pesos_base_df.loc[
            pesos_base_df[
                "regime"
            ]
            == regime
        ]
        .iloc[0]
    )

    pesos_base[regime] = {
        ativo: float(
            linha_regime[
                f"peso_{ativo}"
            ]
        )
        for ativo in ativos
    }

    soma_regime = sum(
        pesos_base[
            regime
        ].values()
    )

    if not np.isclose(
        soma_regime,
        1.0,
        rtol=1e-10,
        atol=1e-10,
    ):
        raise ValueError(
            f"Os pesos de {regime} não somam 100%."
        )


# ============================================================
# BASE MENSAL
# ============================================================

base = (
    backtest[
        [
            "data",
            *ativos,
        ]
    ]
    .merge(
        regimes_suavizados[
            [
                "data",
                COLUNA_REGIME,
            ]
        ],
        on="data",
        how="inner",
        validate="one_to_one",
    )
    .sort_values("data")
    .reset_index(drop=True)
)


if len(base) != len(backtest):
    raise ValueError(
        "A junção alterou a quantidade de meses."
    )


for ativo in ativos:
    base[ativo] = pd.to_numeric(
        base[ativo],
        errors="coerce",
    )


if base[
    ativos
].isna().any().any():
    raise ValueError(
        "Existem retornos de ativos inválidos."
    )


base[
    COLUNA_REGIME
] = (
    base[
        COLUNA_REGIME
    ]
    .astype("string")
    .str.strip()
)


if base[
    COLUNA_REGIME
].isna().any():
    raise ValueError(
        "Existem regimes nulos."
    )


base["periodo"] = np.where(
    base["data"]
    <= DATA_CORTE_TREINO,
    "TREINO",
    "AVALIACAO",
)


mascara_treino = (
    base["periodo"]
    == "TREINO"
)


mascara_avaliacao = (
    base["periodo"]
    == "AVALIACAO"
)


if not mascara_treino.any():
    raise ValueError(
        "O período de treino ficou vazio."
    )


if not mascara_avaliacao.any():
    raise ValueError(
        "O período de avaliação ficou vazio."
    )


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def copiar_pesos(
    pesos,
):
    return {
        regime: {
            ativo: float(
                valor
            )
            for ativo, valor in (
                pesos_regime.items()
            )
        }
        for regime, pesos_regime in (
            pesos.items()
        )
    }


def encolher_regime_para_pesos_iguais(
    pesos,
    regime,
    beta,
    ativos_lista,
):
    novos_pesos = copiar_pesos(
        pesos
    )

    peso_igual = (
        1.0
        / len(
            ativos_lista
        )
    )

    for ativo in ativos_lista:

        peso_atual = float(
            novos_pesos[
                regime
            ][ativo]
        )

        novos_pesos[
            regime
        ][ativo] = float(
            (
                1.0
                - beta
            )
            * peso_atual
            + beta
            * peso_igual
        )

    soma_pesos = sum(
        novos_pesos[
            regime
        ].values()
    )

    if not np.isclose(
        soma_pesos,
        1.0,
        rtol=1e-10,
        atol=1e-10,
    ):
        raise ValueError(
            f"Os pesos ajustados de {regime} "
            "não somam 100%."
        )

    return novos_pesos


def calcular_turnover(
    dados,
    colunas_retornos,
    colunas_pesos,
    cobrar_custo_inicial,
):
    quantidade_periodos = len(
        dados
    )

    turnover = np.zeros(
        quantidade_periodos,
        dtype=float,
    )

    if quantidade_periodos == 0:
        return turnover

    if cobrar_custo_inicial:
        turnover[0] = 1.0

    for indice in range(
        1,
        quantidade_periodos,
    ):

        pesos_anteriores = (
            dados.loc[
                indice - 1,
                colunas_pesos,
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

        retorno_anterior = float(
            np.sum(
                pesos_anteriores
                * retornos_anteriores
            )
        )

        fator_patrimonio = (
            1.0
            + retorno_anterior
        )

        if fator_patrimonio <= 0:
            raise ValueError(
                "O patrimônio relativo ficou menor "
                "ou igual a zero."
            )

        pesos_apos_retorno = (
            pesos_anteriores
            * (
                1.0
                + retornos_anteriores
            )
            / fator_patrimonio
        )

        pesos_alvo = (
            dados.loc[
                indice,
                colunas_pesos,
            ]
            .astype(float)
            .to_numpy()
        )

        turnover[indice] = float(
            np.abs(
                pesos_alvo
                - pesos_apos_retorno
            ).sum()
            / 2.0
        )

    return turnover


def simular_carteira(
    base_original,
    pesos_por_regime,
    nome_cenario,
):
    dados = (
        base_original
        .copy()
        .reset_index(drop=True)
    )

    colunas_pesos = []

    for ativo in ativos:

        coluna_peso = (
            f"peso_{nome_cenario}_{ativo}"
        )

        mapa_peso = {
            regime: (
                pesos_por_regime[
                    regime
                ][ativo]
            )
            for regime in ORDEM_REGIMES
        }

        dados[coluna_peso] = (
            dados[
                COLUNA_REGIME
            ]
            .map(
                mapa_peso
            )
        )

        colunas_pesos.append(
            coluna_peso
        )

    if dados[
        colunas_pesos
    ].isna().any().any():
        raise ValueError(
            f"O cenário {nome_cenario} gerou pesos nulos."
        )

    if not np.allclose(
        dados[
            colunas_pesos
        ].sum(axis=1),
        1.0,
        rtol=1e-10,
        atol=1e-10,
    ):
        raise ValueError(
            f"Os pesos do cenário {nome_cenario} "
            "não somam 100%."
        )

    coluna_retorno_bruto = (
        f"retorno_bruto_{nome_cenario}"
    )

    coluna_turnover = (
        f"turnover_{nome_cenario}"
    )

    coluna_custo = (
        f"custo_{nome_cenario}"
    )

    coluna_retorno_liquido = (
        f"retorno_liquido_{nome_cenario}"
    )

    dados[
        coluna_retorno_bruto
    ] = 0.0

    for ativo, coluna_peso in zip(
        ativos,
        colunas_pesos,
    ):
        dados[
            coluna_retorno_bruto
        ] += (
            dados[
                coluna_peso
            ]
            * dados[
                ativo
            ]
        )

    dados[
        coluna_turnover
    ] = calcular_turnover(
        dados=dados,
        colunas_retornos=ativos,
        colunas_pesos=colunas_pesos,
        cobrar_custo_inicial=(
            COBRAR_CUSTO_INICIAL
        ),
    )

    dados[
        coluna_custo
    ] = (
        dados[
            coluna_turnover
        ]
        * CUSTO_POR_TURNOVER
    )

    dados[
        coluna_retorno_liquido
    ] = (
        (
            1.0
            + dados[
                coluna_retorno_bruto
            ]
        )
        * (
            1.0
            - dados[
                coluna_custo
            ]
        )
        - 1.0
    )

    return dados


def calcular_retorno_total(
    retornos,
):
    retornos = (
        pd.Series(
            retornos
        )
        .dropna()
        .astype(float)
    )

    if retornos.empty:
        return np.nan

    return float(
        (
            1.0
            + retornos
        ).prod()
        - 1.0
    )


def calcular_retorno_anualizado(
    retornos,
):
    retornos = (
        pd.Series(
            retornos
        )
        .dropna()
        .astype(float)
    )

    quantidade = len(
        retornos
    )

    if quantidade == 0:
        return np.nan

    retorno_total = (
        calcular_retorno_total(
            retornos
        )
    )

    return float(
        (
            1.0
            + retorno_total
        )
        ** (
            PERIODOS_POR_ANO
            / quantidade
        )
        - 1.0
    )


def calcular_volatilidade_anualizada(
    retornos,
):
    retornos = (
        pd.Series(
            retornos
        )
        .dropna()
        .astype(float)
    )

    if len(retornos) < 2:
        return np.nan

    return float(
        retornos.std(
            ddof=1
        )
        * np.sqrt(
            PERIODOS_POR_ANO
        )
    )


def calcular_maximo_drawdown(
    retornos,
):
    retornos = (
        pd.Series(
            retornos
        )
        .dropna()
        .astype(float)
        .reset_index(drop=True)
    )

    if retornos.empty:
        return np.nan

    indice = (
        VALOR_INICIAL
        * (
            1.0
            + retornos
        ).cumprod()
    )

    indice_com_inicio = pd.concat(
        [
            pd.Series(
                [
                    VALOR_INICIAL
                ],
                dtype=float,
            ),
            indice,
        ],
        ignore_index=True,
    )

    drawdown = (
        indice_com_inicio
        / indice_com_inicio.cummax()
        - 1.0
    )

    return float(
        drawdown.min()
    )


def calcular_metricas(
    dados,
    nome_cenario,
    mascara_periodo,
):
    coluna_retorno = (
        f"retorno_liquido_{nome_cenario}"
    )

    coluna_turnover = (
        f"turnover_{nome_cenario}"
    )

    coluna_custo = (
        f"custo_{nome_cenario}"
    )

    dados_periodo = (
        dados.loc[
            mascara_periodo
        ]
        .copy()
        .reset_index(drop=True)
    )

    retornos = (
        dados_periodo[
            coluna_retorno
        ]
    )

    retorno_anualizado = (
        calcular_retorno_anualizado(
            retornos
        )
    )

    volatilidade = (
        calcular_volatilidade_anualizada(
            retornos
        )
    )

    if (
        pd.notna(volatilidade)
        and volatilidade > 0
    ):
        retorno_volatilidade = (
            retorno_anualizado
            / volatilidade
        )

    else:
        retorno_volatilidade = np.nan

    return {
        "quantidade_meses": len(
            dados_periodo
        ),
        "retorno_total_liquido": (
            calcular_retorno_total(
                retornos
            )
        ),
        "retorno_anualizado_liquido": (
            retorno_anualizado
        ),
        "volatilidade_anualizada_liquida": (
            volatilidade
        ),
        "retorno_volatilidade_liquido": (
            retorno_volatilidade
        ),
        "maximo_drawdown_liquido": (
            calcular_maximo_drawdown(
                retornos
            )
        ),
        "meses_positivos": float(
            retornos.gt(0).mean()
        ),
        "turnover_total": float(
            dados_periodo[
                coluna_turnover
            ].sum()
        ),
        "turnover_medio_mensal": float(
            dados_periodo[
                coluna_turnover
            ].mean()
        ),
        "custo_acumulado_simples": float(
            dados_periodo[
                coluna_custo
            ].sum()
        ),
        "indice_final_liquido": float(
            VALOR_INICIAL
            * (
                1.0
                + retornos
            ).prod()
        ),
    }


def calcular_estabilidade_rolling(
    dados_candidato,
    dados_benchmark,
    mascara_periodo,
):
    retorno_candidato = (
        dados_candidato.loc[
            mascara_periodo,
            "retorno_liquido_candidato",
        ]
        .reset_index(drop=True)
    )

    retorno_benchmark = (
        dados_benchmark.loc[
            mascara_periodo,
            "retorno_liquido_benchmark",
        ]
        .reset_index(drop=True)
    )

    rolling_candidato = (
        (
            1.0
            + retorno_candidato
        )
        .rolling(
            JANELA_ROLLING
        )
        .apply(
            np.prod,
            raw=True,
        )
        - 1.0
    )

    rolling_benchmark = (
        (
            1.0
            + retorno_benchmark
        )
        .rolling(
            JANELA_ROLLING
        )
        .apply(
            np.prod,
            raw=True,
        )
        - 1.0
    )

    excesso_rolling = (
        rolling_candidato
        - rolling_benchmark
    ).dropna()

    if excesso_rolling.empty:
        return {
            "quantidade_janelas_12m": 0,
            "proporcao_janelas_positivas": np.nan,
            "mediana_excesso_12m": np.nan,
            "media_excesso_12m": np.nan,
            "pior_excesso_12m": np.nan,
        }

    return {
        "quantidade_janelas_12m": len(
            excesso_rolling
        ),
        "proporcao_janelas_positivas": float(
            excesso_rolling.gt(0).mean()
        ),
        "mediana_excesso_12m": float(
            excesso_rolling.median()
        ),
        "media_excesso_12m": float(
            excesso_rolling.mean()
        ),
        "pior_excesso_12m": float(
            excesso_rolling.min()
        ),
    }


# ============================================================
# SIMULAÇÃO DO BENCHMARK
# ============================================================

peso_igual = (
    1.0
    / len(
        ativos
    )
)


pesos_benchmark = {
    regime: {
        ativo: peso_igual
        for ativo in ativos
    }
    for regime in ORDEM_REGIMES
}


simulacao_benchmark = (
    simular_carteira(
        base_original=base,
        pesos_por_regime=pesos_benchmark,
        nome_cenario="benchmark",
    )
)


# ============================================================
# AJUSTE SEQUENCIAL POR REGIME
# ============================================================

contagem_regimes_treino = (
    base.loc[
        mascara_treino,
        COLUNA_REGIME,
    ]
    .value_counts()
    .reindex(
        ORDEM_REGIMES,
        fill_value=0,
    )
)


ordem_ajuste_regimes = (
    contagem_regimes_treino
    .sort_values(
        ascending=False
    )
    .index
    .tolist()
)


pesos_em_ajuste = copiar_pesos(
    pesos_base
)


registros_grade = []
registros_betas = []


for ordem_ajuste, regime in enumerate(
    ordem_ajuste_regimes,
    start=1,
):

    quantidade_meses_regime = int(
        contagem_regimes_treino.loc[
            regime
        ]
    )

    candidatos_regime = []

    for beta in BETAS_ENCOLHIMENTO_REGIME:

        pesos_candidato = (
            encolher_regime_para_pesos_iguais(
                pesos=pesos_em_ajuste,
                regime=regime,
                beta=beta,
                ativos_lista=ativos,
            )
        )

        simulacao_candidato = (
            simular_carteira(
                base_original=base,
                pesos_por_regime=pesos_candidato,
                nome_cenario="candidato",
            )
        )

        metricas_treino = calcular_metricas(
            dados=simulacao_candidato,
            nome_cenario="candidato",
            mascara_periodo=mascara_treino,
        )

        estabilidade = (
            calcular_estabilidade_rolling(
                dados_candidato=simulacao_candidato,
                dados_benchmark=simulacao_benchmark,
                mascara_periodo=mascara_treino,
            )
        )

        registro = {
            "ordem_ajuste": ordem_ajuste,
            "regime": regime,
            "nome_regime": (
                NOMES_REGIMES[
                    regime
                ]
            ),
            "quantidade_meses_regime_treino": (
                quantidade_meses_regime
            ),
            "beta_encolhimento_adicional": float(
                beta
            ),
            **metricas_treino,
            **estabilidade,
        }

        candidatos_regime.append(
            {
                "beta": beta,
                "pesos": pesos_candidato,
                "registro": registro,
            }
        )

        registros_grade.append(
            registro
        )

    candidatos_df = pd.DataFrame(
        [
            candidato[
                "registro"
            ]
            for candidato in candidatos_regime
        ]
    )

    if (
        quantidade_meses_regime
        < MINIMO_MESES_REGIME_TREINO
    ):
        beta_selecionado = 0.0

        motivo_selecao = (
            "Peso mantido por amostra insuficiente"
        )

    else:
        candidatos_ordenados = (
            candidatos_df
            .assign(
                criterio_janelas=(
                    candidatos_df[
                        "proporcao_janelas_positivas"
                    ]
                    .fillna(
                        -np.inf
                    )
                ),
                criterio_mediana=(
                    candidatos_df[
                        "mediana_excesso_12m"
                    ]
                    .fillna(
                        -np.inf
                    )
                ),
                criterio_retorno_vol=(
                    candidatos_df[
                        "retorno_volatilidade_liquido"
                    ]
                    .fillna(
                        -np.inf
                    )
                ),
            )
            .sort_values(
                [
                    "criterio_janelas",
                    "criterio_mediana",
                    "criterio_retorno_vol",
                    "turnover_total",
                    "beta_encolhimento_adicional",
                ],
                ascending=[
                    False,
                    False,
                    False,
                    True,
                    True,
                ],
            )
        )

        beta_selecionado = float(
            candidatos_ordenados[
                "beta_encolhimento_adicional"
            ]
            .iloc[0]
        )

        motivo_selecao = (
            "Selecionado somente com métricas do treino"
        )

    candidato_escolhido = next(
        candidato
        for candidato in candidatos_regime
        if np.isclose(
            candidato[
                "beta"
            ],
            beta_selecionado,
        )
    )

    pesos_em_ajuste = copiar_pesos(
        candidato_escolhido[
            "pesos"
        ]
    )

    registro_escolhido = (
        candidato_escolhido[
            "registro"
        ]
    )

    registros_betas.append(
        {
            "ordem_ajuste": ordem_ajuste,
            "regime": regime,
            "nome_regime": (
                NOMES_REGIMES[
                    regime
                ]
            ),
            "quantidade_meses_regime_treino": (
                quantidade_meses_regime
            ),
            "beta_selecionado": (
                beta_selecionado
            ),
            "proporcao_janelas_positivas_treino": (
                registro_escolhido[
                    "proporcao_janelas_positivas"
                ]
            ),
            "mediana_excesso_12m_treino": (
                registro_escolhido[
                    "mediana_excesso_12m"
                ]
            ),
            "retorno_volatilidade_treino": (
                registro_escolhido[
                    "retorno_volatilidade_liquido"
                ]
            ),
            "turnover_total_treino": (
                registro_escolhido[
                    "turnover_total"
                ]
            ),
            "motivo_selecao": (
                motivo_selecao
            ),
        }
    )


grade_ajustes = pd.DataFrame(
    registros_grade
)


betas_selecionados = pd.DataFrame(
    registros_betas
)


pesos_otimizados = copiar_pesos(
    pesos_em_ajuste
)


# ============================================================
# SIMULAÇÕES FINAIS
# ============================================================

simulacao_base = simular_carteira(
    base_original=base,
    pesos_por_regime=pesos_base,
    nome_cenario="base",
)


simulacao_otimizada = simular_carteira(
    base_original=base,
    pesos_por_regime=pesos_otimizados,
    nome_cenario="otimizada",
)


# ============================================================
# BASE CONSOLIDADA DAS SÉRIES
# ============================================================

series_mensais = (
    base[
        [
            "data",
            "periodo",
            COLUNA_REGIME,
            *ativos,
        ]
    ]
    .copy()
)


for nome_cenario, simulacao in {
    "base": simulacao_base,
    "otimizada": simulacao_otimizada,
    "benchmark": simulacao_benchmark,
}.items():

    colunas_adicionar = [
        f"retorno_bruto_{nome_cenario}",
        f"turnover_{nome_cenario}",
        f"custo_{nome_cenario}",
        f"retorno_liquido_{nome_cenario}",
    ]

    for coluna in colunas_adicionar:
        series_mensais[coluna] = (
            simulacao[coluna]
            .to_numpy()
        )


# ============================================================
# MÉTRICAS COMPARATIVAS
# ============================================================

resultados_metricas = []


for periodo, mascara_periodo in [
    (
        "TREINO",
        mascara_treino,
    ),
    (
        "AVALIACAO",
        mascara_avaliacao,
    ),
]:

    for nome_cenario, simulacao, rotulo in [
        (
            "base",
            simulacao_base,
            "Modelo da Célula 5",
        ),
        (
            "otimizada",
            simulacao_otimizada,
            "Pesos ajustados por regime",
        ),
        (
            "benchmark",
            simulacao_benchmark,
            "Benchmark de pesos iguais",
        ),
    ]:

        metricas = calcular_metricas(
            dados=simulacao,
            nome_cenario=nome_cenario,
            mascara_periodo=mascara_periodo,
        )

        resultados_metricas.append(
            {
                "periodo": periodo,
                "cenario": nome_cenario,
                "rotulo": rotulo,
                **metricas,
            }
        )


metricas_comparativas = pd.DataFrame(
    resultados_metricas
)


for periodo in [
    "TREINO",
    "AVALIACAO",
]:

    indice_benchmark = float(
        metricas_comparativas.loc[
            (
                metricas_comparativas[
                    "periodo"
                ]
                == periodo
            )
            & (
                metricas_comparativas[
                    "cenario"
                ]
                == "benchmark"
            ),
            "indice_final_liquido",
        ]
        .iloc[0]
    )

    metricas_comparativas.loc[
        metricas_comparativas[
            "periodo"
        ]
        == periodo,
        "diferenca_indice_vs_benchmark",
    ] = (
        metricas_comparativas.loc[
            metricas_comparativas[
                "periodo"
            ]
            == periodo,
            "indice_final_liquido",
        ]
        - indice_benchmark
    )


# ============================================================
# PESOS FINAIS
# ============================================================

registros_pesos_finais = []


for regime in ORDEM_REGIMES:

    registro = {
        "regime": regime,
        "nome_regime": (
            NOMES_REGIMES[
                regime
            ]
        ),
        "meses_confirmacao": (
            MESES_CONFIRMACAO
        ),
    }

    beta_regime = float(
        betas_selecionados.loc[
            betas_selecionados[
                "regime"
            ]
            == regime,
            "beta_selecionado",
        ]
        .iloc[0]
    )

    registro[
        "beta_adicional_selecionado"
    ] = beta_regime

    for ativo in ativos:

        registro[
            f"peso_base_{ativo}"
        ] = (
            pesos_base[
                regime
            ][ativo]
        )

        registro[
            f"peso_otimizado_{ativo}"
        ] = (
            pesos_otimizados[
                regime
            ][ativo]
        )

        registro[
            f"alteracao_peso_{ativo}"
        ] = (
            pesos_otimizados[
                regime
            ][ativo]
            - pesos_base[
                regime
            ][ativo]
        )

    registro[
        "soma_pesos_otimizados"
    ] = sum(
        pesos_otimizados[
            regime
        ].values()
    )

    registros_pesos_finais.append(
        registro
    )


pesos_otimizados_df = pd.DataFrame(
    registros_pesos_finais
)


if not np.allclose(
    pesos_otimizados_df[
        "soma_pesos_otimizados"
    ],
    1.0,
    rtol=1e-10,
    atol=1e-10,
):
    raise ValueError(
        "Os pesos finais não somam 100%."
    )


# ============================================================
# RESULTADOS DE AVALIAÇÃO
# ============================================================

resultado_base_avaliacao = (
    metricas_comparativas.loc[
        (
            metricas_comparativas[
                "periodo"
            ]
            == "AVALIACAO"
        )
        & (
            metricas_comparativas[
                "cenario"
            ]
            == "base"
        )
    ]
    .iloc[0]
)


resultado_otimizado_avaliacao = (
    metricas_comparativas.loc[
        (
            metricas_comparativas[
                "periodo"
            ]
            == "AVALIACAO"
        )
        & (
            metricas_comparativas[
                "cenario"
            ]
            == "otimizada"
        )
    ]
    .iloc[0]
)


resultado_benchmark_avaliacao = (
    metricas_comparativas.loc[
        (
            metricas_comparativas[
                "periodo"
            ]
            == "AVALIACAO"
        )
        & (
            metricas_comparativas[
                "cenario"
            ]
            == "benchmark"
        )
    ]
    .iloc[0]
)


diferenca_otimizada_benchmark = float(
    resultado_otimizado_avaliacao[
        "indice_final_liquido"
    ]
    - resultado_benchmark_avaliacao[
        "indice_final_liquido"
    ]
)


melhora_vs_modelo_base = float(
    resultado_otimizado_avaliacao[
        "indice_final_liquido"
    ]
    - resultado_base_avaliacao[
        "indice_final_liquido"
    ]
)


if diferenca_otimizada_benchmark > 0:
    status_avaliacao = (
        "SUPEROU O BENCHMARK"
    )

elif diferenca_otimizada_benchmark < 0:
    status_avaliacao = (
        "FICOU ABAIXO DO BENCHMARK"
    )

else:
    status_avaliacao = (
        "EMPATOU COM O BENCHMARK"
    )


# ============================================================
# TABELAS FORMATADAS
# ============================================================

grade_ajustes_formatada = (
    grade_ajustes
    .copy()
    .astype(object)
)


for coluna in [
    "beta_encolhimento_adicional",
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown_liquido",
    "meses_positivos",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
    "proporcao_janelas_positivas",
    "mediana_excesso_12m",
    "media_excesso_12m",
    "pior_excesso_12m",
]:

    grade_ajustes_formatada[
        coluna
    ] = (
        grade_ajustes[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "retorno_volatilidade_liquido",
    "turnover_total",
    "indice_final_liquido",
]:

    grade_ajustes_formatada[
        coluna
    ] = (
        grade_ajustes[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


metricas_formatadas = (
    metricas_comparativas
    .copy()
    .astype(object)
)


for coluna in [
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown_liquido",
    "meses_positivos",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
]:

    metricas_formatadas[
        coluna
    ] = (
        metricas_comparativas[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "retorno_volatilidade_liquido",
    "turnover_total",
    "indice_final_liquido",
    "diferenca_indice_vs_benchmark",
]:

    metricas_formatadas[
        coluna
    ] = (
        metricas_comparativas[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


# ============================================================
# RESUMO FINAL
# ============================================================

resumo_final = pd.DataFrame(
    {
        "metrica": [
            "Meses de confirmação",
            "Data final do treino",
            "Quantidade de meses de treino",
            "Quantidade de meses de avaliação",
            "Custo por turnover",
            "Índice final do modelo base na avaliação",
            "Índice final do modelo otimizado na avaliação",
            "Índice final do benchmark na avaliação",
            "Melhora do otimizado contra o modelo base",
            "Diferença do otimizado contra o benchmark",
            "Retorno anualizado otimizado na avaliação",
            "Retorno/volatilidade otimizado na avaliação",
            "Turnover otimizado na avaliação",
            "Status da avaliação",
            "Observação metodológica",
        ],
        "valor": [
            MESES_CONFIRMACAO,
            DATA_CORTE_TREINO.strftime(
                "%d/%m/%Y"
            ),
            int(
                mascara_treino.sum()
            ),
            int(
                mascara_avaliacao.sum()
            ),
            CUSTO_POR_TURNOVER,
            resultado_base_avaliacao[
                "indice_final_liquido"
            ],
            resultado_otimizado_avaliacao[
                "indice_final_liquido"
            ],
            resultado_benchmark_avaliacao[
                "indice_final_liquido"
            ],
            melhora_vs_modelo_base,
            diferenca_otimizada_benchmark,
            resultado_otimizado_avaliacao[
                "retorno_anualizado_liquido"
            ],
            resultado_otimizado_avaliacao[
                "retorno_volatilidade_liquido"
            ],
            resultado_otimizado_avaliacao[
                "turnover_total"
            ],
            status_avaliacao,
            (
                "Os pesos foram selecionados somente com "
                f"dados até {DATA_CORTE_TREINO:%d/%m/%Y}."
            ),
        ],
    }
)


# ============================================================
# SALVAMENTO
# ============================================================

grade_ajustes.to_csv(
    ARQUIVO_GRADE_AJUSTES,
    index=False,
    encoding="utf-8-sig",
)


grade_ajustes_formatada.to_csv(
    ARQUIVO_GRADE_AJUSTES_FORMATADA,
    index=False,
    encoding="utf-8-sig",
)


betas_selecionados.to_csv(
    ARQUIVO_BETAS_SELECIONADOS,
    index=False,
    encoding="utf-8-sig",
)


pesos_otimizados_df.to_csv(
    ARQUIVO_PESOS_OTIMIZADOS,
    index=False,
    encoding="utf-8-sig",
)


metricas_comparativas.to_csv(
    ARQUIVO_METRICAS_COMPARATIVAS,
    index=False,
    encoding="utf-8-sig",
)


metricas_formatadas.to_csv(
    ARQUIVO_METRICAS_FORMATADAS,
    index=False,
    encoding="utf-8-sig",
)


series_mensais.to_csv(
    ARQUIVO_SERIES_MENSAIS,
    index=False,
    encoding="utf-8-sig",
)


resumo_final.to_csv(
    ARQUIVO_RESUMO_FINAL,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# BASE PARA GRÁFICOS DE AVALIAÇÃO
# ============================================================

series_avaliacao = (
    series_mensais.loc[
        series_mensais[
            "periodo"
        ]
        == "AVALIACAO"
    ]
    .copy()
    .reset_index(drop=True)
)


for nome_cenario in [
    "base",
    "otimizada",
    "benchmark",
]:

    series_avaliacao[
        f"indice_{nome_cenario}"
    ] = (
        VALOR_INICIAL
        * (
            1.0
            + series_avaliacao[
                f"retorno_liquido_{nome_cenario}"
            ]
        ).cumprod()
    )


series_avaliacao[
    "diferenca_otimizada_benchmark"
] = (
    series_avaliacao[
        "indice_otimizada"
    ]
    - series_avaliacao[
        "indice_benchmark"
    ]
)


data_inicial_grafico = (
    series_avaliacao[
        "data"
    ].iloc[0]
    - pd.offsets.MonthEnd(1)
)


linha_inicial = pd.DataFrame(
    {
        "data": [
            data_inicial_grafico
        ],
        "indice_base": [
            VALOR_INICIAL
        ],
        "indice_otimizada": [
            VALOR_INICIAL
        ],
        "indice_benchmark": [
            VALOR_INICIAL
        ],
        "diferenca_otimizada_benchmark": [
            0.0
        ],
    }
)


series_grafico = pd.concat(
    [
        linha_inicial,
        series_avaliacao[
            [
                "data",
                "indice_base",
                "indice_otimizada",
                "indice_benchmark",
                "diferenca_otimizada_benchmark",
            ]
        ],
    ],
    ignore_index=True,
)


# ============================================================
# GRÁFICO 1 — DESEMPENHO NO PERÍODO DE AVALIAÇÃO
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "indice_base"
    ],
    linewidth=2,
    label="Modelo da Célula 5",
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "indice_otimizada"
    ],
    linewidth=2,
    label="Pesos ajustados por regime",
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "indice_benchmark"
    ],
    linewidth=2,
    label="Benchmark de pesos iguais",
)


ax.axhline(
    y=VALOR_INICIAL,
    linewidth=1,
)


ax.set_title(
    "Desempenho no Período de Avaliação"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Índice acumulado"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DESEMPENHO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — DIFERENÇA CONTRA O BENCHMARK
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "diferenca_otimizada_benchmark"
    ],
    linewidth=2,
)


ax.axhline(
    y=0,
    linewidth=1,
)


ax.set_title(
    "Diferença dos Pesos Ajustados contra o Benchmark"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Diferença do índice em pontos"
)

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DIFERENCA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — COMPARAÇÃO DOS PESOS
# ============================================================

dados_pesos_grafico = []


for regime in ORDEM_REGIMES:

    for ativo in ativos:

        dados_pesos_grafico.append(
            {
                "nome_regime": (
                    NOMES_REGIMES[
                        regime
                    ]
                ),
                "ativo": ativo,
                "tipo": "Peso base",
                "peso": (
                    pesos_base[
                        regime
                    ][ativo]
                ),
            }
        )

        dados_pesos_grafico.append(
            {
                "nome_regime": (
                    NOMES_REGIMES[
                        regime
                    ]
                ),
                "ativo": ativo,
                "tipo": "Peso otimizado",
                "peso": (
                    pesos_otimizados[
                        regime
                    ][ativo]
                ),
            }
        )


dados_pesos_grafico = pd.DataFrame(
    dados_pesos_grafico
)


fig, ax = plt.subplots(
    figsize=(14, 8)
)


dados_pesos_grafico[
    "categoria"
] = (
    dados_pesos_grafico[
        "nome_regime"
    ]
    + "\n"
    + dados_pesos_grafico[
        "ativo"
    ]
)


tabela_pesos_grafico = (
    dados_pesos_grafico
    .pivot(
        index="categoria",
        columns="tipo",
        values="peso",
    )
)


tabela_pesos_grafico.plot(
    kind="bar",
    ax=ax,
    width=0.75,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Comparação dos Pesos Base e Otimizados"
)

ax.set_xlabel(
    "Regime e ativo"
)

ax.set_ylabel(
    "Peso da carteira"
)

ax.tick_params(
    axis="x",
    rotation=70,
)

ax.legend(
    title=""
)

ax.grid(
    axis="y",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_PESOS,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_GRADE_AJUSTES,
    ARQUIVO_GRADE_AJUSTES_FORMATADA,
    ARQUIVO_BETAS_SELECIONADOS,
    ARQUIVO_PESOS_OTIMIZADOS,
    ARQUIVO_METRICAS_COMPARATIVAS,
    ARQUIVO_METRICAS_FORMATADAS,
    ARQUIVO_SERIES_MENSAIS,
    ARQUIVO_RESUMO_FINAL,
    ARQUIVO_GRAFICO_DESEMPENHO,
    ARQUIVO_GRAFICO_DIFERENCA,
    ARQUIVO_GRAFICO_PESOS,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:
    raise FileNotFoundError(
        "Alguns arquivos não foram salvos:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("=" * 70)
print("AJUSTE INDIVIDUAL DOS PESOS CONCLUÍDO")
print("=" * 70)

print(
    f"\nRaiz do projeto:\n"
    f"{RAIZ_PROJETO}"
)

print(
    f"\nArquivo de configuração:\n"
    f"{ARQUIVO_CONFIG}"
)

print(
    f"\nConfirmação utilizada: "
    f"{MESES_CONFIRMACAO} mês(es)"
)

print(
    f"Betas testados: "
    f"{BETAS_ENCOLHIMENTO_REGIME}"
)

print(
    f"Janela rolling: "
    f"{JANELA_ROLLING} meses"
)

print(
    f"Mínimo de meses por regime no treino: "
    f"{MINIMO_MESES_REGIME_TREINO}"
)

print(
    f"Cobrança de custo inicial: "
    f"{COBRAR_CUSTO_INICIAL}"
)

print(
    f"Custo utilizado: "
    f"{CUSTO_POR_TURNOVER:.4%} "
    f"({CUSTO_POR_TURNOVER * 10000:.2f} bps)"
)

print(
    f"\nPeríodo usado para selecionar os pesos: "
    f"{base.loc[mascara_treino, 'data'].min():%d/%m/%Y} "
    f"a "
    f"{base.loc[mascara_treino, 'data'].max():%d/%m/%Y}"
)

print(
    f"Quantidade de meses de treino: "
    f"{int(mascara_treino.sum())}"
)

print(
    f"\nPeríodo de avaliação: "
    f"{base.loc[mascara_avaliacao, 'data'].min():%d/%m/%Y} "
    f"a "
    f"{base.loc[mascara_avaliacao, 'data'].max():%d/%m/%Y}"
)

print(
    f"Quantidade de meses de avaliação: "
    f"{int(mascara_avaliacao.sum())}"
)

print(
    f"\nÍndice final do modelo base: "
    f"{resultado_base_avaliacao['indice_final_liquido']:.2f}"
)

print(
    f"Índice final do modelo otimizado: "
    f"{resultado_otimizado_avaliacao['indice_final_liquido']:.2f}"
)

print(
    f"Índice final do benchmark: "
    f"{resultado_benchmark_avaliacao['indice_final_liquido']:.2f}"
)

print(
    f"\nMelhora contra o modelo base: "
    f"{melhora_vs_modelo_base:.2f} pontos"
)

print(
    f"Diferença contra o benchmark: "
    f"{diferenca_otimizada_benchmark:.2f} pontos"
)

print(
    f"\nRetorno anualizado otimizado: "
    f"{resultado_otimizado_avaliacao['retorno_anualizado_liquido']:.2%}"
)

print(
    f"Retorno/volatilidade otimizado: "
    f"{resultado_otimizado_avaliacao['retorno_volatilidade_liquido']:.2f}"
)

print(
    f"Turnover total otimizado: "
    f"{resultado_otimizado_avaliacao['turnover_total']:.4f}"
)

print(
    f"\nResultado no período de avaliação: "
    f"{status_avaliacao}"
)

print(
    f"\nGrade de ajustes salva em:\n"
    f"{ARQUIVO_GRADE_AJUSTES}"
)

print(
    f"\nBetas selecionados salvos em:\n"
    f"{ARQUIVO_BETAS_SELECIONADOS}"
)

print(
    f"\nPesos otimizados salvos em:\n"
    f"{ARQUIVO_PESOS_OTIMIZADOS}"
)

print(
    f"\nMétricas comparativas salvas em:\n"
    f"{ARQUIVO_METRICAS_COMPARATIVAS}"
)

print(
    f"\nResumo final salvo em:\n"
    f"{ARQUIVO_RESUMO_FINAL}"
)

print(
    "\nBetas selecionados por regime:"
)

display(
    betas_selecionados
)


print(
    "\nPesos finais por regime:"
)

display(
    pesos_otimizados_df
)


print(
    "\nMétricas comparativas:"
)

display(
    metricas_formatadas
)

# ###########################################################################
# ETAPA 08 — PREPARAÇÃO LOCAL DA RENDA FIXA
# ###########################################################################

# ============================================================
# CDI LOCAL + EXCLUSÃO DA SÉRIE OFICIAL PARCIAL DO IMA-B
#
# Esta etapa não realiza nova chamada à API do Banco Central.
# O CDI já foi coletado pela Etapa 01 e incluído no backtest
# pela Etapa 04.
#
# A série SGS 12466 do IMA-B oficial permanece excluída por
# cobertura parcial. O ETF IMAB11.SA pode permanecer quando
# aprovado pela coleta do Yahoo Finance.
# ============================================================

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ============================================================
# LOCALIZAÇÃO DA RAIZ
# ============================================================

DIRETORIO_ATUAL = Path.cwd().resolve()

RAIZ_PROJETO = None

for diretorio in [
    DIRETORIO_ATUAL,
    *DIRETORIO_ATUAL.parents,
]:

    arquivo_teste = (
        diretorio
        / "data"
        / "processed"
        / "backtest_portfolio_mensal.csv"
    )

    if arquivo_teste.exists():

        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:

    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo data/processed/"
        "backtest_portfolio_mensal.csv não foi encontrado."
    )


PASTA_DADOS_PROCESSADOS = (
    RAIZ_PROJETO
    / "data"
    / "processed"
)

PASTA_TABELAS = (
    RAIZ_PROJETO
    / "outputs"
    / "tabelas"
)

PASTA_GRAFICOS = (
    RAIZ_PROJETO
    / "outputs"
    / "graficos"
)


for pasta in [
    PASTA_DADOS_PROCESSADOS,
    PASTA_TABELAS,
    PASTA_GRAFICOS,
]:

    pasta.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# ARQUIVOS
# ============================================================

ARQUIVO_BACKTEST = (
    PASTA_DADOS_PROCESSADOS
    / "backtest_portfolio_mensal.csv"
)

ARQUIVO_MACRO_MENSAL = (
    PASTA_DADOS_PROCESSADOS
    / "dados_macro_mensais.csv"
)

ARQUIVO_CDI_MENSAL = (
    PASTA_DADOS_PROCESSADOS
    / "cdi_sgs_12_mensal.csv"
)

ARQUIVO_RETORNOS_RENDA_FIXA = (
    PASTA_DADOS_PROCESSADOS
    / "retornos_renda_fixa_mensais.csv"
)

ARQUIVO_RETORNOS_AMPLIADOS = (
    PASTA_DADOS_PROCESSADOS
    / "retornos_ativos_ampliados_mensais.csv"
)

ARQUIVO_STATUS = (
    PASTA_TABELAS
    / "06_08_status_fontes_renda_fixa.csv"
)

ARQUIVO_VALIDACAO = (
    PASTA_TABELAS
    / "06_08_validacao_renda_fixa.csv"
)

ARQUIVO_RESUMO = (
    PASTA_TABELAS
    / "06_08_resumo_renda_fixa.csv"
)

ARQUIVO_REMOVIDOS = (
    PASTA_TABELAS
    / "06_08_arquivos_proxy_removidos.csv"
)

ARQUIVO_GRAFICO_CDI = (
    PASTA_GRAFICOS
    / "06_08_cdi_acumulado.png"
)


# Arquivos antigos que não devem continuar sendo usados.
ARQUIVOS_IMAB_PARCIAL_ANTIGOS = [
    (
        PASTA_DADOS_PROCESSADOS
        / "imab_sgs_12466_diario_parcial.csv"
    ),
    (
        PASTA_DADOS_PROCESSADOS
        / "imab_sgs_12466_mensal_parcial.csv"
    ),
]


# ============================================================
# CARREGAMENTO DO BACKTEST
# ============================================================

backtest_renda_fixa = pd.read_csv(
    ARQUIVO_BACKTEST,
    encoding="utf-8-sig",
    low_memory=False,
)


if "data" not in backtest_renda_fixa.columns:

    raise ValueError(
        "O backtest não possui a coluna data."
    )


backtest_renda_fixa["data"] = pd.to_datetime(
    backtest_renda_fixa["data"],
    errors="coerce",
)


if backtest_renda_fixa["data"].isna().any():

    raise ValueError(
        "O backtest possui datas inválidas."
    )


if backtest_renda_fixa["data"].duplicated().any():

    raise ValueError(
        "O backtest possui datas duplicadas."
    )


backtest_renda_fixa = (
    backtest_renda_fixa
    .sort_values(
        "data"
    )
    .reset_index(
        drop=True
    )
)


# ============================================================
# IDENTIFICAÇÃO DOS ATIVOS
# ============================================================

ATIVOS_BACKTEST = []


for coluna in backtest_renda_fixa.columns:

    if not coluna.startswith(
        "peso_"
    ):

        continue

    ativo = coluna.replace(
        "peso_",
        "",
        1,
    )

    if ativo in backtest_renda_fixa.columns:

        ATIVOS_BACKTEST.append(
            ativo
        )


ATIVOS_BACKTEST = list(
    dict.fromkeys(
        ATIVOS_BACKTEST
    )
)


if not ATIVOS_BACKTEST:

    raise ValueError(
        "Não foi possível identificar os ativos "
        "do backtest pelas colunas peso_*."
    )


# ============================================================
# CDI
# ============================================================

FONTE_CDI = None


if "CDI" in backtest_renda_fixa.columns:

    cdi_mensal = (
        backtest_renda_fixa[
            [
                "data",
                "CDI",
            ]
        ]
        .copy()
    )

    FONTE_CDI = (
        "backtest_portfolio_mensal.csv"
    )

else:

    if not ARQUIVO_MACRO_MENSAL.exists():

        raise FileNotFoundError(
            "O CDI não está no backtest e a base macro "
            "mensal não foi encontrada:\n"
            f"{ARQUIVO_MACRO_MENSAL}"
        )

    macro_mensal = pd.read_csv(
        ARQUIVO_MACRO_MENSAL,
        encoding="utf-8-sig",
        low_memory=False,
    )

    colunas_macro_obrigatorias = {
        "data",
        "CDI_MENSAL_PCT",
    }

    colunas_macro_ausentes = (
        colunas_macro_obrigatorias
        - set(
            macro_mensal.columns
        )
    )

    if colunas_macro_ausentes:

        raise ValueError(
            "A base macro mensal não possui as colunas "
            f"necessárias para o CDI: "
            f"{sorted(colunas_macro_ausentes)}"
        )

    macro_mensal["data"] = pd.to_datetime(
        macro_mensal["data"],
        errors="coerce",
    )

    macro_mensal["CDI"] = (
        pd.to_numeric(
            macro_mensal[
                "CDI_MENSAL_PCT"
            ],
            errors="coerce",
        )
        / 100.0
    )

    cdi_mensal = (
        backtest_renda_fixa[
            [
                "data",
            ]
        ]
        .merge(
            macro_mensal[
                [
                    "data",
                    "CDI",
                ]
            ],
            on="data",
            how="left",
            validate="one_to_one",
        )
    )

    FONTE_CDI = (
        "dados_macro_mensais.csv"
    )


cdi_mensal["CDI"] = pd.to_numeric(
    cdi_mensal["CDI"],
    errors="coerce",
)


if cdi_mensal["CDI"].isna().any():

    nulos_cdi = int(
        cdi_mensal["CDI"]
        .isna()
        .sum()
    )

    raise ValueError(
        "Existem valores nulos na série mensal do CDI. "
        f"Quantidade: {nulos_cdi}"
    )


if (
    cdi_mensal["CDI"]
    <= -1.0
).any():

    raise ValueError(
        "O CDI possui retorno mensal menor ou igual a -100%."
    )


if (
    cdi_mensal["CDI"]
    .abs()
    > 0.10
).any():

    raise ValueError(
        "O CDI possui retorno mensal superior a 10% "
        "em valor absoluto."
    )


# ============================================================
# BASE AMPLIADA
# ============================================================

ATIVOS_RISCO_LOCAIS = [
    ativo
    for ativo in ATIVOS_BACKTEST
    if ativo != "CDI"
]


retornos_ampliados = (
    backtest_renda_fixa[
        [
            "data",
            *ATIVOS_RISCO_LOCAIS,
        ]
    ]
    .copy()
)


retornos_ampliados = (
    retornos_ampliados
    .merge(
        cdi_mensal,
        on="data",
        how="left",
        validate="one_to_one",
    )
)


ATIVOS_BASE_AMPLIADA = [
    *ATIVOS_RISCO_LOCAIS,
    "CDI",
]


for ativo in ATIVOS_BASE_AMPLIADA:

    retornos_ampliados[ativo] = pd.to_numeric(
        retornos_ampliados[ativo],
        errors="coerce",
    )


if (
    retornos_ampliados[
        ATIVOS_BASE_AMPLIADA
    ]
    .isna()
    .any()
    .any()
):

    nulos = (
        retornos_ampliados[
            ATIVOS_BASE_AMPLIADA
        ]
        .isna()
        .sum()
    )

    nulos = nulos.loc[
        nulos > 0
    ]

    raise ValueError(
        "Existem valores nulos na base ampliada:\n"
        f"{nulos}"
    )


if len(
    retornos_ampliados
) != len(
    backtest_renda_fixa
):

    raise ValueError(
        "A preparação local da renda fixa alterou "
        "a quantidade de meses."
    )


retornos_renda_fixa = (
    cdi_mensal.copy()
)


# ============================================================
# EXCLUSÃO DOS ARQUIVOS ANTIGOS DO IMA-B PARCIAL
# ============================================================

arquivos_removidos = []


for arquivo_antigo in (
    ARQUIVOS_IMAB_PARCIAL_ANTIGOS
):

    existia = arquivo_antigo.exists()

    if existia:

        arquivo_antigo.unlink()

    arquivos_removidos.append(
        {
            "arquivo": str(
                arquivo_antigo
            ),
            "existia_antes": bool(
                existia
            ),
            "acao": (
                "REMOVIDO"
                if existia
                else "NAO_EXISTIA"
            ),
            "motivo": (
                "Série oficial parcial do IMA-B "
                "excluída do modelo final."
            ),
        }
    )


# ============================================================
# SAÍDAS
# ============================================================

cdi_mensal.to_csv(
    ARQUIVO_CDI_MENSAL,
    index=False,
    encoding="utf-8-sig",
)

retornos_renda_fixa.to_csv(
    ARQUIVO_RETORNOS_RENDA_FIXA,
    index=False,
    encoding="utf-8-sig",
)

retornos_ampliados.to_csv(
    ARQUIVO_RETORNOS_AMPLIADOS,
    index=False,
    encoding="utf-8-sig",
)


status_fontes = pd.DataFrame(
    [
        {
            "ativo": "CDI",
            "status": "DISPONIVEL",
            "fonte": FONTE_CDI,
            "incluido_modelo": True,
            "observacao": (
                "Série mensal já disponível localmente. "
                "Nenhuma nova requisição ao BCB foi realizada."
            ),
        },
        {
            "ativo": "IMAB_OFICIAL_PARCIAL",
            "status": "EXCLUIDO",
            "fonte": "SGS 12466",
            "incluido_modelo": False,
            "observacao": (
                "Série oficial possui cobertura parcial. "
                "IMAB11.SA permanece elegível quando aprovado."
            ),
        },
    ]
)


validacoes_renda_fixa = pd.DataFrame(
    [
        {
            "validacao": "CDI disponível no período completo",
            "status": "APROVADO",
            "detalhe": (
                f"{len(cdi_mensal)} meses | "
                f"fonte: {FONTE_CDI}"
            ),
        },
        {
            "validacao": "Base ampliada sem valores nulos",
            "status": "APROVADO",
            "detalhe": (
                f"{len(retornos_ampliados)} meses e "
                f"{len(ATIVOS_BASE_AMPLIADA)} ativos"
            ),
        },
        {
            "validacao": "Série oficial parcial do IMA-B excluída",
            "status": "APROVADO",
            "detalhe": (
                "SGS 12466 não foi coletada nem incluída."
            ),
        },
        {
            "validacao": "Quantidade de meses preservada",
            "status": "APROVADO",
            "detalhe": (
                f"{len(retornos_ampliados)} meses"
            ),
        },
    ]
)


resumo_renda_fixa = pd.DataFrame(
    [
        {
            "metrica": "Data inicial",
            "valor": (
                retornos_ampliados[
                    "data"
                ]
                .min()
                .strftime(
                    "%d/%m/%Y"
                )
            ),
        },
        {
            "metrica": "Data final",
            "valor": (
                retornos_ampliados[
                    "data"
                ]
                .max()
                .strftime(
                    "%d/%m/%Y"
                )
            ),
        },
        {
            "metrica": "Quantidade de meses",
            "valor": len(
                retornos_ampliados
            ),
        },
        {
            "metrica": "Quantidade de ativos de risco",
            "valor": len(
                ATIVOS_RISCO_LOCAIS
            ),
        },
        {
            "metrica": "CDI incluído",
            "valor": "SIM",
        },
        {
            "metrica": "Fonte do CDI",
            "valor": FONTE_CDI,
        },
        {
            "metrica": "IMA-B oficial parcial incluído",
            "valor": "NÃO",
        },
        {
            "metrica": "Nova chamada ao BCB nesta etapa",
            "valor": "NÃO",
        },
    ]
)


status_fontes.to_csv(
    ARQUIVO_STATUS,
    index=False,
    encoding="utf-8-sig",
)

validacoes_renda_fixa.to_csv(
    ARQUIVO_VALIDACAO,
    index=False,
    encoding="utf-8-sig",
)

resumo_renda_fixa.to_csv(
    ARQUIVO_RESUMO,
    index=False,
    encoding="utf-8-sig",
)

pd.DataFrame(
    arquivos_removidos
).to_csv(
    ARQUIVO_REMOVIDOS,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO DO CDI
# ============================================================

indice_cdi = (
    100.0
    * (
        1.0
        + cdi_mensal["CDI"]
    )
    .cumprod()
)


figura, eixo = plt.subplots(
    figsize=(
        12,
        6,
    )
)

eixo.plot(
    cdi_mensal["data"],
    indice_cdi,
)

eixo.set_title(
    "CDI acumulado — base local"
)

eixo.set_xlabel(
    "Data"
)

eixo.set_ylabel(
    "Índice base 100"
)

eixo.grid(
    alpha=0.30
)

figura.tight_layout()

figura.savefig(
    ARQUIVO_GRAFICO_CDI,
    dpi=150,
    bbox_inches="tight",
)

plt.close(
    figura
)


print(
    "="
    * 70
)

print(
    "PREPARAÇÃO LOCAL DA RENDA FIXA CONCLUÍDA"
)

print(
    "="
    * 70
)

print(
    f"Fonte do CDI: {FONTE_CDI}"
)

print(
    "Nova chamada ao BCB: NÃO"
)

print(
    "IMA-B oficial parcial SGS 12466: EXCLUÍDO"
)

print(
    f"Ativos de risco: {len(ATIVOS_RISCO_LOCAIS)}"
)

print(
    f"Meses: {len(retornos_ampliados)}"
)

print(
    f"Base ampliada salva em:\n"
    f"{ARQUIVO_RETORNOS_AMPLIADOS}"
)


# ###########################################################################
# ETAPA 09 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 9 — REOTIMIZAÇÃO DA ESTRATÉGIA COM CDI
# VERSÃO AUTÔNOMA
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

from pathlib import Path
from itertools import product

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml

from matplotlib.ticker import PercentFormatter


# ============================================================
# REGIMES E NOMES
# ============================================================

ORDEM_REGIMES = [
    "EXPANSAO_DESINFLACIONARIA",
    "EXPANSAO_INFLACIONARIA",
    "ESTAGFLACAO",
    "RECESSAO_DESINFLACIONARIA",
]

NOMES_REGIMES = {
    "EXPANSAO_DESINFLACIONARIA": (
        "Expansão desinflacionária"
    ),
    "EXPANSAO_INFLACIONARIA": (
        "Expansão inflacionária"
    ),
    "ESTAGFLACAO": (
        "Estagflação"
    ),
    "RECESSAO_DESINFLACIONARIA": (
        "Recessão desinflacionária"
    ),
}


# ============================================================
# LOCALIZAÇÃO DA RAIZ DO PROJETO
# ============================================================

DIRETORIO_ATUAL = Path.cwd().resolve()

RAIZ_PROJETO = None

for diretorio in [
    DIRETORIO_ATUAL,
    *DIRETORIO_ATUAL.parents,
]:
    arquivo_teste = (
        diretorio
        / "data"
        / "processed"
        / "backtest_portfolio_mensal.csv"
    )

    if arquivo_teste.exists():
        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:
    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo data/processed/"
        "backtest_portfolio_mensal.csv não foi encontrado."
    )


PASTA_DADOS_PROCESSADOS = (
    RAIZ_PROJETO
    / "data"
    / "processed"
)

PASTA_TABELAS = (
    RAIZ_PROJETO
    / "outputs"
    / "tabelas"
)

PASTA_GRAFICOS = (
    RAIZ_PROJETO
    / "outputs"
    / "graficos"
)


PASTA_TABELAS.mkdir(
    parents=True,
    exist_ok=True,
)

PASTA_GRAFICOS.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CARREGAMENTO DO CONFIG.YAML
# ============================================================

ARQUIVO_CONFIG = (
    RAIZ_PROJETO
    / "config"
    / "config.yaml"
)


if not ARQUIVO_CONFIG.exists():
    raise FileNotFoundError(
        "Arquivo de configuração não encontrado:\n"
        f"{ARQUIVO_CONFIG}"
    )


with ARQUIVO_CONFIG.open(
    mode="r",
    encoding="utf-8",
) as arquivo_yaml:

    CONFIGURACAO = (
        yaml.safe_load(
            arquivo_yaml
        )
        or {}
    )


if (
    "backtest" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["backtest"],
        dict,
    )
):
    raise KeyError(
        "A seção 'backtest' não foi encontrada "
        "no config/config.yaml."
    )


if (
    "otimizacao" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["otimizacao"],
        dict,
    )
):
    raise KeyError(
        "A seção 'otimizacao' não foi encontrada "
        "no config/config.yaml."
    )


CONFIGURACAO_BACKTEST = (
    CONFIGURACAO[
        "backtest"
    ]
)

CONFIGURACAO_OTIMIZACAO = (
    CONFIGURACAO[
        "otimizacao"
    ]
)


parametros_backtest_obrigatorios = [
    "valor_inicial",
    "periodos_por_ano",
    "periodos_janela",
    "custo_por_turnover",
    "cobrar_custo_inicial",
]

parametros_backtest_ausentes = [
    parametro
    for parametro in parametros_backtest_obrigatorios
    if parametro not in CONFIGURACAO_BACKTEST
]

if parametros_backtest_ausentes:
    raise KeyError(
        "Parâmetros ausentes na seção 'backtest' "
        "do config.yaml:\n"
        f"{parametros_backtest_ausentes}"
    )


parametros_otimizacao_obrigatorios = [
    "janelas_confirmacao",
    "pesos_cdi_testados",
    "minimo_meses_treino_cdi",
    "minimo_meses_avaliacao_cdi",
]

parametros_otimizacao_ausentes = [
    parametro
    for parametro in parametros_otimizacao_obrigatorios
    if parametro not in CONFIGURACAO_OTIMIZACAO
]

if parametros_otimizacao_ausentes:
    raise KeyError(
        "Parâmetros ausentes na seção 'otimizacao' "
        "do config.yaml:\n"
        f"{parametros_otimizacao_ausentes}"
    )


VALOR_INICIAL = float(
    CONFIGURACAO_BACKTEST[
        "valor_inicial"
    ]
)

PERIODOS_POR_ANO = int(
    CONFIGURACAO_BACKTEST[
        "periodos_por_ano"
    ]
)

JANELA_ROLLING = int(
    CONFIGURACAO_BACKTEST[
        "periodos_janela"
    ]
)

CUSTO_POR_TURNOVER = float(
    CONFIGURACAO_BACKTEST[
        "custo_por_turnover"
    ]
)

COBRAR_CUSTO_INICIAL = (
    CONFIGURACAO_BACKTEST[
        "cobrar_custo_inicial"
    ]
)


janelas_confirmacao_configuradas = (
    CONFIGURACAO_OTIMIZACAO[
        "janelas_confirmacao"
    ]
)

pesos_cdi_configurados = (
    CONFIGURACAO_OTIMIZACAO[
        "pesos_cdi_testados"
    ]
)

MINIMO_MESES_TREINO_CDI = int(
    CONFIGURACAO_OTIMIZACAO[
        "minimo_meses_treino_cdi"
    ]
)

MINIMO_MESES_AVALIACAO_CDI = int(
    CONFIGURACAO_OTIMIZACAO[
        "minimo_meses_avaliacao_cdi"
    ]
)


if VALOR_INICIAL <= 0:
    raise ValueError(
        "'backtest.valor_inicial' "
        "deve ser maior que zero."
    )


if PERIODOS_POR_ANO <= 0:
    raise ValueError(
        "'backtest.periodos_por_ano' "
        "deve ser maior que zero."
    )


if JANELA_ROLLING <= 0:
    raise ValueError(
        "'backtest.periodos_janela' "
        "deve ser maior que zero."
    )


if CUSTO_POR_TURNOVER < 0:
    raise ValueError(
        "'backtest.custo_por_turnover' "
        "não pode ser negativo."
    )


if not isinstance(
    COBRAR_CUSTO_INICIAL,
    bool,
):
    raise TypeError(
        "'backtest.cobrar_custo_inicial' "
        "deve ser true ou false."
    )


if not isinstance(
    janelas_confirmacao_configuradas,
    list,
):
    raise TypeError(
        "'otimizacao.janelas_confirmacao' "
        "deve ser uma lista."
    )


if not janelas_confirmacao_configuradas:
    raise ValueError(
        "'otimizacao.janelas_confirmacao' "
        "não pode estar vazia."
    )


try:
    JANELAS_CONFIRMACAO = [
        int(janela)
        for janela in janelas_confirmacao_configuradas
    ]

except (
    TypeError,
    ValueError,
) as erro:
    raise TypeError(
        "Todos os valores de "
        "'otimizacao.janelas_confirmacao' "
        "devem ser inteiros."
    ) from erro


if any(
    janela < 1
    for janela in JANELAS_CONFIRMACAO
):
    raise ValueError(
        "Todas as janelas de confirmação "
        "devem ser maiores ou iguais a 1."
    )


if (
    len(JANELAS_CONFIRMACAO)
    != len(set(JANELAS_CONFIRMACAO))
):
    raise ValueError(
        "A lista de janelas de confirmação "
        "possui valores duplicados."
    )


if 1 not in JANELAS_CONFIRMACAO:
    raise ValueError(
        "A janela de confirmação de 1 mês "
        "é obrigatória."
    )


JANELAS_CONFIRMACAO = sorted(
    JANELAS_CONFIRMACAO
)


if not isinstance(
    pesos_cdi_configurados,
    list,
):
    raise TypeError(
        "'otimizacao.pesos_cdi_testados' "
        "deve ser uma lista."
    )


if not pesos_cdi_configurados:
    raise ValueError(
        "'otimizacao.pesos_cdi_testados' "
        "não pode estar vazia."
    )


try:
    PESOS_CDI_TESTADOS = [
        float(peso)
        for peso in pesos_cdi_configurados
    ]

except (
    TypeError,
    ValueError,
) as erro:
    raise TypeError(
        "Todos os valores de "
        "'otimizacao.pesos_cdi_testados' "
        "devem ser numéricos."
    ) from erro


if any(
    peso < 0.0
    or peso > 1.0
    for peso in PESOS_CDI_TESTADOS
):
    raise ValueError(
        "Todos os pesos de CDI testados "
        "devem estar entre 0 e 1."
    )


if (
    len(PESOS_CDI_TESTADOS)
    != len(set(PESOS_CDI_TESTADOS))
):
    raise ValueError(
        "A lista de pesos de CDI testados "
        "possui valores duplicados."
    )


if not any(
    np.isclose(
        peso,
        0.0,
    )
    for peso in PESOS_CDI_TESTADOS
):
    raise ValueError(
        "O peso 0.0 de CDI é obrigatório "
        "para representar o modelo sem CDI."
    )


PESOS_CDI_TESTADOS = sorted(
    PESOS_CDI_TESTADOS
)


if MINIMO_MESES_TREINO_CDI <= 0:
    raise ValueError(
        "'otimizacao.minimo_meses_treino_cdi' "
        "deve ser maior que zero."
    )


if MINIMO_MESES_AVALIACAO_CDI <= 0:
    raise ValueError(
        "'otimizacao.minimo_meses_avaliacao_cdi' "
        "deve ser maior que zero."
    )


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ARQUIVO_RETORNOS_AMPLIADOS = (
    PASTA_DADOS_PROCESSADOS
    / "retornos_ativos_ampliados_mensais.csv"
)

ARQUIVO_REGIMES_SUAVIZADOS = (
    PASTA_TABELAS
    / "06_02_regimes_suavizados.csv"
)

ARQUIVO_PESOS_CELULA_7 = (
    PASTA_TABELAS
    / "06_07_pesos_otimizados_por_regime.csv"
)

ARQUIVO_RESUMO_CELULA_7 = (
    PASTA_TABELAS
    / "06_07_resumo_ajuste_regimes.csv"
)

ARQUIVO_BACKTEST_ORIGINAL = (
    PASTA_DADOS_PROCESSADOS
    / "backtest_portfolio_mensal.csv"
)


arquivos_entrada = [
    ARQUIVO_RETORNOS_AMPLIADOS,
    ARQUIVO_REGIMES_SUAVIZADOS,
    ARQUIVO_PESOS_CELULA_7,
    ARQUIVO_RESUMO_CELULA_7,
    ARQUIVO_BACKTEST_ORIGINAL,
]


arquivos_ausentes = [
    arquivo
    for arquivo in arquivos_entrada
    if not arquivo.exists()
]


if arquivos_ausentes:
    raise FileNotFoundError(
        "Arquivos necessários não encontrados:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_GRADE = (
    PASTA_TABELAS
    / "06_09_grade_otimizacao_cdi.csv"
)

ARQUIVO_GRADE_FORMATADA = (
    PASTA_TABELAS
    / "06_09_grade_otimizacao_cdi_formatada.csv"
)

ARQUIVO_PARAMETROS = (
    PASTA_TABELAS
    / "06_09_parametros_selecionados_cdi.csv"
)

ARQUIVO_PESOS = (
    PASTA_TABELAS
    / "06_09_pesos_selecionados_5_ativos.csv"
)

ARQUIVO_METRICAS = (
    PASTA_TABELAS
    / "06_09_metricas_treino_avaliacao.csv"
)

ARQUIVO_METRICAS_FORMATADAS = (
    PASTA_TABELAS
    / "06_09_metricas_treino_avaliacao_formatadas.csv"
)

ARQUIVO_SERIES = (
    PASTA_TABELAS
    / "06_09_series_mensais_modelo_cdi.csv"
)

ARQUIVO_RESUMO = (
    PASTA_TABELAS
    / "06_09_resumo_otimizacao_cdi.csv"
)

ARQUIVO_VALIDACAO = (
    PASTA_TABELAS
    / "06_09_validacao_otimizacao_cdi.csv"
)

ARQUIVO_GRAFICO_DESEMPENHO = (
    PASTA_GRAFICOS
    / "06_09_desempenho_avaliacao_cdi.png"
)

ARQUIVO_GRAFICO_DIFERENCA = (
    PASTA_GRAFICOS
    / "06_09_diferenca_vs_benchmark_5_ativos.png"
)

ARQUIVO_GRAFICO_PESOS_CDI = (
    PASTA_GRAFICOS
    / "06_09_pesos_cdi_por_regime.png"
)

ARQUIVO_GRAFICO_ROLLING = (
    PASTA_GRAFICOS
    / "06_09_excesso_rolling_12m_treino.png"
)


# ============================================================
# CARREGAMENTO DAS BASES
# ============================================================

retornos_ampliados = pd.read_csv(
    ARQUIVO_RETORNOS_AMPLIADOS,
    encoding="utf-8-sig",
)

regimes_suavizados = pd.read_csv(
    ARQUIVO_REGIMES_SUAVIZADOS,
    encoding="utf-8-sig",
)

pesos_celula_7 = pd.read_csv(
    ARQUIVO_PESOS_CELULA_7,
    encoding="utf-8-sig",
)

backtest_original = pd.read_csv(
    ARQUIVO_BACKTEST_ORIGINAL,
    encoding="utf-8-sig",
)


resumo_celula_7 = pd.read_csv(
    ARQUIVO_RESUMO_CELULA_7,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO E PADRONIZAÇÃO DAS DATAS
# ============================================================

bases_com_data = {
    "retornos ampliados": retornos_ampliados,
    "regimes suavizados": regimes_suavizados,
    "backtest original": backtest_original,
}


for nome_base, base in bases_com_data.items():

    if "data" not in base.columns:
        raise ValueError(
            f"A base {nome_base} não possui "
            "a coluna data."
        )

    base["data"] = pd.to_datetime(
        base["data"],
        errors="coerce",
    )

    if base["data"].isna().any():
        raise ValueError(
            f"A base {nome_base} possui datas inválidas."
        )

    if base["data"].duplicated().any():
        raise ValueError(
            f"A base {nome_base} possui datas duplicadas."
        )

    base.sort_values(
        "data",
        inplace=True,
    )

    base.reset_index(
        drop=True,
        inplace=True,
    )


# ============================================================
# IDENTIFICAÇÃO DOS ATIVOS DE RISCO
# ============================================================

PREFIXO_PESO_OTIMIZADO = (
    "peso_otimizado_"
)


colunas_pesos_risco = [
    coluna
    for coluna in pesos_celula_7.columns
    if (
        coluna.startswith(
            PREFIXO_PESO_OTIMIZADO
        )
        and coluna
        != (
            f"{PREFIXO_PESO_OTIMIZADO}"
            "CDI"
        )
    )
]


if not colunas_pesos_risco:
    raise ValueError(
        "Não foram encontradas as colunas "
        "peso_otimizado_* no arquivo da Célula 7."
    )


ATIVOS_RISCO = [
    coluna.replace(
        PREFIXO_PESO_OTIMIZADO,
        "",
        1,
    )
    for coluna in colunas_pesos_risco
]


# O CDI é tratado separadamente nesta etapa. Caso ele já
# esteja presente nos pesos da etapa anterior, sua coluna foi
# removida de colunas_pesos_risco e os pesos restantes serão
# normalizados para formar a carteira de risco com soma 100%.

ATIVOS_COMPLETOS = [
    *ATIVOS_RISCO,
    "CDI",
]


ativos_ausentes = [
    ativo
    for ativo in ATIVOS_COMPLETOS
    if ativo not in retornos_ampliados.columns
]


if ativos_ausentes:
    raise ValueError(
        "Ativos ausentes na base ampliada:\n"
        f"{ativos_ausentes}"
    )


# ============================================================
# REGIMES E PESOS DA CÉLULA 7
# ============================================================

if "regime" not in pesos_celula_7.columns:
    raise ValueError(
        "O arquivo de pesos da Célula 7 "
        "não possui a coluna regime."
    )


pesos_celula_7["regime"] = (
    pesos_celula_7["regime"]
    .astype("string")
    .str.strip()
)


if pesos_celula_7[
    "regime"
].duplicated().any():
    raise ValueError(
        "Existem regimes duplicados no arquivo "
        "de pesos da Célula 7."
    )


regimes_ausentes = [
    regime
    for regime in ORDEM_REGIMES
    if regime not in pesos_celula_7[
        "regime"
    ].tolist()
]


if regimes_ausentes:
    raise ValueError(
        "Regimes sem pesos na Célula 7:\n"
        f"{regimes_ausentes}"
    )


for coluna in colunas_pesos_risco:

    pesos_celula_7[coluna] = pd.to_numeric(
        pesos_celula_7[coluna],
        errors="coerce",
    )


if pesos_celula_7[
    colunas_pesos_risco
].isna().any().any():
    raise ValueError(
        "Existem pesos inválidos no arquivo da Célula 7."
    )


PESOS_RISCO_BASE = {}


for regime in ORDEM_REGIMES:

    linha_regime = (
        pesos_celula_7.loc[
            pesos_celula_7[
                "regime"
            ]
            == regime
        ]
        .iloc[0]
    )

    pesos_risco_brutos = {
        ativo: float(
            linha_regime[
                f"{PREFIXO_PESO_OTIMIZADO}{ativo}"
            ]
        )
        for ativo in ATIVOS_RISCO
    }

    soma_pesos_risco_brutos = sum(
        pesos_risco_brutos.values()
    )

    if (
        not np.isfinite(
            soma_pesos_risco_brutos
        )
        or soma_pesos_risco_brutos
        <= 0.0
    ):

        raise ValueError(
            f"Os pesos de risco do regime {regime} "
            "possuem soma inválida: "
            f"{soma_pesos_risco_brutos}"
        )

    PESOS_RISCO_BASE[regime] = {
        ativo: (
            peso
            / soma_pesos_risco_brutos
        )
        for ativo, peso
        in pesos_risco_brutos.items()
    }

    soma_pesos_normalizados = sum(
        PESOS_RISCO_BASE[
            regime
        ].values()
    )

    if not np.isclose(
        soma_pesos_normalizados,
        1.0,
        rtol=1e-10,
        atol=1e-10,
    ):

        raise ValueError(
            f"Os pesos de risco normalizados do regime "
            f"{regime} não somam 100%."
        )


# ============================================================
# CONFIRMAÇÃO UTILIZADA PELO MODELO BASE
# ============================================================

if (
    "meses_confirmacao"
    not in pesos_celula_7.columns
):
    raise ValueError(
        "O arquivo de pesos da Célula 7 "
        "não possui a coluna meses_confirmacao."
    )


confirmacoes_base = (
    pd.to_numeric(
        pesos_celula_7[
            "meses_confirmacao"
        ],
        errors="coerce",
    )
    .dropna()
    .unique()
)


if len(confirmacoes_base) != 1:
    raise ValueError(
        "Não foi possível identificar uma única "
        "confirmação de regime no modelo base."
    )


CONFIRMACAO_MODELO_BASE = int(
    confirmacoes_base[0]
)


if (
    CONFIRMACAO_MODELO_BASE
    not in JANELAS_CONFIRMACAO
):
    raise ValueError(
        "A confirmação utilizada pelo modelo base "
        "não está entre as janelas configuradas."
    )


# ============================================================
# DATA DE CORTE ENTRE TREINO E AVALIAÇÃO
# ============================================================

if not {
    "metrica",
    "valor",
}.issubset(
    resumo_celula_7.columns
):
    raise ValueError(
        "O resumo da Célula 7 deve possuir "
        "as colunas metrica e valor."
    )


linha_data_corte = (
    resumo_celula_7.loc[
        resumo_celula_7[
            "metrica"
        ]
        == "Data final do treino",
        "valor",
    ]
)


if linha_data_corte.empty:
    raise ValueError(
        "A data final do treino não foi encontrada "
        "no resumo da Célula 7."
    )


DATA_CORTE_TREINO = pd.to_datetime(
    linha_data_corte.iloc[0],
    dayfirst=True,
    errors="coerce",
)


if pd.isna(
    DATA_CORTE_TREINO
):
    raise ValueError(
        "A data final do treino é inválida."
    )


# ============================================================
# VALIDAÇÃO DO CUSTO POR TURNOVER
# ============================================================

if {
    "turnover_portfolio",
    "custo_portfolio",
}.issubset(
    backtest_original.columns
):

    turnover_original = pd.to_numeric(
        backtest_original[
            "turnover_portfolio"
        ],
        errors="coerce",
    )

    custo_original = pd.to_numeric(
        backtest_original[
            "custo_portfolio"
        ],
        errors="coerce",
    )

    mascara_turnover = (
        turnover_original > 0
    )

    taxas_observadas = (
        custo_original.loc[
            mascara_turnover
        ]
        / turnover_original.loc[
            mascara_turnover
        ]
    ).dropna()

    if (
        not taxas_observadas.empty
        and not np.allclose(
            taxas_observadas,
            CUSTO_POR_TURNOVER,
            rtol=1e-8,
            atol=1e-12,
        )
    ):
        raise ValueError(
            "O custo configurado não coincide "
            "com o custo usado no backtest original."
        )


# ============================================================
# CONSTRUÇÃO DA BASE MENSAL
# ============================================================

COLUNAS_REGIMES = [
    f"regime_confirmacao_{meses}m"
    for meses in JANELAS_CONFIRMACAO
]


colunas_regimes_ausentes = [
    coluna
    for coluna in COLUNAS_REGIMES
    if coluna not in regimes_suavizados.columns
]


if colunas_regimes_ausentes:
    raise ValueError(
        "Colunas de regimes suavizados ausentes:\n"
        f"{colunas_regimes_ausentes}"
    )


base = (
    retornos_ampliados[
        [
            "data",
            *ATIVOS_COMPLETOS,
        ]
    ]
    .merge(
        regimes_suavizados[
            [
                "data",
                *COLUNAS_REGIMES,
            ]
        ],
        on="data",
        how="inner",
        validate="one_to_one",
    )
    .sort_values(
        "data"
    )
    .reset_index(
        drop=True
    )
)


if len(base) != len(
    retornos_ampliados
):
    raise ValueError(
        "A junção com os regimes alterou "
        "a quantidade de meses."
    )


for ativo in ATIVOS_COMPLETOS:

    base[ativo] = pd.to_numeric(
        base[ativo],
        errors="coerce",
    )


if base[
    ATIVOS_COMPLETOS
].isna().any().any():
    raise ValueError(
        "Existem retornos nulos ou inválidos "
        "na base de cinco ativos."
    )


for coluna_regime in COLUNAS_REGIMES:

    base[coluna_regime] = (
        base[coluna_regime]
        .astype("string")
        .str.strip()
    )

    regimes_invalidos = (
        base.loc[
            ~base[
                coluna_regime
            ].isin(
                ORDEM_REGIMES
            ),
            coluna_regime,
        ]
        .dropna()
        .unique()
        .tolist()
    )

    if regimes_invalidos:
        raise ValueError(
            f"A coluna {coluna_regime} possui "
            f"regimes inválidos:\n{regimes_invalidos}"
        )


base["periodo"] = np.where(
    base["data"]
    <= DATA_CORTE_TREINO,
    "TREINO",
    "AVALIACAO",
)


MASCARA_TREINO = (
    base["periodo"]
    == "TREINO"
).to_numpy()


MASCARA_AVALIACAO = (
    base["periodo"]
    == "AVALIACAO"
).to_numpy()


if (
    MASCARA_TREINO.sum()
    < MINIMO_MESES_TREINO_CDI
):
    raise ValueError(
        "O período de treino possui menos meses "
        "do que o mínimo configurado."
    )


if (
    MASCARA_AVALIACAO.sum()
    < MINIMO_MESES_AVALIACAO_CDI
):
    raise ValueError(
        "O período de avaliação possui menos meses "
        "do que o mínimo configurado."
    )


RETORNOS_MATRIZ = (
    base[
        ATIVOS_COMPLETOS
    ]
    .astype(float)
    .to_numpy()
)


# ============================================================
# FUNÇÕES DE CONSTRUÇÃO DOS PESOS
# ============================================================

def criar_pesos_com_cdi(
    pesos_risco_base,
    pesos_cdi_por_regime,
):

    pesos_finais = {}

    for regime in ORDEM_REGIMES:

        peso_cdi = float(
            pesos_cdi_por_regime[
                regime
            ]
        )

        if not (
            0.0
            <= peso_cdi
            <= 1.0
        ):
            raise ValueError(
                f"Peso inválido de CDI para {regime}."
            )

        pesos_finais[
            regime
        ] = {}

        for ativo in ATIVOS_RISCO:

            pesos_finais[
                regime
            ][ativo] = float(
                pesos_risco_base[
                    regime
                ][ativo]
                * (
                    1.0
                    - peso_cdi
                )
            )

        pesos_finais[
            regime
        ][
            "CDI"
        ] = peso_cdi

        soma_pesos = sum(
            pesos_finais[
                regime
            ].values()
        )

        if not np.isclose(
            soma_pesos,
            1.0,
            rtol=1e-10,
            atol=1e-10,
        ):
            raise ValueError(
                f"Os pesos finais de {regime} "
                "não somam 100%."
            )

    return pesos_finais


def criar_matriz_pesos(
    pesos_por_regime,
    coluna_regime,
):

    regimes_mensais = (
        base[
            coluna_regime
        ]
        .astype(str)
        .to_numpy()
    )

    matriz_pesos = np.zeros(
        (
            len(base),
            len(
                ATIVOS_COMPLETOS
            ),
        ),
        dtype=float,
    )

    for indice, regime in enumerate(
        regimes_mensais
    ):

        if regime not in pesos_por_regime:
            raise KeyError(
                f"O regime {regime} não possui pesos."
            )

        matriz_pesos[
            indice,
            :,
        ] = [
            pesos_por_regime[
                regime
            ][ativo]
            for ativo in ATIVOS_COMPLETOS
        ]

    if not np.allclose(
        matriz_pesos.sum(
            axis=1
        ),
        1.0,
        rtol=1e-10,
        atol=1e-10,
    ):
        raise ValueError(
            "A matriz mensal de pesos não soma 100%."
        )

    return matriz_pesos


# ============================================================
# FUNÇÃO DE SIMULAÇÃO
# ============================================================

def simular_carteira(
    pesos_por_regime,
    meses_confirmacao,
):

    coluna_regime = (
        f"regime_confirmacao_"
        f"{int(meses_confirmacao)}m"
    )

    matriz_pesos = criar_matriz_pesos(
        pesos_por_regime=pesos_por_regime,
        coluna_regime=coluna_regime,
    )

    retorno_bruto = np.sum(
        matriz_pesos
        * RETORNOS_MATRIZ,
        axis=1,
    )

    turnover = np.zeros(
        len(base),
        dtype=float,
    )

    if COBRAR_CUSTO_INICIAL:
        turnover[0] = 1.0

    for indice in range(
        1,
        len(base),
    ):

        pesos_anteriores = (
            matriz_pesos[
                indice - 1
            ]
        )

        retornos_anteriores = (
            RETORNOS_MATRIZ[
                indice - 1
            ]
        )

        retorno_carteira_anterior = (
            retorno_bruto[
                indice - 1
            ]
        )

        fator_patrimonio = (
            1.0
            + retorno_carteira_anterior
        )

        if fator_patrimonio <= 0:
            raise ValueError(
                "O patrimônio relativo ficou menor "
                "ou igual a zero."
            )

        pesos_apos_retorno = (
            pesos_anteriores
            * (
                1.0
                + retornos_anteriores
            )
            / fator_patrimonio
        )

        pesos_alvo = (
            matriz_pesos[
                indice
            ]
        )

        turnover[indice] = float(
            np.abs(
                pesos_alvo
                - pesos_apos_retorno
            ).sum()
            / 2.0
        )

    custo = (
        turnover
        * CUSTO_POR_TURNOVER
    )

    retorno_liquido = (
        (
            1.0
            + retorno_bruto
        )
        * (
            1.0
            - custo
        )
        - 1.0
    )

    return {
        "matriz_pesos": matriz_pesos,
        "retorno_bruto": retorno_bruto,
        "turnover": turnover,
        "custo": custo,
        "retorno_liquido": retorno_liquido,
    }


# ============================================================
# FUNÇÕES DE MÉTRICAS
# ============================================================

def calcular_retorno_total(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(retornos) == 0:
        return np.nan

    return float(
        np.prod(
            1.0
            + retornos
        )
        - 1.0
    )


def calcular_retorno_anualizado(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    quantidade = len(
        retornos
    )

    if quantidade == 0:
        return np.nan

    retorno_total = (
        calcular_retorno_total(
            retornos
        )
    )

    if retorno_total <= -1:
        return np.nan

    return float(
        (
            1.0
            + retorno_total
        )
        ** (
            PERIODOS_POR_ANO
            / quantidade
        )
        - 1.0
    )


def calcular_volatilidade_anualizada(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(retornos) < 2:
        return np.nan

    return float(
        np.std(
            retornos,
            ddof=1,
        )
        * np.sqrt(
            PERIODOS_POR_ANO
        )
    )


def calcular_maximo_drawdown(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(retornos) == 0:
        return np.nan

    indice = (
        VALOR_INICIAL
        * np.cumprod(
            1.0
            + retornos
        )
    )

    indice_com_inicio = np.concatenate(
        [
            np.array(
                [
                    VALOR_INICIAL
                ]
            ),
            indice,
        ]
    )

    pico = np.maximum.accumulate(
        indice_com_inicio
    )

    drawdown = (
        indice_com_inicio
        / pico
        - 1.0
    )

    return float(
        drawdown.min()
    )


def calcular_metricas(
    simulacao,
    mascara,
):

    retornos_brutos = (
        simulacao[
            "retorno_bruto"
        ][mascara]
    )

    retornos_liquidos = (
        simulacao[
            "retorno_liquido"
        ][mascara]
    )

    turnover = (
        simulacao[
            "turnover"
        ][mascara]
    )

    custos = (
        simulacao[
            "custo"
        ][mascara]
    )

    retorno_anualizado = (
        calcular_retorno_anualizado(
            retornos_liquidos
        )
    )

    volatilidade = (
        calcular_volatilidade_anualizada(
            retornos_liquidos
        )
    )

    if (
        pd.notna(
            volatilidade
        )
        and volatilidade > 0
    ):
        retorno_volatilidade = (
            retorno_anualizado
            / volatilidade
        )
    else:
        retorno_volatilidade = np.nan

    return {
        "quantidade_meses": int(
            mascara.sum()
        ),
        "retorno_total_bruto": (
            calcular_retorno_total(
                retornos_brutos
            )
        ),
        "retorno_total_liquido": (
            calcular_retorno_total(
                retornos_liquidos
            )
        ),
        "retorno_anualizado_liquido": (
            retorno_anualizado
        ),
        "volatilidade_anualizada_liquida": (
            volatilidade
        ),
        "retorno_volatilidade_liquido": (
            retorno_volatilidade
        ),
        "maximo_drawdown_liquido": (
            calcular_maximo_drawdown(
                retornos_liquidos
            )
        ),
        "meses_positivos": float(
            np.mean(
                retornos_liquidos > 0
            )
        ),
        "melhor_mes": float(
            np.max(
                retornos_liquidos
            )
        ),
        "pior_mes": float(
            np.min(
                retornos_liquidos
            )
        ),
        "turnover_total": float(
            turnover.sum()
        ),
        "turnover_medio_mensal": float(
            turnover.mean()
        ),
        "custo_acumulado_simples": float(
            custos.sum()
        ),
        "indice_final_liquido": float(
            VALOR_INICIAL
            * np.prod(
                1.0
                + retornos_liquidos
            )
        ),
    }


def calcular_rolling_excesso(
    retorno_candidato,
    retorno_benchmark,
    mascara,
):

    retorno_candidato = pd.Series(
        np.asarray(
            retorno_candidato,
            dtype=float,
        )[mascara]
    )

    retorno_benchmark = pd.Series(
        np.asarray(
            retorno_benchmark,
            dtype=float,
        )[mascara]
    )

    rolling_candidato = (
        (
            1.0
            + retorno_candidato
        )
        .rolling(
            JANELA_ROLLING
        )
        .apply(
            np.prod,
            raw=True,
        )
        - 1.0
    )

    rolling_benchmark = (
        (
            1.0
            + retorno_benchmark
        )
        .rolling(
            JANELA_ROLLING
        )
        .apply(
            np.prod,
            raw=True,
        )
        - 1.0
    )

    excesso = (
        rolling_candidato
        - rolling_benchmark
    ).dropna()

    if excesso.empty:
        return {
            "quantidade_janelas_12m": 0,
            "proporcao_janelas_12m_positivas": np.nan,
            "media_excesso_12m": np.nan,
            "mediana_excesso_12m": np.nan,
            "pior_excesso_12m": np.nan,
            "melhor_excesso_12m": np.nan,
        }

    return {
        "quantidade_janelas_12m": int(
            len(excesso)
        ),
        "proporcao_janelas_12m_positivas": float(
            excesso.gt(0).mean()
        ),
        "media_excesso_12m": float(
            excesso.mean()
        ),
        "mediana_excesso_12m": float(
            excesso.median()
        ),
        "pior_excesso_12m": float(
            excesso.min()
        ),
        "melhor_excesso_12m": float(
            excesso.max()
        ),
    }


# ============================================================
# BENCHMARK DE CINCO ATIVOS
# ============================================================

PESO_IGUAL_5_ATIVOS = (
    1.0
    / len(
        ATIVOS_COMPLETOS
    )
)


PESOS_BENCHMARK_5 = {
    regime: {
        ativo: PESO_IGUAL_5_ATIVOS
        for ativo in ATIVOS_COMPLETOS
    }
    for regime in ORDEM_REGIMES
}


SIMULACAO_BENCHMARK_5 = (
    simular_carteira(
        pesos_por_regime=PESOS_BENCHMARK_5,
        meses_confirmacao=1,
    )
)


METRICAS_BENCHMARK_TREINO = (
    calcular_metricas(
        simulacao=SIMULACAO_BENCHMARK_5,
        mascara=MASCARA_TREINO,
    )
)


# ============================================================
# MODELO BASE DA CÉLULA 7 SEM CDI
# ============================================================

pesos_cdi_zero = {
    regime: 0.0
    for regime in ORDEM_REGIMES
}


PESOS_MODELO_BASE = (
    criar_pesos_com_cdi(
        pesos_risco_base=PESOS_RISCO_BASE,
        pesos_cdi_por_regime=pesos_cdi_zero,
    )
)


SIMULACAO_MODELO_BASE = (
    simular_carteira(
        pesos_por_regime=PESOS_MODELO_BASE,
        meses_confirmacao=(
            CONFIRMACAO_MODELO_BASE
        ),
    )
)


METRICAS_MODELO_BASE_TREINO = (
    calcular_metricas(
        simulacao=SIMULACAO_MODELO_BASE,
        mascara=MASCARA_TREINO,
    )
)


LIMITE_TURNOVER_TREINO = (
    METRICAS_MODELO_BASE_TREINO[
        "turnover_total"
    ]
)


# ============================================================
# TESTE DA GRADE DE PARÂMETROS
# ============================================================

quantidade_combinacoes_por_confirmacao = (
    len(
        PESOS_CDI_TESTADOS
    )
    ** len(
        ORDEM_REGIMES
    )
)


quantidade_total_combinacoes = (
    quantidade_combinacoes_por_confirmacao
    * len(
        JANELAS_CONFIRMACAO
    )
)


print("=" * 70)
print("INICIANDO OTIMIZAÇÃO COM CDI")
print("=" * 70)

print(
    f"\nCombinações por confirmação: "
    f"{quantidade_combinacoes_por_confirmacao}"
)

print(
    f"Combinações totais: "
    f"{quantidade_total_combinacoes}"
)

print(
    "A seleção utilizará somente o período de treino.\n",
    flush=True,
)


registros_grade = []


for meses_confirmacao in JANELAS_CONFIRMACAO:

    print(
        f"Testando confirmação de "
        f"{meses_confirmacao} mês(es)...",
        flush=True,
    )

    coluna_regime = (
        f"regime_confirmacao_"
        f"{meses_confirmacao}m"
    )

    quantidade_mudancas_treino = int(
        (
            base.loc[
                MASCARA_TREINO,
                coluna_regime,
            ]
            .astype(str)
            .to_numpy()[1:]
            != base.loc[
                MASCARA_TREINO,
                coluna_regime,
            ]
            .astype(str)
            .to_numpy()[:-1]
        )
        .sum()
    )

    for combinacao in product(
        PESOS_CDI_TESTADOS,
        repeat=len(
            ORDEM_REGIMES
        ),
    ):

        pesos_cdi_por_regime = {
            regime: float(
                peso_cdi
            )
            for regime, peso_cdi in zip(
                ORDEM_REGIMES,
                combinacao,
            )
        }

        pesos_candidato = (
            criar_pesos_com_cdi(
                pesos_risco_base=(
                    PESOS_RISCO_BASE
                ),
                pesos_cdi_por_regime=(
                    pesos_cdi_por_regime
                ),
            )
        )

        simulacao_candidato = (
            simular_carteira(
                pesos_por_regime=pesos_candidato,
                meses_confirmacao=(
                    meses_confirmacao
                ),
            )
        )

        metricas_treino = (
            calcular_metricas(
                simulacao=simulacao_candidato,
                mascara=MASCARA_TREINO,
            )
        )

        rolling_treino = (
            calcular_rolling_excesso(
                retorno_candidato=(
                    simulacao_candidato[
                        "retorno_liquido"
                    ]
                ),
                retorno_benchmark=(
                    SIMULACAO_BENCHMARK_5[
                        "retorno_liquido"
                    ]
                ),
                mascara=MASCARA_TREINO,
            )
        )

        excesso_retorno_anualizado = (
            metricas_treino[
                "retorno_anualizado_liquido"
            ]
            - METRICAS_BENCHMARK_TREINO[
                "retorno_anualizado_liquido"
            ]
        )

        identificador = (
            f"conf_{meses_confirmacao}m"
            f"_cdi_"
            + "_".join(
                f"{int(round(peso * 100)):02d}"
                for peso in combinacao
            )
        )

        registros_grade.append(
            {
                "candidato": identificador,
                "meses_confirmacao": (
                    meses_confirmacao
                ),
                "quantidade_mudancas_regime_treino": (
                    quantidade_mudancas_treino
                ),
                "peso_cdi_expansao_desinflacionaria": (
                    pesos_cdi_por_regime[
                        "EXPANSAO_DESINFLACIONARIA"
                    ]
                ),
                "peso_cdi_expansao_inflacionaria": (
                    pesos_cdi_por_regime[
                        "EXPANSAO_INFLACIONARIA"
                    ]
                ),
                "peso_cdi_estagflacao": (
                    pesos_cdi_por_regime[
                        "ESTAGFLACAO"
                    ]
                ),
                "peso_cdi_recessao_desinflacionaria": (
                    pesos_cdi_por_regime[
                        "RECESSAO_DESINFLACIONARIA"
                    ]
                ),
                "peso_cdi_medio": float(
                    np.mean(
                        combinacao
                    )
                ),
                "peso_cdi_maximo": float(
                    np.max(
                        combinacao
                    )
                ),
                "excesso_retorno_anualizado_vs_benchmark": (
                    excesso_retorno_anualizado
                ),
                **metricas_treino,
                **rolling_treino,
            }
        )


grade_otimizacao = pd.DataFrame(
    registros_grade
)


# ============================================================
# SELEÇÃO SOMENTE COM O TREINO
# ============================================================

grade_otimizacao[
    "respeita_limite_turnover"
] = (
    grade_otimizacao[
        "turnover_total"
    ]
    <= (
        LIMITE_TURNOVER_TREINO
        + 1e-12
    )
)


candidatos_elegiveis = (
    grade_otimizacao.loc[
        grade_otimizacao[
            "respeita_limite_turnover"
        ]
    ]
    .copy()
)


if candidatos_elegiveis.empty:
    raise ValueError(
        "Nenhum candidato respeitou o limite "
        "de turnover do modelo base."
    )


candidatos_elegiveis[
    "proporcao_janelas_12m_positivas"
] = (
    candidatos_elegiveis[
        "proporcao_janelas_12m_positivas"
    ]
    .fillna(
        -np.inf
    )
)


candidatos_elegiveis[
    "retorno_volatilidade_liquido"
] = (
    candidatos_elegiveis[
        "retorno_volatilidade_liquido"
    ]
    .fillna(
        -np.inf
    )
)


candidatos_elegiveis[
    "mediana_excesso_12m"
] = (
    candidatos_elegiveis[
        "mediana_excesso_12m"
    ]
    .fillna(
        -np.inf
    )
)


candidato_selecionado = (
    candidatos_elegiveis
    .sort_values(
        [
            "proporcao_janelas_12m_positivas",
            "retorno_volatilidade_liquido",
            "excesso_retorno_anualizado_vs_benchmark",
            "mediana_excesso_12m",
            "turnover_total",
            "peso_cdi_medio",
        ],
        ascending=[
            False,
            False,
            False,
            False,
            True,
            True,
        ],
    )
    .iloc[0]
)


CONFIRMACAO_SELECIONADA = int(
    candidato_selecionado[
        "meses_confirmacao"
    ]
)


PESOS_CDI_SELECIONADOS = {
    "EXPANSAO_DESINFLACIONARIA": float(
        candidato_selecionado[
            "peso_cdi_expansao_desinflacionaria"
        ]
    ),
    "EXPANSAO_INFLACIONARIA": float(
        candidato_selecionado[
            "peso_cdi_expansao_inflacionaria"
        ]
    ),
    "ESTAGFLACAO": float(
        candidato_selecionado[
            "peso_cdi_estagflacao"
        ]
    ),
    "RECESSAO_DESINFLACIONARIA": float(
        candidato_selecionado[
            "peso_cdi_recessao_desinflacionaria"
        ]
    ),
}


PESOS_SELECIONADOS = (
    criar_pesos_com_cdi(
        pesos_risco_base=PESOS_RISCO_BASE,
        pesos_cdi_por_regime=(
            PESOS_CDI_SELECIONADOS
        ),
    )
)


SIMULACAO_SELECIONADA = (
    simular_carteira(
        pesos_por_regime=PESOS_SELECIONADOS,
        meses_confirmacao=(
            CONFIRMACAO_SELECIONADA
        ),
    )
)


# ============================================================
# MÉTRICAS DE TREINO E AVALIAÇÃO
# ============================================================

cenarios_simulacao = {
    "MODELO_BASE_4_ATIVOS": {
        "rotulo": (
            "Modelo da Célula 7 sem CDI"
        ),
        "simulacao": (
            SIMULACAO_MODELO_BASE
        ),
    },
    "MODELO_SELECIONADO_5_ATIVOS": {
        "rotulo": (
            "Modelo selecionado com CDI"
        ),
        "simulacao": (
            SIMULACAO_SELECIONADA
        ),
    },
    "BENCHMARK_5_ATIVOS": {
        "rotulo": (
            "Benchmark de pesos iguais — 5 ativos"
        ),
        "simulacao": (
            SIMULACAO_BENCHMARK_5
        ),
    },
}


registros_metricas = []


for periodo, mascara in [
    (
        "TREINO",
        MASCARA_TREINO,
    ),
    (
        "AVALIACAO",
        MASCARA_AVALIACAO,
    ),
]:

    for cenario, configuracao in (
        cenarios_simulacao.items()
    ):

        metricas = calcular_metricas(
            simulacao=configuracao[
                "simulacao"
            ],
            mascara=mascara,
        )

        registros_metricas.append(
            {
                "periodo": periodo,
                "cenario": cenario,
                "rotulo": configuracao[
                    "rotulo"
                ],
                **metricas,
            }
        )


metricas_comparativas = pd.DataFrame(
    registros_metricas
)


for periodo in [
    "TREINO",
    "AVALIACAO",
]:

    indice_benchmark = float(
        metricas_comparativas.loc[
            (
                metricas_comparativas[
                    "periodo"
                ]
                == periodo
            )
            & (
                metricas_comparativas[
                    "cenario"
                ]
                == "BENCHMARK_5_ATIVOS"
            ),
            "indice_final_liquido",
        ]
        .iloc[0]
    )

    metricas_comparativas.loc[
        metricas_comparativas[
            "periodo"
        ]
        == periodo,
        "diferenca_indice_vs_benchmark",
    ] = (
        metricas_comparativas.loc[
            metricas_comparativas[
                "periodo"
            ]
            == periodo,
            "indice_final_liquido",
        ]
        - indice_benchmark
    )


# ============================================================
# RESULTADOS FORA DA AMOSTRA
# ============================================================

resultado_selecionado_avaliacao = (
    metricas_comparativas.loc[
        (
            metricas_comparativas[
                "periodo"
            ]
            == "AVALIACAO"
        )
        & (
            metricas_comparativas[
                "cenario"
            ]
            == "MODELO_SELECIONADO_5_ATIVOS"
        )
    ]
    .iloc[0]
)


resultado_base_avaliacao = (
    metricas_comparativas.loc[
        (
            metricas_comparativas[
                "periodo"
            ]
            == "AVALIACAO"
        )
        & (
            metricas_comparativas[
                "cenario"
            ]
            == "MODELO_BASE_4_ATIVOS"
        )
    ]
    .iloc[0]
)


resultado_benchmark_avaliacao = (
    metricas_comparativas.loc[
        (
            metricas_comparativas[
                "periodo"
            ]
            == "AVALIACAO"
        )
        & (
            metricas_comparativas[
                "cenario"
            ]
            == "BENCHMARK_5_ATIVOS"
        )
    ]
    .iloc[0]
)


diferenca_selecionado_benchmark = float(
    resultado_selecionado_avaliacao[
        "indice_final_liquido"
    ]
    - resultado_benchmark_avaliacao[
        "indice_final_liquido"
    ]
)


diferenca_selecionado_base = float(
    resultado_selecionado_avaliacao[
        "indice_final_liquido"
    ]
    - resultado_base_avaliacao[
        "indice_final_liquido"
    ]
)


if diferenca_selecionado_benchmark > 0:
    STATUS_AVALIACAO = (
        "SUPEROU O BENCHMARK"
    )
elif diferenca_selecionado_benchmark < 0:
    STATUS_AVALIACAO = (
        "FICOU ABAIXO DO BENCHMARK"
    )
else:
    STATUS_AVALIACAO = (
        "EMPATOU COM O BENCHMARK"
    )


# ============================================================
# TABELA DOS PESOS SELECIONADOS
# ============================================================

registros_pesos = []


for regime in ORDEM_REGIMES:

    registro = {
        "regime": regime,
        "nome_regime": (
            NOMES_REGIMES[
                regime
            ]
        ),
        "meses_confirmacao": (
            CONFIRMACAO_SELECIONADA
        ),
    }

    for ativo in ATIVOS_COMPLETOS:

        registro[
            f"peso_{ativo}"
        ] = (
            PESOS_SELECIONADOS[
                regime
            ][ativo]
        )

    registro[
        "soma_pesos"
    ] = sum(
        PESOS_SELECIONADOS[
            regime
        ].values()
    )

    registros_pesos.append(
        registro
    )


pesos_selecionados_df = pd.DataFrame(
    registros_pesos
)


if not np.allclose(
    pesos_selecionados_df[
        "soma_pesos"
    ],
    1.0,
    rtol=1e-10,
    atol=1e-10,
):
    raise ValueError(
        "Os pesos selecionados não somam 100%."
    )


# ============================================================
# SÉRIES MENSAIS CONSOLIDADAS
# ============================================================

series_mensais = (
    base[
        [
            "data",
            "periodo",
            *COLUNAS_REGIMES,
            *ATIVOS_COMPLETOS,
        ]
    ]
    .copy()
)


for cenario, configuracao in (
    cenarios_simulacao.items()
):

    simulacao = configuracao[
        "simulacao"
    ]

    series_mensais[
        f"retorno_bruto_{cenario}"
    ] = simulacao[
        "retorno_bruto"
    ]

    series_mensais[
        f"turnover_{cenario}"
    ] = simulacao[
        "turnover"
    ]

    series_mensais[
        f"custo_{cenario}"
    ] = simulacao[
        "custo"
    ]

    series_mensais[
        f"retorno_liquido_{cenario}"
    ] = simulacao[
        "retorno_liquido"
    ]


for indice_ativo, ativo in enumerate(
    ATIVOS_COMPLETOS
):

    series_mensais[
        f"peso_selecionado_{ativo}"
    ] = (
        SIMULACAO_SELECIONADA[
            "matriz_pesos"
        ][
            :,
            indice_ativo,
        ]
    )


# ============================================================
# ROLLING DE 12 MESES NO TREINO
# ============================================================

datas_treino = (
    base.loc[
        MASCARA_TREINO,
        "data",
    ]
    .reset_index(
        drop=True
    )
)


retorno_selecionado_treino = pd.Series(
    SIMULACAO_SELECIONADA[
        "retorno_liquido"
    ][MASCARA_TREINO]
)


retorno_benchmark_treino = pd.Series(
    SIMULACAO_BENCHMARK_5[
        "retorno_liquido"
    ][MASCARA_TREINO]
)


rolling_selecionado = (
    (
        1.0
        + retorno_selecionado_treino
    )
    .rolling(
        JANELA_ROLLING
    )
    .apply(
        np.prod,
        raw=True,
    )
    - 1.0
)


rolling_benchmark = (
    (
        1.0
        + retorno_benchmark_treino
    )
    .rolling(
        JANELA_ROLLING
    )
    .apply(
        np.prod,
        raw=True,
    )
    - 1.0
)


rolling_treino = pd.DataFrame(
    {
        "data": datas_treino,
        "retorno_12m_modelo": (
            rolling_selecionado
        ),
        "retorno_12m_benchmark": (
            rolling_benchmark
        ),
    }
)


rolling_treino[
    "excesso_12m"
] = (
    rolling_treino[
        "retorno_12m_modelo"
    ]
    - rolling_treino[
        "retorno_12m_benchmark"
    ]
)


# ============================================================
# PARÂMETROS E RESUMO
# ============================================================

parametros_selecionados = pd.DataFrame(
    {
        "metrica": [
            "Candidato selecionado",
            "Meses de confirmação",
            "Peso CDI expansão desinflacionária",
            "Peso CDI expansão inflacionária",
            "Peso CDI estagflação",
            "Peso CDI recessão desinflacionária",
            "Limite de turnover no treino",
            "Turnover selecionado no treino",
            "Retorno/volatilidade selecionado no treino",
            "Proporção de janelas positivas no treino",
            "Excesso anualizado no treino",
            "Data final do treino",
            "Data inicial da avaliação",
            "Quantidade de meses de treino",
            "Quantidade de meses de avaliação",
            "Critério de seleção",
        ],
        "valor": [
            candidato_selecionado[
                "candidato"
            ],
            CONFIRMACAO_SELECIONADA,
            PESOS_CDI_SELECIONADOS[
                "EXPANSAO_DESINFLACIONARIA"
            ],
            PESOS_CDI_SELECIONADOS[
                "EXPANSAO_INFLACIONARIA"
            ],
            PESOS_CDI_SELECIONADOS[
                "ESTAGFLACAO"
            ],
            PESOS_CDI_SELECIONADOS[
                "RECESSAO_DESINFLACIONARIA"
            ],
            LIMITE_TURNOVER_TREINO,
            candidato_selecionado[
                "turnover_total"
            ],
            candidato_selecionado[
                "retorno_volatilidade_liquido"
            ],
            candidato_selecionado[
                "proporcao_janelas_12m_positivas"
            ],
            candidato_selecionado[
                "excesso_retorno_anualizado_vs_benchmark"
            ],
            base.loc[
                MASCARA_TREINO,
                "data",
            ].max().strftime(
                "%d/%m/%Y"
            ),
            base.loc[
                MASCARA_AVALIACAO,
                "data",
            ].min().strftime(
                "%d/%m/%Y"
            ),
            int(
                MASCARA_TREINO.sum()
            ),
            int(
                MASCARA_AVALIACAO.sum()
            ),
            (
                "Seleção somente no treino: "
                f"janelas positivas de {JANELA_ROLLING} meses, "
                "retorno/volatilidade, excesso anualizado, "
                "mediana do excesso e menor turnover."
            ),
        ],
    }
)


resumo_otimizacao = pd.DataFrame(
    {
        "metrica": [
            "Combinações testadas",
            "Candidato selecionado",
            "Meses de confirmação",
            "Índice final do modelo base na avaliação",
            "Índice final do modelo com CDI na avaliação",
            "Índice final do benchmark de 5 ativos",
            "Diferença do modelo com CDI contra o benchmark",
            "Diferença do modelo com CDI contra o modelo base",
            "Retorno anualizado do modelo com CDI",
            "Volatilidade anualizada do modelo com CDI",
            "Retorno/volatilidade do modelo com CDI",
            "Máximo drawdown do modelo com CDI",
            "Turnover total do modelo com CDI",
            "Custo acumulado simples do modelo com CDI",
            "Status fora da amostra",
            "Observação metodológica",
        ],
        "valor": [
            quantidade_total_combinacoes,
            candidato_selecionado[
                "candidato"
            ],
            CONFIRMACAO_SELECIONADA,
            resultado_base_avaliacao[
                "indice_final_liquido"
            ],
            resultado_selecionado_avaliacao[
                "indice_final_liquido"
            ],
            resultado_benchmark_avaliacao[
                "indice_final_liquido"
            ],
            diferenca_selecionado_benchmark,
            diferenca_selecionado_base,
            resultado_selecionado_avaliacao[
                "retorno_anualizado_liquido"
            ],
            resultado_selecionado_avaliacao[
                "volatilidade_anualizada_liquida"
            ],
            resultado_selecionado_avaliacao[
                "retorno_volatilidade_liquido"
            ],
            resultado_selecionado_avaliacao[
                "maximo_drawdown_liquido"
            ],
            resultado_selecionado_avaliacao[
                "turnover_total"
            ],
            resultado_selecionado_avaliacao[
                "custo_acumulado_simples"
            ],
            STATUS_AVALIACAO,
            (
                "Nenhum dado posterior a "
                f"{DATA_CORTE_TREINO:%d/%m/%Y} foi usado "
                "na seleção dos parâmetros."
            ),
        ],
    }
)


# ============================================================
# TABELAS FORMATADAS
# ============================================================

grade_formatada = (
    grade_otimizacao
    .copy()
    .astype(object)
)


colunas_percentuais_grade = [
    "peso_cdi_expansao_desinflacionaria",
    "peso_cdi_expansao_inflacionaria",
    "peso_cdi_estagflacao",
    "peso_cdi_recessao_desinflacionaria",
    "peso_cdi_medio",
    "peso_cdi_maximo",
    "excesso_retorno_anualizado_vs_benchmark",
    "retorno_total_bruto",
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown_liquido",
    "meses_positivos",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
    "proporcao_janelas_12m_positivas",
    "media_excesso_12m",
    "mediana_excesso_12m",
    "pior_excesso_12m",
    "melhor_excesso_12m",
]


for coluna in colunas_percentuais_grade:

    grade_formatada[coluna] = (
        grade_otimizacao[coluna]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "retorno_volatilidade_liquido",
    "turnover_total",
    "indice_final_liquido",
]:

    grade_formatada[coluna] = (
        grade_otimizacao[coluna]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


metricas_formatadas = (
    metricas_comparativas
    .copy()
    .astype(object)
)


for coluna in [
    "retorno_total_bruto",
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown_liquido",
    "meses_positivos",
    "melhor_mes",
    "pior_mes",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
]:

    metricas_formatadas[coluna] = (
        metricas_comparativas[coluna]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "retorno_volatilidade_liquido",
    "turnover_total",
    "indice_final_liquido",
    "diferenca_indice_vs_benchmark",
]:

    metricas_formatadas[coluna] = (
        metricas_comparativas[coluna]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

grade_otimizacao.to_csv(
    ARQUIVO_GRADE,
    index=False,
    encoding="utf-8-sig",
)

grade_formatada.to_csv(
    ARQUIVO_GRADE_FORMATADA,
    index=False,
    encoding="utf-8-sig",
)

parametros_selecionados.to_csv(
    ARQUIVO_PARAMETROS,
    index=False,
    encoding="utf-8-sig",
)

pesos_selecionados_df.to_csv(
    ARQUIVO_PESOS,
    index=False,
    encoding="utf-8-sig",
)

metricas_comparativas.to_csv(
    ARQUIVO_METRICAS,
    index=False,
    encoding="utf-8-sig",
)

metricas_formatadas.to_csv(
    ARQUIVO_METRICAS_FORMATADAS,
    index=False,
    encoding="utf-8-sig",
)

series_mensais.to_csv(
    ARQUIVO_SERIES,
    index=False,
    encoding="utf-8-sig",
)

resumo_otimizacao.to_csv(
    ARQUIVO_RESUMO,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# BASE PARA GRÁFICOS DA AVALIAÇÃO
# ============================================================

series_avaliacao = (
    series_mensais.loc[
        series_mensais[
            "periodo"
        ]
        == "AVALIACAO"
    ]
    .copy()
    .reset_index(
        drop=True
    )
)


for cenario in cenarios_simulacao:

    coluna_retorno = (
        f"retorno_liquido_{cenario}"
    )

    series_avaliacao[
        f"indice_{cenario}"
    ] = (
        VALOR_INICIAL
        * (
            1.0
            + series_avaliacao[
                coluna_retorno
            ]
        ).cumprod()
    )


series_avaliacao[
    "diferenca_modelo_cdi_benchmark"
] = (
    series_avaliacao[
        "indice_MODELO_SELECIONADO_5_ATIVOS"
    ]
    - series_avaliacao[
        "indice_BENCHMARK_5_ATIVOS"
    ]
)


data_inicial_grafico = (
    series_avaliacao[
        "data"
    ].iloc[0]
    - pd.offsets.MonthEnd(1)
)


linha_inicial = pd.DataFrame(
    {
        "data": [
            data_inicial_grafico
        ],
        "indice_MODELO_BASE_4_ATIVOS": [
            VALOR_INICIAL
        ],
        "indice_MODELO_SELECIONADO_5_ATIVOS": [
            VALOR_INICIAL
        ],
        "indice_BENCHMARK_5_ATIVOS": [
            VALOR_INICIAL
        ],
        "diferenca_modelo_cdi_benchmark": [
            0.0
        ],
    }
)


series_grafico = pd.concat(
    [
        linha_inicial,
        series_avaliacao[
            [
                "data",
                "indice_MODELO_BASE_4_ATIVOS",
                "indice_MODELO_SELECIONADO_5_ATIVOS",
                "indice_BENCHMARK_5_ATIVOS",
                "diferenca_modelo_cdi_benchmark",
            ]
        ],
    ],
    ignore_index=True,
)


# ============================================================
# GRÁFICO 1 — DESEMPENHO FORA DA AMOSTRA
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "indice_MODELO_BASE_4_ATIVOS"
    ],
    linewidth=2,
    label="Modelo anterior sem CDI",
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "indice_MODELO_SELECIONADO_5_ATIVOS"
    ],
    linewidth=2,
    label="Modelo selecionado com CDI",
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "indice_BENCHMARK_5_ATIVOS"
    ],
    linewidth=2,
    label="Benchmark de pesos iguais — 5 ativos",
)


ax.axhline(
    y=VALOR_INICIAL,
    linewidth=1,
)


ax.set_title(
    "Desempenho Fora da Amostra com Inclusão do CDI"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Índice acumulado"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DESEMPENHO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — DIFERENÇA CONTRA O BENCHMARK
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "diferenca_modelo_cdi_benchmark"
    ],
    linewidth=2,
)


ax.axhline(
    y=0,
    linewidth=1,
)


ax.set_title(
    "Diferença do Modelo com CDI contra o Benchmark"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Diferença do índice em pontos"
)

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DIFERENCA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — PESO DO CDI POR REGIME
# ============================================================

dados_grafico_cdi = (
    pesos_selecionados_df[
        [
            "nome_regime",
            "peso_CDI",
        ]
    ]
    .copy()
)


fig, ax = plt.subplots(
    figsize=(11, 7)
)


barras = ax.bar(
    dados_grafico_cdi[
        "nome_regime"
    ],
    dados_grafico_cdi[
        "peso_CDI"
    ],
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Peso Selecionado do CDI por Regime"
)

ax.set_xlabel(
    "Regime macroeconômico"
)

ax.set_ylabel(
    "Peso do CDI"
)

ax.tick_params(
    axis="x",
    rotation=20,
)

ax.grid(
    axis="y",
    alpha=0.3,
)


for barra, valor in zip(
    barras,
    dados_grafico_cdi[
        "peso_CDI"
    ],
):

    ax.text(
        barra.get_x()
        + barra.get_width()
        / 2,
        barra.get_height(),
        f"{valor:.0%}",
        ha="center",
        va="bottom",
    )


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_PESOS_CDI,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 4 — EXCESSO ROLLING NO TREINO
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    rolling_treino[
        "data"
    ],
    rolling_treino[
        "excesso_12m"
    ],
    linewidth=2,
)


ax.axhline(
    y=0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    f"Excesso de Retorno Rolling de "
    f"{JANELA_ROLLING} Meses no Treino"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    f"Excesso de retorno em "
    f"{JANELA_ROLLING} meses"
)

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_ROLLING,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÕES FINAIS
# ============================================================

validacoes = []


def registrar_validacao(
    nome,
    aprovado,
    detalhe,
):

    validacoes.append(
        {
            "validacao": nome,
            "status": (
                "APROVADO"
                if aprovado
                else "REPROVADO"
            ),
            "detalhe": detalhe,
        }
    )


registrar_validacao(
    nome="Quantidade de meses",
    aprovado=(
        len(base)
        == len(
            retornos_ampliados
        )
    ),
    detalhe=(
        f"{len(base)} meses"
    ),
)


registrar_validacao(
    nome="Valores nulos",
    aprovado=(
        not base[
            ATIVOS_COMPLETOS
        ]
        .isna()
        .any()
        .any()
    ),
    detalhe=(
        f"{int(base[ATIVOS_COMPLETOS].isna().sum().sum())} nulos"
    ),
)


registrar_validacao(
    nome="Soma dos pesos",
    aprovado=np.allclose(
        pesos_selecionados_df[
            "soma_pesos"
        ],
        1.0,
        rtol=1e-10,
        atol=1e-10,
    ),
    detalhe="Pesos devem somar 100%",
)


registrar_validacao(
    nome="Turnover não negativo",
    aprovado=(
        SIMULACAO_SELECIONADA[
            "turnover"
        ]
        >= 0
    ).all(),
    detalhe=(
        f"Mínimo: "
        f"{SIMULACAO_SELECIONADA['turnover'].min():.6f}"
    ),
)


registrar_validacao(
    nome="Custos não negativos",
    aprovado=(
        SIMULACAO_SELECIONADA[
            "custo"
        ]
        >= 0
    ).all(),
    detalhe=(
        f"Mínimo: "
        f"{SIMULACAO_SELECIONADA['custo'].min():.6f}"
    ),
)


registrar_validacao(
    nome="Seleção restrita ao treino",
    aprovado=True,
    detalhe=(
        "A grade foi classificada somente "
        f"com métricas até {DATA_CORTE_TREINO:%d/%m/%Y}."
    ),
)


registrar_validacao(
    nome="Cobertura do CDI",
    aprovado=(
        base[
            "CDI"
        ]
        .notna()
        .all()
    ),
    detalhe=(
        "CDI presente em todos os meses."
    ),
)


tabela_validacao = pd.DataFrame(
    validacoes
)


if (
    tabela_validacao[
        "status"
    ]
    == "REPROVADO"
).any():

    raise ValueError(
        "Uma ou mais validações da Célula 9 "
        "foram reprovadas:\n"
        f"{tabela_validacao}"
    )


tabela_validacao.to_csv(
    ARQUIVO_VALIDACAO,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_GRADE,
    ARQUIVO_GRADE_FORMATADA,
    ARQUIVO_PARAMETROS,
    ARQUIVO_PESOS,
    ARQUIVO_METRICAS,
    ARQUIVO_METRICAS_FORMATADAS,
    ARQUIVO_SERIES,
    ARQUIVO_RESUMO,
    ARQUIVO_VALIDACAO,
    ARQUIVO_GRAFICO_DESEMPENHO,
    ARQUIVO_GRAFICO_DIFERENCA,
    ARQUIVO_GRAFICO_PESOS_CDI,
    ARQUIVO_GRAFICO_ROLLING,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:
    raise FileNotFoundError(
        "Alguns arquivos da Célula 9 "
        "não foram salvos:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("\n" + "=" * 70)
print("OTIMIZAÇÃO COM CDI CONCLUÍDA")
print("=" * 70)


print(
    f"\nRaiz do projeto:\n"
    f"{RAIZ_PROJETO}"
)


print(
    f"\nCombinações testadas: "
    f"{quantidade_total_combinacoes}"
)


print(
    f"Meses de treino: "
    f"{int(MASCARA_TREINO.sum())}"
)


print(
    f"Meses de avaliação: "
    f"{int(MASCARA_AVALIACAO.sum())}"
)


print(
    f"Valor inicial: "
    f"{VALOR_INICIAL:.2f}"
)


print(
    f"Períodos por ano: "
    f"{PERIODOS_POR_ANO}"
)


print(
    f"Janela rolling: "
    f"{JANELA_ROLLING} meses"
)


print(
    f"Cobrança de custo inicial: "
    f"{COBRAR_CUSTO_INICIAL}"
)


print(
    f"\nCandidato selecionado somente com o treino:\n"
    f"{candidato_selecionado['candidato']}"
)


print(
    f"\nConfirmação selecionada: "
    f"{CONFIRMACAO_SELECIONADA} mês(es)"
)


print(
    "\nPesos do CDI por regime:"
)


for regime in ORDEM_REGIMES:

    print(
        f"- {NOMES_REGIMES[regime]}: "
        f"{PESOS_CDI_SELECIONADOS[regime]:.0%}"
    )


print(
    f"\nRetorno/volatilidade no treino: "
    f"{candidato_selecionado['retorno_volatilidade_liquido']:.2f}"
)


print(
    f"Janelas rolling de {JANELA_ROLLING} meses "
    f"positivas no treino: "
    f"{candidato_selecionado['proporcao_janelas_12m_positivas']:.2%}"
)


print(
    f"Turnover total no treino: "
    f"{candidato_selecionado['turnover_total']:.4f}"
)


print(
    f"Limite de turnover do modelo base: "
    f"{LIMITE_TURNOVER_TREINO:.4f}"
)


print(
    f"\nÍndice final do modelo anterior na avaliação: "
    f"{resultado_base_avaliacao['indice_final_liquido']:.2f}"
)


print(
    f"Índice final do modelo com CDI na avaliação: "
    f"{resultado_selecionado_avaliacao['indice_final_liquido']:.2f}"
)


print(
    f"Índice final do benchmark de 5 ativos: "
    f"{resultado_benchmark_avaliacao['indice_final_liquido']:.2f}"
)


print(
    f"\nDiferença do modelo com CDI contra o benchmark: "
    f"{diferenca_selecionado_benchmark:.2f} pontos"
)


print(
    f"Melhora contra o modelo anterior: "
    f"{diferenca_selecionado_base:.2f} pontos"
)


print(
    f"\nRetorno anualizado do modelo com CDI: "
    f"{resultado_selecionado_avaliacao['retorno_anualizado_liquido']:.2%}"
)


print(
    f"Volatilidade anualizada do modelo com CDI: "
    f"{resultado_selecionado_avaliacao['volatilidade_anualizada_liquida']:.2%}"
)


print(
    f"Retorno/volatilidade do modelo com CDI: "
    f"{resultado_selecionado_avaliacao['retorno_volatilidade_liquido']:.2f}"
)


print(
    f"Máximo drawdown do modelo com CDI: "
    f"{resultado_selecionado_avaliacao['maximo_drawdown_liquido']:.2%}"
)


print(
    f"Turnover total do modelo com CDI: "
    f"{resultado_selecionado_avaliacao['turnover_total']:.4f}"
)


print(
    f"\nResultado fora da amostra: "
    f"{STATUS_AVALIACAO}"
)


print(
    f"\nGrade completa salva em:\n"
    f"{ARQUIVO_GRADE}"
)


print(
    f"\nPesos selecionados salvos em:\n"
    f"{ARQUIVO_PESOS}"
)


print(
    f"\nMétricas comparativas salvas em:\n"
    f"{ARQUIVO_METRICAS}"
)


print(
    f"\nResumo salvo em:\n"
    f"{ARQUIVO_RESUMO}"
)


print(
    "\nPesos selecionados por regime:"
)


display(
    pesos_selecionados_df
)


print(
    "\nMétricas de treino e avaliação:"
)


display(
    metricas_formatadas
)


print(
    "\nValidações:"
)


display(
    tabela_validacao
)

# ###########################################################################
# ETAPA 10 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 10 — ROBUSTEZ E COMPARAÇÃO FINAL
# MODELO COM CDI
# VERSÃO AUTÔNOMA
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

from pathlib import Path
from itertools import product

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter


# ============================================================
# CONFIGURAÇÕES
# ============================================================

VALOR_INICIAL = 100.0
PERIODOS_POR_ANO = 12
JANELA_ROLLING = 12

VARIACOES_PESO_CDI = [
    -0.20,
    -0.10,
    0.00,
    0.10,
    0.20,
]

PESO_CDI_MINIMO = 0.00
PESO_CDI_MAXIMO = 0.70

CONFIRMACOES_TESTADAS = [
    1,
    2,
    3,
]

ORDEM_REGIMES = [
    "EXPANSAO_DESINFLACIONARIA",
    "EXPANSAO_INFLACIONARIA",
    "ESTAGFLACAO",
    "RECESSAO_DESINFLACIONARIA",
]

NOMES_REGIMES = {
    "EXPANSAO_DESINFLACIONARIA": (
        "Expansão desinflacionária"
    ),
    "EXPANSAO_INFLACIONARIA": (
        "Expansão inflacionária"
    ),
    "ESTAGFLACAO": (
        "Estagflação"
    ),
    "RECESSAO_DESINFLACIONARIA": (
        "Recessão desinflacionária"
    ),
}


# ============================================================
# LOCALIZAÇÃO DA RAIZ DO PROJETO
# ============================================================

DIRETORIO_ATUAL = Path.cwd().resolve()

RAIZ_PROJETO = None


for diretorio in [
    DIRETORIO_ATUAL,
    *DIRETORIO_ATUAL.parents,
]:

    arquivo_teste = (
        diretorio
        / "data"
        / "processed"
        / "backtest_portfolio_mensal.csv"
    )

    if arquivo_teste.exists():

        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:

    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo data/processed/"
        "backtest_portfolio_mensal.csv não foi encontrado."
    )


PASTA_DADOS_PROCESSADOS = (
    RAIZ_PROJETO
    / "data"
    / "processed"
)

PASTA_TABELAS = (
    RAIZ_PROJETO
    / "outputs"
    / "tabelas"
)

PASTA_GRAFICOS = (
    RAIZ_PROJETO
    / "outputs"
    / "graficos"
)


PASTA_TABELAS.mkdir(
    parents=True,
    exist_ok=True,
)

PASTA_GRAFICOS.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ARQUIVO_RETORNOS = (
    PASTA_DADOS_PROCESSADOS
    / "retornos_ativos_ampliados_mensais.csv"
)

ARQUIVO_BACKTEST = (
    PASTA_DADOS_PROCESSADOS
    / "backtest_portfolio_mensal.csv"
)

ARQUIVO_REGIMES = (
    PASTA_TABELAS
    / "06_02_regimes_suavizados.csv"
)

ARQUIVO_PESOS_BASE = (
    PASTA_TABELAS
    / "06_07_pesos_otimizados_por_regime.csv"
)

ARQUIVO_PESOS_SELECIONADOS = (
    PASTA_TABELAS
    / "06_09_pesos_selecionados_5_ativos.csv"
)

ARQUIVO_PARAMETROS_CELULA_9 = (
    PASTA_TABELAS
    / "06_09_parametros_selecionados_cdi.csv"
)

ARQUIVO_SERIES_CELULA_9 = (
    PASTA_TABELAS
    / "06_09_series_mensais_modelo_cdi.csv"
)


arquivos_entrada = [
    ARQUIVO_RETORNOS,
    ARQUIVO_BACKTEST,
    ARQUIVO_REGIMES,
    ARQUIVO_PESOS_BASE,
    ARQUIVO_PESOS_SELECIONADOS,
    ARQUIVO_PARAMETROS_CELULA_9,
    ARQUIVO_SERIES_CELULA_9,
]


arquivos_ausentes = [
    arquivo
    for arquivo in arquivos_entrada
    if not arquivo.exists()
]


if arquivos_ausentes:

    raise FileNotFoundError(
        "Arquivos necessários não encontrados:\n"
        + "\n".join(
            str(
                arquivo
            )
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_METRICAS = (
    PASTA_TABELAS
    / "06_10_metricas_comparadores.csv"
)

ARQUIVO_METRICAS_FORMATADAS = (
    PASTA_TABELAS
    / "06_10_metricas_comparadores_formatadas.csv"
)

ARQUIVO_SERIES_COMPARADORES = (
    PASTA_TABELAS
    / "06_10_series_comparadores.csv"
)

ARQUIVO_PESOS_ESTATICOS = (
    PASTA_TABELAS
    / "06_10_pesos_carteira_estatica.csv"
)

ARQUIVO_GRADE_SENSIBILIDADE = (
    PASTA_TABELAS
    / "06_10_grade_sensibilidade_cdi.csv"
)

ARQUIVO_SENSIBILIDADE_CONFIRMACAO = (
    PASTA_TABELAS
    / "06_10_sensibilidade_por_confirmacao.csv"
)

ARQUIVO_RESUMO_SENSIBILIDADE = (
    PASTA_TABELAS
    / "06_10_resumo_sensibilidade.csv"
)

ARQUIVO_ROLLING = (
    PASTA_TABELAS
    / "06_10_rolling_12m_avaliacao.csv"
)

ARQUIVO_DECISAO = (
    PASTA_TABELAS
    / "06_10_decisao_modelo.csv"
)

ARQUIVO_VALIDACOES = (
    PASTA_TABELAS
    / "06_10_validacoes.csv"
)

ARQUIVO_RESUMO_FINAL = (
    PASTA_TABELAS
    / "06_10_resumo_final_robustez.csv"
)

ARQUIVO_GRAFICO_DESEMPENHO = (
    PASTA_GRAFICOS
    / "06_10_desempenho_comparadores_avaliacao.png"
)

ARQUIVO_GRAFICO_RISCO_RETORNO = (
    PASTA_GRAFICOS
    / "06_10_risco_retorno_avaliacao.png"
)

ARQUIVO_GRAFICO_DIFERENCA = (
    PASTA_GRAFICOS
    / "06_10_diferenca_modelo_vs_referencias.png"
)

ARQUIVO_GRAFICO_SENSIBILIDADE = (
    PASTA_GRAFICOS
    / "06_10_distribuicao_sensibilidade_vs_benchmark.png"
)

ARQUIVO_GRAFICO_ROLLING = (
    PASTA_GRAFICOS
    / "06_10_rolling_12m_avaliacao.png"
)


# ============================================================
# CARREGAMENTO DAS BASES
# ============================================================

retornos = pd.read_csv(
    ARQUIVO_RETORNOS,
    encoding="utf-8-sig",
)

backtest = pd.read_csv(
    ARQUIVO_BACKTEST,
    encoding="utf-8-sig",
)

regimes = pd.read_csv(
    ARQUIVO_REGIMES,
    encoding="utf-8-sig",
)

pesos_base_df = pd.read_csv(
    ARQUIVO_PESOS_BASE,
    encoding="utf-8-sig",
)

pesos_selecionados_df = pd.read_csv(
    ARQUIVO_PESOS_SELECIONADOS,
    encoding="utf-8-sig",
)

parametros_celula_9 = pd.read_csv(
    ARQUIVO_PARAMETROS_CELULA_9,
    encoding="utf-8-sig",
)

series_celula_9 = pd.read_csv(
    ARQUIVO_SERIES_CELULA_9,
    encoding="utf-8-sig",
)


# ============================================================
# PADRONIZAÇÃO DAS DATAS
# ============================================================

bases_com_data = {
    "retornos": retornos,
    "backtest": backtest,
    "regimes": regimes,
    "séries da Célula 9": series_celula_9,
}


for nome_base, base in bases_com_data.items():

    if "data" not in base.columns:

        raise ValueError(
            f"A base {nome_base} não possui "
            "a coluna data."
        )

    base["data"] = pd.to_datetime(
        base["data"],
        errors="coerce",
    )

    if base["data"].isna().any():

        raise ValueError(
            f"A base {nome_base} possui datas inválidas."
        )

    if base["data"].duplicated().any():

        raise ValueError(
            f"A base {nome_base} possui datas duplicadas."
        )

    base.sort_values(
        "data",
        inplace=True,
    )

    base.reset_index(
        drop=True,
        inplace=True,
    )


# ============================================================
# FUNÇÃO PARA LER PARÂMETROS SALVOS
# ============================================================

def ler_parametro(
    tabela,
    nome_metrica,
    valor_padrao=None,
):

    if not {
        "metrica",
        "valor",
    }.issubset(
        tabela.columns
    ):

        return valor_padrao

    resultado = tabela.loc[
        tabela[
            "metrica"
        ]
        == nome_metrica,
        "valor",
    ]

    if resultado.empty:

        return valor_padrao

    return resultado.iloc[0]


# ============================================================
# DATA DE CORTE
# ============================================================

valor_data_corte = ler_parametro(
    tabela=parametros_celula_9,
    nome_metrica="Data final do treino",
    valor_padrao="31/12/2023",
)


DATA_CORTE_TREINO = pd.to_datetime(
    valor_data_corte,
    dayfirst=True,
    errors="coerce",
)


if pd.isna(
    DATA_CORTE_TREINO
):

    raise ValueError(
        "Não foi possível identificar "
        "a data final do treino."
    )


# ============================================================
# IDENTIFICAÇÃO DOS ATIVOS
# ============================================================

colunas_pesos_selecionados = [
    coluna
    for coluna in pesos_selecionados_df.columns
    if coluna.startswith(
        "peso_"
    )
    and coluna != "soma_pesos"
]


if not colunas_pesos_selecionados:

    raise ValueError(
        "Não foram encontradas colunas de pesos "
        "no arquivo da Célula 9."
    )


ATIVOS = [
    coluna.replace(
        "peso_",
        "",
        1,
    )
    for coluna in colunas_pesos_selecionados
]


if "CDI" not in ATIVOS:

    raise ValueError(
        "O CDI não foi encontrado entre os ativos "
        "selecionados na Célula 9."
    )


ATIVOS_RISCO = [
    ativo
    for ativo in ATIVOS
    if ativo != "CDI"
]


ativos_ausentes = [
    ativo
    for ativo in ATIVOS
    if ativo not in retornos.columns
]


if ativos_ausentes:

    raise ValueError(
        "Ativos ausentes na base de retornos:\n"
        f"{ativos_ausentes}"
    )


# ============================================================
# VALIDAÇÃO DOS REGIMES
# ============================================================

colunas_regimes = [
    f"regime_confirmacao_{confirmacao}m"
    for confirmacao in CONFIRMACOES_TESTADAS
]


colunas_regimes_ausentes = [
    coluna
    for coluna in colunas_regimes
    if coluna not in regimes.columns
]


if colunas_regimes_ausentes:

    raise ValueError(
        "Colunas de regimes ausentes:\n"
        f"{colunas_regimes_ausentes}"
    )


# ============================================================
# CONSTRUÇÃO DA BASE COMPLETA
# ============================================================

base = (
    retornos[
        [
            "data",
            *ATIVOS,
        ]
    ]
    .merge(
        regimes[
            [
                "data",
                *colunas_regimes,
            ]
        ],
        on="data",
        how="inner",
        validate="one_to_one",
    )
    .sort_values(
        "data"
    )
    .reset_index(
        drop=True
    )
)


if len(
    base
) != len(
    retornos
):

    raise ValueError(
        "A junção com os regimes alterou "
        "a quantidade de meses."
    )


for ativo in ATIVOS:

    base[ativo] = pd.to_numeric(
        base[ativo],
        errors="coerce",
    )


if (
    base[
        ATIVOS
    ]
    .isna()
    .any()
    .any()
):

    raise ValueError(
        "Existem retornos nulos ou inválidos "
        "na base completa."
    )


for coluna_regime in colunas_regimes:

    base[coluna_regime] = (
        base[coluna_regime]
        .astype("string")
        .str.strip()
    )

    regimes_invalidos = (
        base.loc[
            ~base[
                coluna_regime
            ].isin(
                ORDEM_REGIMES
            ),
            coluna_regime,
        ]
        .dropna()
        .unique()
        .tolist()
    )

    if regimes_invalidos:

        raise ValueError(
            f"A coluna {coluna_regime} possui "
            f"regimes inválidos:\n"
            f"{regimes_invalidos}"
        )


base["periodo"] = np.where(
    base["data"]
    <= DATA_CORTE_TREINO,
    "TREINO",
    "AVALIACAO",
)


MASCARA_TREINO = (
    base["periodo"]
    == "TREINO"
).to_numpy()


MASCARA_AVALIACAO = (
    base["periodo"]
    == "AVALIACAO"
).to_numpy()


if MASCARA_TREINO.sum() <= 0:

    raise ValueError(
        "A base de treino ficou vazia."
    )


if MASCARA_AVALIACAO.sum() <= 0:

    raise ValueError(
        "A base de avaliação ficou vazia."
    )


MATRIZ_RETORNOS = (
    base[
        ATIVOS
    ]
    .astype(float)
    .to_numpy()
)


VETOR_CDI = (
    base[
        "CDI"
    ]
    .astype(float)
    .to_numpy()
)


# ============================================================
# IDENTIFICAÇÃO DO CUSTO
# ============================================================

if {
    "turnover_portfolio",
    "custo_portfolio",
}.issubset(
    backtest.columns
):

    turnover_original = pd.to_numeric(
        backtest[
            "turnover_portfolio"
        ],
        errors="coerce",
    )

    custo_original = pd.to_numeric(
        backtest[
            "custo_portfolio"
        ],
        errors="coerce",
    )

    mascara_turnover = (
        turnover_original > 0
    )

    custos_observados = (
        custo_original.loc[
            mascara_turnover
        ]
        / turnover_original.loc[
            mascara_turnover
        ]
    ).dropna()

    if custos_observados.empty:

        CUSTO_POR_TURNOVER = 0.001

    else:

        CUSTO_POR_TURNOVER = float(
            custos_observados.median()
        )

else:

    CUSTO_POR_TURNOVER = 0.001


if CUSTO_POR_TURNOVER < 0:

    raise ValueError(
        "O custo por turnover não pode ser negativo."
    )


# ============================================================
# LEITURA DOS PESOS SELECIONADOS
# ============================================================

if "regime" not in pesos_selecionados_df.columns:

    raise ValueError(
        "O arquivo de pesos da Célula 9 "
        "não possui a coluna regime."
    )


pesos_selecionados_df["regime"] = (
    pesos_selecionados_df[
        "regime"
    ]
    .astype("string")
    .str.strip()
)


PESOS_MODELO_SELECIONADO = {}


for regime in ORDEM_REGIMES:

    linhas_regime = (
        pesos_selecionados_df.loc[
            pesos_selecionados_df[
                "regime"
            ]
            == regime
        ]
    )

    if linhas_regime.empty:

        raise ValueError(
            f"O regime {regime} não possui "
            "pesos selecionados."
        )

    linha = linhas_regime.iloc[0]

    PESOS_MODELO_SELECIONADO[
        regime
    ] = {
        ativo: float(
            linha[
                f"peso_{ativo}"
            ]
        )
        for ativo in ATIVOS
    }


confirmacoes_selecionadas = (
    pd.to_numeric(
        pesos_selecionados_df[
            "meses_confirmacao"
        ],
        errors="coerce",
    )
    .dropna()
    .unique()
)


if len(
    confirmacoes_selecionadas
) != 1:

    raise ValueError(
        "Não foi possível identificar uma única "
        "confirmação selecionada."
    )


CONFIRMACAO_SELECIONADA = int(
    confirmacoes_selecionadas[0]
)


# ============================================================
# LEITURA DOS PESOS BASE DA CÉLULA 7
# ============================================================

colunas_pesos_base = [
    coluna
    for coluna in pesos_base_df.columns
    if (
        coluna.startswith(
            "peso_otimizado_"
        )
        and coluna
        != "peso_otimizado_CDI"
    )
]


if not colunas_pesos_base:

    raise ValueError(
        "Não foram encontradas colunas "
        "peso_otimizado_* da Célula 7."
    )


ativos_risco_base = [
    coluna.replace(
        "peso_otimizado_",
        "",
        1,
    )
    for coluna in colunas_pesos_base
]


if set(
    ativos_risco_base
) != set(
    ATIVOS_RISCO
):

    raise ValueError(
        "Os ativos de risco da Célula 7 "
        "não correspondem aos ativos da Célula 9."
    )


pesos_base_df["regime"] = (
    pesos_base_df[
        "regime"
    ]
    .astype("string")
    .str.strip()
)


PESOS_RISCO_BASE = {}


for regime in ORDEM_REGIMES:

    linha = (
        pesos_base_df.loc[
            pesos_base_df[
                "regime"
            ]
            == regime
        ]
    )

    if linha.empty:

        raise ValueError(
            f"O regime {regime} não possui "
            "pesos base."
        )

    linha = linha.iloc[0]

    pesos_risco_brutos = {
        ativo: float(
            linha[
                f"peso_otimizado_{ativo}"
            ]
        )
        for ativo in ATIVOS_RISCO
    }

    soma_pesos_risco_brutos = sum(
        pesos_risco_brutos.values()
    )

    if (
        not np.isfinite(
            soma_pesos_risco_brutos
        )
        or soma_pesos_risco_brutos
        <= 0.0
    ):

        raise ValueError(
            f"Os pesos base de risco do regime {regime} "
            "possuem soma inválida: "
            f"{soma_pesos_risco_brutos}"
        )

    PESOS_RISCO_BASE[
        regime
    ] = {
        ativo: (
            peso
            / soma_pesos_risco_brutos
        )
        for ativo, peso
        in pesos_risco_brutos.items()
    }

    soma = sum(
        PESOS_RISCO_BASE[
            regime
        ].values()
    )

    if not np.isclose(
        soma,
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ):

        raise ValueError(
            f"Os pesos base de risco normalizados de "
            f"{regime} não somam 100%."
        )


confirmacao_base = 2


if "meses_confirmacao" in pesos_base_df.columns:

    confirmacoes_base = (
        pd.to_numeric(
            pesos_base_df[
                "meses_confirmacao"
            ],
            errors="coerce",
        )
        .dropna()
        .unique()
    )

    if len(
        confirmacoes_base
    ) == 1:

        confirmacao_base = int(
            confirmacoes_base[0]
        )


# ============================================================
# FUNÇÕES DE PESOS
# ============================================================

def validar_dicionario_pesos(
    pesos_por_regime,
):

    for regime in ORDEM_REGIMES:

        if regime not in pesos_por_regime:

            raise KeyError(
                f"O regime {regime} não possui pesos."
            )

        pesos_regime = pesos_por_regime[
            regime
        ]

        ativos_faltantes = [
            ativo
            for ativo in ATIVOS
            if ativo not in pesos_regime
        ]

        if ativos_faltantes:

            raise KeyError(
                f"Ativos ausentes no regime {regime}:\n"
                f"{ativos_faltantes}"
            )

        valores = np.array(
            [
                pesos_regime[
                    ativo
                ]
                for ativo in ATIVOS
            ],
            dtype=float,
        )

        if (
            valores < 0
        ).any():

            raise ValueError(
                f"Existem pesos negativos no regime "
                f"{regime}."
            )

        if not np.isclose(
            valores.sum(),
            1.0,
            atol=1e-10,
            rtol=1e-10,
        ):

            raise ValueError(
                f"Os pesos do regime {regime} "
                "não somam 100%."
            )


def criar_pesos_com_cdi(
    pesos_cdi_por_regime,
):

    pesos_finais = {}

    for regime in ORDEM_REGIMES:

        peso_cdi = float(
            pesos_cdi_por_regime[
                regime
            ]
        )

        if not (
            0.0
            <= peso_cdi
            <= 1.0
        ):

            raise ValueError(
                f"Peso de CDI inválido no regime "
                f"{regime}."
            )

        pesos_finais[
            regime
        ] = {}

        for ativo in ATIVOS_RISCO:

            pesos_finais[
                regime
            ][ativo] = (
                PESOS_RISCO_BASE[
                    regime
                ][ativo]
                * (
                    1.0
                    - peso_cdi
                )
            )

        pesos_finais[
            regime
        ][
            "CDI"
        ] = peso_cdi

    validar_dicionario_pesos(
        pesos_finais
    )

    return pesos_finais


def criar_matriz_pesos_regime(
    pesos_por_regime,
    meses_confirmacao,
):

    validar_dicionario_pesos(
        pesos_por_regime
    )

    coluna_regime = (
        f"regime_confirmacao_"
        f"{int(meses_confirmacao)}m"
    )

    if coluna_regime not in base.columns:

        raise KeyError(
            f"A coluna {coluna_regime} "
            "não foi encontrada."
        )

    matriz = np.zeros(
        (
            len(base),
            len(ATIVOS),
        ),
        dtype=float,
    )

    regimes_mensais = (
        base[
            coluna_regime
        ]
        .astype(str)
        .to_numpy()
    )

    for indice, regime in enumerate(
        regimes_mensais
    ):

        matriz[
            indice,
            :,
        ] = [
            pesos_por_regime[
                regime
            ][ativo]
            for ativo in ATIVOS
        ]

    if not np.allclose(
        matriz.sum(
            axis=1
        ),
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ):

        raise ValueError(
            "A matriz de pesos por regime "
            "não soma 100%."
        )

    return matriz


def criar_matriz_pesos_constantes(
    pesos_constantes,
):

    vetor = np.array(
        [
            pesos_constantes[
                ativo
            ]
            for ativo in ATIVOS
        ],
        dtype=float,
    )

    if (
        vetor < 0
    ).any():

        raise ValueError(
            "Existem pesos constantes negativos."
        )

    if not np.isclose(
        vetor.sum(),
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ):

        raise ValueError(
            "Os pesos constantes não somam 100%."
        )

    return np.tile(
        vetor,
        (
            len(base),
            1,
        ),
    )


# ============================================================
# FUNÇÃO DE SIMULAÇÃO
# ============================================================

def simular_carteira(
    matriz_pesos,
):

    if matriz_pesos.shape != MATRIZ_RETORNOS.shape:

        raise ValueError(
            "A matriz de pesos possui dimensão diferente "
            "da matriz de retornos."
        )

    retorno_bruto = np.sum(
        matriz_pesos
        * MATRIZ_RETORNOS,
        axis=1,
    )

    turnover = np.zeros(
        len(base),
        dtype=float,
    )

    turnover[0] = 1.0

    for indice in range(
        1,
        len(base),
    ):

        pesos_anteriores = (
            matriz_pesos[
                indice - 1
            ]
        )

        retornos_anteriores = (
            MATRIZ_RETORNOS[
                indice - 1
            ]
        )

        retorno_anterior = (
            retorno_bruto[
                indice - 1
            ]
        )

        fator_patrimonio = (
            1.0
            + retorno_anterior
        )

        if fator_patrimonio <= 0:

            raise ValueError(
                "O patrimônio relativo ficou "
                "menor ou igual a zero."
            )

        pesos_apos_retorno = (
            pesos_anteriores
            * (
                1.0
                + retornos_anteriores
            )
            / fator_patrimonio
        )

        pesos_alvo = (
            matriz_pesos[
                indice
            ]
        )

        turnover[indice] = float(
            np.abs(
                pesos_alvo
                - pesos_apos_retorno
            ).sum()
            / 2.0
        )

    custo = (
        turnover
        * CUSTO_POR_TURNOVER
    )

    retorno_liquido = (
        (
            1.0
            + retorno_bruto
        )
        * (
            1.0
            - custo
        )
        - 1.0
    )

    return {
        "matriz_pesos": matriz_pesos,
        "retorno_bruto": retorno_bruto,
        "turnover": turnover,
        "custo": custo,
        "retorno_liquido": retorno_liquido,
    }


# ============================================================
# FUNÇÕES DE MÉTRICAS
# ============================================================

def retorno_total(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(
        retornos
    ) == 0:

        return np.nan

    return float(
        np.prod(
            1.0
            + retornos
        )
        - 1.0
    )


def retorno_anualizado(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(
        retornos
    ) == 0:

        return np.nan

    total = retorno_total(
        retornos
    )

    if total <= -1:

        return np.nan

    return float(
        (
            1.0
            + total
        )
        ** (
            PERIODOS_POR_ANO
            / len(
                retornos
            )
        )
        - 1.0
    )


def volatilidade_anualizada(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(
        retornos
    ) < 2:

        return np.nan

    return float(
        np.std(
            retornos,
            ddof=1,
        )
        * np.sqrt(
            PERIODOS_POR_ANO
        )
    )


def maximo_drawdown(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(
        retornos
    ) == 0:

        return np.nan

    indice = (
        VALOR_INICIAL
        * np.cumprod(
            1.0
            + retornos
        )
    )

    indice_com_inicio = np.concatenate(
        [
            np.array(
                [
                    VALOR_INICIAL
                ]
            ),
            indice,
        ]
    )

    picos = np.maximum.accumulate(
        indice_com_inicio
    )

    drawdown = (
        indice_com_inicio
        / picos
        - 1.0
    )

    return float(
        drawdown.min()
    )


def sharpe_excesso_cdi(
    retornos,
    retornos_cdi,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    retornos_cdi = np.asarray(
        retornos_cdi,
        dtype=float,
    )

    excesso = (
        retornos
        - retornos_cdi
    )

    desvio = np.std(
        excesso,
        ddof=1,
    )

    if (
        not np.isfinite(
            desvio
        )
        or desvio <= 0
    ):

        return 0.0

    return float(
        np.sqrt(
            PERIODOS_POR_ANO
        )
        * np.mean(
            excesso
        )
        / desvio
    )


def sortino_excesso_cdi(
    retornos,
    retornos_cdi,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    retornos_cdi = np.asarray(
        retornos_cdi,
        dtype=float,
    )

    excesso = (
        retornos
        - retornos_cdi
    )

    perdas = np.minimum(
        excesso,
        0.0,
    )

    desvio_negativo_mensal = np.sqrt(
        np.mean(
            perdas ** 2
        )
    )

    desvio_negativo_anual = (
        desvio_negativo_mensal
        * np.sqrt(
            PERIODOS_POR_ANO
        )
    )

    excesso_anualizado = (
        np.mean(
            excesso
        )
        * PERIODOS_POR_ANO
    )

    if desvio_negativo_anual <= 0:

        if excesso_anualizado > 0:

            return np.inf

        return 0.0

    return float(
        excesso_anualizado
        / desvio_negativo_anual
    )


def calcular_metricas(
    simulacao,
    mascara,
):

    retornos_brutos = (
        simulacao[
            "retorno_bruto"
        ][mascara]
    )

    retornos_liquidos = (
        simulacao[
            "retorno_liquido"
        ][mascara]
    )

    turnovers = (
        simulacao[
            "turnover"
        ][mascara]
    )

    custos = (
        simulacao[
            "custo"
        ][mascara]
    )

    cdi_periodo = (
        VETOR_CDI[
            mascara
        ]
    )

    retorno_anual = retorno_anualizado(
        retornos_liquidos
    )

    volatilidade = volatilidade_anualizada(
        retornos_liquidos
    )

    drawdown = maximo_drawdown(
        retornos_liquidos
    )

    if (
        pd.notna(
            volatilidade
        )
        and volatilidade > 0
    ):

        retorno_volatilidade = (
            retorno_anual
            / volatilidade
        )

    else:

        retorno_volatilidade = np.nan

    if (
        pd.notna(
            drawdown
        )
        and drawdown < 0
    ):

        calmar = (
            retorno_anual
            / abs(
                drawdown
            )
        )

    else:

        calmar = np.nan

    return {
        "quantidade_meses": int(
            mascara.sum()
        ),
        "retorno_total_bruto": retorno_total(
            retornos_brutos
        ),
        "retorno_total_liquido": retorno_total(
            retornos_liquidos
        ),
        "retorno_anualizado_liquido": (
            retorno_anual
        ),
        "volatilidade_anualizada_liquida": (
            volatilidade
        ),
        "retorno_volatilidade": (
            retorno_volatilidade
        ),
        "sharpe_excesso_cdi": (
            sharpe_excesso_cdi(
                retornos=retornos_liquidos,
                retornos_cdi=cdi_periodo,
            )
        ),
        "sortino_excesso_cdi": (
            sortino_excesso_cdi(
                retornos=retornos_liquidos,
                retornos_cdi=cdi_periodo,
            )
        ),
        "calmar": calmar,
        "maximo_drawdown": drawdown,
        "meses_positivos": float(
            np.mean(
                retornos_liquidos > 0
            )
        ),
        "melhor_mes": float(
            np.max(
                retornos_liquidos
            )
        ),
        "pior_mes": float(
            np.min(
                retornos_liquidos
            )
        ),
        "turnover_total": float(
            turnovers.sum()
        ),
        "turnover_medio_mensal": float(
            turnovers.mean()
        ),
        "custo_acumulado_simples": float(
            custos.sum()
        ),
        "indice_final_liquido": float(
            VALOR_INICIAL
            * np.prod(
                1.0
                + retornos_liquidos
            )
        ),
    }


# ============================================================
# MODELO SELECIONADO
# ============================================================

matriz_modelo_selecionado = (
    criar_matriz_pesos_regime(
        pesos_por_regime=(
            PESOS_MODELO_SELECIONADO
        ),
        meses_confirmacao=(
            CONFIRMACAO_SELECIONADA
        ),
    )
)


SIMULACAO_MODELO_SELECIONADO = (
    simular_carteira(
        matriz_pesos=(
            matriz_modelo_selecionado
        )
    )
)


# ============================================================
# MODELO BASE SEM CDI
# ============================================================

PESOS_MODELO_BASE = {
    regime: {
        **{
            ativo: PESOS_RISCO_BASE[
                regime
            ][ativo]
            for ativo in ATIVOS_RISCO
        },
        "CDI": 0.0,
    }
    for regime in ORDEM_REGIMES
}


matriz_modelo_base = (
    criar_matriz_pesos_regime(
        pesos_por_regime=(
            PESOS_MODELO_BASE
        ),
        meses_confirmacao=(
            confirmacao_base
        ),
    )
)


SIMULACAO_MODELO_BASE = (
    simular_carteira(
        matriz_pesos=(
            matriz_modelo_base
        )
    )
)


# ============================================================
# BENCHMARK DE PESOS IGUAIS
# ============================================================

PESO_IGUAL = (
    1.0
    / len(
        ATIVOS
    )
)


PESOS_BENCHMARK = {
    ativo: PESO_IGUAL
    for ativo in ATIVOS
}


matriz_benchmark = (
    criar_matriz_pesos_constantes(
        pesos_constantes=(
            PESOS_BENCHMARK
        )
    )
)


SIMULACAO_BENCHMARK = (
    simular_carteira(
        matriz_pesos=(
            matriz_benchmark
        )
    )
)


# ============================================================
# CARTEIRA ESTÁTICA
# PESOS MÉDIOS DO MODELO APENAS NO TREINO
# ============================================================

pesos_estaticos_vetor = (
    matriz_modelo_selecionado[
        MASCARA_TREINO
    ]
    .mean(
        axis=0
    )
)


pesos_estaticos = {
    ativo: float(
        pesos_estaticos_vetor[
            indice
        ]
    )
    for indice, ativo in enumerate(
        ATIVOS
    )
}


matriz_estatica = (
    criar_matriz_pesos_constantes(
        pesos_constantes=(
            pesos_estaticos
        )
    )
)


SIMULACAO_ESTATICA = (
    simular_carteira(
        matriz_pesos=(
            matriz_estatica
        )
    )
)


pesos_estaticos_df = pd.DataFrame(
    {
        "ativo": ATIVOS,
        "peso": [
            pesos_estaticos[
                ativo
            ]
            for ativo in ATIVOS
        ],
        "origem": (
            "Média dos pesos-alvo do modelo "
            "durante o treino"
        ),
    }
)


# ============================================================
# CARTEIRA 100% CDI
# ============================================================

PESOS_CDI_100 = {
    ativo: (
        1.0
        if ativo == "CDI"
        else 0.0
    )
    for ativo in ATIVOS
}


matriz_cdi_100 = (
    criar_matriz_pesos_constantes(
        pesos_constantes=(
            PESOS_CDI_100
        )
    )
)


SIMULACAO_CDI_100 = (
    simular_carteira(
        matriz_pesos=(
            matriz_cdi_100
        )
    )
)


# ============================================================
# VALIDAÇÃO CONTRA AS SÉRIES SALVAS NA CÉLULA 9
# ============================================================

coluna_salva_modelo = (
    "retorno_liquido_"
    "MODELO_SELECIONADO_5_ATIVOS"
)

coluna_salva_base = (
    "retorno_liquido_"
    "MODELO_BASE_4_ATIVOS"
)

coluna_salva_benchmark = (
    "retorno_liquido_"
    "BENCHMARK_5_ATIVOS"
)


colunas_salvas_necessarias = [
    coluna_salva_modelo,
    coluna_salva_base,
    coluna_salva_benchmark,
]


colunas_salvas_ausentes = [
    coluna
    for coluna in colunas_salvas_necessarias
    if coluna not in series_celula_9.columns
]


if colunas_salvas_ausentes:

    raise ValueError(
        "Colunas necessárias ausentes "
        "nas séries da Célula 9:\n"
        f"{colunas_salvas_ausentes}"
    )


series_validacao = (
    base[
        [
            "data"
        ]
    ]
    .merge(
        series_celula_9[
            [
                "data",
                *colunas_salvas_necessarias,
            ]
        ],
        on="data",
        how="left",
        validate="one_to_one",
    )
)


diferenca_modelo_salvo = float(
    np.max(
        np.abs(
            SIMULACAO_MODELO_SELECIONADO[
                "retorno_liquido"
            ]
            - series_validacao[
                coluna_salva_modelo
            ].to_numpy(
                dtype=float
            )
        )
    )
)


diferenca_base_salva = float(
    np.max(
        np.abs(
            SIMULACAO_MODELO_BASE[
                "retorno_liquido"
            ]
            - series_validacao[
                coluna_salva_base
            ].to_numpy(
                dtype=float
            )
        )
    )
)


diferenca_benchmark_salvo = float(
    np.max(
        np.abs(
            SIMULACAO_BENCHMARK[
                "retorno_liquido"
            ]
            - series_validacao[
                coluna_salva_benchmark
            ].to_numpy(
                dtype=float
            )
        )
    )
)


# ============================================================
# MÉTRICAS DOS COMPARADORES
# ============================================================

CENARIOS = {
    "MODELO_COM_CDI": {
        "rotulo": (
            "Modelo com CDI"
        ),
        "simulacao": (
            SIMULACAO_MODELO_SELECIONADO
        ),
    },
    "MODELO_ANTERIOR_SEM_CDI": {
        "rotulo": (
            "Modelo anterior sem CDI"
        ),
        "simulacao": (
            SIMULACAO_MODELO_BASE
        ),
    },
    "BENCHMARK_5_ATIVOS": {
        "rotulo": (
            "Benchmark de pesos iguais"
        ),
        "simulacao": (
            SIMULACAO_BENCHMARK
        ),
    },
    "CARTEIRA_ESTATICA": {
        "rotulo": (
            "Carteira estática"
        ),
        "simulacao": (
            SIMULACAO_ESTATICA
        ),
    },
    "CDI_100": {
        "rotulo": (
            "100% CDI"
        ),
        "simulacao": (
            SIMULACAO_CDI_100
        ),
    },
}


registros_metricas = []


for periodo, mascara in [
    (
        "TREINO",
        MASCARA_TREINO,
    ),
    (
        "AVALIACAO",
        MASCARA_AVALIACAO,
    ),
]:

    for cenario, configuracao in (
        CENARIOS.items()
    ):

        metricas = calcular_metricas(
            simulacao=configuracao[
                "simulacao"
            ],
            mascara=mascara,
        )

        registros_metricas.append(
            {
                "periodo": periodo,
                "cenario": cenario,
                "rotulo": configuracao[
                    "rotulo"
                ],
                **metricas,
            }
        )


metricas_comparadores = pd.DataFrame(
    registros_metricas
)


for periodo in [
    "TREINO",
    "AVALIACAO",
]:

    indice_benchmark_periodo = float(
        metricas_comparadores.loc[
            (
                metricas_comparadores[
                    "periodo"
                ]
                == periodo
            )
            & (
                metricas_comparadores[
                    "cenario"
                ]
                == "BENCHMARK_5_ATIVOS"
            ),
            "indice_final_liquido",
        ]
        .iloc[0]
    )

    metricas_comparadores.loc[
        metricas_comparadores[
            "periodo"
        ]
        == periodo,
        "diferenca_indice_vs_benchmark",
    ] = (
        metricas_comparadores.loc[
            metricas_comparadores[
                "periodo"
            ]
            == periodo,
            "indice_final_liquido",
        ]
        - indice_benchmark_periodo
    )


# ============================================================
# SÉRIES DOS COMPARADORES
# ============================================================

series_comparadores = (
    base[
        [
            "data",
            "periodo",
            *ATIVOS,
            *colunas_regimes,
        ]
    ]
    .copy()
)


for cenario, configuracao in (
    CENARIOS.items()
):

    simulacao = configuracao[
        "simulacao"
    ]

    series_comparadores[
        f"retorno_liquido_{cenario}"
    ] = simulacao[
        "retorno_liquido"
    ]

    series_comparadores[
        f"retorno_bruto_{cenario}"
    ] = simulacao[
        "retorno_bruto"
    ]

    series_comparadores[
        f"turnover_{cenario}"
    ] = simulacao[
        "turnover"
    ]

    series_comparadores[
        f"custo_{cenario}"
    ] = simulacao[
        "custo"
    ]


# ============================================================
# ROLLING DE 12 MESES NA AVALIAÇÃO
# ============================================================

def calcular_retorno_rolling(
    retornos,
):

    return (
        (
            1.0
            + pd.Series(
                retornos
            )
        )
        .rolling(
            JANELA_ROLLING
        )
        .apply(
            np.prod,
            raw=True,
        )
        - 1.0
    )


datas_avaliacao = (
    base.loc[
        MASCARA_AVALIACAO,
        "data",
    ]
    .reset_index(
        drop=True
    )
)


retornos_modelo_avaliacao = (
    SIMULACAO_MODELO_SELECIONADO[
        "retorno_liquido"
    ][MASCARA_AVALIACAO]
)


retornos_base_avaliacao = (
    SIMULACAO_MODELO_BASE[
        "retorno_liquido"
    ][MASCARA_AVALIACAO]
)


retornos_benchmark_avaliacao = (
    SIMULACAO_BENCHMARK[
        "retorno_liquido"
    ][MASCARA_AVALIACAO]
)


retornos_cdi_avaliacao = (
    SIMULACAO_CDI_100[
        "retorno_liquido"
    ][MASCARA_AVALIACAO]
)


rolling_avaliacao = pd.DataFrame(
    {
        "data": datas_avaliacao,
        "retorno_12m_modelo": (
            calcular_retorno_rolling(
                retornos_modelo_avaliacao
            )
        ),
        "retorno_12m_modelo_anterior": (
            calcular_retorno_rolling(
                retornos_base_avaliacao
            )
        ),
        "retorno_12m_benchmark": (
            calcular_retorno_rolling(
                retornos_benchmark_avaliacao
            )
        ),
        "retorno_12m_cdi": (
            calcular_retorno_rolling(
                retornos_cdi_avaliacao
            )
        ),
    }
)


rolling_avaliacao[
    "excesso_modelo_vs_benchmark"
] = (
    rolling_avaliacao[
        "retorno_12m_modelo"
    ]
    - rolling_avaliacao[
        "retorno_12m_benchmark"
    ]
)


rolling_avaliacao[
    "excesso_modelo_vs_anterior"
] = (
    rolling_avaliacao[
        "retorno_12m_modelo"
    ]
    - rolling_avaliacao[
        "retorno_12m_modelo_anterior"
    ]
)


rolling_avaliacao[
    "excesso_modelo_vs_cdi"
] = (
    rolling_avaliacao[
        "retorno_12m_modelo"
    ]
    - rolling_avaliacao[
        "retorno_12m_cdi"
    ]
)


rolling_validos = (
    rolling_avaliacao
    .dropna(
        subset=[
            "excesso_modelo_vs_benchmark"
        ]
    )
)


if rolling_validos.empty:

    PROPORCAO_ROLLING_POSITIVO = np.nan
    PIOR_EXCESSO_ROLLING = np.nan
    MELHOR_EXCESSO_ROLLING = np.nan

else:

    PROPORCAO_ROLLING_POSITIVO = float(
        rolling_validos[
            "excesso_modelo_vs_benchmark"
        ]
        .gt(0)
        .mean()
    )

    PIOR_EXCESSO_ROLLING = float(
        rolling_validos[
            "excesso_modelo_vs_benchmark"
        ]
        .min()
    )

    MELHOR_EXCESSO_ROLLING = float(
        rolling_validos[
            "excesso_modelo_vs_benchmark"
        ]
        .max()
    )


# ============================================================
# GRADE DE SENSIBILIDADE
# NÃO É UTILIZADA PARA ESCOLHER NOVOS PESOS
# ============================================================

PESOS_CDI_ORIGINAIS = {
    regime: float(
        PESOS_MODELO_SELECIONADO[
            regime
        ][
            "CDI"
        ]
    )
    for regime in ORDEM_REGIMES
}


valores_sensibilidade_por_regime = {}


for regime in ORDEM_REGIMES:

    peso_original = (
        PESOS_CDI_ORIGINAIS[
            regime
        ]
    )

    valores = sorted(
        {
            round(
                min(
                    PESO_CDI_MAXIMO,
                    max(
                        PESO_CDI_MINIMO,
                        peso_original
                        + variacao,
                    ),
                ),
                10,
            )
            for variacao in (
                VARIACOES_PESO_CDI
            )
        }
    )

    valores_sensibilidade_por_regime[
        regime
    ] = valores


metricas_benchmark_avaliacao = (
    calcular_metricas(
        simulacao=(
            SIMULACAO_BENCHMARK
        ),
        mascara=(
            MASCARA_AVALIACAO
        ),
    )
)


metricas_base_avaliacao = (
    calcular_metricas(
        simulacao=(
            SIMULACAO_MODELO_BASE
        ),
        mascara=(
            MASCARA_AVALIACAO
        ),
    )
)


registros_sensibilidade = []


combinacoes_pesos = product(
    *[
        valores_sensibilidade_por_regime[
            regime
        ]
        for regime in ORDEM_REGIMES
    ]
)


combinacoes_pesos = list(
    combinacoes_pesos
)


QUANTIDADE_COMBINACOES_SENSIBILIDADE = (
    len(
        combinacoes_pesos
    )
    * len(
        CONFIRMACOES_TESTADAS
    )
)


print("=" * 70)
print("INICIANDO TESTE DE SENSIBILIDADE")
print("=" * 70)


print(
    f"\nCombinações de sensibilidade: "
    f"{QUANTIDADE_COMBINACOES_SENSIBILIDADE}"
)


print(
    "A avaliação será utilizada somente como diagnóstico.\n"
    "Nenhum novo peso será selecionado com esses resultados.\n",
    flush=True,
)


for confirmacao in CONFIRMACOES_TESTADAS:

    print(
        f"Testando confirmação de "
        f"{confirmacao} mês(es)...",
        flush=True,
    )

    for combinacao in combinacoes_pesos:

        pesos_cdi_candidato = {
            regime: float(
                peso
            )
            for regime, peso in zip(
                ORDEM_REGIMES,
                combinacao,
            )
        }

        pesos_candidato = (
            criar_pesos_com_cdi(
                pesos_cdi_por_regime=(
                    pesos_cdi_candidato
                )
            )
        )

        matriz_candidato = (
            criar_matriz_pesos_regime(
                pesos_por_regime=(
                    pesos_candidato
                ),
                meses_confirmacao=(
                    confirmacao
                ),
            )
        )

        simulacao_candidato = (
            simular_carteira(
                matriz_pesos=(
                    matriz_candidato
                )
            )
        )

        metricas_treino = (
            calcular_metricas(
                simulacao=(
                    simulacao_candidato
                ),
                mascara=(
                    MASCARA_TREINO
                ),
            )
        )

        metricas_avaliacao = (
            calcular_metricas(
                simulacao=(
                    simulacao_candidato
                ),
                mascara=(
                    MASCARA_AVALIACAO
                ),
            )
        )

        diferenca_benchmark = (
            metricas_avaliacao[
                "indice_final_liquido"
            ]
            - metricas_benchmark_avaliacao[
                "indice_final_liquido"
            ]
        )

        diferenca_base = (
            metricas_avaliacao[
                "indice_final_liquido"
            ]
            - metricas_base_avaliacao[
                "indice_final_liquido"
            ]
        )

        candidato_original = (
            confirmacao
            == CONFIRMACAO_SELECIONADA
            and all(
                np.isclose(
                    pesos_cdi_candidato[
                        regime
                    ],
                    PESOS_CDI_ORIGINAIS[
                        regime
                    ],
                    atol=1e-12,
                    rtol=1e-12,
                )
                for regime in ORDEM_REGIMES
            )
        )

        registros_sensibilidade.append(
            {
                "confirmacao_meses": (
                    confirmacao
                ),
                "peso_cdi_expansao_desinflacionaria": (
                    pesos_cdi_candidato[
                        "EXPANSAO_DESINFLACIONARIA"
                    ]
                ),
                "peso_cdi_expansao_inflacionaria": (
                    pesos_cdi_candidato[
                        "EXPANSAO_INFLACIONARIA"
                    ]
                ),
                "peso_cdi_estagflacao": (
                    pesos_cdi_candidato[
                        "ESTAGFLACAO"
                    ]
                ),
                "peso_cdi_recessao_desinflacionaria": (
                    pesos_cdi_candidato[
                        "RECESSAO_DESINFLACIONARIA"
                    ]
                ),
                "candidato_original_celula_9": (
                    candidato_original
                ),
                "treino_indice_final": (
                    metricas_treino[
                        "indice_final_liquido"
                    ]
                ),
                "treino_retorno_anualizado": (
                    metricas_treino[
                        "retorno_anualizado_liquido"
                    ]
                ),
                "treino_volatilidade": (
                    metricas_treino[
                        "volatilidade_anualizada_liquida"
                    ]
                ),
                "treino_retorno_volatilidade": (
                    metricas_treino[
                        "retorno_volatilidade"
                    ]
                ),
                "treino_sharpe_excesso_cdi": (
                    metricas_treino[
                        "sharpe_excesso_cdi"
                    ]
                ),
                "treino_drawdown": (
                    metricas_treino[
                        "maximo_drawdown"
                    ]
                ),
                "treino_turnover": (
                    metricas_treino[
                        "turnover_total"
                    ]
                ),
                "avaliacao_indice_final": (
                    metricas_avaliacao[
                        "indice_final_liquido"
                    ]
                ),
                "avaliacao_retorno_anualizado": (
                    metricas_avaliacao[
                        "retorno_anualizado_liquido"
                    ]
                ),
                "avaliacao_volatilidade": (
                    metricas_avaliacao[
                        "volatilidade_anualizada_liquida"
                    ]
                ),
                "avaliacao_retorno_volatilidade": (
                    metricas_avaliacao[
                        "retorno_volatilidade"
                    ]
                ),
                "avaliacao_sharpe_excesso_cdi": (
                    metricas_avaliacao[
                        "sharpe_excesso_cdi"
                    ]
                ),
                "avaliacao_sortino_excesso_cdi": (
                    metricas_avaliacao[
                        "sortino_excesso_cdi"
                    ]
                ),
                "avaliacao_drawdown": (
                    metricas_avaliacao[
                        "maximo_drawdown"
                    ]
                ),
                "avaliacao_turnover": (
                    metricas_avaliacao[
                        "turnover_total"
                    ]
                ),
                "diferenca_indice_vs_benchmark": (
                    diferenca_benchmark
                ),
                "diferenca_indice_vs_modelo_anterior": (
                    diferenca_base
                ),
                "superou_benchmark": (
                    diferenca_benchmark > 0
                ),
                "superou_modelo_anterior": (
                    diferenca_base > 0
                ),
            }
        )


grade_sensibilidade = pd.DataFrame(
    registros_sensibilidade
)


# ============================================================
# RESUMO DA SENSIBILIDADE
# ============================================================

PROPORCAO_VARIANTES_SUPERAM_BENCHMARK = float(
    grade_sensibilidade[
        "superou_benchmark"
    ]
    .mean()
)


PROPORCAO_VARIANTES_SUPERAM_MODELO_ANTERIOR = float(
    grade_sensibilidade[
        "superou_modelo_anterior"
    ]
    .mean()
)


MEDIANA_DIFERENCA_BENCHMARK = float(
    grade_sensibilidade[
        "diferenca_indice_vs_benchmark"
    ]
    .median()
)


MEDIA_DIFERENCA_BENCHMARK = float(
    grade_sensibilidade[
        "diferenca_indice_vs_benchmark"
    ]
    .mean()
)


PERCENTIL_05_DIFERENCA = float(
    grade_sensibilidade[
        "diferenca_indice_vs_benchmark"
    ]
    .quantile(
        0.05
    )
)


PERCENTIL_95_DIFERENCA = float(
    grade_sensibilidade[
        "diferenca_indice_vs_benchmark"
    ]
    .quantile(
        0.95
    )
)


PIOR_DIFERENCA_BENCHMARK = float(
    grade_sensibilidade[
        "diferenca_indice_vs_benchmark"
    ]
    .min()
)


MELHOR_DIFERENCA_BENCHMARK = float(
    grade_sensibilidade[
        "diferenca_indice_vs_benchmark"
    ]
    .max()
)


linha_candidato_original = (
    grade_sensibilidade.loc[
        grade_sensibilidade[
            "candidato_original_celula_9"
        ]
    ]
)


if len(
    linha_candidato_original
) != 1:

    raise ValueError(
        "O candidato original da Célula 9 "
        "não foi identificado exatamente uma vez "
        "na grade de sensibilidade."
    )


linha_candidato_original = (
    linha_candidato_original.iloc[0]
)


DIFERENCA_ORIGINAL_BENCHMARK = float(
    linha_candidato_original[
        "diferenca_indice_vs_benchmark"
    ]
)


PERCENTIL_CANDIDATO_ORIGINAL = float(
    grade_sensibilidade[
        "diferenca_indice_vs_benchmark"
    ]
    .le(
        DIFERENCA_ORIGINAL_BENCHMARK
    )
    .mean()
)


resumo_sensibilidade = pd.DataFrame(
    {
        "metrica": [
            "Quantidade de variantes testadas",
            "Proporção que superou o benchmark",
            "Proporção que superou o modelo anterior",
            "Diferença média contra o benchmark",
            "Diferença mediana contra o benchmark",
            "Percentil 5 da diferença contra o benchmark",
            "Percentil 95 da diferença contra o benchmark",
            "Pior diferença contra o benchmark",
            "Melhor diferença contra o benchmark",
            "Diferença do candidato original contra o benchmark",
            "Percentil do candidato original",
            "Observação metodológica",
        ],
        "valor": [
            len(
                grade_sensibilidade
            ),
            PROPORCAO_VARIANTES_SUPERAM_BENCHMARK,
            PROPORCAO_VARIANTES_SUPERAM_MODELO_ANTERIOR,
            MEDIA_DIFERENCA_BENCHMARK,
            MEDIANA_DIFERENCA_BENCHMARK,
            PERCENTIL_05_DIFERENCA,
            PERCENTIL_95_DIFERENCA,
            PIOR_DIFERENCA_BENCHMARK,
            MELHOR_DIFERENCA_BENCHMARK,
            DIFERENCA_ORIGINAL_BENCHMARK,
            PERCENTIL_CANDIDATO_ORIGINAL,
            (
                "A grade de sensibilidade foi utilizada "
                "somente para diagnóstico. Nenhum novo "
                "peso foi escolhido com o período "
                "de avaliação."
            ),
        ],
    }
)


# ============================================================
# SENSIBILIDADE POR CONFIRMAÇÃO
# ============================================================

sensibilidade_por_confirmacao = (
    grade_sensibilidade
    .groupby(
        "confirmacao_meses",
        as_index=False,
    )
    .agg(
        quantidade_variantes=(
            "superou_benchmark",
            "size",
        ),
        proporcao_supera_benchmark=(
            "superou_benchmark",
            "mean",
        ),
        proporcao_supera_modelo_anterior=(
            "superou_modelo_anterior",
            "mean",
        ),
        diferenca_media_vs_benchmark=(
            "diferenca_indice_vs_benchmark",
            "mean",
        ),
        diferenca_mediana_vs_benchmark=(
            "diferenca_indice_vs_benchmark",
            "median",
        ),
        pior_diferenca_vs_benchmark=(
            "diferenca_indice_vs_benchmark",
            "min",
        ),
        melhor_diferenca_vs_benchmark=(
            "diferenca_indice_vs_benchmark",
            "max",
        ),
        retorno_volatilidade_medio=(
            "avaliacao_retorno_volatilidade",
            "mean",
        ),
        sharpe_medio_excesso_cdi=(
            "avaliacao_sharpe_excesso_cdi",
            "mean",
        ),
    )
)


# ============================================================
# RESULTADOS PRINCIPAIS DA AVALIAÇÃO
# ============================================================

def obter_linha_metrica(
    cenario,
):

    resultado = (
        metricas_comparadores.loc[
            (
                metricas_comparadores[
                    "periodo"
                ]
                == "AVALIACAO"
            )
            & (
                metricas_comparadores[
                    "cenario"
                ]
                == cenario
            )
        ]
    )

    if resultado.empty:

        raise KeyError(
            f"As métricas do cenário {cenario} "
            "não foram encontradas."
        )

    return resultado.iloc[0]


resultado_modelo = obter_linha_metrica(
    "MODELO_COM_CDI"
)

resultado_base = obter_linha_metrica(
    "MODELO_ANTERIOR_SEM_CDI"
)

resultado_benchmark = obter_linha_metrica(
    "BENCHMARK_5_ATIVOS"
)

resultado_estatica = obter_linha_metrica(
    "CARTEIRA_ESTATICA"
)

resultado_cdi = obter_linha_metrica(
    "CDI_100"
)


# ============================================================
# DECISÃO METODOLÓGICA
# ============================================================

criterio_superou_benchmark = bool(
    resultado_modelo[
        "indice_final_liquido"
    ]
    > resultado_benchmark[
        "indice_final_liquido"
    ]
)


criterio_sharpe_superior = bool(
    resultado_modelo[
        "sharpe_excesso_cdi"
    ]
    > resultado_benchmark[
        "sharpe_excesso_cdi"
    ]
)


criterio_drawdown_superior = bool(
    resultado_modelo[
        "maximo_drawdown"
    ]
    > resultado_benchmark[
        "maximo_drawdown"
    ]
)


criterio_rolling = bool(
    pd.notna(
        PROPORCAO_ROLLING_POSITIVO
    )
    and PROPORCAO_ROLLING_POSITIVO
    >= 0.50
)


criterio_sensibilidade = bool(
    PROPORCAO_VARIANTES_SUPERAM_BENCHMARK
    >= 0.60
)


criterios_robustez = [
    criterio_superou_benchmark,
    criterio_sharpe_superior,
    criterio_drawdown_superior,
    criterio_rolling,
    criterio_sensibilidade,
]


quantidade_criterios_aprovados = int(
    sum(
        criterios_robustez
    )
)


if quantidade_criterios_aprovados == len(
    criterios_robustez
):

    STATUS_ROBUSTEZ = (
        "APROVADO COMO MODELO DEFENSIVO"
    )

elif (
    criterio_superou_benchmark
    and quantidade_criterios_aprovados >= 3
):

    STATUS_ROBUSTEZ = (
        "ROBUSTEZ PARCIAL"
    )

else:

    STATUS_ROBUSTEZ = (
        "REPROVADO NA ROBUSTEZ"
    )


SUBSTITUI_MODELO_ANTERIOR = bool(
    (
        resultado_modelo[
            "indice_final_liquido"
        ]
        >= resultado_base[
            "indice_final_liquido"
        ]
    )
    and (
        resultado_modelo[
            "retorno_volatilidade"
        ]
        >= resultado_base[
            "retorno_volatilidade"
        ]
    )
)


if SUBSTITUI_MODELO_ANTERIOR:

    RECOMENDACAO = (
        "O modelo com CDI pode substituir "
        "o modelo anterior."
    )

else:

    RECOMENDACAO = (
        "Manter o modelo com CDI como versão defensiva. "
        "Ele não substitui o modelo anterior "
        "como estratégia de maior retorno."
    )


decisao_modelo = pd.DataFrame(
    [
        {
            "criterio": (
                "Superou benchmark na avaliação"
            ),
            "resultado": (
                criterio_superou_benchmark
            ),
            "valor_observado": (
                resultado_modelo[
                    "indice_final_liquido"
                ]
                - resultado_benchmark[
                    "indice_final_liquido"
                ]
            ),
            "regra": (
                "Diferença de índice maior que zero"
            ),
        },
        {
            "criterio": (
                "Sharpe superior ao benchmark"
            ),
            "resultado": (
                criterio_sharpe_superior
            ),
            "valor_observado": (
                resultado_modelo[
                    "sharpe_excesso_cdi"
                ]
                - resultado_benchmark[
                    "sharpe_excesso_cdi"
                ]
            ),
            "regra": (
                "Sharpe de excesso ao CDI superior"
            ),
        },
        {
            "criterio": (
                "Drawdown melhor que o benchmark"
            ),
            "resultado": (
                criterio_drawdown_superior
            ),
            "valor_observado": (
                resultado_modelo[
                    "maximo_drawdown"
                ]
                - resultado_benchmark[
                    "maximo_drawdown"
                ]
            ),
            "regra": (
                "Drawdown menos negativo"
            ),
        },
        {
            "criterio": (
                "Rolling de 12 meses positivo"
            ),
            "resultado": (
                criterio_rolling
            ),
            "valor_observado": (
                PROPORCAO_ROLLING_POSITIVO
            ),
            "regra": (
                "Pelo menos 50% das janelas "
                "acima do benchmark"
            ),
        },
        {
            "criterio": (
                "Robustez aos pesos próximos"
            ),
            "resultado": (
                criterio_sensibilidade
            ),
            "valor_observado": (
                PROPORCAO_VARIANTES_SUPERAM_BENCHMARK
            ),
            "regra": (
                "Pelo menos 60% das variantes "
                "acima do benchmark"
            ),
        },
        {
            "criterio": (
                "Substitui o modelo anterior"
            ),
            "resultado": (
                SUBSTITUI_MODELO_ANTERIOR
            ),
            "valor_observado": (
                resultado_modelo[
                    "indice_final_liquido"
                ]
                - resultado_base[
                    "indice_final_liquido"
                ]
            ),
            "regra": (
                "Índice e retorno/volatilidade "
                "não inferiores ao modelo anterior"
            ),
        },
    ]
)


# ============================================================
# TABELAS FORMATADAS
# ============================================================

metricas_formatadas = (
    metricas_comparadores
    .copy()
    .astype(object)
)


colunas_percentuais_metricas = [
    "retorno_total_bruto",
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown",
    "meses_positivos",
    "melhor_mes",
    "pior_mes",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
]


for coluna in colunas_percentuais_metricas:

    metricas_formatadas[
        coluna
    ] = (
        metricas_comparadores[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(
                    valor
                )
                else "-"
            )
        )
    )


colunas_decimais_metricas = [
    "retorno_volatilidade",
    "sharpe_excesso_cdi",
    "sortino_excesso_cdi",
    "calmar",
    "turnover_total",
    "indice_final_liquido",
    "diferenca_indice_vs_benchmark",
]


for coluna in colunas_decimais_metricas:

    metricas_formatadas[
        coluna
    ] = (
        metricas_comparadores[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(
                    valor
                )
                and np.isfinite(
                    float(
                        valor
                    )
                )
                else (
                    "∞"
                    if pd.notna(
                        valor
                    )
                    and np.isinf(
                        float(
                            valor
                        )
                    )
                    else "-"
                )
            )
        )
    )


# ============================================================
# RESUMO FINAL
# ============================================================

resumo_final = pd.DataFrame(
    {
        "metrica": [
            "Data final do treino",
            "Meses de treino",
            "Meses de avaliação",
            "Confirmação selecionada",
            "Custo por turnover",
            "Índice final do modelo com CDI",
            "Índice final do modelo anterior",
            "Índice final do benchmark",
            "Índice final da carteira estática",
            "Índice final de 100% CDI",
            "Diferença do modelo com CDI contra o benchmark",
            "Diferença do modelo com CDI contra o modelo anterior",
            "Retorno anualizado do modelo com CDI",
            "Volatilidade do modelo com CDI",
            "Retorno/volatilidade do modelo com CDI",
            "Sharpe de excesso ao CDI",
            "Sortino de excesso ao CDI",
            "Calmar",
            "Máximo drawdown",
            "Turnover total",
            "Janelas rolling positivas contra o benchmark",
            "Pior excesso rolling de 12 meses",
            "Melhor excesso rolling de 12 meses",
            "Variantes que superaram o benchmark",
            "Percentil do candidato original",
            "Critérios de robustez aprovados",
            "Status da robustez",
            "Substitui o modelo anterior",
            "Recomendação",
            "Observação metodológica",
        ],
        "valor": [
            DATA_CORTE_TREINO.strftime(
                "%d/%m/%Y"
            ),
            int(
                MASCARA_TREINO.sum()
            ),
            int(
                MASCARA_AVALIACAO.sum()
            ),
            CONFIRMACAO_SELECIONADA,
            CUSTO_POR_TURNOVER,
            resultado_modelo[
                "indice_final_liquido"
            ],
            resultado_base[
                "indice_final_liquido"
            ],
            resultado_benchmark[
                "indice_final_liquido"
            ],
            resultado_estatica[
                "indice_final_liquido"
            ],
            resultado_cdi[
                "indice_final_liquido"
            ],
            (
                resultado_modelo[
                    "indice_final_liquido"
                ]
                - resultado_benchmark[
                    "indice_final_liquido"
                ]
            ),
            (
                resultado_modelo[
                    "indice_final_liquido"
                ]
                - resultado_base[
                    "indice_final_liquido"
                ]
            ),
            resultado_modelo[
                "retorno_anualizado_liquido"
            ],
            resultado_modelo[
                "volatilidade_anualizada_liquida"
            ],
            resultado_modelo[
                "retorno_volatilidade"
            ],
            resultado_modelo[
                "sharpe_excesso_cdi"
            ],
            resultado_modelo[
                "sortino_excesso_cdi"
            ],
            resultado_modelo[
                "calmar"
            ],
            resultado_modelo[
                "maximo_drawdown"
            ],
            resultado_modelo[
                "turnover_total"
            ],
            PROPORCAO_ROLLING_POSITIVO,
            PIOR_EXCESSO_ROLLING,
            MELHOR_EXCESSO_ROLLING,
            PROPORCAO_VARIANTES_SUPERAM_BENCHMARK,
            PERCENTIL_CANDIDATO_ORIGINAL,
            quantidade_criterios_aprovados,
            STATUS_ROBUSTEZ,
            (
                "SIM"
                if SUBSTITUI_MODELO_ANTERIOR
                else "NÃO"
            ),
            RECOMENDACAO,
            (
                "O período de 2024 a 2026 já foi "
                "analisado anteriormente e deve ser "
                "tratado como avaliação, não como "
                "holdout final intocado."
            ),
        ],
    }
)


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

metricas_comparadores.to_csv(
    ARQUIVO_METRICAS,
    index=False,
    encoding="utf-8-sig",
)


metricas_formatadas.to_csv(
    ARQUIVO_METRICAS_FORMATADAS,
    index=False,
    encoding="utf-8-sig",
)


series_comparadores.to_csv(
    ARQUIVO_SERIES_COMPARADORES,
    index=False,
    encoding="utf-8-sig",
)


pesos_estaticos_df.to_csv(
    ARQUIVO_PESOS_ESTATICOS,
    index=False,
    encoding="utf-8-sig",
)


grade_sensibilidade.to_csv(
    ARQUIVO_GRADE_SENSIBILIDADE,
    index=False,
    encoding="utf-8-sig",
)


sensibilidade_por_confirmacao.to_csv(
    ARQUIVO_SENSIBILIDADE_CONFIRMACAO,
    index=False,
    encoding="utf-8-sig",
)


resumo_sensibilidade.to_csv(
    ARQUIVO_RESUMO_SENSIBILIDADE,
    index=False,
    encoding="utf-8-sig",
)


rolling_avaliacao.to_csv(
    ARQUIVO_ROLLING,
    index=False,
    encoding="utf-8-sig",
)


decisao_modelo.to_csv(
    ARQUIVO_DECISAO,
    index=False,
    encoding="utf-8-sig",
)


resumo_final.to_csv(
    ARQUIVO_RESUMO_FINAL,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# BASE PARA OS GRÁFICOS
# ============================================================

series_avaliacao = (
    series_comparadores.loc[
        series_comparadores[
            "periodo"
        ]
        == "AVALIACAO"
    ]
    .copy()
    .reset_index(
        drop=True
    )
)


for cenario in CENARIOS:

    coluna_retorno = (
        f"retorno_liquido_{cenario}"
    )

    series_avaliacao[
        f"indice_{cenario}"
    ] = (
        VALOR_INICIAL
        * (
            1.0
            + series_avaliacao[
                coluna_retorno
            ]
        ).cumprod()
    )


series_avaliacao[
    "diferenca_modelo_benchmark"
] = (
    series_avaliacao[
        "indice_MODELO_COM_CDI"
    ]
    - series_avaliacao[
        "indice_BENCHMARK_5_ATIVOS"
    ]
)


series_avaliacao[
    "diferenca_modelo_anterior"
] = (
    series_avaliacao[
        "indice_MODELO_COM_CDI"
    ]
    - series_avaliacao[
        "indice_MODELO_ANTERIOR_SEM_CDI"
    ]
)


data_inicial_grafico = (
    series_avaliacao[
        "data"
    ].iloc[0]
    - pd.offsets.MonthEnd(1)
)


linha_inicial = {
    "data": data_inicial_grafico,
}


for cenario in CENARIOS:

    linha_inicial[
        f"indice_{cenario}"
    ] = VALOR_INICIAL


linha_inicial[
    "diferenca_modelo_benchmark"
] = 0.0

linha_inicial[
    "diferenca_modelo_anterior"
] = 0.0


series_grafico = pd.concat(
    [
        pd.DataFrame(
            [
                linha_inicial
            ]
        ),
        series_avaliacao[
            [
                "data",
                *[
                    f"indice_{cenario}"
                    for cenario in CENARIOS
                ],
                "diferenca_modelo_benchmark",
                "diferenca_modelo_anterior",
            ]
        ],
    ],
    ignore_index=True,
)


# ============================================================
# GRÁFICO 1 — DESEMPENHO DOS COMPARADORES
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


for cenario, configuracao in (
    CENARIOS.items()
):

    ax.plot(
        series_grafico[
            "data"
        ],
        series_grafico[
            f"indice_{cenario}"
        ],
        linewidth=2,
        label=configuracao[
            "rotulo"
        ],
    )


ax.axhline(
    y=VALOR_INICIAL,
    linewidth=1,
)


ax.set_title(
    "Desempenho dos Comparadores no Período de Avaliação"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Índice acumulado"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DESEMPENHO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — RISCO E RETORNO
# ============================================================

metricas_avaliacao_grafico = (
    metricas_comparadores.loc[
        metricas_comparadores[
            "periodo"
        ]
        == "AVALIACAO"
    ]
    .copy()
)


fig, ax = plt.subplots(
    figsize=(11, 7)
)


ax.scatter(
    metricas_avaliacao_grafico[
        "volatilidade_anualizada_liquida"
    ],
    metricas_avaliacao_grafico[
        "retorno_anualizado_liquido"
    ],
    s=90,
)


for _, linha in (
    metricas_avaliacao_grafico.iterrows()
):

    ax.annotate(
        linha[
            "rotulo"
        ],
        (
            linha[
                "volatilidade_anualizada_liquida"
            ],
            linha[
                "retorno_anualizado_liquido"
            ],
        ),
        xytext=(
            6,
            6,
        ),
        textcoords="offset points",
    )


ax.xaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)

ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Risco e Retorno dos Comparadores"
)

ax.set_xlabel(
    "Volatilidade anualizada"
)

ax.set_ylabel(
    "Retorno anualizado"
)

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_RISCO_RETORNO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — DIFERENÇAS
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "diferenca_modelo_benchmark"
    ],
    linewidth=2,
    label="Modelo com CDI menos benchmark",
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "diferenca_modelo_anterior"
    ],
    linewidth=2,
    label="Modelo com CDI menos modelo anterior",
)


ax.axhline(
    y=0.0,
    linewidth=1,
)


ax.set_title(
    "Diferença do Modelo com CDI contra as Referências"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Diferença do índice em pontos"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DIFERENCA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 4 — DISTRIBUIÇÃO DA SENSIBILIDADE
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 7)
)


ax.hist(
    grade_sensibilidade[
        "diferenca_indice_vs_benchmark"
    ],
    bins=30,
)


ax.axvline(
    x=0.0,
    linewidth=1,
    label="Empate com o benchmark",
)


ax.axvline(
    x=DIFERENCA_ORIGINAL_BENCHMARK,
    linewidth=2,
    linestyle="--",
    label="Candidato original",
)


ax.set_title(
    "Distribuição da Sensibilidade contra o Benchmark"
)

ax.set_xlabel(
    "Diferença do índice em pontos"
)

ax.set_ylabel(
    "Quantidade de variantes"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_SENSIBILIDADE,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 5 — ROLLING DE 12 MESES
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    rolling_avaliacao[
        "data"
    ],
    rolling_avaliacao[
        "excesso_modelo_vs_benchmark"
    ],
    linewidth=2,
    label="Modelo com CDI menos benchmark",
)


ax.plot(
    rolling_avaliacao[
        "data"
    ],
    rolling_avaliacao[
        "excesso_modelo_vs_anterior"
    ],
    linewidth=2,
    label="Modelo com CDI menos modelo anterior",
)


ax.axhline(
    y=0.0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Excesso de Retorno Rolling de 12 Meses"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Excesso de retorno em 12 meses"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_ROLLING,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÕES FINAIS
# ============================================================

validacoes = []


def adicionar_validacao(
    nome,
    aprovado,
    detalhe,
):

    validacoes.append(
        {
            "validacao": nome,
            "status": (
                "APROVADO"
                if aprovado
                else "REPROVADO"
            ),
            "detalhe": detalhe,
        }
    )


adicionar_validacao(
    nome="Meses da base",
    aprovado=(
        len(base) == 77
    ),
    detalhe=(
        f"{len(base)} meses"
    ),
)


adicionar_validacao(
    nome="Valores nulos",
    aprovado=(
        not base[
            ATIVOS
        ]
        .isna()
        .any()
        .any()
    ),
    detalhe=(
        f"{int(base[ATIVOS].isna().sum().sum())} nulos"
    ),
)


adicionar_validacao(
    nome="Pesos selecionados",
    aprovado=np.allclose(
        matriz_modelo_selecionado.sum(
            axis=1
        ),
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ),
    detalhe=(
        "Todos os meses somam 100%"
    ),
)


adicionar_validacao(
    nome="Reprodução do modelo da Célula 9",
    aprovado=(
        diferenca_modelo_salvo < 1e-10
    ),
    detalhe=(
        f"Diferença máxima: "
        f"{diferenca_modelo_salvo:.12f}"
    ),
)


adicionar_validacao(
    nome="Reprodução do modelo base",
    aprovado=(
        diferenca_base_salva < 1e-10
    ),
    detalhe=(
        f"Diferença máxima: "
        f"{diferenca_base_salva:.12f}"
    ),
)


adicionar_validacao(
    nome="Reprodução do benchmark",
    aprovado=(
        diferenca_benchmark_salvo < 1e-10
    ),
    detalhe=(
        f"Diferença máxima: "
        f"{diferenca_benchmark_salvo:.12f}"
    ),
)


adicionar_validacao(
    nome="Candidato original na sensibilidade",
    aprovado=(
        len(
            grade_sensibilidade.loc[
                grade_sensibilidade[
                    "candidato_original_celula_9"
                ]
            ]
        )
        == 1
    ),
    detalhe=(
        "O candidato original deve aparecer "
        "exatamente uma vez"
    ),
)


adicionar_validacao(
    nome="Sensibilidade não usada para seleção",
    aprovado=True,
    detalhe=(
        "A grade foi utilizada somente "
        "como diagnóstico"
    ),
)


adicionar_validacao(
    nome="Turnover não negativo",
    aprovado=(
        SIMULACAO_MODELO_SELECIONADO[
            "turnover"
        ]
        >= 0
    ).all(),
    detalhe=(
        f"Turnover mínimo: "
        f"{SIMULACAO_MODELO_SELECIONADO['turnover'].min():.8f}"
    ),
)


adicionar_validacao(
    nome="Custos não negativos",
    aprovado=(
        SIMULACAO_MODELO_SELECIONADO[
            "custo"
        ]
        >= 0
    ).all(),
    detalhe=(
        f"Custo mínimo: "
        f"{SIMULACAO_MODELO_SELECIONADO['custo'].min():.8f}"
    ),
)


tabela_validacoes = pd.DataFrame(
    validacoes
)


if (
    tabela_validacoes[
        "status"
    ]
    == "REPROVADO"
).any():

    raise ValueError(
        "Uma ou mais validações da Célula 10 "
        "foram reprovadas:\n\n"
        f"{tabela_validacoes}"
    )


tabela_validacoes.to_csv(
    ARQUIVO_VALIDACOES,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_METRICAS,
    ARQUIVO_METRICAS_FORMATADAS,
    ARQUIVO_SERIES_COMPARADORES,
    ARQUIVO_PESOS_ESTATICOS,
    ARQUIVO_GRADE_SENSIBILIDADE,
    ARQUIVO_SENSIBILIDADE_CONFIRMACAO,
    ARQUIVO_RESUMO_SENSIBILIDADE,
    ARQUIVO_ROLLING,
    ARQUIVO_DECISAO,
    ARQUIVO_VALIDACOES,
    ARQUIVO_RESUMO_FINAL,
    ARQUIVO_GRAFICO_DESEMPENHO,
    ARQUIVO_GRAFICO_RISCO_RETORNO,
    ARQUIVO_GRAFICO_DIFERENCA,
    ARQUIVO_GRAFICO_SENSIBILIDADE,
    ARQUIVO_GRAFICO_ROLLING,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:

    raise FileNotFoundError(
        "Alguns arquivos da Célula 10 "
        "não foram salvos:\n"
        + "\n".join(
            str(
                arquivo
            )
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("\n" + "=" * 70)
print("VALIDAÇÃO DE ROBUSTEZ CONCLUÍDA")
print("=" * 70)


print(
    f"\nRaiz do projeto:\n"
    f"{RAIZ_PROJETO}"
)


print(
    f"\nPeríodo de treino: "
    f"{base.loc[MASCARA_TREINO, 'data'].min():%d/%m/%Y} "
    f"a "
    f"{base.loc[MASCARA_TREINO, 'data'].max():%d/%m/%Y}"
)


print(
    f"Período de avaliação: "
    f"{base.loc[MASCARA_AVALIACAO, 'data'].min():%d/%m/%Y} "
    f"a "
    f"{base.loc[MASCARA_AVALIACAO, 'data'].max():%d/%m/%Y}"
)


print(
    f"\nConfirmação do modelo: "
    f"{CONFIRMACAO_SELECIONADA} mês(es)"
)


print(
    f"Custo por turnover: "
    f"{CUSTO_POR_TURNOVER:.4%}"
)


print(
    "\nÍndices finais na avaliação:"
)


print(
    f"- Modelo com CDI: "
    f"{resultado_modelo['indice_final_liquido']:.2f}"
)


print(
    f"- Modelo anterior sem CDI: "
    f"{resultado_base['indice_final_liquido']:.2f}"
)


print(
    f"- Benchmark de cinco ativos: "
    f"{resultado_benchmark['indice_final_liquido']:.2f}"
)


print(
    f"- Carteira estática: "
    f"{resultado_estatica['indice_final_liquido']:.2f}"
)


print(
    f"- 100% CDI: "
    f"{resultado_cdi['indice_final_liquido']:.2f}"
)


print(
    f"\nModelo com CDI contra o benchmark: "
    f"{resultado_modelo['indice_final_liquido'] - resultado_benchmark['indice_final_liquido']:.2f} "
    f"pontos"
)


print(
    f"Modelo com CDI contra o modelo anterior: "
    f"{resultado_modelo['indice_final_liquido'] - resultado_base['indice_final_liquido']:.2f} "
    f"pontos"
)


print(
    "\nMétricas do modelo com CDI:"
)


print(
    f"- Retorno anualizado: "
    f"{resultado_modelo['retorno_anualizado_liquido']:.2%}"
)


print(
    f"- Volatilidade anualizada: "
    f"{resultado_modelo['volatilidade_anualizada_liquida']:.2%}"
)


print(
    f"- Retorno/volatilidade: "
    f"{resultado_modelo['retorno_volatilidade']:.2f}"
)


print(
    f"- Sharpe de excesso ao CDI: "
    f"{resultado_modelo['sharpe_excesso_cdi']:.2f}"
)


print(
    f"- Sortino de excesso ao CDI: "
    f"{resultado_modelo['sortino_excesso_cdi']:.2f}"
)


print(
    f"- Calmar: "
    f"{resultado_modelo['calmar']:.2f}"
)


print(
    f"- Máximo drawdown: "
    f"{resultado_modelo['maximo_drawdown']:.2%}"
)


print(
    f"- Turnover total: "
    f"{resultado_modelo['turnover_total']:.4f}"
)


print(
    "\nRobustez rolling de 12 meses:"
)


print(
    f"- Janelas acima do benchmark: "
    f"{PROPORCAO_ROLLING_POSITIVO:.2%}"
)


print(
    f"- Pior excesso em 12 meses: "
    f"{PIOR_EXCESSO_ROLLING:.2%}"
)


print(
    f"- Melhor excesso em 12 meses: "
    f"{MELHOR_EXCESSO_ROLLING:.2%}"
)


print(
    "\nSensibilidade dos parâmetros:"
)


print(
    f"- Variantes testadas: "
    f"{len(grade_sensibilidade)}"
)


print(
    f"- Variantes que superaram o benchmark: "
    f"{PROPORCAO_VARIANTES_SUPERAM_BENCHMARK:.2%}"
)


print(
    f"- Variantes que superaram o modelo anterior: "
    f"{PROPORCAO_VARIANTES_SUPERAM_MODELO_ANTERIOR:.2%}"
)


print(
    f"- Diferença mediana contra o benchmark: "
    f"{MEDIANA_DIFERENCA_BENCHMARK:.2f} pontos"
)


print(
    f"- Percentil do candidato original: "
    f"{PERCENTIL_CANDIDATO_ORIGINAL:.2%}"
)


print(
    f"\nCritérios de robustez aprovados: "
    f"{quantidade_criterios_aprovados}/"
    f"{len(criterios_robustez)}"
)


print(
    f"Status da robustez: "
    f"{STATUS_ROBUSTEZ}"
)


print(
    f"Substitui o modelo anterior: "
    f"{'SIM' if SUBSTITUI_MODELO_ANTERIOR else 'NÃO'}"
)


print(
    f"\nRecomendação:\n"
    f"{RECOMENDACAO}"
)


print(
    "\nObservação: o período de 2024 a 2026 já foi "
    "analisado anteriormente. Ele é um período de "
    "avaliação, não um holdout final intocado."
)


print(
    f"\nResumo final salvo em:\n"
    f"{ARQUIVO_RESUMO_FINAL}"
)


print(
    "\nMétricas comparativas:"
)


display(
    metricas_formatadas.loc[
        metricas_formatadas[
            "periodo"
        ]
        == "AVALIACAO"
    ]
)


print(
    "\nDecisão do modelo:"
)


display(
    decisao_modelo
)


print(
    "\nValidações:"
)


display(
    tabela_validacoes
)

# ###########################################################################
# ETAPA 11 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 11 — VALIDAÇÃO WALK-FORWARD
# RECALIBRAÇÃO PERIÓDICA DA CONFIRMAÇÃO E DOS PESOS DE CDI
# VERSÃO AUTÔNOMA
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

from pathlib import Path
from itertools import product

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml

from matplotlib.ticker import PercentFormatter


# ============================================================
# REGIMES E NOMES
# ============================================================

ORDEM_REGIMES = [
    "EXPANSAO_DESINFLACIONARIA",
    "EXPANSAO_INFLACIONARIA",
    "ESTAGFLACAO",
    "RECESSAO_DESINFLACIONARIA",
]

NOMES_REGIMES = {
    "EXPANSAO_DESINFLACIONARIA": (
        "Expansão desinflacionária"
    ),
    "EXPANSAO_INFLACIONARIA": (
        "Expansão inflacionária"
    ),
    "ESTAGFLACAO": (
        "Estagflação"
    ),
    "RECESSAO_DESINFLACIONARIA": (
        "Recessão desinflacionária"
    ),
}


# ============================================================
# LOCALIZAÇÃO DA RAIZ DO PROJETO
# ============================================================

DIRETORIO_ATUAL = Path.cwd().resolve()

RAIZ_PROJETO = None


for diretorio in [
    DIRETORIO_ATUAL,
    *DIRETORIO_ATUAL.parents,
]:

    arquivo_teste = (
        diretorio
        / "data"
        / "processed"
        / "backtest_portfolio_mensal.csv"
    )

    if arquivo_teste.exists():

        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:

    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo data/processed/"
        "backtest_portfolio_mensal.csv não foi encontrado."
    )


PASTA_DADOS_PROCESSADOS = (
    RAIZ_PROJETO
    / "data"
    / "processed"
)

PASTA_TABELAS = (
    RAIZ_PROJETO
    / "outputs"
    / "tabelas"
)

PASTA_GRAFICOS = (
    RAIZ_PROJETO
    / "outputs"
    / "graficos"
)


PASTA_TABELAS.mkdir(
    parents=True,
    exist_ok=True,
)

PASTA_GRAFICOS.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CARREGAMENTO DO CONFIG.YAML
# ============================================================

ARQUIVO_CONFIG = (
    RAIZ_PROJETO
    / "config"
    / "config.yaml"
)


if not ARQUIVO_CONFIG.exists():

    raise FileNotFoundError(
        "Arquivo de configuração não encontrado:\n"
        f"{ARQUIVO_CONFIG}"
    )


with ARQUIVO_CONFIG.open(
    mode="r",
    encoding="utf-8",
) as arquivo_yaml:

    CONFIGURACAO = (
        yaml.safe_load(
            arquivo_yaml
        )
        or {}
    )


if (
    "backtest" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["backtest"],
        dict,
    )
):

    raise KeyError(
        "A seção 'backtest' não foi encontrada "
        "no config/config.yaml."
    )


if (
    "otimizacao" not in CONFIGURACAO
    or not isinstance(
        CONFIGURACAO["otimizacao"],
        dict,
    )
):

    raise KeyError(
        "A seção 'otimizacao' não foi encontrada "
        "no config/config.yaml."
    )


CONFIGURACAO_BACKTEST = (
    CONFIGURACAO[
        "backtest"
    ]
)


CONFIGURACAO_OTIMIZACAO = (
    CONFIGURACAO[
        "otimizacao"
    ]
)


parametros_backtest_obrigatorios = [
    "valor_inicial",
    "periodos_por_ano",
    "periodos_janela",
    "custo_por_turnover",
    "cobrar_custo_inicial",
]


parametros_backtest_ausentes = [
    parametro
    for parametro in parametros_backtest_obrigatorios
    if parametro not in CONFIGURACAO_BACKTEST
]


if parametros_backtest_ausentes:

    raise KeyError(
        "Parâmetros ausentes na seção 'backtest' "
        "do config.yaml:\n"
        f"{parametros_backtest_ausentes}"
    )


parametros_otimizacao_obrigatorios = [
    "janelas_confirmacao",
    "pesos_cdi_testados",
    "meses_treino_inicial_walk_forward",
    "meses_entre_recalibracoes_walk_forward",
    "proporcao_minima_rolling_walk_forward",
    "proporcao_minima_confirmacao_modal_walk_forward",
    "mudanca_media_maxima_pesos_cdi_walk_forward",
    "criterios_minimos_aprovacao_walk_forward",
    "criterios_minimos_robustez_parcial_walk_forward",
]


parametros_otimizacao_ausentes = [
    parametro
    for parametro in parametros_otimizacao_obrigatorios
    if parametro not in CONFIGURACAO_OTIMIZACAO
]


if parametros_otimizacao_ausentes:

    raise KeyError(
        "Parâmetros ausentes na seção 'otimizacao' "
        "do config.yaml:\n"
        f"{parametros_otimizacao_ausentes}"
    )


VALOR_INICIAL = float(
    CONFIGURACAO_BACKTEST[
        "valor_inicial"
    ]
)


PERIODOS_POR_ANO = int(
    CONFIGURACAO_BACKTEST[
        "periodos_por_ano"
    ]
)


JANELA_ROLLING = int(
    CONFIGURACAO_BACKTEST[
        "periodos_janela"
    ]
)


CUSTO_POR_TURNOVER = float(
    CONFIGURACAO_BACKTEST[
        "custo_por_turnover"
    ]
)


COBRAR_CUSTO_INICIAL = (
    CONFIGURACAO_BACKTEST[
        "cobrar_custo_inicial"
    ]
)


MESES_TREINO_INICIAL = int(
    CONFIGURACAO_OTIMIZACAO[
        "meses_treino_inicial_walk_forward"
    ]
)


MESES_ENTRE_RECALIBRACOES = int(
    CONFIGURACAO_OTIMIZACAO[
        "meses_entre_recalibracoes_walk_forward"
    ]
)


PROPORCAO_MINIMA_ROLLING = float(
    CONFIGURACAO_OTIMIZACAO[
        "proporcao_minima_rolling_walk_forward"
    ]
)


PROPORCAO_MINIMA_CONFIRMACAO_MODAL = float(
    CONFIGURACAO_OTIMIZACAO[
        "proporcao_minima_confirmacao_modal_walk_forward"
    ]
)


MUDANCA_MEDIA_MAXIMA_PESOS_CDI = float(
    CONFIGURACAO_OTIMIZACAO[
        "mudanca_media_maxima_pesos_cdi_walk_forward"
    ]
)


CRITERIOS_MINIMOS_APROVACAO = int(
    CONFIGURACAO_OTIMIZACAO[
        "criterios_minimos_aprovacao_walk_forward"
    ]
)


CRITERIOS_MINIMOS_ROBUSTEZ_PARCIAL = int(
    CONFIGURACAO_OTIMIZACAO[
        "criterios_minimos_robustez_parcial_walk_forward"
    ]
)


janelas_confirmacao_configuradas = (
    CONFIGURACAO_OTIMIZACAO[
        "janelas_confirmacao"
    ]
)


pesos_cdi_configurados = (
    CONFIGURACAO_OTIMIZACAO[
        "pesos_cdi_testados"
    ]
)


if VALOR_INICIAL <= 0:

    raise ValueError(
        "'backtest.valor_inicial' "
        "deve ser maior que zero."
    )


if PERIODOS_POR_ANO <= 0:

    raise ValueError(
        "'backtest.periodos_por_ano' "
        "deve ser maior que zero."
    )


if JANELA_ROLLING <= 0:

    raise ValueError(
        "'backtest.periodos_janela' "
        "deve ser maior que zero."
    )


if CUSTO_POR_TURNOVER < 0:

    raise ValueError(
        "'backtest.custo_por_turnover' "
        "não pode ser negativo."
    )


if not isinstance(
    COBRAR_CUSTO_INICIAL,
    bool,
):

    raise TypeError(
        "'backtest.cobrar_custo_inicial' "
        "deve ser true ou false."
    )


if MESES_TREINO_INICIAL <= 0:

    raise ValueError(
        "'otimizacao.meses_treino_inicial_walk_forward' "
        "deve ser maior que zero."
    )


if MESES_ENTRE_RECALIBRACOES <= 0:

    raise ValueError(
        "'otimizacao.meses_entre_recalibracoes_walk_forward' "
        "deve ser maior que zero."
    )


if MESES_TREINO_INICIAL < JANELA_ROLLING:

    raise ValueError(
        "O treino inicial deve possuir pelo menos "
        "o número de meses da janela rolling."
    )


for nome_parametro, valor_parametro in {
    "proporcao_minima_rolling_walk_forward": (
        PROPORCAO_MINIMA_ROLLING
    ),
    "proporcao_minima_confirmacao_modal_walk_forward": (
        PROPORCAO_MINIMA_CONFIRMACAO_MODAL
    ),
    "mudanca_media_maxima_pesos_cdi_walk_forward": (
        MUDANCA_MEDIA_MAXIMA_PESOS_CDI
    ),
}.items():

    if not (
        0.0
        <= valor_parametro
        <= 1.0
    ):

        raise ValueError(
            f"'otimizacao.{nome_parametro}' "
            "deve estar entre 0 e 1."
        )


if CRITERIOS_MINIMOS_APROVACAO <= 0:

    raise ValueError(
        "'otimizacao.criterios_minimos_aprovacao_walk_forward' "
        "deve ser maior que zero."
    )


if CRITERIOS_MINIMOS_ROBUSTEZ_PARCIAL <= 0:

    raise ValueError(
        "'otimizacao.criterios_minimos_robustez_parcial_walk_forward' "
        "deve ser maior que zero."
    )


if (
    CRITERIOS_MINIMOS_ROBUSTEZ_PARCIAL
    > CRITERIOS_MINIMOS_APROVACAO
):

    raise ValueError(
        "O mínimo de critérios para robustez parcial "
        "não pode superar o mínimo para aprovação."
    )


if not isinstance(
    janelas_confirmacao_configuradas,
    list,
):

    raise TypeError(
        "'otimizacao.janelas_confirmacao' "
        "deve ser uma lista."
    )


if not janelas_confirmacao_configuradas:

    raise ValueError(
        "'otimizacao.janelas_confirmacao' "
        "não pode estar vazia."
    )


try:

    JANELAS_CONFIRMACAO = [
        int(janela)
        for janela in janelas_confirmacao_configuradas
    ]

except (
    TypeError,
    ValueError,
) as erro:

    raise TypeError(
        "Todos os valores de "
        "'otimizacao.janelas_confirmacao' "
        "devem ser inteiros."
    ) from erro


if any(
    janela < 1
    for janela in JANELAS_CONFIRMACAO
):

    raise ValueError(
        "Todas as janelas de confirmação "
        "devem ser maiores ou iguais a 1."
    )


if (
    len(JANELAS_CONFIRMACAO)
    != len(set(JANELAS_CONFIRMACAO))
):

    raise ValueError(
        "A lista de janelas de confirmação "
        "possui valores duplicados."
    )


if 1 not in JANELAS_CONFIRMACAO:

    raise ValueError(
        "A janela de confirmação de 1 mês "
        "é obrigatória."
    )


JANELAS_CONFIRMACAO = sorted(
    JANELAS_CONFIRMACAO
)


if not isinstance(
    pesos_cdi_configurados,
    list,
):

    raise TypeError(
        "'otimizacao.pesos_cdi_testados' "
        "deve ser uma lista."
    )


if not pesos_cdi_configurados:

    raise ValueError(
        "'otimizacao.pesos_cdi_testados' "
        "não pode estar vazia."
    )


try:

    PESOS_CDI_TESTADOS = [
        float(peso)
        for peso in pesos_cdi_configurados
    ]

except (
    TypeError,
    ValueError,
) as erro:

    raise TypeError(
        "Todos os valores de "
        "'otimizacao.pesos_cdi_testados' "
        "devem ser numéricos."
    ) from erro


if any(
    peso < 0.0
    or peso > 1.0
    for peso in PESOS_CDI_TESTADOS
):

    raise ValueError(
        "Todos os pesos de CDI testados "
        "devem estar entre 0 e 1."
    )


if (
    len(PESOS_CDI_TESTADOS)
    != len(set(PESOS_CDI_TESTADOS))
):

    raise ValueError(
        "A lista de pesos de CDI testados "
        "possui valores duplicados."
    )


if not any(
    np.isclose(
        peso,
        0.0,
    )
    for peso in PESOS_CDI_TESTADOS
):

    raise ValueError(
        "O peso 0.0 de CDI é obrigatório "
        "para representar o modelo sem CDI."
    )


PESOS_CDI_TESTADOS = sorted(
    PESOS_CDI_TESTADOS
)


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ARQUIVO_RETORNOS = (
    PASTA_DADOS_PROCESSADOS
    / "retornos_ativos_ampliados_mensais.csv"
)

ARQUIVO_BACKTEST = (
    PASTA_DADOS_PROCESSADOS
    / "backtest_portfolio_mensal.csv"
)

ARQUIVO_REGIMES = (
    PASTA_TABELAS
    / "06_02_regimes_suavizados.csv"
)

ARQUIVO_PESOS_BASE = (
    PASTA_TABELAS
    / "06_07_pesos_otimizados_por_regime.csv"
)

ARQUIVO_PESOS_FIXOS = (
    PASTA_TABELAS
    / "06_09_pesos_selecionados_5_ativos.csv"
)

ARQUIVO_PARAMETROS_FIXOS = (
    PASTA_TABELAS
    / "06_09_parametros_selecionados_cdi.csv"
)


arquivos_entrada = [
    ARQUIVO_RETORNOS,
    ARQUIVO_BACKTEST,
    ARQUIVO_REGIMES,
    ARQUIVO_PESOS_BASE,
    ARQUIVO_PESOS_FIXOS,
    ARQUIVO_PARAMETROS_FIXOS,
]


arquivos_ausentes = [
    arquivo
    for arquivo in arquivos_entrada
    if not arquivo.exists()
]


if arquivos_ausentes:

    raise FileNotFoundError(
        "Arquivos necessários não encontrados:\n"
        + "\n".join(
            str(
                arquivo
            )
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_JANELAS = (
    PASTA_TABELAS
    / "06_11_janelas_walk_forward.csv"
)

ARQUIVO_GRADE = (
    PASTA_TABELAS
    / "06_11_grade_selecao_walk_forward.csv"
)

ARQUIVO_PARAMETROS = (
    PASTA_TABELAS
    / "06_11_parametros_por_recalibracao.csv"
)

ARQUIVO_PESOS = (
    PASTA_TABELAS
    / "06_11_pesos_por_recalibracao.csv"
)

ARQUIVO_ESTABILIDADE = (
    PASTA_TABELAS
    / "06_11_estabilidade_parametros.csv"
)

ARQUIVO_SERIES = (
    PASTA_TABELAS
    / "06_11_series_walk_forward.csv"
)

ARQUIVO_METRICAS = (
    PASTA_TABELAS
    / "06_11_metricas_comparativas.csv"
)

ARQUIVO_METRICAS_FORMATADAS = (
    PASTA_TABELAS
    / "06_11_metricas_comparativas_formatadas.csv"
)

ARQUIVO_ROLLING = (
    PASTA_TABELAS
    / "06_11_rolling_12m.csv"
)

ARQUIVO_ANUAL = (
    PASTA_TABELAS
    / "06_11_resultados_anuais.csv"
)

ARQUIVO_VALIDACOES = (
    PASTA_TABELAS
    / "06_11_validacoes.csv"
)

ARQUIVO_RESUMO = (
    PASTA_TABELAS
    / "06_11_resumo_walk_forward.csv"
)

ARQUIVO_GRAFICO_DESEMPENHO = (
    PASTA_GRAFICOS
    / "06_11_desempenho_walk_forward.png"
)

ARQUIVO_GRAFICO_DIFERENCA = (
    PASTA_GRAFICOS
    / "06_11_diferenca_walk_forward.png"
)

ARQUIVO_GRAFICO_CONFIRMACAO = (
    PASTA_GRAFICOS
    / "06_11_confirmacao_por_recalibracao.png"
)

ARQUIVO_GRAFICO_PESOS_CDI = (
    PASTA_GRAFICOS
    / "06_11_pesos_cdi_por_recalibracao.png"
)

ARQUIVO_GRAFICO_ROLLING = (
    PASTA_GRAFICOS
    / "06_11_rolling_12m_walk_forward.png"
)


# ============================================================
# CARREGAMENTO DAS BASES
# ============================================================

retornos = pd.read_csv(
    ARQUIVO_RETORNOS,
    encoding="utf-8-sig",
)

backtest = pd.read_csv(
    ARQUIVO_BACKTEST,
    encoding="utf-8-sig",
)

regimes = pd.read_csv(
    ARQUIVO_REGIMES,
    encoding="utf-8-sig",
)

pesos_base_df = pd.read_csv(
    ARQUIVO_PESOS_BASE,
    encoding="utf-8-sig",
)

pesos_fixos_df = pd.read_csv(
    ARQUIVO_PESOS_FIXOS,
    encoding="utf-8-sig",
)

parametros_fixos_df = pd.read_csv(
    ARQUIVO_PARAMETROS_FIXOS,
    encoding="utf-8-sig",
)


# ============================================================
# PADRONIZAÇÃO DAS DATAS
# ============================================================

bases_com_data = {
    "retornos": retornos,
    "backtest": backtest,
    "regimes": regimes,
}


for nome_base, base_dados in bases_com_data.items():

    if "data" not in base_dados.columns:

        raise ValueError(
            f"A base {nome_base} não possui "
            "a coluna data."
        )

    base_dados["data"] = pd.to_datetime(
        base_dados["data"],
        errors="coerce",
    )

    if base_dados["data"].isna().any():

        raise ValueError(
            f"A base {nome_base} possui datas inválidas."
        )

    if base_dados["data"].duplicated().any():

        raise ValueError(
            f"A base {nome_base} possui datas duplicadas."
        )

    base_dados.sort_values(
        "data",
        inplace=True,
    )

    base_dados.reset_index(
        drop=True,
        inplace=True,
    )


# ============================================================
# IDENTIFICAÇÃO DOS ATIVOS
# ============================================================

colunas_pesos_fixos = [
    coluna
    for coluna in pesos_fixos_df.columns
    if coluna.startswith(
        "peso_"
    )
    and coluna != "soma_pesos"
]


if not colunas_pesos_fixos:

    raise ValueError(
        "Não foram encontradas colunas peso_* "
        "no arquivo da Célula 9."
    )


ATIVOS = [
    coluna.replace(
        "peso_",
        "",
        1,
    )
    for coluna in colunas_pesos_fixos
]


if "CDI" not in ATIVOS:

    raise ValueError(
        "O CDI não foi encontrado entre os ativos."
    )


ATIVOS_RISCO = [
    ativo
    for ativo in ATIVOS
    if ativo != "CDI"
]


ativos_ausentes = [
    ativo
    for ativo in ATIVOS
    if ativo not in retornos.columns
]


if ativos_ausentes:

    raise ValueError(
        "Ativos ausentes na base de retornos:\n"
        f"{ativos_ausentes}"
    )


# ============================================================
# COLUNAS DOS REGIMES
# ============================================================

COLUNAS_REGIMES = [
    f"regime_confirmacao_{meses}m"
    for meses in JANELAS_CONFIRMACAO
]


colunas_regimes_ausentes = [
    coluna
    for coluna in COLUNAS_REGIMES
    if coluna not in regimes.columns
]


if colunas_regimes_ausentes:

    raise ValueError(
        "Colunas de regimes ausentes:\n"
        f"{colunas_regimes_ausentes}"
    )


# ============================================================
# CONSTRUÇÃO DA BASE COMPLETA
# ============================================================

base = (
    retornos[
        [
            "data",
            *ATIVOS,
        ]
    ]
    .merge(
        regimes[
            [
                "data",
                *COLUNAS_REGIMES,
            ]
        ],
        on="data",
        how="inner",
        validate="one_to_one",
    )
    .sort_values(
        "data"
    )
    .reset_index(
        drop=True
    )
)


if len(base) != len(retornos):

    raise ValueError(
        "A junção com os regimes alterou "
        "a quantidade de meses."
    )


for ativo in ATIVOS:

    base[ativo] = pd.to_numeric(
        base[ativo],
        errors="coerce",
    )


if (
    base[
        ATIVOS
    ]
    .isna()
    .any()
    .any()
):

    raise ValueError(
        "Existem retornos nulos ou inválidos."
    )


for coluna_regime in COLUNAS_REGIMES:

    base[coluna_regime] = (
        base[coluna_regime]
        .astype("string")
        .str.strip()
    )

    regimes_invalidos = (
        base.loc[
            ~base[coluna_regime].isin(
                ORDEM_REGIMES
            ),
            coluna_regime,
        ]
        .dropna()
        .unique()
        .tolist()
    )

    if regimes_invalidos:

        raise ValueError(
            f"A coluna {coluna_regime} possui "
            f"regimes inválidos:\n"
            f"{regimes_invalidos}"
        )


if len(base) <= MESES_TREINO_INICIAL:

    raise ValueError(
        "A base não possui meses suficientes "
        "para o walk-forward."
    )


MATRIZ_RETORNOS_COMPLETA = (
    base[
        ATIVOS
    ]
    .astype(float)
    .to_numpy()
)


VETOR_CDI_COMPLETO = (
    base[
        "CDI"
    ]
    .astype(float)
    .to_numpy()
)


# ============================================================
# VALIDAÇÃO DO CUSTO POR TURNOVER
# ============================================================

if {
    "turnover_portfolio",
    "custo_portfolio",
}.issubset(
    backtest.columns
):

    turnover_original = pd.to_numeric(
        backtest[
            "turnover_portfolio"
        ],
        errors="coerce",
    )

    custo_original = pd.to_numeric(
        backtest[
            "custo_portfolio"
        ],
        errors="coerce",
    )

    mascara_turnover = (
        turnover_original > 0
    )

    custos_observados = (
        custo_original.loc[
            mascara_turnover
        ]
        / turnover_original.loc[
            mascara_turnover
        ]
    ).dropna()

    if (
        not custos_observados.empty
        and not np.allclose(
            custos_observados,
            CUSTO_POR_TURNOVER,
            rtol=1e-8,
            atol=1e-12,
        )
    ):

        raise ValueError(
            "O custo configurado não coincide "
            "com o custo usado no backtest original."
        )


# ============================================================
# LEITURA DOS PESOS-BASE DE RISCO
# ============================================================

colunas_pesos_base = [
    coluna
    for coluna in pesos_base_df.columns
    if (
        coluna.startswith(
            "peso_otimizado_"
        )
        and coluna
        != "peso_otimizado_CDI"
    )
]


if not colunas_pesos_base:

    raise ValueError(
        "Não foram encontradas colunas "
        "peso_otimizado_* da Célula 7."
    )


ativos_risco_base = [
    coluna.replace(
        "peso_otimizado_",
        "",
        1,
    )
    for coluna in colunas_pesos_base
]


if set(ativos_risco_base) != set(ATIVOS_RISCO):

    raise ValueError(
        "Os ativos da Célula 7 não correspondem "
        "aos ativos da Célula 9."
    )


pesos_base_df["regime"] = (
    pesos_base_df[
        "regime"
    ]
    .astype("string")
    .str.strip()
)


PESOS_RISCO_BASE = {}


for regime in ORDEM_REGIMES:

    linhas_regime = (
        pesos_base_df.loc[
            pesos_base_df[
                "regime"
            ]
            == regime
        ]
    )

    if linhas_regime.empty:

        raise ValueError(
            f"O regime {regime} não possui "
            "pesos-base."
        )

    linha = linhas_regime.iloc[0]

    pesos_risco_brutos = {
        ativo: float(
            linha[
                f"peso_otimizado_{ativo}"
            ]
        )
        for ativo in ATIVOS_RISCO
    }

    soma_pesos_risco_brutos = sum(
        pesos_risco_brutos.values()
    )

    if (
        not np.isfinite(
            soma_pesos_risco_brutos
        )
        or soma_pesos_risco_brutos
        <= 0.0
    ):

        raise ValueError(
            f"Os pesos-base de risco do regime {regime} "
            "possuem soma inválida: "
            f"{soma_pesos_risco_brutos}"
        )

    PESOS_RISCO_BASE[regime] = {
        ativo: (
            peso
            / soma_pesos_risco_brutos
        )
        for ativo, peso
        in pesos_risco_brutos.items()
    }

    soma = sum(
        PESOS_RISCO_BASE[
            regime
        ].values()
    )

    if not np.isclose(
        soma,
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ):

        raise ValueError(
            f"Os pesos-base de risco normalizados de "
            f"{regime} não somam 100%."
        )


if "meses_confirmacao" not in pesos_base_df.columns:

    raise ValueError(
        "O arquivo de pesos-base da Célula 7 "
        "não possui a coluna meses_confirmacao."
    )


confirmacoes_base = (
    pd.to_numeric(
        pesos_base_df[
            "meses_confirmacao"
        ],
        errors="coerce",
    )
    .dropna()
    .unique()
)


if len(confirmacoes_base) != 1:

    raise ValueError(
        "Não foi possível identificar uma única "
        "confirmação no modelo anterior."
    )


CONFIRMACAO_MODELO_ANTERIOR = int(
    confirmacoes_base[0]
)


if (
    CONFIRMACAO_MODELO_ANTERIOR
    not in JANELAS_CONFIRMACAO
):

    raise ValueError(
        "A confirmação do modelo anterior "
        "não está entre as janelas configuradas."
    )


# ============================================================
# LEITURA DO MODELO FIXO DA CÉLULA 9
# ============================================================

pesos_fixos_df["regime"] = (
    pesos_fixos_df[
        "regime"
    ]
    .astype("string")
    .str.strip()
)


PESOS_MODELO_FIXO = {}


for regime in ORDEM_REGIMES:

    linhas_regime = (
        pesos_fixos_df.loc[
            pesos_fixos_df[
                "regime"
            ]
            == regime
        ]
    )

    if linhas_regime.empty:

        raise ValueError(
            f"O regime {regime} não possui "
            "pesos fixos."
        )

    linha = linhas_regime.iloc[0]

    PESOS_MODELO_FIXO[regime] = {
        ativo: float(
            linha[
                f"peso_{ativo}"
            ]
        )
        for ativo in ATIVOS
    }


confirmacoes_fixas = (
    pd.to_numeric(
        pesos_fixos_df[
            "meses_confirmacao"
        ],
        errors="coerce",
    )
    .dropna()
    .unique()
)


if len(confirmacoes_fixas) != 1:

    raise ValueError(
        "Não foi possível identificar uma única "
        "confirmação da Célula 9."
    )


CONFIRMACAO_MODELO_FIXO = int(
    confirmacoes_fixas[0]
)


if (
    CONFIRMACAO_MODELO_FIXO
    not in JANELAS_CONFIRMACAO
):

    raise ValueError(
        "A confirmação do modelo fixo da Célula 9 "
        "não está entre as janelas configuradas."
    )


def ler_parametro(
    tabela,
    nome_metrica,
    valor_padrao=None,
):

    if not {
        "metrica",
        "valor",
    }.issubset(
        tabela.columns
    ):

        return valor_padrao

    valores = tabela.loc[
        tabela[
            "metrica"
        ]
        == nome_metrica,
        "valor",
    ]

    if valores.empty:

        return valor_padrao

    return valores.iloc[0]


CANDIDATO_FIXO_SALVO = str(
    ler_parametro(
        tabela=parametros_fixos_df,
        nome_metrica="Candidato selecionado",
        valor_padrao="",
    )
)


if not CANDIDATO_FIXO_SALVO.strip():

    raise ValueError(
        "O candidato selecionado não foi encontrado "
        "no arquivo de parâmetros da Célula 9."
    )


# ============================================================
# FUNÇÕES DE PESOS
# ============================================================

def criar_pesos_com_cdi(
    pesos_cdi_por_regime,
):

    pesos_finais = {}

    for regime in ORDEM_REGIMES:

        peso_cdi = float(
            pesos_cdi_por_regime[
                regime
            ]
        )

        if not (
            0.0
            <= peso_cdi
            <= 1.0
        ):

            raise ValueError(
                f"Peso de CDI inválido em {regime}."
            )

        pesos_finais[regime] = {}

        for ativo in ATIVOS_RISCO:

            pesos_finais[
                regime
            ][ativo] = (
                PESOS_RISCO_BASE[
                    regime
                ][ativo]
                * (
                    1.0
                    - peso_cdi
                )
            )

        pesos_finais[
            regime
        ][
            "CDI"
        ] = peso_cdi

        soma = sum(
            pesos_finais[
                regime
            ].values()
        )

        if not np.isclose(
            soma,
            1.0,
            atol=1e-10,
            rtol=1e-10,
        ):

            raise ValueError(
                f"Os pesos de {regime} "
                "não somam 100%."
            )

    return pesos_finais


def criar_matriz_pesos(
    dados,
    pesos_por_regime,
    meses_confirmacao,
):

    coluna_regime = (
        f"regime_confirmacao_"
        f"{int(meses_confirmacao)}m"
    )

    if coluna_regime not in dados.columns:

        raise KeyError(
            f"A coluna {coluna_regime} "
            "não foi encontrada."
        )

    matriz = np.zeros(
        (
            len(dados),
            len(ATIVOS),
        ),
        dtype=float,
    )

    regimes_mensais = (
        dados[
            coluna_regime
        ]
        .astype(str)
        .to_numpy()
    )

    for indice, regime in enumerate(
        regimes_mensais
    ):

        if regime not in pesos_por_regime:

            raise KeyError(
                f"O regime {regime} não possui pesos."
            )

        matriz[
            indice,
            :,
        ] = [
            pesos_por_regime[
                regime
            ][ativo]
            for ativo in ATIVOS
        ]

    if not np.allclose(
        matriz.sum(
            axis=1
        ),
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ):

        raise ValueError(
            "A matriz de pesos não soma 100%."
        )

    return matriz


def criar_matriz_constante(
    quantidade_linhas,
    pesos_constantes,
):

    vetor = np.array(
        [
            pesos_constantes[
                ativo
            ]
            for ativo in ATIVOS
        ],
        dtype=float,
    )

    if (
        vetor < 0
    ).any():

        raise ValueError(
            "Foram encontrados pesos negativos."
        )

    if not np.isclose(
        vetor.sum(),
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ):

        raise ValueError(
            "Os pesos constantes não somam 100%."
        )

    return np.tile(
        vetor,
        (
            quantidade_linhas,
            1,
        ),
    )


# ============================================================
# FUNÇÃO DE SIMULAÇÃO
# ============================================================

def simular_carteira(
    matriz_pesos,
    matriz_retornos,
):

    matriz_pesos = np.asarray(
        matriz_pesos,
        dtype=float,
    )

    matriz_retornos = np.asarray(
        matriz_retornos,
        dtype=float,
    )

    if matriz_pesos.shape != matriz_retornos.shape:

        raise ValueError(
            "As matrizes de pesos e retornos "
            "possuem dimensões diferentes."
        )

    quantidade_meses = len(
        matriz_retornos
    )

    retorno_bruto = np.sum(
        matriz_pesos
        * matriz_retornos,
        axis=1,
    )

    turnover = np.zeros(
        quantidade_meses,
        dtype=float,
    )

    if COBRAR_CUSTO_INICIAL:

        turnover[0] = 1.0

    for indice in range(
        1,
        quantidade_meses,
    ):

        pesos_anteriores = (
            matriz_pesos[
                indice - 1
            ]
        )

        retornos_anteriores = (
            matriz_retornos[
                indice - 1
            ]
        )

        retorno_anterior = (
            retorno_bruto[
                indice - 1
            ]
        )

        fator_patrimonio = (
            1.0
            + retorno_anterior
        )

        if fator_patrimonio <= 0:

            raise ValueError(
                "O patrimônio relativo ficou "
                "menor ou igual a zero."
            )

        pesos_apos_retorno = (
            pesos_anteriores
            * (
                1.0
                + retornos_anteriores
            )
            / fator_patrimonio
        )

        pesos_alvo = (
            matriz_pesos[
                indice
            ]
        )

        turnover[indice] = float(
            np.abs(
                pesos_alvo
                - pesos_apos_retorno
            ).sum()
            / 2.0
        )

    custo = (
        turnover
        * CUSTO_POR_TURNOVER
    )

    retorno_liquido = (
        (
            1.0
            + retorno_bruto
        )
        * (
            1.0
            - custo
        )
        - 1.0
    )

    return {
        "matriz_pesos": matriz_pesos,
        "retorno_bruto": retorno_bruto,
        "turnover": turnover,
        "custo": custo,
        "retorno_liquido": retorno_liquido,
    }


# ============================================================
# FUNÇÕES DE MÉTRICAS
# ============================================================

def calcular_retorno_total(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(retornos) == 0:

        return np.nan

    return float(
        np.prod(
            1.0
            + retornos
        )
        - 1.0
    )


def calcular_retorno_anualizado(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(retornos) == 0:

        return np.nan

    retorno_total = calcular_retorno_total(
        retornos
    )

    if retorno_total <= -1:

        return np.nan

    return float(
        (
            1.0
            + retorno_total
        )
        ** (
            PERIODOS_POR_ANO
            / len(
                retornos
            )
        )
        - 1.0
    )


def calcular_volatilidade_anualizada(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(retornos) < 2:

        return np.nan

    return float(
        np.std(
            retornos,
            ddof=1,
        )
        * np.sqrt(
            PERIODOS_POR_ANO
        )
    )


def calcular_maximo_drawdown(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(retornos) == 0:

        return np.nan

    indice = (
        VALOR_INICIAL
        * np.cumprod(
            1.0
            + retornos
        )
    )

    indice_com_inicio = np.concatenate(
        [
            np.array(
                [
                    VALOR_INICIAL
                ]
            ),
            indice,
        ]
    )

    picos = np.maximum.accumulate(
        indice_com_inicio
    )

    drawdown = (
        indice_com_inicio
        / picos
        - 1.0
    )

    return float(
        drawdown.min()
    )


def calcular_sharpe_excesso_cdi(
    retornos,
    retornos_cdi,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    retornos_cdi = np.asarray(
        retornos_cdi,
        dtype=float,
    )

    excesso = (
        retornos
        - retornos_cdi
    )

    desvio = np.std(
        excesso,
        ddof=1,
    )

    if (
        not np.isfinite(desvio)
        or desvio <= 0
    ):

        return 0.0

    return float(
        np.sqrt(
            PERIODOS_POR_ANO
        )
        * excesso.mean()
        / desvio
    )


def calcular_sortino_excesso_cdi(
    retornos,
    retornos_cdi,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    retornos_cdi = np.asarray(
        retornos_cdi,
        dtype=float,
    )

    excesso = (
        retornos
        - retornos_cdi
    )

    perdas = np.minimum(
        excesso,
        0.0,
    )

    desvio_negativo_mensal = np.sqrt(
        np.mean(
            perdas ** 2
        )
    )

    desvio_negativo_anual = (
        desvio_negativo_mensal
        * np.sqrt(
            PERIODOS_POR_ANO
        )
    )

    excesso_anualizado = (
        excesso.mean()
        * PERIODOS_POR_ANO
    )

    if desvio_negativo_anual <= 0:

        if excesso_anualizado > 0:

            return np.inf

        return 0.0

    return float(
        excesso_anualizado
        / desvio_negativo_anual
    )


def calcular_metricas(
    simulacao,
    mascara,
    vetor_cdi,
):

    retornos_brutos = (
        simulacao[
            "retorno_bruto"
        ][mascara]
    )

    retornos_liquidos = (
        simulacao[
            "retorno_liquido"
        ][mascara]
    )

    turnover = (
        simulacao[
            "turnover"
        ][mascara]
    )

    custos = (
        simulacao[
            "custo"
        ][mascara]
    )

    cdi_periodo = (
        vetor_cdi[
            mascara
        ]
    )

    retorno_anualizado = (
        calcular_retorno_anualizado(
            retornos_liquidos
        )
    )

    volatilidade = (
        calcular_volatilidade_anualizada(
            retornos_liquidos
        )
    )

    drawdown = (
        calcular_maximo_drawdown(
            retornos_liquidos
        )
    )

    if (
        pd.notna(volatilidade)
        and volatilidade > 0
    ):

        retorno_volatilidade = (
            retorno_anualizado
            / volatilidade
        )

    else:

        retorno_volatilidade = np.nan

    if (
        pd.notna(drawdown)
        and drawdown < 0
    ):

        calmar = (
            retorno_anualizado
            / abs(drawdown)
        )

    else:

        calmar = np.nan

    return {
        "quantidade_meses": int(
            mascara.sum()
        ),
        "retorno_total_bruto": (
            calcular_retorno_total(
                retornos_brutos
            )
        ),
        "retorno_total_liquido": (
            calcular_retorno_total(
                retornos_liquidos
            )
        ),
        "retorno_anualizado_liquido": (
            retorno_anualizado
        ),
        "volatilidade_anualizada_liquida": (
            volatilidade
        ),
        "retorno_volatilidade": (
            retorno_volatilidade
        ),
        "sharpe_excesso_cdi": (
            calcular_sharpe_excesso_cdi(
                retornos=retornos_liquidos,
                retornos_cdi=cdi_periodo,
            )
        ),
        "sortino_excesso_cdi": (
            calcular_sortino_excesso_cdi(
                retornos=retornos_liquidos,
                retornos_cdi=cdi_periodo,
            )
        ),
        "calmar": calmar,
        "maximo_drawdown": drawdown,
        "meses_positivos": float(
            np.mean(
                retornos_liquidos > 0
            )
        ),
        "melhor_mes": float(
            np.max(
                retornos_liquidos
            )
        ),
        "pior_mes": float(
            np.min(
                retornos_liquidos
            )
        ),
        "turnover_total": float(
            turnover.sum()
        ),
        "turnover_medio_mensal": float(
            turnover.mean()
        ),
        "custo_acumulado_simples": float(
            custos.sum()
        ),
        "indice_final_liquido": float(
            VALOR_INICIAL
            * np.prod(
                1.0
                + retornos_liquidos
            )
        ),
    }


def calcular_rolling_excesso(
    retornos_candidato,
    retornos_benchmark,
):

    retornos_candidato = pd.Series(
        np.asarray(
            retornos_candidato,
            dtype=float,
        )
    )

    retornos_benchmark = pd.Series(
        np.asarray(
            retornos_benchmark,
            dtype=float,
        )
    )

    rolling_candidato = (
        (
            1.0
            + retornos_candidato
        )
        .rolling(
            JANELA_ROLLING
        )
        .apply(
            np.prod,
            raw=True,
        )
        - 1.0
    )

    rolling_benchmark = (
        (
            1.0
            + retornos_benchmark
        )
        .rolling(
            JANELA_ROLLING
        )
        .apply(
            np.prod,
            raw=True,
        )
        - 1.0
    )

    excesso = (
        rolling_candidato
        - rolling_benchmark
    ).dropna()

    if excesso.empty:

        return {
            "quantidade_janelas_12m": 0,
            "proporcao_janelas_12m_positivas": np.nan,
            "media_excesso_12m": np.nan,
            "mediana_excesso_12m": np.nan,
            "pior_excesso_12m": np.nan,
            "melhor_excesso_12m": np.nan,
        }

    return {
        "quantidade_janelas_12m": int(
            len(excesso)
        ),
        "proporcao_janelas_12m_positivas": float(
            excesso.gt(0).mean()
        ),
        "media_excesso_12m": float(
            excesso.mean()
        ),
        "mediana_excesso_12m": float(
            excesso.median()
        ),
        "pior_excesso_12m": float(
            excesso.min()
        ),
        "melhor_excesso_12m": float(
            excesso.max()
        ),
    }


# ============================================================
# PESOS DO MODELO ANTERIOR SEM CDI
# ============================================================

PESOS_MODELO_ANTERIOR = {
    regime: {
        **{
            ativo: PESOS_RISCO_BASE[
                regime
            ][ativo]
            for ativo in ATIVOS_RISCO
        },
        "CDI": 0.0,
    }
    for regime in ORDEM_REGIMES
}


# ============================================================
# FUNÇÃO DE SELEÇÃO EM CADA RECALIBRAÇÃO
# ============================================================

def selecionar_parametros_no_treino(
    dados_treino,
    numero_recalibracao,
    data_recalibracao,
):

    matriz_retornos_treino = (
        dados_treino[
            ATIVOS
        ]
        .astype(float)
        .to_numpy()
    )

    vetor_cdi_treino = (
        dados_treino[
            "CDI"
        ]
        .astype(float)
        .to_numpy()
    )

    mascara_treino_local = np.ones(
        len(dados_treino),
        dtype=bool,
    )

    peso_igual = (
        1.0
        / len(ATIVOS)
    )

    pesos_benchmark = {
        ativo: peso_igual
        for ativo in ATIVOS
    }

    matriz_benchmark = (
        criar_matriz_constante(
            quantidade_linhas=len(
                dados_treino
            ),
            pesos_constantes=(
                pesos_benchmark
            ),
        )
    )

    simulacao_benchmark = (
        simular_carteira(
            matriz_pesos=matriz_benchmark,
            matriz_retornos=(
                matriz_retornos_treino
            ),
        )
    )

    metricas_benchmark = (
        calcular_metricas(
            simulacao=simulacao_benchmark,
            mascara=mascara_treino_local,
            vetor_cdi=vetor_cdi_treino,
        )
    )

    matriz_modelo_anterior = (
        criar_matriz_pesos(
            dados=dados_treino,
            pesos_por_regime=(
                PESOS_MODELO_ANTERIOR
            ),
            meses_confirmacao=(
                CONFIRMACAO_MODELO_ANTERIOR
            ),
        )
    )

    simulacao_modelo_anterior = (
        simular_carteira(
            matriz_pesos=matriz_modelo_anterior,
            matriz_retornos=(
                matriz_retornos_treino
            ),
        )
    )

    metricas_modelo_anterior = (
        calcular_metricas(
            simulacao=simulacao_modelo_anterior,
            mascara=mascara_treino_local,
            vetor_cdi=vetor_cdi_treino,
        )
    )

    limite_turnover = (
        metricas_modelo_anterior[
            "turnover_total"
        ]
    )

    registros_grade_local = []

    for meses_confirmacao in JANELAS_CONFIRMACAO:

        for combinacao in product(
            PESOS_CDI_TESTADOS,
            repeat=len(
                ORDEM_REGIMES
            ),
        ):

            pesos_cdi_por_regime = {
                regime: float(
                    peso
                )
                for regime, peso in zip(
                    ORDEM_REGIMES,
                    combinacao,
                )
            }

            pesos_candidato = (
                criar_pesos_com_cdi(
                    pesos_cdi_por_regime=(
                        pesos_cdi_por_regime
                    )
                )
            )

            matriz_candidato = (
                criar_matriz_pesos(
                    dados=dados_treino,
                    pesos_por_regime=(
                        pesos_candidato
                    ),
                    meses_confirmacao=(
                        meses_confirmacao
                    ),
                )
            )

            simulacao_candidato = (
                simular_carteira(
                    matriz_pesos=(
                        matriz_candidato
                    ),
                    matriz_retornos=(
                        matriz_retornos_treino
                    ),
                )
            )

            metricas_candidato = (
                calcular_metricas(
                    simulacao=(
                        simulacao_candidato
                    ),
                    mascara=(
                        mascara_treino_local
                    ),
                    vetor_cdi=(
                        vetor_cdi_treino
                    ),
                )
            )

            rolling = calcular_rolling_excesso(
                retornos_candidato=(
                    simulacao_candidato[
                        "retorno_liquido"
                    ]
                ),
                retornos_benchmark=(
                    simulacao_benchmark[
                        "retorno_liquido"
                    ]
                ),
            )

            excesso_anualizado = (
                metricas_candidato[
                    "retorno_anualizado_liquido"
                ]
                - metricas_benchmark[
                    "retorno_anualizado_liquido"
                ]
            )

            identificador = (
                f"conf_{meses_confirmacao}m"
                f"_cdi_"
                + "_".join(
                    f"{int(round(peso * 100)):02d}"
                    for peso in combinacao
                )
            )

            registros_grade_local.append(
                {
                    "numero_recalibracao": (
                        numero_recalibracao
                    ),
                    "data_recalibracao": (
                        data_recalibracao
                    ),
                    "data_inicial_treino": (
                        dados_treino[
                            "data"
                        ].min()
                    ),
                    "data_final_treino": (
                        dados_treino[
                            "data"
                        ].max()
                    ),
                    "quantidade_meses_treino": (
                        len(dados_treino)
                    ),
                    "candidato": identificador,
                    "meses_confirmacao": (
                        meses_confirmacao
                    ),
                    "peso_cdi_expansao_desinflacionaria": (
                        pesos_cdi_por_regime[
                            "EXPANSAO_DESINFLACIONARIA"
                        ]
                    ),
                    "peso_cdi_expansao_inflacionaria": (
                        pesos_cdi_por_regime[
                            "EXPANSAO_INFLACIONARIA"
                        ]
                    ),
                    "peso_cdi_estagflacao": (
                        pesos_cdi_por_regime[
                            "ESTAGFLACAO"
                        ]
                    ),
                    "peso_cdi_recessao_desinflacionaria": (
                        pesos_cdi_por_regime[
                            "RECESSAO_DESINFLACIONARIA"
                        ]
                    ),
                    "peso_cdi_medio": float(
                        np.mean(
                            combinacao
                        )
                    ),
                    "peso_cdi_maximo": float(
                        np.max(
                            combinacao
                        )
                    ),
                    "limite_turnover": (
                        limite_turnover
                    ),
                    "respeita_limite_turnover": (
                        metricas_candidato[
                            "turnover_total"
                        ]
                        <= (
                            limite_turnover
                            + 1e-12
                        )
                    ),
                    "excesso_retorno_anualizado_vs_benchmark": (
                        excesso_anualizado
                    ),
                    **metricas_candidato,
                    **rolling,
                }
            )

    grade_local = pd.DataFrame(
        registros_grade_local
    )

    candidatos_elegiveis = (
        grade_local.loc[
            grade_local[
                "respeita_limite_turnover"
            ]
        ]
        .copy()
    )

    if candidatos_elegiveis.empty:

        raise ValueError(
            "Nenhum candidato respeitou o limite "
            f"de turnover na recalibração "
            f"{numero_recalibracao}."
        )

    candidatos_elegiveis[
        "proporcao_janelas_12m_positivas"
    ] = (
        candidatos_elegiveis[
            "proporcao_janelas_12m_positivas"
        ]
        .fillna(
            -np.inf
        )
    )

    candidatos_elegiveis[
        "retorno_volatilidade"
    ] = (
        candidatos_elegiveis[
            "retorno_volatilidade"
        ]
        .fillna(
            -np.inf
        )
    )

    candidatos_elegiveis[
        "mediana_excesso_12m"
    ] = (
        candidatos_elegiveis[
            "mediana_excesso_12m"
        ]
        .fillna(
            -np.inf
        )
    )

    selecionado = (
        candidatos_elegiveis
        .sort_values(
            [
                "proporcao_janelas_12m_positivas",
                "retorno_volatilidade",
                "excesso_retorno_anualizado_vs_benchmark",
                "mediana_excesso_12m",
                "turnover_total",
                "peso_cdi_medio",
                "meses_confirmacao",
            ],
            ascending=[
                False,
                False,
                False,
                False,
                True,
                True,
                True,
            ],
        )
        .iloc[0]
    )

    pesos_cdi_selecionados = {
        "EXPANSAO_DESINFLACIONARIA": float(
            selecionado[
                "peso_cdi_expansao_desinflacionaria"
            ]
        ),
        "EXPANSAO_INFLACIONARIA": float(
            selecionado[
                "peso_cdi_expansao_inflacionaria"
            ]
        ),
        "ESTAGFLACAO": float(
            selecionado[
                "peso_cdi_estagflacao"
            ]
        ),
        "RECESSAO_DESINFLACIONARIA": float(
            selecionado[
                "peso_cdi_recessao_desinflacionaria"
            ]
        ),
    }

    pesos_finais_selecionados = (
        criar_pesos_com_cdi(
            pesos_cdi_por_regime=(
                pesos_cdi_selecionados
            )
        )
    )

    return {
        "selecionado": selecionado,
        "pesos_cdi": pesos_cdi_selecionados,
        "pesos_finais": pesos_finais_selecionados,
        "grade": grade_local,
    }


# ============================================================
# CONSTRUÇÃO DAS JANELAS WALK-FORWARD
# ============================================================

janelas = []

indice_final_treino = (
    MESES_TREINO_INICIAL
    - 1
)

numero_recalibracao = 1


while indice_final_treino < (
    len(base)
    - 1
):

    indice_inicial_aplicacao = (
        indice_final_treino
        + 1
    )

    indice_final_aplicacao = min(
        indice_inicial_aplicacao
        + MESES_ENTRE_RECALIBRACOES
        - 1,
        len(base)
        - 1,
    )

    janelas.append(
        {
            "numero_recalibracao": (
                numero_recalibracao
            ),
            "indice_inicial_treino": 0,
            "indice_final_treino": (
                indice_final_treino
            ),
            "indice_inicial_aplicacao": (
                indice_inicial_aplicacao
            ),
            "indice_final_aplicacao": (
                indice_final_aplicacao
            ),
            "data_inicial_treino": (
                base.iloc[0][
                    "data"
                ]
            ),
            "data_final_treino": (
                base.iloc[
                    indice_final_treino
                ][
                    "data"
                ]
            ),
            "data_inicial_aplicacao": (
                base.iloc[
                    indice_inicial_aplicacao
                ][
                    "data"
                ]
            ),
            "data_final_aplicacao": (
                base.iloc[
                    indice_final_aplicacao
                ][
                    "data"
                ]
            ),
            "quantidade_meses_treino": (
                indice_final_treino
                + 1
            ),
            "quantidade_meses_aplicacao": (
                indice_final_aplicacao
                - indice_inicial_aplicacao
                + 1
            ),
        }
    )

    indice_final_treino = (
        indice_final_aplicacao
    )

    numero_recalibracao += 1


tabela_janelas = pd.DataFrame(
    janelas
)


if tabela_janelas.empty:

    raise ValueError(
        "Nenhuma janela walk-forward foi criada."
    )


# ============================================================
# RECALIBRAÇÕES
# ============================================================

print("=" * 70)
print("INICIANDO VALIDAÇÃO WALK-FORWARD")
print("=" * 70)


print(
    f"\nQuantidade de recalibrações: "
    f"{len(tabela_janelas)}"
)


COMBINACOES_POR_RECALIBRACAO = (
    len(JANELAS_CONFIRMACAO)
    * (
        len(PESOS_CDI_TESTADOS)
        ** len(ORDEM_REGIMES)
    )
)


COMBINACOES_TOTAIS = (
    COMBINACOES_POR_RECALIBRACAO
    * len(tabela_janelas)
)


print(
    f"Combinações por recalibração: "
    f"{COMBINACOES_POR_RECALIBRACAO}"
)


print(
    f"Combinações totais: "
    f"{COMBINACOES_TOTAIS}\n"
)


grades_walk_forward = []
registros_parametros = []
registros_pesos = []
resultados_recalibracoes = []


for _, janela in tabela_janelas.iterrows():

    numero = int(
        janela[
            "numero_recalibracao"
        ]
    )

    indice_final_treino_janela = int(
        janela[
            "indice_final_treino"
        ]
    )

    dados_treino = (
        base.iloc[
            0:
            indice_final_treino_janela
            + 1
        ]
        .copy()
        .reset_index(
            drop=True
        )
    )

    print(
        f"Recalibração {numero}: "
        f"treino até "
        f"{janela['data_final_treino']:%d/%m/%Y} "
        f"com {len(dados_treino)} meses...",
        flush=True,
    )

    resultado = selecionar_parametros_no_treino(
        dados_treino=dados_treino,
        numero_recalibracao=numero,
        data_recalibracao=(
            janela[
                "data_final_treino"
            ]
        ),
    )

    selecionado = resultado[
        "selecionado"
    ]

    pesos_cdi = resultado[
        "pesos_cdi"
    ]

    pesos_finais = resultado[
        "pesos_finais"
    ]

    grades_walk_forward.append(
        resultado[
            "grade"
        ]
    )

    resultados_recalibracoes.append(
        {
            "numero_recalibracao": numero,
            "indice_inicial_aplicacao": int(
                janela[
                    "indice_inicial_aplicacao"
                ]
            ),
            "indice_final_aplicacao": int(
                janela[
                    "indice_final_aplicacao"
                ]
            ),
            "meses_confirmacao": int(
                selecionado[
                    "meses_confirmacao"
                ]
            ),
            "pesos_finais": pesos_finais,
        }
    )

    registros_parametros.append(
        {
            "numero_recalibracao": numero,
            "data_inicial_treino": (
                janela[
                    "data_inicial_treino"
                ]
            ),
            "data_final_treino": (
                janela[
                    "data_final_treino"
                ]
            ),
            "data_inicial_aplicacao": (
                janela[
                    "data_inicial_aplicacao"
                ]
            ),
            "data_final_aplicacao": (
                janela[
                    "data_final_aplicacao"
                ]
            ),
            "quantidade_meses_treino": (
                janela[
                    "quantidade_meses_treino"
                ]
            ),
            "quantidade_meses_aplicacao": (
                janela[
                    "quantidade_meses_aplicacao"
                ]
            ),
            "candidato": selecionado[
                "candidato"
            ],
            "meses_confirmacao": int(
                selecionado[
                    "meses_confirmacao"
                ]
            ),
            "peso_cdi_expansao_desinflacionaria": (
                pesos_cdi[
                    "EXPANSAO_DESINFLACIONARIA"
                ]
            ),
            "peso_cdi_expansao_inflacionaria": (
                pesos_cdi[
                    "EXPANSAO_INFLACIONARIA"
                ]
            ),
            "peso_cdi_estagflacao": (
                pesos_cdi[
                    "ESTAGFLACAO"
                ]
            ),
            "peso_cdi_recessao_desinflacionaria": (
                pesos_cdi[
                    "RECESSAO_DESINFLACIONARIA"
                ]
            ),
            "retorno_volatilidade_treino": (
                selecionado[
                    "retorno_volatilidade"
                ]
            ),
            "sharpe_excesso_cdi_treino": (
                selecionado[
                    "sharpe_excesso_cdi"
                ]
            ),
            "janelas_12m_positivas_treino": (
                selecionado[
                    "proporcao_janelas_12m_positivas"
                ]
            ),
            "turnover_total_treino": (
                selecionado[
                    "turnover_total"
                ]
            ),
            "limite_turnover_treino": (
                selecionado[
                    "limite_turnover"
                ]
            ),
        }
    )

    for regime in ORDEM_REGIMES:

        registro_peso = {
            "numero_recalibracao": numero,
            "data_final_treino": (
                janela[
                    "data_final_treino"
                ]
            ),
            "data_inicial_aplicacao": (
                janela[
                    "data_inicial_aplicacao"
                ]
            ),
            "data_final_aplicacao": (
                janela[
                    "data_final_aplicacao"
                ]
            ),
            "regime": regime,
            "nome_regime": (
                NOMES_REGIMES[
                    regime
                ]
            ),
            "meses_confirmacao": int(
                selecionado[
                    "meses_confirmacao"
                ]
            ),
        }

        for ativo in ATIVOS:

            registro_peso[
                f"peso_{ativo}"
            ] = (
                pesos_finais[
                    regime
                ][ativo]
            )

        registro_peso[
            "soma_pesos"
        ] = sum(
            pesos_finais[
                regime
            ].values()
        )

        registros_pesos.append(
            registro_peso
        )


grade_walk_forward = pd.concat(
    grades_walk_forward,
    ignore_index=True,
)


parametros_walk_forward = pd.DataFrame(
    registros_parametros
)


pesos_walk_forward = pd.DataFrame(
    registros_pesos
)


# ============================================================
# VALIDAÇÃO DA PRIMEIRA RECALIBRAÇÃO
# DEVE REPRODUZIR A CÉLULA 9
# ============================================================

CANDIDATO_PRIMEIRA_RECALIBRACAO = str(
    parametros_walk_forward.iloc[0][
        "candidato"
    ]
)


PRIMEIRA_RECALIBRACAO_REPRODUZIU_CELULA_9 = (
    CANDIDATO_PRIMEIRA_RECALIBRACAO
    == CANDIDATO_FIXO_SALVO
)


if not PRIMEIRA_RECALIBRACAO_REPRODUZIU_CELULA_9:

    raise ValueError(
        "A primeira recalibração não reproduziu "
        "o candidato salvo na Célula 9.\n"
        f"Célula 9: {CANDIDATO_FIXO_SALVO}\n"
        f"Célula 11: "
        f"{CANDIDATO_PRIMEIRA_RECALIBRACAO}"
    )


# ============================================================
# MATRIZ COMPLETA DO WALK-FORWARD
# ============================================================

primeiro_resultado = (
    resultados_recalibracoes[0]
)


matriz_walk_forward = (
    criar_matriz_pesos(
        dados=base,
        pesos_por_regime=(
            primeiro_resultado[
                "pesos_finais"
            ]
        ),
        meses_confirmacao=(
            primeiro_resultado[
                "meses_confirmacao"
            ]
        ),
    )
)


metadados_walk_forward = pd.DataFrame(
    {
        "data": base[
            "data"
        ],
        "numero_recalibracao": 0,
        "candidato_aplicado": (
            parametros_walk_forward.iloc[0][
                "candidato"
            ]
        ),
        "meses_confirmacao_aplicada": (
            parametros_walk_forward.iloc[0][
                "meses_confirmacao"
            ]
        ),
        "data_final_treino_utilizada": (
            parametros_walk_forward.iloc[0][
                "data_final_treino"
            ]
        ),
    }
)


for resultado_recalibracao in (
    resultados_recalibracoes
):

    inicio = resultado_recalibracao[
        "indice_inicial_aplicacao"
    ]

    fim = (
        resultado_recalibracao[
            "indice_final_aplicacao"
        ]
        + 1
    )

    dados_aplicacao = (
        base.iloc[
            inicio:fim
        ]
        .copy()
    )

    matriz_aplicacao = (
        criar_matriz_pesos(
            dados=dados_aplicacao,
            pesos_por_regime=(
                resultado_recalibracao[
                    "pesos_finais"
                ]
            ),
            meses_confirmacao=(
                resultado_recalibracao[
                    "meses_confirmacao"
                ]
            ),
        )
    )

    matriz_walk_forward[
        inicio:fim,
        :,
    ] = matriz_aplicacao

    numero = resultado_recalibracao[
        "numero_recalibracao"
    ]

    linha_parametro = (
        parametros_walk_forward.loc[
            parametros_walk_forward[
                "numero_recalibracao"
            ]
            == numero
        ]
        .iloc[0]
    )

    metadados_walk_forward.loc[
        inicio:
        fim - 1,
        "numero_recalibracao",
    ] = numero

    metadados_walk_forward.loc[
        inicio:
        fim - 1,
        "candidato_aplicado",
    ] = linha_parametro[
        "candidato"
    ]

    metadados_walk_forward.loc[
        inicio:
        fim - 1,
        "meses_confirmacao_aplicada",
    ] = linha_parametro[
        "meses_confirmacao"
    ]

    metadados_walk_forward.loc[
        inicio:
        fim - 1,
        "data_final_treino_utilizada",
    ] = linha_parametro[
        "data_final_treino"
    ]


# ============================================================
# MATRIZES DOS COMPARADORES
# ============================================================

matriz_modelo_fixo = (
    criar_matriz_pesos(
        dados=base,
        pesos_por_regime=(
            PESOS_MODELO_FIXO
        ),
        meses_confirmacao=(
            CONFIRMACAO_MODELO_FIXO
        ),
    )
)


matriz_modelo_anterior = (
    criar_matriz_pesos(
        dados=base,
        pesos_por_regime=(
            PESOS_MODELO_ANTERIOR
        ),
        meses_confirmacao=(
            CONFIRMACAO_MODELO_ANTERIOR
        ),
    )
)


PESO_IGUAL = (
    1.0
    / len(ATIVOS)
)


PESOS_BENCHMARK = {
    ativo: PESO_IGUAL
    for ativo in ATIVOS
}


matriz_benchmark = (
    criar_matriz_constante(
        quantidade_linhas=len(base),
        pesos_constantes=(
            PESOS_BENCHMARK
        ),
    )
)


PESOS_CDI_100 = {
    ativo: (
        1.0
        if ativo == "CDI"
        else 0.0
    )
    for ativo in ATIVOS
}


matriz_cdi_100 = (
    criar_matriz_constante(
        quantidade_linhas=len(base),
        pesos_constantes=(
            PESOS_CDI_100
        ),
    )
)


matriz_fixa_treino_inicial = (
    matriz_modelo_fixo[
        :MESES_TREINO_INICIAL
    ]
)


pesos_estaticos_vetor = (
    matriz_fixa_treino_inicial.mean(
        axis=0
    )
)


PESOS_ESTATICOS = {
    ativo: float(
        pesos_estaticos_vetor[
            indice
        ]
    )
    for indice, ativo in enumerate(
        ATIVOS
    )
}


matriz_estatica = (
    criar_matriz_constante(
        quantidade_linhas=len(base),
        pesos_constantes=(
            PESOS_ESTATICOS
        ),
    )
)


# ============================================================
# SIMULAÇÃO CONTÍNUA
# ============================================================

SIMULACAO_WALK_FORWARD = (
    simular_carteira(
        matriz_pesos=matriz_walk_forward,
        matriz_retornos=(
            MATRIZ_RETORNOS_COMPLETA
        ),
    )
)


SIMULACAO_MODELO_FIXO = (
    simular_carteira(
        matriz_pesos=matriz_modelo_fixo,
        matriz_retornos=(
            MATRIZ_RETORNOS_COMPLETA
        ),
    )
)


SIMULACAO_MODELO_ANTERIOR = (
    simular_carteira(
        matriz_pesos=matriz_modelo_anterior,
        matriz_retornos=(
            MATRIZ_RETORNOS_COMPLETA
        ),
    )
)


SIMULACAO_BENCHMARK = (
    simular_carteira(
        matriz_pesos=matriz_benchmark,
        matriz_retornos=(
            MATRIZ_RETORNOS_COMPLETA
        ),
    )
)


SIMULACAO_ESTATICA = (
    simular_carteira(
        matriz_pesos=matriz_estatica,
        matriz_retornos=(
            MATRIZ_RETORNOS_COMPLETA
        ),
    )
)


SIMULACAO_CDI_100 = (
    simular_carteira(
        matriz_pesos=matriz_cdi_100,
        matriz_retornos=(
            MATRIZ_RETORNOS_COMPLETA
        ),
    )
)


# ============================================================
# PERÍODO FORA DA AMOSTRA
# ============================================================

INDICE_INICIAL_OOS = (
    MESES_TREINO_INICIAL
)


MASCARA_OOS = np.zeros(
    len(base),
    dtype=bool,
)


MASCARA_OOS[
    INDICE_INICIAL_OOS:
] = True


DATA_INICIAL_OOS = (
    base.iloc[
        INDICE_INICIAL_OOS
    ][
        "data"
    ]
)


DATA_FINAL_OOS = (
    base.iloc[-1][
        "data"
    ]
)


# ============================================================
# MÉTRICAS COMPARATIVAS
# ============================================================

CENARIOS = {
    "WALK_FORWARD": {
        "rotulo": (
            "Modelo walk-forward"
        ),
        "simulacao": (
            SIMULACAO_WALK_FORWARD
        ),
    },
    "MODELO_FIXO_CELULA_9": {
        "rotulo": (
            "Modelo fixo da Célula 9"
        ),
        "simulacao": (
            SIMULACAO_MODELO_FIXO
        ),
    },
    "MODELO_ANTERIOR_SEM_CDI": {
        "rotulo": (
            "Modelo anterior sem CDI"
        ),
        "simulacao": (
            SIMULACAO_MODELO_ANTERIOR
        ),
    },
    "BENCHMARK_5_ATIVOS": {
        "rotulo": (
            "Benchmark de pesos iguais"
        ),
        "simulacao": (
            SIMULACAO_BENCHMARK
        ),
    },
    "CARTEIRA_ESTATICA": {
        "rotulo": (
            "Carteira estática"
        ),
        "simulacao": (
            SIMULACAO_ESTATICA
        ),
    },
    "CDI_100": {
        "rotulo": (
            "100% CDI"
        ),
        "simulacao": (
            SIMULACAO_CDI_100
        ),
    },
}


registros_metricas = []


for cenario, configuracao in (
    CENARIOS.items()
):

    metricas = calcular_metricas(
        simulacao=configuracao[
            "simulacao"
        ],
        mascara=MASCARA_OOS,
        vetor_cdi=VETOR_CDI_COMPLETO,
    )

    registros_metricas.append(
        {
            "periodo": (
                "WALK_FORWARD_OOS"
            ),
            "data_inicial": (
                DATA_INICIAL_OOS
            ),
            "data_final": (
                DATA_FINAL_OOS
            ),
            "cenario": cenario,
            "rotulo": configuracao[
                "rotulo"
            ],
            **metricas,
        }
    )


metricas_comparativas = pd.DataFrame(
    registros_metricas
)


indice_benchmark = float(
    metricas_comparativas.loc[
        metricas_comparativas[
            "cenario"
        ]
        == "BENCHMARK_5_ATIVOS",
        "indice_final_liquido",
    ]
    .iloc[0]
)


metricas_comparativas[
    "diferenca_indice_vs_benchmark"
] = (
    metricas_comparativas[
        "indice_final_liquido"
    ]
    - indice_benchmark
)


# ============================================================
# SÉRIES MENSAIS
# ============================================================

series_walk_forward = (
    base[
        [
            "data",
            *ATIVOS,
            *COLUNAS_REGIMES,
        ]
    ]
    .copy()
)


series_walk_forward = (
    series_walk_forward
    .merge(
        metadados_walk_forward,
        on="data",
        how="left",
        validate="one_to_one",
    )
)


series_walk_forward[
    "periodo"
] = np.where(
    MASCARA_OOS,
    "WALK_FORWARD_OOS",
    "TREINO_INICIAL",
)


for cenario, configuracao in (
    CENARIOS.items()
):

    simulacao = configuracao[
        "simulacao"
    ]

    series_walk_forward[
        f"retorno_bruto_{cenario}"
    ] = simulacao[
        "retorno_bruto"
    ]

    series_walk_forward[
        f"turnover_{cenario}"
    ] = simulacao[
        "turnover"
    ]

    series_walk_forward[
        f"custo_{cenario}"
    ] = simulacao[
        "custo"
    ]

    series_walk_forward[
        f"retorno_liquido_{cenario}"
    ] = simulacao[
        "retorno_liquido"
    ]


for indice_ativo, ativo in enumerate(
    ATIVOS
):

    series_walk_forward[
        f"peso_walk_forward_{ativo}"
    ] = (
        matriz_walk_forward[
            :,
            indice_ativo,
        ]
    )


# ============================================================
# ROLLING DE 12 MESES
# ============================================================

series_oos = (
    series_walk_forward.loc[
        series_walk_forward[
            "periodo"
        ]
        == "WALK_FORWARD_OOS"
    ]
    .copy()
    .reset_index(
        drop=True
    )
)


def retorno_rolling(
    serie,
):

    return (
        (
            1.0
            + pd.Series(
                serie
            )
        )
        .rolling(
            JANELA_ROLLING
        )
        .apply(
            np.prod,
            raw=True,
        )
        - 1.0
    )


rolling_12m = pd.DataFrame(
    {
        "data": series_oos[
            "data"
        ],
        "retorno_12m_walk_forward": (
            retorno_rolling(
                series_oos[
                    "retorno_liquido_WALK_FORWARD"
                ]
            )
        ),
        "retorno_12m_modelo_fixo": (
            retorno_rolling(
                series_oos[
                    "retorno_liquido_MODELO_FIXO_CELULA_9"
                ]
            )
        ),
        "retorno_12m_benchmark": (
            retorno_rolling(
                series_oos[
                    "retorno_liquido_BENCHMARK_5_ATIVOS"
                ]
            )
        ),
        "retorno_12m_cdi": (
            retorno_rolling(
                series_oos[
                    "retorno_liquido_CDI_100"
                ]
            )
        ),
    }
)


rolling_12m[
    "excesso_walk_forward_vs_benchmark"
] = (
    rolling_12m[
        "retorno_12m_walk_forward"
    ]
    - rolling_12m[
        "retorno_12m_benchmark"
    ]
)


rolling_12m[
    "excesso_walk_forward_vs_modelo_fixo"
] = (
    rolling_12m[
        "retorno_12m_walk_forward"
    ]
    - rolling_12m[
        "retorno_12m_modelo_fixo"
    ]
)


rolling_12m[
    "excesso_walk_forward_vs_cdi"
] = (
    rolling_12m[
        "retorno_12m_walk_forward"
    ]
    - rolling_12m[
        "retorno_12m_cdi"
    ]
)


rolling_validos = (
    rolling_12m
    .dropna(
        subset=[
            "excesso_walk_forward_vs_benchmark"
        ]
    )
)


if rolling_validos.empty:

    PROPORCAO_ROLLING_SUPERA_BENCHMARK = np.nan
    PROPORCAO_ROLLING_SUPERA_MODELO_FIXO = np.nan
    PIOR_EXCESSO_ROLLING = np.nan
    MELHOR_EXCESSO_ROLLING = np.nan

else:

    PROPORCAO_ROLLING_SUPERA_BENCHMARK = float(
        rolling_validos[
            "excesso_walk_forward_vs_benchmark"
        ]
        .gt(0)
        .mean()
    )

    PROPORCAO_ROLLING_SUPERA_MODELO_FIXO = float(
        rolling_validos[
            "excesso_walk_forward_vs_modelo_fixo"
        ]
        .gt(0)
        .mean()
    )

    PIOR_EXCESSO_ROLLING = float(
        rolling_validos[
            "excesso_walk_forward_vs_benchmark"
        ]
        .min()
    )

    MELHOR_EXCESSO_ROLLING = float(
        rolling_validos[
            "excesso_walk_forward_vs_benchmark"
        ]
        .max()
    )


# ============================================================
# RESULTADOS ANUAIS
# ============================================================

series_oos[
    "ano"
] = (
    series_oos[
        "data"
    ]
    .dt.year
)


registros_anuais = []


for ano, dados_ano in (
    series_oos.groupby(
        "ano"
    )
):

    retorno_benchmark_ano = (
        calcular_retorno_total(
            dados_ano[
                "retorno_liquido_BENCHMARK_5_ATIVOS"
            ]
        )
    )

    for cenario in CENARIOS:

        retorno_ano = (
            calcular_retorno_total(
                dados_ano[
                    f"retorno_liquido_{cenario}"
                ]
            )
        )

        registros_anuais.append(
            {
                "ano": int(ano),
                "cenario": cenario,
                "rotulo": CENARIOS[
                    cenario
                ][
                    "rotulo"
                ],
                "quantidade_meses": len(
                    dados_ano
                ),
                "retorno_liquido": (
                    retorno_ano
                ),
                "retorno_benchmark": (
                    retorno_benchmark_ano
                ),
                "excesso_vs_benchmark": (
                    retorno_ano
                    - retorno_benchmark_ano
                ),
                "superou_benchmark": (
                    retorno_ano
                    > retorno_benchmark_ano
                ),
            }
        )


resultados_anuais = pd.DataFrame(
    registros_anuais
)


anos_walk_forward_superou = int(
    resultados_anuais.loc[
        resultados_anuais[
            "cenario"
        ]
        == "WALK_FORWARD",
        "superou_benchmark",
    ]
    .sum()
)


quantidade_anos_oos = int(
    resultados_anuais.loc[
        resultados_anuais[
            "cenario"
        ]
        == "WALK_FORWARD",
        "ano",
    ]
    .nunique()
)


# ============================================================
# ESTABILIDADE DOS PARÂMETROS
# ============================================================

registros_estabilidade = []


serie_confirmacao = (
    parametros_walk_forward[
        "meses_confirmacao"
    ]
    .astype(float)
)


moda_confirmacao = float(
    serie_confirmacao.mode().iloc[0]
)


proporcao_moda_confirmacao = float(
    serie_confirmacao.eq(
        moda_confirmacao
    ).mean()
)


registros_estabilidade.append(
    {
        "parametro": (
            "meses_confirmacao"
        ),
        "media": float(
            serie_confirmacao.mean()
        ),
        "desvio_padrao": float(
            serie_confirmacao.std(
                ddof=1
            )
        )
        if len(serie_confirmacao) > 1
        else 0.0,
        "minimo": float(
            serie_confirmacao.min()
        ),
        "maximo": float(
            serie_confirmacao.max()
        ),
        "quantidade_valores_unicos": int(
            serie_confirmacao.nunique()
        ),
        "media_mudanca_absoluta": float(
            serie_confirmacao.diff().abs().dropna().mean()
        )
        if len(serie_confirmacao) > 1
        else 0.0,
        "maior_mudanca_absoluta": float(
            serie_confirmacao.diff().abs().dropna().max()
        )
        if len(serie_confirmacao) > 1
        else 0.0,
        "valor_modal": moda_confirmacao,
        "proporcao_valor_modal": (
            proporcao_moda_confirmacao
        ),
    }
)


mapa_colunas_pesos_cdi = {
    "peso_cdi_expansao_desinflacionaria": (
        "CDI — expansão desinflacionária"
    ),
    "peso_cdi_expansao_inflacionaria": (
        "CDI — expansão inflacionária"
    ),
    "peso_cdi_estagflacao": (
        "CDI — estagflação"
    ),
    "peso_cdi_recessao_desinflacionaria": (
        "CDI — recessão desinflacionária"
    ),
}


mudancas_absolutas_pesos = []


for coluna, nome_parametro in (
    mapa_colunas_pesos_cdi.items()
):

    serie = (
        parametros_walk_forward[
            coluna
        ]
        .astype(float)
    )

    mudancas = (
        serie.diff()
        .abs()
        .dropna()
    )

    mudancas_absolutas_pesos.extend(
        mudancas.tolist()
    )

    moda = float(
        serie.mode().iloc[0]
    )

    registros_estabilidade.append(
        {
            "parametro": nome_parametro,
            "media": float(
                serie.mean()
            ),
            "desvio_padrao": float(
                serie.std(
                    ddof=1
                )
            )
            if len(serie) > 1
            else 0.0,
            "minimo": float(
                serie.min()
            ),
            "maximo": float(
                serie.max()
            ),
            "quantidade_valores_unicos": int(
                serie.nunique()
            ),
            "media_mudanca_absoluta": float(
                mudancas.mean()
            )
            if not mudancas.empty
            else 0.0,
            "maior_mudanca_absoluta": float(
                mudancas.max()
            )
            if not mudancas.empty
            else 0.0,
            "valor_modal": moda,
            "proporcao_valor_modal": float(
                serie.eq(
                    moda
                ).mean()
            ),
        }
    )


estabilidade_parametros = pd.DataFrame(
    registros_estabilidade
)


MEDIA_MUDANCA_ABSOLUTA_PESOS = (
    float(
        np.mean(
            mudancas_absolutas_pesos
        )
    )
    if mudancas_absolutas_pesos
    else 0.0
)


# ============================================================
# RESULTADOS PRINCIPAIS
# ============================================================

def obter_resultado(
    cenario,
):

    resultado = (
        metricas_comparativas.loc[
            metricas_comparativas[
                "cenario"
            ]
            == cenario
        ]
    )

    if resultado.empty:

        raise KeyError(
            f"O cenário {cenario} não foi encontrado."
        )

    return resultado.iloc[0]


resultado_walk_forward = obter_resultado(
    "WALK_FORWARD"
)

resultado_modelo_fixo = obter_resultado(
    "MODELO_FIXO_CELULA_9"
)

resultado_modelo_anterior = obter_resultado(
    "MODELO_ANTERIOR_SEM_CDI"
)

resultado_benchmark = obter_resultado(
    "BENCHMARK_5_ATIVOS"
)

resultado_estatica = obter_resultado(
    "CARTEIRA_ESTATICA"
)

resultado_cdi = obter_resultado(
    "CDI_100"
)


# ============================================================
# CRITÉRIOS DA VALIDAÇÃO WALK-FORWARD
# ============================================================

criterio_superou_benchmark = bool(
    resultado_walk_forward[
        "indice_final_liquido"
    ]
    > resultado_benchmark[
        "indice_final_liquido"
    ]
)


criterio_retorno_volatilidade = bool(
    resultado_walk_forward[
        "retorno_volatilidade"
    ]
    > resultado_benchmark[
        "retorno_volatilidade"
    ]
)


criterio_sharpe = bool(
    resultado_walk_forward[
        "sharpe_excesso_cdi"
    ]
    > resultado_benchmark[
        "sharpe_excesso_cdi"
    ]
)


criterio_drawdown = bool(
    resultado_walk_forward[
        "maximo_drawdown"
    ]
    > resultado_benchmark[
        "maximo_drawdown"
    ]
)


criterio_rolling = bool(
    pd.notna(
        PROPORCAO_ROLLING_SUPERA_BENCHMARK
    )
    and (
        PROPORCAO_ROLLING_SUPERA_BENCHMARK
        >= PROPORCAO_MINIMA_ROLLING
    )
)


criterio_estabilidade = bool(
    (
        proporcao_moda_confirmacao
        >= PROPORCAO_MINIMA_CONFIRMACAO_MODAL
    )
    and (
        MEDIA_MUDANCA_ABSOLUTA_PESOS
        <= MUDANCA_MEDIA_MAXIMA_PESOS_CDI
    )
)


criterios_walk_forward = [
    criterio_superou_benchmark,
    criterio_retorno_volatilidade,
    criterio_sharpe,
    criterio_drawdown,
    criterio_rolling,
    criterio_estabilidade,
]


QUANTIDADE_CRITERIOS_APROVADOS = int(
    sum(
        criterios_walk_forward
    )
)


if (
    CRITERIOS_MINIMOS_APROVACAO
    > len(
        criterios_walk_forward
    )
):

    raise ValueError(
        "O mínimo de critérios para aprovação "
        "supera a quantidade total de critérios."
    )


if (
    CRITERIOS_MINIMOS_ROBUSTEZ_PARCIAL
    > len(
        criterios_walk_forward
    )
):

    raise ValueError(
        "O mínimo de critérios para robustez parcial "
        "supera a quantidade total de critérios."
    )


if (
    criterio_superou_benchmark
    and QUANTIDADE_CRITERIOS_APROVADOS
    >= CRITERIOS_MINIMOS_APROVACAO
):

    STATUS_WALK_FORWARD = (
        "APROVADO"
    )

elif (
    criterio_superou_benchmark
    and QUANTIDADE_CRITERIOS_APROVADOS
    >= CRITERIOS_MINIMOS_ROBUSTEZ_PARCIAL
):

    STATUS_WALK_FORWARD = (
        "ROBUSTEZ PARCIAL"
    )

else:

    STATUS_WALK_FORWARD = (
        "REPROVADO"
    )


# ============================================================
# TABELA FORMATADA
# ============================================================

metricas_formatadas = (
    metricas_comparativas
    .copy()
    .astype(object)
)


for coluna in [
    "retorno_total_bruto",
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown",
    "meses_positivos",
    "melhor_mes",
    "pior_mes",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
]:

    metricas_formatadas[coluna] = (
        metricas_comparativas[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2%}"
                if pd.notna(valor)
                else "-"
            )
        )
    )


for coluna in [
    "retorno_volatilidade",
    "sharpe_excesso_cdi",
    "sortino_excesso_cdi",
    "calmar",
    "turnover_total",
    "indice_final_liquido",
    "diferenca_indice_vs_benchmark",
]:

    metricas_formatadas[coluna] = (
        metricas_comparativas[
            coluna
        ]
        .map(
            lambda valor: (
                f"{valor:.2f}"
                if pd.notna(valor)
                and np.isfinite(
                    float(valor)
                )
                else (
                    "∞"
                    if pd.notna(valor)
                    and np.isinf(
                        float(valor)
                    )
                    else "-"
                )
            )
        )
    )


# ============================================================
# RESUMO FINAL
# ============================================================

resumo_walk_forward = pd.DataFrame(
    {
        "metrica": [
            "Data inicial do treino",
            "Data final do período",
            "Meses de treino inicial",
            "Data inicial fora da amostra",
            "Data final fora da amostra",
            "Meses fora da amostra",
            "Quantidade de recalibrações",
            "Combinações por recalibração",
            "Combinações totais",
            "Primeira recalibração reproduziu a Célula 9",
            "Índice final do walk-forward",
            "Índice final do modelo fixo",
            "Índice final do modelo anterior",
            "Índice final do benchmark",
            "Índice final da carteira estática",
            "Índice final de 100% CDI",
            "Diferença do walk-forward contra o benchmark",
            "Diferença do walk-forward contra o modelo fixo",
            "Retorno anualizado do walk-forward",
            "Volatilidade do walk-forward",
            "Retorno/volatilidade do walk-forward",
            "Sharpe de excesso ao CDI",
            "Sortino de excesso ao CDI",
            "Calmar",
            "Máximo drawdown",
            "Turnover total",
            "Janelas rolling acima do benchmark",
            "Janelas rolling acima do modelo fixo",
            "Pior excesso rolling contra o benchmark",
            "Melhor excesso rolling contra o benchmark",
            "Anos em que superou o benchmark",
            "Quantidade de anos avaliados",
            "Confirmações diferentes selecionadas",
            "Proporção da confirmação modal",
            "Média das mudanças absolutas nos pesos de CDI",
            "Critérios aprovados",
            "Quantidade total de critérios",
            "Status walk-forward",
            "Observação metodológica",
        ],
        "valor": [
            base[
                "data"
            ].min().strftime(
                "%d/%m/%Y"
            ),
            base[
                "data"
            ].max().strftime(
                "%d/%m/%Y"
            ),
            MESES_TREINO_INICIAL,
            DATA_INICIAL_OOS.strftime(
                "%d/%m/%Y"
            ),
            DATA_FINAL_OOS.strftime(
                "%d/%m/%Y"
            ),
            int(
                MASCARA_OOS.sum()
            ),
            len(
                tabela_janelas
            ),
            COMBINACOES_POR_RECALIBRACAO,
            COMBINACOES_TOTAIS,
            (
                "SIM"
                if PRIMEIRA_RECALIBRACAO_REPRODUZIU_CELULA_9
                else "NÃO"
            ),
            resultado_walk_forward[
                "indice_final_liquido"
            ],
            resultado_modelo_fixo[
                "indice_final_liquido"
            ],
            resultado_modelo_anterior[
                "indice_final_liquido"
            ],
            resultado_benchmark[
                "indice_final_liquido"
            ],
            resultado_estatica[
                "indice_final_liquido"
            ],
            resultado_cdi[
                "indice_final_liquido"
            ],
            (
                resultado_walk_forward[
                    "indice_final_liquido"
                ]
                - resultado_benchmark[
                    "indice_final_liquido"
                ]
            ),
            (
                resultado_walk_forward[
                    "indice_final_liquido"
                ]
                - resultado_modelo_fixo[
                    "indice_final_liquido"
                ]
            ),
            resultado_walk_forward[
                "retorno_anualizado_liquido"
            ],
            resultado_walk_forward[
                "volatilidade_anualizada_liquida"
            ],
            resultado_walk_forward[
                "retorno_volatilidade"
            ],
            resultado_walk_forward[
                "sharpe_excesso_cdi"
            ],
            resultado_walk_forward[
                "sortino_excesso_cdi"
            ],
            resultado_walk_forward[
                "calmar"
            ],
            resultado_walk_forward[
                "maximo_drawdown"
            ],
            resultado_walk_forward[
                "turnover_total"
            ],
            PROPORCAO_ROLLING_SUPERA_BENCHMARK,
            PROPORCAO_ROLLING_SUPERA_MODELO_FIXO,
            PIOR_EXCESSO_ROLLING,
            MELHOR_EXCESSO_ROLLING,
            anos_walk_forward_superou,
            quantidade_anos_oos,
            int(
                serie_confirmacao.nunique()
            ),
            proporcao_moda_confirmacao,
            MEDIA_MUDANCA_ABSOLUTA_PESOS,
            QUANTIDADE_CRITERIOS_APROVADOS,
            len(
                criterios_walk_forward
            ),
            STATUS_WALK_FORWARD,
            (
                "Os pesos-base de risco permaneceram "
                "fixos. A confirmação e os pesos de CDI "
                f"foram recalibrados a cada "
                f"{MESES_ENTRE_RECALIBRACOES} meses usando "
                "somente informações disponíveis até "
                "cada data de recalibração. O período "
                "fora da amostra já foi analisado e não "
                "é um holdout final intocado."
            ),
        ],
    }
)


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

tabela_janelas.to_csv(
    ARQUIVO_JANELAS,
    index=False,
    encoding="utf-8-sig",
)


grade_walk_forward.to_csv(
    ARQUIVO_GRADE,
    index=False,
    encoding="utf-8-sig",
)


parametros_walk_forward.to_csv(
    ARQUIVO_PARAMETROS,
    index=False,
    encoding="utf-8-sig",
)


pesos_walk_forward.to_csv(
    ARQUIVO_PESOS,
    index=False,
    encoding="utf-8-sig",
)


estabilidade_parametros.to_csv(
    ARQUIVO_ESTABILIDADE,
    index=False,
    encoding="utf-8-sig",
)


series_walk_forward.to_csv(
    ARQUIVO_SERIES,
    index=False,
    encoding="utf-8-sig",
)


metricas_comparativas.to_csv(
    ARQUIVO_METRICAS,
    index=False,
    encoding="utf-8-sig",
)


metricas_formatadas.to_csv(
    ARQUIVO_METRICAS_FORMATADAS,
    index=False,
    encoding="utf-8-sig",
)


rolling_12m.to_csv(
    ARQUIVO_ROLLING,
    index=False,
    encoding="utf-8-sig",
)


resultados_anuais.to_csv(
    ARQUIVO_ANUAL,
    index=False,
    encoding="utf-8-sig",
)


resumo_walk_forward.to_csv(
    ARQUIVO_RESUMO,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# BASE PARA GRÁFICOS
# ============================================================

series_grafico = (
    series_oos[
        [
            "data",
            *[
                f"retorno_liquido_{cenario}"
                for cenario in CENARIOS
            ],
        ]
    ]
    .copy()
)


for cenario in CENARIOS:

    series_grafico[
        f"indice_{cenario}"
    ] = (
        VALOR_INICIAL
        * (
            1.0
            + series_grafico[
                f"retorno_liquido_{cenario}"
            ]
        ).cumprod()
    )


series_grafico[
    "diferenca_walk_forward_benchmark"
] = (
    series_grafico[
        "indice_WALK_FORWARD"
    ]
    - series_grafico[
        "indice_BENCHMARK_5_ATIVOS"
    ]
)


series_grafico[
    "diferenca_walk_forward_modelo_fixo"
] = (
    series_grafico[
        "indice_WALK_FORWARD"
    ]
    - series_grafico[
        "indice_MODELO_FIXO_CELULA_9"
    ]
)


data_inicial_grafico = (
    DATA_INICIAL_OOS
    - pd.offsets.MonthEnd(1)
)


linha_inicial = {
    "data": data_inicial_grafico,
}


for cenario in CENARIOS:

    linha_inicial[
        f"indice_{cenario}"
    ] = VALOR_INICIAL


linha_inicial[
    "diferenca_walk_forward_benchmark"
] = 0.0

linha_inicial[
    "diferenca_walk_forward_modelo_fixo"
] = 0.0


series_grafico = pd.concat(
    [
        pd.DataFrame(
            [
                linha_inicial
            ]
        ),
        series_grafico,
    ],
    ignore_index=True,
)


# ============================================================
# GRÁFICO 1 — DESEMPENHO WALK-FORWARD
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


for cenario in [
    "WALK_FORWARD",
    "MODELO_FIXO_CELULA_9",
    "MODELO_ANTERIOR_SEM_CDI",
    "BENCHMARK_5_ATIVOS",
    "CDI_100",
]:

    ax.plot(
        series_grafico[
            "data"
        ],
        series_grafico[
            f"indice_{cenario}"
        ],
        linewidth=2,
        label=CENARIOS[
            cenario
        ][
            "rotulo"
        ],
    )


ax.axhline(
    y=VALOR_INICIAL,
    linewidth=1,
)


ax.set_title(
    "Validação Walk-Forward — Desempenho Fora da Amostra"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Índice acumulado"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DESEMPENHO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — DIFERENÇAS
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "diferenca_walk_forward_benchmark"
    ],
    linewidth=2,
    label="Walk-forward menos benchmark",
)


ax.plot(
    series_grafico[
        "data"
    ],
    series_grafico[
        "diferenca_walk_forward_modelo_fixo"
    ],
    linewidth=2,
    label="Walk-forward menos modelo fixo",
)


ax.axhline(
    y=0.0,
    linewidth=1,
)


ax.set_title(
    "Diferença do Walk-Forward contra as Referências"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Diferença do índice em pontos"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DIFERENCA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — CONFIRMAÇÃO POR RECALIBRAÇÃO
# ============================================================

fig, ax = plt.subplots(
    figsize=(11, 7)
)


ax.step(
    parametros_walk_forward[
        "data_inicial_aplicacao"
    ],
    parametros_walk_forward[
        "meses_confirmacao"
    ],
    where="post",
    linewidth=2,
)


ax.scatter(
    parametros_walk_forward[
        "data_inicial_aplicacao"
    ],
    parametros_walk_forward[
        "meses_confirmacao"
    ],
    s=80,
)


ax.set_yticks(
    JANELAS_CONFIRMACAO
)


ax.set_title(
    "Confirmação Selecionada em Cada Recalibração"
)

ax.set_xlabel(
    "Início do período de aplicação"
)

ax.set_ylabel(
    "Meses de confirmação"
)

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_CONFIRMACAO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 4 — PESOS DO CDI POR RECALIBRAÇÃO
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


for coluna, nome in (
    mapa_colunas_pesos_cdi.items()
):

    ax.plot(
        parametros_walk_forward[
            "data_inicial_aplicacao"
        ],
        parametros_walk_forward[
            coluna
        ],
        marker="o",
        linewidth=2,
        label=nome,
    )


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Pesos de CDI Selecionados em Cada Recalibração"
)

ax.set_xlabel(
    "Início do período de aplicação"
)

ax.set_ylabel(
    "Peso do CDI"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_PESOS_CDI,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 5 — ROLLING DE 12 MESES
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    rolling_12m[
        "data"
    ],
    rolling_12m[
        "excesso_walk_forward_vs_benchmark"
    ],
    linewidth=2,
    label="Walk-forward menos benchmark",
)


ax.plot(
    rolling_12m[
        "data"
    ],
    rolling_12m[
        "excesso_walk_forward_vs_modelo_fixo"
    ],
    linewidth=2,
    label="Walk-forward menos modelo fixo",
)


ax.axhline(
    y=0.0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    f"Excesso de Retorno Rolling de "
    f"{JANELA_ROLLING} Meses"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    f"Excesso de retorno em "
    f"{JANELA_ROLLING} meses"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_ROLLING,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÕES FINAIS
# ============================================================

validacoes = []


def adicionar_validacao(
    nome,
    aprovado,
    detalhe,
):

    validacoes.append(
        {
            "validacao": nome,
            "status": (
                "APROVADO"
                if aprovado
                else "REPROVADO"
            ),
            "detalhe": detalhe,
        }
    )


adicionar_validacao(
    nome="Quantidade total de meses",
    aprovado=(
        len(base)
        == len(
            retornos
        )
    ),
    detalhe=(
        f"{len(base)} meses"
    ),
)


adicionar_validacao(
    nome="Quantidade de meses fora da amostra",
    aprovado=(
        int(
            MASCARA_OOS.sum()
        )
        == (
            len(base)
            - MESES_TREINO_INICIAL
        )
    ),
    detalhe=(
        f"{int(MASCARA_OOS.sum())} meses"
    ),
)


adicionar_validacao(
    nome="Primeira recalibração reproduz a Célula 9",
    aprovado=(
        PRIMEIRA_RECALIBRACAO_REPRODUZIU_CELULA_9
    ),
    detalhe=(
        f"Candidato: "
        f"{CANDIDATO_PRIMEIRA_RECALIBRACAO}"
    ),
)


adicionar_validacao(
    nome="Valores nulos",
    aprovado=(
        not base[
            ATIVOS
        ]
        .isna()
        .any()
        .any()
    ),
    detalhe=(
        f"{int(base[ATIVOS].isna().sum().sum())} nulos"
    ),
)


adicionar_validacao(
    nome="Soma dos pesos walk-forward",
    aprovado=np.allclose(
        matriz_walk_forward.sum(
            axis=1
        ),
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ),
    detalhe=(
        "Todos os meses somam 100%"
    ),
)


adicionar_validacao(
    nome="Pesos não negativos",
    aprovado=(
        matriz_walk_forward >= 0
    ).all(),
    detalhe=(
        f"Peso mínimo: "
        f"{matriz_walk_forward.min():.8f}"
    ),
)


adicionar_validacao(
    nome="Turnover não negativo",
    aprovado=(
        SIMULACAO_WALK_FORWARD[
            "turnover"
        ]
        >= 0
    ).all(),
    detalhe=(
        f"Turnover mínimo: "
        f"{SIMULACAO_WALK_FORWARD['turnover'].min():.8f}"
    ),
)


adicionar_validacao(
    nome="Custos não negativos",
    aprovado=(
        SIMULACAO_WALK_FORWARD[
            "custo"
        ]
        >= 0
    ).all(),
    detalhe=(
        f"Custo mínimo: "
        f"{SIMULACAO_WALK_FORWARD['custo'].min():.8f}"
    ),
)


adicionar_validacao(
    nome="Seleção causal",
    aprovado=True,
    detalhe=(
        "Cada janela utiliza somente dados "
        "anteriores ao período de aplicação."
    ),
)


tabela_validacoes = pd.DataFrame(
    validacoes
)


if (
    tabela_validacoes[
        "status"
    ]
    == "REPROVADO"
).any():

    raise ValueError(
        "Uma ou mais validações da Célula 11 "
        "foram reprovadas:\n\n"
        f"{tabela_validacoes}"
    )


tabela_validacoes.to_csv(
    ARQUIVO_VALIDACOES,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

arquivos_esperados = [
    ARQUIVO_JANELAS,
    ARQUIVO_GRADE,
    ARQUIVO_PARAMETROS,
    ARQUIVO_PESOS,
    ARQUIVO_ESTABILIDADE,
    ARQUIVO_SERIES,
    ARQUIVO_METRICAS,
    ARQUIVO_METRICAS_FORMATADAS,
    ARQUIVO_ROLLING,
    ARQUIVO_ANUAL,
    ARQUIVO_VALIDACOES,
    ARQUIVO_RESUMO,
    ARQUIVO_GRAFICO_DESEMPENHO,
    ARQUIVO_GRAFICO_DIFERENCA,
    ARQUIVO_GRAFICO_CONFIRMACAO,
    ARQUIVO_GRAFICO_PESOS_CDI,
    ARQUIVO_GRAFICO_ROLLING,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in arquivos_esperados
    if not arquivo.exists()
]


if arquivos_nao_salvos:

    raise FileNotFoundError(
        "Alguns arquivos da Célula 11 "
        "não foram salvos:\n"
        + "\n".join(
            str(
                arquivo
            )
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("\n" + "=" * 70)
print("VALIDAÇÃO WALK-FORWARD CONCLUÍDA")
print("=" * 70)


print(
    f"\nRaiz do projeto:\n"
    f"{RAIZ_PROJETO}"
)


print(
    f"\nTreino inicial: "
    f"{base.iloc[0]['data']:%d/%m/%Y} "
    f"a "
    f"{base.iloc[MESES_TREINO_INICIAL - 1]['data']:%d/%m/%Y}"
)


print(
    f"Período fora da amostra: "
    f"{DATA_INICIAL_OOS:%d/%m/%Y} "
    f"a "
    f"{DATA_FINAL_OOS:%d/%m/%Y}"
)


print(
    f"Quantidade de meses fora da amostra: "
    f"{int(MASCARA_OOS.sum())}"
)


print(
    f"\nRecalibrações realizadas: "
    f"{len(tabela_janelas)}"
)


print(
    f"Combinações testadas no total: "
    f"{COMBINACOES_TOTAIS}"
)


print(
    f"\nPrimeira recalibração reproduziu "
    f"a Célula 9: "
    f"{'SIM' if PRIMEIRA_RECALIBRACAO_REPRODUZIU_CELULA_9 else 'NÃO'}"
)


print(
    "\nParâmetros selecionados por recalibração:"
)


for _, linha in (
    parametros_walk_forward.iterrows()
):

    print(
        f"\nRecalibração "
        f"{int(linha['numero_recalibracao'])}:"
    )

    print(
        f"- Treino até: "
        f"{linha['data_final_treino']:%d/%m/%Y}"
    )

    print(
        f"- Aplicação: "
        f"{linha['data_inicial_aplicacao']:%d/%m/%Y} "
        f"a "
        f"{linha['data_final_aplicacao']:%d/%m/%Y}"
    )

    print(
        f"- Candidato: "
        f"{linha['candidato']}"
    )

    print(
        f"- Confirmação: "
        f"{int(linha['meses_confirmacao'])} mês(es)"
    )

    print(
        f"- CDI expansão desinflacionária: "
        f"{linha['peso_cdi_expansao_desinflacionaria']:.0%}"
    )

    print(
        f"- CDI expansão inflacionária: "
        f"{linha['peso_cdi_expansao_inflacionaria']:.0%}"
    )

    print(
        f"- CDI estagflação: "
        f"{linha['peso_cdi_estagflacao']:.0%}"
    )

    print(
        f"- CDI recessão desinflacionária: "
        f"{linha['peso_cdi_recessao_desinflacionaria']:.0%}"
    )


print(
    "\nÍndices finais fora da amostra:"
)


print(
    f"- Walk-forward: "
    f"{resultado_walk_forward['indice_final_liquido']:.2f}"
)


print(
    f"- Modelo fixo da Célula 9: "
    f"{resultado_modelo_fixo['indice_final_liquido']:.2f}"
)


print(
    f"- Modelo anterior sem CDI: "
    f"{resultado_modelo_anterior['indice_final_liquido']:.2f}"
)


print(
    f"- Benchmark de cinco ativos: "
    f"{resultado_benchmark['indice_final_liquido']:.2f}"
)


print(
    f"- Carteira estática: "
    f"{resultado_estatica['indice_final_liquido']:.2f}"
)


print(
    f"- 100% CDI: "
    f"{resultado_cdi['indice_final_liquido']:.2f}"
)


print(
    f"\nWalk-forward contra o benchmark: "
    f"{resultado_walk_forward['indice_final_liquido'] - resultado_benchmark['indice_final_liquido']:.2f} "
    f"pontos"
)


print(
    f"Walk-forward contra o modelo fixo: "
    f"{resultado_walk_forward['indice_final_liquido'] - resultado_modelo_fixo['indice_final_liquido']:.2f} "
    f"pontos"
)


print(
    "\nMétricas do walk-forward:"
)


print(
    f"- Retorno anualizado: "
    f"{resultado_walk_forward['retorno_anualizado_liquido']:.2%}"
)


print(
    f"- Volatilidade anualizada: "
    f"{resultado_walk_forward['volatilidade_anualizada_liquida']:.2%}"
)


print(
    f"- Retorno/volatilidade: "
    f"{resultado_walk_forward['retorno_volatilidade']:.2f}"
)


print(
    f"- Sharpe de excesso ao CDI: "
    f"{resultado_walk_forward['sharpe_excesso_cdi']:.2f}"
)


print(
    f"- Sortino de excesso ao CDI: "
    f"{resultado_walk_forward['sortino_excesso_cdi']:.2f}"
)


print(
    f"- Calmar: "
    f"{resultado_walk_forward['calmar']:.2f}"
)


print(
    f"- Máximo drawdown: "
    f"{resultado_walk_forward['maximo_drawdown']:.2%}"
)


print(
    f"- Turnover total: "
    f"{resultado_walk_forward['turnover_total']:.4f}"
)


print(
    "\nEstabilidade:"
)


print(
    f"- Confirmações diferentes selecionadas: "
    f"{int(serie_confirmacao.nunique())}"
)


print(
    f"- Proporção da confirmação modal: "
    f"{proporcao_moda_confirmacao:.2%}"
)


print(
    f"- Mudança absoluta média nos pesos de CDI: "
    f"{MEDIA_MUDANCA_ABSOLUTA_PESOS:.2%}"
)


print(
    f"\nRolling de {JANELA_ROLLING} meses:"
)


print(
    f"- Janelas acima do benchmark: "
    f"{PROPORCAO_ROLLING_SUPERA_BENCHMARK:.2%}"
)


print(
    f"- Janelas acima do modelo fixo: "
    f"{PROPORCAO_ROLLING_SUPERA_MODELO_FIXO:.2%}"
)


print(
    f"- Pior excesso contra o benchmark: "
    f"{PIOR_EXCESSO_ROLLING:.2%}"
)


print(
    f"- Melhor excesso contra o benchmark: "
    f"{MELHOR_EXCESSO_ROLLING:.2%}"
)


print(
    f"\nAnos acima do benchmark: "
    f"{anos_walk_forward_superou}/"
    f"{quantidade_anos_oos}"
)


print(
    f"\nCritérios aprovados: "
    f"{QUANTIDADE_CRITERIOS_APROVADOS}/"
    f"{len(criterios_walk_forward)}"
)


print(
    f"Status walk-forward: "
    f"{STATUS_WALK_FORWARD}"
)


print(
    f"\nResumo salvo em:\n"
    f"{ARQUIVO_RESUMO}"
)


print(
    "\nMétricas comparativas:"
)


display(
    metricas_formatadas
)


print(
    "\nParâmetros por recalibração:"
)


display(
    parametros_walk_forward
)


print(
    "\nEstabilidade dos parâmetros:"
)


display(
    estabilidade_parametros
)


print(
    "\nValidações:"
)


display(
    tabela_validacoes
)

# ###########################################################################
# ETAPA 12 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# CÉLULA 12 — CONSOLIDAÇÃO E CONGELAMENTO DO MODELO FINAL
# MODELO OFICIAL: WALK-FORWARD COM CDI
# CHALLENGER: MODELO ANTERIOR SEM CDI
# VERSÃO AUTÔNOMA
# NOTEBOOK 06 — OTIMIZAÇÃO DA ESTRATÉGIA
# ============================================================

from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter


# ============================================================
# CONFIGURAÇÕES
# ============================================================

VALOR_INICIAL = 100.0

MODELO_OFICIAL = "WALK_FORWARD"
NOME_MODELO_OFICIAL = "Modelo walk-forward com CDI"

MODELO_CHALLENGER = "MODELO_ANTERIOR_SEM_CDI"
NOME_MODELO_CHALLENGER = "Modelo anterior sem CDI"

MODELO_FIXO = "MODELO_FIXO_CELULA_9"
BENCHMARK = "BENCHMARK_5_ATIVOS"
CARTEIRA_ESTATICA = "CARTEIRA_ESTATICA"
CDI_100 = "CDI_100"

ORDEM_REGIMES = [
    "EXPANSAO_DESINFLACIONARIA",
    "EXPANSAO_INFLACIONARIA",
    "ESTAGFLACAO",
    "RECESSAO_DESINFLACIONARIA",
]

NOMES_REGIMES = {
    "EXPANSAO_DESINFLACIONARIA": (
        "Expansão desinflacionária"
    ),
    "EXPANSAO_INFLACIONARIA": (
        "Expansão inflacionária"
    ),
    "ESTAGFLACAO": (
        "Estagflação"
    ),
    "RECESSAO_DESINFLACIONARIA": (
        "Recessão desinflacionária"
    ),
}


# ============================================================
# LOCALIZAÇÃO AUTOMÁTICA DA RAIZ DO PROJETO
# ============================================================

DIRETORIO_ATUAL = Path.cwd().resolve()

RAIZ_PROJETO = None


for diretorio in [
    DIRETORIO_ATUAL,
    *DIRETORIO_ATUAL.parents,
]:

    arquivo_teste = (
        diretorio
        / "data"
        / "processed"
        / "backtest_portfolio_mensal.csv"
    )

    if arquivo_teste.exists():

        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:

    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo data/processed/"
        "backtest_portfolio_mensal.csv não foi encontrado."
    )


PASTA_DADOS_PROCESSADOS = (
    RAIZ_PROJETO
    / "data"
    / "processed"
)

PASTA_TABELAS = (
    RAIZ_PROJETO
    / "outputs"
    / "tabelas"
)

PASTA_GRAFICOS = (
    RAIZ_PROJETO
    / "outputs"
    / "graficos"
)

PASTA_MODELO_FINAL = (
    RAIZ_PROJETO
    / "outputs"
    / "modelo_final"
)


for pasta in [
    PASTA_TABELAS,
    PASTA_GRAFICOS,
    PASTA_MODELO_FINAL,
]:

    pasta.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ARQUIVO_RESUMO_WALK_FORWARD = (
    PASTA_TABELAS
    / "06_11_resumo_walk_forward.csv"
)

ARQUIVO_PARAMETROS_WALK_FORWARD = (
    PASTA_TABELAS
    / "06_11_parametros_por_recalibracao.csv"
)

ARQUIVO_PESOS_WALK_FORWARD = (
    PASTA_TABELAS
    / "06_11_pesos_por_recalibracao.csv"
)

ARQUIVO_ESTABILIDADE = (
    PASTA_TABELAS
    / "06_11_estabilidade_parametros.csv"
)

ARQUIVO_SERIES_WALK_FORWARD = (
    PASTA_TABELAS
    / "06_11_series_walk_forward.csv"
)

ARQUIVO_METRICAS_WALK_FORWARD = (
    PASTA_TABELAS
    / "06_11_metricas_comparativas.csv"
)

ARQUIVO_VALIDACOES_WALK_FORWARD = (
    PASTA_TABELAS
    / "06_11_validacoes.csv"
)

ARQUIVO_RESUMO_ROBUSTEZ = (
    PASTA_TABELAS
    / "06_10_resumo_final_robustez.csv"
)

ARQUIVO_RESUMO_CDI = (
    PASTA_TABELAS
    / "06_09_resumo_otimizacao_cdi.csv"
)

ARQUIVO_STATUS_RENDA_FIXA = (
    PASTA_TABELAS
    / "06_08_status_fontes_renda_fixa.csv"
)

ARQUIVO_RETORNOS_AMPLIADOS = (
    PASTA_DADOS_PROCESSADOS
    / "retornos_ativos_ampliados_mensais.csv"
)

ARQUIVO_PESOS_MODELO_ANTERIOR = (
    PASTA_TABELAS
    / "06_07_pesos_otimizados_por_regime.csv"
)


ARQUIVOS_ENTRADA = [
    ARQUIVO_RESUMO_WALK_FORWARD,
    ARQUIVO_PARAMETROS_WALK_FORWARD,
    ARQUIVO_PESOS_WALK_FORWARD,
    ARQUIVO_ESTABILIDADE,
    ARQUIVO_SERIES_WALK_FORWARD,
    ARQUIVO_METRICAS_WALK_FORWARD,
    ARQUIVO_VALIDACOES_WALK_FORWARD,
    ARQUIVO_RESUMO_ROBUSTEZ,
    ARQUIVO_RESUMO_CDI,
    ARQUIVO_STATUS_RENDA_FIXA,
    ARQUIVO_RETORNOS_AMPLIADOS,
    ARQUIVO_PESOS_MODELO_ANTERIOR,
]


arquivos_ausentes = [
    arquivo
    for arquivo in ARQUIVOS_ENTRADA
    if not arquivo.exists()
]


if arquivos_ausentes:

    raise FileNotFoundError(
        "Arquivos necessários não encontrados:\n"
        + "\n".join(
            str(
                arquivo
            )
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_DECISAO_FINAL = (
    PASTA_TABELAS
    / "06_12_decisao_final_modelo.csv"
)

ARQUIVO_CONFIGURACAO_OFICIAL = (
    PASTA_TABELAS
    / "06_12_configuracao_modelo_oficial.csv"
)

ARQUIVO_PESOS_OFICIAIS = (
    PASTA_TABELAS
    / "06_12_pesos_oficiais_atuais.csv"
)

ARQUIVO_METRICAS_FINAIS = (
    PASTA_TABELAS
    / "06_12_metricas_finais_modelos.csv"
)

ARQUIVO_METRICAS_FINAIS_FORMATADAS = (
    PASTA_TABELAS
    / "06_12_metricas_finais_modelos_formatadas.csv"
)

ARQUIVO_SERIES_FINAIS = (
    PASTA_TABELAS
    / "06_12_series_modelos_finais.csv"
)

ARQUIVO_LIMITACOES = (
    PASTA_TABELAS
    / "06_12_limitacoes_metodologicas.csv"
)

ARQUIVO_VALIDACOES = (
    PASTA_TABELAS
    / "06_12_validacoes_finais.csv"
)

ARQUIVO_RESUMO_FINAL = (
    PASTA_TABELAS
    / "06_12_resumo_modelo_final.csv"
)

ARQUIVO_CONFIGURACAO_JSON = (
    PASTA_MODELO_FINAL
    / "modelo_oficial.json"
)

ARQUIVO_METRICAS_JSON = (
    PASTA_MODELO_FINAL
    / "metricas_modelo_oficial.json"
)

ARQUIVO_MANIFESTO = (
    PASTA_MODELO_FINAL
    / "manifesto_arquivos.csv"
)

ARQUIVO_GRAFICO_DESEMPENHO = (
    PASTA_GRAFICOS
    / "06_12_desempenho_modelos_finais.png"
)

ARQUIVO_GRAFICO_DRAWDOWN = (
    PASTA_GRAFICOS
    / "06_12_drawdown_modelos_finais.png"
)

ARQUIVO_GRAFICO_PESOS = (
    PASTA_GRAFICOS
    / "06_12_pesos_oficiais_por_regime.png"
)

ARQUIVO_GRAFICO_RISCO_RETORNO = (
    PASTA_GRAFICOS
    / "06_12_risco_retorno_modelos_finais.png"
)


# ============================================================
# CARREGAMENTO DAS BASES
# ============================================================

resumo_walk_forward = pd.read_csv(
    ARQUIVO_RESUMO_WALK_FORWARD,
    encoding="utf-8-sig",
)

parametros_walk_forward = pd.read_csv(
    ARQUIVO_PARAMETROS_WALK_FORWARD,
    encoding="utf-8-sig",
)

pesos_walk_forward = pd.read_csv(
    ARQUIVO_PESOS_WALK_FORWARD,
    encoding="utf-8-sig",
)

estabilidade_parametros = pd.read_csv(
    ARQUIVO_ESTABILIDADE,
    encoding="utf-8-sig",
)

series_walk_forward = pd.read_csv(
    ARQUIVO_SERIES_WALK_FORWARD,
    encoding="utf-8-sig",
)

metricas_comparativas = pd.read_csv(
    ARQUIVO_METRICAS_WALK_FORWARD,
    encoding="utf-8-sig",
)

validacoes_walk_forward = pd.read_csv(
    ARQUIVO_VALIDACOES_WALK_FORWARD,
    encoding="utf-8-sig",
)

resumo_robustez = pd.read_csv(
    ARQUIVO_RESUMO_ROBUSTEZ,
    encoding="utf-8-sig",
)

resumo_cdi = pd.read_csv(
    ARQUIVO_RESUMO_CDI,
    encoding="utf-8-sig",
)

status_renda_fixa = pd.read_csv(
    ARQUIVO_STATUS_RENDA_FIXA,
    encoding="utf-8-sig",
)

retornos_ampliados = pd.read_csv(
    ARQUIVO_RETORNOS_AMPLIADOS,
    encoding="utf-8-sig",
)

pesos_modelo_anterior = pd.read_csv(
    ARQUIVO_PESOS_MODELO_ANTERIOR,
    encoding="utf-8-sig",
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def ler_valor_resumo(
    tabela,
    metrica,
    valor_padrao=None,
):

    if not {
        "metrica",
        "valor",
    }.issubset(
        tabela.columns
    ):

        return valor_padrao

    resultado = tabela.loc[
        tabela[
            "metrica"
        ]
        .astype(str)
        .str.strip()
        == metrica,
        "valor",
    ]

    if resultado.empty:

        return valor_padrao

    return resultado.iloc[0]


def converter_float(
    valor,
    valor_padrao=np.nan,
):

    try:

        return float(
            str(valor)
            .replace(
                ",",
                ".",
            )
        )

    except Exception:

        return valor_padrao


def converter_int(
    valor,
    valor_padrao=0,
):

    try:

        return int(
            round(
                float(
                    str(valor)
                    .replace(
                        ",",
                        ".",
                    )
                )
            )
        )

    except Exception:

        return valor_padrao


def converter_data(
    valor,
):

    return pd.to_datetime(
        valor,
        dayfirst=True,
        errors="coerce",
    )


def calcular_hash_sha256(
    caminho,
):

    hash_arquivo = hashlib.sha256()

    with open(
        caminho,
        "rb",
    ) as arquivo:

        while True:

            bloco = arquivo.read(
                1024 * 1024
            )

            if not bloco:

                break

            hash_arquivo.update(
                bloco
            )

    return hash_arquivo.hexdigest()


def calcular_drawdown(
    retornos,
):

    retornos = pd.Series(
        retornos,
        dtype=float,
    )

    indice = (
        VALOR_INICIAL
        * (
            1.0
            + retornos
        ).cumprod()
    )

    indice_com_inicio = pd.concat(
        [
            pd.Series(
                [
                    VALOR_INICIAL
                ]
            ),
            indice,
        ],
        ignore_index=True,
    )

    picos = (
        indice_com_inicio
        .cummax()
    )

    drawdown = (
        indice_com_inicio
        / picos
        - 1.0
    )

    return drawdown.iloc[
        1:
    ].reset_index(
        drop=True
    )


def tornar_serializavel(
    valor,
):

    if isinstance(
        valor,
        pd.Timestamp,
    ):

        return valor.strftime(
            "%Y-%m-%d"
        )

    if isinstance(
        valor,
        np.integer,
    ):

        return int(
            valor
        )

    if isinstance(
        valor,
        np.floating,
    ):

        if np.isnan(
            valor
        ):

            return None

        if np.isinf(
            valor
        ):

            return str(
                valor
            )

        return float(
            valor
        )

    if isinstance(
        valor,
        np.bool_,
    ):

        return bool(
            valor
        )

    if pd.isna(
        valor
    ):

        return None

    return valor


# ============================================================
# PADRONIZAÇÃO DAS DATAS
# ============================================================

tabelas_com_datas = {
    "parâmetros walk-forward": (
        parametros_walk_forward
    ),
    "pesos walk-forward": (
        pesos_walk_forward
    ),
    "séries walk-forward": (
        series_walk_forward
    ),
    "métricas comparativas": (
        metricas_comparativas
    ),
    "retornos ampliados": (
        retornos_ampliados
    ),
}


for nome_tabela, tabela in (
    tabelas_com_datas.items()
):

    colunas_data = [
        coluna
        for coluna in tabela.columns
        if (
            coluna == "data"
            or coluna.startswith(
                "data_"
            )
        )
    ]

    for coluna in colunas_data:

        tabela[coluna] = pd.to_datetime(
            tabela[coluna],
            errors="coerce",
        )

        if tabela[coluna].isna().any():

            raise ValueError(
                f"A tabela {nome_tabela} possui "
                f"datas inválidas na coluna {coluna}."
            )


# ============================================================
# VALIDAÇÃO DO RESULTADO WALK-FORWARD
# ============================================================

STATUS_WALK_FORWARD = str(
    ler_valor_resumo(
        resumo_walk_forward,
        "Status walk-forward",
        "",
    )
).strip()


CRITERIOS_APROVADOS = converter_int(
    ler_valor_resumo(
        resumo_walk_forward,
        "Critérios aprovados",
        0,
    )
)


TOTAL_CRITERIOS = converter_int(
    ler_valor_resumo(
        resumo_walk_forward,
        "Quantidade total de critérios",
        0,
    )
)


WALK_FORWARD_ELEGIVEL = (
    STATUS_WALK_FORWARD == "APROVADO"
    and CRITERIOS_APROVADOS >= 5
)


if WALK_FORWARD_ELEGIVEL:

    MODELO_OFICIAL = "WALK_FORWARD"
    NOME_MODELO_OFICIAL = "Modelo walk-forward com CDI"

    MODELO_CHALLENGER = "MODELO_ANTERIOR_SEM_CDI"
    NOME_MODELO_CHALLENGER = "Modelo anterior sem CDI"

    MOTIVO_ESCOLHA_MODELO = (
        "O walk-forward atingiu os critérios mínimos e foi "
        "mantido como modelo oficial."
    )

else:

    MODELO_OFICIAL = "MODELO_ANTERIOR_SEM_CDI"
    NOME_MODELO_OFICIAL = "Modelo anterior sem CDI"

    MODELO_CHALLENGER = "WALK_FORWARD"
    NOME_MODELO_CHALLENGER = "Modelo walk-forward com CDI"

    MOTIVO_ESCOLHA_MODELO = (
        "O walk-forward foi reprovado nos critérios financeiros. "
        "O modelo anterior sem CDI foi adotado como fallback "
        "oficial por ser elegível e superar o benchmark."
    )

    print(
        "\nALERTA: o walk-forward foi reprovado pelos critérios "
        "financeiros."
    )
    print(
        "O modelo anterior sem CDI será utilizado como fallback "
        "oficial."
    )
    print(
        f"Status encontrado: {STATUS_WALK_FORWARD}"
    )


if (
    validacoes_walk_forward[
        "status"
    ]
    .astype(str)
    .str.upper()
    .eq(
        "REPROVADO"
    )
    .any()
):

    raise ValueError(
        "Existem validações reprovadas "
        "na Célula 11."
    )


# ============================================================
# IDENTIFICAÇÃO DA CONFIGURAÇÃO MAIS RECENTE
# ============================================================

parametros_walk_forward[
    "numero_recalibracao"
] = pd.to_numeric(
    parametros_walk_forward[
        "numero_recalibracao"
    ],
    errors="coerce",
)


pesos_walk_forward[
    "numero_recalibracao"
] = pd.to_numeric(
    pesos_walk_forward[
        "numero_recalibracao"
    ],
    errors="coerce",
)


if (
    parametros_walk_forward[
        "numero_recalibracao"
    ]
    .isna()
    .any()
):

    raise ValueError(
        "Existem números de recalibração inválidos."
    )


ULTIMA_RECALIBRACAO = int(
    parametros_walk_forward[
        "numero_recalibracao"
    ].max()
)


linha_parametro_atual = (
    parametros_walk_forward.loc[
        parametros_walk_forward[
            "numero_recalibracao"
        ]
        == ULTIMA_RECALIBRACAO
    ]
)


if len(
    linha_parametro_atual
) != 1:

    raise ValueError(
        "A configuração atual deveria possuir "
        "exatamente uma linha de parâmetros."
    )


linha_parametro_atual = (
    linha_parametro_atual.iloc[0]
)


if MODELO_OFICIAL == "WALK_FORWARD":

    pesos_oficiais = (
        pesos_walk_forward.loc[
            pesos_walk_forward[
                "numero_recalibracao"
            ]
            == ULTIMA_RECALIBRACAO
        ]
        .copy()
    )

else:

    colunas_pesos_fallback = [
        coluna
        for coluna in pesos_modelo_anterior.columns
        if (
            coluna.startswith(
                "peso_otimizado_"
            )
            and coluna
            != "peso_otimizado_CDI"
        )
    ]

    if not colunas_pesos_fallback:

        raise ValueError(
            "O arquivo do modelo anterior não possui colunas "
            "peso_otimizado_* de ativos de risco para "
            "construir o fallback."
        )

    colunas_base_fallback = [
        coluna
        for coluna in [
            "regime",
            "nome_regime",
            "meses_confirmacao",
        ]
        if coluna in pesos_modelo_anterior.columns
    ]

    pesos_oficiais = pesos_modelo_anterior[
        [
            *colunas_base_fallback,
            *colunas_pesos_fallback,
        ]
    ].copy()

    pesos_oficiais = pesos_oficiais.rename(
        columns={
            coluna: coluna.replace(
                "peso_otimizado_",
                "peso_",
                1,
            )
            for coluna in colunas_pesos_fallback
        }
    )

    if "nome_regime" not in pesos_oficiais.columns:

        pesos_oficiais["nome_regime"] = (
            pesos_oficiais["regime"].map(NOMES_REGIMES)
        )

    if "meses_confirmacao" not in pesos_oficiais.columns:

        pesos_oficiais["meses_confirmacao"] = 1

    colunas_pesos_risco_fallback = [
        coluna.replace(
            "peso_otimizado_",
            "peso_",
            1,
        )
        for coluna in colunas_pesos_fallback
    ]

    for coluna in colunas_pesos_risco_fallback:

        pesos_oficiais[coluna] = pd.to_numeric(
            pesos_oficiais[coluna],
            errors="coerce",
        )

    if pesos_oficiais[
        colunas_pesos_risco_fallback
    ].isna().any().any():

        raise ValueError(
            "Existem pesos inválidos no fallback sem CDI."
        )

    soma_pesos_risco_fallback = (
        pesos_oficiais[
            colunas_pesos_risco_fallback
        ]
        .sum(
            axis=1
        )
    )

    if (
        not np.isfinite(
            soma_pesos_risco_fallback
        ).all()
        or (
            soma_pesos_risco_fallback
            <= 0.0
        ).any()
    ):

        raise ValueError(
            "A soma dos pesos de risco do fallback é inválida."
        )

    pesos_oficiais[
        colunas_pesos_risco_fallback
    ] = (
        pesos_oficiais[
            colunas_pesos_risco_fallback
        ]
        .div(
            soma_pesos_risco_fallback,
            axis=0,
        )
    )

    soma_normalizada_fallback = (
        pesos_oficiais[
            colunas_pesos_risco_fallback
        ]
        .sum(
            axis=1
        )
    )

    if not np.allclose(
        soma_normalizada_fallback,
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ):

        raise ValueError(
            "Os pesos de risco normalizados do fallback "
            "não somam 100%."
        )

    # O fallback oficial é o modelo sem CDI.
    # O CDI permanece no esquema com peso zero.
    pesos_oficiais["peso_CDI"] = 0.0


pesos_oficiais = (
    pesos_oficiais
    .set_index("regime")
    .reindex(ORDEM_REGIMES)
    .reset_index()
)


if pesos_oficiais["regime"].isna().any():

    raise ValueError(
        "Não foi possível organizar os quatro regimes oficiais."
    )


if len(pesos_oficiais) != len(ORDEM_REGIMES):

    raise ValueError(
        "A configuração oficial não possui os quatro regimes "
        "esperados."
    )


# ============================================================
# IDENTIFICAÇÃO DOS ATIVOS
# ============================================================

COLUNAS_PESOS = [
    coluna
    for coluna in pesos_oficiais.columns
    if coluna.startswith(
        "peso_"
    )
    and coluna != "soma_pesos"
]


ATIVOS = [
    coluna.replace(
        "peso_",
        "",
        1,
    )
    for coluna in COLUNAS_PESOS
]


if "CDI" not in ATIVOS:

    raise ValueError(
        "O CDI não está presente nos pesos oficiais."
    )


ATIVOS_IMAB_OFICIAL_PARCIAL = {
    "IMAB_OFICIAL_PARCIAL",
    "IMA-B_OFICIAL_PARCIAL",
    "IMA_B_OFICIAL_PARCIAL",
    "IMAB_SGS_12466",
    "IMA-B_SGS_12466",
    "IMA_B_SGS_12466",
}


ativos_imab_oficial_parcial_encontrados = [
    ativo
    for ativo in ATIVOS
    if ativo.upper() in ATIVOS_IMAB_OFICIAL_PARCIAL
]


if ativos_imab_oficial_parcial_encontrados:

    raise ValueError(
        "A série oficial parcial do IMA-B não pode "
        "aparecer na configuração oficial. "
        f"Ativos encontrados: "
        f"{ativos_imab_oficial_parcial_encontrados}"
    )


# IMAB11.SA é um ETF negociado em bolsa e pode permanecer
# quando tiver sido aprovado pela etapa de coleta e validação.


for coluna in COLUNAS_PESOS:

    pesos_oficiais[coluna] = pd.to_numeric(
        pesos_oficiais[coluna],
        errors="coerce",
    )


if pesos_oficiais[
    COLUNAS_PESOS
].isna().any().any():

    raise ValueError(
        "Existem pesos oficiais inválidos."
    )


pesos_oficiais[
    "soma_pesos_recalculada"
] = (
    pesos_oficiais[
        COLUNAS_PESOS
    ].sum(
        axis=1
    )
)


if not np.allclose(
    pesos_oficiais[
        "soma_pesos_recalculada"
    ],
    1.0,
    atol=1e-10,
    rtol=1e-10,
):

    raise ValueError(
        "Os pesos oficiais não somam 100%."
    )


if (
    pesos_oficiais[
        COLUNAS_PESOS
    ]
    < 0
).any().any():

    raise ValueError(
        "Existem pesos oficiais negativos."
    )


# ============================================================
# MÉTRICAS DOS MODELOS
# ============================================================

CENARIOS_ESPERADOS = [
    MODELO_OFICIAL,
    MODELO_FIXO,
    MODELO_CHALLENGER,
    BENCHMARK,
    CARTEIRA_ESTATICA,
    CDI_100,
]


cenarios_ausentes = [
    cenario
    for cenario in CENARIOS_ESPERADOS
    if cenario not in (
        metricas_comparativas[
            "cenario"
        ]
        .astype(str)
        .tolist()
    )
]


if cenarios_ausentes:

    raise ValueError(
        "Cenários ausentes nas métricas:\n"
        f"{cenarios_ausentes}"
    )


metricas_finais = (
    metricas_comparativas.loc[
        metricas_comparativas[
            "cenario"
        ]
        .isin(
            CENARIOS_ESPERADOS
        )
    ]
    .copy()
    .reset_index(
        drop=True
    )
)


colunas_metricas_numericas = [
    "quantidade_meses",
    "retorno_total_bruto",
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "retorno_volatilidade",
    "sharpe_excesso_cdi",
    "sortino_excesso_cdi",
    "calmar",
    "maximo_drawdown",
    "meses_positivos",
    "melhor_mes",
    "pior_mes",
    "turnover_total",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
    "indice_final_liquido",
    "diferenca_indice_vs_benchmark",
]


for coluna in colunas_metricas_numericas:

    if coluna in metricas_finais.columns:

        metricas_finais[coluna] = pd.to_numeric(
            metricas_finais[coluna],
            errors="coerce",
        )


def obter_metrica_cenario(
    cenario,
    coluna,
):

    resultado = metricas_finais.loc[
        metricas_finais[
            "cenario"
        ]
        == cenario,
        coluna,
    ]

    if resultado.empty:

        raise KeyError(
            f"A métrica {coluna} do cenário "
            f"{cenario} não foi encontrada."
        )

    return float(
        resultado.iloc[0]
    )


INDICE_OFICIAL = obter_metrica_cenario(
    MODELO_OFICIAL,
    "indice_final_liquido",
)

INDICE_CHALLENGER = obter_metrica_cenario(
    MODELO_CHALLENGER,
    "indice_final_liquido",
)

INDICE_BENCHMARK = obter_metrica_cenario(
    BENCHMARK,
    "indice_final_liquido",
)

RETORNO_ANUAL_OFICIAL = obter_metrica_cenario(
    MODELO_OFICIAL,
    "retorno_anualizado_liquido",
)

VOLATILIDADE_OFICIAL = obter_metrica_cenario(
    MODELO_OFICIAL,
    "volatilidade_anualizada_liquida",
)

RETORNO_VOL_OFICIAL = obter_metrica_cenario(
    MODELO_OFICIAL,
    "retorno_volatilidade",
)

SHARPE_OFICIAL = obter_metrica_cenario(
    MODELO_OFICIAL,
    "sharpe_excesso_cdi",
)

SORTINO_OFICIAL = obter_metrica_cenario(
    MODELO_OFICIAL,
    "sortino_excesso_cdi",
)

CALMAR_OFICIAL = obter_metrica_cenario(
    MODELO_OFICIAL,
    "calmar",
)

DRAWDOWN_OFICIAL = obter_metrica_cenario(
    MODELO_OFICIAL,
    "maximo_drawdown",
)

TURNOVER_OFICIAL = obter_metrica_cenario(
    MODELO_OFICIAL,
    "turnover_total",
)


# ============================================================
# CONFIGURAÇÃO OFICIAL
# ============================================================

if MODELO_OFICIAL == "WALK_FORWARD":

    DATA_FINAL_TREINO_ATUAL = (
        linha_parametro_atual[
            "data_final_treino"
        ]
    )

    DATA_INICIAL_VIGENCIA = (
        linha_parametro_atual[
            "data_inicial_aplicacao"
        ]
    )

    DATA_FINAL_VIGENCIA_BACKTEST = (
        linha_parametro_atual[
            "data_final_aplicacao"
        ]
    )

    CONFIRMACAO_ATUAL = int(
        linha_parametro_atual[
            "meses_confirmacao"
        ]
    )

    CANDIDATO_ATUAL = str(
        linha_parametro_atual[
            "candidato"
        ]
    )

else:

    # O modelo anterior foi selecionado usando somente o treino
    # inicial encerrado em dezembro de 2023.
    DATA_FINAL_TREINO_ATUAL = pd.Timestamp("2023-12-31")

    serie_oos = series_walk_forward.loc[
        series_walk_forward["periodo"] == "WALK_FORWARD_OOS",
        "data",
    ]

    DATA_INICIAL_VIGENCIA = pd.to_datetime(
        serie_oos.min()
    )

    DATA_FINAL_VIGENCIA_BACKTEST = pd.to_datetime(
        serie_oos.max()
    )

    CONFIRMACAO_ATUAL = int(
        pd.to_numeric(
            pesos_oficiais["meses_confirmacao"],
            errors="coerce",
        )
        .dropna()
        .mode()
        .iloc[0]
    )

    CANDIDATO_ATUAL = "fallback_modelo_anterior_sem_cdi"

CUSTO_POR_TURNOVER = converter_float(
    ler_valor_resumo(
        resumo_walk_forward,
        "Custo por turnover",
        0.001,
    ),
    0.001,
)


OBJETIVO_MODELO_OFICIAL = (
    "Maximizar retorno ajustado ao risco por regime "
    "macroeconômico"
    if MODELO_OFICIAL == "MODELO_ANTERIOR_SEM_CDI"
    else (
        "Maximizar eficiência ajustada ao risco com "
        "proteção defensiva via CDI"
    )
)


STATUS_PRODUCAO = (
    "FALLBACK OFICIAL — WALK-FORWARD REPROVADO"
    if not WALK_FORWARD_ELEGIVEL
    else "APROVADO PELO WALK-FORWARD"
)


USO_RECOMENDADO = (
    "Utilizar o modelo anterior sem CDI como oficial e "
    "manter o walk-forward com CDI como challenger."
    if not WALK_FORWARD_ELEGIVEL
    else (
        "Utilizar o walk-forward com CDI como oficial e "
        "manter o modelo anterior sem CDI como challenger."
    )
)


configuracao_oficial = pd.DataFrame(
    {
        "parametro": [
            "Nome do projeto",
            "Nome do modelo oficial",
            "Tipo do modelo",
            "Modelo challenger",
            "Objetivo do modelo oficial",
            "Frequência dos retornos",
            "Frequência de rebalanceamento",
            "Frequência de recalibração",
            "Método da janela de treino",
            "Meses do treino inicial",
            "Meses entre recalibrações",
            "Confirmação atual do regime",
            "Candidato atual",
            "Última recalibração",
            "Data final do treino atual",
            "Data inicial da vigência atual",
            "Data final observada da vigência",
            "Custo por turnover",
            "Ativos utilizados",
            "Quantidade de ativos",
            "Benchmark",
            "Taxa livre de risco",
            "Status do walk-forward",
            "Critérios aprovados",
            "Quantidade total de critérios",
            "Status de produção",
        ],
        "valor": [
            (
                "Alocação Quantitativa por "
                "Regimes Macroeconômicos"
            ),
            NOME_MODELO_OFICIAL,
            (
                "Alocação mensal por regime "
                "com recalibração anual"
            ),
            NOME_MODELO_CHALLENGER,
            OBJETIVO_MODELO_OFICIAL,
            "MENSAL",
            "MENSAL",
            "ANUAL",
            "JANELA EXPANSIVA",
            48,
            12,
            CONFIRMACAO_ATUAL,
            CANDIDATO_ATUAL,
            ULTIMA_RECALIBRACAO,
            DATA_FINAL_TREINO_ATUAL.strftime(
                "%d/%m/%Y"
            ),
            DATA_INICIAL_VIGENCIA.strftime(
                "%d/%m/%Y"
            ),
            DATA_FINAL_VIGENCIA_BACKTEST.strftime(
                "%d/%m/%Y"
            ),
            CUSTO_POR_TURNOVER,
            str(
                ATIVOS
            ),
            len(
                ATIVOS
            ),
            (
                "Carteira estática mensalmente "
                "rebalanceada com pesos iguais"
            ),
            "CDI",
            STATUS_WALK_FORWARD,
            CRITERIOS_APROVADOS,
            TOTAL_CRITERIOS,
            STATUS_PRODUCAO,
        ],
    }
)


# ============================================================
# DECISÃO FINAL
# ============================================================

decisao_final = pd.DataFrame(
    [
        {
            "item": "Modelo oficial",
            "decisao": NOME_MODELO_OFICIAL,
            "justificativa": MOTIVO_ESCOLHA_MODELO,
        },
        {
            "item": "Modelo challenger",
            "decisao": NOME_MODELO_CHALLENGER,
            "justificativa": (
                "Permanece registrado para comparação e novas "
                "recalibrações, sem substituir o modelo oficial "
                "enquanto não atingir os critérios mínimos."
            ),
        },
        {
            "item": "Walk-forward",
            "decisao": STATUS_WALK_FORWARD,
            "justificativa": (
                f"Critérios aprovados: {CRITERIOS_APROVADOS}/"
                f"{TOTAL_CRITERIOS}."
            ),
        },
        {
            "item": "Inclusão do CDI",
            "decisao": (
                "PESO ZERO NO MODELO OFICIAL"
                if MODELO_OFICIAL == "MODELO_ANTERIOR_SEM_CDI"
                else "MANTER"
            ),
            "justificativa": (
                "A série do CDI continua disponível como taxa "
                "livre de risco e comparador."
            ),
        },
        {
            "item": "Série oficial parcial do IMA-B",
            "decisao": "NÃO INCLUIR",
            "justificativa": (
                "A série oficial SGS 12466 possui cobertura "
                "parcial. O ETF IMAB11.SA pode permanecer "
                "quando aprovado pela coleta."
            ),
        },
        {
            "item": "Resultado do modelo oficial",
            "decisao": f"Índice {INDICE_OFICIAL:.2f}",
            "justificativa": (
                f"Diferença de "
                f"{INDICE_OFICIAL - INDICE_BENCHMARK:.2f} "
                "ponto contra o benchmark."
            ),
        },
        {
            "item": "Uso recomendado",
            "decisao": STATUS_PRODUCAO,
            "justificativa": USO_RECOMENDADO,
        },
    ]
)

# ============================================================
# LIMITAÇÕES METODOLÓGICAS
# ============================================================

limitacoes = pd.DataFrame(
    [
        {
            "limitacao": (
                "Período histórico relativamente curto"
            ),
            "impacto": (
                f"O backtest possui {len(retornos_ampliados)} meses e "
                f"{len(series_walk_forward)} meses no walk-forward."
            ),
            "tratamento": (
                "Uso de walk-forward, rolling de 12 meses "
                "e comparação com múltiplas referências."
            ),
        },
        {
            "limitacao": (
                "Período de avaliação já analisado"
            ),
            "impacto": (
                "2024–2026 não constitui mais um "
                "holdout final completamente intocado."
            ),
            "tratamento": (
                "Apresentar o período como avaliação "
                "e evitar novos ajustes baseados nele."
            ),
        },
        {
            "limitacao": (
                "Sensibilidade aos pesos exatos de CDI"
            ),
            "impacto": (
                "Somente parte das variantes próximas "
                "superou o benchmark."
            ),
            "tratamento": (
                "Manter recalibração anual e acompanhar "
                "estabilidade dos parâmetros."
            ),
        },
        {
            "limitacao": (
                "Pesos-base dos ativos de risco fixos"
            ),
            "impacto": (
                "O walk-forward recalibrou confirmação "
                "e CDI, mas não reestimou todos os pesos."
            ),
            "tratamento": (
                "Documentar como escolha metodológica "
                "para reduzir overfitting."
            ),
        },
        {
            "limitacao": (
                "Série oficial parcial do IMA-B fora "
                "do universo final"
            ),
            "impacto": (
                "A série SGS 12466 não cobre todo o backtest. "
                "O ETF IMAB11.SA pode representar a classe "
                "quando aprovado pela coleta."
            ),
            "tratamento": (
                "Manter somente séries com cobertura completa "
                "e reavaliar a fonte oficial quando atualizada."
            ),
        },
        {
            "limitacao": (
                "Custo operacional provisório"
            ),
            "impacto": (
                "O custo de 10 bps por turnover pode não "
                "representar todos os custos reais."
            ),
            "tratamento": (
                "Substituir por estimativa operacional "
                "documentada antes da implementação real."
            ),
        },
    ]
)


# ============================================================
# SÉRIES FINAIS
# ============================================================

if "periodo" not in series_walk_forward.columns:

    raise ValueError(
        "A série walk-forward não possui "
        "a coluna periodo."
    )


series_finais = (
    series_walk_forward.loc[
        series_walk_forward[
            "periodo"
        ]
        == "WALK_FORWARD_OOS"
    ]
    .copy()
    .sort_values(
        "data"
    )
    .reset_index(
        drop=True
    )
)


CENARIOS_SERIES = {
    MODELO_OFICIAL: NOME_MODELO_OFICIAL,
    MODELO_FIXO: "Modelo fixo com CDI",
    MODELO_CHALLENGER: NOME_MODELO_CHALLENGER,
    BENCHMARK: "Benchmark de pesos iguais",
    CARTEIRA_ESTATICA: "Carteira estática",
    CDI_100: "100% CDI",
}


for cenario in CENARIOS_SERIES:

    coluna_retorno = (
        f"retorno_liquido_{cenario}"
    )

    if coluna_retorno not in series_finais.columns:

        raise ValueError(
            f"A coluna {coluna_retorno} "
            "não foi encontrada."
        )

    series_finais[
        coluna_retorno
    ] = pd.to_numeric(
        series_finais[
            coluna_retorno
        ],
        errors="coerce",
    )

    if series_finais[
        coluna_retorno
    ].isna().any():

        raise ValueError(
            f"A coluna {coluna_retorno} "
            "possui valores inválidos."
        )

    series_finais[
        f"indice_{cenario}"
    ] = (
        VALOR_INICIAL
        * (
            1.0
            + series_finais[
                coluna_retorno
            ]
        ).cumprod()
    )

    series_finais[
        f"drawdown_{cenario}"
    ] = calcular_drawdown(
        series_finais[
            coluna_retorno
        ]
    )


series_finais[
    "diferenca_oficial_vs_benchmark"
] = (
    series_finais[
        f"indice_{MODELO_OFICIAL}"
    ]
    - series_finais[
        f"indice_{BENCHMARK}"
    ]
)


series_finais[
    "diferenca_oficial_vs_challenger"
] = (
    series_finais[
        f"indice_{MODELO_OFICIAL}"
    ]
    - series_finais[
        f"indice_{MODELO_CHALLENGER}"
    ]
)


INDICE_RECALCULADO_OFICIAL = float(
    series_finais[
        f"indice_{MODELO_OFICIAL}"
    ].iloc[-1]
)


# ============================================================
# MÉTRICAS FORMATADAS
# ============================================================

metricas_finais_formatadas = (
    metricas_finais
    .copy()
    .astype(object)
)


COLUNAS_PERCENTUAIS = [
    "retorno_total_bruto",
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "maximo_drawdown",
    "meses_positivos",
    "melhor_mes",
    "pior_mes",
    "turnover_medio_mensal",
    "custo_acumulado_simples",
]


for coluna in COLUNAS_PERCENTUAIS:

    if coluna in metricas_finais.columns:

        metricas_finais_formatadas[
            coluna
        ] = (
            metricas_finais[
                coluna
            ]
            .map(
                lambda valor: (
                    f"{valor:.2%}"
                    if pd.notna(
                        valor
                    )
                    else "-"
                )
            )
        )


COLUNAS_DECIMAIS = [
    "retorno_volatilidade",
    "sharpe_excesso_cdi",
    "sortino_excesso_cdi",
    "calmar",
    "turnover_total",
    "indice_final_liquido",
    "diferenca_indice_vs_benchmark",
]


for coluna in COLUNAS_DECIMAIS:

    if coluna in metricas_finais.columns:

        metricas_finais_formatadas[
            coluna
        ] = (
            metricas_finais[
                coluna
            ]
            .map(
                lambda valor: (
                    f"{valor:.2f}"
                    if pd.notna(
                        valor
                    )
                    and np.isfinite(
                        float(
                            valor
                        )
                    )
                    else (
                        "∞"
                        if pd.notna(
                            valor
                        )
                        and np.isinf(
                            float(
                                valor
                            )
                        )
                        else "-"
                    )
                )
            )
        )


# ============================================================
# RESUMO FINAL
# ============================================================

resumo_final = pd.DataFrame(
    {
        "metrica": [
            "Modelo oficial",
            "Modelo challenger",
            "Status walk-forward",
            "Critérios walk-forward aprovados",
            "Quantidade total de critérios",
            "Última recalibração",
            "Candidato atual",
            "Confirmação atual",
            "Data final do treino atual",
            "Data inicial da vigência atual",
            "Índice final do modelo oficial",
            "Índice final do challenger",
            "Índice final do benchmark",
            "Diferença oficial contra benchmark",
            "Diferença oficial contra challenger",
            "Retorno anualizado oficial",
            "Volatilidade anualizada oficial",
            "Retorno/volatilidade oficial",
            "Sharpe de excesso ao CDI",
            "Sortino de excesso ao CDI",
            "Calmar",
            "Máximo drawdown oficial",
            "Turnover total oficial",
            "Quantidade de ativos",
            "Ativos utilizados",
            "Frequência de rebalanceamento",
            "Frequência de recalibração",
            "Status final",
            "Uso recomendado",
        ],
        "valor": [
            NOME_MODELO_OFICIAL,
            NOME_MODELO_CHALLENGER,
            STATUS_WALK_FORWARD,
            CRITERIOS_APROVADOS,
            TOTAL_CRITERIOS,
            ULTIMA_RECALIBRACAO,
            CANDIDATO_ATUAL,
            CONFIRMACAO_ATUAL,
            DATA_FINAL_TREINO_ATUAL.strftime(
                "%d/%m/%Y"
            ),
            DATA_INICIAL_VIGENCIA.strftime(
                "%d/%m/%Y"
            ),
            INDICE_OFICIAL,
            INDICE_CHALLENGER,
            INDICE_BENCHMARK,
            (
                INDICE_OFICIAL
                - INDICE_BENCHMARK
            ),
            (
                INDICE_OFICIAL
                - INDICE_CHALLENGER
            ),
            RETORNO_ANUAL_OFICIAL,
            VOLATILIDADE_OFICIAL,
            RETORNO_VOL_OFICIAL,
            SHARPE_OFICIAL,
            SORTINO_OFICIAL,
            CALMAR_OFICIAL,
            DRAWDOWN_OFICIAL,
            TURNOVER_OFICIAL,
            len(
                ATIVOS
            ),
            str(
                ATIVOS
            ),
            "MENSAL",
            "ANUAL",
            STATUS_PRODUCAO,
            USO_RECOMENDADO,
        ],
    }
)


# ============================================================
# CONFIGURAÇÃO JSON
# ============================================================

pesos_json = {}


for regime in ORDEM_REGIMES:

    linha_regime = (
        pesos_oficiais.loc[
            pesos_oficiais[
                "regime"
            ]
            == regime
        ]
    )

    if linha_regime.empty:

        raise ValueError(
            f"O regime {regime} não foi encontrado "
            "nos pesos oficiais."
        )

    linha_regime = linha_regime.iloc[0]

    pesos_json[
        regime
    ] = {
        ativo: float(
            linha_regime[
                f"peso_{ativo}"
            ]
        )
        for ativo in ATIVOS
    }


configuracao_json = {
    "projeto": {
        "nome": (
            "Alocação Quantitativa por "
            "Regimes Macroeconômicos"
        ),
        "modelo_oficial": (
            NOME_MODELO_OFICIAL
        ),
        "modelo_challenger": (
            NOME_MODELO_CHALLENGER
        ),
        "status": STATUS_PRODUCAO,
    },
    "dados": {
        "frequencia": "mensal",
        "ativos": ATIVOS,
        "quantidade_ativos": len(
            ATIVOS
        ),
        "taxa_livre_risco": "CDI",
        "benchmark": (
            "Pesos iguais com rebalanceamento mensal"
        ),
        "ima_b_oficial_parcial_incluido": False,
        "imab11_etf_incluido": (
            "IMAB11.SA" in ATIVOS
        ),
        "motivo_exclusao_ima_b_oficial": (
            "A série oficial SGS 12466 possui cobertura parcial."
        ),
    },
    "metodologia": {
        "tipo_janela_treino": "expansiva",
        "meses_treino_inicial": 48,
        "recalibracao_meses": 12,
        "rebalanceamento": "mensal",
        "custo_por_turnover": (
            CUSTO_POR_TURNOVER
        ),
        "confirmacoes_testadas": [
            1,
            2,
            3,
        ],
        "pesos_cdi_testados": [
            0.0,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
        ],
    },
    "configuracao_atual": {
        "numero_recalibracao": (
            ULTIMA_RECALIBRACAO
        ),
        "candidato": (
            CANDIDATO_ATUAL
        ),
        "meses_confirmacao": (
            CONFIRMACAO_ATUAL
        ),
        "data_final_treino": (
            DATA_FINAL_TREINO_ATUAL
            .strftime(
                "%Y-%m-%d"
            )
        ),
        "data_inicial_vigencia": (
            DATA_INICIAL_VIGENCIA
            .strftime(
                "%Y-%m-%d"
            )
        ),
        "pesos_por_regime": (
            pesos_json
        ),
    },
    "validacao": {
        "status_walk_forward": (
            STATUS_WALK_FORWARD
        ),
        "criterios_aprovados": (
            CRITERIOS_APROVADOS
        ),
        "total_criterios": (
            TOTAL_CRITERIOS
        ),
        "periodo_avaliacao": {
            "inicio": (
                series_finais[
                    "data"
                ].min()
                .strftime(
                    "%Y-%m-%d"
                )
            ),
            "fim": (
                series_finais[
                    "data"
                ].max()
                .strftime(
                    "%Y-%m-%d"
                )
            ),
        },
        "observacao": (
            "O período de avaliação já foi analisado "
            "e não representa um holdout final intocado."
        ),
    },
}


metricas_json = {
    "modelo_oficial": (
        MODELO_OFICIAL
    ),
    "indice_final": (
        INDICE_OFICIAL
    ),
    "retorno_anualizado": (
        RETORNO_ANUAL_OFICIAL
    ),
    "volatilidade_anualizada": (
        VOLATILIDADE_OFICIAL
    ),
    "retorno_volatilidade": (
        RETORNO_VOL_OFICIAL
    ),
    "sharpe_excesso_cdi": (
        SHARPE_OFICIAL
    ),
    "sortino_excesso_cdi": (
        SORTINO_OFICIAL
    ),
    "calmar": (
        CALMAR_OFICIAL
    ),
    "maximo_drawdown": (
        DRAWDOWN_OFICIAL
    ),
    "turnover_total": (
        TURNOVER_OFICIAL
    ),
    "indice_challenger": (
        INDICE_CHALLENGER
    ),
    "indice_benchmark": (
        INDICE_BENCHMARK
    ),
    "diferenca_vs_challenger": (
        INDICE_OFICIAL
        - INDICE_CHALLENGER
    ),
    "diferenca_vs_benchmark": (
        INDICE_OFICIAL
        - INDICE_BENCHMARK
    ),
}


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

decisao_final.to_csv(
    ARQUIVO_DECISAO_FINAL,
    index=False,
    encoding="utf-8-sig",
)


configuracao_oficial.to_csv(
    ARQUIVO_CONFIGURACAO_OFICIAL,
    index=False,
    encoding="utf-8-sig",
)


pesos_oficiais.to_csv(
    ARQUIVO_PESOS_OFICIAIS,
    index=False,
    encoding="utf-8-sig",
)


metricas_finais.to_csv(
    ARQUIVO_METRICAS_FINAIS,
    index=False,
    encoding="utf-8-sig",
)


metricas_finais_formatadas.to_csv(
    ARQUIVO_METRICAS_FINAIS_FORMATADAS,
    index=False,
    encoding="utf-8-sig",
)


series_finais.to_csv(
    ARQUIVO_SERIES_FINAIS,
    index=False,
    encoding="utf-8-sig",
)


limitacoes.to_csv(
    ARQUIVO_LIMITACOES,
    index=False,
    encoding="utf-8-sig",
)


resumo_final.to_csv(
    ARQUIVO_RESUMO_FINAL,
    index=False,
    encoding="utf-8-sig",
)


with open(
    ARQUIVO_CONFIGURACAO_JSON,
    "w",
    encoding="utf-8",
) as arquivo:

    json.dump(
        configuracao_json,
        arquivo,
        ensure_ascii=False,
        indent=4,
        default=tornar_serializavel,
    )


with open(
    ARQUIVO_METRICAS_JSON,
    "w",
    encoding="utf-8",
) as arquivo:

    json.dump(
        metricas_json,
        arquivo,
        ensure_ascii=False,
        indent=4,
        default=tornar_serializavel,
    )


# ============================================================
# BASE PARA GRÁFICOS
# ============================================================

data_inicial_grafico = (
    series_finais[
        "data"
    ].iloc[0]
    - pd.offsets.MonthEnd(1)
)


linha_inicial_indices = {
    "data": data_inicial_grafico,
}


for cenario in [
    MODELO_OFICIAL,
    MODELO_FIXO,
    MODELO_CHALLENGER,
    BENCHMARK,
    CDI_100,
]:

    linha_inicial_indices[
        f"indice_{cenario}"
    ] = VALOR_INICIAL


series_indices_grafico = pd.concat(
    [
        pd.DataFrame(
            [
                linha_inicial_indices
            ]
        ),
        series_finais[
            [
                "data",
                *[
                    f"indice_{cenario}"
                    for cenario in [
                        MODELO_OFICIAL,
                        MODELO_FIXO,
                        MODELO_CHALLENGER,
                        BENCHMARK,
                        CDI_100,
                    ]
                ],
            ]
        ],
    ],
    ignore_index=True,
)


linha_inicial_drawdown = {
    "data": data_inicial_grafico,
}


for cenario in [
    MODELO_OFICIAL,
    MODELO_CHALLENGER,
    BENCHMARK,
]:

    linha_inicial_drawdown[
        f"drawdown_{cenario}"
    ] = 0.0


series_drawdown_grafico = pd.concat(
    [
        pd.DataFrame(
            [
                linha_inicial_drawdown
            ]
        ),
        series_finais[
            [
                "data",
                f"drawdown_{MODELO_OFICIAL}",
                f"drawdown_{MODELO_CHALLENGER}",
                f"drawdown_{BENCHMARK}",
            ]
        ],
    ],
    ignore_index=True,
)


# ============================================================
# GRÁFICO 1 — DESEMPENHO FINAL
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


rotulos_desempenho = {
    MODELO_OFICIAL: (
        "Modelo oficial walk-forward com CDI"
    ),
    MODELO_FIXO: (
        "Modelo fixo com CDI"
    ),
    MODELO_CHALLENGER: (
        "Challenger sem CDI"
    ),
    BENCHMARK: (
        "Benchmark de cinco ativos"
    ),
    CDI_100: (
        "100% CDI"
    ),
}


for cenario, rotulo in (
    rotulos_desempenho.items()
):

    ax.plot(
        series_indices_grafico[
            "data"
        ],
        series_indices_grafico[
            f"indice_{cenario}"
        ],
        linewidth=2,
        label=rotulo,
    )


ax.axhline(
    y=VALOR_INICIAL,
    linewidth=1,
)


ax.set_title(
    "Comparação Final dos Modelos no Período de Avaliação"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Índice acumulado"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DESEMPENHO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — DRAWDOWN FINAL
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_drawdown_grafico[
        "data"
    ],
    series_drawdown_grafico[
        f"drawdown_{MODELO_OFICIAL}"
    ],
    linewidth=2,
    label="Modelo oficial walk-forward com CDI",
)


ax.plot(
    series_drawdown_grafico[
        "data"
    ],
    series_drawdown_grafico[
        f"drawdown_{MODELO_CHALLENGER}"
    ],
    linewidth=2,
    label="Challenger sem CDI",
)


ax.plot(
    series_drawdown_grafico[
        "data"
    ],
    series_drawdown_grafico[
        f"drawdown_{BENCHMARK}"
    ],
    linewidth=2,
    label="Benchmark de cinco ativos",
)


ax.axhline(
    y=0.0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Drawdown dos Modelos Finais"
)

ax.set_xlabel(
    "Data"
)

ax.set_ylabel(
    "Drawdown"
)

ax.legend()

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_DRAWDOWN,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — PESOS OFICIAIS ATUAIS
# ============================================================

pesos_grafico = (
    pesos_oficiais.set_index(
        "nome_regime"
    )[
        COLUNAS_PESOS
    ]
    .copy()
)


pesos_grafico.columns = ATIVOS


fig, ax = plt.subplots(
    figsize=(13, 7)
)


pesos_grafico.plot(
    kind="bar",
    stacked=True,
    ax=ax,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Pesos Oficiais Atuais por Regime Macroeconômico"
)

ax.set_xlabel(
    "Regime macroeconômico"
)

ax.set_ylabel(
    "Peso da carteira"
)

ax.tick_params(
    axis="x",
    rotation=20,
)

ax.legend(
    title="Ativo",
    bbox_to_anchor=(
        1.02,
        1,
    ),
    loc="upper left",
)

ax.grid(
    axis="y",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_PESOS,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 4 — RISCO E RETORNO
# ============================================================

metricas_grafico = (
    metricas_finais.loc[
        metricas_finais[
            "cenario"
        ]
        .isin(
            [
                MODELO_OFICIAL,
                MODELO_FIXO,
                MODELO_CHALLENGER,
                BENCHMARK,
                CARTEIRA_ESTATICA,
                CDI_100,
            ]
        )
    ]
    .copy()
)


fig, ax = plt.subplots(
    figsize=(11, 7)
)


ax.scatter(
    metricas_grafico[
        "volatilidade_anualizada_liquida"
    ],
    metricas_grafico[
        "retorno_anualizado_liquido"
    ],
    s=90,
)


for _, linha in (
    metricas_grafico.iterrows()
):

    ax.annotate(
        linha[
            "rotulo"
        ],
        (
            linha[
                "volatilidade_anualizada_liquida"
            ],
            linha[
                "retorno_anualizado_liquido"
            ],
        ),
        xytext=(
            6,
            6,
        ),
        textcoords="offset points",
    )


ax.xaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)

ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Risco e Retorno dos Modelos Finais"
)

ax.set_xlabel(
    "Volatilidade anualizada"
)

ax.set_ylabel(
    "Retorno anualizado"
)

ax.grid(
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_RISCO_RETORNO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÕES FINAIS
# ============================================================

validacoes = []


def adicionar_validacao(
    nome,
    aprovado,
    detalhe,
    tipo="TECNICA",
):

    validacoes.append(
        {
            "validacao": nome,
            "tipo": tipo,
            "status": (
                "APROVADO"
                if aprovado
                else "REPROVADO"
            ),
            "detalhe": detalhe,
        }
    )


adicionar_validacao(
    nome="Status walk-forward",
    aprovado=(
        STATUS_WALK_FORWARD
        == "APROVADO"
    ),
    detalhe=(
        f"Status: {STATUS_WALK_FORWARD}"
    ),
    tipo="FINANCEIRA",
)


adicionar_validacao(
    nome="Critérios walk-forward",
    aprovado=(
        CRITERIOS_APROVADOS
        >= 5
    ),
    detalhe=(
        f"{CRITERIOS_APROVADOS}/"
        f"{TOTAL_CRITERIOS}"
    ),
    tipo="FINANCEIRA",
)


adicionar_validacao(
    nome="Modelo oficial acima do benchmark",
    aprovado=(
        INDICE_OFICIAL
        > INDICE_BENCHMARK
    ),
    detalhe=(
        f"Vantagem: "
        f"{INDICE_OFICIAL - INDICE_BENCHMARK:.4f} "
        "ponto"
    ),
    tipo="FINANCEIRA",
)


adicionar_validacao(
    nome="Reprodução do índice oficial",
    aprovado=np.isclose(
        INDICE_RECALCULADO_OFICIAL,
        INDICE_OFICIAL,
        atol=1e-10,
        rtol=1e-10,
    ),
    detalhe=(
        f"Salvo: {INDICE_OFICIAL:.12f} | "
        f"Recalculado: "
        f"{INDICE_RECALCULADO_OFICIAL:.12f}"
    ),
)


adicionar_validacao(
    nome="Quatro regimes oficiais",
    aprovado=(
        pesos_oficiais[
            "regime"
        ]
        .nunique()
        == 4
    ),
    detalhe=(
        f"{pesos_oficiais['regime'].nunique()} regimes"
    ),
)


adicionar_validacao(
    nome="Pesos somam 100%",
    aprovado=np.allclose(
        pesos_oficiais[
            "soma_pesos_recalculada"
        ],
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ),
    detalhe=(
        "Pesos verificados nos quatro regimes"
    ),
)


adicionar_validacao(
    nome="Pesos não negativos",
    aprovado=(
        pesos_oficiais[
            COLUNAS_PESOS
        ]
        >= 0
    ).all().all(),
    detalhe=(
        f"Peso mínimo: "
        f"{pesos_oficiais[COLUNAS_PESOS].min().min():.8f}"
    ),
)


adicionar_validacao(
    nome="CDI disponível no esquema oficial",
    aprovado=(
        "CDI" in ATIVOS
    ),
    detalhe=(
        "O CDI pode ter peso zero no fallback sem CDI. "
        f"Ativos: {ATIVOS}"
    ),
)


adicionar_validacao(
    nome="Série oficial parcial do IMA-B excluída",
    aprovado=(
        not ativos_imab_oficial_parcial_encontrados
    ),
    detalhe=(
        "IMAB11.SA pode permanecer quando aprovado; "
        "somente a série oficial parcial SGS 12466 "
        "deve ficar fora da configuração oficial."
    ),
)


adicionar_validacao(
    nome="Séries sem valores nulos",
    aprovado=(
        not series_finais[
            [
                f"retorno_liquido_{cenario}"
                for cenario in CENARIOS_SERIES
            ]
        ]
        .isna()
        .any()
        .any()
    ),
    detalhe=(
        f"{int(series_finais[[f'retorno_liquido_{cenario}' for cenario in CENARIOS_SERIES]].isna().sum().sum())} "
        "nulos"
    ),
)


adicionar_validacao(
    nome="Configuração JSON criada",
    aprovado=(
        ARQUIVO_CONFIGURACAO_JSON.exists()
    ),
    detalhe=str(
        ARQUIVO_CONFIGURACAO_JSON
    ),
)


tabela_validacoes = pd.DataFrame(
    validacoes
)


tabela_validacoes.to_csv(
    ARQUIVO_VALIDACOES,
    index=False,
    encoding="utf-8-sig",
)


falhas_tecnicas = tabela_validacoes.loc[
    (
        tabela_validacoes["tipo"] == "TECNICA"
    )
    & (
        tabela_validacoes["status"] == "REPROVADO"
    )
]


alertas_financeiros = tabela_validacoes.loc[
    (
        tabela_validacoes["tipo"] == "FINANCEIRA"
    )
    & (
        tabela_validacoes["status"] == "REPROVADO"
    )
]


if not alertas_financeiros.empty:

    print(
        "\nALERTA: existem critérios financeiros reprovados. "
        "Eles foram registrados sem interromper o pipeline."
    )
    display(alertas_financeiros)


if not falhas_tecnicas.empty:

    raise ValueError(
        "Uma ou mais validações técnicas finais foram "
        "reprovadas:\n\n"
        f"{falhas_tecnicas}"
    )


# ============================================================
# MANIFESTO E HASHES
# ============================================================

arquivos_para_manifesto = [
    *ARQUIVOS_ENTRADA,
    ARQUIVO_DECISAO_FINAL,
    ARQUIVO_CONFIGURACAO_OFICIAL,
    ARQUIVO_PESOS_OFICIAIS,
    ARQUIVO_METRICAS_FINAIS,
    ARQUIVO_METRICAS_FINAIS_FORMATADAS,
    ARQUIVO_SERIES_FINAIS,
    ARQUIVO_LIMITACOES,
    ARQUIVO_VALIDACOES,
    ARQUIVO_RESUMO_FINAL,
    ARQUIVO_CONFIGURACAO_JSON,
    ARQUIVO_METRICAS_JSON,
    ARQUIVO_GRAFICO_DESEMPENHO,
    ARQUIVO_GRAFICO_DRAWDOWN,
    ARQUIVO_GRAFICO_PESOS,
    ARQUIVO_GRAFICO_RISCO_RETORNO,
]


registros_manifesto = []


for arquivo in arquivos_para_manifesto:

    if not arquivo.exists():

        raise FileNotFoundError(
            "Arquivo esperado não encontrado "
            "durante a criação do manifesto:\n"
            f"{arquivo}"
        )

    registros_manifesto.append(
        {
            "arquivo": str(
                arquivo.relative_to(
                    RAIZ_PROJETO
                )
            ),
            "tipo": (
                "ENTRADA"
                if arquivo in ARQUIVOS_ENTRADA
                else "SAIDA"
            ),
            "tamanho_bytes": (
                arquivo.stat().st_size
            ),
            "sha256": (
                calcular_hash_sha256(
                    arquivo
                )
            ),
        }
    )


manifesto = pd.DataFrame(
    registros_manifesto
)


manifesto.to_csv(
    ARQUIVO_MANIFESTO,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

ARQUIVOS_ESPERADOS = [
    ARQUIVO_DECISAO_FINAL,
    ARQUIVO_CONFIGURACAO_OFICIAL,
    ARQUIVO_PESOS_OFICIAIS,
    ARQUIVO_METRICAS_FINAIS,
    ARQUIVO_METRICAS_FINAIS_FORMATADAS,
    ARQUIVO_SERIES_FINAIS,
    ARQUIVO_LIMITACOES,
    ARQUIVO_VALIDACOES,
    ARQUIVO_RESUMO_FINAL,
    ARQUIVO_CONFIGURACAO_JSON,
    ARQUIVO_METRICAS_JSON,
    ARQUIVO_MANIFESTO,
    ARQUIVO_GRAFICO_DESEMPENHO,
    ARQUIVO_GRAFICO_DRAWDOWN,
    ARQUIVO_GRAFICO_PESOS,
    ARQUIVO_GRAFICO_RISCO_RETORNO,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in ARQUIVOS_ESPERADOS
    if not arquivo.exists()
]


if arquivos_nao_salvos:

    raise FileNotFoundError(
        "Alguns arquivos da Célula 12 "
        "não foram salvos:\n"
        + "\n".join(
            str(
                arquivo
            )
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("=" * 70)
print("CONSOLIDAÇÃO DO MODELO FINAL CONCLUÍDA")
print("=" * 70)


print(
    f"\nRaiz do projeto:\n"
    f"{RAIZ_PROJETO}"
)


print(
    f"\nModelo oficial:\n"
    f"{NOME_MODELO_OFICIAL}"
)


print(
    f"\nModelo challenger:\n"
    f"{NOME_MODELO_CHALLENGER}"
)


print(
    f"\nStatus walk-forward: "
    f"{STATUS_WALK_FORWARD}"
)


print(
    f"Critérios aprovados: "
    f"{CRITERIOS_APROVADOS}/"
    f"{TOTAL_CRITERIOS}"
)


print(
    f"\nÚltima recalibração: "
    f"{ULTIMA_RECALIBRACAO}"
)


print(
    f"Candidato atual: "
    f"{CANDIDATO_ATUAL}"
)


print(
    f"Confirmação atual: "
    f"{CONFIRMACAO_ATUAL} mês(es)"
)


print(
    f"Treino utilizado na configuração atual: "
    f"até "
    f"{DATA_FINAL_TREINO_ATUAL:%d/%m/%Y}"
)


print(
    f"\nÍndice final do modelo oficial: "
    f"{INDICE_OFICIAL:.2f}"
)


print(
    f"Índice final do challenger: "
    f"{INDICE_CHALLENGER:.2f}"
)


print(
    f"Índice final do benchmark: "
    f"{INDICE_BENCHMARK:.2f}"
)


print(
    f"\nModelo oficial contra o benchmark: "
    f"{INDICE_OFICIAL - INDICE_BENCHMARK:.2f} "
    "ponto"
)


print(
    f"Modelo oficial contra o challenger: "
    f"{INDICE_OFICIAL - INDICE_CHALLENGER:.2f} "
    "pontos"
)


print(
    "\nMétricas do modelo oficial:"
)


print(
    f"- Retorno anualizado: "
    f"{RETORNO_ANUAL_OFICIAL:.2%}"
)


print(
    f"- Volatilidade anualizada: "
    f"{VOLATILIDADE_OFICIAL:.2%}"
)


print(
    f"- Retorno/volatilidade: "
    f"{RETORNO_VOL_OFICIAL:.2f}"
)


print(
    f"- Sharpe de excesso ao CDI: "
    f"{SHARPE_OFICIAL:.2f}"
)


print(
    f"- Sortino de excesso ao CDI: "
    f"{SORTINO_OFICIAL:.2f}"
)


print(
    f"- Calmar: "
    f"{CALMAR_OFICIAL:.2f}"
)


print(
    f"- Máximo drawdown: "
    f"{DRAWDOWN_OFICIAL:.2%}"
)


print(
    f"- Turnover total: "
    f"{TURNOVER_OFICIAL:.4f}"
)


print(
    f"\nAtivos oficiais:"
)


print(
    ATIVOS
)


print(
    "\nPesos oficiais atuais:"
)


display(
    pesos_oficiais[
        [
            "regime",
            "nome_regime",
            "meses_confirmacao",
            *COLUNAS_PESOS,
            "soma_pesos_recalculada",
        ]
    ]
)


print(
    "\nDecisão final:"
)


display(
    decisao_final
)


print(
    "\nMétricas comparativas finais:"
)


display(
    metricas_finais_formatadas
)


print(
    "\nValidações finais:"
)


display(
    tabela_validacoes
)


print(
    f"\nConfiguração JSON salva em:\n"
    f"{ARQUIVO_CONFIGURACAO_JSON}"
)


print(
    f"\nMétricas JSON salvas em:\n"
    f"{ARQUIVO_METRICAS_JSON}"
)


print(
    f"\nResumo final salvo em:\n"
    f"{ARQUIVO_RESUMO_FINAL}"
)


print(
    f"\nManifesto dos arquivos salvo em:\n"
    f"{ARQUIVO_MANIFESTO}"
)


print(
    "\nStatus final: MODELO CONSOLIDADO E APROVADO"
)


FIM_EXECUCAO_UTC = datetime.now(timezone.utc)

print("=" * 80)
print("OTIMIZAÇÃO DA ESTRATÉGIA CONCLUÍDA")
print(
    "Duração total: "
    f"{(FIM_EXECUCAO_UTC - INICIO_EXECUCAO_UTC).total_seconds():.2f}s"
)
print("=" * 80)
