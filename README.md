🚀 Deploy Automatizado com Docker + n8n + Monitoramento
📌 1. Visão Geral
Este projeto implementa um sistema completo de:
CI/CD automatizado
Deploy via Docker
Execução via webhook (n8n)
Monitoramento contínuo
Notificações em múltiplos canais
Auto recuperação de containers (self-healing)
📍 Baseado no fluxo apresentado ao longo do PDF (principalmente páginas 34, 46 e 50).
🧱 2. Estrutura do Projeto
📄 Conforme página 2:
O projeto segue uma estrutura organizada contendo:
.github/workflows/ → pipeline CI/CD
app.py → aplicação principal
Dockerfile → build da imagem
docker-compose.yml → orquestração
requirements.txt → dependências Python
templates/ e static/ → frontend
README.md → documentação
👉 Estrutura pensada para deploy simples e escalável.
⚙️ 3. Pipeline CI/CD (GitHub Actions)
📄 Página 3
O pipeline automatiza:
Checkout do código
Setup do ambiente Python
Instalação de dependências
Execução de testes
Disparo de webhook para deploy
🔁 Fluxo

git push → GitHub Actions → Webhook → n8n → Deploy Docker
📌 Destaque importante
O deploy não acontece direto no GitHub —
ele é delegado ao n8n, permitindo automação avançada.
🐳 4. Containerização com Docker
📄 Página 4
Dockerfile
Base: python:3.12-slim
Diretório: /app
Instala dependências via pip
Expõe porta 8024
Executa app.py
📌 Vantagens
Build leve
Ambiente padronizado
Fácil replicação
📦 5. Docker Compose
📄 Página 5
Responsável por:
Subir containers automaticamente
Definir serviços
Facilitar deploy local e produção
🌐 6. Exposição com Cloudflare Tunnel
📄 Página 9
O projeto utiliza Cloudflare Tunnel para:
Expor o n8n/public endpoint
Evitar necessidade de IP público
Garantir segurança via Cloudflare
🔗 Configuração
Domínio configurado: retrogamesonline.com.br
Rota → /webhook/deploy
Serviço → http://127.0.0.1:5678
🔐 7. Variáveis de Ambiente
📄 Página 10
Configuradas para:
URL do webhook
Integrações externas
Scripts de deploy
Exemplo:

WEBHOOK_URL=https://seu-dominio/webhook/deploy
Também há alias para facilitar deploy via git:

git deploy
🔗 8. Integração com GitHub Webhook
📄 Páginas 6–8
Passos realizados:
Acessar Settings do repositório
Criar Webhook
Configurar:
URL: endpoint do n8n
Método: POST
Evento: push
📌 Importante: O workflow precisa estar ativo no n8n.
🤖 9. Automação com n8n
📄 Página 34 (principal)
🔥 Workflow de Deploy
Fluxo completo:
Webhook Trigger
Execução de comandos Docker
Verificação do container
Envio de notificações
⚙️ Etapas detalhadas
1. Webhook
Recebe requisição do GitHub
2. Deploy Docker
Executa comandos como:

docker-compose down
docker-compose up -d --build
3. Check Container
Valida se o container está rodando
4. Notificações
Dispara mensagens para múltiplos canais
📢 10. Sistema de Notificações
💬 Slack
📄 Páginas 12–19
Criação de App
Ativação de Incoming Webhook
Geração de URL
✔ Usado para alertas de deploy
🎮 Discord
📄 Páginas 20–25
Configuração de Webhook por canal
Integração direta com n8n
✔ Ideal para notificações rápidas
📧 Email SMTP
📄 Páginas 26–30
Configuração via Gmail:
Ativar verificação em duas etapas
Criar senha de app
Configurar SMTP no n8n
✔ Envio de alertas formais
📱 Telegram
📄 Páginas 31–33
Criação de bot via BotFather
Geração de token
Integração via API
✔ Notificação direta no celular
📊 11. Monitoramento de Containers
📄 Página 46
Workflow de Monitoramento
Executa periodicamente:
docker ps
docker logs
docker stats
🔁 Estrutura

Schedule Trigger → Docker Command → Notificação
✔ Monitoramento contínuo
✔ Visibilidade operacional
🔄 12. Auto Healing (Restart Automático)
📄 Página 50
Workflow
Verifica status do container
Se estiver parado: → executa start
Se estiver rodando: → não faz nada
🧠 Lógica

IF container == stopped → start
ELSE → no-op
✔ Alta disponibilidade
✔ Redução de downtime