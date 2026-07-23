#!/usr/bin/env python3
"""
SAMARA - Assistente IA para TeamTalk 5
v3 - Testa conexão e grava resultado
"""
import os, sys, time, json, requests, logging, socket

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("Samara")

HOST = "tt5.angelsclan.net"
PORT = 23351
USER = "Gustavo"
PASS = "2007"
NICK = "Samara"
CHANNEL = "Grupo dos Amigos"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "openai/gpt-4o-mini"

# TESTE 1: Socket TCP
log.info("=" * 50)
log.info(f"Testando conexão TCP com {HOST}:{PORT}...")
log.info("=" * 50)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    log.info(f"✅ CONEXÃO TCP BEM-SUCEDIDA! {HOST}:{PORT}")
    s.settimeout(3)
    try:
        data = s.recv(4096)
        log.info(f"📡 Dados recebidos: {data[:200]}")
    except:
        log.info("📡 Conectado mas sem dados iniciais")
    s.close()
except Exception as e:
    log.error(f"❌ CONEXÃO TCP FALHOU: {e}")

# TESTE 2: OpenRouter
if API_KEY:
    log.info("\n--- Testando OpenRouter ---")
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": MODEL, "messages": [{"role": "user", "content": "diga OK"}], "max_tokens": 10}, timeout=15)
        log.info(f"✅ OpenRouter: {r.json()['choices'][0]['message']['content']}")
    except Exception as e:
        log.error(f"❌ OpenRouter: {e}")
else:
    log.warning("⚠️ OPENROUTER_API_KEY não configurada")

# TESTE 3: DNS
log.info("\n--- Testando DNS ---")
try:
    ip = socket.gethostbyname(HOST)
    log.info(f"✅ DNS: {HOST} -> {ip}")
except Exception as e:
    log.error(f"❌ DNS: {e}")

# Resultado final
log.info("\n" + "=" * 50)
log.info("TESTE CONCLUÍDO")
log.info("=" * 50)