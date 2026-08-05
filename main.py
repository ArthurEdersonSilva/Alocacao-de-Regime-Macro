from __future__ import annotations

import argparse
import csv
import logging
import os
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

import yaml


# ============================================================
# ESTRUTURAS
# ============================================================

@dataclass(frozen=True)
class TarefaExecucao:
    """Representa um arquivo Python que pode atender uma ou mais etapas."""

    etapas: tuple[str, ...]
    arquivo: Path
    ordem: int
    critica: bool


# ============================================================
# CAMINHOS E CONFIGURAÇÃO
# ============================================================

RAIZ_PROJETO = Path(__file__).resolve().parent
ARQUIVO_CONFIG_PADRAO = RAIZ_PROJETO / "config" / "config.yaml"


def carregar_configuracao(caminho: Path) -> dict[str, Any]:
    """Carrega e valida a estrutura básica do config.yaml."""

    if not caminho.is_file():
        raise FileNotFoundError(
            f"Arquivo de configuração não encontrado: {caminho}"
        )

    with caminho.open("r", encoding="utf-8") as arquivo:
        configuracao = yaml.safe_load(arquivo) or {}

    if not isinstance(configuracao, dict):
        raise TypeError("O config.yaml deve possuir um dicionário na raiz.")

    execucao = configuracao.get("execucao")
    if not isinstance(execucao, dict):
        raise KeyError("A seção obrigatória 'execucao' não foi encontrada.")

    etapas = execucao.get("etapas")
    if not isinstance(etapas, dict) or not etapas:
        raise KeyError(
            "A seção 'execucao.etapas' deve possuir ao menos uma etapa."
        )

    return configuracao


def resolver_caminho(caminho: str | Path) -> Path:
    """Resolve um caminho relativo a partir da raiz do projeto."""

    caminho_resolvido = Path(caminho)

    if not caminho_resolvido.is_absolute():
        caminho_resolvido = RAIZ_PROJETO / caminho_resolvido

    return caminho_resolvido.resolve()


# ============================================================
# LOGS
# ============================================================

def configurar_logger(configuracao: dict[str, Any]) -> logging.Logger:
    """Configura logs no console e em arquivo com rotação."""

    config_logs = configuracao.get("logs", {})
    nivel_texto = str(config_logs.get("nivel", "INFO")).upper()
    nivel = getattr(logging, nivel_texto, logging.INFO)

    logger = logging.getLogger("alocacao_regimes_macro")
    logger.setLevel(nivel)
    logger.handlers.clear()
    logger.propagate = False

    formatador = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if bool(config_logs.get("registrar_console", True)):
        manipulador_console = logging.StreamHandler(sys.stdout)
        manipulador_console.setFormatter(formatador)
        manipulador_console.setLevel(nivel)
        logger.addHandler(manipulador_console)

    if bool(config_logs.get("registrar_arquivo", True)):
        diretorio_logs = resolver_caminho(
            config_logs.get("diretorio", "outputs/logs")
        )
        diretorio_logs.mkdir(parents=True, exist_ok=True)

        arquivo_log = diretorio_logs / str(
            config_logs.get("arquivo", "execucao.log")
        )

        config_rotacao = config_logs.get("rotacao", {})
        usar_rotacao = bool(config_rotacao.get("ativo", True))

        if usar_rotacao:
            tamanho_maximo_mb = float(
                config_rotacao.get("tamanho_maximo_mb", 10)
            )
            quantidade_backups = int(
                config_rotacao.get("quantidade_backups", 5)
            )

            manipulador_arquivo = RotatingFileHandler(
                arquivo_log,
                maxBytes=int(tamanho_maximo_mb * 1024 * 1024),
                backupCount=quantidade_backups,
                encoding="utf-8",
            )
        else:
            manipulador_arquivo = logging.FileHandler(
                arquivo_log,
                encoding="utf-8",
            )

        manipulador_arquivo.setFormatter(formatador)
        manipulador_arquivo.setLevel(nivel)
        logger.addHandler(manipulador_arquivo)

    return logger


# ============================================================
# ETAPAS
# ============================================================

def montar_tarefas(
    configuracao: dict[str, Any],
    somente_etapas: set[str] | None = None,
) -> list[TarefaExecucao]:
    """
    Converte execucao.etapas em tarefas executáveis.

    Quando duas etapas apontam para o mesmo arquivo, o arquivo é executado
    apenas uma vez e as etapas são agrupadas.
    """

    etapas_config = configuracao["execucao"]["etapas"]
    tarefas_por_arquivo: dict[Path, dict[str, Any]] = {}

    for posicao, (nome_etapa, dados_etapa) in enumerate(
        etapas_config.items(),
        start=1,
    ):
        if not isinstance(dados_etapa, dict):
            raise TypeError(
                f"A etapa '{nome_etapa}' deve ser um dicionário."
            )

        ativa = bool(dados_etapa.get("ativo", False))

        if somente_etapas is not None:
            ativa = nome_etapa in somente_etapas

        if not ativa:
            continue

        arquivo_config = dados_etapa.get("arquivo")
        if not arquivo_config:
            raise KeyError(
                f"A etapa ativa '{nome_etapa}' está sem a chave 'arquivo'."
            )

        arquivo = resolver_caminho(str(arquivo_config))
        ordem = int(dados_etapa.get("ordem", posicao * 10))
        critica = bool(dados_etapa.get("critica", True))

        if arquivo not in tarefas_por_arquivo:
            tarefas_por_arquivo[arquivo] = {
                "etapas": [nome_etapa],
                "ordem": ordem,
                "critica": critica,
            }
        else:
            tarefas_por_arquivo[arquivo]["etapas"].append(nome_etapa)
            tarefas_por_arquivo[arquivo]["ordem"] = min(
                tarefas_por_arquivo[arquivo]["ordem"],
                ordem,
            )
            tarefas_por_arquivo[arquivo]["critica"] = (
                tarefas_por_arquivo[arquivo]["critica"] or critica
            )

    tarefas = [
        TarefaExecucao(
            etapas=tuple(dados["etapas"]),
            arquivo=arquivo,
            ordem=int(dados["ordem"]),
            critica=bool(dados["critica"]),
        )
        for arquivo, dados in tarefas_por_arquivo.items()
    ]

    tarefas.sort(key=lambda tarefa: (tarefa.ordem, str(tarefa.arquivo)))

    if not tarefas:
        raise RuntimeError("Nenhuma etapa está ativa para execução.")

    arquivos_ausentes = [
        tarefa.arquivo
        for tarefa in tarefas
        if not tarefa.arquivo.is_file()
    ]

    if arquivos_ausentes:
        raise FileNotFoundError(
            "Arquivos Python de etapas ativas não encontrados:\n- "
            + "\n- ".join(str(arquivo) for arquivo in arquivos_ausentes)
        )

    return tarefas


def listar_etapas(configuracao: dict[str, Any]) -> None:
    """Exibe todas as etapas declaradas no config.yaml."""

    print("=" * 90)
    print("ETAPAS CONFIGURADAS")
    print("=" * 90)

    etapas_config = configuracao["execucao"]["etapas"]

    for nome, dados in etapas_config.items():
        ativo = bool(dados.get("ativo", False))
        arquivo = dados.get("arquivo", "")
        ordem = dados.get("ordem", "")
        critica = bool(dados.get("critica", True))

        print(
            f"{ordem!s:>3} | "
            f"{'ATIVA' if ativo else 'INATIVA':7} | "
            f"{'CRÍTICA' if critica else 'NÃO CRÍTICA':11} | "
            f"{nome} -> {arquivo}"
        )


# ============================================================
# CONTROLE DE EXECUÇÃO
# ============================================================

def gerar_identificador_execucao(
    configuracao: dict[str, Any],
) -> str:
    """Gera o identificador único da execução."""

    config_execucao = configuracao.get("execucao", {})

    if not bool(config_execucao.get("criar_identificador_execucao", True)):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    formato = str(
        config_execucao.get(
            "formato_identificador",
            "%Y%m%d_%H%M%S",
        )
    )

    return datetime.now().strftime(formato)


def caminho_controle_execucoes(
    configuracao: dict[str, Any],
) -> Path:
    """Retorna o caminho do CSV de controle."""

    caminho = configuracao.get("execucao", {}).get(
        "arquivo_controle",
        "data/state/execucoes.csv",
    )
    return resolver_caminho(caminho)


def registrar_execucao(
    configuracao: dict[str, Any],
    registro: dict[str, Any],
) -> None:
    """Acrescenta uma linha ao arquivo de controle das execuções."""

    caminho = caminho_controle_execucoes(configuracao)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    colunas = [
        "id_execucao",
        "data_hora_inicio",
        "data_hora_fim",
        "etapas",
        "arquivo",
        "status",
        "duracao_segundos",
        "codigo_retorno",
        "erro",
    ]

    arquivo_novo = not caminho.exists() or caminho.stat().st_size == 0

    with caminho.open("a", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas,
            extrasaction="ignore",
        )

        if arquivo_novo:
            escritor.writeheader()

        escritor.writerow(
            {
                coluna: registro.get(coluna, "")
                for coluna in colunas
            }
        )


# ============================================================
# EXECUÇÃO DOS ARQUIVOS
# ============================================================

def executar_tarefa(
    tarefa: TarefaExecucao,
    indice: int,
    total: int,
    id_execucao: str,
    arquivo_config: Path,
    logger: logging.Logger,
) -> tuple[int, float, str]:
    """Executa um arquivo Python e transmite sua saída em tempo real."""

    etapas_texto = ", ".join(tarefa.etapas)
    arquivo_relativo = tarefa.arquivo.relative_to(RAIZ_PROJETO)

    logger.info("=" * 90)
    logger.info(
        "[%s/%s] EXECUTANDO %s | etapas: %s",
        indice,
        total,
        arquivo_relativo,
        etapas_texto,
    )
    logger.info("=" * 90)

    ambiente = os.environ.copy()
    ambiente["PYTHONUTF8"] = "1"
    ambiente["PYTHONIOENCODING"] = "utf-8"
    ambiente["PROJECT_ROOT"] = str(RAIZ_PROJETO)
    ambiente["PROJECT_CONFIG"] = str(arquivo_config)
    ambiente["PROJECT_RUN_ID"] = id_execucao
    ambiente["PROJECT_STAGES"] = ",".join(tarefa.etapas)

    comando = [
        sys.executable,
        "-u",
        str(tarefa.arquivo),
    ]

    inicio = time.perf_counter()
    mensagens_saida: list[str] = []

    processo = subprocess.Popen(
        comando,
        cwd=RAIZ_PROJETO,
        env=ambiente,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    if processo.stdout is not None:
        for linha in processo.stdout:
            texto = linha.rstrip("\n")
            mensagens_saida.append(texto)
            logger.info("[%s] %s", tarefa.arquivo.name, texto)

    codigo_retorno = processo.wait()
    duracao = time.perf_counter() - inicio

    erro = ""

    if codigo_retorno != 0:
        ultimas_linhas = mensagens_saida[-20:]
        erro = "\n".join(ultimas_linhas).strip()

        logger.error(
            "FALHA: %s | código %s | duração %.2fs",
            arquivo_relativo,
            codigo_retorno,
            duracao,
        )
    else:
        logger.info(
            "CONCLUÍDO: %s | duração %.2fs",
            arquivo_relativo,
            duracao,
        )

    return codigo_retorno, duracao, erro


# ============================================================
# ARGUMENTOS
# ============================================================

def interpretar_argumentos() -> argparse.Namespace:
    """Lê os argumentos de linha de comando."""

    parser = argparse.ArgumentParser(
        description=(
            "Executa sequencialmente os arquivos Python definidos "
            "em config.yaml."
        )
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=ARQUIVO_CONFIG_PADRAO,
        help="Caminho do arquivo config.yaml.",
    )

    parser.add_argument(
        "--listar",
        action="store_true",
        help="Lista as etapas configuradas sem executá-las.",
    )

    parser.add_argument(
        "--etapa",
        action="append",
        dest="etapas",
        help=(
            "Executa somente a etapa informada. "
            "Pode ser repetido para selecionar várias etapas."
        ),
    )

    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    argumentos = interpretar_argumentos()
    arquivo_config = argumentos.config.resolve()

    configuracao = carregar_configuracao(arquivo_config)

    if argumentos.listar:
        listar_etapas(configuracao)
        return

    logger = configurar_logger(configuracao)
    id_execucao = gerar_identificador_execucao(configuracao)

    etapas_solicitadas = (
        set(argumentos.etapas)
        if argumentos.etapas
        else None
    )

    tarefas = montar_tarefas(
        configuracao=configuracao,
        somente_etapas=etapas_solicitadas,
    )

    config_execucao = configuracao.get("execucao", {})
    continuar_apos_erro_nao_critico = bool(
        config_execucao.get(
            "continuar_apos_erro_nao_critico",
            True,
        )
    )

    logger.info("=" * 90)
    logger.info("EXECUÇÃO SEQUENCIAL DO PROJETO")
    logger.info("Identificador: %s", id_execucao)
    logger.info("Raiz: %s", RAIZ_PROJETO)
    logger.info("Configuração: %s", arquivo_config)
    logger.info("Arquivos únicos a executar: %s", len(tarefas))
    logger.info("=" * 90)

    falhas: list[str] = []

    for indice, tarefa in enumerate(tarefas, start=1):
        inicio_iso = datetime.now().isoformat(timespec="seconds")
        codigo_retorno = -1
        duracao = 0.0
        erro = ""

        try:
            codigo_retorno, duracao, erro = executar_tarefa(
                tarefa=tarefa,
                indice=indice,
                total=len(tarefas),
                id_execucao=id_execucao,
                arquivo_config=arquivo_config,
                logger=logger,
            )

            status = "SUCESSO" if codigo_retorno == 0 else "ERRO"

        except Exception as excecao:
            status = "ERRO"
            erro = str(excecao)
            logger.exception(
                "Erro inesperado ao executar %s",
                tarefa.arquivo,
            )

        fim_iso = datetime.now().isoformat(timespec="seconds")

        registrar_execucao(
            configuracao=configuracao,
            registro={
                "id_execucao": id_execucao,
                "data_hora_inicio": inicio_iso,
                "data_hora_fim": fim_iso,
                "etapas": ",".join(tarefa.etapas),
                "arquivo": str(
                    tarefa.arquivo.relative_to(RAIZ_PROJETO)
                ),
                "status": status,
                "duracao_segundos": round(duracao, 4),
                "codigo_retorno": codigo_retorno,
                "erro": erro,
            },
        )

        if status == "ERRO":
            falhas.append(
                f"{tarefa.arquivo.name}: {erro or 'erro sem mensagem'}"
            )

            deve_interromper = (
                tarefa.critica
                or not continuar_apos_erro_nao_critico
            )

            if deve_interromper:
                raise RuntimeError(
                    "A execução foi interrompida após falha em "
                    f"{tarefa.arquivo.name}."
                )

    if falhas:
        raise RuntimeError(
            "A execução terminou com falhas não críticas:\n- "
            + "\n- ".join(falhas)
        )

    logger.info("=" * 90)
    logger.info("TODAS AS ETAPAS ATIVAS FORAM CONCLUÍDAS COM SUCESSO")
    logger.info("=" * 90)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
        sys.exit(130)

    except Exception as erro:
        print(f"\nERRO: {erro}")
        traceback.print_exc()
        sys.exit(1)
