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

   ```bash
     [System.Environment]::SetEnvironmentVariable("WEBHOOK_URL", "https://www.retrogamesonline.com.br", "User")
   ```


Definindo Variavel para Executar somente Comando Git Deploy:
![Env](./docs/VariavelGithubDeploy.png)

   ```bash
     git config --global alias.deploy '!git add . && git commit -m "deploy" && git push'    
   ```


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

## 🚀 Fluxo Completo

![Deploy Workflow](./docs/WorkflowDeploy.png)

Passo 01:

![Deploy Workflow](./docs/DeployDocker01.png)

Passo 02:

![Deploy Workflow](./docs/DeployDocker02.png)

```bash
    cd "C:\Users\Kaique\Documents\FerramentadePublicacaoConteudo" && git pull origin main && docker-compose down && docker-compose up -d --build
```

Passo 03:

![Deploy Workflow](./docs/DeployDocker04.png)

```bash
   docker logs flask_app --tail 50
```


Passo 04:

![Deploy Workflow](./docs/DeployDocker05.png)

```bash
    const log = ($json.stdout || "") + "\n" + ($json.stderr || "");

    // captura URLs (http e https)
    const urls = log.match(/https?:\/\/[^\s]+/g) || [];
    
    // detecta status
    let status = "🟢 Running";
    
    if (log.includes("WARNING")) status = "⚠️ Warning";
    if (log.includes("Error")) status = "❌ Error";
    
    // mensagem
    let message;
    
    if (urls.length === 0) {
      message = "⚠️ Nenhum endpoint detectado ainda";
    } else {
      message = urls.map(u => '🔗 `' + u + '`').join('\n');
    }
    
    return [{
      json: {
        status,
        urls,
        message,
        log
      }
    }];
```

Passo 05:

![Deploy Workflow](./docs/DeployDocker06.png)

![Deploy Workflow](./docs/DeployDocker07.png)

```bash
    {{
    "🚀 Deploy realizado com sucesso!\n" +
    "📦 App Publicado\n" +
    "🕒 " + new Date().toLocaleString("pt-BR")  +
    "\n" + "--------------------------//------------------//------------------"
    }}
    📊 *Flask Log*
    
    {{$json.status}}
    
    🌐 *Endpoints:*
    {{$json.urls.map(u => '🔗 `' + u + '`').join('\n')}}
    
    🟢 *Status:* Running
```

Passo 06:

![Deploy Workflow](./docs/DeployDocker08.png)

![Deploy Workflow](./docs/DeployDocker09.png)


Passo 07:

![Deploy Workflow](./docs/DeployDocker10.png)

```bash
   {{
    {
      content: `🚀 Deploy realizado com sucesso!
    📦 App Publicado
    🕒 ${new Date().toLocaleString("pt-BR")}
    --------------------------
    
    📊 *Flask Log*
    
    ${$json.status}
    
    🌐 *Endpoints:*
    ${($json.urls || []).map(u => '🔗 `' + u + '`').join('\n')}
    
    🟢 *Status:* Running`
    }
    }}
```

Passo 08:

![Deploy Workflow](./docs/DeployDocker11.png)

```bash
    {{
    {
      content: `🚀 Deploy realizado com sucesso!
    📦 App Publicado
    🕒 ${new Date().toLocaleString("pt-BR")}
    --------------------------
    
    📊 *Flask Log*
    
    ${$json.status}
    
    🌐 *Endpoints:*
    ${($json.urls || []).map(u => '🔗 `' + u + '`').join('\n')}
    
    🟢 *Status:* Running`
    }
    }}
```




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
Passo 01:

![Telegram](./docs/Telegram01.png)

Passo 02:

![Telegram](./docs/Telegram02.png)

Passo 03:

![Telegram](./docs/Telegram03.png)

- Bot criado via BotFather
- Notificações diretas

---

## 📊 Monitoramento de Containers

![Monitoramento](./docs/WorkflowPsLogsStats.png)

## 🚀 Fluxo Completo

Executa:

- docker ps
  
    Passo 01:
  
   ![Monitoramento](./docs/DockerPs01.png)

     Passo 02:
  
   ![Monitoramento](./docs/DockerPs02.png)

    ```bash
       docker ps --filter "name=flask_app" --format "{{.ID}}|{{.Image}}|{{.Command}}|{{.RunningFor}}|{{.Status}}|{{.Ports}}|{{.Names}}"
    ```

     Passo 03:
  
   ![Monitoramento](./docs/DockerPs03.png)

   ```bash
    const raw = $json.stdout.trim();

    const data = raw.split("|");
    return [
      {
      json: {
        id: data[0],
        image: data[1],
        command: data[2],
        uptime: data[3],
        status: data[4],
        ports: data[5],
        name: data[6]
      }
      }
    ];
  ```

     Passo 04:
  
   ![Monitoramento](./docs/DockerPs04.png)

  
   ```bash
    📦 *Docker Container Info*
    
    📛 *Nome:* `{{$json.name}}`
    🆔 *ID:* `{{$json.id}}`
    
    🐳 *Imagem:*  
    `{{$json.image}}`
    
    🚀 *Comando:*  
    `{{$json.command}}`
    
    ⏱️ *Uptime:* `{{$json.uptime}}`  
    🟢 *Status:* `{{$json.status}}`
    
    🌐 *Portas:*  
    `{{$json.ports}}`
  ```
- docker logs
  
     Passo 01:
  
   ![Monitoramento](./docs/DockerLogs01.png)

     Passo 02:
  
   ![Monitoramento](./docs/DockerLogs02.png)

    ```bash
      docker logs flask_app --tail 50
    ```


     Passo 03:
  
   ![Monitoramento](./docs/DockerLogs03.png)

   ```bash
    const log = ($json.stdout || "") + "\n" + ($json.stderr || "");

    // captura URLs (http e https)
    const urls = log.match(/https?:\/\/[^\s]+/g) || [];
    
    // detecta status
    let status = "🟢 Running";
    
    if (log.includes("WARNING")) status = "⚠️ Warning";
    if (log.includes("Error")) status = "❌ Error";
    
    // mensagem
    let message;
    
    if (urls.length === 0) {
      message = "⚠️ Nenhum endpoint detectado ainda";
    } else {
      message = urls.map(u => '🔗 `' + u + '`').join('\n');
    }
    
    return [{
      json: {
        status,
        urls,
        message,
        log
      }
    }];
  ```

     Passo 04:
  
   ![Monitoramento](./docs/DockerLogs04.png)

  
   ```bash
    📊 *Flask Log*
    
    {{$json.status}}
    
    🌐 *Endpoints:*
    {{$json.urls.map(u => '🔗 `' + u + '`').join('\n')}}
    
    🟢 *Status:* Running
  ```
- docker stats
  
     Passo 01:
  
   ![Monitoramento](./docs/DockerStats01.png)

     Passo 02:
  
   ![Monitoramento](./docs/DockerStats02.png)

   ```bash
      docker stats flask_app --no-stream --format "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}|{{.PIDs}}"
    ```


     Passo 03:
  
   ![Monitoramento](./docs/DockerStats03.png)

   ```bash
   const raw = $json.stdout.trim();

    const data = raw.split("|");
    
    return [
      {
        json: {
          nome: data[0],
          cpu: data[1],
          mem: data[2],
          memPerc: data[3],
          net: data[4],
          block: data[5],
          pids: data[6]
        }
      }
    ];
  ```


     Passo 04:
  
   ![Monitoramento](./docs/DockerStats04.png)

  
   ```bash
    📦 *Docker Monitor*
    
    📛 *Container:* `{{$json.nome}}`
    
    ⚙️ *CPU:* `{{$json.cpu}}`  
    🧠 *Memória:* `{{$json.mem}}`  
    📊 *Uso:* `{{$json.memPerc}}`
    
    🌐 *Rede:*  
    ⬆️⬇️ `{{$json.net}}`
    
    💾 *Disco:*  
    ⬆️⬇️ `{{$json.block}}`
    
    🧵 *Processos:* `{{$json.pids}}`
  ```

---

## 🔄 Auto Healing (Restart automático)
![Restart](./docs/WorkflowRestartDocker.png)

## 🚀 Fluxo Completo

Passo 01:

![Restart](./docs/DockerRestart01.png)

Passo 02:

![Restart](./docs/DockerRestart02.png)

  ```bash
      docker inspect -f '{{.State.Running}}' flask_app
  ```

Passo 03:

![Restart](./docs/DockerRestart03.png)

 ```bash
     {{ $json["stdout"].replace(/[^a-z]/gi, '').toLowerCase() === "false" }}
 ```

Passo 04:

![Restart](./docs/DockerRestart04.png)

Passo 05:

![Restart](./docs/DockerRestart05.png)

  ```bash
      docker start flask_app
  ```

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

