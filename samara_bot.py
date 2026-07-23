#!/usr/bin/env python3
"""
SAMARA v3 - Assistente IA para TeamTalk 5
Conecta via teamtalk.py, usa OpenRouter pra responder
Personalidade: zoeira, direta, brasileira
"""

import os, sys, time, json, requests, logging, asyncio

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

class Cerebro:
    def __init__(self, key):
        self.key = key
        self.hist = [{"role": "system", "content": "Você é a Samara, uma IA zoeira e engraçada do TeamTalk. Responda curto, direto, com gírias brasileiras, sem moralismo e sem frescura. Seja autêntica."}]

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

def main():
    import teamtalk
    bot = teamtalk.Bot()
    cereb = Cerebro(API_KEY) if API_KEY else None

    @bot.event
    async def on_ready():
        log.info("✅ Samara online!")
        await bot.join_channel(CHANNEL)
        log.info(f"✅ Entrou no canal: {CHANNEL}")
        if cereb:
            await bot.send_message("Salve salve, família! Samara chegou pra alegrar o grupo! 🎉")
        else:
            await bot.send_message("Salve! Samara online! (modo offline - sem IA)")

    @bot.event
    async def on_message(msg):
        texto = msg.content.strip()
        nome = msg.user.nickname if msg.user else "Alguém"
        if not texto or nome == NICK:
            return
        log.info(f"💬 {nome}: {texto}")
        if cereb:
            resposta = cereb.perguntar(texto, nome)
            await bot.send_message(resposta)
            log.info(f"🤖 Samara: {resposta[:100]}")

    bot.run(HOST, PORT, username=USER, password=PASS, nickname=NICK)

if __name__ == "__main__":
    log.info("🧠 Samara iniciando...")
    if API_KEY:
        log.info("✅ OpenRouter configurada!")
    else:
        log.warning("⚠️ Sem OPENROUTER_API_KEY - modo offline")
    main()