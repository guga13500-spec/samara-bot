#!/usr/bin/env python3
"""
JARVIS v1 - Assistente IA para TeamTalk 5
Conecta via teamtalk.py, usa OpenRouter pra responder
Personalidade: zoeira, direta, brasileira
"""

import os, sys, time, json, requests, logging, asyncio
from teamtalk import TeamTalkBot, TeamTalkServerInfo
from teamtalk.enums import UserStatusMode

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("Jarvis")

HOST = "tt5.angelsclan.net"
PORT = 23351
USER = "Gustavo"
PASS = "2007"
NICK = "Jarvis"
CHANNEL_NAME = "Grupo dos Amigos"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "openai/gpt-4o-mini"

class Cerebro:
    def __init__(self, key):
        self.key = key
        self.hist = [{"role": "system", "content": "Você é o Jarvis, uma IA zoeira e brincalhona do TeamTalk. Responda curto, direto, com gírias brasileiras, sem moralismo e sem frescura. Seja autêntico e engraçado."}]

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
    bot = TeamTalkBot(client_name="JarvisBot")
    cereb = Cerebro(API_KEY) if API_KEY else None

    server_info = TeamTalkServerInfo(
        host=HOST,
        tcp_port=PORT,
        udp_port=PORT,
        username=USER,
        password=PASS,
        nickname=NICK,
        join_channel_id=0
    )

    @bot.event
    async def on_ready():
        log.info("✅ Jarvis online!")
        # Procurar o canal pelo nome
        log.info(f"🔍 Procurando canal: {CHANNEL_NAME}")
        # Enviar mensagem de boas-vindas
        time.sleep(2)
        try:
            await bot.send_message("Fala galera! Jarvis na área, prepara que o bagulho vai ficar bom! 🤖🔥")
            log.info("✅ Mensagem de entrada enviada!")
        except Exception as e:
            log.error(f"Erro ao enviar mensagem: {e}")

    @bot.event
    async def on_message(msg):
        texto = msg.content.strip() if hasattr(msg, 'content') else str(msg).strip()
        nome = msg.user.nickname if hasattr(msg, 'user') and msg.user else "Alguém"
        if not texto or nome == NICK:
            return
        log.info(f"💬 {nome}: {texto}")
        if cereb:
            resposta = cereb.perguntar(texto, nome)
            await bot.send_message(resposta)
            log.info(f"🤖 Jarvis: {resposta[:100]}")

    log.info(f"🔗 Conectando em {HOST}:{PORT}...")
    bot.add_server(server_info)
    bot.run()

if __name__ == "__main__":
    log.info("🧠 Jarvis iniciando...")
    if API_KEY:
        log.info("✅ OpenRouter configurada!")
    else:
        log.warning("⚠️ Sem OPENROUTER_API_KEY - modo offline")
    main()