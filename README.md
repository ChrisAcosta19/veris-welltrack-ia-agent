# WellTrack IA Agent

Proyecto que implementa un agente conversacional para el onboarding de usuarios de la plataforma WellTrack, solicitando Nombre, Edad y Objetivo Principal.

## Stack Tecnológico
* **Python** 3.10+
* **FastAPI** (API REST)
* **LangChain** (Orquestación del Agente)
* **OpenAI** (LLM Provider)

## Requisitos Previos
Contar con una API Key de OpenAI funcional.

## Instalación Local

1. Clone el repositorio y acceda a la carpeta:
```bash
cd veris-welltrack-ia-agent
```

2. Se recomienda crear un entorno virtual e instalar las dependencias:
```bash
python -m venv venv

# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

3. Configure las variables de entorno:
Renombre el archivo `.env.example` a `.env` y agregue su API Key de OpenAI:
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Ejecución del Servidor

Levante el servidor FastAPI ejecutando el siguiente comando al nivel de la carpeta del proyecto:
```bash
uvicorn main:app --reload
```
El servidor se ejecutará en `http://127.0.0.1:8000`.

---

## Uso de la API y Flujo Multiusuario (Sesiones Concurrentes)

La API expone un único endpoint: `POST /chat`. El agente es capaz de manejar múltiples usuarios simultáneamente y aísla el contexto de cada conversación gracias al parámetro `session_id`.

A continuación, se detalla un escenario completo enviando solicitudes intercaladas entre dos usuarios distintos (`usuario_123` y `usuario_456`), donde cada uno completa sus 3 preguntas de forma independiente. Se provee el comando `curl` tanto para **Linux/Mac** como para **Windows** y las respuestas esperadas.

*Nota para Windows:* Use `curl.exe` o `Invoke-RestMethod` si su terminal de PowerShell tiene `curl` como alias heredado, y asegúrese de escapar las comillas internas en el JSON con `\"`.

---

**Paso 1: Usuario A inicia la conversación (Pregunta 1: Nombre)**

*Linux / Mac (Bash):*
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id": "usuario_123", "message": "Hola, quiero iniciar mi registro"}'
```
*Windows (CMD / PowerShell con curl.exe):*
```cmd
curl.exe -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"session_id\": \"usuario_123\", \"message\": \"Hola, quiero iniciar mi registro\"}"
```
**Respuesta Esperada:**
```json
{
  "response": "¡Hola! Bienvenido a WellTrack. Para empezar, ¿Cuál es su nombre?",
  "is_final": false,
  "summary": null
}
```

**Paso 2: Usuario B inicia la conversación en paralelo (Pregunta 1: Nombre)**

*Linux / Mac (Bash):*
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id": "usuario_456", "message": "Buen día, quiero registrarme"}'
```
*Windows (CMD / PowerShell con curl.exe):*
```cmd
curl.exe -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"session_id\": \"usuario_456\", \"message\": \"Buen dia, quiero registrarme\"}"
```
**Respuesta Esperada:**
```json
{
  "response": "¡Hola! Bienvenido a WellTrack. Para empezar, ¿Cuál es su nombre?",
  "is_final": false,
  "summary": null
}
```

**Paso 3: Usuario A responde su nombre (Pregunta 2: Edad)**

*Linux / Mac (Bash):*
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id": "usuario_123", "message": "Me llamo Carlos"}'
```
*Windows (CMD / PowerShell con curl.exe):*
```cmd
curl.exe -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"session_id\": \"usuario_123\", \"message\": \"Me llamo Carlos\"}"
```
**Respuesta Esperada:**
```json
{
  "response": "Mucho gusto Carlos. ¿Cuántos años tiene?",
  "is_final": false,
  "summary": null
}
```

**Paso 4: Usuario B responde su nombre (Pregunta 2: Edad)**

*Linux / Mac (Bash):*
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id": "usuario_456", "message": "Soy Ana"}'
```
*Windows (CMD / PowerShell con curl.exe):*
```cmd
curl.exe -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"session_id\": \"usuario_456\", \"message\": \"Soy Ana\"}"
```
**Respuesta Esperada:**
```json
{
  "response": "Mucho gusto Ana. ¿Cuántos años tiene?",
  "is_final": false,
  "summary": null
}
```

**Paso 5: Usuario A responde su edad (Pregunta 3: Objetivo)**

*Linux / Mac (Bash):*
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id": "usuario_123", "message": "Tengo 28 años"}'
```
*Windows (CMD / PowerShell con curl.exe):*
```cmd
curl.exe -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"session_id\": \"usuario_123\", \"message\": \"Tengo 28 anos\"}"
```
**Respuesta Esperada:**
```json
{
  "response": "Perfecto. Finalmente Carlos, ¿Cuál es su objetivo principal: perder peso, ganar músculo o mejorar resistencia?",
  "is_final": false,
  "summary": null
}
```

**Paso 6: Usuario B responde su edad (Pregunta 3: Objetivo)**

*Linux / Mac (Bash):*
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id": "usuario_456", "message": "Tengo 25"}'
```
*Windows (CMD / PowerShell con curl.exe):*
```cmd
curl.exe -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"session_id\": \"usuario_456\", \"message\": \"Tengo 25\"}"
```
**Respuesta Esperada:**
```json
{
  "response": "Perfecto. Finalmente Ana, ¿Cuál es su objetivo principal: perder peso, ganar músculo o mejorar resistencia?",
  "is_final": false,
  "summary": null
}
```

**Paso 7: Usuario A responde su objetivo (Resumen Final)**

*Linux / Mac (Bash):*
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id": "usuario_123", "message": "Mi meta es perder peso"}'
```
*Windows (CMD / PowerShell con curl.exe):*
```cmd
curl.exe -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"session_id\": \"usuario_123\", \"message\": \"Mi meta es perder peso\"}"
```
**Respuesta Esperada:**
```json
{
  "response": "¡Perfecto Carlos! He guardado sus datos:\n- Nombre: Carlos\n- Edad: 28 años\n- Objetivo: perder peso\n¡Gracias por registrarse en WellTrack!",
  "is_final": true,
  "summary": {
    "nombre": "Carlos",
    "edad": "28",
    "objetivo": "perder peso"
  }
}
```

**Paso 8: Usuario B responde su objetivo (Resumen Final)**

*Linux / Mac (Bash):*
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id": "usuario_456", "message": "Quiero ganar masa muscular"}'
```
*Windows (CMD / PowerShell con curl.exe):*
```cmd
curl.exe -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"session_id\": \"usuario_456\", \"message\": \"Quiero ganar masa muscular\"}"
```
**Respuesta Esperada:**
```json
{
  "response": "¡Perfecto Ana! He guardado sus datos:\n- Nombre: Ana\n- Edad: 25 años\n- Objetivo: ganar masa muscular\n¡Gracias por registrarse en WellTrack!",
  "is_final": true,
  "summary": {
    "nombre": "Ana",
    "edad": "25",
    "objetivo": "ganar masa muscular"
  }
}
```