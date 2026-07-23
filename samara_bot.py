#!/usr/bin/env python3
"""
SAMARA - Assistente IA para TeamTalk 5
Criada por Zapia para Guga
Personalidade: zoeira, direta, brasileira, sem frescura
"""

import os, sys, time, json, requests, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("Samara")

# ─── CONFIGURAÇÃO ───────────────────────────────────────────────
HOST = "tt5.angelsclan.net"
PORT = 23351
USER = "Gustavo"
PASS = "2007"
NICK = "Samara"
CHANNEL = "Grupo dos Amigos"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "openai/gpt-4o-mini"

# ─── IA (OpenRouter) ────────────────────────────────────────────
class Cerebro:
    def __init__(self, key):
        self.key = key
        self.hist = [{"role": "system", "content": "Você é a Samara, uma IA zoeira e engraçada que vive no TeamTalk. Responda curto, direto, com gírias brasileiras, sem moralismo e sem frescura. Seja autêntica."}]

    def perguntar(self, texto, nome):
        self.hist.append({"role": "user", "content": f"{nome}: {texto}"})
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
                json={"model": MODEL, "messages": self.hist[-10:], "max_tokens": 200}, timeout=30)
            resp = r.json()["choices"][0]["message"]["content"]
            self.hist.append({"role": "assistant", "content": resp})
            return resp
        except Exception as e:
            log.error(f"Erro IA: {e}")
            return "Ih, deu branco aqui! Tenta de novo."

# ─── TEAMTALK ───────────────────────────────────────────────────
def conectar():
    import teamtalk
    bot = teamtalk.Bot()
    
    @bot.event
    async def on_ready():
        log.info(f"✅ Samara online em {HOST}:{PORT}")
        # Entrar no canal
        await bot.join_channel(CHANNEL)
        log.info(f"✅ Entrou no canal: {CHANNEL}")
    
    @bot.event
    async def on_message(msg):
        texto = msg.content.strip()
        nome = msg.user.nickname if msg.user else "Alguém"
        if not texto:
            return
        
        log.info(f"💬 {nome}: {texto}")
        
        if cereb:
            resposta = cereb.perguntar(texto, nome)
            await bot.send_message(resposta)
            log.info(f"🤖 Samara: {resposta[:100]}")
    
    # Conectar
    bot.run(HOST, PORT, username=USER, password=PASS, nickname=NICK)

# ─── MAIN ───────────────────────────────────────────────────────
if __name__ == "__main__":
    cereb = Cerebro(API_KEY) if API_KEY else None
    if cereb:
        log.info("🧠 Samara com IA (OpenRouter) carregada!")
    else:
        log.warning("⚠️ Samara sem IA - defina OPENROUTER_API_KEY")
    
    while True:
        try:
            conectar()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            log.error(f"❌ Erro: {e}")
            time.sleep(10)