"""Configuracoes centralizadas da automacao."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _env_bool(nome: str, padrao: bool = False) -> bool:
    """Converte uma variavel de ambiente em booleano."""
    return os.getenv(nome, str(padrao)).strip().lower() in {
        "1",
        "true",
        "sim",
        "yes",
        "on",
    }


@dataclass(frozen=True)
class ConfiguracaoEmail:
    """Dados necessarios para conexao com um servidor SMTP."""

    habilitado: bool
    provedor: str
    remetente: str
    senha: str
    destinatarios: tuple[str, ...]
    servidor: str
    porta: int

    @classmethod
    def carregar(cls) -> "ConfiguracaoEmail":
        provedor = os.getenv("EMAIL_PROVIDER", "gmail").strip().lower()
        servidores = {
            "gmail": ("smtp.gmail.com", 587),
            "outlook": ("smtp.office365.com", 587),
        }

        servidor_padrao, porta_padrao = servidores.get(provedor, ("", 587))
        destinatarios = tuple(
            email.strip()
            for email in os.getenv("EMAIL_TO", "").split(",")
            if email.strip()
        )

        return cls(
            habilitado=_env_bool("EMAIL_ENABLED"),
            provedor=provedor,
            remetente=os.getenv("EMAIL_FROM", "").strip(),
            senha=os.getenv("EMAIL_PASSWORD", "").strip(),
            destinatarios=destinatarios,
            servidor=os.getenv("SMTP_SERVER", servidor_padrao).strip(),
            porta=int(os.getenv("SMTP_PORT", str(porta_padrao))),
        )

    def validar(self) -> None:
        """Valida apenas quando o envio de e-mail estiver habilitado."""
        if not self.habilitado:
            return

        campos_ausentes = []
        if not self.remetente:
            campos_ausentes.append("EMAIL_FROM")
        if not self.senha:
            campos_ausentes.append("EMAIL_PASSWORD")
        if not self.destinatarios:
            campos_ausentes.append("EMAIL_TO")
        if not self.servidor:
            campos_ausentes.append("SMTP_SERVER")

        if campos_ausentes:
            raise ValueError(
                "Variaveis de ambiente ausentes para envio: "
                + ", ".join(campos_ausentes)
            )


ATIVOS = {
    "^BVSP": "IBOVESPA",
    "BRL=X": "Dolar (USD/BRL)",
    "EURBRL=X": "Euro (EUR/BRL)",
    "BTC-USD": "Bitcoin (BTC/USD)",
    "PETR4.SA": "Petrobras PN",
    "VALE3.SA": "Vale ON",
    "ITUB4.SA": "Itau Unibanco PN",
}

PASTA_RELATORIOS = BASE_DIR / "relatorios"
EMAIL = ConfiguracaoEmail.carregar()
