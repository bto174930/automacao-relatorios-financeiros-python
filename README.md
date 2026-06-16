# Automação de Relatórios Financeiros

Projeto em Python que automatiza um fluxo comum em áreas financeiras: coleta
de cotações de mercado, tratamento dos dados, geração de relatório executivo
em Excel e envio por e-mail.

O projeto foi estruturado para demonstração em portfólio no GitHub e LinkedIn,
com separação de responsabilidades, configuração segura e tratamento de falhas.

## Funcionalidades

- Coleta dados do IBOVESPA, dólar, euro, Bitcoin, PETR4, VALE3 e ITUB4.
- Calcula preço atual, variação diária, máxima, mínima e volume.
- Continua o processo quando apenas um dos ativos apresenta falha.
- Gera um arquivo `.xlsx` formatado com título, data e tabela profissional.
- Destaca variações positivas em verde e negativas em vermelho.
- Cria um resumo executivo com maior alta, maior queda e panorama do dia.
- Envia o relatório em anexo por Gmail, Outlook ou outro servidor SMTP.
- Mantém credenciais fora do código por meio de variáveis de ambiente.

## Tecnologias

- Python
- Pandas
- OpenPyXL
- yfinance
- smtplib
- python-dotenv

## Estrutura

```text
Automacao_Relatorios_Financeiros/
├── main.py
├── coleta_dados.py
├── gerar_relatorio.py
├── enviar_email.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

Os relatórios gerados são armazenados automaticamente na pasta `relatorios/`.

## Como executar

### 1. Criar e ativar o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Crie uma cópia de `.env.example` chamada `.env` e preencha os valores:

```env
EMAIL_ENABLED=false
EMAIL_PROVIDER=gmail
EMAIL_FROM=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_aplicativo
EMAIL_TO=destinatario@empresa.com
```

Mantenha `EMAIL_ENABLED=false` para gerar apenas o Excel. Depois de validar as
credenciais, altere para `true` para ativar o envio automático.

Para múltiplos destinatários, separe os endereços por vírgula:

```env
EMAIL_TO=gestor@empresa.com,financeiro@empresa.com
```

### 4. Executar

```bash
python main.py
```

Exemplo de saída:

```text
15/06/2026 09:00:00 | INFO | Iniciando coleta das cotacoes financeiras.
15/06/2026 09:00:03 | INFO | Gerando relatorio com 7 ativo(s).
15/06/2026 09:00:04 | INFO | Relatorio gerado em: .../relatorios/relatorio_financeiro_20260615_090004.xlsx
```

## Configuração do Gmail

Contas Gmail com verificação em duas etapas devem usar uma **senha de
aplicativo**, e não a senha normal da conta:

1. Ative a verificação em duas etapas na Conta Google.
2. Gere uma senha de aplicativo.
3. Informe essa senha em `EMAIL_PASSWORD`.

O projeto usa `smtp.gmail.com` e a porta `587`.

## Configuração do Outlook

Use:

```env
EMAIL_PROVIDER=outlook
EMAIL_FROM=seu_email@outlook.com
EMAIL_PASSWORD=sua_senha_ou_senha_de_aplicativo
```

O projeto usa `smtp.office365.com` e a porta `587`. Algumas contas
corporativas bloqueiam autenticação SMTP; nesse caso, o administrador do
Microsoft 365 precisa liberar o recurso ou fornecer um método autorizado.

## O que este projeto simula em uma empresa

Esta automação representa uma rotina de fechamento ou acompanhamento diário:

1. O sistema consulta indicadores financeiros usados pela gestão.
2. Os dados são consolidados e transformados em informações comparáveis.
3. Um relatório padronizado é gerado para reduzir trabalho manual.
4. O material é distribuído automaticamente a gestores e áreas interessadas.

Em um ambiente real, a execução pode ser agendada pelo Agendador de Tarefas do
Windows, cron no Linux, GitHub Actions ou uma plataforma de automação.

## Segurança

- O arquivo `.env` está listado no `.gitignore`.
- Nunca publique senhas, tokens ou credenciais no repositório.
- Prefira senhas de aplicativo e contas exclusivas para automações.
- Em produção, considere um cofre de segredos, como Azure Key Vault ou AWS
  Secrets Manager.

## Aviso

As cotações são obtidas de uma fonte pública e podem ter atraso. Este projeto
tem finalidade educacional e de portfólio e não constitui recomendação de
investimento.
