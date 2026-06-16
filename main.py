"""Ponto de entrada da automacao de relatorios financeiros."""

from __future__ import annotations

import logging

from coleta_dados import coletar_dados
from config import EMAIL
from enviar_email import enviar_relatorio
from gerar_relatorio import gerar_relatorio


def executar() -> None:
    """Executa coleta, geracao do Excel e envio opcional por e-mail."""
    logging.info("Iniciando coleta das cotacoes financeiras.")
    dados, avisos = coletar_dados()

    logging.info("Gerando relatorio com %d ativo(s).", len(dados))
    caminho_relatorio = gerar_relatorio(dados, avisos)
    logging.info("Relatorio gerado em: %s", caminho_relatorio)

    if EMAIL.habilitado:
        logging.info(
            "Enviando relatorio para %d destinatario(s).",
            len(EMAIL.destinatarios),
        )
        enviar_relatorio(caminho_relatorio, EMAIL)
        logging.info("E-mail enviado com sucesso.")
    else:
        logging.info(
            "Envio desabilitado. Defina EMAIL_ENABLED=true no arquivo .env "
            "para enviar automaticamente."
        )

    if avisos:
        logging.warning("O processo terminou com %d aviso(s) de coleta.", len(avisos))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    try:
        executar()
    except Exception:
        logging.exception("A automacao foi interrompida por um erro.")
        raise SystemExit(1)
