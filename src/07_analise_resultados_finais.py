# VERSAO_V3_PESOS_E_REGIMES_DO_MODELO_OFICIAL_CORRIGIDOS
from __future__ import annotations

import os
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

os.chdir(RAIZ_PROJETO)


def display(objeto) -> None:
    """
    Compatibilidade textual com as antigas chamadas display()
    utilizadas no notebook.
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
print("07 — ANÁLISE DOS RESULTADOS FINAIS")
print(f"Raiz do projeto: {RAIZ_PROJETO}")
print("=" * 80)


# ###########################################################################
# ETAPA 01 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# ETAPA 1 — CARREGAMENTO E VALIDAÇÃO DOS RESULTADOS FINAIS
# SCRIPT 07 — ANÁLISE DOS RESULTADOS FINAIS
# VERSÃO CORRIGIDA
# ============================================================

from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd

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
        / "outputs"
        / "modelo_final"
        / "modelo_oficial.json"
    )

    if arquivo_teste.exists():
        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:

    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo outputs/modelo_final/modelo_oficial.json "
        "não foi encontrado."
    )


PASTA_TABELAS = (
    RAIZ_PROJETO
    / "outputs"
    / "tabelas"
)

PASTA_MODELO_FINAL = (
    RAIZ_PROJETO
    / "outputs"
    / "modelo_final"
)


PASTA_TABELAS.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ARQUIVO_RESUMO_FINAL = (
    PASTA_TABELAS
    / "06_12_resumo_modelo_final.csv"
)

ARQUIVO_METRICAS_FINAIS = (
    PASTA_TABELAS
    / "06_12_metricas_finais_modelos.csv"
)

ARQUIVO_SERIES_FINAIS = (
    PASTA_TABELAS
    / "06_12_series_modelos_finais.csv"
)

ARQUIVO_PESOS_OFICIAIS = (
    PASTA_TABELAS
    / "06_12_pesos_oficiais_atuais.csv"
)

ARQUIVO_DECISAO_FINAL = (
    PASTA_TABELAS
    / "06_12_decisao_final_modelo.csv"
)

ARQUIVO_CONFIGURACAO_OFICIAL = (
    PASTA_TABELAS
    / "06_12_configuracao_modelo_oficial.csv"
)

ARQUIVO_LIMITACOES = (
    PASTA_TABELAS
    / "06_12_limitacoes_metodologicas.csv"
)

ARQUIVO_VALIDACOES_FINAIS = (
    PASTA_TABELAS
    / "06_12_validacoes_finais.csv"
)

ARQUIVO_MODELO_JSON = (
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


ARQUIVOS_ENTRADA = [
    ARQUIVO_RESUMO_FINAL,
    ARQUIVO_METRICAS_FINAIS,
    ARQUIVO_SERIES_FINAIS,
    ARQUIVO_PESOS_OFICIAIS,
    ARQUIVO_DECISAO_FINAL,
    ARQUIVO_CONFIGURACAO_OFICIAL,
    ARQUIVO_LIMITACOES,
    ARQUIVO_VALIDACOES_FINAIS,
    ARQUIVO_MODELO_JSON,
    ARQUIVO_METRICAS_JSON,
    ARQUIVO_MANIFESTO,
]


arquivos_ausentes = [
    arquivo
    for arquivo in ARQUIVOS_ENTRADA
    if not arquivo.exists()
]


if arquivos_ausentes:

    raise FileNotFoundError(
        "Arquivos finais não encontrados:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_INVENTARIO = (
    PASTA_TABELAS
    / "07_01_inventario_arquivos_finais.csv"
)

ARQUIVO_RESUMO_BASE = (
    PASTA_TABELAS
    / "07_01_resumo_base_final.csv"
)

ARQUIVO_VALIDACOES = (
    PASTA_TABELAS
    / "07_01_validacoes_entradas.csv"
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def calcular_sha256(caminho):

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


def obter_metrica(
    tabela,
    cenario,
    coluna,
):

    resultado = tabela.loc[
        tabela["cenario"].eq(
            cenario
        ),
        coluna,
    ]

    if len(resultado) != 1:

        raise ValueError(
            f"A métrica {coluna} do cenário "
            f"{cenario} deveria possuir uma linha."
        )

    return float(
        resultado.iloc[0]
    )


# ============================================================
# INVENTÁRIO DOS ARQUIVOS
# ============================================================

inventario_arquivos = pd.DataFrame(
    [
        {
            "arquivo": str(
                arquivo.relative_to(
                    RAIZ_PROJETO
                )
            ),
            "existe": arquivo.exists(),
            "tamanho_bytes": (
                arquivo.stat().st_size
            ),
            "sha256": calcular_sha256(
                arquivo
            ),
        }
        for arquivo in ARQUIVOS_ENTRADA
    ]
)


# ============================================================
# CARREGAMENTO DAS TABELAS
# ============================================================

resumo_final = pd.read_csv(
    ARQUIVO_RESUMO_FINAL,
    encoding="utf-8-sig",
)

metricas_finais = pd.read_csv(
    ARQUIVO_METRICAS_FINAIS,
    encoding="utf-8-sig",
)

series_finais = pd.read_csv(
    ARQUIVO_SERIES_FINAIS,
    encoding="utf-8-sig",
)

pesos_oficiais = pd.read_csv(
    ARQUIVO_PESOS_OFICIAIS,
    encoding="utf-8-sig",
)

decisao_final = pd.read_csv(
    ARQUIVO_DECISAO_FINAL,
    encoding="utf-8-sig",
)

configuracao_oficial = pd.read_csv(
    ARQUIVO_CONFIGURACAO_OFICIAL,
    encoding="utf-8-sig",
)

limitacoes = pd.read_csv(
    ARQUIVO_LIMITACOES,
    encoding="utf-8-sig",
)

validacoes_finais = pd.read_csv(
    ARQUIVO_VALIDACOES_FINAIS,
    encoding="utf-8-sig",
)

manifesto = pd.read_csv(
    ARQUIVO_MANIFESTO,
    encoding="utf-8-sig",
)


with open(
    ARQUIVO_MODELO_JSON,
    "r",
    encoding="utf-8",
) as arquivo:

    modelo_json = json.load(
        arquivo
    )


with open(
    ARQUIVO_METRICAS_JSON,
    "r",
    encoding="utf-8",
) as arquivo:

    metricas_json = json.load(
        arquivo
    )


# ============================================================
# PADRONIZAÇÃO DAS DATAS
# ============================================================

if "data" not in series_finais.columns:

    raise ValueError(
        "A série final não possui a coluna data."
    )


series_finais["data"] = pd.to_datetime(
    series_finais["data"],
    errors="coerce",
)


if series_finais["data"].isna().any():

    raise ValueError(
        "A série final possui datas inválidas."
    )


if series_finais["data"].duplicated().any():

    raise ValueError(
        "A série final possui datas duplicadas."
    )


series_finais.sort_values(
    "data",
    inplace=True,
)

series_finais.reset_index(
    drop=True,
    inplace=True,
)


# ============================================================
# IDENTIFICAÇÃO DO MODELO
# ============================================================

MODELO_OFICIAL = str(
    modelo_json[
        "projeto"
    ][
        "modelo_oficial"
    ]
)

MODELO_CHALLENGER = str(
    modelo_json[
        "projeto"
    ][
        "modelo_challenger"
    ]
)

STATUS_MODELO = str(
    modelo_json[
        "projeto"
    ][
        "status"
    ]
)

CANDIDATO_ATUAL = str(
    modelo_json[
        "configuracao_atual"
    ][
        "candidato"
    ]
)

CONFIRMACAO_ATUAL = int(
    modelo_json[
        "configuracao_atual"
    ][
        "meses_confirmacao"
    ]
)

ATIVOS_OFICIAIS = list(
    modelo_json[
        "dados"
    ][
        "ativos"
    ]
)


MAPA_MODELO_PARA_CENARIO = {
    "Modelo walk-forward com CDI": "WALK_FORWARD",
    "Modelo fixo da Célula 9": "MODELO_FIXO_CELULA_9",
    "Modelo fixo da Etapa 9": "MODELO_FIXO_CELULA_9",
    "Modelo anterior sem CDI": "MODELO_ANTERIOR_SEM_CDI",
    "Benchmark de cinco ativos": "BENCHMARK_5_ATIVOS",
    "Carteira estática": "CARTEIRA_ESTATICA",
    "100% CDI": "CDI_100",
}


CENARIO_OFICIAL_JSON = MAPA_MODELO_PARA_CENARIO.get(
    MODELO_OFICIAL
)

CENARIO_CHALLENGER_JSON = MAPA_MODELO_PARA_CENARIO.get(
    MODELO_CHALLENGER
)


if CENARIO_OFICIAL_JSON is None:

    raise ValueError(
        "O modelo oficial informado no JSON não possui "
        f"mapeamento de cenário: {MODELO_OFICIAL}"
    )


if CENARIO_CHALLENGER_JSON is None:

    raise ValueError(
        "O modelo challenger informado no JSON não possui "
        f"mapeamento de cenário: {MODELO_CHALLENGER}"
    )


# ============================================================
# CENÁRIOS ESPERADOS
# ============================================================

CENARIOS_ESPERADOS = [
    "WALK_FORWARD",
    "MODELO_FIXO_CELULA_9",
    "MODELO_ANTERIOR_SEM_CDI",
    "BENCHMARK_5_ATIVOS",
    "CARTEIRA_ESTATICA",
    "CDI_100",
]


if "cenario" not in metricas_finais.columns:

    raise ValueError(
        "A tabela de métricas não possui "
        "a coluna cenario."
    )


cenarios_ausentes = [
    cenario
    for cenario in CENARIOS_ESPERADOS
    if cenario not in (
        metricas_finais[
            "cenario"
        ]
        .astype(str)
        .tolist()
    )
]


if cenarios_ausentes:

    raise ValueError(
        "Cenários ausentes nas métricas finais:\n"
        f"{cenarios_ausentes}"
    )


if "rotulo" not in metricas_finais.columns:

    mapa_rotulos = {
        "WALK_FORWARD": (
            "Modelo walk-forward"
        ),
        "MODELO_FIXO_CELULA_9": (
            "Modelo fixo da Etapa 9"
        ),
        "MODELO_ANTERIOR_SEM_CDI": (
            "Modelo anterior sem CDI"
        ),
        "BENCHMARK_5_ATIVOS": (
            "Benchmark de cinco ativos"
        ),
        "CARTEIRA_ESTATICA": (
            "Carteira estática"
        ),
        "CDI_100": (
            "100% CDI"
        ),
    }

    metricas_finais["rotulo"] = (
        metricas_finais[
            "cenario"
        ].map(
            mapa_rotulos
        )
    )


# ============================================================
# CONVERSÃO DAS MÉTRICAS
# ============================================================

COLUNAS_METRICAS_OBRIGATORIAS = [
    "retorno_total_bruto",
    "retorno_total_liquido",
    "retorno_anualizado_liquido",
    "volatilidade_anualizada_liquida",
    "retorno_volatilidade",
    "sharpe_excesso_cdi",
    "sortino_excesso_cdi",
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

COLUNAS_METRICAS_OPCIONAIS = [
    "calmar",
]


colunas_ausentes = [
    coluna
    for coluna in (
        COLUNAS_METRICAS_OBRIGATORIAS
        + COLUNAS_METRICAS_OPCIONAIS
    )
    if coluna not in metricas_finais.columns
]


if colunas_ausentes:

    raise ValueError(
        "Colunas de métricas ausentes:\n"
        f"{colunas_ausentes}"
    )


for coluna in (
    COLUNAS_METRICAS_OBRIGATORIAS
    + COLUNAS_METRICAS_OPCIONAIS
):

    metricas_finais[coluna] = pd.to_numeric(
        metricas_finais[coluna],
        errors="coerce",
    )


nulos_obrigatorios = (
    metricas_finais[
        COLUNAS_METRICAS_OBRIGATORIAS
    ]
    .isna()
    .sum()
)

nulos_obrigatorios = (
    nulos_obrigatorios.loc[
        nulos_obrigatorios > 0
    ]
)


if not nulos_obrigatorios.empty:

    raise ValueError(
        "Existem métricas obrigatórias inválidas:\n"
        f"{nulos_obrigatorios}"
    )


# ============================================================
# TRATAMENTO CORRETO DO CALMAR
# ============================================================

metricas_finais[
    "calmar_indefinido"
] = (
    metricas_finais[
        "calmar"
    ].isna()
)


linhas_calmar_invalidas = (
    metricas_finais.loc[
        metricas_finais[
            "calmar_indefinido"
        ]
        & (
            metricas_finais[
                "maximo_drawdown"
            ]
            .abs()
            > 1e-12
        )
    ]
)


if not linhas_calmar_invalidas.empty:

    raise ValueError(
        "Existe Calmar ausente em cenário com "
        "drawdown diferente de zero:\n"
        f"{linhas_calmar_invalidas[['cenario', 'maximo_drawdown']]}"
    )


metricas_finais[
    "calmar_exibicao"
] = (
    metricas_finais[
        "calmar"
    ]
    .map(
        lambda valor: (
            f"{valor:.4f}"
            if pd.notna(
                valor
            )
            else "INDEFINIDO — DRAWDOWN ZERO"
        )
    )
)


# A cópia é criada somente após calmar_exibicao existir.
linhas_calmar_indefinido = (
    metricas_finais.loc[
        metricas_finais[
            "calmar_indefinido"
        ],
        [
            "cenario",
            "rotulo",
            "retorno_anualizado_liquido",
            "maximo_drawdown",
            "calmar",
            "calmar_exibicao",
        ],
    ]
    .copy()
)


# ============================================================
# MÉTRICAS PRINCIPAIS
# ============================================================

INDICE_OFICIAL = obter_metrica(
    metricas_finais,
    CENARIO_OFICIAL_JSON,
    "indice_final_liquido",
)

INDICE_CHALLENGER = obter_metrica(
    metricas_finais,
    CENARIO_CHALLENGER_JSON,
    "indice_final_liquido",
)

INDICE_BENCHMARK = obter_metrica(
    metricas_finais,
    "BENCHMARK_5_ATIVOS",
    "indice_final_liquido",
)

RETORNO_ANUAL_OFICIAL = obter_metrica(
    metricas_finais,
    CENARIO_OFICIAL_JSON,
    "retorno_anualizado_liquido",
)

VOLATILIDADE_OFICIAL = obter_metrica(
    metricas_finais,
    CENARIO_OFICIAL_JSON,
    "volatilidade_anualizada_liquida",
)

RETORNO_VOL_OFICIAL = obter_metrica(
    metricas_finais,
    CENARIO_OFICIAL_JSON,
    "retorno_volatilidade",
)

SHARPE_OFICIAL = obter_metrica(
    metricas_finais,
    CENARIO_OFICIAL_JSON,
    "sharpe_excesso_cdi",
)

SORTINO_OFICIAL = obter_metrica(
    metricas_finais,
    CENARIO_OFICIAL_JSON,
    "sortino_excesso_cdi",
)

CALMAR_OFICIAL = obter_metrica(
    metricas_finais,
    CENARIO_OFICIAL_JSON,
    "calmar",
)

DRAWDOWN_OFICIAL = obter_metrica(
    metricas_finais,
    CENARIO_OFICIAL_JSON,
    "maximo_drawdown",
)

TURNOVER_OFICIAL = obter_metrica(
    metricas_finais,
    CENARIO_OFICIAL_JSON,
    "turnover_total",
)


# ============================================================
# VALIDAÇÃO DOS PESOS
# ============================================================

if "regime" not in pesos_oficiais.columns:

    raise ValueError(
        "A tabela de pesos não possui a coluna regime."
    )


COLUNAS_PESOS = [
    coluna
    for coluna in pesos_oficiais.columns
    if coluna.startswith(
        "peso_"
    )
    and coluna != "soma_pesos"
]


if not COLUNAS_PESOS:

    raise ValueError(
        "Nenhuma coluna de peso foi encontrada."
    )


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
    "soma_pesos_validacao"
] = (
    pesos_oficiais[
        COLUNAS_PESOS
    ].sum(
        axis=1
    )
)


# ============================================================
# VALIDAÇÃO DAS SÉRIES
# ============================================================

COLUNAS_RETORNOS_ESPERADAS = [
    f"retorno_liquido_{cenario}"
    for cenario in CENARIOS_ESPERADOS
]


colunas_retorno_ausentes = [
    coluna
    for coluna in COLUNAS_RETORNOS_ESPERADAS
    if coluna not in series_finais.columns
]


if colunas_retorno_ausentes:

    raise ValueError(
        "Colunas de retorno ausentes:\n"
        f"{colunas_retorno_ausentes}"
    )


for coluna in COLUNAS_RETORNOS_ESPERADAS:

    series_finais[coluna] = pd.to_numeric(
        series_finais[coluna],
        errors="coerce",
    )


# ============================================================
# RESUMO DA BASE FINAL
# ============================================================

resumo_base_final = pd.DataFrame(
    {
        "metrica": [
            "Modelo oficial",
            "Modelo challenger",
            "Status do modelo",
            "Candidato atual",
            "Confirmação atual",
            "Quantidade de ativos",
            "Ativos oficiais",
            "Data inicial da avaliação",
            "Data final da avaliação",
            "Quantidade de meses",
            "Índice final oficial",
            "Índice final challenger",
            "Índice final benchmark",
            "Diferença oficial contra benchmark",
            "Diferença oficial contra challenger",
            "Retorno anualizado oficial",
            "Volatilidade anualizada oficial",
            "Retorno/volatilidade oficial",
            "Sharpe de excesso ao CDI",
            "Sortino de excesso ao CDI",
            "Calmar oficial",
            "Máximo drawdown",
            "Turnover total",
            "Cenários com Calmar indefinido",
            "Quantidade de limitações documentadas",
            "Quantidade de arquivos no manifesto",
        ],
        "valor": [
            MODELO_OFICIAL,
            MODELO_CHALLENGER,
            STATUS_MODELO,
            CANDIDATO_ATUAL,
            CONFIRMACAO_ATUAL,
            len(
                ATIVOS_OFICIAIS
            ),
            str(
                ATIVOS_OFICIAIS
            ),
            series_finais[
                "data"
            ].min().strftime(
                "%d/%m/%Y"
            ),
            series_finais[
                "data"
            ].max().strftime(
                "%d/%m/%Y"
            ),
            len(
                series_finais
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
                linhas_calmar_indefinido
            ),
            len(
                limitacoes
            ),
            len(
                manifesto
            ),
        ],
    }
)


# ============================================================
# VALIDAÇÕES
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


STATUS_MODELO_NORMALIZADO = STATUS_MODELO.upper()


adicionar_validacao(
    nome="Status do modelo",
    aprovado=(
        STATUS_MODELO_NORMALIZADO.startswith(
            "APROVADO"
        )
        or (
            "FALLBACK OFICIAL"
            in STATUS_MODELO_NORMALIZADO
        )
    ),
    detalhe=(
        f"Status: {STATUS_MODELO}"
    ),
)


adicionar_validacao(
    nome="Modelo oficial",
    aprovado=(
        CENARIO_OFICIAL_JSON
        in CENARIOS_ESPERADOS
    ),
    detalhe=(
        f"{MODELO_OFICIAL} -> "
        f"{CENARIO_OFICIAL_JSON}"
    ),
)


adicionar_validacao(
    nome="Quantidade de ativos",
    aprovado=(
        len(
            ATIVOS_OFICIAIS
        )
        >= 1
    ),
    detalhe=(
        f"{len(ATIVOS_OFICIAIS)} ativos: "
        f"{ATIVOS_OFICIAIS}"
    ),
)


adicionar_validacao(
    nome="CDI disponível",
    aprovado=(
        "CDI"
        in ATIVOS_OFICIAIS
    ),
    detalhe=(
        "O CDI pode ter peso zero no fallback sem CDI. "
        f"Ativos: {ATIVOS_OFICIAIS}"
    ),
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
    for ativo in ATIVOS_OFICIAIS
    if ativo.upper()
    in ATIVOS_IMAB_OFICIAL_PARCIAL
]


adicionar_validacao(
    nome="Série oficial parcial do IMA-B excluída",
    aprovado=(
        not ativos_imab_oficial_parcial_encontrados
    ),
    detalhe=(
        "IMAB11.SA pode permanecer quando aprovado. "
        "Somente a série oficial parcial SGS 12466 "
        "deve ficar fora do universo oficial."
    ),
)


adicionar_validacao(
    nome="Quatro regimes",
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
            "soma_pesos_validacao"
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
    nome="Período de avaliação",
    aprovado=(
        len(series_finais) > 0
    ),
    detalhe=(
        f"{len(series_finais)} meses"
    ),
)


adicionar_validacao(
    nome="Séries sem nulos",
    aprovado=(
        not series_finais[
            COLUNAS_RETORNOS_ESPERADAS
        ]
        .isna()
        .any()
        .any()
    ),
    detalhe=(
        f"{int(series_finais[COLUNAS_RETORNOS_ESPERADAS].isna().sum().sum())} "
        "nulos"
    ),
)


adicionar_validacao(
    nome="Métricas obrigatórias válidas",
    aprovado=(
        not metricas_finais[
            COLUNAS_METRICAS_OBRIGATORIAS
        ]
        .isna()
        .any()
        .any()
    ),
    detalhe=(
        "Nenhuma métrica obrigatória ausente"
    ),
)


adicionar_validacao(
    nome="Calmar indefinido justificado",
    aprovado=(
        linhas_calmar_invalidas.empty
    ),
    detalhe=(
        f"{len(linhas_calmar_indefinido)} "
        "cenário(s) com drawdown zero"
    ),
)


adicionar_validacao(
    nome="Modelo acima do benchmark",
    aprovado=(
        INDICE_OFICIAL
        > INDICE_BENCHMARK
    ),
    detalhe=(
        f"Vantagem: "
        f"{INDICE_OFICIAL - INDICE_BENCHMARK:.4f}"
    ),
)


adicionar_validacao(
    nome="Consistência do índice no JSON",
    aprovado=np.isclose(
        INDICE_OFICIAL,
        float(
            metricas_json[
                "indice_final"
            ]
        ),
        atol=1e-10,
        rtol=1e-10,
    ),
    detalhe=(
        f"CSV: {INDICE_OFICIAL:.12f} | "
        f"JSON: "
        f"{float(metricas_json['indice_final']):.12f}"
    ),
)


if "tipo" in validacoes_finais.columns:

    falhas_tecnicas_etapa_06 = validacoes_finais.loc[
        (
            validacoes_finais[
                "tipo"
            ]
            .astype(str)
            .str.upper()
            .eq(
                "TECNICA"
            )
        )
        & (
            validacoes_finais[
                "status"
            ]
            .astype(str)
            .str.upper()
            .eq(
                "REPROVADO"
            )
        )
    ].copy()

else:

    falhas_tecnicas_etapa_06 = validacoes_finais.loc[
        validacoes_finais[
            "status"
        ]
        .astype(str)
        .str.upper()
        .eq(
            "REPROVADO"
        )
    ].copy()


adicionar_validacao(
    nome="Validações técnicas da Etapa 06",
    aprovado=(
        falhas_tecnicas_etapa_06.empty
    ),
    detalhe=(
        "Nenhuma validação técnica final reprovada"
        if falhas_tecnicas_etapa_06.empty
        else falhas_tecnicas_etapa_06.to_string(
            index=False
        )
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
        "Uma ou mais validações da Etapa 1 "
        "foram reprovadas:\n\n"
        f"{tabela_validacoes}"
    )


# ============================================================
# SALVAMENTO
# ============================================================

inventario_arquivos.to_csv(
    ARQUIVO_INVENTARIO,
    index=False,
    encoding="utf-8-sig",
)


resumo_base_final.to_csv(
    ARQUIVO_RESUMO_BASE,
    index=False,
    encoding="utf-8-sig",
)


tabela_validacoes.to_csv(
    ARQUIVO_VALIDACOES,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

ARQUIVOS_SAIDA = [
    ARQUIVO_INVENTARIO,
    ARQUIVO_RESUMO_BASE,
    ARQUIVO_VALIDACOES,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in ARQUIVOS_SAIDA
    if not arquivo.exists()
]


if arquivos_nao_salvos:

    raise FileNotFoundError(
        "Arquivos da Etapa 1 não foram salvos:\n"
        + "\n".join(
            str(arquivo)
            for arquivo in arquivos_nao_salvos
        )
    )


# ============================================================
# RESULTADOS
# ============================================================

print("=" * 70)
print("SCRIPT 07 — BASE FINAL CARREGADA E VALIDADA")
print("=" * 70)


print(
    f"\nRaiz do projeto:\n"
    f"{RAIZ_PROJETO}"
)


print(
    f"\nModelo oficial: "
    f"{MODELO_OFICIAL}"
)


print(
    f"Modelo challenger: "
    f"{MODELO_CHALLENGER}"
)


print(
    f"Status: "
    f"{STATUS_MODELO}"
)


print(
    f"\nCandidato atual: "
    f"{CANDIDATO_ATUAL}"
)


print(
    f"Confirmação atual: "
    f"{CONFIRMACAO_ATUAL} mês(es)"
)


print(
    f"\nPeríodo de avaliação: "
    f"{series_finais['data'].min():%d/%m/%Y} "
    f"a "
    f"{series_finais['data'].max():%d/%m/%Y}"
)


print(
    f"Quantidade de meses: "
    f"{len(series_finais)}"
)


print(
    f"\nÍndice final oficial: "
    f"{INDICE_OFICIAL:.2f}"
)


print(
    f"Índice final challenger: "
    f"{INDICE_CHALLENGER:.2f}"
)


print(
    f"Índice final benchmark: "
    f"{INDICE_BENCHMARK:.2f}"
)


print(
    f"\nVantagem contra o benchmark: "
    f"{INDICE_OFICIAL - INDICE_BENCHMARK:.2f} ponto"
)


print(
    f"Resultado contra o challenger: "
    f"{INDICE_OFICIAL - INDICE_CHALLENGER:.2f} pontos"
)


print(
    f"\nRetorno anualizado: "
    f"{RETORNO_ANUAL_OFICIAL:.2%}"
)


print(
    f"Volatilidade anualizada: "
    f"{VOLATILIDADE_OFICIAL:.2%}"
)


print(
    f"Retorno/volatilidade: "
    f"{RETORNO_VOL_OFICIAL:.2f}"
)


print(
    f"Sharpe de excesso ao CDI: "
    f"{SHARPE_OFICIAL:.2f}"
)


print(
    f"Sortino de excesso ao CDI: "
    f"{SORTINO_OFICIAL:.2f}"
)


print(
    f"Calmar oficial: "
    f"{CALMAR_OFICIAL:.2f}"
)


print(
    f"Máximo drawdown: "
    f"{DRAWDOWN_OFICIAL:.2%}"
)


print(
    f"Turnover total: "
    f"{TURNOVER_OFICIAL:.4f}"
)


print(
    f"\nCenários com Calmar indefinido: "
    f"{len(linhas_calmar_indefinido)}"
)


if not linhas_calmar_indefinido.empty:

    print(
        "\nCenários com drawdown zero "
        "e Calmar indefinido:"
    )

    display(
        linhas_calmar_indefinido
    )


print(
    f"\nAtivos oficiais:\n"
    f"{ATIVOS_OFICIAIS}"
)


print(
    f"\nInventário salvo em:\n"
    f"{ARQUIVO_INVENTARIO}"
)


print(
    f"\nResumo da base salvo em:\n"
    f"{ARQUIVO_RESUMO_BASE}"
)


print(
    "\nResumo da base final:"
)


display(
    resumo_base_final
)


print(
    "\nValidações:"
)


display(
    tabela_validacoes
)

# ###########################################################################
# ETAPA 02 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# ETAPA 2 — COMPARAÇÃO DE DESEMPENHO E RISCO
# SCRIPT 07 — ANÁLISE DOS RESULTADOS FINAIS
# VERSÃO AUTÔNOMA
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter


# ============================================================
# CONFIGURAÇÕES
# ============================================================

VALOR_INICIAL = 100.0
PERIODOS_POR_ANO = 12

CENARIO_OFICIAL = CENARIO_OFICIAL_JSON
CENARIO_MODELO_FIXO = "MODELO_FIXO_CELULA_9"
CENARIO_CHALLENGER = CENARIO_CHALLENGER_JSON
CENARIO_BENCHMARK = "BENCHMARK_5_ATIVOS"
CENARIO_ESTATICO = "CARTEIRA_ESTATICA"
CENARIO_CDI = "CDI_100"

CENARIOS = [
    CENARIO_OFICIAL,
    CENARIO_MODELO_FIXO,
    CENARIO_CHALLENGER,
    CENARIO_BENCHMARK,
    CENARIO_ESTATICO,
    CENARIO_CDI,
]

ROTULOS = {
    CENARIO_OFICIAL: (
        f"Modelo oficial — {MODELO_OFICIAL}"
    ),
    CENARIO_MODELO_FIXO: (
        "Modelo fixo com CDI"
    ),
    CENARIO_CHALLENGER: (
        f"Challenger — {MODELO_CHALLENGER}"
    ),
    CENARIO_BENCHMARK: (
        "Benchmark de cinco ativos"
    ),
    CENARIO_ESTATICO: (
        "Carteira estática"
    ),
    CENARIO_CDI: (
        "100% CDI"
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
        / "outputs"
        / "tabelas"
        / "07_01_validacoes_entradas.csv"
    )

    if arquivo_teste.exists():

        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:

    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo outputs/tabelas/"
        "07_01_validacoes_entradas.csv não foi encontrado."
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

ARQUIVO_VALIDACOES_CELULA_1 = (
    PASTA_TABELAS
    / "07_01_validacoes_entradas.csv"
)

ARQUIVO_METRICAS_FINAIS = (
    PASTA_TABELAS
    / "06_12_metricas_finais_modelos.csv"
)

ARQUIVO_SERIES_FINAIS = (
    PASTA_TABELAS
    / "06_12_series_modelos_finais.csv"
)


ARQUIVOS_ENTRADA = [
    ARQUIVO_VALIDACOES_CELULA_1,
    ARQUIVO_METRICAS_FINAIS,
    ARQUIVO_SERIES_FINAIS,
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
            str(arquivo)
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_COMPARACAO = (
    PASTA_TABELAS
    / "07_02_comparacao_desempenho_risco.csv"
)

ARQUIVO_COMPARACAO_FORMATADA = (
    PASTA_TABELAS
    / "07_02_comparacao_desempenho_risco_formatada.csv"
)

ARQUIVO_RESULTADOS_ANUAIS = (
    PASTA_TABELAS
    / "07_02_resultados_anuais.csv"
)

ARQUIVO_RESULTADOS_ANUAIS_FORMATADOS = (
    PASTA_TABELAS
    / "07_02_resultados_anuais_formatados.csv"
)

ARQUIVO_COMPARACAO_MENSAL = (
    PASTA_TABELAS
    / "07_02_comparacao_mensal_modelo_oficial.csv"
)

ARQUIVO_POSICOES_METRICAS = (
    PASTA_TABELAS
    / "07_02_posicoes_por_metrica.csv"
)

ARQUIVO_CONCLUSOES = (
    PASTA_TABELAS
    / "07_02_conclusoes_comparativas.csv"
)

ARQUIVO_VALIDACOES = (
    PASTA_TABELAS
    / "07_02_validacoes.csv"
)

ARQUIVO_GRAFICO_DESEMPENHO = (
    PASTA_GRAFICOS
    / "07_02_desempenho_acumulado.png"
)

ARQUIVO_GRAFICO_ANUAL = (
    PASTA_GRAFICOS
    / "07_02_retornos_anuais.png"
)

ARQUIVO_GRAFICO_RISCO_RETORNO = (
    PASTA_GRAFICOS
    / "07_02_risco_retorno.png"
)

ARQUIVO_GRAFICO_DRAWDOWN = (
    PASTA_GRAFICOS
    / "07_02_drawdown_comparativo.png"
)


# ============================================================
# CARREGAMENTO
# ============================================================

validacoes_celula_1 = pd.read_csv(
    ARQUIVO_VALIDACOES_CELULA_1,
    encoding="utf-8-sig",
)

metricas_finais = pd.read_csv(
    ARQUIVO_METRICAS_FINAIS,
    encoding="utf-8-sig",
)

series_finais = pd.read_csv(
    ARQUIVO_SERIES_FINAIS,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DA ETAPA ANTERIOR
# ============================================================

if not {
    "validacao",
    "status",
    "detalhe",
}.issubset(
    validacoes_celula_1.columns
):

    raise ValueError(
        "O arquivo de validações da Etapa 1 "
        "possui estrutura inválida."
    )


if (
    validacoes_celula_1[
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
        "A Etapa 1 possui validações reprovadas."
    )


# ============================================================
# PADRONIZAÇÃO DAS DATAS
# ============================================================

if "data" not in series_finais.columns:

    raise ValueError(
        "A série final não possui a coluna data."
    )


series_finais[
    "data"
] = pd.to_datetime(
    series_finais[
        "data"
    ],
    errors="coerce",
)


if series_finais[
    "data"
].isna().any():

    raise ValueError(
        "Foram encontradas datas inválidas."
    )


if series_finais[
    "data"
].duplicated().any():

    raise ValueError(
        "Foram encontradas datas duplicadas."
    )


series_finais.sort_values(
    "data",
    inplace=True,
)

series_finais.reset_index(
    drop=True,
    inplace=True,
)


# ============================================================
# VALIDAÇÃO DOS CENÁRIOS
# ============================================================

if "cenario" not in metricas_finais.columns:

    raise ValueError(
        "A tabela de métricas não possui "
        "a coluna cenario."
    )


cenarios_encontrados = (
    metricas_finais[
        "cenario"
    ]
    .astype(str)
    .unique()
    .tolist()
)


cenarios_ausentes = [
    cenario
    for cenario in CENARIOS
    if cenario not in cenarios_encontrados
]


if cenarios_ausentes:

    raise ValueError(
        "Cenários ausentes:\n"
        f"{cenarios_ausentes}"
    )


if metricas_finais[
    "cenario"
].duplicated().any():

    cenarios_duplicados = (
        metricas_finais.loc[
            metricas_finais[
                "cenario"
            ].duplicated(
                keep=False
            ),
            "cenario",
        ]
        .tolist()
    )

    raise ValueError(
        "Existem cenários duplicados:\n"
        f"{cenarios_duplicados}"
    )


# ============================================================
# CONVERSÃO DAS MÉTRICAS
# ============================================================

COLUNAS_METRICAS = [
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
    "custo_acumulado_simples",
    "indice_final_liquido",
]


colunas_metricas_ausentes = [
    coluna
    for coluna in COLUNAS_METRICAS
    if coluna not in metricas_finais.columns
]


if colunas_metricas_ausentes:

    raise ValueError(
        "Métricas ausentes:\n"
        f"{colunas_metricas_ausentes}"
    )


for coluna in COLUNAS_METRICAS:

    metricas_finais[
        coluna
    ] = pd.to_numeric(
        metricas_finais[
            coluna
        ],
        errors="coerce",
    )


COLUNAS_OBRIGATORIAS_SEM_CALMAR = [
    coluna
    for coluna in COLUNAS_METRICAS
    if coluna != "calmar"
]


if metricas_finais[
    COLUNAS_OBRIGATORIAS_SEM_CALMAR
].isna().any().any():

    nulos = (
        metricas_finais[
            COLUNAS_OBRIGATORIAS_SEM_CALMAR
        ]
        .isna()
        .sum()
    )

    nulos = nulos.loc[
        nulos > 0
    ]

    raise ValueError(
        "Existem métricas obrigatórias inválidas:\n"
        f"{nulos}"
    )


# ============================================================
# CONVERSÃO DAS SÉRIES DE RETORNO
# ============================================================

COLUNAS_RETORNOS = {
    cenario: (
        f"retorno_liquido_{cenario}"
    )
    for cenario in CENARIOS
}


for cenario, coluna in (
    COLUNAS_RETORNOS.items()
):

    if coluna not in series_finais.columns:

        raise ValueError(
            f"A coluna {coluna} não foi encontrada."
        )

    series_finais[
        coluna
    ] = pd.to_numeric(
        series_finais[
            coluna
        ],
        errors="coerce",
    )

    if series_finais[
        coluna
    ].isna().any():

        raise ValueError(
            f"A coluna {coluna} possui "
            "retornos inválidos."
        )


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def calcular_retorno_total(
    retornos,
):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    return float(
        np.prod(
            1.0
            + retornos
        )
        - 1.0
    )


def calcular_indice(
    retornos,
):

    retornos = pd.Series(
        retornos,
        dtype=float,
    )

    return (
        VALOR_INICIAL
        * (
            1.0
            + retornos
        ).cumprod()
    )


def calcular_drawdown(
    retornos,
):

    indice = calcular_indice(
        retornos
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

    return (
        drawdown.iloc[
            1:
        ]
        .reset_index(
            drop=True
        )
    )


def obter_linha_cenario(
    cenario,
):

    linha = (
        metricas_finais.loc[
            metricas_finais[
                "cenario"
            ]
            .eq(
                cenario
            )
        ]
    )

    if len(linha) != 1:

        raise ValueError(
            f"O cenário {cenario} deveria "
            "possuir exatamente uma linha."
        )

    return linha.iloc[0]


# ============================================================
# RECONSTRUÇÃO DOS ÍNDICES E DRAWDOWNS
# ============================================================

for cenario in CENARIOS:

    coluna_retorno = (
        COLUNAS_RETORNOS[
            cenario
        ]
    )

    series_finais[
        f"indice_recalculado_{cenario}"
    ] = calcular_indice(
        series_finais[
            coluna_retorno
        ]
    )

    series_finais[
        f"drawdown_recalculado_{cenario}"
    ] = calcular_drawdown(
        series_finais[
            coluna_retorno
        ]
    )


# ============================================================
# TABELA COMPARATIVA
# ============================================================

registros_comparacao = []


for cenario in CENARIOS:

    linha = obter_linha_cenario(
        cenario
    )

    registros_comparacao.append(
        {
            "cenario": cenario,
            "modelo": ROTULOS[
                cenario
            ],
            "retorno_total_liquido": float(
                linha[
                    "retorno_total_liquido"
                ]
            ),
            "retorno_anualizado": float(
                linha[
                    "retorno_anualizado_liquido"
                ]
            ),
            "volatilidade_anualizada": float(
                linha[
                    "volatilidade_anualizada_liquida"
                ]
            ),
            "retorno_volatilidade": float(
                linha[
                    "retorno_volatilidade"
                ]
            ),
            "sharpe_excesso_cdi": float(
                linha[
                    "sharpe_excesso_cdi"
                ]
            ),
            "sortino_excesso_cdi": float(
                linha[
                    "sortino_excesso_cdi"
                ]
            ),
            "calmar": (
                float(
                    linha[
                        "calmar"
                    ]
                )
                if pd.notna(
                    linha[
                        "calmar"
                    ]
                )
                else np.nan
            ),
            "maximo_drawdown": float(
                linha[
                    "maximo_drawdown"
                ]
            ),
            "meses_positivos": float(
                linha[
                    "meses_positivos"
                ]
            ),
            "melhor_mes": float(
                linha[
                    "melhor_mes"
                ]
            ),
            "pior_mes": float(
                linha[
                    "pior_mes"
                ]
            ),
            "turnover_total": float(
                linha[
                    "turnover_total"
                ]
            ),
            "custo_acumulado_simples": float(
                linha[
                    "custo_acumulado_simples"
                ]
            ),
            "indice_final": float(
                linha[
                    "indice_final_liquido"
                ]
            ),
        }
    )


comparacao = pd.DataFrame(
    registros_comparacao
)


linha_benchmark = (
    comparacao.loc[
        comparacao[
            "cenario"
        ]
        .eq(
            CENARIO_BENCHMARK
        )
    ]
    .iloc[0]
)


linha_oficial = (
    comparacao.loc[
        comparacao[
            "cenario"
        ]
        .eq(
            CENARIO_OFICIAL
        )
    ]
    .iloc[0]
)


comparacao[
    "diferenca_indice_vs_benchmark"
] = (
    comparacao[
        "indice_final"
    ]
    - float(
        linha_benchmark[
            "indice_final"
        ]
    )
)


comparacao[
    "diferenca_indice_vs_oficial"
] = (
    comparacao[
        "indice_final"
    ]
    - float(
        linha_oficial[
            "indice_final"
        ]
    )
)


comparacao[
    "diferenca_retorno_anual_vs_benchmark"
] = (
    comparacao[
        "retorno_anualizado"
    ]
    - float(
        linha_benchmark[
            "retorno_anualizado"
        ]
    )
)


comparacao[
    "diferenca_volatilidade_vs_benchmark"
] = (
    comparacao[
        "volatilidade_anualizada"
    ]
    - float(
        linha_benchmark[
            "volatilidade_anualizada"
        ]
    )
)


# ============================================================
# POSIÇÕES POR MÉTRICA
# NÃO É CRIADO UM SCORE AGREGADO
# ============================================================

posicoes_metricas = (
    comparacao[
        [
            "cenario",
            "modelo",
        ]
    ]
    .copy()
)


posicoes_metricas[
    "posicao_retorno_anualizado"
] = (
    comparacao[
        "retorno_anualizado"
    ]
    .rank(
        method="min",
        ascending=False,
    )
    .astype(int)
)


posicoes_metricas[
    "posicao_menor_volatilidade"
] = (
    comparacao[
        "volatilidade_anualizada"
    ]
    .rank(
        method="min",
        ascending=True,
    )
    .astype(int)
)


posicoes_metricas[
    "posicao_retorno_volatilidade"
] = (
    comparacao[
        "retorno_volatilidade"
    ]
    .rank(
        method="min",
        ascending=False,
    )
    .astype(int)
)


posicoes_metricas[
    "posicao_sharpe"
] = (
    comparacao[
        "sharpe_excesso_cdi"
    ]
    .rank(
        method="min",
        ascending=False,
    )
    .astype(int)
)


posicoes_metricas[
    "posicao_sortino"
] = (
    comparacao[
        "sortino_excesso_cdi"
    ]
    .rank(
        method="min",
        ascending=False,
    )
    .astype(int)
)


posicoes_metricas[
    "posicao_menor_drawdown"
] = (
    comparacao[
        "maximo_drawdown"
    ]
    .rank(
        method="min",
        ascending=False,
    )
    .astype(int)
)


posicoes_metricas[
    "observacao"
] = (
    "As posições são independentes por métrica. "
    "Não foi calculado score agregado."
)


# ============================================================
# RESULTADOS ANUAIS
# ============================================================

series_finais[
    "ano"
] = (
    series_finais[
        "data"
    ]
    .dt.year
)


registros_anuais = []


for ano, dados_ano in (
    series_finais.groupby(
        "ano",
        sort=True,
    )
):

    quantidade_meses_ano = len(
        dados_ano
    )

    periodo_ano = (
        str(
            int(ano)
        )
        if quantidade_meses_ano == 12
        else (
            f"{int(ano)} — parcial "
            f"({quantidade_meses_ano} meses)"
        )
    )

    retorno_benchmark_ano = (
        calcular_retorno_total(
            dados_ano[
                COLUNAS_RETORNOS[
                    CENARIO_BENCHMARK
                ]
            ]
        )
    )

    for cenario in CENARIOS:

        retorno_ano = calcular_retorno_total(
            dados_ano[
                COLUNAS_RETORNOS[
                    cenario
                ]
            ]
        )

        registros_anuais.append(
            {
                "ano": int(
                    ano
                ),
                "periodo": periodo_ano,
                "quantidade_meses": (
                    quantidade_meses_ano
                ),
                "cenario": cenario,
                "modelo": ROTULOS[
                    cenario
                ],
                "retorno_liquido": retorno_ano,
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


# ============================================================
# COMPARAÇÃO MENSAL DO MODELO OFICIAL
# ============================================================

retorno_oficial_mensal = (
    series_finais[
        COLUNAS_RETORNOS[
            CENARIO_OFICIAL
        ]
    ]
)


registros_comparacao_mensal = []


for cenario in [
    CENARIO_MODELO_FIXO,
    CENARIO_CHALLENGER,
    CENARIO_BENCHMARK,
    CENARIO_ESTATICO,
    CENARIO_CDI,
]:

    retorno_comparador = (
        series_finais[
            COLUNAS_RETORNOS[
                cenario
            ]
        ]
    )

    diferenca = (
        retorno_oficial_mensal
        - retorno_comparador
    )

    registros_comparacao_mensal.append(
        {
            "comparador": cenario,
            "modelo_comparador": ROTULOS[
                cenario
            ],
            "quantidade_meses": len(
                diferenca
            ),
            "meses_modelo_oficial_superou": int(
                diferenca.gt(
                    0
                ).sum()
            ),
            "meses_modelo_oficial_empatou": int(
                np.isclose(
                    diferenca,
                    0.0,
                    atol=1e-12,
                    rtol=1e-12,
                ).sum()
            ),
            "meses_modelo_oficial_perdeu": int(
                diferenca.lt(
                    0
                ).sum()
            ),
            "proporcao_meses_superou": float(
                diferenca.gt(
                    0
                ).mean()
            ),
            "excesso_medio_mensal": float(
                diferenca.mean()
            ),
            "melhor_excesso_mensal": float(
                diferenca.max()
            ),
            "pior_excesso_mensal": float(
                diferenca.min()
            ),
        }
    )


comparacao_mensal = pd.DataFrame(
    registros_comparacao_mensal
)


# ============================================================
# TABELAS FORMATADAS
# ============================================================

comparacao_formatada = (
    comparacao
    .copy()
    .astype(object)
)


COLUNAS_PERCENTUAIS_COMPARACAO = [
    "retorno_total_liquido",
    "retorno_anualizado",
    "volatilidade_anualizada",
    "maximo_drawdown",
    "meses_positivos",
    "melhor_mes",
    "pior_mes",
    "custo_acumulado_simples",
    "diferenca_retorno_anual_vs_benchmark",
    "diferenca_volatilidade_vs_benchmark",
]


for coluna in (
    COLUNAS_PERCENTUAIS_COMPARACAO
):

    comparacao_formatada[
        coluna
    ] = comparacao[
        coluna
    ].map(
        lambda valor: (
            f"{valor:.2%}"
            if pd.notna(
                valor
            )
            else "-"
        )
    )


COLUNAS_DECIMAIS_COMPARACAO = [
    "retorno_volatilidade",
    "sharpe_excesso_cdi",
    "sortino_excesso_cdi",
    "calmar",
    "turnover_total",
    "indice_final",
    "diferenca_indice_vs_benchmark",
    "diferenca_indice_vs_oficial",
]


for coluna in (
    COLUNAS_DECIMAIS_COMPARACAO
):

    comparacao_formatada[
        coluna
    ] = comparacao[
        coluna
    ].map(
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
                "INDEFINIDO"
                if pd.isna(
                    valor
                )
                else "∞"
            )
        )
    )


resultados_anuais_formatados = (
    resultados_anuais
    .copy()
    .astype(object)
)


for coluna in [
    "retorno_liquido",
    "retorno_benchmark",
    "excesso_vs_benchmark",
]:

    resultados_anuais_formatados[
        coluna
    ] = resultados_anuais[
        coluna
    ].map(
        lambda valor: (
            f"{valor:.2%}"
        )
    )


# ============================================================
# CONCLUSÕES COMPARATIVAS
# ============================================================

linha_challenger = (
    comparacao.loc[
        comparacao[
            "cenario"
        ]
        .eq(
            CENARIO_CHALLENGER
        )
    ]
    .iloc[0]
)


linha_estatica = (
    comparacao.loc[
        comparacao[
            "cenario"
        ]
        .eq(
            CENARIO_ESTATICO
        )
    ]
    .iloc[0]
)


linha_cdi = (
    comparacao.loc[
        comparacao[
            "cenario"
        ]
        .eq(
            CENARIO_CDI
        )
    ]
    .iloc[0]
)


anos_oficial = (
    resultados_anuais.loc[
        resultados_anuais[
            "cenario"
        ]
        .eq(
            CENARIO_OFICIAL
        )
    ]
)


quantidade_anos_superou_benchmark = int(
    anos_oficial[
        "superou_benchmark"
    ].sum()
)


quantidade_anos_avaliados = int(
    len(
        anos_oficial
    )
)


conclusoes = pd.DataFrame(
    [
        {
            "tema": "Resultado contra o benchmark",
            "conclusao": (
                "O modelo oficial superou o benchmark."
                if float(
                    linha_oficial[
                        "indice_final"
                    ]
                )
                > float(
                    linha_benchmark[
                        "indice_final"
                    ]
                )
                else (
                    "O modelo oficial não superou "
                    "o benchmark."
                )
            ),
            "valor": (
                float(
                    linha_oficial[
                        "indice_final"
                    ]
                )
                - float(
                    linha_benchmark[
                        "indice_final"
                    ]
                )
            ),
            "unidade": "pontos de índice",
        },
        {
            "tema": "Resultado contra o challenger",
            "conclusao": (
                "O challenger apresentou maior "
                "retorno absoluto."
                if float(
                    linha_challenger[
                        "indice_final"
                    ]
                )
                > float(
                    linha_oficial[
                        "indice_final"
                    ]
                )
                else (
                    "O modelo oficial apresentou maior "
                    "retorno absoluto que o challenger."
                )
            ),
            "valor": (
                float(
                    linha_oficial[
                        "indice_final"
                    ]
                )
                - float(
                    linha_challenger[
                        "indice_final"
                    ]
                )
            ),
            "unidade": "pontos de índice",
        },
        {
            "tema": "Valor da alocação dinâmica",
            "conclusao": (
                "A alocação dinâmica superou "
                "a carteira estática."
                if float(
                    linha_oficial[
                        "indice_final"
                    ]
                )
                > float(
                    linha_estatica[
                        "indice_final"
                    ]
                )
                else (
                    "A carteira estática superou "
                    "a alocação dinâmica."
                )
            ),
            "valor": (
                float(
                    linha_oficial[
                        "indice_final"
                    ]
                )
                - float(
                    linha_estatica[
                        "indice_final"
                    ]
                )
            ),
            "unidade": "pontos de índice",
        },
        {
            "tema": "Retorno sobre o CDI",
            "conclusao": (
                "O modelo oficial superou "
                "uma carteira de 100% CDI."
                if float(
                    linha_oficial[
                        "indice_final"
                    ]
                )
                > float(
                    linha_cdi[
                        "indice_final"
                    ]
                )
                else (
                    "O modelo oficial não superou "
                    "uma carteira de 100% CDI."
                )
            ),
            "valor": (
                float(
                    linha_oficial[
                        "indice_final"
                    ]
                )
                - float(
                    linha_cdi[
                        "indice_final"
                    ]
                )
            ),
            "unidade": "pontos de índice",
        },
        {
            "tema": "Consistência anual",
            "conclusao": (
                f"O modelo oficial superou o benchmark "
                f"em {quantidade_anos_superou_benchmark} "
                f"de {quantidade_anos_avaliados} períodos anuais."
            ),
            "valor": (
                quantidade_anos_superou_benchmark
            ),
            "unidade": (
                f"de {quantidade_anos_avaliados} períodos"
            ),
        },
        {
            "tema": "Perfil do modelo oficial",
            "conclusao": (
                "O modelo oficial foi mantido como "
                "versão defensiva, priorizando controle "
                "de risco e estabilidade."
            ),
            "valor": float(
                linha_oficial[
                    "maximo_drawdown"
                ]
            ),
            "unidade": "drawdown máximo",
        },
    ]
)


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

comparacao.to_csv(
    ARQUIVO_COMPARACAO,
    index=False,
    encoding="utf-8-sig",
)


comparacao_formatada.to_csv(
    ARQUIVO_COMPARACAO_FORMATADA,
    index=False,
    encoding="utf-8-sig",
)


resultados_anuais.to_csv(
    ARQUIVO_RESULTADOS_ANUAIS,
    index=False,
    encoding="utf-8-sig",
)


resultados_anuais_formatados.to_csv(
    ARQUIVO_RESULTADOS_ANUAIS_FORMATADOS,
    index=False,
    encoding="utf-8-sig",
)


comparacao_mensal.to_csv(
    ARQUIVO_COMPARACAO_MENSAL,
    index=False,
    encoding="utf-8-sig",
)


posicoes_metricas.to_csv(
    ARQUIVO_POSICOES_METRICAS,
    index=False,
    encoding="utf-8-sig",
)


conclusoes.to_csv(
    ARQUIVO_CONCLUSOES,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO 1 — DESEMPENHO ACUMULADO
# ============================================================

data_inicial_grafico = (
    series_finais[
        "data"
    ].iloc[0]
    - pd.offsets.MonthEnd(1)
)


fig, ax = plt.subplots(
    figsize=(13, 7)
)


for cenario in [
    CENARIO_OFICIAL,
    CENARIO_MODELO_FIXO,
    CENARIO_CHALLENGER,
    CENARIO_BENCHMARK,
    CENARIO_CDI,
]:

    datas_grafico = pd.concat(
        [
            pd.Series(
                [
                    data_inicial_grafico
                ]
            ),
            series_finais[
                "data"
            ],
        ],
        ignore_index=True,
    )

    indices_grafico = pd.concat(
        [
            pd.Series(
                [
                    VALOR_INICIAL
                ]
            ),
            series_finais[
                f"indice_recalculado_{cenario}"
            ],
        ],
        ignore_index=True,
    )

    ax.plot(
        datas_grafico,
        indices_grafico,
        linewidth=2,
        label=ROTULOS[
            cenario
        ],
    )


ax.axhline(
    y=VALOR_INICIAL,
    linewidth=1,
)


ax.set_title(
    "Desempenho Acumulado no Período de Avaliação"
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
# GRÁFICO 2 — RETORNOS ANUAIS
# ============================================================

retornos_anuais_grafico = (
    resultados_anuais.loc[
        resultados_anuais[
            "cenario"
        ]
        .isin(
            [
                CENARIO_OFICIAL,
                CENARIO_CHALLENGER,
                CENARIO_BENCHMARK,
                CENARIO_CDI,
            ]
        )
    ]
    .pivot(
        index="periodo",
        columns="modelo",
        values="retorno_liquido",
    )
)


fig, ax = plt.subplots(
    figsize=(13, 7)
)


retornos_anuais_grafico.plot(
    kind="bar",
    ax=ax,
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
    "Retornos por Ano do Período de Avaliação"
)

ax.set_xlabel(
    "Período"
)

ax.set_ylabel(
    "Retorno líquido"
)

ax.tick_params(
    axis="x",
    rotation=0,
)

ax.legend(
    title="Modelo",
)


ax.grid(
    axis="y",
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_ANUAL,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — RISCO E RETORNO
# ============================================================

fig, ax = plt.subplots(
    figsize=(11, 7)
)


ax.scatter(
    comparacao[
        "volatilidade_anualizada"
    ],
    comparacao[
        "retorno_anualizado"
    ],
    s=100,
)


for _, linha in comparacao.iterrows():

    ax.annotate(
        linha[
            "modelo"
        ],
        (
            linha[
                "volatilidade_anualizada"
            ],
            linha[
                "retorno_anualizado"
            ],
        ),
        xytext=(
            7,
            7,
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
    "Relação entre Risco e Retorno"
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
# GRÁFICO 4 — DRAWDOWN
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


for cenario in [
    CENARIO_OFICIAL,
    CENARIO_CHALLENGER,
    CENARIO_BENCHMARK,
]:

    datas_grafico = pd.concat(
        [
            pd.Series(
                [
                    data_inicial_grafico
                ]
            ),
            series_finais[
                "data"
            ],
        ],
        ignore_index=True,
    )

    drawdowns_grafico = pd.concat(
        [
            pd.Series(
                [
                    0.0
                ]
            ),
            series_finais[
                f"drawdown_recalculado_{cenario}"
            ],
        ],
        ignore_index=True,
    )

    ax.plot(
        datas_grafico,
        drawdowns_grafico,
        linewidth=2,
        label=ROTULOS[
            cenario
        ],
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
    "Drawdown Comparativo"
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
# VALIDAÇÕES
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
    nome="Validações da Etapa 1",
    aprovado=True,
    detalhe=(
        f"{len(validacoes_celula_1)} validações aprovadas"
    ),
)


adicionar_validacao(
    nome="Quantidade de cenários",
    aprovado=(
        comparacao[
            "cenario"
        ].nunique()
        == len(
            CENARIOS
        )
    ),
    detalhe=(
        f"{comparacao['cenario'].nunique()} cenários"
    ),
)


adicionar_validacao(
    nome="Quantidade de meses",
    aprovado=(
        len(series_finais) > 0
    ),
    detalhe=(
        f"{len(series_finais)} meses"
    ),
)


adicionar_validacao(
    nome="Retornos sem nulos",
    aprovado=(
        not series_finais[
            list(
                COLUNAS_RETORNOS.values()
            )
        ]
        .isna()
        .any()
        .any()
    ),
    detalhe=(
        f"{int(series_finais[list(COLUNAS_RETORNOS.values())].isna().sum().sum())} "
        "nulos"
    ),
)


indices_consistentes = True
maior_diferenca_indice = 0.0


for cenario in CENARIOS:

    indice_recalculado = float(
        series_finais[
            f"indice_recalculado_{cenario}"
        ].iloc[-1]
    )

    indice_salvo = float(
        comparacao.loc[
            comparacao[
                "cenario"
            ]
            .eq(
                cenario
            ),
            "indice_final",
        ].iloc[0]
    )

    diferenca = abs(
        indice_recalculado
        - indice_salvo
    )

    maior_diferenca_indice = max(
        maior_diferenca_indice,
        diferenca,
    )

    if not np.isclose(
        indice_recalculado,
        indice_salvo,
        atol=1e-10,
        rtol=1e-10,
    ):

        indices_consistentes = False


adicionar_validacao(
    nome="Consistência dos índices",
    aprovado=(
        indices_consistentes
    ),
    detalhe=(
        f"Maior diferença: "
        f"{maior_diferenca_indice:.12f}"
    ),
)


adicionar_validacao(
    nome="Modelo oficial acima do benchmark",
    aprovado=(
        float(
            linha_oficial[
                "indice_final"
            ]
        )
        > float(
            linha_benchmark[
                "indice_final"
            ]
        )
    ),
    detalhe=(
        f"Vantagem: "
        f"{float(linha_oficial['indice_final']) - float(linha_benchmark['indice_final']):.4f}"
    ),
)


adicionar_validacao(
    nome="Resultados anuais completos",
    aprovado=(
        resultados_anuais["ano"].nunique() > 0
    ),
    detalhe=(
        f"{resultados_anuais['ano'].nunique()} períodos anuais"
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


if (
    tabela_validacoes[
        "status"
    ]
    .eq(
        "REPROVADO"
    )
    .any()
):

    raise ValueError(
        "Uma ou mais validações da Etapa 2 "
        "foram reprovadas:\n\n"
        f"{tabela_validacoes}"
    )


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

ARQUIVOS_ESPERADOS = [
    ARQUIVO_COMPARACAO,
    ARQUIVO_COMPARACAO_FORMATADA,
    ARQUIVO_RESULTADOS_ANUAIS,
    ARQUIVO_RESULTADOS_ANUAIS_FORMATADOS,
    ARQUIVO_COMPARACAO_MENSAL,
    ARQUIVO_POSICOES_METRICAS,
    ARQUIVO_CONCLUSOES,
    ARQUIVO_VALIDACOES,
    ARQUIVO_GRAFICO_DESEMPENHO,
    ARQUIVO_GRAFICO_ANUAL,
    ARQUIVO_GRAFICO_RISCO_RETORNO,
    ARQUIVO_GRAFICO_DRAWDOWN,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in ARQUIVOS_ESPERADOS
    if not arquivo.exists()
]


if arquivos_nao_salvos:

    raise FileNotFoundError(
        "Alguns arquivos da Etapa 2 "
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
print("ETAPA 2 — COMPARAÇÃO DE DESEMPENHO E RISCO CONCLUÍDA")
print("=" * 70)


print(
    f"\nPeríodo de avaliação: "
    f"{series_finais['data'].min():%d/%m/%Y} "
    f"a "
    f"{series_finais['data'].max():%d/%m/%Y}"
)


print(
    f"Quantidade de meses: "
    f"{len(series_finais)}"
)


print(
    "\nÍndices finais:"
)


for cenario in CENARIOS:

    indice = float(
        comparacao.loc[
            comparacao[
                "cenario"
            ]
            .eq(
                cenario
            ),
            "indice_final",
        ].iloc[0]
    )

    print(
        f"- {ROTULOS[cenario]}: "
        f"{indice:.2f}"
    )


print(
    "\nModelo oficial:"
)


print(
    f"- Retorno anualizado: "
    f"{float(linha_oficial['retorno_anualizado']):.2%}"
)


print(
    f"- Volatilidade anualizada: "
    f"{float(linha_oficial['volatilidade_anualizada']):.2%}"
)


print(
    f"- Retorno/volatilidade: "
    f"{float(linha_oficial['retorno_volatilidade']):.2f}"
)


print(
    f"- Sharpe de excesso ao CDI: "
    f"{float(linha_oficial['sharpe_excesso_cdi']):.2f}"
)


print(
    f"- Máximo drawdown: "
    f"{float(linha_oficial['maximo_drawdown']):.2%}"
)


print(
    f"\nDiferença contra o benchmark: "
    f"{float(linha_oficial['indice_final']) - float(linha_benchmark['indice_final']):.2f} "
    "ponto"
)


print(
    f"Diferença contra o challenger: "
    f"{float(linha_oficial['indice_final']) - float(linha_challenger['indice_final']):.2f} "
    "pontos"
)


print(
    f"\nPeríodos anuais acima do benchmark: "
    f"{quantidade_anos_superou_benchmark}/"
    f"{quantidade_anos_avaliados}"
)


print(
    "\nComparação dos modelos:"
)


display(
    comparacao_formatada
)


print(
    "\nResultados anuais:"
)


display(
    resultados_anuais_formatados
)


print(
    "\nPosições independentes por métrica:"
)


display(
    posicoes_metricas
)


print(
    "\nConclusões comparativas:"
)


display(
    conclusoes
)


print(
    "\nValidações:"
)


display(
    tabela_validacoes
)

# ###########################################################################
# ETAPA 03 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# ETAPA 3 — ANÁLISE POR REGIME E CONTRIBUIÇÃO DOS ATIVOS
# SCRIPT 07 — ANÁLISE DOS RESULTADOS FINAIS
# VERSÃO AUTÔNOMA
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PERIODOS_POR_ANO = 12
MINIMO_MESES_AMOSTRA = 6

CENARIO_OFICIAL = CENARIO_OFICIAL_JSON
CENARIO_CHALLENGER = CENARIO_CHALLENGER_JSON
CENARIO_BENCHMARK = "BENCHMARK_5_ATIVOS"

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
        / "outputs"
        / "tabelas"
        / "07_02_validacoes.csv"
    )

    if arquivo_teste.exists():

        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:

    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo outputs/tabelas/"
        "07_02_validacoes.csv não foi encontrado."
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

ARQUIVO_VALIDACOES_CELULA_2 = (
    PASTA_TABELAS
    / "07_02_validacoes.csv"
)

ARQUIVO_SERIES_FINAIS = (
    PASTA_TABELAS
    / "06_12_series_modelos_finais.csv"
)

ARQUIVO_MODELO_OFICIAL = (
    RAIZ_PROJETO
    / "outputs"
    / "modelo_final"
    / "modelo_oficial.json"
)


ARQUIVOS_ENTRADA = [
    ARQUIVO_VALIDACOES_CELULA_2,
    ARQUIVO_SERIES_FINAIS,
    ARQUIVO_MODELO_OFICIAL,
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
            str(arquivo)
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_REGIMES_MENSAIS = (
    PASTA_TABELAS
    / "07_03_regimes_mensais_aplicados.csv"
)

ARQUIVO_DESEMPENHO_REGIMES = (
    PASTA_TABELAS
    / "07_03_desempenho_por_regime.csv"
)

ARQUIVO_DESEMPENHO_REGIMES_FORMATADO = (
    PASTA_TABELAS
    / "07_03_desempenho_por_regime_formatado.csv"
)

ARQUIVO_PESOS_MEDIOS = (
    PASTA_TABELAS
    / "07_03_pesos_medios_por_regime.csv"
)

ARQUIVO_CONTRIBUICAO_MENSAL = (
    PASTA_TABELAS
    / "07_03_contribuicao_mensal_ativos.csv"
)

ARQUIVO_CONTRIBUICAO_REGIMES = (
    PASTA_TABELAS
    / "07_03_contribuicao_ativos_por_regime.csv"
)

ARQUIVO_CONTRIBUICAO_TOTAL = (
    PASTA_TABELAS
    / "07_03_contribuicao_total_ativos.csv"
)

ARQUIVO_CONCLUSOES = (
    PASTA_TABELAS
    / "07_03_conclusoes_por_regime.csv"
)

ARQUIVO_VALIDACOES = (
    PASTA_TABELAS
    / "07_03_validacoes.csv"
)

ARQUIVO_GRAFICO_FREQUENCIA = (
    PASTA_GRAFICOS
    / "07_03_frequencia_regimes.png"
)

ARQUIVO_GRAFICO_RETORNOS = (
    PASTA_GRAFICOS
    / "07_03_retorno_por_regime.png"
)

ARQUIVO_GRAFICO_CONTRIBUICAO = (
    PASTA_GRAFICOS
    / "07_03_contribuicao_ativos_por_regime.png"
)

ARQUIVO_GRAFICO_PESOS = (
    PASTA_GRAFICOS
    / "07_03_pesos_medios_por_regime.png"
)


# ============================================================
# CARREGAMENTO
# ============================================================

validacoes_celula_2 = pd.read_csv(
    ARQUIVO_VALIDACOES_CELULA_2,
    encoding="utf-8-sig",
)

series_finais = pd.read_csv(
    ARQUIVO_SERIES_FINAIS,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DA ETAPA ANTERIOR
# ============================================================

if not {
    "validacao",
    "status",
    "detalhe",
}.issubset(
    validacoes_celula_2.columns
):

    raise ValueError(
        "O arquivo de validações da Etapa 2 "
        "possui estrutura inválida."
    )


if (
    validacoes_celula_2[
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
        "A Etapa 2 possui validações reprovadas."
    )


# ============================================================
# PADRONIZAÇÃO DAS DATAS
# ============================================================

if "data" not in series_finais.columns:

    raise ValueError(
        "A série final não possui a coluna data."
    )


series_finais["data"] = pd.to_datetime(
    series_finais["data"],
    errors="coerce",
)


if series_finais["data"].isna().any():

    raise ValueError(
        "A série final possui datas inválidas."
    )


if series_finais["data"].duplicated().any():

    raise ValueError(
        "A série final possui datas duplicadas."
    )


series_finais.sort_values(
    "data",
    inplace=True,
)

series_finais.reset_index(
    drop=True,
    inplace=True,
)


# ============================================================
# IDENTIFICAÇÃO DOS ATIVOS OFICIAIS
# ============================================================

ATIVOS = list(
    ATIVOS_OFICIAIS
)


if not ATIVOS:

    raise ValueError(
        "O JSON do modelo oficial não possui ativos."
    )


ativos_sem_retorno = [
    ativo
    for ativo in ATIVOS
    if ativo not in series_finais.columns
]


if ativos_sem_retorno:

    raise ValueError(
        "Ativos oficiais sem coluna de retorno:\n"
        f"{ativos_sem_retorno}"
    )


# ============================================================
# IDENTIFICAÇÃO DO REGIME APLICADO
# ============================================================

USA_CONFIRMACAO_DINAMICA = (
    CENARIO_OFICIAL_JSON
    == "WALK_FORWARD"
)


if USA_CONFIRMACAO_DINAMICA:

    if "meses_confirmacao_aplicada" not in series_finais.columns:

        raise ValueError(
            "A série final não possui a coluna "
            "meses_confirmacao_aplicada."
        )


    series_finais[
        "meses_confirmacao_oficial"
    ] = pd.to_numeric(
        series_finais[
            "meses_confirmacao_aplicada"
        ],
        errors="coerce",
    )

else:

    series_finais[
        "meses_confirmacao_oficial"
    ] = int(
        CONFIRMACAO_ATUAL
    )


if series_finais[
    "meses_confirmacao_oficial"
].isna().any():

    raise ValueError(
        "Existem confirmações oficiais inválidas."
    )


series_finais[
    "meses_confirmacao_oficial"
] = (
    series_finais[
        "meses_confirmacao_oficial"
    ]
    .astype(int)
)


colunas_regimes_necessarias = [
    (
        f"regime_confirmacao_"
        f"{meses}m"
    )
    for meses in (
        series_finais[
            "meses_confirmacao_oficial"
        ]
        .unique()
        .tolist()
    )
]


colunas_regimes_ausentes = [
    coluna
    for coluna in colunas_regimes_necessarias
    if coluna not in series_finais.columns
]


if colunas_regimes_ausentes:

    raise ValueError(
        "Colunas de regime oficiais ausentes:\n"
        f"{colunas_regimes_ausentes}"
    )


def obter_regime_aplicado(
    linha,
):

    meses = int(
        linha[
            "meses_confirmacao_oficial"
        ]
    )

    coluna = (
        f"regime_confirmacao_{meses}m"
    )

    return str(
        linha[
            coluna
        ]
    ).strip()


series_finais[
    "regime_aplicado"
] = series_finais.apply(
    obter_regime_aplicado,
    axis=1,
)


regimes_invalidos = (
    series_finais.loc[
        ~series_finais[
            "regime_aplicado"
        ]
        .isin(
            ORDEM_REGIMES
        ),
        "regime_aplicado",
    ]
    .unique()
    .tolist()
)


if regimes_invalidos:

    raise ValueError(
        "Foram encontrados regimes inválidos:\n"
        f"{regimes_invalidos}"
    )


series_finais[
    "nome_regime"
] = series_finais[
    "regime_aplicado"
].map(
    NOMES_REGIMES
)


series_finais[
    "ano"
] = series_finais[
    "data"
].dt.year


# ============================================================
# PESOS HISTÓRICOS DO MODELO OFICIAL
# ============================================================

PESOS_OFICIAIS_JSON = (
    modelo_json[
        "configuracao_atual"
    ][
        "pesos_por_regime"
    ]
)


regimes_sem_pesos = [
    regime
    for regime in ORDEM_REGIMES
    if regime not in PESOS_OFICIAIS_JSON
]


if regimes_sem_pesos:

    raise ValueError(
        "Regimes sem pesos no JSON oficial:\n"
        f"{regimes_sem_pesos}"
    )


for regime in ORDEM_REGIMES:

    ativos_ausentes_regime = [
        ativo
        for ativo in ATIVOS
        if ativo
        not in PESOS_OFICIAIS_JSON[
            regime
        ]
    ]

    if ativos_ausentes_regime:

        raise ValueError(
            f"Ativos sem peso no regime {regime}:\n"
            f"{ativos_ausentes_regime}"
        )


for ativo in ATIVOS:

    coluna_oficial = (
        f"peso_oficial_{ativo}"
    )

    if (
        CENARIO_OFICIAL_JSON
        == "WALK_FORWARD"
    ):

        coluna_origem = (
            f"peso_oficial_{ativo}"
        )

        if coluna_origem not in series_finais.columns:

            raise ValueError(
                "Coluna de peso walk-forward ausente: "
                f"{coluna_origem}"
            )

        series_finais[
            coluna_oficial
        ] = pd.to_numeric(
            series_finais[
                coluna_origem
            ],
            errors="coerce",
        )

    else:

        mapa_pesos = {
            regime: float(
                PESOS_OFICIAIS_JSON[
                    regime
                ][
                    ativo
                ]
            )
            for regime in ORDEM_REGIMES
        }

        series_finais[
            coluna_oficial
        ] = (
            series_finais[
                "regime_aplicado"
            ]
            .map(
                mapa_pesos
            )
        )


COLUNAS_PESOS = [
    f"peso_oficial_{ativo}"
    for ativo in ATIVOS
]


if series_finais[
    COLUNAS_PESOS
].isna().any().any():

    nulos_pesos = (
        series_finais[
            COLUNAS_PESOS
        ]
        .isna()
        .sum()
    )

    nulos_pesos = nulos_pesos.loc[
        nulos_pesos > 0
    ]

    raise ValueError(
        "Existem pesos oficiais mensais inválidos:\n"
        f"{nulos_pesos}"
    )


soma_pesos_oficiais = (
    series_finais[
        COLUNAS_PESOS
    ]
    .sum(
        axis=1
    )
)


if not np.allclose(
    soma_pesos_oficiais,
    1.0,
    atol=1e-10,
    rtol=1e-10,
):

    raise ValueError(
        "Os pesos oficiais mensais não somam 100%. "
        f"Maior diferença: "
        f"{float((soma_pesos_oficiais - 1.0).abs().max()):.12f}"
    )


# ============================================================
# COLUNAS DOS CENÁRIOS
# ============================================================

COLUNA_RETORNO_OFICIAL = (
    f"retorno_liquido_{CENARIO_OFICIAL}"
)

COLUNA_RETORNO_CHALLENGER = (
    f"retorno_liquido_{CENARIO_CHALLENGER}"
)

COLUNA_RETORNO_BENCHMARK = (
    f"retorno_liquido_{CENARIO_BENCHMARK}"
)

COLUNA_RETORNO_BRUTO_OFICIAL = (
    f"retorno_bruto_{CENARIO_OFICIAL}"
)

COLUNA_CUSTO_OFICIAL = (
    f"custo_{CENARIO_OFICIAL}"
)


COLUNAS_CENARIOS_NECESSARIAS = [
    COLUNA_RETORNO_OFICIAL,
    COLUNA_RETORNO_CHALLENGER,
    COLUNA_RETORNO_BENCHMARK,
    COLUNA_RETORNO_BRUTO_OFICIAL,
    COLUNA_CUSTO_OFICIAL,
]


colunas_cenarios_ausentes = [
    coluna
    for coluna in COLUNAS_CENARIOS_NECESSARIAS
    if coluna not in series_finais.columns
]


if colunas_cenarios_ausentes:

    raise ValueError(
        "Colunas dos cenários ausentes:\n"
        f"{colunas_cenarios_ausentes}"
    )


# ============================================================
# CONVERSÃO DAS COLUNAS NUMÉRICAS
# ============================================================

COLUNAS_NUMERICAS = [
    *ATIVOS,
    *COLUNAS_PESOS,
    *COLUNAS_CENARIOS_NECESSARIAS,
]


for coluna in COLUNAS_NUMERICAS:

    series_finais[coluna] = pd.to_numeric(
        series_finais[coluna],
        errors="coerce",
    )


if series_finais[
    COLUNAS_NUMERICAS
].isna().any().any():

    nulos = (
        series_finais[
            COLUNAS_NUMERICAS
        ]
        .isna()
        .sum()
    )

    nulos = nulos.loc[
        nulos > 0
    ]

    raise ValueError(
        "Existem valores numéricos inválidos:\n"
        f"{nulos}"
    )


# ============================================================
# FUNÇÕES AUXILIARES
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


# ============================================================
# CONTRIBUIÇÃO MENSAL DOS ATIVOS
# ============================================================

contribuicao_mensal = series_finais[
    [
        "data",
        "ano",
        "regime_aplicado",
        "nome_regime",
    ]
].copy()


for ativo in ATIVOS:

    coluna_peso = (
        f"peso_oficial_{ativo}"
    )

    coluna_contribuicao = (
        f"contribuicao_bruta_{ativo}"
    )

    contribuicao_mensal[
        f"retorno_{ativo}"
    ] = series_finais[
        ativo
    ]

    contribuicao_mensal[
        f"peso_{ativo}"
    ] = series_finais[
        coluna_peso
    ]

    contribuicao_mensal[
        coluna_contribuicao
    ] = (
        series_finais[
            coluna_peso
        ]
        * series_finais[
            ativo
        ]
    )


COLUNAS_CONTRIBUICAO = [
    f"contribuicao_bruta_{ativo}"
    for ativo in ATIVOS
]


contribuicao_mensal[
    "soma_contribuicoes_brutas"
] = (
    contribuicao_mensal[
        COLUNAS_CONTRIBUICAO
    ]
    .sum(
        axis=1
    )
)


contribuicao_mensal[
    "retorno_bruto_modelo"
] = series_finais[
    COLUNA_RETORNO_BRUTO_OFICIAL
]


contribuicao_mensal[
    "custo_modelo"
] = series_finais[
    COLUNA_CUSTO_OFICIAL
]


contribuicao_mensal[
    "retorno_liquido_modelo"
] = series_finais[
    COLUNA_RETORNO_OFICIAL
]


contribuicao_mensal[
    "diferenca_contribuicao_vs_retorno_bruto"
] = (
    contribuicao_mensal[
        "soma_contribuicoes_brutas"
    ]
    - contribuicao_mensal[
        "retorno_bruto_modelo"
    ]
)


# ============================================================
# DESEMPENHO POR REGIME
# ============================================================

registros_desempenho = []


for regime in ORDEM_REGIMES:

    dados_regime = (
        series_finais.loc[
            series_finais[
                "regime_aplicado"
            ]
            .eq(
                regime
            )
        ]
        .copy()
    )

    quantidade_meses = len(
        dados_regime
    )

    if quantidade_meses == 0:

        registros_desempenho.append(
            {
                "regime": regime,
                "nome_regime": (
                    NOMES_REGIMES[
                        regime
                    ]
                ),
                "quantidade_meses": 0,
                "proporcao_periodo": 0.0,
                "amostra_reduzida": True,
                "retorno_total_oficial": np.nan,
                "retorno_total_challenger": np.nan,
                "retorno_total_benchmark": np.nan,
                "excesso_oficial_vs_benchmark": np.nan,
                "excesso_oficial_vs_challenger": np.nan,
                "retorno_medio_mensal_oficial": np.nan,
                "volatilidade_anualizada_oficial": np.nan,
                "retorno_volatilidade_oficial": np.nan,
                "meses_positivos_oficial": np.nan,
                "melhor_mes_oficial": np.nan,
                "pior_mes_oficial": np.nan,
                "custo_total_simples": np.nan,
            }
        )

        continue

    retornos_oficial = dados_regime[
        COLUNA_RETORNO_OFICIAL
    ]

    retornos_challenger = dados_regime[
        COLUNA_RETORNO_CHALLENGER
    ]

    retornos_benchmark = dados_regime[
        COLUNA_RETORNO_BENCHMARK
    ]

    retorno_total_oficial = (
        calcular_retorno_total(
            retornos_oficial
        )
    )

    retorno_total_challenger = (
        calcular_retorno_total(
            retornos_challenger
        )
    )

    retorno_total_benchmark = (
        calcular_retorno_total(
            retornos_benchmark
        )
    )

    volatilidade = (
        calcular_volatilidade_anualizada(
            retornos_oficial
        )
    )

    retorno_anualizado = (
        calcular_retorno_anualizado(
            retornos_oficial
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

    registros_desempenho.append(
        {
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
                    series_finais
                )
            ),
            "amostra_reduzida": (
                quantidade_meses
                < MINIMO_MESES_AMOSTRA
            ),
            "retorno_total_oficial": (
                retorno_total_oficial
            ),
            "retorno_total_challenger": (
                retorno_total_challenger
            ),
            "retorno_total_benchmark": (
                retorno_total_benchmark
            ),
            "excesso_oficial_vs_benchmark": (
                retorno_total_oficial
                - retorno_total_benchmark
            ),
            "excesso_oficial_vs_challenger": (
                retorno_total_oficial
                - retorno_total_challenger
            ),
            "retorno_medio_mensal_oficial": float(
                retornos_oficial.mean()
            ),
            "volatilidade_anualizada_oficial": (
                volatilidade
            ),
            "retorno_volatilidade_oficial": (
                retorno_volatilidade
            ),
            "meses_positivos_oficial": float(
                retornos_oficial.gt(
                    0
                ).mean()
            ),
            "melhor_mes_oficial": float(
                retornos_oficial.max()
            ),
            "pior_mes_oficial": float(
                retornos_oficial.min()
            ),
            "custo_total_simples": float(
                dados_regime[
                    COLUNA_CUSTO_OFICIAL
                ].sum()
            ),
        }
    )


desempenho_regimes = pd.DataFrame(
    registros_desempenho
)


desempenho_regimes[
    "regime"
] = pd.Categorical(
    desempenho_regimes[
        "regime"
    ],
    categories=ORDEM_REGIMES,
    ordered=True,
)


desempenho_regimes.sort_values(
    "regime",
    inplace=True,
)

desempenho_regimes.reset_index(
    drop=True,
    inplace=True,
)


# ============================================================
# PESOS MÉDIOS POR REGIME
# ============================================================

registros_pesos = []


for regime in ORDEM_REGIMES:

    dados_regime = (
        series_finais.loc[
            series_finais[
                "regime_aplicado"
            ]
            .eq(
                regime
            )
        ]
    )

    if dados_regime.empty:

        continue

    registro = {
        "regime": regime,
        "nome_regime": (
            NOMES_REGIMES[
                regime
            ]
        ),
        "quantidade_meses": len(
            dados_regime
        ),
    }

    for ativo in ATIVOS:

        registro[
            f"peso_medio_{ativo}"
        ] = float(
            dados_regime[
                f"peso_oficial_{ativo}"
            ].mean()
        )

        registro[
            f"peso_minimo_{ativo}"
        ] = float(
            dados_regime[
                f"peso_oficial_{ativo}"
            ].min()
        )

        registro[
            f"peso_maximo_{ativo}"
        ] = float(
            dados_regime[
                f"peso_oficial_{ativo}"
            ].max()
        )

    registro[
        "soma_pesos_medios"
    ] = sum(
        registro[
            f"peso_medio_{ativo}"
        ]
        for ativo in ATIVOS
    )

    registros_pesos.append(
        registro
    )


pesos_medios = pd.DataFrame(
    registros_pesos
)


pesos_medios[
    "regime"
] = pd.Categorical(
    pesos_medios[
        "regime"
    ],
    categories=ORDEM_REGIMES,
    ordered=True,
)


pesos_medios.sort_values(
    "regime",
    inplace=True,
)

pesos_medios.reset_index(
    drop=True,
    inplace=True,
)


# ============================================================
# CONTRIBUIÇÃO DOS ATIVOS POR REGIME
# ============================================================

registros_contribuicao_regime = []


for regime in ORDEM_REGIMES:

    dados_regime = (
        contribuicao_mensal.loc[
            contribuicao_mensal[
                "regime_aplicado"
            ]
            .eq(
                regime
            )
        ]
    )

    if dados_regime.empty:

        continue

    for ativo in ATIVOS:

        contribuicoes = dados_regime[
            f"contribuicao_bruta_{ativo}"
        ]

        registros_contribuicao_regime.append(
            {
                "regime": regime,
                "nome_regime": (
                    NOMES_REGIMES[
                        regime
                    ]
                ),
                "ativo": ativo,
                "quantidade_meses": len(
                    dados_regime
                ),
                "contribuicao_bruta_simples": float(
                    contribuicoes.sum()
                ),
                "contribuicao_media_mensal": float(
                    contribuicoes.mean()
                ),
                "melhor_contribuicao_mensal": float(
                    contribuicoes.max()
                ),
                "pior_contribuicao_mensal": float(
                    contribuicoes.min()
                ),
                "meses_contribuicao_positiva": float(
                    contribuicoes.gt(
                        0
                    ).mean()
                ),
            }
        )


contribuicao_regimes = pd.DataFrame(
    registros_contribuicao_regime
)


registros_contribuicao_total = []


for ativo in ATIVOS:

    contribuicoes = contribuicao_mensal[
        f"contribuicao_bruta_{ativo}"
    ]

    registros_contribuicao_total.append(
        {
            "ativo": ativo,
            "contribuicao_bruta_simples": float(
                contribuicoes.sum()
            ),
            "contribuicao_media_mensal": float(
                contribuicoes.mean()
            ),
            "melhor_contribuicao_mensal": float(
                contribuicoes.max()
            ),
            "pior_contribuicao_mensal": float(
                contribuicoes.min()
            ),
            "meses_contribuicao_positiva": float(
                contribuicoes.gt(
                    0
                ).mean()
            ),
        }
    )


contribuicao_total = pd.DataFrame(
    registros_contribuicao_total
)


contribuicao_total.sort_values(
    "contribuicao_bruta_simples",
    ascending=False,
    inplace=True,
)

contribuicao_total.reset_index(
    drop=True,
    inplace=True,
)


# ============================================================
# REGIMES MENSAIS APLICADOS
# ============================================================

colunas_regimes_mensais = [
    "data",
    "ano",
    "regime_aplicado",
    "nome_regime",
    "meses_confirmacao_aplicada",
]


for coluna in [
    "numero_recalibracao",
    "candidato_aplicado",
    "data_final_treino_utilizada",
]:

    if coluna in series_finais.columns:

        colunas_regimes_mensais.append(
            coluna
        )


regimes_mensais = series_finais[
    colunas_regimes_mensais
].copy()


# ============================================================
# TABELA FORMATADA
# ============================================================

desempenho_regimes_formatado = (
    desempenho_regimes
    .copy()
    .astype(object)
)


COLUNAS_PERCENTUAIS = [
    "proporcao_periodo",
    "retorno_total_oficial",
    "retorno_total_challenger",
    "retorno_total_benchmark",
    "excesso_oficial_vs_benchmark",
    "excesso_oficial_vs_challenger",
    "retorno_medio_mensal_oficial",
    "volatilidade_anualizada_oficial",
    "meses_positivos_oficial",
    "melhor_mes_oficial",
    "pior_mes_oficial",
    "custo_total_simples",
]


for coluna in COLUNAS_PERCENTUAIS:

    desempenho_regimes_formatado[
        coluna
    ] = desempenho_regimes[
        coluna
    ].map(
        lambda valor: (
            f"{valor:.2%}"
            if pd.notna(
                valor
            )
            else "-"
        )
    )


desempenho_regimes_formatado[
    "retorno_volatilidade_oficial"
] = desempenho_regimes[
    "retorno_volatilidade_oficial"
].map(
    lambda valor: (
        f"{valor:.2f}"
        if pd.notna(
            valor
        )
        else "-"
    )
)


# ============================================================
# CONCLUSÕES
# ============================================================

regimes_com_dados = (
    desempenho_regimes.loc[
        desempenho_regimes[
            "quantidade_meses"
        ]
        > 0
    ]
    .copy()
)


melhor_regime_retorno = (
    regimes_com_dados.loc[
        regimes_com_dados[
            "retorno_total_oficial"
        ].idxmax()
    ]
)


pior_regime_retorno = (
    regimes_com_dados.loc[
        regimes_com_dados[
            "retorno_total_oficial"
        ].idxmin()
    ]
)


melhor_regime_excesso = (
    regimes_com_dados.loc[
        regimes_com_dados[
            "excesso_oficial_vs_benchmark"
        ].idxmax()
    ]
)


pior_regime_excesso = (
    regimes_com_dados.loc[
        regimes_com_dados[
            "excesso_oficial_vs_benchmark"
        ].idxmin()
    ]
)


regime_mais_frequente = (
    regimes_com_dados.loc[
        regimes_com_dados[
            "quantidade_meses"
        ].idxmax()
    ]
)


ativo_maior_contribuicao = (
    contribuicao_total.iloc[0]
)


ativo_menor_contribuicao = (
    contribuicao_total.iloc[-1]
)


conclusoes = pd.DataFrame(
    [
        {
            "tema": "Regime mais frequente",
            "conclusao": (
                regime_mais_frequente[
                    "nome_regime"
                ]
            ),
            "valor": int(
                regime_mais_frequente[
                    "quantidade_meses"
                ]
            ),
            "unidade": "meses",
            "cautela_amostral": (
                "NÃO"
                if int(
                    regime_mais_frequente[
                        "quantidade_meses"
                    ]
                )
                >= MINIMO_MESES_AMOSTRA
                else "SIM"
            ),
        },
        {
            "tema": "Melhor retorno do modelo",
            "conclusao": (
                melhor_regime_retorno[
                    "nome_regime"
                ]
            ),
            "valor": float(
                melhor_regime_retorno[
                    "retorno_total_oficial"
                ]
            ),
            "unidade": "retorno acumulado no regime",
            "cautela_amostral": (
                "SIM"
                if bool(
                    melhor_regime_retorno[
                        "amostra_reduzida"
                    ]
                )
                else "NÃO"
            ),
        },
        {
            "tema": "Pior retorno do modelo",
            "conclusao": (
                pior_regime_retorno[
                    "nome_regime"
                ]
            ),
            "valor": float(
                pior_regime_retorno[
                    "retorno_total_oficial"
                ]
            ),
            "unidade": "retorno acumulado no regime",
            "cautela_amostral": (
                "SIM"
                if bool(
                    pior_regime_retorno[
                        "amostra_reduzida"
                    ]
                )
                else "NÃO"
            ),
        },
        {
            "tema": "Maior excesso contra benchmark",
            "conclusao": (
                melhor_regime_excesso[
                    "nome_regime"
                ]
            ),
            "valor": float(
                melhor_regime_excesso[
                    "excesso_oficial_vs_benchmark"
                ]
            ),
            "unidade": "diferença de retorno",
            "cautela_amostral": (
                "SIM"
                if bool(
                    melhor_regime_excesso[
                        "amostra_reduzida"
                    ]
                )
                else "NÃO"
            ),
        },
        {
            "tema": "Menor excesso contra benchmark",
            "conclusao": (
                pior_regime_excesso[
                    "nome_regime"
                ]
            ),
            "valor": float(
                pior_regime_excesso[
                    "excesso_oficial_vs_benchmark"
                ]
            ),
            "unidade": "diferença de retorno",
            "cautela_amostral": (
                "SIM"
                if bool(
                    pior_regime_excesso[
                        "amostra_reduzida"
                    ]
                )
                else "NÃO"
            ),
        },
        {
            "tema": "Maior contribuição bruta simples",
            "conclusao": (
                ativo_maior_contribuicao[
                    "ativo"
                ]
            ),
            "valor": float(
                ativo_maior_contribuicao[
                    "contribuicao_bruta_simples"
                ]
            ),
            "unidade": (
                "soma das contribuições mensais"
            ),
            "cautela_amostral": "NÃO",
        },
        {
            "tema": "Menor contribuição bruta simples",
            "conclusao": (
                ativo_menor_contribuicao[
                    "ativo"
                ]
            ),
            "valor": float(
                ativo_menor_contribuicao[
                    "contribuicao_bruta_simples"
                ]
            ),
            "unidade": (
                "soma das contribuições mensais"
            ),
            "cautela_amostral": "NÃO",
        },
    ]
)


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

regimes_mensais.to_csv(
    ARQUIVO_REGIMES_MENSAIS,
    index=False,
    encoding="utf-8-sig",
)


desempenho_regimes.to_csv(
    ARQUIVO_DESEMPENHO_REGIMES,
    index=False,
    encoding="utf-8-sig",
)


desempenho_regimes_formatado.to_csv(
    ARQUIVO_DESEMPENHO_REGIMES_FORMATADO,
    index=False,
    encoding="utf-8-sig",
)


pesos_medios.to_csv(
    ARQUIVO_PESOS_MEDIOS,
    index=False,
    encoding="utf-8-sig",
)


contribuicao_mensal.to_csv(
    ARQUIVO_CONTRIBUICAO_MENSAL,
    index=False,
    encoding="utf-8-sig",
)


contribuicao_regimes.to_csv(
    ARQUIVO_CONTRIBUICAO_REGIMES,
    index=False,
    encoding="utf-8-sig",
)


contribuicao_total.to_csv(
    ARQUIVO_CONTRIBUICAO_TOTAL,
    index=False,
    encoding="utf-8-sig",
)


conclusoes.to_csv(
    ARQUIVO_CONCLUSOES,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO 1 — FREQUÊNCIA DOS REGIMES
# ============================================================

dados_frequencia = (
    desempenho_regimes.set_index(
        "nome_regime"
    )[
        "quantidade_meses"
    ]
)


fig, ax = plt.subplots(
    figsize=(11, 7)
)


dados_frequencia.plot(
    kind="bar",
    ax=ax,
)


ax.set_title(
    "Quantidade de Meses por Regime Macroeconômico"
)

ax.set_xlabel(
    "Regime"
)

ax.set_ylabel(
    "Quantidade de meses"
)

ax.tick_params(
    axis="x",
    rotation=20,
)

ax.grid(
    axis="y",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_FREQUENCIA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — RETORNO POR REGIME
# ============================================================

dados_retorno_grafico = (
    desempenho_regimes.set_index(
        "nome_regime"
    )[
        [
            "retorno_total_oficial",
            "retorno_total_challenger",
            "retorno_total_benchmark",
        ]
    ]
    .copy()
)


dados_retorno_grafico.columns = [
    "Modelo oficial",
    "Challenger",
    "Benchmark",
]


fig, ax = plt.subplots(
    figsize=(13, 7)
)


dados_retorno_grafico.plot(
    kind="bar",
    ax=ax,
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
    "Retorno Acumulado nos Meses de Cada Regime"
)

ax.set_xlabel(
    "Regime"
)

ax.set_ylabel(
    "Retorno acumulado"
)

ax.tick_params(
    axis="x",
    rotation=20,
)

ax.legend(
    title="Carteira"
)

ax.grid(
    axis="y",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_RETORNOS,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — CONTRIBUIÇÃO DOS ATIVOS POR REGIME
# ============================================================

contribuicao_grafico = (
    contribuicao_regimes.pivot(
        index="nome_regime",
        columns="ativo",
        values="contribuicao_bruta_simples",
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


contribuicao_grafico.plot(
    kind="bar",
    ax=ax,
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
    "Soma das Contribuições Mensais dos Ativos por Regime"
)

ax.set_xlabel(
    "Regime"
)

ax.set_ylabel(
    "Contribuição bruta simples"
)

ax.tick_params(
    axis="x",
    rotation=20,
)

ax.legend(
    title="Ativo",
)

ax.grid(
    axis="y",
    alpha=0.3,
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_CONTRIBUICAO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 4 — PESOS MÉDIOS POR REGIME
# ============================================================

colunas_pesos_medios = [
    f"peso_medio_{ativo}"
    for ativo in ATIVOS
]


pesos_grafico = (
    pesos_medios.set_index(
        "nome_regime"
    )[
        colunas_pesos_medios
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
    "Pesos Médios do Modelo Oficial por Regime"
)

ax.set_xlabel(
    "Regime"
)

ax.set_ylabel(
    "Peso médio"
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
# VALIDAÇÕES
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
    nome="Validações da Etapa 2",
    aprovado=True,
    detalhe=(
        f"{len(validacoes_celula_2)} "
        "validações aprovadas"
    ),
)


adicionar_validacao(
    nome="Quantidade de meses",
    aprovado=(
        len(series_finais) > 0
    ),
    detalhe=(
        f"{len(series_finais)} meses"
    ),
)


REGIMES_OBSERVADOS = set(
    series_finais[
        "regime_aplicado"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


adicionar_validacao(
    nome="Regimes observados válidos",
    aprovado=(
        bool(
            REGIMES_OBSERVADOS
        )
        and REGIMES_OBSERVADOS.issubset(
            set(
                ORDEM_REGIMES
            )
        )
    ),
    detalhe=(
        f"{len(REGIMES_OBSERVADOS)} regime(s) presente(s): "
        f"{sorted(REGIMES_OBSERVADOS)}"
    ),
)


adicionar_validacao(
    nome="Todos os meses possuem regime",
    aprovado=(
        not series_finais[
            "regime_aplicado"
        ]
        .isna()
        .any()
    ),
    detalhe=(
        f"{int(series_finais['regime_aplicado'].isna().sum())} "
        "meses sem regime"
    ),
)


adicionar_validacao(
    nome="Soma das frequências",
    aprovado=(
        int(
            desempenho_regimes[
                "quantidade_meses"
            ].sum()
        )
        == len(
            series_finais
        )
    ),
    detalhe=(
        f"{int(desempenho_regimes['quantidade_meses'].sum())} "
        "meses classificados"
    ),
)


adicionar_validacao(
    nome="Pesos mensais somam 100%",
    aprovado=np.allclose(
        series_finais[
            COLUNAS_PESOS
        ]
        .sum(
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
    nome="Pesos médios somam 100%",
    aprovado=np.allclose(
        pesos_medios[
            "soma_pesos_medios"
        ],
        1.0,
        atol=1e-10,
        rtol=1e-10,
    ),
    detalhe=(
        "Todos os regimes somam 100%"
    ),
)


MAIOR_DIFERENCA_CONTRIBUICAO = float(
    contribuicao_mensal[
        "diferenca_contribuicao_vs_retorno_bruto"
    ]
    .abs()
    .max()
)


adicionar_validacao(
    nome="Contribuições reproduzem retorno bruto",
    aprovado=(
        MAIOR_DIFERENCA_CONTRIBUICAO
        <= 1e-10
    ),
    detalhe=(
        f"Maior diferença: "
        f"{MAIOR_DIFERENCA_CONTRIBUICAO:.12f}"
    ),
)


adicionar_validacao(
    nome="Contribuições sem nulos",
    aprovado=(
        not contribuicao_mensal[
            COLUNAS_CONTRIBUICAO
        ]
        .isna()
        .any()
        .any()
    ),
    detalhe=(
        f"{int(contribuicao_mensal[COLUNAS_CONTRIBUICAO].isna().sum().sum())} "
        "nulos"
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


if (
    tabela_validacoes[
        "status"
    ]
    .eq(
        "REPROVADO"
    )
    .any()
):

    raise ValueError(
        "Uma ou mais validações da Etapa 3 "
        "foram reprovadas:\n\n"
        f"{tabela_validacoes}"
    )


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

ARQUIVOS_ESPERADOS = [
    ARQUIVO_REGIMES_MENSAIS,
    ARQUIVO_DESEMPENHO_REGIMES,
    ARQUIVO_DESEMPENHO_REGIMES_FORMATADO,
    ARQUIVO_PESOS_MEDIOS,
    ARQUIVO_CONTRIBUICAO_MENSAL,
    ARQUIVO_CONTRIBUICAO_REGIMES,
    ARQUIVO_CONTRIBUICAO_TOTAL,
    ARQUIVO_CONCLUSOES,
    ARQUIVO_VALIDACOES,
    ARQUIVO_GRAFICO_FREQUENCIA,
    ARQUIVO_GRAFICO_RETORNOS,
    ARQUIVO_GRAFICO_CONTRIBUICAO,
    ARQUIVO_GRAFICO_PESOS,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in ARQUIVOS_ESPERADOS
    if not arquivo.exists()
]


if arquivos_nao_salvos:

    raise FileNotFoundError(
        "Alguns arquivos da Etapa 3 "
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
print("ETAPA 3 — ANÁLISE POR REGIME CONCLUÍDA")
print("=" * 70)


print(
    f"\nPeríodo analisado: "
    f"{series_finais['data'].min():%d/%m/%Y} "
    f"a "
    f"{series_finais['data'].max():%d/%m/%Y}"
)


print(
    f"Quantidade de meses: "
    f"{len(series_finais)}"
)


print(
    "\nDistribuição dos regimes:"
)


for _, linha in desempenho_regimes.iterrows():

    print(
        f"- {linha['nome_regime']}: "
        f"{int(linha['quantidade_meses'])} meses "
        f"({float(linha['proporcao_periodo']):.2%})"
    )


print(
    "\nRetorno do modelo oficial por regime:"
)


for _, linha in (
    desempenho_regimes.loc[
        desempenho_regimes[
            "quantidade_meses"
        ]
        > 0
    ]
    .iterrows()
):

    aviso = (
        " — AMOSTRA REDUZIDA"
        if bool(
            linha[
                "amostra_reduzida"
            ]
        )
        else ""
    )

    print(
        f"- {linha['nome_regime']}: "
        f"{float(linha['retorno_total_oficial']):.2%} | "
        f"excesso vs benchmark: "
        f"{float(linha['excesso_oficial_vs_benchmark']):.2%}"
        f"{aviso}"
    )


print(
    "\nContribuição bruta simples dos ativos:"
)


for _, linha in contribuicao_total.iterrows():

    print(
        f"- {linha['ativo']}: "
        f"{float(linha['contribuicao_bruta_simples']):.2%}"
    )


print(
    f"\nRegime com melhor retorno: "
    f"{melhor_regime_retorno['nome_regime']} "
    f"({float(melhor_regime_retorno['retorno_total_oficial']):.2%})"
)


print(
    f"Regime com maior excesso contra o benchmark: "
    f"{melhor_regime_excesso['nome_regime']} "
    f"({float(melhor_regime_excesso['excesso_oficial_vs_benchmark']):.2%})"
)


print(
    f"Ativo com maior contribuição bruta simples: "
    f"{ativo_maior_contribuicao['ativo']} "
    f"({float(ativo_maior_contribuicao['contribuicao_bruta_simples']):.2%})"
)


print(
    "\nDesempenho por regime:"
)


display(
    desempenho_regimes_formatado
)


print(
    "\nPesos médios por regime:"
)


display(
    pesos_medios
)


print(
    "\nContribuição total dos ativos:"
)


display(
    contribuicao_total
)


print(
    "\nConclusões:"
)


display(
    conclusoes
)


print(
    "\nValidações:"
)


display(
    tabela_validacoes
)

# ###########################################################################
# ETAPA 04 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# ETAPA 4 — ESTABILIDADE TEMPORAL E PERÍODOS DE ESTRESSE
# SCRIPT 07 — ANÁLISE DOS RESULTADOS FINAIS
# VERSÃO AUTÔNOMA
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter


# ============================================================
# CONFIGURAÇÕES
# ============================================================

VALOR_INICIAL = 100.0
PERIODOS_POR_ANO = 12

JANELA_CURTA = 6
JANELA_LONGA = 12
QUANTIDADE_MESES_ESTRESSE = 5

CENARIO_OFICIAL = CENARIO_OFICIAL_JSON
CENARIO_CHALLENGER = CENARIO_CHALLENGER_JSON
CENARIO_BENCHMARK = "BENCHMARK_5_ATIVOS"
CENARIO_CDI = "CDI_100"

CENARIOS_ANALISADOS = [
    CENARIO_OFICIAL,
    CENARIO_CHALLENGER,
    CENARIO_BENCHMARK,
    CENARIO_CDI,
]

ROTULOS = {
    CENARIO_OFICIAL: "Modelo oficial",
    CENARIO_CHALLENGER: f"Challenger — {MODELO_CHALLENGER}",
    CENARIO_BENCHMARK: "Benchmark",
    CENARIO_CDI: "100% CDI",
}

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
        / "outputs"
        / "tabelas"
        / "07_03_validacoes.csv"
    )

    if arquivo_teste.exists():

        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:

    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo outputs/tabelas/"
        "07_03_validacoes.csv não foi encontrado."
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

ARQUIVO_VALIDACOES_CELULA_3 = (
    PASTA_TABELAS
    / "07_03_validacoes.csv"
)

ARQUIVO_SERIES_FINAIS = (
    PASTA_TABELAS
    / "06_12_series_modelos_finais.csv"
)

ARQUIVO_REGIMES = (
    PASTA_TABELAS
    / "07_03_regimes_mensais_aplicados.csv"
)

ARQUIVO_COMPARACAO = (
    PASTA_TABELAS
    / "07_02_comparacao_desempenho_risco.csv"
)


ARQUIVOS_ENTRADA = [
    ARQUIVO_VALIDACOES_CELULA_3,
    ARQUIVO_SERIES_FINAIS,
    ARQUIVO_REGIMES,
    ARQUIVO_COMPARACAO,
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
            str(arquivo)
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_SERIES_ROLLING = (
    PASTA_TABELAS
    / "07_04_series_rolling.csv"
)

ARQUIVO_SUBPERIODOS = (
    PASTA_TABELAS
    / "07_04_resultados_subperiodos.csv"
)

ARQUIVO_SUBPERIODOS_FORMATADO = (
    PASTA_TABELAS
    / "07_04_resultados_subperiodos_formatado.csv"
)

ARQUIVO_PIORES_MESES = (
    PASTA_TABELAS
    / "07_04_piores_meses.csv"
)

ARQUIVO_MELHORES_MESES = (
    PASTA_TABELAS
    / "07_04_melhores_meses.csv"
)

ARQUIVO_TRANSICOES = (
    PASTA_TABELAS
    / "07_04_transicoes_regime.csv"
)

ARQUIVO_EPISODIOS = (
    PASTA_TABELAS
    / "07_04_episodios_regime.csv"
)

ARQUIVO_RESUMO_ESTABILIDADE = (
    PASTA_TABELAS
    / "07_04_resumo_estabilidade.csv"
)

ARQUIVO_CONCLUSOES = (
    PASTA_TABELAS
    / "07_04_conclusoes_estabilidade.csv"
)

ARQUIVO_VALIDACOES = (
    PASTA_TABELAS
    / "07_04_validacoes.csv"
)

ARQUIVO_GRAFICO_ROLLING = (
    PASTA_GRAFICOS
    / "07_04_retornos_rolling_12m.png"
)

ARQUIVO_GRAFICO_EXCESSO = (
    PASTA_GRAFICOS
    / "07_04_excesso_rolling_12m.png"
)

ARQUIVO_GRAFICO_VOLATILIDADE = (
    PASTA_GRAFICOS
    / "07_04_volatilidade_rolling_12m.png"
)

ARQUIVO_GRAFICO_SEMESTRAL = (
    PASTA_GRAFICOS
    / "07_04_retornos_semestrais.png"
)

ARQUIVO_GRAFICO_ESTRESSE = (
    PASTA_GRAFICOS
    / "07_04_piores_meses.png"
)


# ============================================================
# CARREGAMENTO
# ============================================================

validacoes_celula_3 = pd.read_csv(
    ARQUIVO_VALIDACOES_CELULA_3,
    encoding="utf-8-sig",
)

series_finais = pd.read_csv(
    ARQUIVO_SERIES_FINAIS,
    encoding="utf-8-sig",
)

regimes_mensais = pd.read_csv(
    ARQUIVO_REGIMES,
    encoding="utf-8-sig",
)

comparacao_modelos = pd.read_csv(
    ARQUIVO_COMPARACAO,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DA ETAPA ANTERIOR
# ============================================================

if not {
    "validacao",
    "status",
    "detalhe",
}.issubset(
    validacoes_celula_3.columns
):

    raise ValueError(
        "O arquivo de validações da Etapa 3 "
        "possui estrutura inválida."
    )


if (
    validacoes_celula_3["status"]
    .astype(str)
    .str.upper()
    .eq("REPROVADO")
    .any()
):

    raise ValueError(
        "A Etapa 3 possui validações reprovadas."
    )


# ============================================================
# PADRONIZAÇÃO DAS DATAS
# ============================================================

for nome_base, base_dados in {
    "séries finais": series_finais,
    "regimes mensais": regimes_mensais,
}.items():

    if "data" not in base_dados.columns:

        raise ValueError(
            f"A base {nome_base} não possui a coluna data."
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
# JUNÇÃO DO REGIME APLICADO
# ============================================================

colunas_regime = [
    "data",
    "regime_aplicado",
    "nome_regime",
]


for coluna_opcional in [
    "meses_confirmacao_aplicada",
    "numero_recalibracao",
    "candidato_aplicado",
    "data_final_treino_utilizada",
]:

    if coluna_opcional in regimes_mensais.columns:

        colunas_regime.append(
            coluna_opcional
        )


series_base = (
    series_finais
    .drop(
        columns=[
            coluna
            for coluna in colunas_regime
            if (
                coluna != "data"
                and coluna in series_finais.columns
            )
        ],
        errors="ignore",
    )
    .merge(
        regimes_mensais[
            colunas_regime
        ],
        on="data",
        how="left",
        validate="one_to_one",
    )
    .sort_values("data")
    .reset_index(drop=True)
)


if series_base["regime_aplicado"].isna().any():

    raise ValueError(
        "Existem meses sem regime aplicado."
    )


regimes_invalidos = (
    series_base.loc[
        ~series_base["regime_aplicado"].isin(
            ORDEM_REGIMES
        ),
        "regime_aplicado",
    ]
    .unique()
    .tolist()
)


if regimes_invalidos:

    raise ValueError(
        "Foram encontrados regimes inválidos:\n"
        f"{regimes_invalidos}"
    )


# ============================================================
# COLUNAS DOS RETORNOS
# ============================================================

COLUNAS_RETORNOS = {
    cenario: f"retorno_liquido_{cenario}"
    for cenario in CENARIOS_ANALISADOS
}


for cenario, coluna in COLUNAS_RETORNOS.items():

    if coluna not in series_base.columns:

        raise ValueError(
            f"A coluna {coluna} não foi encontrada."
        )

    series_base[coluna] = pd.to_numeric(
        series_base[coluna],
        errors="coerce",
    )

    if series_base[coluna].isna().any():

        raise ValueError(
            f"A coluna {coluna} possui valores inválidos."
        )


if len(series_base) == 0:

    raise ValueError(
        "A base final de avaliação ficou vazia."
    )


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def calcular_retorno_total(retornos):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(retornos) == 0:

        return np.nan

    return float(
        np.prod(1.0 + retornos) - 1.0
    )


def calcular_retorno_anualizado(retornos):

    retornos = np.asarray(
        retornos,
        dtype=float,
    )

    if len(retornos) == 0:

        return np.nan

    retorno_total = calcular_retorno_total(
        retornos
    )

    if retorno_total <= -1.0:

        return np.nan

    return float(
        (1.0 + retorno_total)
        ** (
            PERIODOS_POR_ANO
            / len(retornos)
        )
        - 1.0
    )


def calcular_volatilidade_anualizada(retornos):

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
        * np.sqrt(PERIODOS_POR_ANO)
    )


def calcular_drawdown(retornos):

    retornos = pd.Series(
        retornos,
        dtype=float,
    ).reset_index(drop=True)

    indice = (
        VALOR_INICIAL
        * (1.0 + retornos).cumprod()
    )

    indice_com_inicio = pd.concat(
        [
            pd.Series(
                [VALOR_INICIAL],
                dtype=float,
            ),
            indice,
        ],
        ignore_index=True,
    )

    picos = indice_com_inicio.cummax()

    drawdown = (
        indice_com_inicio
        / picos
        - 1.0
    )

    return (
        drawdown.iloc[1:]
        .reset_index(drop=True)
    )


def calcular_maximo_drawdown(retornos):

    drawdown = calcular_drawdown(
        retornos
    )

    if drawdown.empty:

        return np.nan

    return float(
        drawdown.min()
    )


def calcular_retorno_rolling(
    retornos,
    janela,
):

    retornos = pd.Series(
        retornos,
        dtype=float,
    )

    return (
        (1.0 + retornos)
        .rolling(janela)
        .apply(
            np.prod,
            raw=True,
        )
        - 1.0
    )


def calcular_volatilidade_rolling(
    retornos,
    janela,
):

    retornos = pd.Series(
        retornos,
        dtype=float,
    )

    return (
        retornos
        .rolling(janela)
        .std(ddof=1)
        * np.sqrt(PERIODOS_POR_ANO)
    )


def calcular_sharpe_rolling(
    retornos,
    retornos_cdi,
    janela,
):

    excesso = (
        pd.Series(
            retornos,
            dtype=float,
        )
        - pd.Series(
            retornos_cdi,
            dtype=float,
        )
    )

    media = (
        excesso
        .rolling(janela)
        .mean()
    )

    desvio = (
        excesso
        .rolling(janela)
        .std(ddof=1)
    )

    sharpe = (
        np.sqrt(PERIODOS_POR_ANO)
        * media
        / desvio
    )

    sharpe = sharpe.where(
        desvio > 0
    )

    return sharpe


# ============================================================
# ÍNDICES, DRAWDOWNS E JANELAS ROLLING
# ============================================================

series_rolling = series_base[
    [
        "data",
        "regime_aplicado",
        "nome_regime",
    ]
].copy()


for coluna_opcional in [
    "meses_confirmacao_aplicada",
    "numero_recalibracao",
    "candidato_aplicado",
    "data_final_treino_utilizada",
]:

    if coluna_opcional in series_base.columns:

        series_rolling[coluna_opcional] = (
            series_base[coluna_opcional]
        )


for cenario in CENARIOS_ANALISADOS:

    coluna_retorno = COLUNAS_RETORNOS[
        cenario
    ]

    retornos = series_base[
        coluna_retorno
    ]

    series_rolling[
        f"retorno_{cenario}"
    ] = retornos

    series_rolling[
        f"indice_{cenario}"
    ] = (
        VALOR_INICIAL
        * (1.0 + retornos).cumprod()
    )

    series_rolling[
        f"drawdown_{cenario}"
    ] = calcular_drawdown(
        retornos
    )

    for janela in [
        JANELA_CURTA,
        JANELA_LONGA,
    ]:

        series_rolling[
            f"retorno_rolling_{janela}m_{cenario}"
        ] = calcular_retorno_rolling(
            retornos=retornos,
            janela=janela,
        )

        series_rolling[
            f"volatilidade_rolling_{janela}m_{cenario}"
        ] = calcular_volatilidade_rolling(
            retornos=retornos,
            janela=janela,
        )


series_rolling[
    "excesso_rolling_6m_vs_benchmark"
] = (
    series_rolling[
        f"retorno_rolling_6m_{CENARIO_OFICIAL}"
    ]
    - series_rolling[
        f"retorno_rolling_6m_{CENARIO_BENCHMARK}"
    ]
)


series_rolling[
    "excesso_rolling_12m_vs_benchmark"
] = (
    series_rolling[
        f"retorno_rolling_12m_{CENARIO_OFICIAL}"
    ]
    - series_rolling[
        f"retorno_rolling_12m_{CENARIO_BENCHMARK}"
    ]
)


series_rolling[
    "excesso_rolling_12m_vs_challenger"
] = (
    series_rolling[
        f"retorno_rolling_12m_{CENARIO_OFICIAL}"
    ]
    - series_rolling[
        f"retorno_rolling_12m_{CENARIO_CHALLENGER}"
    ]
)


series_rolling[
    "excesso_rolling_12m_vs_cdi"
] = (
    series_rolling[
        f"retorno_rolling_12m_{CENARIO_OFICIAL}"
    ]
    - series_rolling[
        f"retorno_rolling_12m_{CENARIO_CDI}"
    ]
)


series_rolling[
    "sharpe_rolling_12m_excesso_cdi"
] = calcular_sharpe_rolling(
    retornos=series_base[
        COLUNAS_RETORNOS[
            CENARIO_OFICIAL
        ]
    ],
    retornos_cdi=series_base[
        COLUNAS_RETORNOS[
            CENARIO_CDI
        ]
    ],
    janela=JANELA_LONGA,
)


# ============================================================
# RESULTADOS POR SUBPERÍODO
# ============================================================

series_base["ano"] = (
    series_base["data"]
    .dt.year
)


series_base["semestre_numero"] = np.where(
    series_base["data"].dt.month <= 6,
    1,
    2,
)


series_base["semestre"] = (
    series_base["ano"].astype(str)
    + "S"
    + series_base["semestre_numero"].astype(str)
)


def construir_resultados_subperiodos(
    dados,
    coluna_grupo,
    tipo_periodo,
    meses_periodo_completo,
):

    registros = []

    for periodo, dados_periodo in dados.groupby(
        coluna_grupo,
        sort=True,
    ):

        dados_periodo = (
            dados_periodo
            .sort_values("data")
            .copy()
        )

        quantidade_meses = len(
            dados_periodo
        )

        retorno_benchmark = (
            calcular_retorno_total(
                dados_periodo[
                    COLUNAS_RETORNOS[
                        CENARIO_BENCHMARK
                    ]
                ]
            )
        )

        for cenario in CENARIOS_ANALISADOS:

            retornos = dados_periodo[
                COLUNAS_RETORNOS[
                    cenario
                ]
            ]

            retorno_total = (
                calcular_retorno_total(
                    retornos
                )
            )

            registros.append(
                {
                    "tipo_periodo": tipo_periodo,
                    "periodo": str(periodo),
                    "data_inicial": (
                        dados_periodo["data"].min()
                    ),
                    "data_final": (
                        dados_periodo["data"].max()
                    ),
                    "quantidade_meses": (
                        quantidade_meses
                    ),
                    "periodo_completo": (
                        quantidade_meses
                        == meses_periodo_completo
                    ),
                    "cenario": cenario,
                    "modelo": ROTULOS[cenario],
                    "retorno_total": retorno_total,
                    "retorno_anualizado": (
                        calcular_retorno_anualizado(
                            retornos
                        )
                    ),
                    "volatilidade_anualizada": (
                        calcular_volatilidade_anualizada(
                            retornos
                        )
                    ),
                    "maximo_drawdown": (
                        calcular_maximo_drawdown(
                            retornos
                        )
                    ),
                    "meses_positivos": float(
                        retornos.gt(0).mean()
                    ),
                    "retorno_benchmark": (
                        retorno_benchmark
                    ),
                    "excesso_vs_benchmark": (
                        retorno_total
                        - retorno_benchmark
                    ),
                    "superou_benchmark": (
                        retorno_total
                        > retorno_benchmark
                    ),
                }
            )

    return pd.DataFrame(
        registros
    )


resultados_anuais = (
    construir_resultados_subperiodos(
        dados=series_base,
        coluna_grupo="ano",
        tipo_periodo="ANUAL",
        meses_periodo_completo=12,
    )
)


resultados_semestrais = (
    construir_resultados_subperiodos(
        dados=series_base,
        coluna_grupo="semestre",
        tipo_periodo="SEMESTRAL",
        meses_periodo_completo=6,
    )
)


resultados_subperiodos = pd.concat(
    [
        resultados_anuais,
        resultados_semestrais,
    ],
    ignore_index=True,
)


# ============================================================
# TABELA FORMATADA DOS SUBPERÍODOS
# ============================================================

resultados_subperiodos_formatado = (
    resultados_subperiodos
    .copy()
    .astype(object)
)


for coluna in [
    "retorno_total",
    "retorno_anualizado",
    "volatilidade_anualizada",
    "maximo_drawdown",
    "meses_positivos",
    "retorno_benchmark",
    "excesso_vs_benchmark",
]:

    resultados_subperiodos_formatado[
        coluna
    ] = resultados_subperiodos[
        coluna
    ].map(
        lambda valor: (
            f"{valor:.2%}"
            if pd.notna(valor)
            else "-"
        )
    )


# ============================================================
# MELHORES E PIORES MESES
# ============================================================

colunas_estresse = [
    "data",
    "regime_aplicado",
    "nome_regime",
    COLUNAS_RETORNOS[CENARIO_OFICIAL],
    COLUNAS_RETORNOS[CENARIO_CHALLENGER],
    COLUNAS_RETORNOS[CENARIO_BENCHMARK],
    COLUNAS_RETORNOS[CENARIO_CDI],
]


meses_estresse = (
    series_base[
        colunas_estresse
    ]
    .copy()
)


meses_estresse.rename(
    columns={
        COLUNAS_RETORNOS[CENARIO_OFICIAL]: (
            "retorno_modelo_oficial"
        ),
        COLUNAS_RETORNOS[CENARIO_CHALLENGER]: (
            "retorno_challenger"
        ),
        COLUNAS_RETORNOS[CENARIO_BENCHMARK]: (
            "retorno_benchmark"
        ),
        COLUNAS_RETORNOS[CENARIO_CDI]: (
            "retorno_cdi"
        ),
    },
    inplace=True,
)


meses_estresse[
    "excesso_vs_benchmark"
] = (
    meses_estresse[
        "retorno_modelo_oficial"
    ]
    - meses_estresse[
        "retorno_benchmark"
    ]
)


meses_estresse[
    "excesso_vs_challenger"
] = (
    meses_estresse[
        "retorno_modelo_oficial"
    ]
    - meses_estresse[
        "retorno_challenger"
    ]
)


piores_meses = (
    meses_estresse
    .nsmallest(
        QUANTIDADE_MESES_ESTRESSE,
        "retorno_modelo_oficial",
    )
    .copy()
    .reset_index(drop=True)
)


piores_meses.insert(
    0,
    "posicao",
    np.arange(
        1,
        len(piores_meses) + 1,
    ),
)


melhores_meses = (
    meses_estresse
    .nlargest(
        QUANTIDADE_MESES_ESTRESSE,
        "retorno_modelo_oficial",
    )
    .copy()
    .reset_index(drop=True)
)


melhores_meses.insert(
    0,
    "posicao",
    np.arange(
        1,
        len(melhores_meses) + 1,
    ),
)


# ============================================================
# TRANSIÇÕES E EPISÓDIOS DOS REGIMES
# ============================================================

series_regimes = (
    series_base[
        [
            "data",
            "regime_aplicado",
            "nome_regime",
        ]
    ]
    .copy()
)


series_regimes[
    "regime_anterior"
] = (
    series_regimes[
        "regime_aplicado"
    ].shift(1)
)


transicoes_regime = pd.crosstab(
    series_regimes[
        "regime_anterior"
    ],
    series_regimes[
        "regime_aplicado"
    ],
)


transicoes_regime = (
    transicoes_regime
    .reindex(
        index=ORDEM_REGIMES,
        columns=ORDEM_REGIMES,
        fill_value=0,
    )
)


transicoes_regime.index.name = (
    "regime_origem"
)

transicoes_regime.columns.name = (
    "regime_destino"
)


transicoes_regime.reset_index(
    inplace=True
)


series_regimes[
    "grupo_episodio"
] = (
    series_regimes[
        "regime_aplicado"
    ]
    .ne(
        series_regimes[
            "regime_aplicado"
        ].shift(1)
    )
    .cumsum()
)


episodios_regime = (
    series_regimes
    .groupby(
        "grupo_episodio",
        as_index=False,
    )
    .agg(
        regime_aplicado=(
            "regime_aplicado",
            "first",
        ),
        nome_regime=(
            "nome_regime",
            "first",
        ),
        data_inicial=(
            "data",
            "min",
        ),
        data_final=(
            "data",
            "max",
        ),
        quantidade_meses=(
            "data",
            "size",
        ),
    )
)


episodios_regime.insert(
    0,
    "numero_episodio",
    np.arange(
        1,
        len(episodios_regime) + 1,
    ),
)


# ============================================================
# ESTATÍSTICAS DE ESTABILIDADE
# ============================================================

rolling_12m_validos = (
    series_rolling
    .dropna(
        subset=[
            "excesso_rolling_12m_vs_benchmark",
            "excesso_rolling_12m_vs_challenger",
            "excesso_rolling_12m_vs_cdi",
        ]
    )
    .copy()
)


PROPORCAO_ROLLING_SUPERA_BENCHMARK = float(
    rolling_12m_validos[
        "excesso_rolling_12m_vs_benchmark"
    ]
    .gt(0)
    .mean()
)


PROPORCAO_ROLLING_SUPERA_CHALLENGER = float(
    rolling_12m_validos[
        "excesso_rolling_12m_vs_challenger"
    ]
    .gt(0)
    .mean()
)


PROPORCAO_ROLLING_SUPERA_CDI = float(
    rolling_12m_validos[
        "excesso_rolling_12m_vs_cdi"
    ]
    .gt(0)
    .mean()
)


PIOR_EXCESSO_ROLLING_BENCHMARK = float(
    rolling_12m_validos[
        "excesso_rolling_12m_vs_benchmark"
    ].min()
)


MELHOR_EXCESSO_ROLLING_BENCHMARK = float(
    rolling_12m_validos[
        "excesso_rolling_12m_vs_benchmark"
    ].max()
)


EXCESSO_ROLLING_ATUAL_BENCHMARK = float(
    rolling_12m_validos[
        "excesso_rolling_12m_vs_benchmark"
    ].iloc[-1]
)


resultados_anuais_oficial = (
    resultados_subperiodos.loc[
        resultados_subperiodos[
            "tipo_periodo"
        ].eq("ANUAL")
        & resultados_subperiodos[
            "cenario"
        ].eq(CENARIO_OFICIAL)
    ]
)


resultados_semestrais_oficial = (
    resultados_subperiodos.loc[
        resultados_subperiodos[
            "tipo_periodo"
        ].eq("SEMESTRAL")
        & resultados_subperiodos[
            "cenario"
        ].eq(CENARIO_OFICIAL)
    ]
)


ANOS_ACIMA_BENCHMARK = int(
    resultados_anuais_oficial[
        "superou_benchmark"
    ].sum()
)


SEMESTRES_ACIMA_BENCHMARK = int(
    resultados_semestrais_oficial[
        "superou_benchmark"
    ].sum()
)


QUANTIDADE_ANOS = int(
    len(resultados_anuais_oficial)
)


QUANTIDADE_SEMESTRES = int(
    len(resultados_semestrais_oficial)
)


QUANTIDADE_MUDANCAS_REGIME = int(
    max(
        len(episodios_regime) - 1,
        0,
    )
)


DURACAO_MEDIA_REGIME = float(
    episodios_regime[
        "quantidade_meses"
    ].mean()
)


DURACAO_MAXIMA_REGIME = int(
    episodios_regime[
        "quantidade_meses"
    ].max()
)


episodio_mais_longo = (
    episodios_regime.loc[
        episodios_regime[
            "quantidade_meses"
        ].idxmax()
    ]
)


pior_mes = piores_meses.iloc[0]
melhor_mes = melhores_meses.iloc[0]


PROPORCAO_PIORES_MESES_SUPERA_BENCHMARK = float(
    piores_meses[
        "excesso_vs_benchmark"
    ]
    .gt(0)
    .mean()
)


# ============================================================
# RESUMO DA ESTABILIDADE
# ============================================================

resumo_estabilidade = pd.DataFrame(
    {
        "metrica": [
            "Quantidade de meses",
            "Quantidade de janelas rolling de 12 meses",
            "Janelas de 12 meses acima do benchmark",
            "Janelas de 12 meses acima do challenger",
            "Janelas de 12 meses acima do CDI",
            "Pior excesso rolling contra benchmark",
            "Melhor excesso rolling contra benchmark",
            "Excesso rolling atual contra benchmark",
            "Períodos anuais acima do benchmark",
            "Quantidade de períodos anuais",
            "Períodos semestrais acima do benchmark",
            "Quantidade de períodos semestrais",
            "Quantidade de mudanças de regime",
            "Quantidade de episódios de regime",
            "Duração média dos episódios",
            "Maior duração de um episódio",
            "Regime do episódio mais longo",
            "Pior mês do modelo oficial",
            "Retorno no pior mês",
            "Excesso contra benchmark no pior mês",
            "Melhor mês do modelo oficial",
            "Retorno no melhor mês",
            "Piores meses acima do benchmark",
        ],
        "valor": [
            len(series_base),
            len(rolling_12m_validos),
            PROPORCAO_ROLLING_SUPERA_BENCHMARK,
            PROPORCAO_ROLLING_SUPERA_CHALLENGER,
            PROPORCAO_ROLLING_SUPERA_CDI,
            PIOR_EXCESSO_ROLLING_BENCHMARK,
            MELHOR_EXCESSO_ROLLING_BENCHMARK,
            EXCESSO_ROLLING_ATUAL_BENCHMARK,
            ANOS_ACIMA_BENCHMARK,
            QUANTIDADE_ANOS,
            SEMESTRES_ACIMA_BENCHMARK,
            QUANTIDADE_SEMESTRES,
            QUANTIDADE_MUDANCAS_REGIME,
            len(episodios_regime),
            DURACAO_MEDIA_REGIME,
            DURACAO_MAXIMA_REGIME,
            episodio_mais_longo[
                "nome_regime"
            ],
            pior_mes["data"].strftime(
                "%d/%m/%Y"
            ),
            pior_mes[
                "retorno_modelo_oficial"
            ],
            pior_mes[
                "excesso_vs_benchmark"
            ],
            melhor_mes["data"].strftime(
                "%d/%m/%Y"
            ),
            melhor_mes[
                "retorno_modelo_oficial"
            ],
            PROPORCAO_PIORES_MESES_SUPERA_BENCHMARK,
        ],
    }
)


# ============================================================
# CONCLUSÕES
# ============================================================

conclusoes = pd.DataFrame(
    [
        {
            "tema": "Consistência rolling contra benchmark",
            "conclusao": (
                "O modelo oficial superou o benchmark "
                f"em {PROPORCAO_ROLLING_SUPERA_BENCHMARK:.2%} "
                "das janelas de 12 meses."
            ),
            "valor": (
                PROPORCAO_ROLLING_SUPERA_BENCHMARK
            ),
            "unidade": (
                "proporção das janelas de 12 meses"
            ),
        },
        {
            "tema": "Consistência rolling contra challenger",
            "conclusao": (
                "O modelo oficial superou o challenger "
                f"em {PROPORCAO_ROLLING_SUPERA_CHALLENGER:.2%} "
                "das janelas de 12 meses."
            ),
            "valor": (
                PROPORCAO_ROLLING_SUPERA_CHALLENGER
            ),
            "unidade": (
                "proporção das janelas de 12 meses"
            ),
        },
        {
            "tema": "Desempenho anual",
            "conclusao": (
                f"O modelo oficial superou o benchmark "
                f"em {ANOS_ACIMA_BENCHMARK} de "
                f"{QUANTIDADE_ANOS} períodos anuais."
            ),
            "valor": ANOS_ACIMA_BENCHMARK,
            "unidade": (
                f"de {QUANTIDADE_ANOS} períodos"
            ),
        },
        {
            "tema": "Desempenho semestral",
            "conclusao": (
                f"O modelo oficial superou o benchmark "
                f"em {SEMESTRES_ACIMA_BENCHMARK} de "
                f"{QUANTIDADE_SEMESTRES} períodos semestrais."
            ),
            "valor": SEMESTRES_ACIMA_BENCHMARK,
            "unidade": (
                f"de {QUANTIDADE_SEMESTRES} períodos"
            ),
        },
        {
            "tema": "Pior janela rolling",
            "conclusao": (
                "O pior excesso de retorno em uma janela "
                "de 12 meses contra o benchmark foi de "
                f"{PIOR_EXCESSO_ROLLING_BENCHMARK:.2%}."
            ),
            "valor": (
                PIOR_EXCESSO_ROLLING_BENCHMARK
            ),
            "unidade": (
                "excesso de retorno"
            ),
        },
        {
            "tema": "Mudanças de regime",
            "conclusao": (
                f"Foram observadas "
                f"{QUANTIDADE_MUDANCAS_REGIME} mudanças "
                "de regime durante o período."
            ),
            "valor": (
                QUANTIDADE_MUDANCAS_REGIME
            ),
            "unidade": "mudanças",
        },
        {
            "tema": "Episódio mais longo",
            "conclusao": (
                f"O episódio mais longo foi de "
                f"{DURACAO_MAXIMA_REGIME} meses em "
                f"{episodio_mais_longo['nome_regime']}."
            ),
            "valor": (
                DURACAO_MAXIMA_REGIME
            ),
            "unidade": "meses",
        },
        {
            "tema": "Pior mês",
            "conclusao": (
                f"O pior mês ocorreu em "
                f"{pior_mes['data']:%m/%Y}, "
                f"com retorno de "
                f"{pior_mes['retorno_modelo_oficial']:.2%}."
            ),
            "valor": (
                pior_mes[
                    "retorno_modelo_oficial"
                ]
            ),
            "unidade": "retorno mensal",
        },
    ]
)


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

series_rolling.to_csv(
    ARQUIVO_SERIES_ROLLING,
    index=False,
    encoding="utf-8-sig",
)


resultados_subperiodos.to_csv(
    ARQUIVO_SUBPERIODOS,
    index=False,
    encoding="utf-8-sig",
)


resultados_subperiodos_formatado.to_csv(
    ARQUIVO_SUBPERIODOS_FORMATADO,
    index=False,
    encoding="utf-8-sig",
)


piores_meses.to_csv(
    ARQUIVO_PIORES_MESES,
    index=False,
    encoding="utf-8-sig",
)


melhores_meses.to_csv(
    ARQUIVO_MELHORES_MESES,
    index=False,
    encoding="utf-8-sig",
)


transicoes_regime.to_csv(
    ARQUIVO_TRANSICOES,
    index=False,
    encoding="utf-8-sig",
)


episodios_regime.to_csv(
    ARQUIVO_EPISODIOS,
    index=False,
    encoding="utf-8-sig",
)


resumo_estabilidade.to_csv(
    ARQUIVO_RESUMO_ESTABILIDADE,
    index=False,
    encoding="utf-8-sig",
)


conclusoes.to_csv(
    ARQUIVO_CONCLUSOES,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO 1 — RETORNOS ROLLING DE 12 MESES
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


for cenario in CENARIOS_ANALISADOS:

    ax.plot(
        series_rolling["data"],
        series_rolling[
            f"retorno_rolling_12m_{cenario}"
        ],
        linewidth=2,
        label=ROTULOS[cenario],
    )


ax.axhline(
    y=0.0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(xmax=1.0)
)


ax.set_title(
    "Retorno Acumulado em Janelas Móveis de 12 Meses"
)

ax.set_xlabel("Data")
ax.set_ylabel("Retorno em 12 meses")

ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_ROLLING,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 2 — EXCESSO ROLLING
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


ax.plot(
    series_rolling["data"],
    series_rolling[
        "excesso_rolling_12m_vs_benchmark"
    ],
    linewidth=2,
    label="Oficial menos benchmark",
)


ax.plot(
    series_rolling["data"],
    series_rolling[
        "excesso_rolling_12m_vs_challenger"
    ],
    linewidth=2,
    label="Oficial menos challenger",
)


ax.axhline(
    y=0.0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(xmax=1.0)
)


ax.set_title(
    "Excesso de Retorno em Janelas de 12 Meses"
)

ax.set_xlabel("Data")
ax.set_ylabel("Excesso de retorno")

ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_EXCESSO,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — VOLATILIDADE ROLLING
# ============================================================

fig, ax = plt.subplots(
    figsize=(13, 7)
)


for cenario in [
    CENARIO_OFICIAL,
    CENARIO_CHALLENGER,
    CENARIO_BENCHMARK,
]:

    ax.plot(
        series_rolling["data"],
        series_rolling[
            f"volatilidade_rolling_12m_{cenario}"
        ],
        linewidth=2,
        label=ROTULOS[cenario],
    )


ax.yaxis.set_major_formatter(
    PercentFormatter(xmax=1.0)
)


ax.set_title(
    "Volatilidade Anualizada em Janelas de 12 Meses"
)

ax.set_xlabel("Data")
ax.set_ylabel("Volatilidade anualizada")

ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_VOLATILIDADE,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 4 — RETORNOS SEMESTRAIS
# ============================================================

dados_semestrais_grafico = (
    resultados_subperiodos.loc[
        resultados_subperiodos[
            "tipo_periodo"
        ].eq("SEMESTRAL")
        & resultados_subperiodos[
            "cenario"
        ].isin(
            CENARIOS_ANALISADOS
        )
    ]
    .pivot(
        index="periodo",
        columns="modelo",
        values="retorno_total",
    )
)


fig, ax = plt.subplots(
    figsize=(13, 7)
)


dados_semestrais_grafico.plot(
    kind="bar",
    ax=ax,
)


ax.axhline(
    y=0.0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(xmax=1.0)
)


ax.set_title(
    "Retornos por Semestre"
)

ax.set_xlabel("Semestre")
ax.set_ylabel("Retorno líquido")

ax.tick_params(
    axis="x",
    rotation=0,
)

ax.legend(
    title="Modelo",
)

ax.grid(
    axis="y",
    alpha=0.3,
)

fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_SEMESTRAL,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 5 — PIORES MESES
# ============================================================

dados_estresse_grafico = (
    piores_meses[
        [
            "data",
            "retorno_modelo_oficial",
            "retorno_challenger",
            "retorno_benchmark",
            "retorno_cdi",
        ]
    ]
    .copy()
)


dados_estresse_grafico["periodo"] = (
    dados_estresse_grafico["data"]
    .dt.strftime("%m/%Y")
)


dados_estresse_grafico.set_index(
    "periodo",
    inplace=True,
)


dados_estresse_grafico.drop(
    columns=["data"],
    inplace=True,
)


dados_estresse_grafico.columns = [
    "Modelo oficial",
    "Challenger",
    "Benchmark",
    "CDI",
]


fig, ax = plt.subplots(
    figsize=(13, 7)
)


dados_estresse_grafico.plot(
    kind="bar",
    ax=ax,
)


ax.axhline(
    y=0.0,
    linewidth=1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(xmax=1.0)
)


ax.set_title(
    "Cinco Piores Meses do Modelo Oficial"
)

ax.set_xlabel("Mês")
ax.set_ylabel("Retorno mensal")

ax.tick_params(
    axis="x",
    rotation=0,
)

ax.legend(
    title="Carteira",
)

ax.grid(
    axis="y",
    alpha=0.3,
)

fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_ESTRESSE,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÕES
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
    nome="Validações da Etapa 3",
    aprovado=True,
    detalhe=(
        f"{len(validacoes_celula_3)} "
        "validações aprovadas"
    ),
)


adicionar_validacao(
    nome="Quantidade de meses",
    aprovado=(
        len(series_base) > 0
    ),
    detalhe=(
        f"{len(series_base)} meses"
    ),
)


QUANTIDADE_JANELAS_12M_ESPERADA = (
    len(series_base)
    - JANELA_LONGA
    + 1
)


adicionar_validacao(
    nome="Quantidade de janelas rolling de 12 meses",
    aprovado=(
        len(rolling_12m_validos)
        == QUANTIDADE_JANELAS_12M_ESPERADA
    ),
    detalhe=(
        f"{len(rolling_12m_validos)} janelas"
    ),
)


adicionar_validacao(
    nome="Retornos rolling válidos",
    aprovado=(
        not rolling_12m_validos[
            [
                "excesso_rolling_12m_vs_benchmark",
                "excesso_rolling_12m_vs_challenger",
                "excesso_rolling_12m_vs_cdi",
            ]
        ]
        .isna()
        .any()
        .any()
    ),
    detalhe=(
        "Nenhum valor nulo nas janelas completas"
    ),
)


adicionar_validacao(
    nome="Meses classificados por subperíodo anual",
    aprovado=(
        int(
            resultados_anuais_oficial[
                "quantidade_meses"
            ].sum()
        )
        == len(series_base)
    ),
    detalhe=(
        f"{int(resultados_anuais_oficial['quantidade_meses'].sum())} "
        "meses"
    ),
)


adicionar_validacao(
    nome="Meses classificados por subperíodo semestral",
    aprovado=(
        int(
            resultados_semestrais_oficial[
                "quantidade_meses"
            ].sum()
        )
        == len(series_base)
    ),
    detalhe=(
        f"{int(resultados_semestrais_oficial['quantidade_meses'].sum())} "
        "meses"
    ),
)


adicionar_validacao(
    nome="Quantidade de transições mensais",
    aprovado=(
        int(
            transicoes_regime[
                ORDEM_REGIMES
            ]
            .to_numpy()
            .sum()
        )
        == len(series_base) - 1
    ),
    detalhe=(
        f"{int(transicoes_regime[ORDEM_REGIMES].to_numpy().sum())} "
        "transições"
    ),
)


adicionar_validacao(
    nome="Episódios cobrem todo o período",
    aprovado=(
        int(
            episodios_regime[
                "quantidade_meses"
            ].sum()
        )
        == len(series_base)
    ),
    detalhe=(
        f"{int(episodios_regime['quantidade_meses'].sum())} "
        "meses"
    ),
)


adicionar_validacao(
    nome="Cinco piores meses identificados",
    aprovado=(
        len(piores_meses)
        == QUANTIDADE_MESES_ESTRESSE
    ),
    detalhe=(
        f"{len(piores_meses)} meses"
    ),
)


adicionar_validacao(
    nome="Cinco melhores meses identificados",
    aprovado=(
        len(melhores_meses)
        == QUANTIDADE_MESES_ESTRESSE
    ),
    detalhe=(
        f"{len(melhores_meses)} meses"
    ),
)


adicionar_validacao(
    nome="Resumo sem valores ausentes",
    aprovado=(
        not resumo_estabilidade[
            "valor"
        ].isna().any()
    ),
    detalhe=(
        f"{int(resumo_estabilidade['valor'].isna().sum())} "
        "valores ausentes"
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


if (
    tabela_validacoes["status"]
    .eq("REPROVADO")
    .any()
):

    raise ValueError(
        "Uma ou mais validações da Etapa 4 "
        "foram reprovadas:\n\n"
        f"{tabela_validacoes}"
    )


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

ARQUIVOS_ESPERADOS = [
    ARQUIVO_SERIES_ROLLING,
    ARQUIVO_SUBPERIODOS,
    ARQUIVO_SUBPERIODOS_FORMATADO,
    ARQUIVO_PIORES_MESES,
    ARQUIVO_MELHORES_MESES,
    ARQUIVO_TRANSICOES,
    ARQUIVO_EPISODIOS,
    ARQUIVO_RESUMO_ESTABILIDADE,
    ARQUIVO_CONCLUSOES,
    ARQUIVO_VALIDACOES,
    ARQUIVO_GRAFICO_ROLLING,
    ARQUIVO_GRAFICO_EXCESSO,
    ARQUIVO_GRAFICO_VOLATILIDADE,
    ARQUIVO_GRAFICO_SEMESTRAL,
    ARQUIVO_GRAFICO_ESTRESSE,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in ARQUIVOS_ESPERADOS
    if not arquivo.exists()
]


if arquivos_nao_salvos:

    raise FileNotFoundError(
        "Alguns arquivos da Etapa 4 "
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
print("ETAPA 4 — ESTABILIDADE TEMPORAL CONCLUÍDA")
print("=" * 70)


print(
    f"\nPeríodo analisado: "
    f"{series_base['data'].min():%d/%m/%Y} "
    f"a "
    f"{series_base['data'].max():%d/%m/%Y}"
)


print(
    f"Quantidade de meses: "
    f"{len(series_base)}"
)


print(
    f"\nJanelas rolling de 12 meses: "
    f"{len(rolling_12m_validos)}"
)


print(
    f"- Acima do benchmark: "
    f"{PROPORCAO_ROLLING_SUPERA_BENCHMARK:.2%}"
)


print(
    f"- Acima do challenger: "
    f"{PROPORCAO_ROLLING_SUPERA_CHALLENGER:.2%}"
)


print(
    f"- Acima do CDI: "
    f"{PROPORCAO_ROLLING_SUPERA_CDI:.2%}"
)


print(
    f"- Pior excesso contra o benchmark: "
    f"{PIOR_EXCESSO_ROLLING_BENCHMARK:.2%}"
)


print(
    f"- Melhor excesso contra o benchmark: "
    f"{MELHOR_EXCESSO_ROLLING_BENCHMARK:.2%}"
)


print(
    f"- Excesso atual contra o benchmark: "
    f"{EXCESSO_ROLLING_ATUAL_BENCHMARK:.2%}"
)


print(
    f"\nPeríodos anuais acima do benchmark: "
    f"{ANOS_ACIMA_BENCHMARK}/"
    f"{QUANTIDADE_ANOS}"
)


print(
    f"Períodos semestrais acima do benchmark: "
    f"{SEMESTRES_ACIMA_BENCHMARK}/"
    f"{QUANTIDADE_SEMESTRES}"
)


print(
    f"\nMudanças de regime: "
    f"{QUANTIDADE_MUDANCAS_REGIME}"
)


print(
    f"Episódios de regime: "
    f"{len(episodios_regime)}"
)


print(
    f"Duração média dos episódios: "
    f"{DURACAO_MEDIA_REGIME:.2f} meses"
)


print(
    f"Episódio mais longo: "
    f"{episodio_mais_longo['nome_regime']} "
    f"— {DURACAO_MAXIMA_REGIME} meses"
)


print(
    f"\nPior mês: "
    f"{pior_mes['data']:%m/%Y}"
)


print(
    f"- Retorno oficial: "
    f"{pior_mes['retorno_modelo_oficial']:.2%}"
)


print(
    f"- Retorno benchmark: "
    f"{pior_mes['retorno_benchmark']:.2%}"
)


print(
    f"- Excesso contra benchmark: "
    f"{pior_mes['excesso_vs_benchmark']:.2%}"
)


print(
    f"\nMelhor mês: "
    f"{melhor_mes['data']:%m/%Y}"
)


print(
    f"- Retorno oficial: "
    f"{melhor_mes['retorno_modelo_oficial']:.2%}"
)


print(
    "\nResumo da estabilidade:"
)


display(
    resumo_estabilidade
)


print(
    "\nResultados por subperíodo:"
)


display(
    resultados_subperiodos_formatado
)


print(
    "\nCinco piores meses:"
)


display(
    piores_meses
)


print(
    "\nEpisódios de regime:"
)


display(
    episodios_regime
)


print(
    "\nConclusões:"
)


display(
    conclusoes
)


print(
    "\nValidações:"
)


display(
    tabela_validacoes
)

# ###########################################################################
# ETAPA 05 — CÓDIGO CONSOLIDADO DO ANTIGO NOTEBOOK
# ###########################################################################

# ============================================================
# ETAPA 5 — SÍNTESE EXECUTIVA E LIMITES DAS CONCLUSÕES
# SCRIPT 07 — ANÁLISE DOS RESULTADOS FINAIS
# VERSÃO AUTÔNOMA
#
# IMPORTANTE:
# As validações desta célula verificam integridade técnica.
# Elas não representam aprovação metodológica do modelo.
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter


# ============================================================
# CONFIGURAÇÕES
# ============================================================

CENARIO_OFICIAL = CENARIO_OFICIAL_JSON
CENARIO_FIXO = "MODELO_FIXO_CELULA_9"
CENARIO_CHALLENGER = CENARIO_CHALLENGER_JSON
CENARIO_BENCHMARK = "BENCHMARK_5_ATIVOS"
CENARIO_ESTATICO = "CARTEIRA_ESTATICA"
CENARIO_CDI = "CDI_100"

CENARIOS_EXECUTIVOS = [
    CENARIO_OFICIAL,
    CENARIO_FIXO,
    CENARIO_CHALLENGER,
    CENARIO_BENCHMARK,
    CENARIO_ESTATICO,
    CENARIO_CDI,
]

ROTULOS = {
    CENARIO_OFICIAL: (
        f"Modelo oficial — {MODELO_OFICIAL}"
    ),
    CENARIO_FIXO: (
        "Modelo fixo com CDI"
    ),
    CENARIO_CHALLENGER: (
        f"Challenger — {MODELO_CHALLENGER}"
    ),
    CENARIO_BENCHMARK: (
        "Benchmark de cinco ativos"
    ),
    CENARIO_ESTATICO: (
        "Carteira estática"
    ),
    CENARIO_CDI: (
        "100% CDI"
    ),
}

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
        / "outputs"
        / "tabelas"
        / "07_04_validacoes.csv"
    )

    if arquivo_teste.exists():

        RAIZ_PROJETO = diretorio
        break


if RAIZ_PROJETO is None:

    raise FileNotFoundError(
        "Não foi possível localizar a raiz do projeto.\n"
        "O arquivo outputs/tabelas/"
        "07_04_validacoes.csv não foi encontrado."
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

ARQUIVO_VALIDACOES_CELULA_4 = (
    PASTA_TABELAS
    / "07_04_validacoes.csv"
)

ARQUIVO_COMPARACAO_MODELOS = (
    PASTA_TABELAS
    / "07_02_comparacao_desempenho_risco.csv"
)

ARQUIVO_RESULTADOS_ANUAIS = (
    PASTA_TABELAS
    / "07_02_resultados_anuais.csv"
)

ARQUIVO_DESEMPENHO_REGIMES = (
    PASTA_TABELAS
    / "07_03_desempenho_por_regime.csv"
)

ARQUIVO_CONTRIBUICAO_ATIVOS = (
    PASTA_TABELAS
    / "07_03_contribuicao_total_ativos.csv"
)

ARQUIVO_RESUMO_ESTABILIDADE = (
    PASTA_TABELAS
    / "07_04_resumo_estabilidade.csv"
)

ARQUIVO_PIORES_MESES = (
    PASTA_TABELAS
    / "07_04_piores_meses.csv"
)

ARQUIVO_EPISODIOS_REGIME = (
    PASTA_TABELAS
    / "07_04_episodios_regime.csv"
)

ARQUIVO_SERIES_ROLLING = (
    PASTA_TABELAS
    / "07_04_series_rolling.csv"
)

ARQUIVO_LIMITACOES_ORIGINAIS = (
    PASTA_TABELAS
    / "06_12_limitacoes_metodologicas.csv"
)

ARQUIVO_DECISAO_ORIGINAL = (
    PASTA_TABELAS
    / "06_12_decisao_final_modelo.csv"
)

ARQUIVO_PESOS_OFICIAIS = (
    PASTA_TABELAS
    / "06_12_pesos_oficiais_atuais.csv"
)


ARQUIVOS_ENTRADA = [
    ARQUIVO_VALIDACOES_CELULA_4,
    ARQUIVO_COMPARACAO_MODELOS,
    ARQUIVO_RESULTADOS_ANUAIS,
    ARQUIVO_DESEMPENHO_REGIMES,
    ARQUIVO_CONTRIBUICAO_ATIVOS,
    ARQUIVO_RESUMO_ESTABILIDADE,
    ARQUIVO_PIORES_MESES,
    ARQUIVO_EPISODIOS_REGIME,
    ARQUIVO_SERIES_ROLLING,
    ARQUIVO_LIMITACOES_ORIGINAIS,
    ARQUIVO_DECISAO_ORIGINAL,
    ARQUIVO_PESOS_OFICIAIS,
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
            str(arquivo)
            for arquivo in arquivos_ausentes
        )
    )


# ============================================================
# ARQUIVOS DE SAÍDA
# ============================================================

ARQUIVO_SCORECARD = (
    PASTA_TABELAS
    / "07_05_scorecard_executivo.csv"
)

ARQUIVO_SCORECARD_FORMATADO = (
    PASTA_TABELAS
    / "07_05_scorecard_executivo_formatado.csv"
)

ARQUIVO_MATRIZ_EVIDENCIAS = (
    PASTA_TABELAS
    / "07_05_matriz_evidencias.csv"
)

ARQUIVO_LIMITES_CONCLUSOES = (
    PASTA_TABELAS
    / "07_05_limites_das_conclusoes.csv"
)

ARQUIVO_PONTOS_FORTES = (
    PASTA_TABELAS
    / "07_05_pontos_fortes.csv"
)

ARQUIVO_PONTOS_ATENCAO = (
    PASTA_TABELAS
    / "07_05_pontos_atencao.csv"
)

ARQUIVO_RESUMO_NARRATIVO = (
    PASTA_TABELAS
    / "07_05_resumo_narrativo_relatorio.csv"
)

ARQUIVO_RESUMO_EXECUTIVO = (
    PASTA_TABELAS
    / "07_05_resumo_executivo.csv"
)

ARQUIVO_VALIDACOES = (
    PASTA_TABELAS
    / "07_05_validacoes_tecnicas.csv"
)

ARQUIVO_GRAFICO_RISCO_RETORNO = (
    PASTA_GRAFICOS
    / "07_05_risco_retorno_executivo.png"
)

ARQUIVO_GRAFICO_CONSISTENCIA = (
    PASTA_GRAFICOS
    / "07_05_consistencia_temporal.png"
)

ARQUIVO_GRAFICO_COBERTURA = (
    PASTA_GRAFICOS
    / "07_05_cobertura_dos_regimes.png"
)

ARQUIVO_GRAFICO_INDICES = (
    PASTA_GRAFICOS
    / "07_05_indices_finais.png"
)


# ============================================================
# CARREGAMENTO
# ============================================================

validacoes_celula_4 = pd.read_csv(
    ARQUIVO_VALIDACOES_CELULA_4,
    encoding="utf-8-sig",
)

comparacao_modelos = pd.read_csv(
    ARQUIVO_COMPARACAO_MODELOS,
    encoding="utf-8-sig",
)

resultados_anuais = pd.read_csv(
    ARQUIVO_RESULTADOS_ANUAIS,
    encoding="utf-8-sig",
)

desempenho_regimes = pd.read_csv(
    ARQUIVO_DESEMPENHO_REGIMES,
    encoding="utf-8-sig",
)

contribuicao_ativos = pd.read_csv(
    ARQUIVO_CONTRIBUICAO_ATIVOS,
    encoding="utf-8-sig",
)

resumo_estabilidade = pd.read_csv(
    ARQUIVO_RESUMO_ESTABILIDADE,
    encoding="utf-8-sig",
)

piores_meses = pd.read_csv(
    ARQUIVO_PIORES_MESES,
    encoding="utf-8-sig",
)

episodios_regime = pd.read_csv(
    ARQUIVO_EPISODIOS_REGIME,
    encoding="utf-8-sig",
)

series_rolling = pd.read_csv(
    ARQUIVO_SERIES_ROLLING,
    encoding="utf-8-sig",
)

limitacoes_originais = pd.read_csv(
    ARQUIVO_LIMITACOES_ORIGINAIS,
    encoding="utf-8-sig",
)

decisao_original = pd.read_csv(
    ARQUIVO_DECISAO_ORIGINAL,
    encoding="utf-8-sig",
)

pesos_oficiais = pd.read_csv(
    ARQUIVO_PESOS_OFICIAIS,
    encoding="utf-8-sig",
)


# ============================================================
# VALIDAÇÃO DA ETAPA ANTERIOR
# ============================================================

if not {
    "validacao",
    "status",
    "detalhe",
}.issubset(
    validacoes_celula_4.columns
):

    raise ValueError(
        "O arquivo de validações da Etapa 4 "
        "possui estrutura inválida."
    )


if (
    validacoes_celula_4[
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
        "A Etapa 4 possui validações técnicas reprovadas."
    )


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def converter_float(
    valor,
    valor_padrao=np.nan,
):

    try:

        return float(
            str(valor)
            .strip()
            .replace(
                ",",
                ".",
            )
        )

    except Exception:

        return valor_padrao


def obter_valor_resumo(
    tabela,
    nome_metrica,
):

    if not {
        "metrica",
        "valor",
    }.issubset(
        tabela.columns
    ):

        raise ValueError(
            "A tabela de resumo não possui "
            "as colunas metrica e valor."
        )

    resultado = tabela.loc[
        tabela[
            "metrica"
        ]
        .astype(str)
        .str.strip()
        .eq(
            nome_metrica
        ),
        "valor",
    ]

    if len(resultado) != 1:

        raise ValueError(
            f"A métrica '{nome_metrica}' deveria "
            "possuir exatamente uma linha."
        )

    return resultado.iloc[0]


def obter_linha_cenario(
    cenario,
):

    resultado = comparacao_modelos.loc[
        comparacao_modelos[
            "cenario"
        ]
        .astype(str)
        .eq(
            cenario
        )
    ]

    if len(resultado) != 1:

        raise ValueError(
            f"O cenário {cenario} deveria possuir "
            "exatamente uma linha."
        )

    return resultado.iloc[0]


def formatar_percentual(
    valor,
):

    if pd.isna(
        valor
    ):

        return "-"

    return f"{float(valor):.2%}"


def formatar_decimal(
    valor,
):

    if pd.isna(
        valor
    ):

        return "-"

    if np.isinf(
        float(valor)
    ):

        return "∞"

    return f"{float(valor):.2f}"


# ============================================================
# PADRONIZAÇÃO DAS DATAS
# ============================================================

for nome_base, base in {
    "piores meses": piores_meses,
    "episódios de regime": episodios_regime,
    "séries rolling": series_rolling,
}.items():

    colunas_data = [
        coluna
        for coluna in base.columns
        if (
            coluna == "data"
            or coluna.startswith(
                "data_"
            )
        )
    ]

    for coluna in colunas_data:

        base[coluna] = pd.to_datetime(
            base[coluna],
            errors="coerce",
        )

        if base[coluna].isna().any():

            raise ValueError(
                f"A base {nome_base} possui datas "
                f"inválidas na coluna {coluna}."
            )


# ============================================================
# PADRONIZAÇÃO DAS MÉTRICAS COMPARATIVAS
# ============================================================

COLUNAS_NUMERICAS_COMPARACAO = [
    "retorno_total_liquido",
    "retorno_anualizado",
    "volatilidade_anualizada",
    "retorno_volatilidade",
    "sharpe_excesso_cdi",
    "sortino_excesso_cdi",
    "calmar",
    "maximo_drawdown",
    "meses_positivos",
    "melhor_mes",
    "pior_mes",
    "turnover_total",
    "custo_acumulado_simples",
    "indice_final",
    "diferenca_indice_vs_benchmark",
    "diferenca_indice_vs_oficial",
]


colunas_ausentes = [
    coluna
    for coluna in COLUNAS_NUMERICAS_COMPARACAO
    if coluna not in comparacao_modelos.columns
]


if colunas_ausentes:

    raise ValueError(
        "Colunas ausentes na comparação dos modelos:\n"
        f"{colunas_ausentes}"
    )


for coluna in COLUNAS_NUMERICAS_COMPARACAO:

    comparacao_modelos[coluna] = pd.to_numeric(
        comparacao_modelos[coluna],
        errors="coerce",
    )


colunas_obrigatorias = [
    coluna
    for coluna in COLUNAS_NUMERICAS_COMPARACAO
    if coluna != "calmar"
]


if comparacao_modelos[
    colunas_obrigatorias
].isna().any().any():

    nulos = (
        comparacao_modelos[
            colunas_obrigatorias
        ]
        .isna()
        .sum()
    )

    nulos = nulos.loc[
        nulos > 0
    ]

    raise ValueError(
        "Existem métricas obrigatórias inválidas:\n"
        f"{nulos}"
    )


# ============================================================
# EXTRAÇÃO DOS CENÁRIOS
# ============================================================

linhas_cenarios = {
    cenario: obter_linha_cenario(
        cenario
    )
    for cenario in CENARIOS_EXECUTIVOS
}


linha_oficial = linhas_cenarios[
    CENARIO_OFICIAL
]

linha_fixo = linhas_cenarios[
    CENARIO_FIXO
]

linha_challenger = linhas_cenarios[
    CENARIO_CHALLENGER
]

linha_benchmark = linhas_cenarios[
    CENARIO_BENCHMARK
]

linha_estatico = linhas_cenarios[
    CENARIO_ESTATICO
]

linha_cdi = linhas_cenarios[
    CENARIO_CDI
]


# ============================================================
# EXTRAÇÃO DAS MÉTRICAS DE ESTABILIDADE
# ============================================================

QUANTIDADE_MESES = int(
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Quantidade de meses",
        )
    )
)


QUANTIDADE_JANELAS_12M = int(
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Quantidade de janelas rolling de 12 meses",
        )
    )
)


PROPORCAO_ROLLING_BENCHMARK = (
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Janelas de 12 meses acima do benchmark",
        )
    )
)


PROPORCAO_ROLLING_CHALLENGER = (
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Janelas de 12 meses acima do challenger",
        )
    )
)


PROPORCAO_ROLLING_CDI = (
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Janelas de 12 meses acima do CDI",
        )
    )
)


PIOR_EXCESSO_ROLLING = (
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Pior excesso rolling contra benchmark",
        )
    )
)


MELHOR_EXCESSO_ROLLING = (
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Melhor excesso rolling contra benchmark",
        )
    )
)


EXCESSO_ROLLING_ATUAL = (
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Excesso rolling atual contra benchmark",
        )
    )
)


ANOS_ACIMA_BENCHMARK = int(
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Períodos anuais acima do benchmark",
        )
    )
)


QUANTIDADE_ANOS = int(
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Quantidade de períodos anuais",
        )
    )
)


SEMESTRES_ACIMA_BENCHMARK = int(
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Períodos semestrais acima do benchmark",
        )
    )
)


QUANTIDADE_SEMESTRES = int(
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Quantidade de períodos semestrais",
        )
    )
)


QUANTIDADE_MUDANCAS_REGIME = int(
    converter_float(
        obter_valor_resumo(
            resumo_estabilidade,
            "Quantidade de mudanças de regime",
        )
    )
)


# ============================================================
# ANÁLISE DE COBERTURA DOS REGIMES
# ============================================================

if not {
    "regime",
    "nome_regime",
    "quantidade_meses",
    "proporcao_periodo",
    "retorno_total_oficial",
    "excesso_oficial_vs_benchmark",
}.issubset(
    desempenho_regimes.columns
):

    raise ValueError(
        "A tabela de desempenho por regime "
        "possui estrutura inválida."
    )


COLUNAS_NUMERICAS_REGIMES = [
    "quantidade_meses",
    "proporcao_periodo",
    "retorno_total_oficial",
    "excesso_oficial_vs_benchmark",
]


for coluna in COLUNAS_NUMERICAS_REGIMES:

    desempenho_regimes[coluna] = pd.to_numeric(
        desempenho_regimes[coluna],
        errors="coerce",
    )


if desempenho_regimes[
    [
        "quantidade_meses",
        "proporcao_periodo",
    ]
].isna().any().any():

    raise ValueError(
        "Existem frequências de regime inválidas."
    )


REGIMES_PRESENTES = int(
    desempenho_regimes[
        "quantidade_meses"
    ]
    .gt(0)
    .sum()
)


REGIMES_AUSENTES = (
    desempenho_regimes.loc[
        desempenho_regimes[
            "quantidade_meses"
        ]
        .eq(0),
        "nome_regime",
    ]
    .astype(str)
    .tolist()
)


desempenho_regimes_ordenado = (
    desempenho_regimes
    .sort_values(
        "quantidade_meses",
        ascending=False,
    )
    .reset_index(
        drop=True
    )
)


CONCENTRACAO_DOIS_REGIMES = float(
    desempenho_regimes_ordenado[
        "quantidade_meses"
    ]
    .head(2)
    .sum()
    / QUANTIDADE_MESES
)


regimes_com_dados = (
    desempenho_regimes.loc[
        desempenho_regimes[
            "quantidade_meses"
        ]
        .gt(0)
    ]
    .copy()
)


regime_melhor_excesso = (
    regimes_com_dados.loc[
        regimes_com_dados[
            "excesso_oficial_vs_benchmark"
        ]
        .idxmax()
    ]
)


regime_pior_excesso = (
    regimes_com_dados.loc[
        regimes_com_dados[
            "excesso_oficial_vs_benchmark"
        ]
        .idxmin()
    ]
)


# ============================================================
# CONTRIBUIÇÃO DOS ATIVOS
# ============================================================

if not {
    "ativo",
    "contribuicao_bruta_simples",
}.issubset(
    contribuicao_ativos.columns
):

    raise ValueError(
        "A tabela de contribuição dos ativos "
        "possui estrutura inválida."
    )


contribuicao_ativos[
    "contribuicao_bruta_simples"
] = pd.to_numeric(
    contribuicao_ativos[
        "contribuicao_bruta_simples"
    ],
    errors="coerce",
)


if contribuicao_ativos[
    "contribuicao_bruta_simples"
].isna().any():

    raise ValueError(
        "Existem contribuições de ativos inválidas."
    )


ativo_maior_contribuicao = (
    contribuicao_ativos.loc[
        contribuicao_ativos[
            "contribuicao_bruta_simples"
        ]
        .idxmax()
    ]
)


ativo_menor_contribuicao = (
    contribuicao_ativos.loc[
        contribuicao_ativos[
            "contribuicao_bruta_simples"
        ]
        .idxmin()
    ]
)


# ============================================================
# SCORECARD EXECUTIVO
# ============================================================

scorecard = pd.DataFrame(
    [
        {
            "cenario": cenario,
            "modelo": ROTULOS[cenario],
            "retorno_total": float(
                linhas_cenarios[
                    cenario
                ][
                    "retorno_total_liquido"
                ]
            ),
            "retorno_anualizado": float(
                linhas_cenarios[
                    cenario
                ][
                    "retorno_anualizado"
                ]
            ),
            "volatilidade_anualizada": float(
                linhas_cenarios[
                    cenario
                ][
                    "volatilidade_anualizada"
                ]
            ),
            "retorno_volatilidade": float(
                linhas_cenarios[
                    cenario
                ][
                    "retorno_volatilidade"
                ]
            ),
            "sharpe_excesso_cdi": float(
                linhas_cenarios[
                    cenario
                ][
                    "sharpe_excesso_cdi"
                ]
            ),
            "sortino_excesso_cdi": float(
                linhas_cenarios[
                    cenario
                ][
                    "sortino_excesso_cdi"
                ]
            ),
            "calmar": (
                float(
                    linhas_cenarios[
                        cenario
                    ][
                        "calmar"
                    ]
                )
                if pd.notna(
                    linhas_cenarios[
                        cenario
                    ][
                        "calmar"
                    ]
                )
                else np.nan
            ),
            "maximo_drawdown": float(
                linhas_cenarios[
                    cenario
                ][
                    "maximo_drawdown"
                ]
            ),
            "turnover_total": float(
                linhas_cenarios[
                    cenario
                ][
                    "turnover_total"
                ]
            ),
            "indice_final": float(
                linhas_cenarios[
                    cenario
                ][
                    "indice_final"
                ]
            ),
            "diferenca_indice_vs_benchmark": (
                float(
                    linhas_cenarios[
                        cenario
                    ][
                        "indice_final"
                    ]
                )
                - float(
                    linha_benchmark[
                        "indice_final"
                    ]
                )
            ),
            "diferenca_indice_vs_oficial": (
                float(
                    linhas_cenarios[
                        cenario
                    ][
                        "indice_final"
                    ]
                )
                - float(
                    linha_oficial[
                        "indice_final"
                    ]
                )
            ),
        }
        for cenario in CENARIOS_EXECUTIVOS
    ]
)


scorecard_formatado = (
    scorecard
    .copy()
    .astype(object)
)


for coluna in [
    "retorno_total",
    "retorno_anualizado",
    "volatilidade_anualizada",
    "maximo_drawdown",
]:

    scorecard_formatado[coluna] = (
        scorecard[coluna]
        .map(
            formatar_percentual
        )
    )


for coluna in [
    "retorno_volatilidade",
    "sharpe_excesso_cdi",
    "sortino_excesso_cdi",
    "calmar",
    "turnover_total",
    "indice_final",
    "diferenca_indice_vs_benchmark",
    "diferenca_indice_vs_oficial",
]:

    scorecard_formatado[coluna] = (
        scorecard[coluna]
        .map(
            formatar_decimal
        )
    )


# ============================================================
# MATRIZ DE EVIDÊNCIAS
# ============================================================

EXCESSO_INDICE_BENCHMARK = (
    float(
        linha_oficial[
            "indice_final"
        ]
    )
    - float(
        linha_benchmark[
            "indice_final"
        ]
    )
)


DIFERENCA_INDICE_CHALLENGER = (
    float(
        linha_oficial[
            "indice_final"
        ]
    )
    - float(
        linha_challenger[
            "indice_final"
        ]
    )
)


DIFERENCA_INDICE_ESTATICO = (
    float(
        linha_oficial[
            "indice_final"
        ]
    )
    - float(
        linha_estatico[
            "indice_final"
        ]
    )
)


DIFERENCA_INDICE_CDI = (
    float(
        linha_oficial[
            "indice_final"
        ]
    )
    - float(
        linha_cdi[
            "indice_final"
        ]
    )
)


matriz_evidencias = pd.DataFrame(
    [
        {
            "dimensao": "Retorno total",
            "evidencia": (
                "O modelo oficial terminou acima "
                "do benchmark."
            ),
            "valor": EXCESSO_INDICE_BENCHMARK,
            "unidade": "pontos de índice",
            "leitura": "FAVORÁVEL",
            "forca_da_evidencia": "LIMITADA",
            "motivo_cautela": (
                f"A avaliação contém {QUANTIDADE_MESES} meses."
            ),
        },
        {
            "dimensao": "Comparação com challenger",
            "evidencia": (
                "O challenger sem CDI apresentou "
                "maior retorno absoluto."
            ),
            "valor": DIFERENCA_INDICE_CHALLENGER,
            "unidade": "pontos de índice",
            "leitura": "DESFAVORÁVEL",
            "forca_da_evidencia": "MODERADA",
            "motivo_cautela": (
                "Os modelos possuem propostas de risco diferentes."
            ),
        },
        {
            "dimensao": "Alocação dinâmica",
            "evidencia": (
                "O modelo oficial terminou acima "
                "da carteira estática."
            ),
            "valor": DIFERENCA_INDICE_ESTATICO,
            "unidade": "pontos de índice",
            "leitura": "FAVORÁVEL",
            "forca_da_evidencia": "LIMITADA",
            "motivo_cautela": (
                "O resultado pode depender da composição "
                "e do período analisado."
            ),
        },
        {
            "dimensao": "Retorno sobre CDI",
            "evidencia": (
                "O modelo oficial terminou acima "
                "da carteira de 100% CDI."
            ),
            "valor": DIFERENCA_INDICE_CDI,
            "unidade": "pontos de índice",
            "leitura": "FAVORÁVEL",
            "forca_da_evidencia": "MODERADA",
            "motivo_cautela": (
                "O modelo assume risco superior ao CDI."
            ),
        },
        {
            "dimensao": "Consistência rolling",
            "evidencia": (
                "O modelo superou o benchmark em "
                f"{PROPORCAO_ROLLING_BENCHMARK:.2%} "
                "das janelas de 12 meses."
            ),
            "valor": PROPORCAO_ROLLING_BENCHMARK,
            "unidade": "proporção",
            "leitura": "MISTA",
            "forca_da_evidencia": "MODERADA",
            "motivo_cautela": (
                "Um terço das janelas ficou abaixo "
                "do benchmark."
            ),
        },
        {
            "dimensao": "Consistência contra challenger",
            "evidencia": (
                "O modelo oficial superou o challenger em "
                f"{PROPORCAO_ROLLING_CHALLENGER:.2%} "
                "das janelas de 12 meses."
            ),
            "valor": PROPORCAO_ROLLING_CHALLENGER,
            "unidade": "proporção",
            "leitura": "DESFAVORÁVEL",
            "forca_da_evidencia": "MODERADA",
            "motivo_cautela": (
                "O modelo oficial tem objetivo mais defensivo."
            ),
        },
        {
            "dimensao": "Consistência anual",
            "evidencia": (
                f"O modelo superou o benchmark em "
                f"{ANOS_ACIMA_BENCHMARK} de "
                f"{QUANTIDADE_ANOS} períodos anuais."
            ),
            "valor": (
                ANOS_ACIMA_BENCHMARK
                / QUANTIDADE_ANOS
            ),
            "unidade": "proporção",
            "leitura": "MISTA",
            "forca_da_evidencia": "LIMITADA",
            "motivo_cautela": (
                f"Existem {QUANTIDADE_ANOS} períodos anuais, "
                "e o último pode ser parcial."
            ),
        },
        {
            "dimensao": "Consistência semestral",
            "evidencia": (
                f"O modelo superou o benchmark em "
                f"{SEMESTRES_ACIMA_BENCHMARK} de "
                f"{QUANTIDADE_SEMESTRES} semestres."
            ),
            "valor": (
                SEMESTRES_ACIMA_BENCHMARK
                / QUANTIDADE_SEMESTRES
            ),
            "unidade": "proporção",
            "leitura": "MISTA",
            "forca_da_evidencia": "LIMITADA",
            "motivo_cautela": (
                "O último semestre é parcial."
            ),
        },
        {
            "dimensao": "Risco",
            "evidencia": (
                "O modelo apresentou drawdown máximo "
                f"de {float(linha_oficial['maximo_drawdown']):.2%}."
            ),
            "valor": float(
                linha_oficial[
                    "maximo_drawdown"
                ]
            ),
            "unidade": "drawdown",
            "leitura": "FAVORÁVEL",
            "forca_da_evidencia": "LIMITADA",
            "motivo_cautela": (
                "O período pode não conter todos os tipos "
                "de crise relevantes."
            ),
        },
        {
            "dimensao": "Cobertura de regimes",
            "evidencia": (
                f"Foram observados {REGIMES_PRESENTES} "
                "dos quatro regimes."
            ),
            "valor": (
                REGIMES_PRESENTES
                / len(
                    ORDEM_REGIMES
                )
            ),
            "unidade": "proporção dos regimes",
            "leitura": "INCOMPLETA",
            "forca_da_evidencia": "FRACA",
            "motivo_cautela": (
                "Não houve observações de "
                + ", ".join(
                    REGIMES_AUSENTES
                )
                + "."
                if REGIMES_AUSENTES
                else "Todos os regimes foram observados."
            ),
        },
        {
            "dimensao": "Concentração temporal",
            "evidencia": (
                "Os dois regimes mais frequentes representam "
                f"{CONCENTRACAO_DOIS_REGIMES:.2%} "
                "da avaliação."
            ),
            "valor": CONCENTRACAO_DOIS_REGIMES,
            "unidade": "proporção",
            "leitura": "CONCENTRADA",
            "forca_da_evidencia": "FRACA",
            "motivo_cautela": (
                "O desempenho pode estar condicionado "
                "a poucos ambientes macroeconômicos."
            ),
        },
        {
            "dimensao": "Pior janela rolling",
            "evidencia": (
                "A pior janela de 12 meses ficou "
                f"{PIOR_EXCESSO_ROLLING:.2%} "
                "abaixo do benchmark."
            ),
            "valor": PIOR_EXCESSO_ROLLING,
            "unidade": "excesso de retorno",
            "leitura": "DESFAVORÁVEL",
            "forca_da_evidencia": "MODERADA",
            "motivo_cautela": (
                "O desempenho relativo não foi positivo "
                "em todas as janelas."
            ),
        },
    ]
)


# ============================================================
# LIMITES DAS CONCLUSÕES
# ============================================================

limites_conclusoes = pd.DataFrame(
    [
        {
            "afirmacao": (
                "O modelo superou o benchmark no período avaliado."
            ),
            "nivel_suporte": "SUPORTADA",
            "base": (
                f"Índice oficial "
                f"{float(linha_oficial['indice_final']):.2f} "
                f"contra "
                f"{float(linha_benchmark['indice_final']):.2f}."
            ),
            "pode_ser_usada_no_relatorio": "SIM",
        },
        {
            "afirmacao": (
                "O modelo foi superior ao benchmark "
                "em todos os momentos."
            ),
            "nivel_suporte": "NÃO SUPORTADA",
            "base": (
                f"Somente "
                f"{PROPORCAO_ROLLING_BENCHMARK:.2%} "
                "das janelas de 12 meses foram superiores."
            ),
            "pode_ser_usada_no_relatorio": "NÃO",
        },
        {
            "afirmacao": (
                "O modelo possui maior retorno que "
                "o challenger sem CDI."
            ),
            "nivel_suporte": "NÃO SUPORTADA",
            "base": (
                f"Modelo oficial ficou "
                f"{abs(DIFERENCA_INDICE_CHALLENGER):.2f} "
                "pontos abaixo do challenger."
            ),
            "pode_ser_usada_no_relatorio": "NÃO",
        },
        {
            "afirmacao": (
                "A inclusão do CDI produziu um perfil "
                "mais defensivo."
            ),
            "nivel_suporte": "PARCIALMENTE SUPORTADA",
            "base": (
                "O modelo oficial apresentou baixa "
                "volatilidade e drawdown, mas a causalidade "
                "não foi isolada completamente."
            ),
            "pode_ser_usada_no_relatorio": (
                "SIM, COM RESSALVA"
            ),
        },
        {
            "afirmacao": (
                "O modelo funciona em estagflação."
            ),
            "nivel_suporte": "NÃO AVALIADA",
            "base": (
                "Não houve meses de estagflação "
                "no período de avaliação."
            ),
            "pode_ser_usada_no_relatorio": "NÃO",
        },
        {
            "afirmacao": (
                "O modelo funciona em recessão "
                "desinflacionária."
            ),
            "nivel_suporte": "EVIDÊNCIA INSUFICIENTE",
            "base": (
                "Foram observados somente três meses "
                "nesse regime."
            ),
            "pode_ser_usada_no_relatorio": (
                "SIM, COMO OBSERVAÇÃO"
            ),
        },
        {
            "afirmacao": (
                "O modelo continuará superando o benchmark "
                "no futuro."
            ),
            "nivel_suporte": "NÃO SUPORTADA",
            "base": (
                "Resultados históricos não garantem "
                "desempenho futuro."
            ),
            "pode_ser_usada_no_relatorio": "NÃO",
        },
        {
            "afirmacao": (
                "O período de avaliação é um holdout "
                "final intocado."
            ),
            "nivel_suporte": "NÃO SUPORTADA",
            "base": (
                "Esse período foi analisado durante "
                "o desenvolvimento e a escolha final."
            ),
            "pode_ser_usada_no_relatorio": "NÃO",
        },
        {
            "afirmacao": (
                "O modelo apresenta evidência inicial "
                "favorável, mas ainda não conclusiva."
            ),
            "nivel_suporte": "SUPORTADA",
            "base": (
                "Resultado total positivo contra o benchmark, "
                "porém com amostra curta, cobertura incompleta "
                "de regimes e consistência temporal parcial."
            ),
            "pode_ser_usada_no_relatorio": "SIM",
        },
    ]
)


# ============================================================
# PONTOS FORTES
# ============================================================

pontos_fortes = pd.DataFrame(
    [
        {
            "ordem": 1,
            "ponto_forte": (
                "Superação do benchmark no resultado acumulado"
            ),
            "evidencia": (
                f"Vantagem de "
                f"{EXCESSO_INDICE_BENCHMARK:.2f} "
                "ponto de índice."
            ),
        },
        {
            "ordem": 2,
            "ponto_forte": (
                "Resultado superior à carteira estática"
            ),
            "evidencia": (
                f"Vantagem de "
                f"{DIFERENCA_INDICE_ESTATICO:.2f} "
                "pontos de índice."
            ),
        },
        {
            "ordem": 3,
            "ponto_forte": (
                "Retorno ajustado ao risco positivo"
            ),
            "evidencia": (
                f"Retorno/volatilidade de "
                f"{float(linha_oficial['retorno_volatilidade']):.2f} "
                f"e Sharpe sobre CDI de "
                f"{float(linha_oficial['sharpe_excesso_cdi']):.2f}."
            ),
        },
        {
            "ordem": 4,
            "ponto_forte": (
                "Drawdown controlado na avaliação"
            ),
            "evidencia": (
                f"Máximo drawdown de "
                f"{float(linha_oficial['maximo_drawdown']):.2%}."
            ),
        },
        {
            "ordem": 5,
            "ponto_forte": (
                "Desempenho acima do CDI"
            ),
            "evidencia": (
                f"Vantagem de "
                f"{DIFERENCA_INDICE_CDI:.2f} "
                "pontos de índice."
            ),
        },
        {
            "ordem": 6,
            "ponto_forte": (
                "Diversificação das contribuições"
            ),
            "evidencia": (
                f"Principal contribuição: "
                f"{ativo_maior_contribuicao['ativo']} "
                f"com "
                f"{float(ativo_maior_contribuicao['contribuicao_bruta_simples']):.2%}."
            ),
        },
    ]
)


# ============================================================
# PONTOS DE ATENÇÃO
# ============================================================

pontos_atencao = pd.DataFrame(
    [
        {
            "ordem": 1,
            "ponto_atencao": (
                "Período de avaliação curto"
            ),
            "evidencia": (
                f"A avaliação possui somente "
                f"{QUANTIDADE_MESES} meses."
            ),
            "impacto": "ALTO",
        },
        {
            "ordem": 2,
            "ponto_atencao": (
                "Cobertura incompleta dos regimes"
            ),
            "evidencia": (
                f"Foram observados somente "
                f"{REGIMES_PRESENTES} dos quatro regimes."
            ),
            "impacto": "ALTO",
        },
        {
            "ordem": 3,
            "ponto_atencao": (
                "Ausência de estagflação na avaliação"
            ),
            "evidencia": (
                "Não existem observações fora da amostra "
                "para esse regime."
            ),
            "impacto": "ALTO",
        },
        {
            "ordem": 4,
            "ponto_atencao": (
                "Baixa superioridade contra o challenger"
            ),
            "evidencia": (
                f"O modelo oficial superou o challenger "
                f"em apenas "
                f"{PROPORCAO_ROLLING_CHALLENGER:.2%} "
                "das janelas de 12 meses."
            ),
            "impacto": "MÉDIO",
        },
        {
            "ordem": 5,
            "ponto_atencao": (
                "Consistência parcial contra o benchmark"
            ),
            "evidencia": (
                f"O modelo ficou acima do benchmark em "
                f"{PROPORCAO_ROLLING_BENCHMARK:.2%} "
                "das janelas."
            ),
            "impacto": "MÉDIO",
        },
        {
            "ordem": 6,
            "ponto_atencao": (
                "Pior janela abaixo do benchmark"
            ),
            "evidencia": (
                f"Pior excesso rolling: "
                f"{PIOR_EXCESSO_ROLLING:.2%}."
            ),
            "impacto": "MÉDIO",
        },
        {
            "ordem": 7,
            "ponto_atencao": (
                "Concentração em dois regimes"
            ),
            "evidencia": (
                f"Os dois regimes mais frequentes "
                f"representam "
                f"{CONCENTRACAO_DOIS_REGIMES:.2%} "
                "do período."
            ),
            "impacto": "ALTO",
        },
        {
            "ordem": 8,
            "ponto_atencao": (
                "Período de avaliação já inspecionado"
            ),
            "evidencia": (
                "O período de avaliação não pode mais ser tratado "
                "como teste final intocado."
            ),
            "impacto": "ALTO",
        },
        {
            "ordem": 9,
            "ponto_atencao": (
                "Resultado inferior ao challenger "
                "em retorno absoluto"
            ),
            "evidencia": (
                f"Diferença de "
                f"{DIFERENCA_INDICE_CHALLENGER:.2f} "
                "pontos de índice."
            ),
            "impacto": "MÉDIO",
        },
    ]
)


# ============================================================
# RESUMO NARRATIVO PARA O RELATÓRIO
# ============================================================

resumo_narrativo = pd.DataFrame(
    [
        {
            "secao": "Objetivo",
            "texto": (
                "Avaliar uma estratégia de alocação "
                "multimercado condicionada por regimes "
                "macroeconômicos, com inclusão do CDI "
                "como componente defensivo."
            ),
        },
        {
            "secao": "Metodologia",
            "texto": (
                "O modelo utiliza regimes macroeconômicos, "
                "rebalanceamento mensal, custos por turnover "
                "e validação walk-forward com janela expansiva."
            ),
        },
        {
            "secao": "Resultado acumulado",
            "texto": (
                f"Entre {series_rolling['data'].min():%m/%Y} e "
                f"{series_rolling['data'].max():%m/%Y}, "
                f"o modelo oficial atingiu índice final de "
                f"{float(linha_oficial['indice_final']):.2f}, "
                f"contra "
                f"{float(linha_benchmark['indice_final']):.2f} "
                "do benchmark."
            ),
        },
        {
            "secao": "Retorno e risco",
            "texto": (
                f"O retorno anualizado foi de "
                f"{float(linha_oficial['retorno_anualizado']):.2%}, "
                f"com volatilidade anualizada de "
                f"{float(linha_oficial['volatilidade_anualizada']):.2%} "
                f"e drawdown máximo de "
                f"{float(linha_oficial['maximo_drawdown']):.2%}."
            ),
        },
        {
            "secao": "Consistência temporal",
            "texto": (
                f"O modelo superou o benchmark em "
                f"{PROPORCAO_ROLLING_BENCHMARK:.2%} "
                f"das {QUANTIDADE_JANELAS_12M} janelas "
                "móveis de 12 meses."
            ),
        },
        {
            "secao": "Comparação com challenger",
            "texto": (
                f"O challenger sem CDI apresentou índice final "
                f"de {float(linha_challenger['indice_final']):.2f}, "
                "superior ao modelo oficial em retorno absoluto."
            ),
        },
        {
            "secao": "Regimes",
            "texto": (
                f"A avaliação cobriu {REGIMES_PRESENTES} "
                "dos quatro regimes, com concentração de "
                f"{CONCENTRACAO_DOIS_REGIMES:.2%} "
                "nos dois regimes mais frequentes."
            ),
        },
        {
            "secao": "Contribuição dos ativos",
            "texto": (
                f"O ativo com maior contribuição bruta simples "
                f"foi {ativo_maior_contribuicao['ativo']}, "
                f"com "
                f"{float(ativo_maior_contribuicao['contribuicao_bruta_simples']):.2%}."
            ),
        },
        {
            "secao": "Limitação principal",
            "texto": (
                "A principal limitação é a combinação entre "
                "amostra curta, ausência de estagflação e uso "
                "repetido do período de avaliação durante "
                "o desenvolvimento."
            ),
        },
        {
            "secao": "Conclusão analítica",
            "texto": (
                "Os resultados são promissores no período "
                "analisado, mas ainda não são suficientes "
                "para afirmar superioridade estrutural ou "
                "generalização futura."
            ),
        },
    ]
)


# ============================================================
# CLASSIFICAÇÃO ANALÍTICA
# ============================================================

CLASSIFICACAO_ANALITICA = (
    "RESULTADO PROMISSOR, MAS NÃO CONCLUSIVO"
)


resumo_executivo = pd.DataFrame(
    {
        "metrica": [
            "Classificação analítica",
            "Quantidade de meses",
            "Índice final oficial",
            "Índice final benchmark",
            "Índice final challenger",
            "Diferença contra benchmark",
            "Diferença contra challenger",
            "Retorno anualizado oficial",
            "Volatilidade anualizada oficial",
            "Máximo drawdown oficial",
            "Retorno/volatilidade oficial",
            "Sharpe sobre CDI",
            "Janelas acima do benchmark",
            "Janelas acima do challenger",
            "Janelas acima do CDI",
            "Anos acima do benchmark",
            "Semestres acima do benchmark",
            "Regimes presentes",
            "Regimes ausentes",
            "Concentração nos dois principais regimes",
            "Pior excesso rolling",
            "Melhor excesso rolling",
            "Excesso rolling atual",
            "Quantidade de mudanças de regime",
            "Maior contribuição de ativo",
            "Contribuição do principal ativo",
            "Conclusão principal",
        ],
        "valor": [
            CLASSIFICACAO_ANALITICA,
            QUANTIDADE_MESES,
            float(
                linha_oficial[
                    "indice_final"
                ]
            ),
            float(
                linha_benchmark[
                    "indice_final"
                ]
            ),
            float(
                linha_challenger[
                    "indice_final"
                ]
            ),
            EXCESSO_INDICE_BENCHMARK,
            DIFERENCA_INDICE_CHALLENGER,
            float(
                linha_oficial[
                    "retorno_anualizado"
                ]
            ),
            float(
                linha_oficial[
                    "volatilidade_anualizada"
                ]
            ),
            float(
                linha_oficial[
                    "maximo_drawdown"
                ]
            ),
            float(
                linha_oficial[
                    "retorno_volatilidade"
                ]
            ),
            float(
                linha_oficial[
                    "sharpe_excesso_cdi"
                ]
            ),
            PROPORCAO_ROLLING_BENCHMARK,
            PROPORCAO_ROLLING_CHALLENGER,
            PROPORCAO_ROLLING_CDI,
            (
                f"{ANOS_ACIMA_BENCHMARK}/"
                f"{QUANTIDADE_ANOS}"
            ),
            (
                f"{SEMESTRES_ACIMA_BENCHMARK}/"
                f"{QUANTIDADE_SEMESTRES}"
            ),
            REGIMES_PRESENTES,
            str(
                REGIMES_AUSENTES
            ),
            CONCENTRACAO_DOIS_REGIMES,
            PIOR_EXCESSO_ROLLING,
            MELHOR_EXCESSO_ROLLING,
            EXCESSO_ROLLING_ATUAL,
            QUANTIDADE_MUDANCAS_REGIME,
            ativo_maior_contribuicao[
                "ativo"
            ],
            float(
                ativo_maior_contribuicao[
                    "contribuicao_bruta_simples"
                ]
            ),
            (
                "O modelo apresentou evidência favorável "
                "contra o benchmark, porém com consistência "
                "parcial e cobertura incompleta dos regimes."
            ),
        ],
    }
)


# ============================================================
# SALVAMENTO DAS TABELAS
# ============================================================

scorecard.to_csv(
    ARQUIVO_SCORECARD,
    index=False,
    encoding="utf-8-sig",
)


scorecard_formatado.to_csv(
    ARQUIVO_SCORECARD_FORMATADO,
    index=False,
    encoding="utf-8-sig",
)


matriz_evidencias.to_csv(
    ARQUIVO_MATRIZ_EVIDENCIAS,
    index=False,
    encoding="utf-8-sig",
)


limites_conclusoes.to_csv(
    ARQUIVO_LIMITES_CONCLUSOES,
    index=False,
    encoding="utf-8-sig",
)


pontos_fortes.to_csv(
    ARQUIVO_PONTOS_FORTES,
    index=False,
    encoding="utf-8-sig",
)


pontos_atencao.to_csv(
    ARQUIVO_PONTOS_ATENCAO,
    index=False,
    encoding="utf-8-sig",
)


resumo_narrativo.to_csv(
    ARQUIVO_RESUMO_NARRATIVO,
    index=False,
    encoding="utf-8-sig",
)


resumo_executivo.to_csv(
    ARQUIVO_RESUMO_EXECUTIVO,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# GRÁFICO 1 — RISCO E RETORNO
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 7)
)


ax.scatter(
    scorecard[
        "volatilidade_anualizada"
    ],
    scorecard[
        "retorno_anualizado"
    ],
    s=100,
)


for _, linha in scorecard.iterrows():

    ax.annotate(
        linha[
            "modelo"
        ],
        (
            linha[
                "volatilidade_anualizada"
            ],
            linha[
                "retorno_anualizado"
            ],
        ),
        xytext=(
            7,
            7,
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
    "Síntese Executiva de Risco e Retorno"
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
# GRÁFICO 2 — CONSISTÊNCIA TEMPORAL
# ============================================================

consistencia_grafico = pd.Series(
    {
        "Rolling 12m\nvs benchmark": (
            PROPORCAO_ROLLING_BENCHMARK
        ),
        "Rolling 12m\nvs challenger": (
            PROPORCAO_ROLLING_CHALLENGER
        ),
        "Rolling 12m\nvs CDI": (
            PROPORCAO_ROLLING_CDI
        ),
        "Períodos\nanuais": (
            ANOS_ACIMA_BENCHMARK
            / QUANTIDADE_ANOS
        ),
        "Períodos\nsemestrais": (
            SEMESTRES_ACIMA_BENCHMARK
            / QUANTIDADE_SEMESTRES
        ),
    }
)


fig, ax = plt.subplots(
    figsize=(12, 7)
)


consistencia_grafico.plot(
    kind="bar",
    ax=ax,
)


ax.axhline(
    y=0.5,
    linewidth=1,
)


ax.set_ylim(
    0,
    1,
)


ax.yaxis.set_major_formatter(
    PercentFormatter(
        xmax=1.0
    )
)


ax.set_title(
    "Consistência Temporal do Modelo Oficial"
)

ax.set_xlabel(
    "Critério"
)

ax.set_ylabel(
    "Proporção favorável"
)

ax.tick_params(
    axis="x",
    rotation=0,
)

ax.grid(
    axis="y",
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_CONSISTENCIA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 3 — COBERTURA DOS REGIMES
# ============================================================

cobertura_grafico = (
    desempenho_regimes
    .set_index(
        "nome_regime"
    )[
        "quantidade_meses"
    ]
    .copy()
)


fig, ax = plt.subplots(
    figsize=(12, 7)
)


cobertura_grafico.plot(
    kind="bar",
    ax=ax,
)


ax.set_title(
    "Cobertura dos Regimes no Período de Avaliação"
)

ax.set_xlabel(
    "Regime macroeconômico"
)

ax.set_ylabel(
    "Quantidade de meses"
)

ax.tick_params(
    axis="x",
    rotation=20,
)

ax.grid(
    axis="y",
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_COBERTURA,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# GRÁFICO 4 — ÍNDICES FINAIS
# ============================================================

indices_grafico = (
    scorecard
    .set_index(
        "modelo"
    )[
        "indice_final"
    ]
)


fig, ax = plt.subplots(
    figsize=(13, 7)
)


indices_grafico.plot(
    kind="bar",
    ax=ax,
)


ax.axhline(
    y=100.0,
    linewidth=1,
)


ax.set_title(
    "Índices Finais dos Modelos"
)

ax.set_xlabel(
    "Modelo"
)

ax.set_ylabel(
    "Índice final"
)

ax.tick_params(
    axis="x",
    rotation=25,
)

ax.grid(
    axis="y",
    alpha=0.3
)


fig.tight_layout()

fig.savefig(
    ARQUIVO_GRAFICO_INDICES,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# VALIDAÇÕES TÉCNICAS
# ============================================================

validacoes = []


def adicionar_validacao(
    nome,
    correto,
    detalhe,
):

    validacoes.append(
        {
            "validacao_tecnica": nome,
            "status": (
                "OK"
                if correto
                else "ERRO"
            ),
            "detalhe": detalhe,
            "observacao": (
                "Validação de integridade técnica; "
                "não representa aprovação do modelo."
            ),
        }
    )


adicionar_validacao(
    nome="Etapa 4 sem reprovação técnica",
    correto=(
        not validacoes_celula_4[
            "status"
        ]
        .astype(str)
        .str.upper()
        .eq(
            "REPROVADO"
        )
        .any()
    ),
    detalhe=(
        f"{len(validacoes_celula_4)} "
        "verificações anteriores."
    ),
)


adicionar_validacao(
    nome="Seis cenários encontrados",
    correto=(
        scorecard[
            "cenario"
        ]
        .nunique()
        == len(
            CENARIOS_EXECUTIVOS
        )
    ),
    detalhe=(
        f"{scorecard['cenario'].nunique()} cenários."
    ),
)


adicionar_validacao(
    nome="Quantidade de meses consistente",
    correto=(
        QUANTIDADE_MESES > 0
    ),
    detalhe=(
        f"{QUANTIDADE_MESES} meses."
    ),
)


adicionar_validacao(
    nome="Quantidade de janelas consistente",
    correto=(
        QUANTIDADE_JANELAS_12M
        == 18
    ),
    detalhe=(
        f"{QUANTIDADE_JANELAS_12M} janelas."
    ),
)


adicionar_validacao(
    nome="Frequências rolling entre zero e um",
    correto=(
        0.0
        <= PROPORCAO_ROLLING_BENCHMARK
        <= 1.0
        and 0.0
        <= PROPORCAO_ROLLING_CHALLENGER
        <= 1.0
        and 0.0
        <= PROPORCAO_ROLLING_CDI
        <= 1.0
    ),
    detalhe=(
        f"Benchmark: "
        f"{PROPORCAO_ROLLING_BENCHMARK:.4f} | "
        f"Challenger: "
        f"{PROPORCAO_ROLLING_CHALLENGER:.4f} | "
        f"CDI: "
        f"{PROPORCAO_ROLLING_CDI:.4f}"
    ),
)


adicionar_validacao(
    nome="Meses dos regimes somam o período",
    correto=(
        int(
            desempenho_regimes[
                "quantidade_meses"
            ]
            .sum()
        )
        == QUANTIDADE_MESES
    ),
    detalhe=(
        f"{int(desempenho_regimes['quantidade_meses'].sum())} "
        "meses classificados."
    ),
)


adicionar_validacao(
    nome="Regimes dentro do universo esperado",
    correto=(
        set(
            desempenho_regimes[
                "regime"
            ]
            .astype(str)
        )
        .issubset(
            set(
                ORDEM_REGIMES
            )
        )
    ),
    detalhe=(
        str(
            desempenho_regimes[
                "regime"
            ]
            .astype(str)
            .tolist()
        )
    ),
)


adicionar_validacao(
    nome="Resultado oficial reproduz comparação anterior",
    correto=np.isclose(
        EXCESSO_INDICE_BENCHMARK,
        float(
            linha_oficial[
                "diferenca_indice_vs_benchmark"
            ]
        ),
        atol=1e-10,
        rtol=1e-10,
    ),
    detalhe=(
        f"Recalculado: "
        f"{EXCESSO_INDICE_BENCHMARK:.12f} | "
        f"Salvo: "
        f"{float(linha_oficial['diferenca_indice_vs_benchmark']):.12f}"
    ),
)


adicionar_validacao(
    nome="Matriz possui evidências favoráveis e limitações",
    correto=(
        matriz_evidencias[
            "leitura"
        ]
        .isin(
            [
                "FAVORÁVEL",
                "MISTA",
                "DESFAVORÁVEL",
                "INCOMPLETA",
                "CONCENTRADA",
            ]
        )
        .all()
    ),
    detalhe=(
        str(
            matriz_evidencias[
                "leitura"
            ]
            .value_counts()
            .to_dict()
        )
    ),
)


adicionar_validacao(
    nome="Limites das conclusões documentados",
    correto=(
        len(
            limites_conclusoes
        )
        >= 8
    ),
    detalhe=(
        f"{len(limites_conclusoes)} "
        "afirmações avaliadas."
    ),
)


adicionar_validacao(
    nome="Resumo narrativo completo",
    correto=(
        resumo_narrativo[
            "secao"
        ]
        .nunique()
        >= 9
    ),
    detalhe=(
        f"{resumo_narrativo['secao'].nunique()} seções."
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


if (
    tabela_validacoes[
        "status"
    ]
    .eq(
        "ERRO"
    )
    .any()
):

    raise ValueError(
        "Uma ou mais verificações técnicas "
        "da Etapa 5 apresentaram erro:\n\n"
        f"{tabela_validacoes}"
    )


# ============================================================
# VALIDAÇÃO DOS ARQUIVOS SALVOS
# ============================================================

ARQUIVOS_ESPERADOS = [
    ARQUIVO_SCORECARD,
    ARQUIVO_SCORECARD_FORMATADO,
    ARQUIVO_MATRIZ_EVIDENCIAS,
    ARQUIVO_LIMITES_CONCLUSOES,
    ARQUIVO_PONTOS_FORTES,
    ARQUIVO_PONTOS_ATENCAO,
    ARQUIVO_RESUMO_NARRATIVO,
    ARQUIVO_RESUMO_EXECUTIVO,
    ARQUIVO_VALIDACOES,
    ARQUIVO_GRAFICO_RISCO_RETORNO,
    ARQUIVO_GRAFICO_CONSISTENCIA,
    ARQUIVO_GRAFICO_COBERTURA,
    ARQUIVO_GRAFICO_INDICES,
]


arquivos_nao_salvos = [
    arquivo
    for arquivo in ARQUIVOS_ESPERADOS
    if not arquivo.exists()
]


if arquivos_nao_salvos:

    raise FileNotFoundError(
        "Alguns arquivos da Etapa 5 "
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
print("ETAPA 5 — SÍNTESE EXECUTIVA CONCLUÍDA")
print("=" * 70)


print(
    "\nATENÇÃO:"
)


print(
    "As verificações desta célula confirmam somente "
    "integridade técnica dos dados e arquivos."
)


print(
    "Elas não representam aprovação final do modelo."
)


print(
    f"\nClassificação analítica: "
    f"{CLASSIFICACAO_ANALITICA}"
)


print(
    f"\nPeríodo avaliado: "
    f"{QUANTIDADE_MESES} meses"
)


print(
    f"Regimes observados: "
    f"{REGIMES_PRESENTES}/4"
)


print(
    f"Regimes ausentes: "
    f"{REGIMES_AUSENTES}"
)


print(
    f"Concentração nos dois principais regimes: "
    f"{CONCENTRACAO_DOIS_REGIMES:.2%}"
)


print(
    "\nResultado principal:"
)


print(
    f"- Índice oficial: "
    f"{float(linha_oficial['indice_final']):.2f}"
)


print(
    f"- Índice benchmark: "
    f"{float(linha_benchmark['indice_final']):.2f}"
)


print(
    f"- Diferença: "
    f"{EXCESSO_INDICE_BENCHMARK:.2f} ponto"
)


print(
    f"- Índice challenger: "
    f"{float(linha_challenger['indice_final']):.2f}"
)


print(
    f"- Diferença contra challenger: "
    f"{DIFERENCA_INDICE_CHALLENGER:.2f} pontos"
)


print(
    "\nConsistência:"
)


print(
    f"- Rolling 12 meses contra benchmark: "
    f"{PROPORCAO_ROLLING_BENCHMARK:.2%}"
)


print(
    f"- Rolling 12 meses contra challenger: "
    f"{PROPORCAO_ROLLING_CHALLENGER:.2%}"
)


print(
    f"- Períodos anuais: "
    f"{ANOS_ACIMA_BENCHMARK}/"
    f"{QUANTIDADE_ANOS}"
)


print(
    f"- Períodos semestrais: "
    f"{SEMESTRES_ACIMA_BENCHMARK}/"
    f"{QUANTIDADE_SEMESTRES}"
)


print(
    "\nPrincipal ponto forte:"
)


print(
    f"- Vantagem contra o benchmark no resultado total: "
    f"{EXCESSO_INDICE_BENCHMARK:.2f} ponto"
)


print(
    "\nPrincipal ponto de atenção:"
)


print(
    f"- Amostra de somente "
    f"{QUANTIDADE_MESES} meses e cobertura de "
    f"{REGIMES_PRESENTES} dos quatro regimes"
)


print(
    "\nScorecard executivo:"
)


display(
    scorecard_formatado
)


print(
    "\nMatriz de evidências:"
)


display(
    matriz_evidencias
)


print(
    "\nLimites das conclusões:"
)


display(
    limites_conclusoes
)


print(
    "\nPontos fortes:"
)


display(
    pontos_fortes
)


print(
    "\nPontos de atenção:"
)


display(
    pontos_atencao
)


print(
    "\nResumo narrativo:"
)


display(
    resumo_narrativo
)


print(
    "\nVerificações técnicas:"
)


display(
    tabela_validacoes
)


FIM_EXECUCAO_UTC = datetime.now(timezone.utc)

print("=" * 80)
print("ANÁLISE DOS RESULTADOS FINAIS CONCLUÍDA")
print(
    "Duração total: "
    f"{(FIM_EXECUCAO_UTC - INICIO_EXECUCAO_UTC).total_seconds():.2f}s"
)
print("=" * 80)
