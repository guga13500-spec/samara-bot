#!/usr/bin/env python3
"""
SAMARA - Teste de Conexão com TeamTalk 5
Sem dependências externas - só Python puro
"""
import os, sys, time, json, logging, socket

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("SamaraTest")

HOST = "tt5.angelsclan.net"
PORT = 23351

log.info("=" * 50)
log.info(f"TESTE DE CONEXÃO: {HOST}:{PORT}")
log.info("=" * 50)

# DNS
log.info("\n📡 Testando DNS...")
try:
    ips = socket.getaddrinfo(HOST, PORT, socket.AF_INET, socket.SOCK_STREAM)
    ip = ips[0][4][0]
    log.info(f"   ✅ DNS resolvido: {HOST} -> {ip}")
except Exception as e:
    log.error(f"   ❌ DNS falhou: {e}")
    sys.exit(1)

# TCP
log.info(f"\n🔌 Testando TCP...")
for i in range(3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((ip, PORT))
        s.settimeout(3)
        log.info(f"   ✅ CONEXÃO BEM-SUCEDIDA! (tentativa {i+1})")
        try:
            data = s.recv(4096)
            log.info(f"   📨 Dados: {data[:200]}")
        except socket.timeout:
            log.info(f"   📨 Conectado, sem dados iniciais")
        s.close()
        log.info("\n🎉 SAMARA PODE CONECTAR NESSE SERVIDOR!")
        sys.exit(0)
    except ConnectionRefusedError:
        log.error(f"   ❌ Conexão recusada (tentativa {i+1}/3)")
    except Exception as e:
        log.error(f"   ❌ Erro: {e} (tentativa {i+1}/3)")
    time.sleep(2)

log.error("\n❌ SAMARA NÃO CONSEGUIU CONECTAR")
sys.exit(1)