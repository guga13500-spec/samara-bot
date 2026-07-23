#!/usr/bin/env python3
"""Setup SDK + roda Jarvis - tudo num script"""
import os, sys, subprocess, shutil, urllib.request, ctypes, site

def run(cmd, **kwargs):
    print(f"$ {cmd}")
    return subprocess.run(cmd, shell=True, **kwargs)

print("=" * 50)
print("JARVIS - SETUP SDK E BOT")
print("=" * 50)

# 1. Dependências
print("\n[1/5] Instalando dependencias...")
run("sudo apt-get update -qq")
run("sudo apt-get install -y -qq p7zip-full")
run("pip install -q requests teamtalk.py")

# 2. Localizar teamtalk
print("\n[2/5] Localizando teamtalk.py...")
tt_dir = os.path.join(site.getsitepackages()[0], "teamtalk")
print(f"  TeamTalk: {tt_dir}")

# 3. Baixar SDK
print("\n[3/5] Baixando SDK TeamTalk 5...")
sdk_url = "https://www.bearware.dk/teamtalksdk/v5.22a/tt5sdk_v5.22a_ubuntu22_x86_64.7z"
sdk_file = "/tmp/ttsdk.7z"
if not os.path.exists(sdk_file):
    urllib.request.urlretrieve(sdk_url, sdk_file)
print(f"  OK ({os.path.getsize(sdk_file)/1024/1024:.1f} MB)")

# 4. Extrair e copiar SDK
print("\n[4/5] Instalando SDK...")
extract_dir = "/tmp/ttsdk_extracted"
if os.path.exists(extract_dir):
    shutil.rmtree(extract_dir)
os.makedirs(extract_dir, exist_ok=True)

run(f"7z x -y {sdk_file} -o{extract_dir} > /dev/null 2>&1")

# Encontrar diretórios
found_py = found_dll = ""
for root, dirs, files in os.walk(extract_dir):
    if "TeamTalkPy" in dirs:
        found_py = os.path.join(root, "TeamTalkPy")
    if "TeamTalk_DLL" in dirs:
        found_dll = os.path.join(root, "TeamTalk_DLL")

print(f"  TeamTalkPy: {found_py}")
print(f"  TeamTalk_DLL: {found_dll}")

impl = os.path.join(tt_dir, "implementation")
if os.path.exists(impl):
    shutil.rmtree(impl)
os.makedirs(impl)

shutil.copytree(found_py, os.path.join(impl, "TeamTalkPy"))
shutil.copytree(found_dll, os.path.join(impl, "TeamTalk_DLL"))
with open(os.path.join(impl, "__init__.py"), "w") as f:
    f.write("")

# Remover testes
test_dir = os.path.join(impl, "TeamTalkPy", "test")
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)

sdk_path = os.path.join(impl, "TeamTalk_DLL")
print(f"  SDK_PATH: {sdk_path}")

# 5. Testar import
print("\n[5/5] Testando import...")
os.environ["LD_LIBRARY_PATH"] = sdk_path
lib = os.path.join(sdk_path, "libTeamTalk5.so")
print(f"  libTeamTalk5.so: {os.path.exists(lib)}")

ctypes.cdll.LoadLibrary(lib)
from teamtalk import TeamTalkBot
from teamtalk.enums import TeamTalkServerInfo
print("  ✅ IMPORT FUNCIONOU!")

# 6. Rodar bot
print("\n" + "=" * 50)
print("RODANDO JARVIS...")
print("=" * 50)
os.environ["SDK_PATH"] = sdk_path
os.environ["LD_LIBRARY_PATH"] = sdk_path

# Mudar pro diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Rodar bot
sys.path.insert(0, script_dir)
exec(open("samara_bot.py").read())