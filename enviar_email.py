"""Envio do relatorio por e-mail usando SMTP."""

from __future__ import annotations

import mimetypes
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from config import ConfiguracaoEmail


def enviar_relatorio(
    arquivo: Path,
    configuracao: ConfiguracaoEmail,
) -> None:
    """Envia o arquivo Excel como anexo via Gmail, Outlook ou SMTP."""
    configuracao.validar()

    if not arquivo.exists():
        raise FileNotFoundError(f"Relatorio nao encontrado: {arquivo}")

    hoje = datetime.now()
    mensagem = EmailMessage()
    mensagem["From"] = configuracao.remetente
    mensagem["To"] = ", ".join(configuracao.destinatarios)
    mensagem["Subject"] = (
        f"Relatorio Financeiro Diario - {hoje:%d/%m/%Y}"
    )
    mensagem.set_content(
        "Prezados,\n\n"
        "Segue em anexo o relatorio financeiro diario com as principais "
        "cotacoes de mercado, variacoes e indicadores consolidados.\n\n"
        "O arquivo foi gerado automaticamente pela automacao de relatorios "
        "financeiros.\n\n"
        "Atenciosamente,\n"
        "Automacao de Relatorios Financeiros"
    )

    tipo_mime, _ = mimetypes.guess_type(arquivo.name)
    tipo_principal, subtipo = (
        tipo_mime.split("/", 1)
        if tipo_mime
        else (
            "application",
            "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    )
    mensagem.add_attachment(
        arquivo.read_bytes(),
        maintype=tipo_principal,
        subtype=subtipo,
        filename=arquivo.name,
    )

    contexto_ssl = ssl.create_default_context()
    with smtplib.SMTP(
        configuracao.servidor,
        configuracao.porta,
        timeout=30,
    ) as servidor:
        servidor.ehlo()
        servidor.starttls(context=contexto_ssl)
        servidor.ehlo()
        servidor.login(configuracao.remetente, configuracao.senha)
        servidor.send_message(mensagem)
