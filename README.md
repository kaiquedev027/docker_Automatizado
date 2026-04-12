# 🚀 Deploy Automatizado com Docker + n8n + Monitoramento

Sistema completo de CI/CD com deploy automatizado, monitoramento e notificações em tempo real.

---

## 📌 Visão Geral

Este projeto implementa:

- Deploy automático via GitHub Actions
- Automação com n8n
- Containerização com Docker
- Monitoramento contínuo
- Notificações (Slack, Discord, Email, Telegram)
- Auto-restart de containers

---

## 🧱 Estrutura do Projeto

![Estrutura](./docs/estruturadoprojeto.png)



---

## ⚙️ CI/CD com GitHub Actions
```bash
    name: Pipeline Completo
    
    on:
      push:
        branches:
          - main
    
    jobs:
      build-and-deploy:
        runs-on: ubuntu-latest
    
        steps:
          # 1. Clonar código
          - name: Checkout
            uses: actions/checkout@v4
    
          # 2. Validar Python (opcional, mas TOP)
          - name: Instalar Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.12'
    
          - name: Instalar dependências
            run: |
              pip install -r requirements.txt
    
          # 3. Teste básico (evita deploy quebrado)
          - name: Teste rápido
            run: |
              python -m py_compile app.py
    
          # 4. Disparar seu n8n (AQUI É A CHAVE)
          - name: Deploy via n8n
            run: |
              curl -X POST https://www.retrogamesonline.com.br/webhook/deploy
```

### Fluxo


---

## 🐳 Docker
```bash
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8024

CMD ["python", "app.py"]
```


### Descrição

- Imagem base Python
- Instala dependências
- Executa aplicação

---

## 📦 Docker Compose

```bash
version: '3.8'

services:
  flask_app:
    build: .
    container_name: flask_app
    ports:
      - "8024:8024"
    restart: always
```

## 🌐 Cloudflare Tunnel

![Cloudflare](./docs/Cloudflared.png)

- Expõe serviço local
- Evita uso de IP público
- Usado para webhook do GitHub

---

## 🔐 Variáveis de Ambiente
Definindo Variavel para Fixar o Dominio no N8N:
![Env](./docs/VariavelDominioN8N.png)

Definindo Variavel para Executar somente Comando Git Deploy:
![Env](./docs/VariavelGithubDeploy.png)

Exemplo:


---

## 🔗 Configuração Webhook GitHub

Passo 01:

![Webhook](./docs/GitHub01.png)

Passo 02:

![Webhook](./docs/GitHub02.png)

Passo 03:

![Webhook](./docs/GitHub03.png)

Passo 04:

![Webhook](./docs/GitHub04.png)

- Método: POST
- Evento: Push
- URL → n8n

---

## 🤖 Workflow de Deploy (n8n)

📷 **Workflow completo (Página 34)**  
![Deploy Workflow](./docs/workflow-deploy.png)

### Etapas:

1. Webhook
2. Deploy Docker
3. Verificação
4. Notificações

---

## 📢 Notificações

---

### 💬 Slack
Passo 01: 

![Slack](./docs/Slack01.png)

Passo 02: 

![Slack](./docs/Slack02.png)

Passo 03: 

![Slack](./docs/Slack03.png)
Passo 04: 

![Slack](./docs/Slack04.png)

Passo 05: 

![Slack](./docs/Slack05.png)

Passo 06: 

![Slack](./docs/Slack06.png)

Passo 07: 

![Slack](./docs/Slack07.png)

Passo 08: 

![Slack](./docs/Slack08.png)


- Incoming Webhook
- Alertas de deploy

---

### 🎮 Discord

Passo 1:

![Discord](./docs/Discord01.png)

Passo 2:

![Discord](./docs/Discord02.png)

Passo 3:

![Discord](./docs/Discord03.png)

Passo 4:

![Discord](./docs/Discord04.png)

Passo 5:

![Discord](./docs/Discord05.png)

Passo 6:

![Discord](./docs/Discord06.png)


- Webhook por canal
- Notificações em tempo real

---

### 📧 Email SMTP

Passo 01:

![SMTP](./docs/Email01.png)

Passo 02:

![SMTP](./docs/Email02.png)

Passo 03:

![SMTP](./docs/Email03.png)

Passo 04:

![SMTP](./docs/Email04.png)

Passo 05:

![SMTP](./docs/Email05.png)



- Gmail + senha de app
- Envio automático de emails

---

### 📱 Telegram

📷 **Bot Telegram (Páginas 31–33)**  
![Telegram](./docs/telegram.png)

- Bot criado via BotFather
- Notificações diretas

---

## 📊 Monitoramento de Containers

📷 **Workflow Monitoramento (Página 46)**  
![Monitoramento](./docs/monitoramento.png)

Executa:

- docker ps
- docker logs
- docker stats

---

## 🔄 Auto Healing (Restart automático)

📷 **Workflow Restart (Página 50)**  
![Restart](./docs/restart.png)

### Lógica:


---

## 🚀 Fluxo Completo



---

## 🧠 Tecnologias Utilizadas

- Docker
- Docker Compose
- GitHub Actions
- n8n
- Cloudflare Tunnel
- Python
- Slack API
- Discord Webhooks
- Telegram Bot
- SMTP (Gmail)

---

## 📈 Benefícios

- Deploy automatizado
- Alta disponibilidade
- Monitoramento contínuo
- Alertas em tempo real

---

## 📌 Melhorias Futuras

- Kubernetes
- Prometheus + Grafana
- Logs centralizados
- CI/CD avançado com Buildx

---

## 👨‍💻 Autor

Kaique Alves Fernandes
