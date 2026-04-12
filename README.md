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

📷 **Configuração Tunnel (Página 9)**  
![Cloudflare](./docs/cloudflare.png)

- Expõe serviço local
- Evita uso de IP público
- Usado para webhook do GitHub

---

## 🔐 Variáveis de Ambiente

📷 **Variáveis (Página 10)**  
![Env](./docs/env.png)

Exemplo:


---

## 🔗 Configuração Webhook GitHub

📷 **Webhook GitHub (Páginas 6–8)**  
![Webhook](./docs/github-webhook.png)

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

📷 **Configuração Slack (Páginas 12–19)**  
![Slack](./docs/slack.png)

- Incoming Webhook
- Alertas de deploy

---

### 🎮 Discord

📷 **Configuração Discord (Páginas 20–25)**  
![Discord](./docs/discord.png)

- Webhook por canal
- Notificações em tempo real

---

### 📧 Email SMTP

📷 **Configuração SMTP (Páginas 26–30)**  
![SMTP](./docs/smtp.png)

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
