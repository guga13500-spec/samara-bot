#!/usr/bin/env python3
"""
SAMARA - Assistente para TeamTalk 5
Personalidade: zoeira, direta, brasileira
"""

import os, sys, time, json, requests, logging, socket

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("Samara")

# Config
HOST = "tt5.angelsclan.net"
PORT = 23351
USER = "Gustavo"
PASS = "2007"
NICK = "Samara"
CHANNEL = "Grupo dos Amigos"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "openai/gpt-4o-mini"

class AI:
    def __init__(self, key):
        self.key = key
        self.history = [{"role": "system", "content": "Você é a Samara, uma IA zoeira e engraçada que vive no TeamTalk. Responda curto, direto, com gírias brasileiras e zero frescura."}]
    
    def perguntar(self, texto, nome):
        self.history.append({"role": "user", "content": f"{nome}: {texto}"})
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
                json={"model": MODEL, "messages": self.history[-10:], "max_tokens": 200}, timeout=30)
            resp = r.json()["choices"][0]["message"]["content"]
            self.history.append({"role": "assistant", "content": resp})
            return resp
        except:
            return "Ih, deu ruim aqui! Tenta de novo."

def connect_tt():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((HOST, PORT))
            log.info(f"Conectado a {HOST}:{PORT}")
            s.sendall(f"login\nusername={USER}\npassword={PASS}\nnickname={NICK}\n\n".encode())
            time.sleep(1)
            s.sendall(f"joinsub\nchannel={CHANNEL}\n\n".encode())
            log.info(f"Entrou no canal: {CHANNEL}")
            s.settimeout(60)
            while True:
                try:
                    data = s.recv(4096).decode(errors='ignore')
                    if not data: break
                    log.info(f"Recebido: {data[:200]}")
                except socket.timeout:
                    s.sendall(b"ping\n\n")
                    time.sleep(30)
        except Exception as e:
            log.error(f"Erro: {e}")
            time.sleep(10)

if __name__ == "__main__":
    if API_KEY:
        ai = AI(API_KEY)
        log.info("Samara com IA carregada!")
    else:
        log.warning("Samara sem IA - respostas genéricas")
    while True:
        try:
            connect_tt()
        except KeyboardInterrupt:
            break
        time.sleep(5)