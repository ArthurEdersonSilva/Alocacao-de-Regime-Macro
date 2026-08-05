from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml


RAIZ_GLOBAL = Path(
    os.getenv(
        "PROJECT_ROOT",
        Path(__file__).resolve().parent,
    )
).resolve()

os.chdir(
    RAIZ_GLOBAL
)


ARQUIVO_CONFIG_GLOBAL = (
    RAIZ_GLOBAL
    / "config"
    / "config.yaml"
)

if ARQUIVO_CONFIG_GLOBAL.exists():

    with ARQUIVO_CONFIG_GLOBAL.open(
        mode="r",
        encoding="utf-8",
    ) as arquivo_yaml:

        CONFIGURACAO_GLOBAL = (
            yaml.safe_load(
                arquivo_yaml
            )
            or {}
        )

else:

    CONFIGURACAO_GLOBAL = {}


CONFIGURACAO_AUDITORIA = (
    CONFIGURACAO_GLOBAL.get(
        "auditoria",
        {},
    )
    if isinstance(
        CONFIGURACAO_GLOBAL,
        dict,
    )
    else {}
)


CONTINUAR_APOS_ERRO_ETAPA = bool(
    CONFIGURACAO_AUDITORIA.get(
        "continuar_apos_erro_etapa",
        True,
    )
)

FALHAR_EM_ACHADO_CRITICO = bool(
    CONFIGURACAO_AUDITORIA.get(
        "falhar_em_achado_critico",
        True,
    )
)


def display(objeto) -> None:
    """
    Exibição textual compatível com os antigos notebooks.
    """

    if hasattr(
        objeto,
        "to_string",
    ):

        try:

            print(
                objeto.to_string(
                    index=False
                )
            )

            return

        except TypeError:

            print(
                objeto.to_string()
            )

            return

    print(
        objeto
    )


INICIO_EXECUCAO_UTC = datetime.now(
    timezone.utc
)

print("=" * 80)
print("08 — AUDITORIA GLOBAL DO PROJETO")
print(f"Raiz do projeto: {RAIZ_GLOBAL}")
print("=" * 80)


def executar_etapa_01() -> None:
    from datetime import datetime

    import pandas as pd


    RAIZ_PROJETO = RAIZ_GLOBAL

    PASTA_AUDITORIA = (
        RAIZ_PROJETO
        / "outputs"
        / "auditoria"
    )

    PASTA_AUDITORIA.mkdir(
        parents=True,
        exist_ok=True,
    )

    ARQUIVO_INVENTARIO = (
        PASTA_AUDITORIA
        / "08_01_inventario_arquivos.csv"
    )

    ARQUIVO_RESUMO = (
        PASTA_AUDITORIA
        / "08_01_resumo_inventario.csv"
    )

    ARQUIVO_ESSENCIAIS = (
        PASTA_AUDITORIA
        / "08_01_verificacao_arquivos_essenciais.csv"
    )


    EXTENSOES_ANALISADAS = {
        ".csv",
        ".parquet",
        ".json",
        ".yaml",
        ".yml",
        ".png",
        ".jpg",
        ".jpeg",
        ".py",
        ".txt",
        ".pdf",
    }

    DIRETORIOS_IGNORADOS = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }


    registros_arquivos = []

    for arquivo in RAIZ_PROJETO.rglob("*"):

        if not arquivo.is_file():
            continue

        caminho_relativo = arquivo.relative_to(
            RAIZ_PROJETO
        )

        if any(
            parte in DIRETORIOS_IGNORADOS
            for parte in caminho_relativo.parts
        ):
            continue

        if arquivo.suffix.lower() not in EXTENSOES_ANALISADAS:
            continue

        estatisticas = arquivo.stat()

        parte_principal = (
            caminho_relativo.parts[0]
            if caminho_relativo.parts
            else ""
        )

        registros_arquivos.append(
            {
                "caminho_relativo": str(
                    caminho_relativo
                ),
                "nome_arquivo": arquivo.name,
                "extensao": arquivo.suffix.lower(),
                "diretorio_principal": parte_principal,
                "tamanho_bytes": estatisticas.st_size,
                "tamanho_kb": (
                    estatisticas.st_size
                    / 1024
                ),
                "tamanho_mb": (
                    estatisticas.st_size
                    / 1024
                    / 1024
                ),
                "data_modificacao": datetime.fromtimestamp(
                    estatisticas.st_mtime
                ),
                "arquivo_vazio": (
                    estatisticas.st_size == 0
                ),
            }
        )


    inventario_arquivos = pd.DataFrame(
        registros_arquivos
    )

    if inventario_arquivos.empty:
        raise RuntimeError(
            "Nenhum arquivo do projeto foi encontrado."
        )

    inventario_arquivos = (
        inventario_arquivos
        .sort_values(
            [
                "diretorio_principal",
                "caminho_relativo",
            ]
        )
        .reset_index(
            drop=True
        )
    )


    resumo_inventario = (
        inventario_arquivos
        .groupby(
            [
                "diretorio_principal",
                "extensao",
            ],
            as_index=False,
        )
        .agg(
            quantidade_arquivos=(
                "caminho_relativo",
                "size",
            ),
            tamanho_total_mb=(
                "tamanho_mb",
                "sum",
            ),
            quantidade_vazios=(
                "arquivo_vazio",
                "sum",
            ),
        )
    )

    resumo_inventario[
        "tamanho_total_mb"
    ] = resumo_inventario[
        "tamanho_total_mb"
    ].round(4)


    ARQUIVOS_ESSENCIAIS = [
        "config/config.yaml",
        "main.py",
        "coletar_ativo_yfinance.py",
        "selecionar_ativos.py",
        "01_coleta_dados.py",
        "02_analise_exploratoria.py",
        "03_regimes_macroeconomicos.py",
        "04_alocacao_portfolio.py",
        "05_backtest.py",
        "06_otimizacao_estrategia.py",
        "07_analise_resultados_finais.py",
        "08_auditoria_global.py",
        "data/raw/market/precos_ativos.csv",
        "data/processed/retornos_ativos.csv",
        "data/processed/dados_macro_mensais.csv",
        "data/processed/backtest_portfolio_mensal.csv",
        "outputs/modelo_final/modelo_oficial.json",
        "outputs/modelo_final/metricas_modelo_oficial.json",
        "outputs/modelo_final/manifesto_arquivos.csv",
    ]


    registros_essenciais = []

    for caminho_relativo in ARQUIVOS_ESSENCIAIS:

        caminho_completo = (
            RAIZ_PROJETO
            / caminho_relativo
        )

        arquivo_valido = (
            caminho_completo.exists()
            and caminho_completo.is_file()
            and caminho_completo.stat().st_size > 0
        )

        registros_essenciais.append(
            {
                "arquivo_esperado": caminho_relativo,
                "existe": caminho_completo.exists(),
                "arquivo_valido": arquivo_valido,
                "tamanho_kb": (
                    caminho_completo.stat().st_size / 1024
                    if caminho_completo.exists()
                    and caminho_completo.is_file()
                    else 0
                ),
                "status": (
                    "OK"
                    if arquivo_valido
                    else "AUSENTE_OU_VAZIO"
                ),
            }
        )


    verificacao_essenciais = pd.DataFrame(
        registros_essenciais
    )


    inventario_arquivos.to_csv(
        ARQUIVO_INVENTARIO,
        index=False,
        encoding="utf-8-sig",
    )

    resumo_inventario.to_csv(
        ARQUIVO_RESUMO,
        index=False,
        encoding="utf-8-sig",
    )

    verificacao_essenciais.to_csv(
        ARQUIVO_ESSENCIAIS,
        index=False,
        encoding="utf-8-sig",
    )


    ARQUIVOS_GERADOS = [
        ARQUIVO_INVENTARIO,
        ARQUIVO_RESUMO,
        ARQUIVO_ESSENCIAIS,
    ]

    arquivos_nao_salvos = [
        arquivo
        for arquivo in ARQUIVOS_GERADOS
        if (
            not arquivo.exists()
            or arquivo.stat().st_size == 0
        )
    ]

    if arquivos_nao_salvos:
        raise FileNotFoundError(
            "Os seguintes arquivos da auditoria "
            "não foram salvos corretamente:\n"
            + "\n".join(
                str(arquivo)
                for arquivo in arquivos_nao_salvos
            )
        )


    quantidade_arquivos = len(
        inventario_arquivos
    )

    quantidade_vazios = int(
        inventario_arquivos[
            "arquivo_vazio"
        ].sum()
    )

    quantidade_essenciais_ok = int(
        verificacao_essenciais[
            "arquivo_valido"
        ].sum()
    )

    quantidade_essenciais_total = len(
        verificacao_essenciais
    )


    print("=" * 70)
    print("AUDITORIA GLOBAL — INVENTÁRIO CONCLUÍDO")
    print("=" * 70)

    print(
        f"\nRaiz do projeto:\n{RAIZ_PROJETO}"
    )

    print(
        f"\nArquivos encontrados: "
        f"{quantidade_arquivos}"
    )

    print(
        f"Arquivos vazios: "
        f"{quantidade_vazios}"
    )

    print(
        f"Arquivos essenciais válidos: "
        f"{quantidade_essenciais_ok}/"
        f"{quantidade_essenciais_total}"
    )

    print(
        "\nVerificação dos arquivos essenciais:"
    )

    display(
        verificacao_essenciais
    )

    print(
        "\nResumo por diretório e extensão:"
    )

    display(
        resumo_inventario
    )

    print(
        "\nArquivos da auditoria salvos:"
    )

    for arquivo in ARQUIVOS_GERADOS:
        print(
            f"- {arquivo.relative_to(RAIZ_PROJETO)}"
        )

def executar_etapa_02() -> None:
    # ============================================================
    # SCRIPT 08 — AUDITORIA GLOBAL DO PROJETO
    # ETAPA 2 — CONSISTÊNCIA DOS ARQUIVOS ESSENCIAIS
    #
    # OBJETIVO:
    # - verificar se os principais arquivos estão legíveis;
    # - conferir estrutura, períodos e ativos;
    # - comparar o índice final do backtest com as métricas;
    # - verificar os arquivos listados no manifesto;
    # - não alterar dados, parâmetros ou resultados do modelo.
    # ============================================================

    from pathlib import Path
    import json
    import re

    import numpy as np
    import pandas as pd

    # ============================================================
    # LOCALIZAÇÃO DA RAIZ DO PROJETO
    # ============================================================

    RAIZ_PROJETO = RAIZ_GLOBAL


    # ============================================================
    # DIRETÓRIO E ARQUIVOS DA AUDITORIA
    # ============================================================

    PASTA_AUDITORIA = (
        RAIZ_PROJETO
        / "outputs"
        / "auditoria"
    )


    PASTA_AUDITORIA.mkdir(
        parents=True,
        exist_ok=True,
    )


    ARQUIVO_RESUMO_ESTRUTURA = (
        PASTA_AUDITORIA
        / "08_02_resumo_estrutura_arquivos.csv"
    )


    ARQUIVO_VALIDACOES = (
        PASTA_AUDITORIA
        / "08_02_validacoes_consistencia.csv"
    )


    ARQUIVO_MANIFESTO_VERIFICADO = (
        PASTA_AUDITORIA
        / "08_02_verificacao_manifesto.csv"
    )


    ARQUIVO_CHAVES_JSON = (
        PASTA_AUDITORIA
        / "08_02_chaves_arquivos_json.csv"
    )


    # ============================================================
    # ARQUIVOS ESSENCIAIS
    # ============================================================

    CAMINHOS_ESSENCIAIS = {
        "precos_ativos": (
            RAIZ_PROJETO
            / "data"
            / "raw"
            / "market"
            / "precos_ativos.csv"
        ),
        "retornos_ativos": (
            RAIZ_PROJETO
            / "data"
            / "processed"
            / "retornos_ativos.csv"
        ),
        "dados_macro_mensais": (
            RAIZ_PROJETO
            / "data"
            / "processed"
            / "dados_macro_mensais.csv"
        ),
        "backtest_portfolio_mensal": (
            RAIZ_PROJETO
            / "data"
            / "processed"
            / "backtest_portfolio_mensal.csv"
        ),
        "modelo_oficial": (
            RAIZ_PROJETO
            / "outputs"
            / "modelo_final"
            / "modelo_oficial.json"
        ),
        "metricas_modelo_oficial": (
            RAIZ_PROJETO
            / "outputs"
            / "modelo_final"
            / "metricas_modelo_oficial.json"
        ),
        "manifesto_arquivos": (
            RAIZ_PROJETO
            / "outputs"
            / "modelo_final"
            / "manifesto_arquivos.csv"
        ),
    }


    # ============================================================
    # FUNÇÕES AUXILIARES
    # ============================================================

    def normalizar_texto(valor) -> str:
        """
        Normaliza nomes de colunas e chaves.
        """

        texto = str(valor).strip().lower()

        texto = (
            texto
            .replace("á", "a")
            .replace("à", "a")
            .replace("ã", "a")
            .replace("â", "a")
            .replace("é", "e")
            .replace("ê", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ô", "o")
            .replace("õ", "o")
            .replace("ú", "u")
            .replace("ç", "c")
        )

        texto = re.sub(
            r"[^a-z0-9]+",
            "_",
            texto,
        )

        return texto.strip("_")


    def ler_csv_seguro(
        caminho: Path,
    ) -> pd.DataFrame:
        """
        Lê um CSV utilizando as codificações esperadas.
        """

        ultimo_erro = None

        for encoding in [
            "utf-8-sig",
            "utf-8",
            "latin1",
        ]:

            try:

                return pd.read_csv(
                    caminho,
                    encoding=encoding,
                    low_memory=False,
                )

            except Exception as erro:

                ultimo_erro = erro


        raise RuntimeError(
            f"Não foi possível ler o arquivo:\n"
            f"{caminho}\n"
            f"Erro: {ultimo_erro}"
        )


    def localizar_coluna_data(
        tabela: pd.DataFrame,
    ):
        """
        Localiza a coluna de data mais provável.
        """

        prioridades = [
            "data",
            "date",
            "mes",
            "competencia",
            "data_referencia",
            "data_final",
        ]


        colunas_normalizadas = {
            normalizar_texto(coluna): coluna
            for coluna in tabela.columns
        }


        for prioridade in prioridades:

            if prioridade in colunas_normalizadas:

                return colunas_normalizadas[
                    prioridade
                ]


        for coluna_normalizada, coluna_original in (
            colunas_normalizadas.items()
        ):

            if (
                "data" in coluna_normalizada
                or "date" in coluna_normalizada
            ):

                return coluna_original


        return None


    def obter_periodo_tabela(
        tabela: pd.DataFrame,
    ):
        """
        Retorna a data mínima e máxima da tabela.
        """

        coluna_data = localizar_coluna_data(
            tabela
        )


        if coluna_data is None:

            return (
                None,
                pd.NaT,
                pd.NaT,
            )


        datas = pd.to_datetime(
            tabela[coluna_data],
            errors="coerce",
        )


        datas_validas = datas.dropna()


        if datas_validas.empty:

            return (
                coluna_data,
                pd.NaT,
                pd.NaT,
            )


        return (
            coluna_data,
            datas_validas.min(),
            datas_validas.max(),
        )


    def achatar_json(
        objeto,
        prefixo="",
    ):
        """
        Converte um JSON aninhado em uma tabela de chave e valor.
        """

        registros = []


        if isinstance(
            objeto,
            dict,
        ):

            for chave, valor in objeto.items():

                nova_chave = (
                    f"{prefixo}.{chave}"
                    if prefixo
                    else str(chave)
                )

                registros.extend(
                    achatar_json(
                        valor,
                        nova_chave,
                    )
                )


        elif isinstance(
            objeto,
            list,
        ):

            for indice, valor in enumerate(
                objeto
            ):

                nova_chave = (
                    f"{prefixo}[{indice}]"
                )

                registros.extend(
                    achatar_json(
                        valor,
                        nova_chave,
                    )
                )


        else:

            registros.append(
                {
                    "chave": prefixo,
                    "valor": objeto,
                    "tipo": type(objeto).__name__,
                }
            )


        return registros


    def extrair_tickers(
        tabela: pd.DataFrame,
    ) -> set:
        """
        Extrai tickers de tabela em formato longo ou largo.
        """

        colunas_normalizadas = {
            normalizar_texto(coluna): coluna
            for coluna in tabela.columns
        }


        if "ticker" in colunas_normalizadas:

            coluna_ticker = colunas_normalizadas[
                "ticker"
            ]

            return set(
                tabela[coluna_ticker]
                .dropna()
                .astype(str)
                .str.strip()
                .loc[
                    lambda serie:
                    serie.ne("")
                ]
                .unique()
                .tolist()
            )


        tickers = set()


        padrao_ticker = re.compile(
            r"^[A-Z0-9]{2,12}([.=^-][A-Z0-9]+)?$"
        )


        for coluna in tabela.columns:

            nome = str(coluna).strip()

            nome_normalizado = normalizar_texto(
                nome
            )


            if nome_normalizado in {
                "data",
                "date",
                "mes",
                "competencia",
                "regime",
                "regime_macro",
            }:

                continue


            if padrao_ticker.match(
                nome.upper()
            ):

                tickers.add(
                    nome
                )


        return tickers


    def adicionar_validacao(
        lista,
        nome,
        status,
        detalhe,
    ):
        """
        Adiciona uma verificação à tabela da auditoria.
        """

        lista.append(
            {
                "validacao": nome,
                "status": status,
                "detalhe": detalhe,
                "observacao": (
                    "Auditoria técnica. Não altera nem aprova "
                    "automaticamente o modelo."
                ),
            }
        )


    # ============================================================
    # LEITURA DOS ARQUIVOS
    # ============================================================

    tabelas = {}
    jsons = {}

    registros_estrutura = []
    validacoes = []
    registros_json = []


    for nome, caminho in CAMINHOS_ESSENCIAIS.items():

        existe = caminho.exists()

        tamanho_bytes = (
            caminho.stat().st_size
            if existe
            else 0
        )

        registro = {
            "arquivo": nome,
            "caminho_relativo": str(
                caminho.relative_to(
                    RAIZ_PROJETO
                )
            ),
            "existe": existe,
            "tamanho_bytes": tamanho_bytes,
            "tipo": caminho.suffix.lower(),
            "leitura_realizada": False,
            "quantidade_linhas": pd.NA,
            "quantidade_colunas": pd.NA,
            "coluna_data": "",
            "data_inicial": pd.NaT,
            "data_final": pd.NaT,
            "erro_leitura": "",
        }


        if not existe or tamanho_bytes == 0:

            registro[
                "erro_leitura"
            ] = "Arquivo ausente ou vazio"

            registros_estrutura.append(
                registro
            )

            continue


        try:

            if caminho.suffix.lower() == ".csv":

                tabela = ler_csv_seguro(
                    caminho
                )

                tabelas[nome] = tabela

                (
                    coluna_data,
                    data_inicial,
                    data_final,
                ) = obter_periodo_tabela(
                    tabela
                )

                registro[
                    "leitura_realizada"
                ] = True

                registro[
                    "quantidade_linhas"
                ] = len(
                    tabela
                )

                registro[
                    "quantidade_colunas"
                ] = len(
                    tabela.columns
                )

                registro[
                    "coluna_data"
                ] = (
                    coluna_data
                    if coluna_data is not None
                    else ""
                )

                registro[
                    "data_inicial"
                ] = data_inicial

                registro[
                    "data_final"
                ] = data_final


            elif caminho.suffix.lower() == ".json":

                with open(
                    caminho,
                    mode="r",
                    encoding="utf-8",
                ) as arquivo:

                    dados_json = json.load(
                        arquivo
                    )


                jsons[nome] = dados_json

                registros_arquivo_json = (
                    achatar_json(
                        dados_json
                    )
                )


                for registro_json in (
                    registros_arquivo_json
                ):

                    registro_json[
                        "arquivo"
                    ] = nome

                    registros_json.append(
                        registro_json
                    )


                registro[
                    "leitura_realizada"
                ] = True

                registro[
                    "quantidade_linhas"
                ] = len(
                    registros_arquivo_json
                )

                registro[
                    "quantidade_colunas"
                ] = 3


        except Exception as erro:

            registro[
                "erro_leitura"
            ] = str(
                erro
            )


        registros_estrutura.append(
            registro
        )


    resumo_estrutura = pd.DataFrame(
        registros_estrutura
    )


    chaves_json = pd.DataFrame(
        registros_json,
        columns=[
            "arquivo",
            "chave",
            "valor",
            "tipo",
        ],
    )


    # ============================================================
    # VALIDAÇÃO 1 — ARQUIVOS EXISTENTES
    # ============================================================

    arquivos_validos = (
        resumo_estrutura[
            "existe"
        ]
        & (
            resumo_estrutura[
                "tamanho_bytes"
            ]
            > 0
        )
    )


    adicionar_validacao(
        lista=validacoes,
        nome="Arquivos essenciais existentes e não vazios",
        status=(
            "OK"
            if arquivos_validos.all()
            else "ERRO"
        ),
        detalhe=(
            f"{int(arquivos_validos.sum())}/"
            f"{len(arquivos_validos)} arquivos válidos"
        ),
    )


    # ============================================================
    # VALIDAÇÃO 2 — LEITURA DOS ARQUIVOS
    # ============================================================

    leituras_validas = (
        resumo_estrutura[
            "leitura_realizada"
        ]
    )


    adicionar_validacao(
        lista=validacoes,
        nome="Arquivos essenciais legíveis",
        status=(
            "OK"
            if leituras_validas.all()
            else "ERRO"
        ),
        detalhe=(
            f"{int(leituras_validas.sum())}/"
            f"{len(leituras_validas)} arquivos lidos"
        ),
    )


    # ============================================================
    # VALIDAÇÃO 3 — CSVs NÃO VAZIOS
    # ============================================================

    csvs_estrutura = resumo_estrutura.loc[
        resumo_estrutura[
            "tipo"
        ].eq(
            ".csv"
        )
    ].copy()


    csvs_nao_vazios = (
        pd.to_numeric(
            csvs_estrutura[
                "quantidade_linhas"
            ],
            errors="coerce",
        )
        .fillna(0)
        .gt(0)
    )


    adicionar_validacao(
        lista=validacoes,
        nome="Arquivos CSV possuem registros",
        status=(
            "OK"
            if csvs_nao_vazios.all()
            else "ERRO"
        ),
        detalhe=(
            f"{int(csvs_nao_vazios.sum())}/"
            f"{len(csvs_nao_vazios)} CSVs não vazios"
        ),
    )


    # ============================================================
    # VALIDAÇÃO 4 — COLUNAS DUPLICADAS
    # ============================================================

    arquivos_colunas_duplicadas = []


    for nome, tabela in tabelas.items():

        duplicadas = tabela.columns[
            tabela.columns.duplicated()
        ].tolist()


        if duplicadas:

            arquivos_colunas_duplicadas.append(
                f"{nome}: {duplicadas}"
            )


    adicionar_validacao(
        lista=validacoes,
        nome="Ausência de colunas duplicadas nos CSVs",
        status=(
            "OK"
            if not arquivos_colunas_duplicadas
            else "ERRO"
        ),
        detalhe=(
            "Nenhuma coluna duplicada"
            if not arquivos_colunas_duplicadas
            else " | ".join(
                arquivos_colunas_duplicadas
            )
        ),
    )


    # ============================================================
    # VALIDAÇÃO 5 — ATIVOS DOS RETORNOS E PREÇOS
    # ============================================================

    if (
        "precos_ativos" in tabelas
        and "retornos_ativos" in tabelas
    ):

        tickers_precos = extrair_tickers(
            tabelas[
                "precos_ativos"
            ]
        )

        tickers_retornos = extrair_tickers(
            tabelas[
                "retornos_ativos"
            ]
        )


        tickers_retornos_ausentes = (
            tickers_retornos
            - tickers_precos
        )


        if not tickers_retornos:

            status_tickers = (
                "NAO_VERIFICADO"
            )

            detalhe_tickers = (
                "Não foi possível identificar os tickers "
                "no arquivo de retornos."
            )

        else:

            status_tickers = (
                "OK"
                if not tickers_retornos_ausentes
                else "ERRO"
            )

            detalhe_tickers = (
                f"Preços: {sorted(tickers_precos)} | "
                f"Retornos: {sorted(tickers_retornos)} | "
                f"Ausentes nos preços: "
                f"{sorted(tickers_retornos_ausentes)}"
            )


        adicionar_validacao(
            lista=validacoes,
            nome="Ativos dos retornos encontrados nos preços",
            status=status_tickers,
            detalhe=detalhe_tickers,
        )


    else:

        adicionar_validacao(
            lista=validacoes,
            nome="Ativos dos retornos encontrados nos preços",
            status="NAO_VERIFICADO",
            detalhe=(
                "Arquivo de preços ou retornos não disponível."
            ),
        )


    # ============================================================
    # VALIDAÇÃO 6 — PERÍODO DO BACKTEST E DADOS MACRO
    # ============================================================

    if (
        "backtest_portfolio_mensal" in tabelas
        and "dados_macro_mensais" in tabelas
    ):

        (
            coluna_data_backtest,
            inicio_backtest,
            fim_backtest,
        ) = obter_periodo_tabela(
            tabelas[
                "backtest_portfolio_mensal"
            ]
        )


        (
            coluna_data_macro,
            inicio_macro,
            fim_macro,
        ) = obter_periodo_tabela(
            tabelas[
                "dados_macro_mensais"
            ]
        )


        datas_disponiveis = all(
            pd.notna(
                valor
            )
            for valor in [
                inicio_backtest,
                fim_backtest,
                inicio_macro,
                fim_macro,
            ]
        )


        if datas_disponiveis:

            periodo_contido = (
                inicio_backtest >= inicio_macro
                and fim_backtest <= fim_macro
            )

            status_periodo = (
                "OK"
                if periodo_contido
                else "ERRO"
            )

            detalhe_periodo = (
                f"Backtest: {inicio_backtest:%Y-%m-%d} "
                f"a {fim_backtest:%Y-%m-%d} | "
                f"Macro: {inicio_macro:%Y-%m-%d} "
                f"a {fim_macro:%Y-%m-%d}"
            )

        else:

            status_periodo = (
                "NAO_VERIFICADO"
            )

            detalhe_periodo = (
                "Não foi possível identificar todos os períodos."
            )


        adicionar_validacao(
            lista=validacoes,
            nome="Período do backtest coberto pelos dados macro",
            status=status_periodo,
            detalhe=detalhe_periodo,
        )


    else:

        adicionar_validacao(
            lista=validacoes,
            nome="Período do backtest coberto pelos dados macro",
            status="NAO_VERIFICADO",
            detalhe=(
                "Backtest ou dados macro não disponíveis."
            ),
        )


    # ============================================================
    # VALIDAÇÃO 7 — DUPLICIDADE DE DATAS NO BACKTEST
    # ============================================================

    if "backtest_portfolio_mensal" in tabelas:

        backtest = tabelas[
            "backtest_portfolio_mensal"
        ]


        coluna_data_backtest = localizar_coluna_data(
            backtest
        )


        if coluna_data_backtest is not None:

            datas_backtest = pd.to_datetime(
                backtest[
                    coluna_data_backtest
                ],
                errors="coerce",
            )


            duplicidades_datas = int(
                datas_backtest
                .dropna()
                .duplicated()
                .sum()
            )


            adicionar_validacao(
                lista=validacoes,
                nome="Sem datas mensais duplicadas no backtest",
                status=(
                    "OK"
                    if duplicidades_datas == 0
                    else "ERRO"
                ),
                detalhe=(
                    f"{duplicidades_datas} datas duplicadas"
                ),
            )


        else:

            adicionar_validacao(
                lista=validacoes,
                nome="Sem datas mensais duplicadas no backtest",
                status="NAO_VERIFICADO",
                detalhe=(
                    "Coluna de data do backtest não identificada."
                ),
            )


    # ============================================================
    # VALIDAÇÃO 8 — MANIFESTO DE ARQUIVOS
    # ============================================================

    registros_manifesto = []


    if "manifesto_arquivos" in tabelas:

        manifesto = tabelas[
            "manifesto_arquivos"
        ].copy()


        coluna_caminho = None


        for coluna in manifesto.columns:

            nome_normalizado = normalizar_texto(
                coluna
            )


            if any(
                termo in nome_normalizado
                for termo in [
                    "caminho",
                    "arquivo",
                    "path",
                ]
            ):

                coluna_caminho = coluna
                break


        if coluna_caminho is not None:

            for valor in manifesto[
                coluna_caminho
            ].dropna():

                texto_caminho = str(
                    valor
                ).strip()


                if not texto_caminho:

                    continue


                caminho_normalizado = (
                    texto_caminho
                    .replace("\\", "/")
                )


                caminho_objeto = Path(
                    caminho_normalizado
                )


                if caminho_objeto.is_absolute():

                    caminho_verificado = (
                        caminho_objeto
                    )

                else:

                    caminho_verificado = (
                        RAIZ_PROJETO
                        / caminho_objeto
                    )


                registros_manifesto.append(
                    {
                        "caminho_manifesto": texto_caminho,
                        "caminho_verificado": str(
                            caminho_verificado
                        ),
                        "existe": caminho_verificado.exists(),
                        "arquivo_valido": (
                            caminho_verificado.exists()
                            and caminho_verificado.is_file()
                            and caminho_verificado.stat().st_size > 0
                        ),
                    }
                )


            verificacao_manifesto = pd.DataFrame(
                registros_manifesto
            )


            if verificacao_manifesto.empty:

                status_manifesto = (
                    "NAO_VERIFICADO"
                )

                detalhe_manifesto = (
                    "Nenhum caminho válido foi encontrado no manifesto."
                )

            else:

                quantidade_manifesto_ok = int(
                    verificacao_manifesto[
                        "arquivo_valido"
                    ].sum()
                )

                quantidade_manifesto_total = len(
                    verificacao_manifesto
                )

                status_manifesto = (
                    "OK"
                    if quantidade_manifesto_ok
                    == quantidade_manifesto_total
                    else "ERRO"
                )

                detalhe_manifesto = (
                    f"{quantidade_manifesto_ok}/"
                    f"{quantidade_manifesto_total} "
                    "arquivos do manifesto encontrados"
                )


        else:

            verificacao_manifesto = pd.DataFrame(
                columns=[
                    "caminho_manifesto",
                    "caminho_verificado",
                    "existe",
                    "arquivo_valido",
                ]
            )

            status_manifesto = (
                "NAO_VERIFICADO"
            )

            detalhe_manifesto = (
                "Coluna de caminho não identificada no manifesto."
            )


    else:

        verificacao_manifesto = pd.DataFrame(
            columns=[
                "caminho_manifesto",
                "caminho_verificado",
                "existe",
                "arquivo_valido",
            ]
        )

        status_manifesto = (
            "NAO_VERIFICADO"
        )

        detalhe_manifesto = (
            "Manifesto não disponível."
        )


    adicionar_validacao(
        lista=validacoes,
        nome="Arquivos registrados no manifesto existem",
        status=status_manifesto,
        detalhe=detalhe_manifesto,
    )


    # ============================================================
    # VALIDAÇÃO 9 — ÍNDICE FINAL DO BACKTEST E MÉTRICAS
    # ============================================================

    status_indice_final = "NAO_VERIFICADO"

    detalhe_indice_final = (
        "Não foi possível localizar automaticamente "
        "o índice final nos dois arquivos."
    )


    if (
        "backtest_portfolio_mensal" in tabelas
        and "metricas_modelo_oficial" in jsons
    ):

        backtest = tabelas[
            "backtest_portfolio_mensal"
        ]


        colunas_numericas = (
            backtest
            .select_dtypes(
                include=[
                    np.number
                ]
            )
            .columns
            .tolist()
        )


        prioridade_colunas = [
            "indice_modelo_oficial",
            "indice_walk_forward",
            "patrimonio_modelo_oficial",
            "indice_portfolio",
            "indice_carteira",
        ]


        mapa_colunas = {
            normalizar_texto(coluna): coluna
            for coluna in colunas_numericas
        }


        coluna_indice_backtest = None


        for prioridade in prioridade_colunas:

            if prioridade in mapa_colunas:

                coluna_indice_backtest = mapa_colunas[
                    prioridade
                ]

                break


        if coluna_indice_backtest is None:

            for coluna_normalizada, coluna_original in (
                mapa_colunas.items()
            ):

                possui_indice = (
                    "indice" in coluna_normalizada
                    or "patrimonio" in coluna_normalizada
                )

                possui_exclusao = any(
                    termo in coluna_normalizada
                    for termo in [
                        "benchmark",
                        "challenger",
                        "desafiante",
                        "estatico",
                        "static",
                        "cdi",
                    ]
                )


                if (
                    possui_indice
                    and not possui_exclusao
                ):

                    coluna_indice_backtest = (
                        coluna_original
                    )

                    break


        registros_metricas_json = achatar_json(
            jsons[
                "metricas_modelo_oficial"
            ]
        )


        valor_indice_json = None
        chave_indice_json = None


        for registro_json in registros_metricas_json:

            chave_normalizada = normalizar_texto(
                registro_json[
                    "chave"
                ]
            )


            possui_indice = (
                "indice" in chave_normalizada
                or "patrimonio" in chave_normalizada
            )

            possui_final = any(
                termo in chave_normalizada
                for termo in [
                    "final",
                    "acumulado",
                ]
            )

            possui_exclusao = any(
                termo in chave_normalizada
                for termo in [
                    "benchmark",
                    "challenger",
                    "desafiante",
                    "estatico",
                    "static",
                    "cdi",
                ]
            )


            if (
                possui_indice
                and possui_final
                and not possui_exclusao
            ):

                valor_convertido = pd.to_numeric(
                    pd.Series(
                        [
                            registro_json[
                                "valor"
                            ]
                        ]
                    ),
                    errors="coerce",
                ).iloc[0]


                if pd.notna(
                    valor_convertido
                ):

                    valor_indice_json = float(
                        valor_convertido
                    )

                    chave_indice_json = (
                        registro_json[
                            "chave"
                        ]
                    )

                    break


        if (
            coluna_indice_backtest is not None
            and valor_indice_json is not None
        ):

            serie_indice = pd.to_numeric(
                backtest[
                    coluna_indice_backtest
                ],
                errors="coerce",
            ).dropna()


            if not serie_indice.empty:

                valor_indice_backtest = float(
                    serie_indice.iloc[-1]
                )


                diferenca_indice = abs(
                    valor_indice_backtest
                    - valor_indice_json
                )


                tolerancia = max(
                    1e-6,
                    abs(
                        valor_indice_json
                    )
                    * 1e-6,
                )


                status_indice_final = (
                    "OK"
                    if diferenca_indice <= tolerancia
                    else "ERRO"
                )


                detalhe_indice_final = (
                    f"Backtest ({coluna_indice_backtest}): "
                    f"{valor_indice_backtest:.10f} | "
                    f"JSON ({chave_indice_json}): "
                    f"{valor_indice_json:.10f} | "
                    f"Diferença: {diferenca_indice:.10f}"
                )


    adicionar_validacao(
        lista=validacoes,
        nome="Índice final consistente entre backtest e métricas",
        status=status_indice_final,
        detalhe=detalhe_indice_final,
    )


    # ============================================================
    # TABELA FINAL DE VALIDAÇÕES
    # ============================================================

    tabela_validacoes = pd.DataFrame(
        validacoes
    )


    # ============================================================
    # SALVAMENTO
    # ============================================================

    resumo_estrutura.to_csv(
        ARQUIVO_RESUMO_ESTRUTURA,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )


    tabela_validacoes.to_csv(
        ARQUIVO_VALIDACOES,
        index=False,
        encoding="utf-8-sig",
    )


    verificacao_manifesto.to_csv(
        ARQUIVO_MANIFESTO_VERIFICADO,
        index=False,
        encoding="utf-8-sig",
    )


    chaves_json.to_csv(
        ARQUIVO_CHAVES_JSON,
        index=False,
        encoding="utf-8-sig",
    )


    # ============================================================
    # VERIFICAÇÃO DOS ARQUIVOS SALVOS
    # ============================================================

    ARQUIVOS_GERADOS = [
        ARQUIVO_RESUMO_ESTRUTURA,
        ARQUIVO_VALIDACOES,
        ARQUIVO_MANIFESTO_VERIFICADO,
        ARQUIVO_CHAVES_JSON,
    ]


    arquivos_nao_salvos = [
        arquivo
        for arquivo in ARQUIVOS_GERADOS
        if (
            not arquivo.exists()
            or arquivo.stat().st_size == 0
        )
    ]


    if arquivos_nao_salvos:

        raise FileNotFoundError(
            "Os seguintes arquivos da Etapa 2 "
            "não foram salvos corretamente:\n"
            + "\n".join(
                str(arquivo)
                for arquivo in arquivos_nao_salvos
            )
        )


    # ============================================================
    # RESULTADOS
    # ============================================================

    quantidade_ok = int(
        tabela_validacoes[
            "status"
        ].eq(
            "OK"
        ).sum()
    )


    quantidade_erros = int(
        tabela_validacoes[
            "status"
        ].eq(
            "ERRO"
        ).sum()
    )


    quantidade_nao_verificada = int(
        tabela_validacoes[
            "status"
        ].eq(
            "NAO_VERIFICADO"
        ).sum()
    )


    print("=" * 70)
    print("AUDITORIA GLOBAL — CONSISTÊNCIA DOS ARQUIVOS")
    print("=" * 70)


    print(
        f"\nRaiz do projeto:\n{RAIZ_PROJETO}"
    )


    print(
        f"\nValidações OK: "
        f"{quantidade_ok}"
    )


    print(
        f"Validações com erro: "
        f"{quantidade_erros}"
    )


    print(
        f"Validações não verificadas automaticamente: "
        f"{quantidade_nao_verificada}"
    )


    print(
        "\nEstrutura dos arquivos essenciais:"
    )


    display(
        resumo_estrutura
    )


    print(
        "\nValidações de consistência:"
    )


    display(
        tabela_validacoes
    )


    if not verificacao_manifesto.empty:

        print(
            "\nVerificação dos arquivos do manifesto:"
        )

        display(
            verificacao_manifesto
        )


    print(
        "\nArquivos salvos:"
    )


    for arquivo in ARQUIVOS_GERADOS:

        print(
            f"- {arquivo.relative_to(RAIZ_PROJETO)}"
        )


    print(
        "\nEsta célula apenas auditou os arquivos existentes. "
        "Nenhum dado, peso ou parâmetro do modelo foi alterado."
    )

def executar_etapa_03() -> None:
    # ============================================================
    # SCRIPT 08 — AUDITORIA GLOBAL DO PROJETO
    # ETAPA 3 — AUDITORIA DE VAZAMENTO TEMPORAL E LOOK-AHEAD
    #
    # OBJETIVO:
    # - verificar se o regime é aplicado com defasagem;
    # - conferir separação entre treino e avaliação;
    # - validar a ordem temporal do walk-forward;
    # - procurar operações potencialmente futuras nos notebooks;
    # - registrar evidências sem alterar o modelo.
    # ============================================================

    from pathlib import Path
    import json
    import re

    import pandas as pd

    # ============================================================
    # LOCALIZAÇÃO DA RAIZ DO PROJETO
    # ============================================================

    RAIZ_PROJETO = RAIZ_GLOBAL


    # ============================================================
    # DIRETÓRIOS
    # ============================================================

    PASTA_SCRIPTS = (
        RAIZ_PROJETO
        / "notebooks"
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

    PASTA_AUDITORIA = (
        RAIZ_PROJETO
        / "outputs"
        / "auditoria"
    )


    PASTA_AUDITORIA.mkdir(
        parents=True,
        exist_ok=True,
    )


    # ============================================================
    # ARQUIVOS DE SAÍDA
    # ============================================================

    ARQUIVO_VALIDACOES = (
        PASTA_AUDITORIA
        / "08_03_validacoes_vazamento_temporal.csv"
    )

    ARQUIVO_EVIDENCIAS = (
        PASTA_AUDITORIA
        / "08_03_evidencias_temporais.csv"
    )

    ARQUIVO_INSPECAO_SCRIPTS = (
        PASTA_AUDITORIA
        / "08_03_inspecao_codigo_scripts.csv"
    )

    ARQUIVO_WALK_FORWARD = (
        PASTA_AUDITORIA
        / "08_03_verificacao_walk_forward.csv"
    )


    # ============================================================
    # FUNÇÕES AUXILIARES
    # ============================================================

    def normalizar_texto(
        valor,
    ) -> str:
        """
        Normaliza nomes de colunas, chaves e arquivos.
        """

        texto = str(
            valor
        ).strip().lower()

        substituicoes = {
            "á": "a",
            "à": "a",
            "ã": "a",
            "â": "a",
            "é": "e",
            "ê": "e",
            "í": "i",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ú": "u",
            "ç": "c",
        }


        for original, substituto in (
            substituicoes.items()
        ):

            texto = texto.replace(
                original,
                substituto,
            )


        texto = re.sub(
            r"[^a-z0-9]+",
            "_",
            texto,
        )


        return texto.strip(
            "_"
        )


    def ler_csv_seguro(
        caminho: Path,
        nrows=None,
    ) -> pd.DataFrame:
        """
        Lê CSV usando as codificações mais comuns do projeto.
        """

        ultimo_erro = None


        for encoding in [
            "utf-8-sig",
            "utf-8",
            "latin1",
        ]:

            try:

                return pd.read_csv(
                    caminho,
                    encoding=encoding,
                    low_memory=False,
                    nrows=nrows,
                )

            except Exception as erro:

                ultimo_erro = erro


        raise RuntimeError(
            f"Não foi possível ler:\n"
            f"{caminho}\n"
            f"Erro: {ultimo_erro}"
        )


    def adicionar_validacao(
        lista,
        nome,
        status,
        detalhe,
    ):
        """
        Registra uma conclusão técnica da auditoria.
        """

        lista.append(
            {
                "validacao": nome,
                "status": status,
                "detalhe": detalhe,
                "observacao": (
                    "Esta verificação identifica evidências técnicas. "
                    "Ela não altera nem aprova automaticamente o modelo."
                ),
            }
        )


    def adicionar_evidencia(
        lista,
        categoria,
        origem,
        evidencia,
        resultado,
    ):
        """
        Registra evidência utilizada pela auditoria.
        """

        lista.append(
            {
                "categoria": categoria,
                "origem": origem,
                "evidencia": evidencia,
                "resultado": resultado,
            }
        )


    def localizar_coluna(
        tabela: pd.DataFrame,
        grupos_tokens,
    ):
        """
        Procura uma coluna que contenha todos os termos de
        um dos grupos informados.
        """

        mapa_colunas = {
            normalizar_texto(
                coluna
            ): coluna
            for coluna in tabela.columns
        }


        for grupo in grupos_tokens:

            for nome_normalizado, nome_original in (
                mapa_colunas.items()
            ):

                if all(
                    token in nome_normalizado
                    for token in grupo
                ):

                    return nome_original


        return None


    def converter_data(
        valor,
    ):
        """
        Converte um valor isolado em data.
        """

        return pd.to_datetime(
            valor,
            errors="coerce",
        )


    def achatar_json(
        objeto,
        prefixo="",
    ):
        """
        Converte JSON aninhado em pares de chave e valor.
        """

        registros = []


        if isinstance(
            objeto,
            dict,
        ):

            for chave, valor in objeto.items():

                nova_chave = (
                    f"{prefixo}.{chave}"
                    if prefixo
                    else str(chave)
                )

                registros.extend(
                    achatar_json(
                        valor,
                        nova_chave,
                    )
                )


        elif isinstance(
            objeto,
            list,
        ):

            for indice, valor in enumerate(
                objeto
            ):

                nova_chave = (
                    f"{prefixo}[{indice}]"
                )

                registros.extend(
                    achatar_json(
                        valor,
                        nova_chave,
                    )
                )


        else:

            registros.append(
                {
                    "chave": prefixo,
                    "valor": objeto,
                }
            )


        return registros


    def localizar_data_json(
        registros_json,
        grupos_tokens,
    ):
        """
        Procura uma data no JSON usando grupos de termos.
        """

        for grupo in grupos_tokens:

            for registro in registros_json:

                chave_normalizada = normalizar_texto(
                    registro[
                        "chave"
                    ]
                )


                if all(
                    token in chave_normalizada
                    for token in grupo
                ):

                    data = converter_data(
                        registro[
                            "valor"
                        ]
                    )


                    if pd.notna(
                        data
                    ):

                        return (
                            registro[
                                "chave"
                            ],
                            data,
                        )


        return (
            None,
            pd.NaT,
        )


    # ============================================================
    # ESTRUTURAS DE CONTROLE
    # ============================================================

    validacoes = []
    evidencias = []
    inspecao_scripts = []
    registros_walk_forward = []


    # ============================================================
    # INSPEÇÃO DOS SCRIPTS 03 A 06
    # ============================================================

    padroes_scripts = [
        "03*.py",
        "04*.py",
        "05*.py",
        "06*.py",
    ]

    arquivos_scripts = []

    for padrao in padroes_scripts:
        arquivos_scripts.extend(
            PASTA_SCRIPTS.glob(
                padrao
            )
        )

    arquivos_scripts = sorted(
        set(
            caminho
            for caminho in arquivos_scripts
            if caminho.is_file()
            and caminho.name != Path(__file__).name
        )
    )

    inspecao_scripts = []

    for caminho_script in arquivos_scripts:

        try:

            codigo_script = caminho_script.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            ocorrencias_shift = re.findall(
                r"\.shift\s*\([^)]*\)",
                codigo_script,
                flags=re.IGNORECASE,
            )

            ocorrencias_shift_negativo = re.findall(
                r"\.shift\s*\(\s*-\s*\d+",
                codigo_script,
                flags=re.IGNORECASE,
            )

            ocorrencias_bfill = re.findall(
                r"\.bfill\s*\(",
                codigo_script,
                flags=re.IGNORECASE,
            )

            ocorrencias_fillna_bfill = re.findall(
                r"fillna\s*\([^)]*bfill",
                codigo_script,
                flags=re.IGNORECASE,
            )

            ocorrencias_center_true = re.findall(
                r"center\s*=\s*True",
                codigo_script,
                flags=re.IGNORECASE,
            )

            mencoes_treino = len(
                re.findall(
                    r"treino|training|train_",
                    codigo_script,
                    flags=re.IGNORECASE,
                )
            )

            mencoes_avaliacao = len(
                re.findall(
                    r"avaliacao|evaluation|eval_",
                    codigo_script,
                    flags=re.IGNORECASE,
                )
            )

            inspecao_scripts.append(
                {
                    "script": caminho_script.name,
                    "quantidade_linhas_codigo": len(
                        codigo_script.splitlines()
                    ),
                    "quantidade_shift": len(
                        ocorrencias_shift
                    ),
                    "exemplos_shift": " | ".join(
                        sorted(
                            set(
                                ocorrencias_shift
                            )
                        )[:10]
                    ),
                    "quantidade_shift_negativo": len(
                        ocorrencias_shift_negativo
                    ),
                    "quantidade_bfill": (
                        len(
                            ocorrencias_bfill
                        )
                        + len(
                            ocorrencias_fillna_bfill
                        )
                    ),
                    "quantidade_center_true": len(
                        ocorrencias_center_true
                    ),
                    "mencoes_treino": mencoes_treino,
                    "mencoes_avaliacao": mencoes_avaliacao,
                    "erro_leitura": "",
                }
            )

        except Exception as erro:

            inspecao_scripts.append(
                {
                    "script": caminho_script.name,
                    "quantidade_linhas_codigo": 0,
                    "quantidade_shift": 0,
                    "exemplos_shift": "",
                    "quantidade_shift_negativo": 0,
                    "quantidade_bfill": 0,
                    "quantidade_center_true": 0,
                    "mencoes_treino": 0,
                    "mencoes_avaliacao": 0,
                    "erro_leitura": str(
                        erro
                    ),
                }
            )


    tabela_inspecao_scripts = pd.DataFrame(
        inspecao_scripts
    )


    # ============================================================
    # VALIDAÇÃO — OPERAÇÕES SHIFT
    # ============================================================

    if tabela_inspecao_scripts.empty:

        adicionar_validacao(
            lista=validacoes,
            nome="Scripts de construção e validação localizados",
            status="NAO_VERIFICADO",
            detalhe=(
                "Nenhum script 03, 04, 05 ou 06 foi localizado."
            ),
        )


    else:

        notebooks_lidos = (
            tabela_inspecao_scripts[
                "erro_leitura"
            ]
            .astype(str)
            .eq("")
        )


        adicionar_validacao(
            lista=validacoes,
            nome="Scripts de construção e validação legíveis",
            status=(
                "OK"
                if notebooks_lidos.all()
                else "ERRO"
            ),
            detalhe=(
                f"{int(notebooks_lidos.sum())}/"
                f"{len(notebooks_lidos)} scripts lidos"
            ),
        )


        quantidade_shift = int(
            tabela_inspecao_scripts[
                "quantidade_shift"
            ].sum()
        )


        adicionar_validacao(
            lista=validacoes,
            nome="Existência de defasagem temporal no código",
            status=(
                "OK"
                if quantidade_shift > 0
                else "NAO_VERIFICADO"
            ),
            detalhe=(
                f"{quantidade_shift} operações shift encontradas"
            ),
        )


        quantidade_shift_negativo = int(
            tabela_inspecao_scripts[
                "quantidade_shift_negativo"
            ].sum()
        )


        adicionar_validacao(
            lista=validacoes,
            nome="Ausência de shift negativo",
            status=(
                "OK"
                if quantidade_shift_negativo == 0
                else "ERRO"
            ),
            detalhe=(
                f"{quantidade_shift_negativo} ocorrências "
                "de shift negativo"
            ),
        )


        quantidade_bfill = int(
            tabela_inspecao_scripts[
                "quantidade_bfill"
            ].sum()
        )


        adicionar_validacao(
            lista=validacoes,
            nome="Ausência de preenchimento com dados futuros",
            status=(
                "OK"
                if quantidade_bfill == 0
                else "ATENCAO"
            ),
            detalhe=(
                f"{quantidade_bfill} ocorrências de bfill"
            ),
        )


        quantidade_center_true = int(
            tabela_inspecao_scripts[
                "quantidade_center_true"
            ].sum()
        )


        adicionar_validacao(
            lista=validacoes,
            nome="Ausência de janela móvel centralizada",
            status=(
                "OK"
                if quantidade_center_true == 0
                else "ATENCAO"
            ),
            detalhe=(
                f"{quantidade_center_true} ocorrências "
                "de center=True"
            ),
        )


    # ============================================================
    # EVIDÊNCIAS DE SHIFT POR NOTEBOOK
    # ============================================================

    for _, linha in tabela_inspecao_scripts.iterrows():

        if int(
            linha[
                "quantidade_shift"
            ]
        ) > 0:

            adicionar_evidencia(
                lista=evidencias,
                categoria="DEFASAGEM",
                origem=linha[
                    "script"
                ],
                evidencia=linha[
                    "exemplos_shift"
                ],
                resultado=(
                    f"{linha['quantidade_shift']} "
                    "operações shift encontradas"
                ),
            )


    # ============================================================
    # VERIFICAÇÃO DAS RECALIBRAÇÕES WALK-FORWARD
    # ============================================================

    arquivos_candidatos_walk_forward = []


    if PASTA_TABELAS.exists():

        arquivos_candidatos_walk_forward.extend(
            PASTA_TABELAS.glob(
                "06_11*.csv"
            )
        )

        arquivos_candidatos_walk_forward.extend(
            PASTA_TABELAS.glob(
                "*walk*forward*.csv"
            )
        )

        arquivos_candidatos_walk_forward.extend(
            PASTA_TABELAS.glob(
                "*recalibr*.csv"
            )
        )


    arquivos_candidatos_walk_forward = sorted(
        set(
            arquivos_candidatos_walk_forward
        )
    )


    arquivo_walk_forward_utilizado = None
    tabela_walk_forward_utilizada = None


    for caminho_csv in arquivos_candidatos_walk_forward:

        try:

            cabecalho = ler_csv_seguro(
                caminho_csv,
                nrows=5,
            )


            coluna_fim_treino = localizar_coluna(
                cabecalho,
                grupos_tokens=[
                    [
                        "fim",
                        "treino",
                    ],
                    [
                        "final",
                        "treino",
                    ],
                    [
                        "train",
                        "end",
                    ],
                ],
            )


            coluna_inicio_aplicacao = localizar_coluna(
                cabecalho,
                grupos_tokens=[
                    [
                        "inicio",
                        "aplicacao",
                    ],
                    [
                        "inicio",
                        "avaliacao",
                    ],
                    [
                        "inicio",
                        "teste",
                    ],
                    [
                        "apply",
                        "start",
                    ],
                    [
                        "evaluation",
                        "start",
                    ],
                ],
            )


            if (
                coluna_fim_treino is not None
                and coluna_inicio_aplicacao is not None
            ):

                arquivo_walk_forward_utilizado = (
                    caminho_csv
                )

                tabela_walk_forward_utilizada = (
                    ler_csv_seguro(
                        caminho_csv
                    )
                )

                break


        except Exception:

            continue


    if tabela_walk_forward_utilizada is not None:

        coluna_fim_treino = localizar_coluna(
            tabela_walk_forward_utilizada,
            grupos_tokens=[
                [
                    "fim",
                    "treino",
                ],
                [
                    "final",
                    "treino",
                ],
                [
                    "train",
                    "end",
                ],
            ],
        )


        coluna_inicio_aplicacao = localizar_coluna(
            tabela_walk_forward_utilizada,
            grupos_tokens=[
                [
                    "inicio",
                    "aplicacao",
                ],
                [
                    "inicio",
                    "avaliacao",
                ],
                [
                    "inicio",
                    "teste",
                ],
                [
                    "apply",
                    "start",
                ],
                [
                    "evaluation",
                    "start",
                ],
            ],
        )


        for indice, linha in (
            tabela_walk_forward_utilizada
            .iterrows()
        ):

            fim_treino = converter_data(
                linha[
                    coluna_fim_treino
                ]
            )


            inicio_aplicacao = converter_data(
                linha[
                    coluna_inicio_aplicacao
                ]
            )


            ordem_valida = (
                pd.notna(
                    fim_treino
                )
                and pd.notna(
                    inicio_aplicacao
                )
                and fim_treino < inicio_aplicacao
            )


            registros_walk_forward.append(
                {
                    "arquivo_origem": str(
                        arquivo_walk_forward_utilizado.relative_to(
                            RAIZ_PROJETO
                        )
                    ),
                    "linha_origem": indice,
                    "fim_treino": fim_treino,
                    "inicio_aplicacao": inicio_aplicacao,
                    "ordem_temporal_valida": ordem_valida,
                    "diferenca_dias": (
                        (
                            inicio_aplicacao
                            - fim_treino
                        ).days
                        if (
                            pd.notna(
                                fim_treino
                            )
                            and pd.notna(
                                inicio_aplicacao
                            )
                        )
                        else pd.NA
                    ),
                }
            )


        tabela_walk_forward = pd.DataFrame(
            registros_walk_forward
        )


        ordens_validas = (
            tabela_walk_forward[
                "ordem_temporal_valida"
            ]
        )


        adicionar_validacao(
            lista=validacoes,
            nome="Treino termina antes da aplicação walk-forward",
            status=(
                "OK"
                if ordens_validas.all()
                else "ERRO"
            ),
            detalhe=(
                f"{int(ordens_validas.sum())}/"
                f"{len(ordens_validas)} recalibrações válidas"
            ),
        )


        adicionar_evidencia(
            lista=evidencias,
            categoria="WALK_FORWARD",
            origem=str(
                arquivo_walk_forward_utilizado.relative_to(
                    RAIZ_PROJETO
                )
            ),
            evidencia=(
                f"Colunas utilizadas: "
                f"{coluna_fim_treino} e "
                f"{coluna_inicio_aplicacao}"
            ),
            resultado=(
                f"{int(ordens_validas.sum())}/"
                f"{len(ordens_validas)} ordens válidas"
            ),
        )


    else:

        tabela_walk_forward = pd.DataFrame(
            columns=[
                "arquivo_origem",
                "linha_origem",
                "fim_treino",
                "inicio_aplicacao",
                "ordem_temporal_valida",
                "diferenca_dias",
            ]
        )


        adicionar_validacao(
            lista=validacoes,
            nome="Treino termina antes da aplicação walk-forward",
            status="NAO_VERIFICADO",
            detalhe=(
                "Nenhuma tabela com fim de treino e "
                "início de aplicação foi identificada automaticamente."
            ),
        )


    # ============================================================
    # VERIFICAÇÃO DO JSON DO MODELO OFICIAL
    # ============================================================

    ARQUIVO_MODELO_OFICIAL = (
        PASTA_MODELO_FINAL
        / "modelo_oficial.json"
    )


    if ARQUIVO_MODELO_OFICIAL.exists():

        try:

            with open(
                ARQUIVO_MODELO_OFICIAL,
                mode="r",
                encoding="utf-8",
            ) as arquivo:

                modelo_json = json.load(
                    arquivo
                )


            registros_modelo_json = achatar_json(
                modelo_json
            )


            (
                chave_fim_treino,
                data_fim_treino,
            ) = localizar_data_json(
                registros_modelo_json,
                grupos_tokens=[
                    [
                        "fim",
                        "treino",
                    ],
                    [
                        "final",
                        "treino",
                    ],
                    [
                        "train",
                        "end",
                    ],
                ],
            )


            (
                chave_inicio_avaliacao,
                data_inicio_avaliacao,
            ) = localizar_data_json(
                registros_modelo_json,
                grupos_tokens=[
                    [
                        "inicio",
                        "avaliacao",
                    ],
                    [
                        "data",
                        "inicial",
                        "avaliacao",
                    ],
                    [
                        "evaluation",
                        "start",
                    ],
                ],
            )


            if (
                pd.notna(
                    data_fim_treino
                )
                and pd.notna(
                    data_inicio_avaliacao
                )
            ):

                separacao_valida = (
                    data_fim_treino
                    < data_inicio_avaliacao
                )


                adicionar_validacao(
                    lista=validacoes,
                    nome="Avaliação começa após o período de treino",
                    status=(
                        "OK"
                        if separacao_valida
                        else "ERRO"
                    ),
                    detalhe=(
                        f"{chave_fim_treino}: "
                        f"{data_fim_treino:%Y-%m-%d} | "
                        f"{chave_inicio_avaliacao}: "
                        f"{data_inicio_avaliacao:%Y-%m-%d}"
                    ),
                )


                adicionar_evidencia(
                    lista=evidencias,
                    categoria="SEPARACAO_TEMPORAL",
                    origem=str(
                        ARQUIVO_MODELO_OFICIAL.relative_to(
                            RAIZ_PROJETO
                        )
                    ),
                    evidencia=(
                        f"Fim do treino: "
                        f"{data_fim_treino:%Y-%m-%d}; "
                        f"início da avaliação: "
                        f"{data_inicio_avaliacao:%Y-%m-%d}"
                    ),
                    resultado=(
                        "Ordem temporal válida"
                        if separacao_valida
                        else "Sobreposição temporal encontrada"
                    ),
                )


            else:

                adicionar_validacao(
                    lista=validacoes,
                    nome="Avaliação começa após o período de treino",
                    status="NAO_VERIFICADO",
                    detalhe=(
                        "As datas de treino e avaliação não foram "
                        "localizadas automaticamente no JSON."
                    ),
                )


        except Exception as erro:

            adicionar_validacao(
                lista=validacoes,
                nome="Avaliação começa após o período de treino",
                status="NAO_VERIFICADO",
                detalhe=(
                    f"Erro ao ler o modelo oficial: {erro}"
                ),
            )


    else:

        adicionar_validacao(
            lista=validacoes,
            nome="Avaliação começa após o período de treino",
            status="NAO_VERIFICADO",
            detalhe=(
                "O arquivo modelo_oficial.json não foi encontrado."
            ),
        )


    # ============================================================
    # VERIFICAÇÃO DO PERÍODO DO BACKTEST
    # ============================================================

    ARQUIVO_BACKTEST = (
        RAIZ_PROJETO
        / "data"
        / "processed"
        / "backtest_portfolio_mensal.csv"
    )


    if ARQUIVO_BACKTEST.exists():

        try:

            backtest = ler_csv_seguro(
                ARQUIVO_BACKTEST
            )


            coluna_data_backtest = localizar_coluna(
                backtest,
                grupos_tokens=[
                    [
                        "data",
                    ],
                    [
                        "date",
                    ],
                    [
                        "mes",
                    ],
                ],
            )


            if coluna_data_backtest is not None:

                datas_backtest = pd.to_datetime(
                    backtest[
                        coluna_data_backtest
                    ],
                    errors="coerce",
                ).dropna()


                if not datas_backtest.empty:

                    adicionar_evidencia(
                        lista=evidencias,
                        categoria="PERIODO_BACKTEST",
                        origem=str(
                            ARQUIVO_BACKTEST.relative_to(
                                RAIZ_PROJETO
                            )
                        ),
                        evidencia=(
                            f"Coluna utilizada: "
                            f"{coluna_data_backtest}"
                        ),
                        resultado=(
                            f"{datas_backtest.min():%Y-%m-%d} "
                            f"a {datas_backtest.max():%Y-%m-%d}; "
                            f"{len(datas_backtest)} registros"
                        ),
                    )


        except Exception as erro:

            adicionar_evidencia(
                lista=evidencias,
                categoria="PERIODO_BACKTEST",
                origem=str(
                    ARQUIVO_BACKTEST.relative_to(
                        RAIZ_PROJETO
                    )
                ),
                evidencia="Erro durante a leitura",
                resultado=str(
                    erro
                ),
            )


    # ============================================================
    # TABELAS FINAIS
    # ============================================================

    tabela_validacoes = pd.DataFrame(
        validacoes
    )


    tabela_evidencias = pd.DataFrame(
        evidencias,
        columns=[
            "categoria",
            "origem",
            "evidencia",
            "resultado",
        ],
    )


    # ============================================================
    # SALVAMENTO
    # ============================================================

    tabela_validacoes.to_csv(
        ARQUIVO_VALIDACOES,
        index=False,
        encoding="utf-8-sig",
    )


    tabela_evidencias.to_csv(
        ARQUIVO_EVIDENCIAS,
        index=False,
        encoding="utf-8-sig",
    )


    tabela_inspecao_scripts.to_csv(
        ARQUIVO_INSPECAO_SCRIPTS,
        index=False,
        encoding="utf-8-sig",
    )


    tabela_walk_forward.to_csv(
        ARQUIVO_WALK_FORWARD,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )


    # ============================================================
    # VERIFICAÇÃO DOS ARQUIVOS SALVOS
    # ============================================================

    ARQUIVOS_GERADOS = [
        ARQUIVO_VALIDACOES,
        ARQUIVO_EVIDENCIAS,
        ARQUIVO_INSPECAO_SCRIPTS,
        ARQUIVO_WALK_FORWARD,
    ]


    arquivos_nao_salvos = [
        arquivo
        for arquivo in ARQUIVOS_GERADOS
        if (
            not arquivo.exists()
            or arquivo.stat().st_size == 0
        )
    ]


    if arquivos_nao_salvos:

        raise FileNotFoundError(
            "Os seguintes arquivos da Etapa 3 "
            "não foram salvos corretamente:\n"
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

    quantidade_ok = int(
        tabela_validacoes[
            "status"
        ].eq(
            "OK"
        ).sum()
    )


    quantidade_erros = int(
        tabela_validacoes[
            "status"
        ].eq(
            "ERRO"
        ).sum()
    )


    quantidade_atencao = int(
        tabela_validacoes[
            "status"
        ].eq(
            "ATENCAO"
        ).sum()
    )


    quantidade_nao_verificado = int(
        tabela_validacoes[
            "status"
        ].eq(
            "NAO_VERIFICADO"
        ).sum()
    )


    print("=" * 70)
    print("AUDITORIA GLOBAL — VAZAMENTO TEMPORAL E LOOK-AHEAD")
    print("=" * 70)


    print(
        f"\nValidações OK: "
        f"{quantidade_ok}"
    )


    print(
        f"Validações com erro: "
        f"{quantidade_erros}"
    )


    print(
        f"Validações com atenção: "
        f"{quantidade_atencao}"
    )


    print(
        f"Validações não verificadas: "
        f"{quantidade_nao_verificado}"
    )


    print(
        "\nInspeção dos scripts:"
    )


    display(
        tabela_inspecao_scripts
    )


    print(
        "\nVerificação temporal do walk-forward:"
    )


    display(
        tabela_walk_forward
    )


    print(
        "\nValidações de vazamento temporal:"
    )


    display(
        tabela_validacoes
    )


    print(
        "\nEvidências utilizadas:"
    )


    display(
        tabela_evidencias
    )


    print(
        "\nArquivos salvos:"
    )


    for arquivo in ARQUIVOS_GERADOS:

        print(
            f"- {arquivo.relative_to(RAIZ_PROJETO)}"
        )


    print(
        "\nEsta célula não alterou dados, parâmetros, "
        "pesos ou resultados do modelo."
    )

def executar_etapa_04() -> None:
    # ============================================================
    # SCRIPT 08 — AUDITORIA GLOBAL DO PROJETO
    # ETAPA 4 — RECÁLCULO E CONFERÊNCIA DAS MÉTRICAS
    #
    # OBJETIVO:
    # - localizar a série mensal do modelo oficial;
    # - recalcular as principais métricas;
    # - comparar os valores recalculados com o JSON oficial;
    # - registrar divergências sem alterar o modelo.
    # ============================================================

    from pathlib import Path
    import json
    import re

    import numpy as np
    import pandas as pd

    # ============================================================
    # LOCALIZAÇÃO DA RAIZ DO PROJETO
    # ============================================================

    RAIZ_PROJETO = RAIZ_GLOBAL


    # ============================================================
    # DIRETÓRIOS
    # ============================================================

    PASTA_PROCESSADOS = (
        RAIZ_PROJETO
        / "data"
        / "processed"
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

    PASTA_AUDITORIA = (
        RAIZ_PROJETO
        / "outputs"
        / "auditoria"
    )


    PASTA_AUDITORIA.mkdir(
        parents=True,
        exist_ok=True,
    )


    # ============================================================
    # ARQUIVOS DE SAÍDA
    # ============================================================

    ARQUIVO_FONTES_ANALISADAS = (
        PASTA_AUDITORIA
        / "08_04_fontes_series_analisadas.csv"
    )

    ARQUIVO_SERIE_UTILIZADA = (
        PASTA_AUDITORIA
        / "08_04_serie_mensal_utilizada.csv"
    )

    ARQUIVO_METRICAS_RECALCULADAS = (
        PASTA_AUDITORIA
        / "08_04_metricas_recalculadas.csv"
    )

    ARQUIVO_COMPARACAO_METRICAS = (
        PASTA_AUDITORIA
        / "08_04_comparacao_metricas_oficiais.csv"
    )

    ARQUIVO_VALIDACOES = (
        PASTA_AUDITORIA
        / "08_04_validacoes_metricas.csv"
    )


    # ============================================================
    # ARQUIVOS OFICIAIS
    # ============================================================

    ARQUIVO_MODELO_OFICIAL = (
        PASTA_MODELO_FINAL
        / "modelo_oficial.json"
    )

    ARQUIVO_METRICAS_OFICIAIS = (
        PASTA_MODELO_FINAL
        / "metricas_modelo_oficial.json"
    )


    if not ARQUIVO_MODELO_OFICIAL.exists():

        raise FileNotFoundError(
            "O arquivo modelo_oficial.json não foi encontrado."
        )


    if not ARQUIVO_METRICAS_OFICIAIS.exists():

        raise FileNotFoundError(
            "O arquivo metricas_modelo_oficial.json "
            "não foi encontrado."
        )


    # ============================================================
    # FUNÇÕES AUXILIARES
    # ============================================================

    def normalizar_texto(
        valor,
    ) -> str:
        """
        Normaliza nomes de colunas e chaves.
        """

        texto = str(
            valor
        ).strip().lower()

        substituicoes = {
            "á": "a",
            "à": "a",
            "ã": "a",
            "â": "a",
            "é": "e",
            "ê": "e",
            "í": "i",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ú": "u",
            "ç": "c",
        }


        for original, novo in substituicoes.items():

            texto = texto.replace(
                original,
                novo,
            )


        texto = re.sub(
            r"[^a-z0-9]+",
            "_",
            texto,
        )


        return texto.strip(
            "_"
        )


    def ler_csv_seguro(
        caminho: Path,
        nrows=None,
    ) -> pd.DataFrame:
        """
        Lê um CSV utilizando as codificações do projeto.
        """

        ultimo_erro = None


        for encoding in [
            "utf-8-sig",
            "utf-8",
            "latin1",
        ]:

            try:

                return pd.read_csv(
                    caminho,
                    encoding=encoding,
                    low_memory=False,
                    nrows=nrows,
                )

            except Exception as erro:

                ultimo_erro = erro


        raise RuntimeError(
            f"Não foi possível ler o arquivo:\n"
            f"{caminho}\n"
            f"Erro: {ultimo_erro}"
        )


    def localizar_coluna(
        tabela: pd.DataFrame,
        grupos_tokens,
        exclusoes=None,
    ):
        """
        Localiza uma coluna usando grupos de palavras prioritários.
        """

        if exclusoes is None:
            exclusoes = []


        colunas_normalizadas = [
            (
                normalizar_texto(
                    coluna
                ),
                coluna,
            )
            for coluna in tabela.columns
        ]


        for grupo in grupos_tokens:

            candidatas = []


            for nome_normalizado, nome_original in (
                colunas_normalizadas
            ):

                possui_grupo = all(
                    token in nome_normalizado
                    for token in grupo
                )


                possui_exclusao = any(
                    exclusao in nome_normalizado
                    for exclusao in exclusoes
                )


                if (
                    possui_grupo
                    and not possui_exclusao
                ):

                    candidatas.append(
                        (
                            len(
                                nome_normalizado
                            ),
                            nome_original,
                        )
                    )


            if candidatas:

                candidatas.sort(
                    key=lambda item: item[0]
                )

                return candidatas[0][1]


        return None


    def localizar_coluna_data(
        tabela: pd.DataFrame,
    ):
        """
        Localiza a coluna temporal da tabela.
        """

        return localizar_coluna(
            tabela=tabela,
            grupos_tokens=[
                [
                    "data",
                ],
                [
                    "date",
                ],
                [
                    "mes",
                ],
                [
                    "competencia",
                ],
            ],
        )


    def achatar_json(
        objeto,
        prefixo="",
    ):
        """
        Converte um JSON aninhado em registros de chave e valor.
        """

        registros = []


        if isinstance(
            objeto,
            dict,
        ):

            for chave, valor in objeto.items():

                nova_chave = (
                    f"{prefixo}.{chave}"
                    if prefixo
                    else str(chave)
                )

                registros.extend(
                    achatar_json(
                        valor,
                        nova_chave,
                    )
                )


        elif isinstance(
            objeto,
            list,
        ):

            for indice, valor in enumerate(
                objeto
            ):

                nova_chave = (
                    f"{prefixo}[{indice}]"
                )

                registros.extend(
                    achatar_json(
                        valor,
                        nova_chave,
                    )
                )


        else:

            registros.append(
                {
                    "chave": prefixo,
                    "valor": objeto,
                }
            )


        return registros


    def localizar_data_json(
        registros_json,
        grupos_tokens,
    ):
        """
        Localiza uma data dentro de um JSON achatado.
        """

        for grupo in grupos_tokens:

            for registro in registros_json:

                chave_normalizada = normalizar_texto(
                    registro[
                        "chave"
                    ]
                )


                if all(
                    token in chave_normalizada
                    for token in grupo
                ):

                    data = pd.to_datetime(
                        registro[
                            "valor"
                        ],
                        errors="coerce",
                    )


                    if pd.notna(
                        data
                    ):

                        return (
                            registro[
                                "chave"
                            ],
                            data,
                        )


        return (
            None,
            pd.NaT,
        )


    def localizar_valor_json(
        registros_json,
        grupos_tokens,
        exclusoes=None,
    ):
        """
        Localiza uma métrica numérica dentro do JSON.
        """

        if exclusoes is None:
            exclusoes = []


        for grupo in grupos_tokens:

            for registro in registros_json:

                chave_normalizada = normalizar_texto(
                    registro[
                        "chave"
                    ]
                )


                possui_grupo = all(
                    token in chave_normalizada
                    for token in grupo
                )


                possui_exclusao = any(
                    exclusao in chave_normalizada
                    for exclusao in exclusoes
                )


                if (
                    possui_grupo
                    and not possui_exclusao
                ):

                    valor = pd.to_numeric(
                        pd.Series(
                            [
                                registro[
                                    "valor"
                                ]
                            ]
                        ),
                        errors="coerce",
                    ).iloc[0]


                    if pd.notna(
                        valor
                    ):

                        return (
                            registro[
                                "chave"
                            ],
                            float(
                                valor
                            ),
                        )


        return (
            None,
            np.nan,
        )


    def ajustar_retorno_decimal(
        serie: pd.Series,
    ) -> pd.Series:
        """
        Garante que os retornos estejam em formato decimal.
        """

        serie = pd.to_numeric(
            serie,
            errors="coerce",
        )


        valores_validos = serie.dropna()


        if valores_validos.empty:

            return serie


        percentil_95 = valores_validos.abs().quantile(
            0.95
        )


        if percentil_95 > 1.5:

            serie = serie / 100.0


        return serie


    def adicionar_validacao(
        lista,
        nome,
        status,
        detalhe,
    ):
        """
        Registra uma validação da auditoria.
        """

        lista.append(
            {
                "validacao": nome,
                "status": status,
                "detalhe": detalhe,
                "observacao": (
                    "A auditoria não altera nem aprova "
                    "automaticamente o modelo."
                ),
            }
        )


    # ============================================================
    # LEITURA DOS JSONS
    # ============================================================

    with open(
        ARQUIVO_MODELO_OFICIAL,
        mode="r",
        encoding="utf-8",
    ) as arquivo:

        modelo_oficial_json = json.load(
            arquivo
        )


    with open(
        ARQUIVO_METRICAS_OFICIAIS,
        mode="r",
        encoding="utf-8",
    ) as arquivo:

        metricas_oficiais_json = json.load(
            arquivo
        )


    registros_modelo_json = achatar_json(
        modelo_oficial_json
    )


    registros_metricas_json = achatar_json(
        metricas_oficiais_json
    )


    # ============================================================
    # PERÍODO OFICIAL DE AVALIAÇÃO
    # ============================================================

    (
        chave_inicio_avaliacao,
        DATA_INICIO_AVALIACAO,
    ) = localizar_data_json(
        registros_modelo_json,
        grupos_tokens=[
            [
                "inicio",
                "avaliacao",
            ],
            [
                "data",
                "inicial",
                "avaliacao",
            ],
            [
                "evaluation",
                "start",
            ],
        ],
    )


    (
        chave_fim_avaliacao,
        DATA_FIM_AVALIACAO,
    ) = localizar_data_json(
        registros_modelo_json,
        grupos_tokens=[
            [
                "fim",
                "avaliacao",
            ],
            [
                "data",
                "final",
                "avaliacao",
            ],
            [
                "evaluation",
                "end",
            ],
        ],
    )


    # ============================================================
    # CANDIDATOS A SÉRIE OFICIAL
    # ============================================================

    arquivos_candidatos = []


    candidatos_diretos = [
        (
            PASTA_PROCESSADOS
            / "backtest_portfolio_mensal.csv"
        ),
    ]


    for arquivo in candidatos_diretos:

        if arquivo.exists():

            arquivos_candidatos.append(
                arquivo
            )


    padroes_tabelas = [
        "06_11*.csv",
        "06_12*.csv",
        "07_01*.csv",
        "07_02*.csv",
        "*walk*forward*.csv",
        "*modelo*oficial*.csv",
        "*series*compar*.csv",
    ]


    for padrao in padroes_tabelas:

        arquivos_candidatos.extend(
            PASTA_TABELAS.glob(
                padrao
            )
        )


    arquivos_candidatos = sorted(
        set(
            arquivos_candidatos
        )
    )


    if not arquivos_candidatos:

        raise FileNotFoundError(
            "Nenhum arquivo candidato contendo a série "
            "do modelo oficial foi encontrado."
        )


    # ============================================================
    # ANÁLISE DOS CANDIDATOS
    # ============================================================

    registros_fontes = []


    EXCLUSOES_MODELO = [
        "benchmark",
        "challenger",
        "desafiante",
        "anterior",
        "sem_cdi",
        "fixo",
        "fixed",
        "estatico",
        "static",
        "cdi",
    ]


    for caminho in arquivos_candidatos:

        registro_fonte = {
            "arquivo": str(
                caminho.relative_to(
                    RAIZ_PROJETO
                )
            ),
            "legivel": False,
            "quantidade_colunas": 0,
            "coluna_data": "",
            "coluna_retorno_oficial": "",
            "coluna_indice_oficial": "",
            "coluna_retorno_cdi": "",
            "coluna_turnover": "",
            "pontuacao": 0,
            "erro": "",
        }


        try:

            cabecalho = ler_csv_seguro(
                caminho,
                nrows=5,
            )


            coluna_data = localizar_coluna_data(
                cabecalho
            )


            coluna_retorno_oficial = localizar_coluna(
                tabela=cabecalho,
                grupos_tokens=[
                    [
                        "retorno",
                        "walk",
                        "forward",
                    ],
                    [
                        "return",
                        "walk",
                        "forward",
                    ],
                    [
                        "retorno",
                        "modelo",
                        "oficial",
                    ],
                    [
                        "retorno",
                        "oficial",
                    ],
                    [
                        "retorno",
                        "wf",
                    ],
                ],
                exclusoes=EXCLUSOES_MODELO,
            )


            coluna_indice_oficial = localizar_coluna(
                tabela=cabecalho,
                grupos_tokens=[
                    [
                        "indice",
                        "walk",
                        "forward",
                    ],
                    [
                        "patrimonio",
                        "walk",
                        "forward",
                    ],
                    [
                        "indice",
                        "modelo",
                        "oficial",
                    ],
                    [
                        "patrimonio",
                        "modelo",
                        "oficial",
                    ],
                    [
                        "indice",
                        "oficial",
                    ],
                ],
                exclusoes=EXCLUSOES_MODELO,
            )


            coluna_retorno_cdi = localizar_coluna(
                tabela=cabecalho,
                grupos_tokens=[
                    [
                        "retorno",
                        "cdi",
                    ],
                    [
                        "return",
                        "cdi",
                    ],
                ],
            )


            coluna_turnover = localizar_coluna(
                tabela=cabecalho,
                grupos_tokens=[
                    [
                        "turnover",
                        "mensal",
                    ],
                    [
                        "turnover",
                    ],
                    [
                        "giro",
                        "mensal",
                    ],
                ],
                exclusoes=[
                    "benchmark",
                    "challenger",
                    "estatico",
                    "static",
                ],
            )


            pontuacao = 0


            if coluna_data is not None:
                pontuacao += 3


            if coluna_retorno_oficial is not None:
                pontuacao += 12


            if coluna_indice_oficial is not None:
                pontuacao += 9


            if coluna_retorno_cdi is not None:
                pontuacao += 3


            if coluna_turnover is not None:
                pontuacao += 2


            nome_normalizado = normalizar_texto(
                caminho.name
            )


            if "06_11" in nome_normalizado:
                pontuacao += 5


            if "walk_forward" in nome_normalizado:
                pontuacao += 4


            if "07_02" in nome_normalizado:
                pontuacao += 3


            registro_fonte.update(
                {
                    "legivel": True,
                    "quantidade_colunas": len(
                        cabecalho.columns
                    ),
                    "coluna_data": (
                        coluna_data
                        if coluna_data is not None
                        else ""
                    ),
                    "coluna_retorno_oficial": (
                        coluna_retorno_oficial
                        if coluna_retorno_oficial is not None
                        else ""
                    ),
                    "coluna_indice_oficial": (
                        coluna_indice_oficial
                        if coluna_indice_oficial is not None
                        else ""
                    ),
                    "coluna_retorno_cdi": (
                        coluna_retorno_cdi
                        if coluna_retorno_cdi is not None
                        else ""
                    ),
                    "coluna_turnover": (
                        coluna_turnover
                        if coluna_turnover is not None
                        else ""
                    ),
                    "pontuacao": pontuacao,
                }
            )


        except Exception as erro:

            registro_fonte[
                "erro"
            ] = str(
                erro
            )


        registros_fontes.append(
            registro_fonte
        )


    fontes_analisadas = pd.DataFrame(
        registros_fontes
    )


    fontes_validas = fontes_analisadas.loc[
        (
            fontes_analisadas[
                "legivel"
            ]
        )
        & (
            fontes_analisadas[
                "pontuacao"
            ]
            > 0
        )
    ].copy()


    if fontes_validas.empty:

        raise RuntimeError(
            "Nenhuma tabela adequada para o recálculo "
            "das métricas foi identificada."
        )


    fonte_selecionada = (
        fontes_validas
        .sort_values(
            [
                "pontuacao",
                "arquivo",
            ],
            ascending=[
                False,
                True,
            ],
        )
        .iloc[0]
    )


    CAMINHO_FONTE = (
        RAIZ_PROJETO
        / fonte_selecionada[
            "arquivo"
        ]
    )


    # ============================================================
    # LEITURA DA SÉRIE SELECIONADA
    # ============================================================

    tabela_fonte = ler_csv_seguro(
        CAMINHO_FONTE
    )


    COLUNA_DATA = (
        fonte_selecionada[
            "coluna_data"
        ]
    )


    COLUNA_RETORNO_OFICIAL = (
        fonte_selecionada[
            "coluna_retorno_oficial"
        ]
    )


    COLUNA_INDICE_OFICIAL = (
        fonte_selecionada[
            "coluna_indice_oficial"
        ]
    )


    COLUNA_RETORNO_CDI = (
        fonte_selecionada[
            "coluna_retorno_cdi"
        ]
    )


    COLUNA_TURNOVER = (
        fonte_selecionada[
            "coluna_turnover"
        ]
    )


    if not COLUNA_DATA:

        raise RuntimeError(
            "A coluna de data da série oficial "
            "não foi identificada."
        )


    if (
        not COLUNA_RETORNO_OFICIAL
        and not COLUNA_INDICE_OFICIAL
    ):

        raise RuntimeError(
            "A tabela selecionada não possui retorno nem "
            "índice identificável do modelo oficial."
        )


    serie_utilizada = pd.DataFrame(
        {
            "data": pd.to_datetime(
                tabela_fonte[
                    COLUNA_DATA
                ],
                errors="coerce",
            )
        }
    )


    if COLUNA_RETORNO_OFICIAL:

        serie_utilizada[
            "retorno_modelo_oficial"
        ] = ajustar_retorno_decimal(
            tabela_fonte[
                COLUNA_RETORNO_OFICIAL
            ]
        )


    if COLUNA_INDICE_OFICIAL:

        serie_utilizada[
            "indice_modelo_oficial_origem"
        ] = pd.to_numeric(
            tabela_fonte[
                COLUNA_INDICE_OFICIAL
            ],
            errors="coerce",
        )


    if COLUNA_RETORNO_CDI:

        serie_utilizada[
            "retorno_cdi"
        ] = ajustar_retorno_decimal(
            tabela_fonte[
                COLUNA_RETORNO_CDI
            ]
        )


    if COLUNA_TURNOVER:

        serie_utilizada[
            "turnover_mensal"
        ] = pd.to_numeric(
            tabela_fonte[
                COLUNA_TURNOVER
            ],
            errors="coerce",
        )


    serie_utilizada = (
        serie_utilizada
        .dropna(
            subset=[
                "data",
            ]
        )
        .sort_values(
            "data"
        )
        .drop_duplicates(
            subset=[
                "data",
            ],
            keep="last",
        )
        .reset_index(
            drop=True
        )
    )


    # ============================================================
    # FILTRO DO PERÍODO OFICIAL
    # ============================================================

    if pd.notna(
        DATA_INICIO_AVALIACAO
    ):

        serie_utilizada = serie_utilizada.loc[
            serie_utilizada[
                "data"
            ]
            >= DATA_INICIO_AVALIACAO
        ]


    if pd.notna(
        DATA_FIM_AVALIACAO
    ):

        serie_utilizada = serie_utilizada.loc[
            serie_utilizada[
                "data"
            ]
            <= DATA_FIM_AVALIACAO
        ]


    serie_utilizada.reset_index(
        drop=True,
        inplace=True,
    )


    # ============================================================
    # CONSTRUÇÃO DOS RETORNOS QUANDO NECESSÁRIO
    # ============================================================

    if (
        "retorno_modelo_oficial"
        not in serie_utilizada.columns
    ):

        indice_origem = serie_utilizada[
            "indice_modelo_oficial_origem"
        ]


        serie_utilizada[
            "retorno_modelo_oficial"
        ] = indice_origem.pct_change()


    serie_utilizada[
        "retorno_modelo_oficial"
    ] = pd.to_numeric(
        serie_utilizada[
            "retorno_modelo_oficial"
        ],
        errors="coerce",
    )


    # ============================================================
    # BUSCA ALTERNATIVA DO CDI
    # ============================================================

    if (
        "retorno_cdi"
        not in serie_utilizada.columns
        or serie_utilizada[
            "retorno_cdi"
        ].isna().all()
    ):

        arquivos_cdi = [
            (
                PASTA_PROCESSADOS
                / "retornos_ativos_ampliados_mensais.csv"
            ),
            (
                PASTA_PROCESSADOS
                / "retornos_ativos.csv"
            ),
        ]


        retorno_cdi_alternativo = None
        origem_cdi_alternativa = None


        for caminho_cdi in arquivos_cdi:

            if not caminho_cdi.exists():
                continue


            tabela_cdi = ler_csv_seguro(
                caminho_cdi
            )


            coluna_data_cdi = localizar_coluna_data(
                tabela_cdi
            )


            coluna_cdi = localizar_coluna(
                tabela=tabela_cdi,
                grupos_tokens=[
                    [
                        "retorno",
                        "cdi",
                    ],
                    [
                        "cdi",
                    ],
                ],
            )


            if (
                coluna_data_cdi is not None
                and coluna_cdi is not None
            ):

                retorno_cdi_alternativo = pd.DataFrame(
                    {
                        "data": pd.to_datetime(
                            tabela_cdi[
                                coluna_data_cdi
                            ],
                            errors="coerce",
                        ),
                        "retorno_cdi": ajustar_retorno_decimal(
                            tabela_cdi[
                                coluna_cdi
                            ]
                        ),
                    }
                )


                origem_cdi_alternativa = caminho_cdi
                break


        if retorno_cdi_alternativo is not None:

            retorno_cdi_alternativo = (
                retorno_cdi_alternativo
                .dropna(
                    subset=[
                        "data",
                    ]
                )
                .drop_duplicates(
                    subset=[
                        "data",
                    ],
                    keep="last",
                )
            )


            if "retorno_cdi" in serie_utilizada.columns:

                serie_utilizada.drop(
                    columns=[
                        "retorno_cdi",
                    ],
                    inplace=True,
                )


            serie_utilizada = serie_utilizada.merge(
                retorno_cdi_alternativo,
                on="data",
                how="left",
            )


    # ============================================================
    # LIMPEZA FINAL DA SÉRIE
    # ============================================================

    serie_utilizada = serie_utilizada.dropna(
        subset=[
            "retorno_modelo_oficial",
        ]
    ).reset_index(
        drop=True
    )


    if serie_utilizada.empty:

        raise RuntimeError(
            "A série mensal do modelo oficial ficou vazia."
        )


    # ============================================================
    # RECÁLCULO DO ÍNDICE E DRAWDOWN
    # ============================================================

    serie_utilizada[
        "indice_modelo_oficial_recalculado"
    ] = (
        100.0
        * (
            1.0
            + serie_utilizada[
                "retorno_modelo_oficial"
            ]
        )
        .cumprod()
    )


    serie_utilizada[
        "pico_indice_recalculado"
    ] = (
        serie_utilizada[
            "indice_modelo_oficial_recalculado"
        ]
        .cummax()
    )


    serie_utilizada[
        "drawdown_recalculado"
    ] = (
        serie_utilizada[
            "indice_modelo_oficial_recalculado"
        ]
        / serie_utilizada[
            "pico_indice_recalculado"
        ]
        - 1.0
    )


    # ============================================================
    # RECÁLCULO DAS MÉTRICAS
    # ============================================================

    retornos = serie_utilizada[
        "retorno_modelo_oficial"
    ].dropna()


    quantidade_meses = len(
        retornos
    )


    produto_retorno = float(
        (
            1.0
            + retornos
        ).prod()
    )


    indice_final_recalculado = (
        100.0
        * produto_retorno
    )


    retorno_anualizado = (
        produto_retorno
        ** (
            12.0
            / quantidade_meses
        )
        - 1.0
    )


    volatilidade_anualizada = float(
        retornos.std(
            ddof=1
        )
        * np.sqrt(
            12.0
        )
    )


    if volatilidade_anualizada > 0:

        retorno_volatilidade = (
            retorno_anualizado
            / volatilidade_anualizada
        )

    else:

        retorno_volatilidade = np.nan


    drawdown_maximo = float(
        serie_utilizada[
            "drawdown_recalculado"
        ].min()
    )


    if drawdown_maximo < 0:

        calmar = (
            retorno_anualizado
            / abs(
                drawdown_maximo
            )
        )

    else:

        calmar = np.nan


    sharpe_excesso_cdi = np.nan
    sortino_excesso_cdi = np.nan


    if (
        "retorno_cdi"
        in serie_utilizada.columns
    ):

        tabela_excesso = serie_utilizada[
            [
                "retorno_modelo_oficial",
                "retorno_cdi",
            ]
        ].dropna()


        if len(
            tabela_excesso
        ) >= 2:

            excesso_cdi = (
                tabela_excesso[
                    "retorno_modelo_oficial"
                ]
                - tabela_excesso[
                    "retorno_cdi"
                ]
            )


            desvio_excesso = excesso_cdi.std(
                ddof=1
            )


            if desvio_excesso > 0:

                sharpe_excesso_cdi = (
                    excesso_cdi.mean()
                    * 12.0
                    / (
                        desvio_excesso
                        * np.sqrt(
                            12.0
                        )
                    )
                )


            retornos_negativos = np.minimum(
                excesso_cdi,
                0.0,
            )


            desvio_negativo = np.sqrt(
                np.mean(
                    retornos_negativos ** 2
                )
            )


            if desvio_negativo > 0:

                sortino_excesso_cdi = (
                    excesso_cdi.mean()
                    * 12.0
                    / (
                        desvio_negativo
                        * np.sqrt(
                            12.0
                        )
                    )
                )


    turnover_total = np.nan


    if (
        "turnover_mensal"
        in serie_utilizada.columns
    ):

        turnover_total = float(
            serie_utilizada[
                "turnover_mensal"
            ]
            .fillna(
                0.0
            )
            .sum()
        )


    # ============================================================
    # TABELA DE MÉTRICAS RECALCULADAS
    # ============================================================

    metricas_recalculadas = pd.DataFrame(
        [
            {
                "metrica": "quantidade_meses",
                "valor_recalculado": quantidade_meses,
                "unidade": "meses",
                "formula": (
                    "Quantidade de retornos mensais válidos"
                ),
            },
            {
                "metrica": "indice_final",
                "valor_recalculado": indice_final_recalculado,
                "unidade": "indice_base_100",
                "formula": (
                    "100 * produto(1 + retorno mensal)"
                ),
            },
            {
                "metrica": "retorno_anualizado",
                "valor_recalculado": retorno_anualizado,
                "unidade": "decimal",
                "formula": (
                    "produto(1+r)^(12/n) - 1"
                ),
            },
            {
                "metrica": "volatilidade_anualizada",
                "valor_recalculado": volatilidade_anualizada,
                "unidade": "decimal",
                "formula": (
                    "desvio padrão mensal * raiz(12)"
                ),
            },
            {
                "metrica": "retorno_volatilidade",
                "valor_recalculado": retorno_volatilidade,
                "unidade": "razao",
                "formula": (
                    "retorno anualizado / volatilidade anualizada"
                ),
            },
            {
                "metrica": "sharpe_excesso_cdi",
                "valor_recalculado": sharpe_excesso_cdi,
                "unidade": "razao",
                "formula": (
                    "média mensal do excesso sobre CDI anualizada "
                    "/ volatilidade anualizada do excesso"
                ),
            },
            {
                "metrica": "sortino_excesso_cdi",
                "valor_recalculado": sortino_excesso_cdi,
                "unidade": "razao",
                "formula": (
                    "média mensal do excesso sobre CDI anualizada "
                    "/ downside deviation anualizado"
                ),
            },
            {
                "metrica": "calmar",
                "valor_recalculado": calmar,
                "unidade": "razao",
                "formula": (
                    "retorno anualizado / valor absoluto "
                    "do drawdown máximo"
                ),
            },
            {
                "metrica": "drawdown_maximo",
                "valor_recalculado": drawdown_maximo,
                "unidade": "decimal",
                "formula": (
                    "menor valor de índice / pico acumulado - 1"
                ),
            },
            {
                "metrica": "turnover_total",
                "valor_recalculado": turnover_total,
                "unidade": "decimal",
                "formula": (
                    "soma do turnover mensal, quando disponível"
                ),
            },
        ]
    )


    # ============================================================
    # CONFIGURAÇÃO DE BUSCA NO JSON
    # ============================================================

    CONFIGURACAO_METRICAS = {
        "indice_final": {
            "grupos": [
                [
                    "indice",
                    "final",
                ],
                [
                    "patrimonio",
                    "final",
                ],
            ],
            "exclusoes": [
                "benchmark",
                "challenger",
                "anterior",
                "static",
                "estatico",
                "cdi",
            ],
            "escalas": [
                1.0,
            ],
            "tolerancia": 0.01,
        },
        "retorno_anualizado": {
            "grupos": [
                [
                    "retorno",
                    "anualizado",
                ],
                [
                    "retorno",
                    "anual",
                ],
            ],
            "exclusoes": [
                "benchmark",
                "challenger",
                "anterior",
                "static",
                "estatico",
                "cdi",
            ],
            "escalas": [
                1.0,
                0.01,
                100.0,
            ],
            "tolerancia": 0.0005,
        },
        "volatilidade_anualizada": {
            "grupos": [
                [
                    "volatilidade",
                    "anualizada",
                ],
                [
                    "volatilidade",
                    "anual",
                ],
            ],
            "exclusoes": [
                "benchmark",
                "challenger",
                "anterior",
                "static",
                "estatico",
                "cdi",
            ],
            "escalas": [
                1.0,
                0.01,
                100.0,
            ],
            "tolerancia": 0.0005,
        },
        "retorno_volatilidade": {
            "grupos": [
                [
                    "retorno",
                    "volatilidade",
                ],
                [
                    "return",
                    "vol",
                ],
            ],
            "exclusoes": [
                "benchmark",
                "challenger",
                "anterior",
            ],
            "escalas": [
                1.0,
            ],
            "tolerancia": 0.005,
        },
        "sharpe_excesso_cdi": {
            "grupos": [
                [
                    "sharpe",
                    "cdi",
                ],
                [
                    "sharpe",
                    "excesso",
                ],
                [
                    "sharpe",
                ],
            ],
            "exclusoes": [
                "benchmark",
                "challenger",
                "anterior",
            ],
            "escalas": [
                1.0,
            ],
            "tolerancia": 0.01,
        },
        "sortino_excesso_cdi": {
            "grupos": [
                [
                    "sortino",
                    "cdi",
                ],
                [
                    "sortino",
                    "excesso",
                ],
                [
                    "sortino",
                ],
            ],
            "exclusoes": [
                "benchmark",
                "challenger",
                "anterior",
            ],
            "escalas": [
                1.0,
            ],
            "tolerancia": 0.02,
        },
        "calmar": {
            "grupos": [
                [
                    "calmar",
                ],
            ],
            "exclusoes": [
                "benchmark",
                "challenger",
                "anterior",
            ],
            "escalas": [
                1.0,
            ],
            "tolerancia": 0.02,
        },
        "drawdown_maximo": {
            "grupos": [
                [
                    "drawdown",
                    "maximo",
                ],
                [
                    "max",
                    "drawdown",
                ],
            ],
            "exclusoes": [
                "benchmark",
                "challenger",
                "anterior",
            ],
            "escalas": [
                1.0,
                0.01,
                100.0,
            ],
            "tolerancia": 0.0005,
        },
        "turnover_total": {
            "grupos": [
                [
                    "turnover",
                    "total",
                ],
                [
                    "turnover",
                ],
            ],
            "exclusoes": [
                "benchmark",
                "challenger",
                "anterior",
            ],
            "escalas": [
                1.0,
            ],
            "tolerancia": 0.005,
        },
    }


    # ============================================================
    # COMPARAÇÃO COM AS MÉTRICAS OFICIAIS
    # ============================================================

    registros_comparacao = []


    for _, linha_metrica in metricas_recalculadas.iterrows():

        nome_metrica = linha_metrica[
            "metrica"
        ]


        if nome_metrica not in CONFIGURACAO_METRICAS:
            continue


        valor_recalculado = linha_metrica[
            "valor_recalculado"
        ]


        configuracao = CONFIGURACAO_METRICAS[
            nome_metrica
        ]


        (
            chave_json,
            valor_json_original,
        ) = localizar_valor_json(
            registros_json=registros_metricas_json,
            grupos_tokens=configuracao[
                "grupos"
            ],
            exclusoes=configuracao[
                "exclusoes"
            ],
        )


        if pd.isna(
            valor_recalculado
        ):

            registros_comparacao.append(
                {
                    "metrica": nome_metrica,
                    "chave_json": chave_json,
                    "valor_json_original": valor_json_original,
                    "escala_aplicada_json": np.nan,
                    "valor_json_ajustado": np.nan,
                    "valor_recalculado": valor_recalculado,
                    "diferenca_absoluta": np.nan,
                    "tolerancia": configuracao[
                        "tolerancia"
                    ],
                    "status": "NAO_RECALCULADA",
                    "detalhe": (
                        "A série necessária não estava disponível."
                    ),
                }
            )

            continue


        if pd.isna(
            valor_json_original
        ):

            registros_comparacao.append(
                {
                    "metrica": nome_metrica,
                    "chave_json": "",
                    "valor_json_original": np.nan,
                    "escala_aplicada_json": np.nan,
                    "valor_json_ajustado": np.nan,
                    "valor_recalculado": valor_recalculado,
                    "diferenca_absoluta": np.nan,
                    "tolerancia": configuracao[
                        "tolerancia"
                    ],
                    "status": "NAO_ENCONTRADA_NO_JSON",
                    "detalhe": (
                        "A métrica não foi localizada automaticamente "
                        "no JSON oficial."
                    ),
                }
            )

            continue


        candidatos_escala = []


        for escala in configuracao[
            "escalas"
        ]:

            valor_ajustado = (
                valor_json_original
                * escala
            )


            diferenca = abs(
                valor_recalculado
                - valor_ajustado
            )


            candidatos_escala.append(
                {
                    "escala": escala,
                    "valor_ajustado": valor_ajustado,
                    "diferenca": diferenca,
                }
            )


        melhor_escala = min(
            candidatos_escala,
            key=lambda item: item[
                "diferenca"
            ],
        )


        status_comparacao = (
            "OK"
            if melhor_escala[
                "diferenca"
            ]
            <= configuracao[
                "tolerancia"
            ]
            else "DIVERGENTE"
        )


        registros_comparacao.append(
            {
                "metrica": nome_metrica,
                "chave_json": chave_json,
                "valor_json_original": valor_json_original,
                "escala_aplicada_json": melhor_escala[
                    "escala"
                ],
                "valor_json_ajustado": melhor_escala[
                    "valor_ajustado"
                ],
                "valor_recalculado": valor_recalculado,
                "diferenca_absoluta": melhor_escala[
                    "diferenca"
                ],
                "tolerancia": configuracao[
                    "tolerancia"
                ],
                "status": status_comparacao,
                "detalhe": (
                    "Valores dentro da tolerância."
                    if status_comparacao == "OK"
                    else "Diferença superior à tolerância."
                ),
            }
        )


    comparacao_metricas = pd.DataFrame(
        registros_comparacao
    )


    # ============================================================
    # VALIDAÇÕES DA ETAPA
    # ============================================================

    validacoes = []


    adicionar_validacao(
        lista=validacoes,
        nome="Fonte da série oficial identificada",
        status="OK",
        detalhe=str(
            CAMINHO_FONTE.relative_to(
                RAIZ_PROJETO
            )
        ),
    )


    adicionar_validacao(
        lista=validacoes,
        nome="Série oficial possui retornos mensais",
        status=(
            "OK"
            if quantidade_meses > 0
            else "ERRO"
        ),
        detalhe=(
            f"{quantidade_meses} retornos mensais válidos"
        ),
    )


    adicionar_validacao(
        lista=validacoes,
        nome="Período possui ao menos 12 meses",
        status=(
            "OK"
            if quantidade_meses >= 12
            else "ATENCAO"
        ),
        detalhe=(
            f"{quantidade_meses} meses"
        ),
    )


    adicionar_validacao(
        lista=validacoes,
        nome="Retornos mensais superiores a -100%",
        status=(
            "OK"
            if (
                retornos > -1.0
            ).all()
            else "ERRO"
        ),
        detalhe=(
            f"Menor retorno mensal: "
            f"{retornos.min():.6f}"
        ),
    )


    quantidade_metricas_ok = int(
        comparacao_metricas[
            "status"
        ].eq(
            "OK"
        ).sum()
    )


    quantidade_metricas_divergentes = int(
        comparacao_metricas[
            "status"
        ].eq(
            "DIVERGENTE"
        ).sum()
    )


    quantidade_metricas_comparaveis = int(
        comparacao_metricas[
            "status"
        ].isin(
            [
                "OK",
                "DIVERGENTE",
            ]
        ).sum()
    )


    adicionar_validacao(
        lista=validacoes,
        nome="Métricas comparáveis consistentes com o JSON",
        status=(
            "OK"
            if (
                quantidade_metricas_comparaveis > 0
                and quantidade_metricas_divergentes == 0
            )
            else (
                "ERRO"
                if quantidade_metricas_divergentes > 0
                else "NAO_VERIFICADO"
            )
        ),
        detalhe=(
            f"{quantidade_metricas_ok}/"
            f"{quantidade_metricas_comparaveis} "
            "métricas comparáveis dentro da tolerância"
        ),
    )


    adicionar_validacao(
        lista=validacoes,
        nome="Índice final positivo",
        status=(
            "OK"
            if indice_final_recalculado > 0
            else "ERRO"
        ),
        detalhe=(
            f"Índice final: "
            f"{indice_final_recalculado:.10f}"
        ),
    )


    tabela_validacoes = pd.DataFrame(
        validacoes
    )


    # ============================================================
    # SALVAMENTO
    # ============================================================

    fontes_analisadas.to_csv(
        ARQUIVO_FONTES_ANALISADAS,
        index=False,
        encoding="utf-8-sig",
    )


    serie_utilizada.to_csv(
        ARQUIVO_SERIE_UTILIZADA,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )


    metricas_recalculadas.to_csv(
        ARQUIVO_METRICAS_RECALCULADAS,
        index=False,
        encoding="utf-8-sig",
    )


    comparacao_metricas.to_csv(
        ARQUIVO_COMPARACAO_METRICAS,
        index=False,
        encoding="utf-8-sig",
    )


    tabela_validacoes.to_csv(
        ARQUIVO_VALIDACOES,
        index=False,
        encoding="utf-8-sig",
    )


    # ============================================================
    # VERIFICAÇÃO DOS ARQUIVOS SALVOS
    # ============================================================

    ARQUIVOS_GERADOS = [
        ARQUIVO_FONTES_ANALISADAS,
        ARQUIVO_SERIE_UTILIZADA,
        ARQUIVO_METRICAS_RECALCULADAS,
        ARQUIVO_COMPARACAO_METRICAS,
        ARQUIVO_VALIDACOES,
    ]


    arquivos_nao_salvos = [
        arquivo
        for arquivo in ARQUIVOS_GERADOS
        if (
            not arquivo.exists()
            or arquivo.stat().st_size == 0
        )
    ]


    if arquivos_nao_salvos:

        raise FileNotFoundError(
            "Os seguintes arquivos da Etapa 4 "
            "não foram salvos corretamente:\n"
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
    print("AUDITORIA GLOBAL — RECÁLCULO DAS MÉTRICAS")
    print("=" * 70)


    print(
        f"\nFonte selecionada:\n"
        f"{CAMINHO_FONTE.relative_to(RAIZ_PROJETO)}"
    )


    print(
        f"\nColuna de retorno oficial:\n"
        f"{COLUNA_RETORNO_OFICIAL or 'Derivada do índice'}"
    )


    print(
        f"\nPeríodo utilizado:\n"
        f"{serie_utilizada['data'].min():%Y-%m-%d} "
        f"a "
        f"{serie_utilizada['data'].max():%Y-%m-%d}"
    )


    print(
        f"\nQuantidade de meses: "
        f"{quantidade_meses}"
    )


    print(
        f"Índice final recalculado: "
        f"{indice_final_recalculado:.10f}"
    )


    print(
        f"Retorno anualizado: "
        f"{retorno_anualizado:.6%}"
    )


    print(
        f"Volatilidade anualizada: "
        f"{volatilidade_anualizada:.6%}"
    )


    print(
        f"Retorno/volatilidade: "
        f"{retorno_volatilidade:.6f}"
    )


    print(
        f"Drawdown máximo: "
        f"{drawdown_maximo:.6%}"
    )


    print(
        "\nMétricas recalculadas:"
    )


    display(
        metricas_recalculadas
    )


    print(
        "\nComparação com o JSON oficial:"
    )


    display(
        comparacao_metricas
    )


    print(
        "\nValidações:"
    )


    display(
        tabela_validacoes
    )


    print(
        "\nArquivos salvos:"
    )


    for arquivo in ARQUIVOS_GERADOS:

        print(
            f"- {arquivo.relative_to(RAIZ_PROJETO)}"
        )


    print(
        "\nNenhum dado, peso, parâmetro ou resultado "
        "oficial foi alterado."
    )

def executar_etapa_05() -> None:
    # ============================================================
    # SCRIPT 08 — AUDITORIA GLOBAL DO PROJETO
    # ETAPA 5 — ROBUSTEZ, OVERFITTING E EXCESSO DE APROVAÇÕES
    #
    # OBJETIVO:
    # - avaliar a estabilidade do modelo;
    # - verificar concentração temporal e por regime;
    # - analisar sensibilidade dos parâmetros;
    # - comparar o modelo com benchmark e desafiante;
    # - separar validações técnicas de aprovação metodológica;
    # - identificar risco de overfitting;
    # - não alterar o modelo ou seus resultados.
    # ============================================================

    from pathlib import Path
    import json
    import re

    import numpy as np
    import pandas as pd

    # ============================================================
    # LOCALIZAÇÃO DA RAIZ DO PROJETO
    # ============================================================

    RAIZ_PROJETO = RAIZ_GLOBAL


    # ============================================================
    # DIRETÓRIOS
    # ============================================================

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

    PASTA_AUDITORIA = (
        RAIZ_PROJETO
        / "outputs"
        / "auditoria"
    )


    PASTA_AUDITORIA.mkdir(
        parents=True,
        exist_ok=True,
    )


    # ============================================================
    # ARQUIVOS DE SAÍDA
    # ============================================================

    ARQUIVO_ARQUIVOS_ANALISADOS = (
        PASTA_AUDITORIA
        / "08_05_arquivos_analisados.csv"
    )

    ARQUIVO_STATUS_EXISTENTES = (
        PASTA_AUDITORIA
        / "08_05_status_validacoes_existentes.csv"
    )

    ARQUIVO_RESUMO_APROVACOES = (
        PASTA_AUDITORIA
        / "08_05_resumo_aprovacoes.csv"
    )

    ARQUIVO_EVIDENCIAS = (
        PASTA_AUDITORIA
        / "08_05_evidencias_robustez.csv"
    )

    ARQUIVO_RISCOS = (
        PASTA_AUDITORIA
        / "08_05_riscos_overfitting.csv"
    )

    ARQUIVO_INDICADORES = (
        PASTA_AUDITORIA
        / "08_05_indicadores_robustez.csv"
    )

    ARQUIVO_VALIDACOES = (
        PASTA_AUDITORIA
        / "08_05_validacoes_auditoria.csv"
    )


    # ============================================================
    # FUNÇÕES AUXILIARES
    # ============================================================

    def normalizar_texto(valor) -> str:
        """
        Normaliza textos para comparação.
        """

        texto = str(
            valor
        ).strip().lower()

        substituicoes = {
            "á": "a",
            "à": "a",
            "ã": "a",
            "â": "a",
            "é": "e",
            "ê": "e",
            "í": "i",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ú": "u",
            "ç": "c",
        }


        for original, novo in substituicoes.items():

            texto = texto.replace(
                original,
                novo,
            )


        texto = re.sub(
            r"[^a-z0-9]+",
            "_",
            texto,
        )


        return texto.strip("_")


    def ler_csv_seguro(caminho: Path) -> pd.DataFrame:
        """
        Lê CSV utilizando codificações comuns do projeto.
        """

        ultimo_erro = None


        for encoding in [
            "utf-8-sig",
            "utf-8",
            "latin1",
        ]:

            try:

                return pd.read_csv(
                    caminho,
                    encoding=encoding,
                    low_memory=False,
                )

            except Exception as erro:

                ultimo_erro = erro


        raise RuntimeError(
            f"Não foi possível ler:\n"
            f"{caminho}\n"
            f"Erro: {ultimo_erro}"
        )


    def localizar_coluna(
        tabela: pd.DataFrame,
        grupos_tokens,
        exclusoes=None,
    ):
        """
        Localiza uma coluna por grupos de palavras.
        """

        if exclusoes is None:
            exclusoes = []


        mapa_colunas = [
            (
                normalizar_texto(coluna),
                coluna,
            )
            for coluna in tabela.columns
        ]


        for grupo in grupos_tokens:

            candidatas = []


            for nome_normalizado, nome_original in mapa_colunas:

                possui_grupo = all(
                    token in nome_normalizado
                    for token in grupo
                )


                possui_exclusao = any(
                    token in nome_normalizado
                    for token in exclusoes
                )


                if (
                    possui_grupo
                    and not possui_exclusao
                ):

                    candidatas.append(
                        (
                            len(nome_normalizado),
                            nome_original,
                        )
                    )


            if candidatas:

                candidatas.sort(
                    key=lambda item: item[0]
                )

                return candidatas[0][1]


        return None


    def converter_booleano(serie: pd.Series) -> pd.Series:
        """
        Converte diferentes representações em booleano.
        """

        mapa = {
            "true": True,
            "verdadeiro": True,
            "sim": True,
            "yes": True,
            "1": True,
            "ok": True,
            "aprovado": True,
            "superou": True,
            "acima": True,
            "false": False,
            "falso": False,
            "nao": False,
            "no": False,
            "0": False,
            "erro": False,
            "reprovado": False,
            "abaixo": False,
        }


        return (
            serie
            .astype(str)
            .map(normalizar_texto)
            .map(mapa)
        )


    def classificar_status(valor) -> str:
        """
        Classifica status encontrados nos arquivos existentes.
        """

        status = normalizar_texto(valor)


        termos_negativos = [
            "erro",
            "reprovado",
            "reprovada",
            "falha",
            "divergente",
            "nao_aprovado",
            "nao_aprovada",
            "abaixo_do_benchmark",
            "nao_superou",
        ]


        termos_atencao = [
            "atencao",
            "nao_verificado",
            "nao_verificada",
            "parcial",
            "robustez_parcial",
            "aprovado_com_ressalvas",
            "aprovada_com_ressalvas",
            "promissor",
            "nao_conclusivo",
            "inconclusivo",
            "pendente",
        ]


        termos_positivos = [
            "ok",
            "aprovado",
            "aprovada",
            "sucesso",
            "superou_o_benchmark",
            "validado",
            "validada",
            "robusto",
            "robusta",
            "concluido",
            "concluida",
        ]


        if any(
            termo in status
            for termo in termos_negativos
        ):

            return "NEGATIVO"


        if any(
            termo in status
            for termo in termos_atencao
        ):

            return "ATENCAO"


        if any(
            termo in status
            for termo in termos_positivos
        ):

            return "POSITIVO"


        return "NAO_CLASSIFICADO"


    def achatar_json(objeto, prefixo=""):
        """
        Converte JSON aninhado em registros de chave e valor.
        """

        registros = []


        if isinstance(objeto, dict):

            for chave, valor in objeto.items():

                nova_chave = (
                    f"{prefixo}.{chave}"
                    if prefixo
                    else str(chave)
                )


                registros.extend(
                    achatar_json(
                        valor,
                        nova_chave,
                    )
                )


        elif isinstance(objeto, list):

            for indice, valor in enumerate(objeto):

                registros.extend(
                    achatar_json(
                        valor,
                        f"{prefixo}[{indice}]",
                    )
                )


        else:

            registros.append(
                {
                    "chave": prefixo,
                    "valor": objeto,
                }
            )


        return registros


    def buscar_valor_json(
        registros_json,
        grupos_tokens,
        exclusoes=None,
    ):
        """
        Procura um valor numérico no JSON.
        """

        if exclusoes is None:
            exclusoes = []


        for grupo in grupos_tokens:

            for registro in registros_json:

                chave_normalizada = normalizar_texto(
                    registro["chave"]
                )


                possui_grupo = all(
                    token in chave_normalizada
                    for token in grupo
                )


                possui_exclusao = any(
                    token in chave_normalizada
                    for token in exclusoes
                )


                if (
                    possui_grupo
                    and not possui_exclusao
                ):

                    valor = pd.to_numeric(
                        pd.Series(
                            [
                                registro["valor"]
                            ]
                        ),
                        errors="coerce",
                    ).iloc[0]


                    if pd.notna(valor):

                        return (
                            registro["chave"],
                            float(valor),
                        )


        return (
            None,
            np.nan,
        )


    def buscar_data_json(
        registros_json,
        grupos_tokens,
    ):
        """
        Procura uma data no JSON.
        """

        for grupo in grupos_tokens:

            for registro in registros_json:

                chave_normalizada = normalizar_texto(
                    registro["chave"]
                )


                if all(
                    token in chave_normalizada
                    for token in grupo
                ):

                    data = pd.to_datetime(
                        registro["valor"],
                        errors="coerce",
                    )


                    if pd.notna(data):

                        return (
                            registro["chave"],
                            data,
                        )


        return (
            None,
            pd.NaT,
        )


    def adicionar_risco(
        lista,
        criterio,
        nivel,
        evidencia,
        impacto,
    ):
        """
        Registra risco metodológico.
        """

        lista.append(
            {
                "criterio": criterio,
                "nivel_risco": nivel,
                "evidencia": evidencia,
                "impacto_metodologico": impacto,
                "altera_modelo": False,
            }
        )


    def adicionar_validacao(
        lista,
        nome,
        status,
        detalhe,
    ):
        """
        Registra validação da auditoria.
        """

        lista.append(
            {
                "validacao": nome,
                "status": status,
                "detalhe": detalhe,
                "observacao": (
                    "Validação da auditoria. "
                    "Não representa aprovação automática do modelo."
                ),
            }
        )


    # ============================================================
    # LOCALIZAÇÃO DOS ARQUIVOS RELEVANTES
    # ============================================================

    padroes_arquivos = [
        "06_09*.csv",
        "06_10*.csv",
        "06_11*.csv",
        "06_12*.csv",
        "07_01*.csv",
        "07_02*.csv",
        "07_03*.csv",
        "07_04*.csv",
        "07_05*.csv",
        "*validacoes*.csv",
        "*robustez*.csv",
        "*sensibilidade*.csv",
        "*walk_forward*.csv",
    ]


    arquivos_candidatos = []


    for padrao in padroes_arquivos:

        arquivos_candidatos.extend(
            PASTA_TABELAS.glob(padrao)
        )


    arquivos_candidatos = sorted(
        set(arquivos_candidatos)
    )


    # Evita analisar arquivos gerados pelo próprio Notebook 08.
    arquivos_candidatos = [
        arquivo
        for arquivo in arquivos_candidatos
        if not arquivo.name.startswith("08_")
    ]


    # ============================================================
    # LEITURA DOS ARQUIVOS
    # ============================================================

    tabelas = {}
    registros_arquivos = []


    for caminho in arquivos_candidatos:

        try:

            tabela = ler_csv_seguro(
                caminho
            )


            tabelas[caminho] = tabela


            registros_arquivos.append(
                {
                    "arquivo": str(
                        caminho.relative_to(
                            RAIZ_PROJETO
                        )
                    ),
                    "legivel": True,
                    "quantidade_linhas": len(tabela),
                    "quantidade_colunas": len(
                        tabela.columns
                    ),
                    "erro": "",
                }
            )


        except Exception as erro:

            registros_arquivos.append(
                {
                    "arquivo": str(
                        caminho.relative_to(
                            RAIZ_PROJETO
                        )
                    ),
                    "legivel": False,
                    "quantidade_linhas": 0,
                    "quantidade_colunas": 0,
                    "erro": str(erro),
                }
            )


    arquivos_analisados = pd.DataFrame(
        registros_arquivos
    )


    # ============================================================
    # LEVANTAMENTO DOS STATUS EXISTENTES
    # ============================================================

    registros_status = []


    for caminho, tabela in tabelas.items():

        colunas_status = [
            coluna
            for coluna in tabela.columns
            if any(
                termo in normalizar_texto(coluna)
                for termo in [
                    "status",
                    "situacao",
                    "classificacao",
                    "aprovacao",
                ]
            )
        ]


        for coluna_status in colunas_status:

            for indice, valor in tabela[
                coluna_status
            ].items():

                if pd.isna(valor):
                    continue


                registros_status.append(
                    {
                        "arquivo": str(
                            caminho.relative_to(
                                RAIZ_PROJETO
                            )
                        ),
                        "linha": indice,
                        "coluna_status": coluna_status,
                        "status_original": str(valor),
                        "status_normalizado": normalizar_texto(
                            valor
                        ),
                        "classificacao_auditoria": classificar_status(
                            valor
                        ),
                        "tipo_validacao": (
                            "TECNICA"
                            if (
                                "validacao"
                                in normalizar_texto(
                                    caminho.name
                                )
                                or "validacao"
                                in normalizar_texto(
                                    coluna_status
                                )
                            )
                            else "RESULTADO_OU_MODELO"
                        ),
                    }
                )


    status_existentes = pd.DataFrame(
        registros_status,
        columns=[
            "arquivo",
            "linha",
            "coluna_status",
            "status_original",
            "status_normalizado",
            "classificacao_auditoria",
            "tipo_validacao",
        ],
    )


    if status_existentes.empty:

        resumo_aprovacoes = pd.DataFrame(
            columns=[
                "tipo_validacao",
                "classificacao_auditoria",
                "quantidade",
                "percentual",
            ]
        )


    else:

        resumo_aprovacoes = (
            status_existentes
            .groupby(
                [
                    "tipo_validacao",
                    "classificacao_auditoria",
                ],
                as_index=False,
            )
            .size()
            .rename(
                columns={
                    "size": "quantidade",
                }
            )
        )


        totais_tipo = (
            resumo_aprovacoes
            .groupby(
                "tipo_validacao"
            )[
                "quantidade"
            ]
            .transform("sum")
        )


        resumo_aprovacoes[
            "percentual"
        ] = (
            resumo_aprovacoes[
                "quantidade"
            ]
            / totais_tipo
        )


    # ============================================================
    # EXTRAÇÃO DE EVIDÊNCIAS TEXTUAIS
    # ============================================================

    PALAVRAS_EVIDENCIA = [
        "robustez",
        "sensibilidade",
        "benchmark",
        "challenger",
        "desafiante",
        "overfitting",
        "holdout",
        "amostra",
        "regime",
        "walk_forward",
        "rolling",
        "nao_conclusivo",
        "parcial",
        "avaliacao",
        "inspecionado",
        "recalibracao",
    ]


    registros_evidencias = []


    for caminho, tabela in tabelas.items():

        for indice, linha in tabela.iterrows():

            texto_linha = " | ".join(
                str(valor)
                for valor in linha.tolist()
                if pd.notna(valor)
            )


            texto_normalizado = normalizar_texto(
                texto_linha
            )


            palavras_encontradas = [
                palavra
                for palavra in PALAVRAS_EVIDENCIA
                if palavra in texto_normalizado
            ]


            if palavras_encontradas:

                registros_evidencias.append(
                    {
                        "arquivo": str(
                            caminho.relative_to(
                                RAIZ_PROJETO
                            )
                        ),
                        "linha": indice,
                        "palavras_encontradas": ", ".join(
                            palavras_encontradas
                        ),
                        "evidencia": texto_linha[:1000],
                    }
                )


    evidencias_robustez = pd.DataFrame(
        registros_evidencias,
        columns=[
            "arquivo",
            "linha",
            "palavras_encontradas",
            "evidencia",
        ],
    )


    # ============================================================
    # LEITURA DO MODELO E DAS MÉTRICAS OFICIAIS
    # ============================================================

    ARQUIVO_MODELO = (
        PASTA_MODELO_FINAL
        / "modelo_oficial.json"
    )

    ARQUIVO_METRICAS = (
        PASTA_MODELO_FINAL
        / "metricas_modelo_oficial.json"
    )


    registros_modelo = []
    registros_metricas = []


    if ARQUIVO_MODELO.exists():

        with open(
            ARQUIVO_MODELO,
            mode="r",
            encoding="utf-8",
        ) as arquivo:

            registros_modelo = achatar_json(
                json.load(arquivo)
            )


    if ARQUIVO_METRICAS.exists():

        with open(
            ARQUIVO_METRICAS,
            mode="r",
            encoding="utf-8",
        ) as arquivo:

            registros_metricas = achatar_json(
                json.load(arquivo)
            )


    # ============================================================
    # PERÍODO DE AVALIAÇÃO
    # ============================================================

    (
        _,
        data_inicio_avaliacao,
    ) = buscar_data_json(
        registros_modelo,
        grupos_tokens=[
            [
                "inicio",
                "avaliacao",
            ],
            [
                "data",
                "inicial",
                "avaliacao",
            ],
            [
                "evaluation",
                "start",
            ],
        ],
    )


    (
        _,
        data_fim_avaliacao,
    ) = buscar_data_json(
        registros_modelo,
        grupos_tokens=[
            [
                "fim",
                "avaliacao",
            ],
            [
                "data",
                "final",
                "avaliacao",
            ],
            [
                "evaluation",
                "end",
            ],
        ],
    )


    quantidade_meses_avaliacao = np.nan


    if (
        pd.notna(data_inicio_avaliacao)
        and pd.notna(data_fim_avaliacao)
    ):

        quantidade_meses_avaliacao = len(
            pd.period_range(
                start=data_inicio_avaliacao,
                end=data_fim_avaliacao,
                freq="M",
            )
        )


    # ============================================================
    # ÍNDICES OFICIAIS
    # ============================================================

    (
        _,
        indice_modelo_oficial,
    ) = buscar_valor_json(
        registros_metricas,
        grupos_tokens=[
            [
                "indice",
                "modelo",
                "oficial",
            ],
            [
                "indice",
                "oficial",
            ],
            [
                "indice",
                "walk",
                "forward",
            ],
        ],
        exclusoes=[
            "benchmark",
            "challenger",
            "desafiante",
            "anterior",
            "fixo",
            "fixed",
        ],
    )


    (
        _,
        indice_benchmark,
    ) = buscar_valor_json(
        registros_metricas,
        grupos_tokens=[
            [
                "indice",
                "benchmark",
            ],
            [
                "benchmark",
                "final",
            ],
        ],
    )


    (
        _,
        indice_challenger,
    ) = buscar_valor_json(
        registros_metricas,
        grupos_tokens=[
            [
                "indice",
                "challenger",
            ],
            [
                "indice",
                "desafiante",
            ],
            [
                "indice",
                "modelo",
                "anterior",
            ],
        ],
    )


    diferenca_benchmark = np.nan
    diferenca_challenger = np.nan


    if (
        pd.notna(indice_modelo_oficial)
        and pd.notna(indice_benchmark)
    ):

        diferenca_benchmark = (
            indice_modelo_oficial
            - indice_benchmark
        )


    if (
        pd.notna(indice_modelo_oficial)
        and pd.notna(indice_challenger)
    ):

        diferenca_challenger = (
            indice_modelo_oficial
            - indice_challenger
        )


    # ============================================================
    # COBERTURA DOS REGIMES
    # ============================================================

    quantidade_regimes_observados = np.nan
    participacao_dois_maiores = np.nan
    arquivo_regimes_utilizado = ""


    for caminho, tabela in tabelas.items():

        if not caminho.name.startswith("07_03"):
            continue


        coluna_regime = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "regime",
                ],
            ],
        )


        coluna_quantidade = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "quantidade",
                    "mes",
                ],
                [
                    "meses",
                ],
                [
                    "quantidade",
                ],
            ],
        )


        coluna_percentual = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "percentual",
                ],
                [
                    "participacao",
                ],
                [
                    "proporcao",
                ],
            ],
        )


        if coluna_regime is None:
            continue


        tabela_regimes = tabela.copy()


        if coluna_quantidade is not None:

            quantidades = pd.to_numeric(
                tabela_regimes[
                    coluna_quantidade
                ],
                errors="coerce",
            ).fillna(0)


            quantidade_regimes_observados = int(
                (
                    quantidades > 0
                ).sum()
            )


            if quantidades.sum() > 0:

                participacoes = (
                    quantidades
                    / quantidades.sum()
                )


                participacao_dois_maiores = float(
                    participacoes
                    .nlargest(2)
                    .sum()
                )


        elif coluna_percentual is not None:

            participacoes = pd.to_numeric(
                tabela_regimes[
                    coluna_percentual
                ],
                errors="coerce",
            ).dropna()


            if not participacoes.empty:

                if participacoes.max() > 1.5:

                    participacoes = (
                        participacoes
                        / 100.0
                    )


                quantidade_regimes_observados = int(
                    (
                        participacoes > 0
                    ).sum()
                )


                participacao_dois_maiores = float(
                    participacoes
                    .nlargest(2)
                    .sum()
                )


        arquivo_regimes_utilizado = str(
            caminho.relative_to(
                RAIZ_PROJETO
            )
        )

        break


    # ============================================================
    # SENSIBILIDADE DOS PARÂMETROS
    # ============================================================

    percentual_sensibilidade_superou = np.nan
    quantidade_variantes_sensibilidade = np.nan
    arquivo_sensibilidade_utilizado = ""


    for caminho, tabela in tabelas.items():

        nome_normalizado = normalizar_texto(
            caminho.name
        )


        possui_contexto_sensibilidade = (
            caminho.name.startswith("06_10")
            or "sensibilidade" in nome_normalizado
        )


        if not possui_contexto_sensibilidade:
            continue


        coluna_superou = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "superou",
                    "benchmark",
                ],
                [
                    "acima",
                    "benchmark",
                ],
                [
                    "bateu",
                    "benchmark",
                ],
            ],
        )


        if coluna_superou is not None:

            valores_booleanos = converter_booleano(
                tabela[
                    coluna_superou
                ]
            ).dropna()


            if len(valores_booleanos) >= 3:

                percentual_sensibilidade_superou = float(
                    valores_booleanos.mean()
                )


                quantidade_variantes_sensibilidade = int(
                    len(valores_booleanos)
                )


                arquivo_sensibilidade_utilizado = str(
                    caminho.relative_to(
                        RAIZ_PROJETO
                    )
                )

                break


        coluna_indice_modelo = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "indice",
                    "modelo",
                ],
                [
                    "indice",
                    "candidato",
                ],
                [
                    "indice",
                    "estrategia",
                ],
            ],
            exclusoes=[
                "benchmark",
                "challenger",
                "anterior",
            ],
        )


        coluna_indice_benchmark = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "indice",
                    "benchmark",
                ],
            ],
        )


        if (
            coluna_indice_modelo is not None
            and coluna_indice_benchmark is not None
            and len(tabela) >= 3
        ):

            indice_modelo = pd.to_numeric(
                tabela[
                    coluna_indice_modelo
                ],
                errors="coerce",
            )


            indice_bench = pd.to_numeric(
                tabela[
                    coluna_indice_benchmark
                ],
                errors="coerce",
            )


            validos = (
                indice_modelo.notna()
                & indice_bench.notna()
            )


            if validos.sum() >= 3:

                percentual_sensibilidade_superou = float(
                    (
                        indice_modelo.loc[validos]
                        > indice_bench.loc[validos]
                    ).mean()
                )


                quantidade_variantes_sensibilidade = int(
                    validos.sum()
                )


                arquivo_sensibilidade_utilizado = str(
                    caminho.relative_to(
                        RAIZ_PROJETO
                    )
                )

                break


    # ============================================================
    # JANELAS MÓVEIS
    # ============================================================

    percentual_rolling_benchmark = np.nan
    percentual_rolling_challenger = np.nan
    quantidade_janelas_rolling = np.nan
    arquivo_rolling_utilizado = ""


    for caminho, tabela in tabelas.items():

        if not caminho.name.startswith("07_04"):
            continue


        coluna_excesso_benchmark = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "excesso",
                    "benchmark",
                ],
                [
                    "diferenca",
                    "benchmark",
                ],
            ],
        )


        coluna_excesso_challenger = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "excesso",
                    "challenger",
                ],
                [
                    "excesso",
                    "desafiante",
                ],
                [
                    "diferenca",
                    "challenger",
                ],
            ],
        )


        encontrou = False


        if coluna_excesso_benchmark is not None:

            excesso_benchmark = pd.to_numeric(
                tabela[
                    coluna_excesso_benchmark
                ],
                errors="coerce",
            ).dropna()


            if len(excesso_benchmark) >= 3:

                percentual_rolling_benchmark = float(
                    (
                        excesso_benchmark > 0
                    ).mean()
                )


                quantidade_janelas_rolling = int(
                    len(excesso_benchmark)
                )


                encontrou = True


        if coluna_excesso_challenger is not None:

            excesso_challenger = pd.to_numeric(
                tabela[
                    coluna_excesso_challenger
                ],
                errors="coerce",
            ).dropna()


            if len(excesso_challenger) >= 3:

                percentual_rolling_challenger = float(
                    (
                        excesso_challenger > 0
                    ).mean()
                )


                if pd.isna(
                    quantidade_janelas_rolling
                ):

                    quantidade_janelas_rolling = int(
                        len(excesso_challenger)
                    )


                encontrou = True


        if encontrou:

            arquivo_rolling_utilizado = str(
                caminho.relative_to(
                    RAIZ_PROJETO
                )
            )

            break


    # ============================================================
    # WALK-FORWARD POR ANO
    # ============================================================

    periodos_walk_forward_superados = np.nan
    periodos_walk_forward_total = np.nan
    percentual_periodos_walk_forward = np.nan
    arquivo_walk_forward_utilizado = ""


    for caminho, tabela in tabelas.items():

        if not caminho.name.startswith("06_11"):
            continue


        coluna_superou = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "superou",
                    "benchmark",
                ],
                [
                    "acima",
                    "benchmark",
                ],
                [
                    "bateu",
                    "benchmark",
                ],
            ],
        )


        if coluna_superou is not None:

            valores_booleanos = converter_booleano(
                tabela[
                    coluna_superou
                ]
            ).dropna()


            if 2 <= len(valores_booleanos) <= 20:

                periodos_walk_forward_superados = int(
                    valores_booleanos.sum()
                )


                periodos_walk_forward_total = int(
                    len(valores_booleanos)
                )


                percentual_periodos_walk_forward = float(
                    valores_booleanos.mean()
                )


                arquivo_walk_forward_utilizado = str(
                    caminho.relative_to(
                        RAIZ_PROJETO
                    )
                )

                break


        coluna_retorno_modelo = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "retorno",
                    "walk",
                    "forward",
                ],
                [
                    "retorno",
                    "modelo",
                ],
                [
                    "retorno",
                    "oficial",
                ],
            ],
            exclusoes=[
                "benchmark",
                "challenger",
                "anterior",
            ],
        )


        coluna_retorno_benchmark = localizar_coluna(
            tabela,
            grupos_tokens=[
                [
                    "retorno",
                    "benchmark",
                ],
            ],
        )


        if (
            coluna_retorno_modelo is not None
            and coluna_retorno_benchmark is not None
            and 2 <= len(tabela) <= 20
        ):

            retorno_modelo = pd.to_numeric(
                tabela[
                    coluna_retorno_modelo
                ],
                errors="coerce",
            )


            retorno_benchmark = pd.to_numeric(
                tabela[
                    coluna_retorno_benchmark
                ],
                errors="coerce",
            )


            validos = (
                retorno_modelo.notna()
                & retorno_benchmark.notna()
            )


            if 2 <= validos.sum() <= 20:

                comparacao = (
                    retorno_modelo.loc[validos]
                    > retorno_benchmark.loc[validos]
                )


                periodos_walk_forward_superados = int(
                    comparacao.sum()
                )


                periodos_walk_forward_total = int(
                    comparacao.size
                )


                percentual_periodos_walk_forward = float(
                    comparacao.mean()
                )


                arquivo_walk_forward_utilizado = str(
                    caminho.relative_to(
                        RAIZ_PROJETO
                    )
                )

                break


    # ============================================================
    # VERIFICAÇÃO DE HOLDOUT NÃO PRESERVADO
    # ============================================================

    texto_evidencias = " ".join(
        evidencias_robustez[
            "evidencia"
        ].astype(str).tolist()
    )


    texto_evidencias_normalizado = normalizar_texto(
        texto_evidencias
    )


    termos_holdout_inspecionado = [
        "periodo_de_avaliacao_ja_inspecionado",
        "avaliacao_ja_inspecionada",
        "nao_e_holdout",
        "nao_e_um_holdout",
        "holdout_nao_preservado",
        "periodo_ja_utilizado",
        "resultado_nao_conclusivo",
        "nao_conclusivo",
    ]


    holdout_nao_preservado = any(
        termo in texto_evidencias_normalizado
        for termo in termos_holdout_inspecionado
    )


    # ============================================================
    # INDICADORES CONSOLIDADOS
    # ============================================================

    indicadores_robustez = pd.DataFrame(
        [
            {
                "indicador": "meses_avaliacao",
                "valor": quantidade_meses_avaliacao,
                "unidade": "meses",
                "arquivo_origem": (
                    "outputs/modelo_final/modelo_oficial.json"
                ),
            },
            {
                "indicador": "indice_modelo_oficial",
                "valor": indice_modelo_oficial,
                "unidade": "indice_base_100",
                "arquivo_origem": (
                    "outputs/modelo_final/"
                    "metricas_modelo_oficial.json"
                ),
            },
            {
                "indicador": "indice_benchmark",
                "valor": indice_benchmark,
                "unidade": "indice_base_100",
                "arquivo_origem": (
                    "outputs/modelo_final/"
                    "metricas_modelo_oficial.json"
                ),
            },
            {
                "indicador": "indice_challenger",
                "valor": indice_challenger,
                "unidade": "indice_base_100",
                "arquivo_origem": (
                    "outputs/modelo_final/"
                    "metricas_modelo_oficial.json"
                ),
            },
            {
                "indicador": "diferenca_modelo_benchmark",
                "valor": diferenca_benchmark,
                "unidade": "pontos_indice",
                "arquivo_origem": (
                    "outputs/modelo_final/"
                    "metricas_modelo_oficial.json"
                ),
            },
            {
                "indicador": "diferenca_modelo_challenger",
                "valor": diferenca_challenger,
                "unidade": "pontos_indice",
                "arquivo_origem": (
                    "outputs/modelo_final/"
                    "metricas_modelo_oficial.json"
                ),
            },
            {
                "indicador": "regimes_observados",
                "valor": quantidade_regimes_observados,
                "unidade": "regimes",
                "arquivo_origem": arquivo_regimes_utilizado,
            },
            {
                "indicador": "participacao_dois_maiores_regimes",
                "valor": participacao_dois_maiores,
                "unidade": "decimal",
                "arquivo_origem": arquivo_regimes_utilizado,
            },
            {
                "indicador": "variantes_sensibilidade",
                "valor": quantidade_variantes_sensibilidade,
                "unidade": "variantes",
                "arquivo_origem": arquivo_sensibilidade_utilizado,
            },
            {
                "indicador": (
                    "percentual_sensibilidade_superou_benchmark"
                ),
                "valor": percentual_sensibilidade_superou,
                "unidade": "decimal",
                "arquivo_origem": arquivo_sensibilidade_utilizado,
            },
            {
                "indicador": "janelas_rolling",
                "valor": quantidade_janelas_rolling,
                "unidade": "janelas",
                "arquivo_origem": arquivo_rolling_utilizado,
            },
            {
                "indicador": "rolling_acima_benchmark",
                "valor": percentual_rolling_benchmark,
                "unidade": "decimal",
                "arquivo_origem": arquivo_rolling_utilizado,
            },
            {
                "indicador": "rolling_acima_challenger",
                "valor": percentual_rolling_challenger,
                "unidade": "decimal",
                "arquivo_origem": arquivo_rolling_utilizado,
            },
            {
                "indicador": "periodos_walk_forward_superados",
                "valor": periodos_walk_forward_superados,
                "unidade": "periodos",
                "arquivo_origem": arquivo_walk_forward_utilizado,
            },
            {
                "indicador": "periodos_walk_forward_total",
                "valor": periodos_walk_forward_total,
                "unidade": "periodos",
                "arquivo_origem": arquivo_walk_forward_utilizado,
            },
            {
                "indicador": "percentual_periodos_walk_forward",
                "valor": percentual_periodos_walk_forward,
                "unidade": "decimal",
                "arquivo_origem": arquivo_walk_forward_utilizado,
            },
            {
                "indicador": "holdout_nao_preservado",
                "valor": holdout_nao_preservado,
                "unidade": "booleano",
                "arquivo_origem": (
                    "Arquivos 07_05 e evidências narrativas"
                ),
            },
        ]
    )


    # ============================================================
    # CLASSIFICAÇÃO DOS RISCOS
    # ============================================================

    riscos = []


    if pd.isna(
        quantidade_meses_avaliacao
    ):

        adicionar_risco(
            lista=riscos,
            criterio="Tamanho da amostra de avaliação",
            nivel="NAO_VERIFICADO",
            evidencia=(
                "Período de avaliação não identificado."
            ),
            impacto=(
                "Não é possível medir a força temporal "
                "da evidência."
            ),
        )


    elif quantidade_meses_avaliacao < 36:

        adicionar_risco(
            lista=riscos,
            criterio="Tamanho da amostra de avaliação",
            nivel="ALTO",
            evidencia=(
                f"{int(quantidade_meses_avaliacao)} "
                "meses de avaliação."
            ),
            impacto=(
                "A amostra é curta para sustentar uma "
                "conclusão forte sobre desempenho estrutural."
            ),
        )


    else:

        adicionar_risco(
            lista=riscos,
            criterio="Tamanho da amostra de avaliação",
            nivel="BAIXO",
            evidencia=(
                f"{int(quantidade_meses_avaliacao)} "
                "meses de avaliação."
            ),
            impacto=(
                "A extensão temporal reduz, mas não elimina, "
                "o risco amostral."
            ),
        )


    if pd.isna(
        quantidade_regimes_observados
    ):

        adicionar_risco(
            lista=riscos,
            criterio="Cobertura dos regimes",
            nivel="NAO_VERIFICADO",
            evidencia=(
                "Distribuição de regimes não localizada."
            ),
            impacto=(
                "Não foi possível verificar se todos os "
                "regimes foram testados."
            ),
        )


    elif quantidade_regimes_observados < 4:

        adicionar_risco(
            lista=riscos,
            criterio="Cobertura dos regimes",
            nivel="ALTO",
            evidencia=(
                f"{int(quantidade_regimes_observados)}/4 "
                "regimes observados."
            ),
            impacto=(
                "O desempenho do modelo não foi observado "
                "em todos os estados macroeconômicos."
            ),
        )


    else:

        adicionar_risco(
            lista=riscos,
            criterio="Cobertura dos regimes",
            nivel="BAIXO",
            evidencia="4/4 regimes observados.",
            impacto=(
                "Todos os regimes apareceram no período analisado."
            ),
        )


    if pd.notna(
        participacao_dois_maiores
    ):

        if participacao_dois_maiores > 0.80:

            adicionar_risco(
                lista=riscos,
                criterio="Concentração entre regimes",
                nivel="ALTO",
                evidencia=(
                    f"Os dois maiores regimes representam "
                    f"{participacao_dois_maiores:.2%} "
                    "da avaliação."
                ),
                impacto=(
                    "O resultado depende excessivamente "
                    "de poucos ambientes macroeconômicos."
                ),
            )


        elif participacao_dois_maiores > 0.65:

            adicionar_risco(
                lista=riscos,
                criterio="Concentração entre regimes",
                nivel="MEDIO",
                evidencia=(
                    f"Os dois maiores regimes representam "
                    f"{participacao_dois_maiores:.2%} "
                    "da avaliação."
                ),
                impacto=(
                    "Há concentração relevante na amostra."
                ),
            )


        else:

            adicionar_risco(
                lista=riscos,
                criterio="Concentração entre regimes",
                nivel="BAIXO",
                evidencia=(
                    f"Os dois maiores regimes representam "
                    f"{participacao_dois_maiores:.2%} "
                    "da avaliação."
                ),
                impacto=(
                    "A distribuição entre regimes é relativamente "
                    "mais equilibrada."
                ),
            )


    if pd.isna(
        percentual_sensibilidade_superou
    ):

        adicionar_risco(
            lista=riscos,
            criterio="Sensibilidade dos parâmetros",
            nivel="NAO_VERIFICADO",
            evidencia=(
                "Tabela de sensibilidade não identificada."
            ),
            impacto=(
                "Não foi possível medir a estabilidade "
                "perante pequenas alterações."
            ),
        )


    elif percentual_sensibilidade_superou < 0.50:

        adicionar_risco(
            lista=riscos,
            criterio="Sensibilidade dos parâmetros",
            nivel="ALTO",
            evidencia=(
                f"{percentual_sensibilidade_superou:.2%} "
                "das variantes superaram o benchmark."
            ),
            impacto=(
                "O resultado depende de uma região restrita "
                "dos parâmetros, elevando o risco de overfitting."
            ),
        )


    elif percentual_sensibilidade_superou < 0.75:

        adicionar_risco(
            lista=riscos,
            criterio="Sensibilidade dos parâmetros",
            nivel="MEDIO",
            evidencia=(
                f"{percentual_sensibilidade_superou:.2%} "
                "das variantes superaram o benchmark."
            ),
            impacto=(
                "A estabilidade existe, mas ainda é limitada."
            ),
        )


    else:

        adicionar_risco(
            lista=riscos,
            criterio="Sensibilidade dos parâmetros",
            nivel="BAIXO",
            evidencia=(
                f"{percentual_sensibilidade_superou:.2%} "
                "das variantes superaram o benchmark."
            ),
            impacto=(
                "O desempenho mostrou estabilidade ampla "
                "entre as variantes testadas."
            ),
        )


    if pd.notna(
        percentual_rolling_benchmark
    ):

        nivel = (
            "BAIXO"
            if percentual_rolling_benchmark >= 0.75
            else (
                "MEDIO"
                if percentual_rolling_benchmark >= 0.50
                else "ALTO"
            )
        )


        adicionar_risco(
            lista=riscos,
            criterio="Consistência em janelas móveis contra benchmark",
            nivel=nivel,
            evidencia=(
                f"{percentual_rolling_benchmark:.2%} "
                "das janelas ficaram acima do benchmark."
            ),
            impacto=(
                "Mede se a vantagem ocorreu de forma recorrente "
                "ou ficou concentrada em poucos meses."
            ),
        )


    if pd.notna(
        percentual_rolling_challenger
    ):

        nivel = (
            "BAIXO"
            if percentual_rolling_challenger >= 0.75
            else (
                "MEDIO"
                if percentual_rolling_challenger >= 0.50
                else "ALTO"
            )
        )


        adicionar_risco(
            lista=riscos,
            criterio="Consistência em janelas móveis contra desafiante",
            nivel=nivel,
            evidencia=(
                f"{percentual_rolling_challenger:.2%} "
                "das janelas ficaram acima do desafiante."
            ),
            impacto=(
                "Verifica se o modelo oficial realmente melhora "
                "a versão anterior de forma recorrente."
            ),
        )


    if pd.notna(
        diferenca_benchmark
    ):

        adicionar_risco(
            lista=riscos,
            criterio="Resultado acumulado contra benchmark",
            nivel=(
                "BAIXO"
                if diferenca_benchmark > 0
                else "ALTO"
            ),
            evidencia=(
                f"Diferença de "
                f"{diferenca_benchmark:+.4f} "
                "pontos de índice."
            ),
            impacto=(
                "Uma vantagem pequena pode desaparecer com "
                "mudanças de custos ou da amostra."
            ),
        )


    if pd.notna(
        diferenca_challenger
    ):

        adicionar_risco(
            lista=riscos,
            criterio="Resultado acumulado contra desafiante",
            nivel=(
                "BAIXO"
                if diferenca_challenger >= 0
                else "ALTO"
            ),
            evidencia=(
                f"Diferença de "
                f"{diferenca_challenger:+.4f} "
                "pontos de índice."
            ),
            impacto=(
                "Resultado negativo indica que a versão oficial "
                "não superou a alternativa anterior em retorno."
            ),
        )


    if pd.notna(
        percentual_periodos_walk_forward
    ):

        nivel = (
            "BAIXO"
            if percentual_periodos_walk_forward >= 0.75
            else (
                "MEDIO"
                if percentual_periodos_walk_forward >= 0.50
                else "ALTO"
            )
        )


        adicionar_risco(
            lista=riscos,
            criterio="Consistência por período walk-forward",
            nivel=nivel,
            evidencia=(
                f"{int(periodos_walk_forward_superados)}/"
                f"{int(periodos_walk_forward_total)} "
                "períodos superaram o benchmark."
            ),
            impacto=(
                "Indica a estabilidade da vantagem entre "
                "recalibrações sucessivas."
            ),
        )


    adicionar_risco(
        lista=riscos,
        criterio="Preservação de holdout independente",
        nivel=(
            "ALTO"
            if holdout_nao_preservado
            else "NAO_VERIFICADO"
        ),
        evidencia=(
            "Os arquivos indicam que o período de avaliação "
            "já foi utilizado na análise e na escolha do modelo."
            if holdout_nao_preservado
            else (
                "Não foi encontrada confirmação automática "
                "de um holdout totalmente preservado."
            )
        ),
        impacto=(
            "Uma avaliação já inspecionada não representa "
            "um teste final completamente independente."
        ),
    )


    tabela_riscos = pd.DataFrame(
        riscos
    )


    # ============================================================
    # ANÁLISE DO EXCESSO DE APROVAÇÕES
    # ============================================================

    validacoes_tecnicas = status_existentes.loc[
        status_existentes[
            "tipo_validacao"
        ].eq(
            "TECNICA"
        )
    ].copy()


    quantidade_validacoes_tecnicas = len(
        validacoes_tecnicas
    )


    quantidade_tecnicas_positivas = int(
        validacoes_tecnicas[
            "classificacao_auditoria"
        ].eq(
            "POSITIVO"
        ).sum()
    )


    percentual_tecnicas_positivas = np.nan


    if quantidade_validacoes_tecnicas > 0:

        percentual_tecnicas_positivas = (
            quantidade_tecnicas_positivas
            / quantidade_validacoes_tecnicas
        )


    # ============================================================
    # VALIDAÇÕES DA ETAPA
    # ============================================================

    validacoes_auditoria = []


    adicionar_validacao(
        lista=validacoes_auditoria,
        nome="Arquivos de robustez localizados",
        status=(
            "OK"
            if len(tabelas) > 0
            else "ERRO"
        ),
        detalhe=(
            f"{len(tabelas)} arquivos lidos."
        ),
    )


    adicionar_validacao(
        lista=validacoes_auditoria,
        nome="Validações técnicas separadas da aprovação do modelo",
        status="OK",
        detalhe=(
            f"{quantidade_validacoes_tecnicas} registros técnicos "
            "foram classificados separadamente."
        ),
    )


    adicionar_validacao(
        lista=validacoes_auditoria,
        nome="Percentual elevado de OK técnicos interpretado corretamente",
        status=(
            "ATENCAO"
            if (
                pd.notna(
                    percentual_tecnicas_positivas
                )
                and percentual_tecnicas_positivas >= 0.90
            )
            else "OK"
        ),
        detalhe=(
            (
                f"{percentual_tecnicas_positivas:.2%} "
                "das validações técnicas são positivas. "
                "Isso demonstra integridade de execução, "
                "não prova qualidade econômica."
            )
            if pd.notna(
                percentual_tecnicas_positivas
            )
            else (
                "Não foi possível calcular o percentual."
            )
        ),
    )


    quantidade_riscos_altos = int(
        tabela_riscos[
            "nivel_risco"
        ].eq(
            "ALTO"
        ).sum()
    )


    quantidade_riscos_medios = int(
        tabela_riscos[
            "nivel_risco"
        ].eq(
            "MEDIO"
        ).sum()
    )


    quantidade_riscos_nao_verificados = int(
        tabela_riscos[
            "nivel_risco"
        ].eq(
            "NAO_VERIFICADO"
        ).sum()
    )


    adicionar_validacao(
        lista=validacoes_auditoria,
        nome="Riscos metodológicos identificados",
        status=(
            "ATENCAO"
            if (
                quantidade_riscos_altos > 0
                or quantidade_riscos_medios > 0
            )
            else "OK"
        ),
        detalhe=(
            f"{quantidade_riscos_altos} riscos altos, "
            f"{quantidade_riscos_medios} riscos médios e "
            f"{quantidade_riscos_nao_verificados} "
            "não verificados."
        ),
    )


    tabela_validacoes = pd.DataFrame(
        validacoes_auditoria
    )


    # ============================================================
    # SALVAMENTO
    # ============================================================

    arquivos_analisados.to_csv(
        ARQUIVO_ARQUIVOS_ANALISADOS,
        index=False,
        encoding="utf-8-sig",
    )


    status_existentes.to_csv(
        ARQUIVO_STATUS_EXISTENTES,
        index=False,
        encoding="utf-8-sig",
    )


    resumo_aprovacoes.to_csv(
        ARQUIVO_RESUMO_APROVACOES,
        index=False,
        encoding="utf-8-sig",
    )


    evidencias_robustez.to_csv(
        ARQUIVO_EVIDENCIAS,
        index=False,
        encoding="utf-8-sig",
    )


    tabela_riscos.to_csv(
        ARQUIVO_RISCOS,
        index=False,
        encoding="utf-8-sig",
    )


    indicadores_robustez.to_csv(
        ARQUIVO_INDICADORES,
        index=False,
        encoding="utf-8-sig",
    )


    tabela_validacoes.to_csv(
        ARQUIVO_VALIDACOES,
        index=False,
        encoding="utf-8-sig",
    )


    # ============================================================
    # VERIFICAÇÃO DOS ARQUIVOS SALVOS
    # ============================================================

    ARQUIVOS_GERADOS = [
        ARQUIVO_ARQUIVOS_ANALISADOS,
        ARQUIVO_STATUS_EXISTENTES,
        ARQUIVO_RESUMO_APROVACOES,
        ARQUIVO_EVIDENCIAS,
        ARQUIVO_RISCOS,
        ARQUIVO_INDICADORES,
        ARQUIVO_VALIDACOES,
    ]


    arquivos_nao_salvos = [
        arquivo
        for arquivo in ARQUIVOS_GERADOS
        if (
            not arquivo.exists()
            or arquivo.stat().st_size == 0
        )
    ]


    if arquivos_nao_salvos:

        raise FileNotFoundError(
            "Os seguintes arquivos da Etapa 5 "
            "não foram salvos corretamente:\n"
            + "\n".join(
                str(arquivo)
                for arquivo in arquivos_nao_salvos
            )
        )


    # ============================================================
    # RESULTADOS
    # ============================================================

    print("=" * 70)
    print("AUDITORIA GLOBAL — ROBUSTEZ E OVERFITTING")
    print("=" * 70)


    print(
        f"\nArquivos analisados: "
        f"{len(arquivos_analisados)}"
    )


    print(
        f"Registros de status encontrados: "
        f"{len(status_existentes)}"
    )


    print(
        f"Validações técnicas positivas: "
        f"{quantidade_tecnicas_positivas}/"
        f"{quantidade_validacoes_tecnicas}"
    )


    if pd.notna(
        percentual_tecnicas_positivas
    ):

        print(
            f"Percentual técnico positivo: "
            f"{percentual_tecnicas_positivas:.2%}"
        )


    print(
        f"\nRiscos altos: "
        f"{quantidade_riscos_altos}"
    )


    print(
        f"Riscos médios: "
        f"{quantidade_riscos_medios}"
    )


    print(
        f"Riscos não verificados: "
        f"{quantidade_riscos_nao_verificados}"
    )


    print(
        "\nIndicadores de robustez:"
    )


    display(
        indicadores_robustez
    )


    print(
        "\nResumo das aprovações existentes:"
    )


    display(
        resumo_aprovacoes
    )


    print(
        "\nRiscos metodológicos:"
    )


    display(
        tabela_riscos
    )


    print(
        "\nValidações da auditoria:"
    )


    display(
        tabela_validacoes
    )


    print(
        "\nArquivos salvos:"
    )


    for arquivo in ARQUIVOS_GERADOS:

        print(
            f"- {arquivo.relative_to(RAIZ_PROJETO)}"
        )


    print(
        "\nEsta célula não alterou dados, regras, pesos, "
        "parâmetros ou resultados do modelo."
    )


    print(
        "\nA conclusão definitiva será produzida na Etapa 6."
    )

def executar_etapa_06() -> None:
    # ============================================================
    # SCRIPT 08 — AUDITORIA GLOBAL DO PROJETO
    # ETAPA 6 — DIAGNÓSTICO FINAL CORRIGIDO E AUTÔNOMO
    #
    # Esta célula:
    # - não depende das variáveis das células anteriores;
    # - localiza os notebooks pelos nomes reais;
    # - localiza a série oficial walk-forward pelo resultado oficial;
    # - recalcula as métricas quando a série mensal é identificada;
    # - valida cada recalibração walk-forward separadamente;
    # - salva o consolidado mesmo quando alguma verificação falha;
    # - não altera dados, parâmetros, pesos ou resultados do modelo.
    # ============================================================

    from pathlib import Path
    from datetime import datetime, timezone
    import json
    import re

    import numpy as np
    import pandas as pd

    # ============================================================
    # LOCALIZAÇÃO DA RAIZ DO PROJETO
    # ============================================================

    RAIZ_PROJETO = RAIZ_GLOBAL


    PASTA_SCRIPTS = RAIZ_PROJETO / "notebooks"
    PASTA_PROCESSADOS = RAIZ_PROJETO / "data" / "processed"
    PASTA_TABELAS = RAIZ_PROJETO / "outputs" / "tabelas"
    PASTA_MODELO_FINAL = RAIZ_PROJETO / "outputs" / "modelo_final"
    PASTA_AUDITORIA = RAIZ_PROJETO / "outputs" / "auditoria"
    PASTA_AUDITORIA.mkdir(parents=True, exist_ok=True)

    ARQUIVO_MODELO = PASTA_MODELO_FINAL / "modelo_oficial.json"
    ARQUIVO_METRICAS_OFICIAIS = PASTA_MODELO_FINAL / "metricas_modelo_oficial.json"

    ARQUIVO_SCRIPTS = PASTA_AUDITORIA / "08_06_scripts_localizados_corrigido.csv"
    ARQUIVO_FONTES = PASTA_AUDITORIA / "08_06_fontes_serie_oficial_corrigido.csv"
    ARQUIVO_SERIE = PASTA_AUDITORIA / "08_06_serie_oficial_corrigida.csv"
    ARQUIVO_WALK_FORWARD = PASTA_AUDITORIA / "08_06_walk_forward_corrigido.csv"
    ARQUIVO_METRICAS = PASTA_AUDITORIA / "08_06_metricas_recalculadas_corrigido.csv"
    ARQUIVO_COMPARACAO = PASTA_AUDITORIA / "08_06_comparacao_metricas_corrigida.csv"
    ARQUIVO_ACHADOS = PASTA_AUDITORIA / "08_06_achados_consolidados_corrigido.csv"
    ARQUIVO_DIAGNOSTICO = PASTA_AUDITORIA / "08_06_diagnostico_final_corrigido.csv"
    ARQUIVO_JSON = PASTA_AUDITORIA / "08_06_diagnostico_final_corrigido.json"
    ARQUIVO_RELATORIO = PASTA_AUDITORIA / "08_06_relatorio_final_corrigido.txt"


    # ============================================================
    # FUNÇÕES AUXILIARES
    # ============================================================

    def normalizar_texto(valor) -> str:
        texto = str(valor).strip().lower()
        substituicoes = {
            "á": "a", "à": "a", "ã": "a", "â": "a",
            "é": "e", "ê": "e", "í": "i",
            "ó": "o", "ô": "o", "õ": "o",
            "ú": "u", "ç": "c",
        }
        for original, novo in substituicoes.items():
            texto = texto.replace(original, novo)
        texto = re.sub(r"[^a-z0-9]+", "_", texto)
        return texto.strip("_")


    def ler_csv_seguro(caminho: Path, nrows=None) -> pd.DataFrame:
        ultimo_erro = None
        for encoding in ["utf-8-sig", "utf-8", "latin1"]:
            try:
                return pd.read_csv(
                    caminho,
                    encoding=encoding,
                    low_memory=False,
                    nrows=nrows,
                )
            except Exception as erro:
                ultimo_erro = erro
        raise RuntimeError(f"Não foi possível ler {caminho}: {ultimo_erro}")


    def achatar_json(objeto, prefixo=""):
        registros = []
        if isinstance(objeto, dict):
            for chave, valor in objeto.items():
                nova_chave = f"{prefixo}.{chave}" if prefixo else str(chave)
                registros.extend(achatar_json(valor, nova_chave))
        elif isinstance(objeto, list):
            for indice, valor in enumerate(objeto):
                registros.extend(achatar_json(valor, f"{prefixo}[{indice}]"))
        else:
            registros.append({"chave": prefixo, "valor": objeto})
        return registros


    def localizar_data_json(registros, grupos, exclusoes=None):
        exclusoes = exclusoes or []
        for grupo in grupos:
            for registro in registros:
                chave = normalizar_texto(registro["chave"])
                if all(token in chave for token in grupo) and not any(
                    token in chave for token in exclusoes
                ):
                    data = pd.to_datetime(registro["valor"], errors="coerce")
                    if pd.notna(data):
                        return registro["chave"], data
        return None, pd.NaT


    def localizar_numero_json(registros, grupos, exclusoes=None):
        exclusoes = exclusoes or []
        for grupo in grupos:
            for registro in registros:
                chave = normalizar_texto(registro["chave"])
                if all(token in chave for token in grupo) and not any(
                    token in chave for token in exclusoes
                ):
                    valor = pd.to_numeric(
                        pd.Series([registro["valor"]]),
                        errors="coerce",
                    ).iloc[0]
                    if pd.notna(valor):
                        return registro["chave"], float(valor)
        return None, np.nan


    def localizar_coluna_data(tabela: pd.DataFrame):
        prioridades = ["data", "date", "mes", "competencia", "data_referencia"]
        mapa = {normalizar_texto(coluna): coluna for coluna in tabela.columns}
        for prioridade in prioridades:
            if prioridade in mapa:
                return mapa[prioridade]
        for nome_normalizado, nome_original in mapa.items():
            if "data" in nome_normalizado or "date" in nome_normalizado:
                return nome_original
        return None


    def localizar_coluna_tokens(tabela, grupos, exclusoes=None):
        exclusoes = exclusoes or []
        colunas = [(normalizar_texto(coluna), coluna) for coluna in tabela.columns]
        for grupo in grupos:
            candidatas = []
            for nome_normalizado, nome_original in colunas:
                if all(token in nome_normalizado for token in grupo) and not any(
                    token in nome_normalizado for token in exclusoes
                ):
                    candidatas.append((len(nome_normalizado), nome_original))
            if candidatas:
                candidatas.sort(key=lambda item: item[0])
                return candidatas[0][1]
        return None


    def ajustar_retorno_decimal(serie: pd.Series) -> pd.Series:
        resultado = pd.to_numeric(serie, errors="coerce")
        validos = resultado.dropna()
        if not validos.empty and validos.abs().quantile(0.95) > 1.5:
            resultado = resultado / 100.0
        return resultado


    def adicionar_achado(lista, categoria, item, status, severidade, detalhe):
        lista.append(
            {
                "categoria": categoria,
                "item": item,
                "status": status,
                "severidade": severidade,
                "detalhe": detalhe,
                "modelo_alterado": False,
            }
        )


    def converter_json(valor):
        if isinstance(valor, pd.Timestamp):
            return valor.isoformat()
        if isinstance(valor, (np.integer,)):
            return int(valor)
        if isinstance(valor, (np.floating,)):
            return None if np.isnan(valor) else float(valor)
        if isinstance(valor, (np.bool_,)):
            return bool(valor)
        if pd.isna(valor):
            return None
        return valor


    # ============================================================
    # ESTRUTURAS INICIAIS
    # ============================================================

    achados = []
    registros_fontes = []
    registros_walk_forward = []
    registros_comparacao = []
    registros_metricas = []

    serie_oficial = pd.DataFrame(
        columns=[
            "data",
            "retorno_oficial",
            "indice_oficial_origem",
            "indice_recalculado",
            "drawdown_recalculado",
            "turnover_mensal",
            "retorno_cdi",
        ]
    )

    tabela_walk_forward = pd.DataFrame(
        columns=[
            "arquivo",
            "linha",
            "fim_treino",
            "inicio_aplicacao",
            "ordem_temporal_valida",
            "diferenca_dias",
        ]
    )

    fontes_serie = pd.DataFrame()
    metricas_recalculadas = pd.DataFrame()
    comparacao_metricas = pd.DataFrame()

    modelo_json = {}
    metricas_json = {}
    registros_modelo = []
    registros_metricas_json = []


    # ============================================================
    # 1 — LEITURA DOS ARQUIVOS OFICIAIS
    # ============================================================

    if ARQUIVO_MODELO.exists() and ARQUIVO_MODELO.stat().st_size > 0:
        try:
            with open(ARQUIVO_MODELO, "r", encoding="utf-8") as arquivo:
                modelo_json = json.load(arquivo)
            registros_modelo = achatar_json(modelo_json)
            adicionar_achado(
                achados,
                "ARQUIVO_OFICIAL",
                "modelo_oficial.json",
                "OK",
                "BAIXA",
                str(ARQUIVO_MODELO.relative_to(RAIZ_PROJETO)),
            )
        except Exception as erro:
            adicionar_achado(
                achados,
                "ARQUIVO_OFICIAL",
                "modelo_oficial.json",
                "ERRO_LEITURA",
                "CRITICA",
                str(erro),
            )
    else:
        adicionar_achado(
            achados,
            "ARQUIVO_OFICIAL",
            "modelo_oficial.json",
            "AUSENTE_OU_VAZIO",
            "CRITICA",
            str(ARQUIVO_MODELO),
        )

    if ARQUIVO_METRICAS_OFICIAIS.exists() and ARQUIVO_METRICAS_OFICIAIS.stat().st_size > 0:
        try:
            with open(ARQUIVO_METRICAS_OFICIAIS, "r", encoding="utf-8") as arquivo:
                metricas_json = json.load(arquivo)
            registros_metricas_json = achatar_json(metricas_json)
            adicionar_achado(
                achados,
                "ARQUIVO_OFICIAL",
                "metricas_modelo_oficial.json",
                "OK",
                "BAIXA",
                str(ARQUIVO_METRICAS_OFICIAIS.relative_to(RAIZ_PROJETO)),
            )
        except Exception as erro:
            adicionar_achado(
                achados,
                "ARQUIVO_OFICIAL",
                "metricas_modelo_oficial.json",
                "ERRO_LEITURA",
                "CRITICA",
                str(erro),
            )
    else:
        adicionar_achado(
            achados,
            "ARQUIVO_OFICIAL",
            "metricas_modelo_oficial.json",
            "AUSENTE_OU_VAZIO",
            "CRITICA",
            str(ARQUIVO_METRICAS_OFICIAIS),
        )

    registros_json_combinados = registros_modelo + registros_metricas_json


    # ============================================================
    # 2 — PERÍODO OFICIAL DE AVALIAÇÃO
    # ============================================================

    _, DATA_INICIO_AVALIACAO = localizar_data_json(
        registros_json_combinados,
        [
            ["periodo", "avaliacao", "inicio"],
            ["avaliacao", "data", "inicial"],
            ["avaliacao", "inicio"],
            ["evaluation", "start"],
        ],
        exclusoes=["treino", "training", "configuracao_atual"],
    )

    _, DATA_FIM_AVALIACAO = localizar_data_json(
        registros_json_combinados,
        [
            ["periodo", "avaliacao", "fim"],
            ["avaliacao", "data", "final"],
            ["avaliacao", "fim"],
            ["evaluation", "end"],
        ],
        exclusoes=["treino", "training", "configuracao_atual"],
    )

    def inferir_periodo_avaliacao():
        candidatos_periodo = [
            PASTA_TABELAS / "06_12_series_modelos_finais.csv",
            PASTA_PROCESSADOS / "backtest_portfolio_mensal.csv",
        ]

        candidatos_periodo.extend(
            sorted(
                PASTA_TABELAS.glob(
                    "*series*walk*forward*.csv"
                )
            )
        )

        for caminho_periodo in candidatos_periodo:
            if not caminho_periodo.exists():
                continue

            try:
                tabela_periodo = ler_csv_seguro(
                    caminho_periodo
                )

                coluna_data_periodo = localizar_coluna_data(
                    tabela_periodo
                )

                if coluna_data_periodo is None:
                    continue

                datas_periodo = pd.to_datetime(
                    tabela_periodo[
                        coluna_data_periodo
                    ],
                    errors="coerce",
                ).dropna()

                if datas_periodo.empty:
                    continue

                return (
                    datas_periodo.min(),
                    datas_periodo.max(),
                    caminho_periodo,
                )

            except Exception:
                continue

        return (
            pd.NaT,
            pd.NaT,
            None,
        )


    inicio_inferido, fim_inferido, origem_periodo = (
        inferir_periodo_avaliacao()
    )

    if pd.isna(DATA_INICIO_AVALIACAO):
        DATA_INICIO_AVALIACAO = inicio_inferido

        adicionar_achado(
            achados,
            "PERIODO",
            "Data inicial da avaliação",
            (
                "INFERIDA"
                if pd.notna(
                    DATA_INICIO_AVALIACAO
                )
                else "NAO_LOCALIZADA"
            ),
            (
                "BAIXA"
                if pd.notna(
                    DATA_INICIO_AVALIACAO
                )
                else "ALTA"
            ),
            (
                f"Data inferida a partir de "
                f"{origem_periodo.relative_to(RAIZ_PROJETO)}."
                if origem_periodo is not None
                else "Não foi possível inferir a data inicial."
            ),
        )

    if pd.isna(DATA_FIM_AVALIACAO):
        DATA_FIM_AVALIACAO = fim_inferido

        adicionar_achado(
            achados,
            "PERIODO",
            "Data final da avaliação",
            (
                "INFERIDA"
                if pd.notna(
                    DATA_FIM_AVALIACAO
                )
                else "NAO_LOCALIZADA"
            ),
            (
                "BAIXA"
                if pd.notna(
                    DATA_FIM_AVALIACAO
                )
                else "ALTA"
            ),
            (
                f"Data inferida a partir de "
                f"{origem_periodo.relative_to(RAIZ_PROJETO)}."
                if origem_periodo is not None
                else "Não foi possível inferir a data final."
            ),
        )

    if pd.isna(DATA_INICIO_AVALIACAO):
        DATA_INICIO_AVALIACAO = pd.Timestamp(
            "1900-01-01"
        )

    if pd.isna(DATA_FIM_AVALIACAO):
        DATA_FIM_AVALIACAO = pd.Timestamp.today().normalize()


    # ============================================================
    # 3 — LOCALIZAÇÃO FLEXÍVEL DOS SCRIPTS 01 A 07
    # ============================================================

    arquivos_scripts = sorted(
        caminho
        for caminho in PASTA_SCRIPTS.glob(
            "*.py"
        )
        if caminho.is_file()
    )

    registros_scripts = []

    for numero in range(
        1,
        8,
    ):

        prefixo = f"{numero:02d}"

        candidatos = [
            caminho
            for caminho in arquivos_scripts
            if caminho.name.startswith(
                prefixo
            )
            and caminho.stat().st_size > 0
        ]

        candidatos = sorted(
            set(
                candidatos
            )
        )

        valido = len(
            candidatos
        ) > 0

        registros_scripts.append(
            {
                "numero_script": prefixo,
                "quantidade_encontrada": len(
                    candidatos
                ),
                "arquivos_encontrados": " | ".join(
                    caminho.name
                    for caminho in candidatos
                ),
                "script_valido": valido,
            }
        )

        adicionar_achado(
            achados,
            "ESTRUTURA",
            f"Script {prefixo}",
            (
                "OK"
                if valido
                else "NAO_LOCALIZADO"
            ),
            (
                "BAIXA"
                if valido
                else "MEDIA"
            ),
            (
                " | ".join(
                    caminho.name
                    for caminho in candidatos
                )
                if valido
                else (
                    "Nenhum arquivo correspondente "
                    "foi localizado automaticamente."
                )
            ),
        )


    tabela_scripts = pd.DataFrame(
        registros_scripts
    )


    # ============================================================
    # 4 — MÉTRICAS OFICIAIS DO JSON
    # ============================================================

    EXCLUSOES = [
        "benchmark",
        "challenger",
        "desafiante",
        "anterior",
        "sem_cdi",
        "fixo",
        "fixed",
        "estatico",
        "static",
    ]

    _, INDICE_OFICIAL_JSON = localizar_numero_json(
        registros_metricas_json,
        [
            ["indice", "modelo", "oficial"],
            ["indice", "walk", "forward"],
            ["indice", "oficial"],
            ["indice", "final"],
        ],
        exclusoes=EXCLUSOES,
    )

    if pd.isna(INDICE_OFICIAL_JSON):
        adicionar_achado(
            achados,
            "METRICA_OFICIAL",
            "Índice final oficial",
            "NAO_LOCALIZADO",
            "CRITICA",
            "Não foi possível localizar o índice final no JSON oficial.",
        )


    # ============================================================
    # 5 — LOCALIZAÇÃO DA SÉRIE OFICIAL WALK-FORWARD
    # ============================================================

    candidatos_arquivos = []
    for padrao in [
        "06_11*.csv",
        "06_12*.csv",
        "07_01*.csv",
        "07_02*.csv",
        "*walk*forward*.csv",
        "*modelo*oficial*.csv",
    ]:
        candidatos_arquivos.extend(PASTA_TABELAS.glob(padrao))

    arquivo_backtest = PASTA_PROCESSADOS / "backtest_portfolio_mensal.csv"
    if arquivo_backtest.exists():
        candidatos_arquivos.append(arquivo_backtest)

    candidatos_arquivos = sorted(set(candidatos_arquivos))
    candidatos_series = []
    tabelas_carregadas = {}

    for caminho in candidatos_arquivos:
        try:
            tabela = ler_csv_seguro(caminho)
            tabelas_carregadas[caminho] = tabela
            coluna_data = localizar_coluna_data(tabela)

            if coluna_data is None:
                registros_fontes.append(
                    {
                        "arquivo": str(caminho.relative_to(RAIZ_PROJETO)),
                        "legivel": True,
                        "coluna_data": "",
                        "tipo_candidato": "",
                        "coluna_candidata": "",
                        "indice_resultante": np.nan,
                        "diferenca_indice_oficial": np.nan,
                        "pontuacao_semantica": 0,
                        "erro": "Coluna de data não localizada",
                    }
                )
                continue

            datas = pd.to_datetime(tabela[coluna_data], errors="coerce")
            mascara = (
                datas.notna()
                & (datas >= DATA_INICIO_AVALIACAO)
                & (datas <= DATA_FIM_AVALIACAO)
            )

            if not mascara.any():
                continue

            nome_arquivo_normalizado = normalizar_texto(caminho.name)
            penalidade_arquivo = 100.0 if "backtest_portfolio_mensal" in nome_arquivo_normalizado else 0.0

            for coluna in tabela.columns:
                nome = normalizar_texto(coluna)
                if coluna == coluna_data:
                    continue

                exclusao_coluna = any(
                    termo in nome
                    for termo in [
                        "benchmark",
                        "challenger",
                        "desafiante",
                        "anterior",
                        "sem_cdi",
                        "estatico",
                        "static",
                    ]
                )
                if exclusao_coluna:
                    continue

                valores = pd.to_numeric(tabela.loc[mascara, coluna], errors="coerce")
                valores_validos = valores.dropna()
                if valores_validos.empty:
                    continue

                pontuacao_semantica = 0
                if "modelo_oficial" in nome:
                    pontuacao_semantica += 100
                if "oficial" in nome:
                    pontuacao_semantica += 70
                if "walk_forward" in nome or ("walk" in nome and "forward" in nome):
                    pontuacao_semantica += 100
                if re.search(r"(^|_)wf($|_)", nome):
                    pontuacao_semantica += 60

                if "indice" in nome or "patrimonio" in nome:
                    indice_resultante = float(valores_validos.iloc[-1])
                    diferenca = (
                        abs(indice_resultante - INDICE_OFICIAL_JSON)
                        if pd.notna(INDICE_OFICIAL_JSON)
                        else np.nan
                    )
                    candidatos_series.append(
                        {
                            "caminho": caminho,
                            "coluna_data": coluna_data,
                            "tipo": "indice",
                            "coluna": coluna,
                            "indice_resultante": indice_resultante,
                            "diferenca": diferenca,
                            "pontuacao_semantica": pontuacao_semantica,
                            "penalidade_arquivo": penalidade_arquivo,
                        }
                    )

                if "retorno" in nome or "return" in nome:
                    if nome in {"retorno_cdi", "cdi_retorno", "return_cdi"}:
                        continue
                    retornos_candidatos = ajustar_retorno_decimal(valores_validos)
                    retornos_candidatos = retornos_candidatos.dropna()
                    if retornos_candidatos.empty or (retornos_candidatos <= -1.0).any():
                        continue
                    indice_resultante = float(100.0 * (1.0 + retornos_candidatos).prod())
                    diferenca = (
                        abs(indice_resultante - INDICE_OFICIAL_JSON)
                        if pd.notna(INDICE_OFICIAL_JSON)
                        else np.nan
                    )
                    candidatos_series.append(
                        {
                            "caminho": caminho,
                            "coluna_data": coluna_data,
                            "tipo": "retorno",
                            "coluna": coluna,
                            "indice_resultante": indice_resultante,
                            "diferenca": diferenca,
                            "pontuacao_semantica": pontuacao_semantica,
                            "penalidade_arquivo": penalidade_arquivo,
                        }
                    )

        except Exception as erro:
            registros_fontes.append(
                {
                    "arquivo": str(caminho.relative_to(RAIZ_PROJETO)),
                    "legivel": False,
                    "coluna_data": "",
                    "tipo_candidato": "",
                    "coluna_candidata": "",
                    "indice_resultante": np.nan,
                    "diferenca_indice_oficial": np.nan,
                    "pontuacao_semantica": 0,
                    "erro": str(erro),
                }
            )

    for candidato in candidatos_series:
        registros_fontes.append(
            {
                "arquivo": str(candidato["caminho"].relative_to(RAIZ_PROJETO)),
                "legivel": True,
                "coluna_data": candidato["coluna_data"],
                "tipo_candidato": candidato["tipo"],
                "coluna_candidata": candidato["coluna"],
                "indice_resultante": candidato["indice_resultante"],
                "diferenca_indice_oficial": candidato["diferenca"],
                "pontuacao_semantica": candidato["pontuacao_semantica"],
                "erro": "",
            }
        )

    fontes_serie = pd.DataFrame(registros_fontes)

    candidato_selecionado = None
    CAMINHO_SERIE = None
    COLUNA_DATA = None
    COLUNA_RETORNO = None
    COLUNA_INDICE = None
    RETORNO_CONFIAVEL = False

    if candidatos_series:
        candidatos_ordenados = sorted(
            candidatos_series,
            key=lambda item: (
                np.inf if pd.isna(item["diferenca"]) else item["diferenca"],
                0 if item["tipo"] == "retorno" else 1,
                item["penalidade_arquivo"],
                -item["pontuacao_semantica"],
                str(item["caminho"]),
            ),
        )
        candidato_selecionado = candidatos_ordenados[0]
        CAMINHO_SERIE = candidato_selecionado["caminho"]
        COLUNA_DATA = candidato_selecionado["coluna_data"]

        if candidato_selecionado["tipo"] == "retorno":
            COLUNA_RETORNO = candidato_selecionado["coluna"]
            RETORNO_CONFIAVEL = True
        else:
            COLUNA_INDICE = candidato_selecionado["coluna"]

        tabela_fonte = tabelas_carregadas[CAMINHO_SERIE]
        datas = pd.to_datetime(tabela_fonte[COLUNA_DATA], errors="coerce")
        mascara = (
            datas.notna()
            & (datas >= DATA_INICIO_AVALIACAO)
            & (datas <= DATA_FIM_AVALIACAO)
        )

        serie_oficial = pd.DataFrame({"data": datas.loc[mascara]})

        if COLUNA_RETORNO is not None:
            serie_oficial["retorno_oficial"] = ajustar_retorno_decimal(
                tabela_fonte.loc[mascara, COLUNA_RETORNO]
            ).values

        if COLUNA_INDICE is not None:
            serie_oficial["indice_oficial_origem"] = pd.to_numeric(
                tabela_fonte.loc[mascara, COLUNA_INDICE],
                errors="coerce",
            ).values

            candidatos_retorno_mesmo_arquivo = [
                candidato
                for candidato in candidatos_series
                if candidato["caminho"] == CAMINHO_SERIE
                and candidato["tipo"] == "retorno"
            ]
            if candidatos_retorno_mesmo_arquivo:
                melhor_retorno = sorted(
                    candidatos_retorno_mesmo_arquivo,
                    key=lambda item: (
                        np.inf if pd.isna(item["diferenca"]) else item["diferenca"],
                        -item["pontuacao_semantica"],
                    ),
                )[0]
                if pd.isna(melhor_retorno["diferenca"]) or melhor_retorno["diferenca"] <= 0.05:
                    COLUNA_RETORNO = melhor_retorno["coluna"]
                    serie_oficial["retorno_oficial"] = ajustar_retorno_decimal(
                        tabela_fonte.loc[mascara, COLUNA_RETORNO]
                    ).values
                    RETORNO_CONFIAVEL = True

        coluna_turnover = localizar_coluna_tokens(
            tabela_fonte,
            [["turnover", "walk", "forward"], ["turnover", "oficial"], ["turnover"]],
            exclusoes=["benchmark", "challenger", "anterior", "static", "estatico"],
        )
        if coluna_turnover is not None:
            serie_oficial["turnover_mensal"] = pd.to_numeric(
                tabela_fonte.loc[mascara, coluna_turnover],
                errors="coerce",
            ).values

        coluna_cdi = localizar_coluna_tokens(
            tabela_fonte,
            [["retorno", "cdi"], ["cdi", "retorno"]],
        )
        if coluna_cdi is not None:
            serie_oficial["retorno_cdi"] = ajustar_retorno_decimal(
                tabela_fonte.loc[mascara, coluna_cdi]
            ).values

        serie_oficial = (
            serie_oficial
            .dropna(subset=["data"])
            .sort_values("data")
            .drop_duplicates(subset=["data"], keep="last")
            .reset_index(drop=True)
        )

        if "retorno_oficial" not in serie_oficial.columns and "indice_oficial_origem" in serie_oficial.columns:
            serie_oficial["retorno_oficial"] = serie_oficial["indice_oficial_origem"].pct_change()
            RETORNO_CONFIAVEL = False

        adicionar_achado(
            achados,
            "SERIE_OFICIAL",
            "Fonte da série walk-forward",
            "OK",
            "BAIXA",
            (
                f"Arquivo: {CAMINHO_SERIE.relative_to(RAIZ_PROJETO)} | "
                f"Tipo selecionado: {candidato_selecionado['tipo']} | "
                f"Coluna: {candidato_selecionado['coluna']} | "
                f"Diferença para o índice oficial: {candidato_selecionado['diferenca']}"
            ),
        )
    else:
        adicionar_achado(
            achados,
            "SERIE_OFICIAL",
            "Fonte da série walk-forward",
            "NAO_LOCALIZADA",
            "CRITICA",
            "Nenhuma coluna de retorno ou índice compatível foi encontrada nos arquivos candidatos.",
        )


    # ============================================================
    # 6 — CDI ALTERNATIVO, QUANDO NECESSÁRIO
    # ============================================================

    if not serie_oficial.empty and (
        "retorno_cdi" not in serie_oficial.columns
        or serie_oficial["retorno_cdi"].isna().all()
    ):
        for caminho_cdi in [
            PASTA_PROCESSADOS / "retornos_ativos_ampliados_mensais.csv",
            PASTA_PROCESSADOS / "retornos_ativos.csv",
        ]:
            if not caminho_cdi.exists():
                continue
            try:
                tabela_cdi = ler_csv_seguro(caminho_cdi)
                coluna_data_cdi = localizar_coluna_data(tabela_cdi)
                coluna_cdi = localizar_coluna_tokens(
                    tabela_cdi,
                    [["retorno", "cdi"], ["cdi"]],
                )
                if coluna_data_cdi is None or coluna_cdi is None:
                    continue
                auxiliar_cdi = pd.DataFrame(
                    {
                        "data": pd.to_datetime(tabela_cdi[coluna_data_cdi], errors="coerce"),
                        "retorno_cdi": ajustar_retorno_decimal(tabela_cdi[coluna_cdi]),
                    }
                )
                auxiliar_cdi = (
                    auxiliar_cdi
                    .dropna(subset=["data"])
                    .drop_duplicates(subset=["data"], keep="last")
                )
                serie_oficial = serie_oficial.drop(columns=["retorno_cdi"], errors="ignore")
                serie_oficial = serie_oficial.merge(auxiliar_cdi, on="data", how="left")
                break
            except Exception:
                continue


    # ============================================================
    # 7 — RECÁLCULO DAS MÉTRICAS
    # ============================================================

    valores_recalculados = {
        "indice_final": np.nan,
        "retorno_anualizado": np.nan,
        "volatilidade_anualizada": np.nan,
        "retorno_volatilidade": np.nan,
        "sharpe_excesso_cdi": np.nan,
        "sortino_excesso_cdi": np.nan,
        "calmar": np.nan,
        "drawdown_maximo": np.nan,
        "turnover_total": np.nan,
    }

    if not serie_oficial.empty and "retorno_oficial" in serie_oficial.columns:
        serie_oficial["retorno_oficial"] = pd.to_numeric(
            serie_oficial["retorno_oficial"],
            errors="coerce",
        )
        serie_oficial = serie_oficial.dropna(subset=["retorno_oficial"]).reset_index(drop=True)

        retornos = serie_oficial["retorno_oficial"]
        if not retornos.empty and (retornos > -1.0).all():
            produto = float((1.0 + retornos).prod())
            quantidade_meses = len(retornos)
            indice_recalculado = float(100.0 * produto)
            retorno_anualizado = float(produto ** (12.0 / quantidade_meses) - 1.0)
            volatilidade_anualizada = float(retornos.std(ddof=1) * np.sqrt(12.0))
            retorno_volatilidade = (
                retorno_anualizado / volatilidade_anualizada
                if volatilidade_anualizada > 0
                else np.nan
            )

            serie_oficial["indice_recalculado"] = 100.0 * (1.0 + retornos).cumprod()
            serie_oficial["pico_recalculado"] = serie_oficial["indice_recalculado"].cummax()
            serie_oficial["drawdown_recalculado"] = (
                serie_oficial["indice_recalculado"]
                / serie_oficial["pico_recalculado"]
                - 1.0
            )
            drawdown_maximo = float(serie_oficial["drawdown_recalculado"].min())
            calmar = (
                retorno_anualizado / abs(drawdown_maximo)
                if drawdown_maximo < 0
                else np.nan
            )

            turnover_total = np.nan
            if "turnover_mensal" in serie_oficial.columns:
                turnover_total = float(
                    pd.to_numeric(serie_oficial["turnover_mensal"], errors="coerce")
                    .fillna(0.0)
                    .sum()
                )

            sharpe = np.nan
            sortino = np.nan
            if "retorno_cdi" in serie_oficial.columns:
                base_excesso = serie_oficial[["retorno_oficial", "retorno_cdi"]].copy()
                base_excesso["retorno_cdi"] = pd.to_numeric(
                    base_excesso["retorno_cdi"],
                    errors="coerce",
                )
                base_excesso = base_excesso.dropna()
                if len(base_excesso) >= 2:
                    excesso = base_excesso["retorno_oficial"] - base_excesso["retorno_cdi"]
                    desvio = excesso.std(ddof=1)
                    if desvio > 0:
                        sharpe = float(excesso.mean() / desvio * np.sqrt(12.0))
                    downside = float(np.sqrt(np.mean(np.minimum(excesso, 0.0) ** 2)))
                    if downside > 0:
                        sortino = float(excesso.mean() / downside * np.sqrt(12.0))

            valores_recalculados.update(
                {
                    "indice_final": indice_recalculado,
                    "retorno_anualizado": retorno_anualizado,
                    "volatilidade_anualizada": volatilidade_anualizada,
                    "retorno_volatilidade": retorno_volatilidade,
                    "sharpe_excesso_cdi": sharpe,
                    "sortino_excesso_cdi": sortino,
                    "calmar": calmar,
                    "drawdown_maximo": drawdown_maximo,
                    "turnover_total": turnover_total,
                }
            )


    # ============================================================
    # 8 — COMPARAÇÃO COM O JSON OFICIAL
    # ============================================================

    configuracao_metricas = {
        "indice_final": {
            "grupos": [["indice", "modelo", "oficial"], ["indice", "walk", "forward"], ["indice", "oficial"], ["indice", "final"]],
            "escalas": [1.0],
            "tolerancia": 0.02,
            "critica": True,
        },
        "retorno_anualizado": {
            "grupos": [["retorno", "anualizado"], ["retorno", "anual"]],
            "escalas": [1.0, 0.01, 100.0],
            "tolerancia": 0.0005,
            "critica": RETORNO_CONFIAVEL,
        },
        "volatilidade_anualizada": {
            "grupos": [["volatilidade", "anualizada"], ["volatilidade", "anual"]],
            "escalas": [1.0, 0.01, 100.0],
            "tolerancia": 0.0005,
            "critica": RETORNO_CONFIAVEL,
        },
        "retorno_volatilidade": {
            "grupos": [["retorno", "volatilidade"], ["return", "vol"]],
            "escalas": [1.0],
            "tolerancia": 0.01,
            "critica": False,
        },
        "sharpe_excesso_cdi": {
            "grupos": [["sharpe", "excesso", "cdi"], ["sharpe", "cdi"], ["sharpe"]],
            "escalas": [1.0],
            "tolerancia": 0.03,
            "critica": False,
        },
        "sortino_excesso_cdi": {
            "grupos": [["sortino", "excesso", "cdi"], ["sortino", "cdi"], ["sortino"]],
            "escalas": [1.0],
            "tolerancia": 0.05,
            "critica": False,
        },
        "calmar": {
            "grupos": [["calmar"]],
            "escalas": [1.0],
            "tolerancia": 0.10,
            "critica": False,
        },
        "drawdown_maximo": {
            "grupos": [["drawdown", "maximo"], ["max", "drawdown"]],
            "escalas": [1.0, 0.01, 100.0],
            "tolerancia": 0.0005,
            "critica": RETORNO_CONFIAVEL,
        },
        "turnover_total": {
            "grupos": [["turnover", "total"], ["turnover"]],
            "escalas": [1.0],
            "tolerancia": 0.05,
            "critica": False,
        },
    }

    for nome_metrica, configuracao in configuracao_metricas.items():
        valor_recalculado = valores_recalculados[nome_metrica]
        chave_json, valor_json = localizar_numero_json(
            registros_metricas_json,
            configuracao["grupos"],
            exclusoes=EXCLUSOES,
        )

        registros_metricas.append(
            {
                "metrica": nome_metrica,
                "valor_recalculado": valor_recalculado,
                "chave_json": chave_json or "",
                "valor_json_original": valor_json,
            }
        )

        if pd.isna(valor_recalculado):
            status = "NAO_RECALCULADA"
            valor_ajustado = np.nan
            escala = np.nan
            diferenca = np.nan
            severidade = "MEDIA"
        elif pd.isna(valor_json):
            status = "NAO_LOCALIZADA_NO_JSON"
            valor_ajustado = np.nan
            escala = np.nan
            diferenca = np.nan
            severidade = "MEDIA"
        else:
            candidatos_escala = []
            for escala_teste in configuracao["escalas"]:
                ajustado = valor_json * escala_teste
                candidatos_escala.append(
                    {
                        "escala": escala_teste,
                        "ajustado": ajustado,
                        "diferenca": abs(valor_recalculado - ajustado),
                    }
                )
            melhor = min(candidatos_escala, key=lambda item: item["diferenca"])
            valor_ajustado = melhor["ajustado"]
            escala = melhor["escala"]
            diferenca = melhor["diferenca"]
            status = "OK" if diferenca <= configuracao["tolerancia"] else "DIVERGENTE"
            severidade = (
                "BAIXA"
                if status == "OK"
                else ("CRITICA" if configuracao["critica"] else "ALTA")
            )

        registros_comparacao.append(
            {
                "metrica": nome_metrica,
                "valor_recalculado": valor_recalculado,
                "chave_json": chave_json or "",
                "valor_json_original": valor_json,
                "valor_json_ajustado": valor_ajustado,
                "escala_json": escala,
                "diferenca_absoluta": diferenca,
                "tolerancia": configuracao["tolerancia"],
                "status": status,
                "metrica_critica": configuracao["critica"],
            }
        )

        adicionar_achado(
            achados,
            "METRICA",
            nome_metrica,
            status,
            severidade,
            (
                f"Recalculado={valor_recalculado} | JSON={valor_ajustado} | "
                f"Diferença={diferenca} | Tolerância={configuracao['tolerancia']}"
            ),
        )

    metricas_recalculadas = pd.DataFrame(registros_metricas)
    comparacao_metricas = pd.DataFrame(registros_comparacao)


    # ============================================================
    # 9 — WALK-FORWARD POR RECALIBRAÇÃO
    # ============================================================

    arquivos_walk_forward = sorted(
        set(
            list(PASTA_TABELAS.glob("06_11*.csv"))
            + list(PASTA_TABELAS.glob("*recalibr*.csv"))
            + list(PASTA_TABELAS.glob("*walk*forward*.csv"))
        )
    )

    for caminho in arquivos_walk_forward:
        try:
            tabela = ler_csv_seguro(caminho)
            coluna_fim_treino = localizar_coluna_tokens(
                tabela,
                [
                    ["data", "final", "treino"],
                    ["fim", "treino"],
                    ["train", "end"],
                ],
            )
            coluna_inicio_aplicacao = localizar_coluna_tokens(
                tabela,
                [
                    ["data", "inicial", "aplicacao"],
                    ["inicio", "aplicacao"],
                    ["inicio", "avaliacao"],
                    ["apply", "start"],
                ],
            )
            if coluna_fim_treino is None or coluna_inicio_aplicacao is None:
                continue

            registros_arquivo = []
            for indice, linha in tabela.iterrows():
                fim_treino = pd.to_datetime(linha[coluna_fim_treino], errors="coerce")
                inicio_aplicacao = pd.to_datetime(linha[coluna_inicio_aplicacao], errors="coerce")
                if pd.isna(fim_treino) or pd.isna(inicio_aplicacao):
                    continue
                registros_arquivo.append(
                    {
                        "arquivo": str(caminho.relative_to(RAIZ_PROJETO)),
                        "linha": indice,
                        "fim_treino": fim_treino,
                        "inicio_aplicacao": inicio_aplicacao,
                        "ordem_temporal_valida": fim_treino < inicio_aplicacao,
                        "diferenca_dias": (inicio_aplicacao - fim_treino).days,
                    }
                )

            if registros_arquivo:
                registros_walk_forward.extend(registros_arquivo)
                break
        except Exception:
            continue

    tabela_walk_forward = pd.DataFrame(
        registros_walk_forward,
        columns=[
            "arquivo",
            "linha",
            "fim_treino",
            "inicio_aplicacao",
            "ordem_temporal_valida",
            "diferenca_dias",
        ],
    )

    if tabela_walk_forward.empty:
        adicionar_achado(
            achados,
            "VAZAMENTO_TEMPORAL",
            "Ordem das recalibrações walk-forward",
            "NAO_VERIFICADA",
            "MEDIA",
            "A tabela de treino e aplicação não foi localizada automaticamente.",
        )
    else:
        validas = int(tabela_walk_forward["ordem_temporal_valida"].sum())
        total = len(tabela_walk_forward)
        correto = validas == total
        adicionar_achado(
            achados,
            "VAZAMENTO_TEMPORAL",
            "Treino anterior à aplicação em cada recalibração",
            "OK" if correto else "ERRO",
            "BAIXA" if correto else "CRITICA",
            f"{validas}/{total} recalibrações com ordem temporal válida.",
        )


    # ============================================================
    # 10 — RISCOS METODOLÓGICOS DA ETAPA 5
    # ============================================================

    arquivo_riscos = PASTA_AUDITORIA / "08_05_riscos_overfitting.csv"
    if arquivo_riscos.exists() and arquivo_riscos.stat().st_size > 0:
        try:
            tabela_riscos = ler_csv_seguro(arquivo_riscos)
            coluna_criterio = localizar_coluna_tokens(tabela_riscos, [["criterio"]])
            coluna_nivel = localizar_coluna_tokens(tabela_riscos, [["nivel", "risco"], ["nivel"]])
            coluna_evidencia = localizar_coluna_tokens(tabela_riscos, [["evidencia"]])

            if coluna_criterio is not None and coluna_nivel is not None:
                for _, linha in tabela_riscos.iterrows():
                    nivel = normalizar_texto(linha[coluna_nivel])
                    severidade = {
                        "alto": "ALTA",
                        "medio": "MEDIA",
                        "baixo": "BAIXA",
                        "nao_verificado": "MEDIA",
                    }.get(nivel, "MEDIA")
                    detalhe = (
                        str(linha[coluna_evidencia])
                        if coluna_evidencia is not None
                        else ""
                    )
                    adicionar_achado(
                        achados,
                        "RISCO_METODOLOGICO",
                        str(linha[coluna_criterio]),
                        str(linha[coluna_nivel]),
                        severidade,
                        detalhe,
                    )
        except Exception as erro:
            adicionar_achado(
                achados,
                "RISCO_METODOLOGICO",
                "Leitura da auditoria de robustez",
                "NAO_VERIFICADA",
                "MEDIA",
                str(erro),
            )


    # ============================================================
    # 11 — RESSALVAS E DIAGNÓSTICO FINAL
    # ============================================================

    if not serie_oficial.empty:
        quantidade_meses = int(serie_oficial["retorno_oficial"].notna().sum())
        if quantidade_meses < 36:
            adicionar_achado(
                achados,
                "RISCO_METODOLOGICO",
                "Tamanho da avaliação",
                "RESSALVA",
                "ALTA",
                f"A avaliação possui {quantidade_meses} retornos mensais; a amostra ainda é curta.",
            )

    adicionar_achado(
        achados,
        "RISCO_METODOLOGICO",
        "Holdout final independente",
        "RESSALVA",
        "ALTA",
        (
            f"O período de {DATA_INICIO_AVALIACAO:%Y-%m-%d} a "f"{DATA_FIM_AVALIACAO:%Y-%m-%d} já foi analisado durante o desenvolvimento; "
            "não representa um holdout final totalmente preservado."
        ),
    )

    achados_corrigidos = pd.DataFrame(achados)

    ordem = {"CRITICA": 1, "ALTA": 2, "MEDIA": 3, "BAIXA": 4}
    achados_corrigidos["ordem"] = achados_corrigidos["severidade"].map(ordem).fillna(5)
    achados_corrigidos = (
        achados_corrigidos
        .sort_values(["ordem", "categoria", "item"])
        .drop(columns=["ordem"])
        .reset_index(drop=True)
    )

    quantidade_criticos = int(achados_corrigidos["severidade"].eq("CRITICA").sum())
    quantidade_altos = int(achados_corrigidos["severidade"].eq("ALTA").sum())
    quantidade_medios = int(achados_corrigidos["severidade"].eq("MEDIA").sum())
    quantidade_baixos = int(achados_corrigidos["severidade"].eq("BAIXA").sum())

    if quantidade_criticos > 0:
        CLASSIFICACAO_FINAL = "REPROVADO"
        STATUS_OPERACIONAL = "CORREÇÃO OBRIGATÓRIA ANTES DA EXECUÇÃO INTEGRAL"
        CONCLUSAO = (
            "A auditoria corrigida encontrou ao menos um erro crítico real. "
            "Analise os achados críticos antes de executar o pipeline integral."
        )
        PROXIMA_ETAPA = "Corrigir os achados críticos restantes e executar novamente o script 08."
    elif quantidade_altos > 0 or quantidade_medios > 0:
        CLASSIFICACAO_FINAL = "APROVADO COM RESSALVAS"
        STATUS_OPERACIONAL = "APTO PARA EXECUÇÃO COMO MODELO EXPERIMENTAL"
        CONCLUSAO = (
            "A auditoria corrigida não encontrou erro crítico suficiente para impedir a modularização. "
            "O modelo permanece promissor, mas não conclusivo devido aos riscos metodológicos registrados."
        )
        PROXIMA_ETAPA = (
            "Manter a lógica validada, preservar o config.yaml e executar o pipeline integral, "
            "sem alterar pesos, regras ou resultados históricos."
        )
    else:
        CLASSIFICACAO_FINAL = "APROVADO"
        STATUS_OPERACIONAL = "APTO PARA EXECUÇÃO INTEGRAL"
        CONCLUSAO = "A auditoria corrigida não encontrou erro técnico ou metodológico relevante."
        PROXIMA_ETAPA = "Executar o pipeline integral e preservar os arquivos auditados."

    data_hora_utc = datetime.now(timezone.utc)
    fonte_serie_texto = (
        str(CAMINHO_SERIE.relative_to(RAIZ_PROJETO))
        if CAMINHO_SERIE is not None
        else ""
    )

    diagnostico_final = pd.DataFrame(
        [
            {
                "data_hora_utc": data_hora_utc.isoformat(),
                "classificacao_final": CLASSIFICACAO_FINAL,
                "status_operacional": STATUS_OPERACIONAL,
                "achados_criticos": quantidade_criticos,
                "achados_altos": quantidade_altos,
                "achados_medios": quantidade_medios,
                "achados_baixos": quantidade_baixos,
                "fonte_serie_oficial": fonte_serie_texto,
                "data_inicio_avaliacao": DATA_INICIO_AVALIACAO,
                "data_fim_avaliacao": DATA_FIM_AVALIACAO,
                "retorno_confiavel": RETORNO_CONFIAVEL,
                "conclusao": CONCLUSAO,
                "proxima_etapa": PROXIMA_ETAPA,
                "modelo_alterado": False,
            }
        ]
    )


    # ============================================================
    # 12 — SALVAMENTO GARANTIDO
    # ============================================================

    if fontes_serie.empty:
        fontes_serie = pd.DataFrame(
            columns=[
                "arquivo",
                "legivel",
                "coluna_data",
                "tipo_candidato",
                "coluna_candidata",
                "indice_resultante",
                "diferenca_indice_oficial",
                "pontuacao_semantica",
                "erro",
            ]
        )

    if metricas_recalculadas.empty:
        metricas_recalculadas = pd.DataFrame(
            columns=["metrica", "valor_recalculado", "chave_json", "valor_json_original"]
        )

    if comparacao_metricas.empty:
        comparacao_metricas = pd.DataFrame(
            columns=[
                "metrica",
                "valor_recalculado",
                "chave_json",
                "valor_json_original",
                "valor_json_ajustado",
                "escala_json",
                "diferenca_absoluta",
                "tolerancia",
                "status",
                "metrica_critica",
            ]
        )

    # O arquivo consolidado é salvo primeiro para existir mesmo se outro salvamento falhar.
    achados_corrigidos.to_csv(
        ARQUIVO_ACHADOS,
        index=False,
        encoding="utf-8-sig",
    )

    tabela_scripts.to_csv(ARQUIVO_SCRIPTS, index=False, encoding="utf-8-sig")
    fontes_serie.to_csv(ARQUIVO_FONTES, index=False, encoding="utf-8-sig")
    serie_oficial.to_csv(
        ARQUIVO_SERIE,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )
    tabela_walk_forward.to_csv(
        ARQUIVO_WALK_FORWARD,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )
    metricas_recalculadas.to_csv(ARQUIVO_METRICAS, index=False, encoding="utf-8-sig")
    comparacao_metricas.to_csv(ARQUIVO_COMPARACAO, index=False, encoding="utf-8-sig")
    diagnostico_final.to_csv(
        ARQUIVO_DIAGNOSTICO,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )

    diagnostico_json = {
        chave: converter_json(valor)
        for chave, valor in diagnostico_final.iloc[0].to_dict().items()
    }
    diagnostico_json["achados"] = {
        "criticos": quantidade_criticos,
        "altos": quantidade_altos,
        "medios": quantidade_medios,
        "baixos": quantidade_baixos,
    }

    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(diagnostico_json, arquivo, ensure_ascii=False, indent=4)

    linhas_relatorio = [
        "=" * 78,
        "AUDITORIA GLOBAL CORRIGIDA",
        "=" * 78,
        "",
        f"Data UTC: {data_hora_utc.isoformat()}",
        f"Classificação final: {CLASSIFICACAO_FINAL}",
        f"Status operacional: {STATUS_OPERACIONAL}",
        "",
        f"Críticos: {quantidade_criticos}",
        f"Altos: {quantidade_altos}",
        f"Médios: {quantidade_medios}",
        f"Baixos: {quantidade_baixos}",
        "",
        f"Fonte da série oficial: {fonte_serie_texto}",
        f"Período: {DATA_INICIO_AVALIACAO:%Y-%m-%d} a {DATA_FIM_AVALIACAO:%Y-%m-%d}",
        "",
        "CONCLUSÃO",
        CONCLUSAO,
        "",
        "PRÓXIMA ETAPA",
        PROXIMA_ETAPA,
        "",
        "A auditoria não alterou dados, parâmetros, pesos ou resultados históricos.",
    ]

    with open(ARQUIVO_RELATORIO, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(linhas_relatorio))


    # ============================================================
    # 13 — RESULTADOS
    # ============================================================

    print("=" * 78)
    print("AUDITORIA GLOBAL CORRIGIDA — CONCLUÍDA")
    print("=" * 78)
    print(f"\nClassificação final:\n{CLASSIFICACAO_FINAL}")
    print(f"\nStatus operacional:\n{STATUS_OPERACIONAL}")
    print("\nAchados:")
    print(f"- Críticos: {quantidade_criticos}")
    print(f"- Altos: {quantidade_altos}")
    print(f"- Médios: {quantidade_medios}")
    print(f"- Baixos: {quantidade_baixos}")
    print(f"\nFonte da série oficial:\n{fonte_serie_texto or 'Não localizada'}")
    print(
        f"\nPeríodo utilizado:\n"
        f"{DATA_INICIO_AVALIACAO:%Y-%m-%d} a {DATA_FIM_AVALIACAO:%Y-%m-%d}"
    )
    print(f"\nConclusão:\n{CONCLUSAO}")
    print(f"\nPróxima etapa:\n{PROXIMA_ETAPA}")

    print("\nAchados corrigidos:")
    display(achados_corrigidos)

    print("\nComparação das métricas:")
    display(comparacao_metricas)

    print("\nVerificação walk-forward:")
    display(tabela_walk_forward)

    print("\nDiagnóstico final:")
    display(diagnostico_final)

    print("\nArquivos salvos:")
    for arquivo in [
        ARQUIVO_ACHADOS,
        ARQUIVO_SCRIPTS,
        ARQUIVO_FONTES,
        ARQUIVO_SERIE,
        ARQUIVO_WALK_FORWARD,
        ARQUIVO_METRICAS,
        ARQUIVO_COMPARACAO,
        ARQUIVO_DIAGNOSTICO,
        ARQUIVO_JSON,
        ARQUIVO_RELATORIO,
    ]:
        print(f"- {arquivo.relative_to(RAIZ_PROJETO)}")

    print("\nNenhum dado, parâmetro, peso, sinal ou resultado histórico foi alterado.")

def executar_etapa_07() -> None:
    import pandas as pd


    RAIZ_PROJETO = RAIZ_GLOBAL

    ARQUIVO_ACHADOS_CORRIGIDOS = (
        RAIZ_PROJETO
        / "outputs"
        / "auditoria"
        / "08_06_achados_consolidados_corrigido.csv"
    )

    if not ARQUIVO_ACHADOS_CORRIGIDOS.exists():
        raise FileNotFoundError(
            "O resultado corrigido ainda não existe.\n"
            "Execute primeiro a Etapa 6 inteira.\n\n"
            f"Arquivo esperado:\n{ARQUIVO_ACHADOS_CORRIGIDOS}"
        )


    achados_corrigidos = pd.read_csv(
        ARQUIVO_ACHADOS_CORRIGIDOS,
        encoding="utf-8-sig",
    )

    COLUNAS_OBRIGATORIAS = [
        "categoria",
        "item",
        "status",
        "severidade",
        "detalhe",
    ]

    colunas_ausentes = [
        coluna
        for coluna in COLUNAS_OBRIGATORIAS
        if coluna not in achados_corrigidos.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            "O arquivo corrigido não possui as colunas esperadas:\n"
            f"{colunas_ausentes}"
        )


    achados_criticos = (
        achados_corrigidos.loc[
            achados_corrigidos[
                "severidade"
            ].eq(
                "CRITICA"
            )
        ]
        .reset_index(
            drop=True
        )
    )

    achados_altos = (
        achados_corrigidos.loc[
            achados_corrigidos[
                "severidade"
            ].eq(
                "ALTA"
            )
        ]
        .reset_index(
            drop=True
        )
    )

    achados_medios = (
        achados_corrigidos.loc[
            achados_corrigidos[
                "severidade"
            ].eq(
                "MEDIA"
            )
        ]
        .reset_index(
            drop=True
        )
    )


    print("=" * 78)
    print("ACHADOS DA AUDITORIA CORRIGIDA")
    print("=" * 78)

    print(
        f"\nArquivo utilizado:\n"
        f"{ARQUIVO_ACHADOS_CORRIGIDOS.relative_to(RAIZ_PROJETO)}"
    )

    print(
        f"\nCríticos: {len(achados_criticos)}"
    )

    print(
        f"Altos: {len(achados_altos)}"
    )

    print(
        f"Médios: {len(achados_medios)}"
    )

    if not achados_criticos.empty:

        print(
            "\nACHADOS CRÍTICOS:"
        )

        display(
            achados_criticos[
                COLUNAS_OBRIGATORIAS
            ]
        )

    else:

        print(
            "\nNenhum achado crítico foi encontrado "
            "na auditoria corrigida."
        )

    if not achados_altos.empty:

        print(
            "\nRESSALVAS ALTAS:"
        )

        display(
            achados_altos[
                COLUNAS_OBRIGATORIAS
            ]
        )

    if not achados_medios.empty:

        print(
            "\nRESSALVAS MÉDIAS:"
        )

        display(
            achados_medios[
                COLUNAS_OBRIGATORIAS
            ]
        )



FIM_EXECUCAO_UTC = datetime.now(timezone.utc)

print("=" * 80)
print("ANÁLISE DOS RESULTADOS FINAIS CONCLUÍDA")
print(
    "Duração total: "
    f"{(FIM_EXECUCAO_UTC - INICIO_EXECUCAO_UTC).total_seconds():.2f}s"
)
print("=" * 80)
