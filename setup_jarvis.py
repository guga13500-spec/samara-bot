#!/usr/bin/env python3
"""
Setup Jarvis - Baixa o SDK do TeamTalk 5 e configura
"""
import os, sys, json, requests, shutil, urllib.request

SDK_URL = "https://www.bearware.dk/teamtalksdk/v5.22a/tt5sdk_v5.22a_ubuntu22_x86_64.7z"
SDK_PATH = "/tmp/ttsdk.7z"
EXTRACT_DIR = "/tmp/ttsdk_extracted"
IMPLEMENTATION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "implementation")

print("=" * 50)
print("SETUP JARVIS - SDK do TeamTalk 5")
print("=" * 50)

# 1. Baixar SDK
print(f"\n📥 Baixando SDK de v5.22a...")
if not os.path.exists(SDK_PATH):
    urllib.request.urlretrieve(SDK_URL, SDK_PATH)
    size_mb = os.path.getsize(SDK_PATH) / 1024 / 1024
    print(f"   ✅ SDK baixado ({size_mb:.1f} MB)")
else:
    print(f"   ✅ SDK já existe")

# 2. Extrair - assume que 7z está instalado pelo apt
print(f"\n📦 Extraindo SDK...")
os.makedirs(EXTRACT_DIR, exist_ok=True)
ret = os.system(f"7z x -y {SDK_PATH} -o{EXTRACT_DIR} > /dev/null 2>&1")
if ret != 0:
    print(f"   ❌ Erro na extração (código {ret})")
    sys.exit(1)

# 3. Encontrar os diretórios TeamTalk_DLL e TeamTalkPy
print(f"\n🔍 Procurando TeamTalk_DLL e TeamTalkPy...")
found_py = None
found_dll = None
for root, dirs, files in os.walk(EXTRACT_DIR):
    for d in dirs:
        if d == "TeamTalkPy":
            found_py = os.path.join(root, d)
        if d == "TeamTalk_DLL":
            found_dll = os.path.join(root, d)

if not found_py or not found_dll:
    print(f"   ❌ Não encontrou TeamTalkPy ou TeamTalk_DLL")
    for root, dirs, files in os.walk(EXTRACT_DIR):
        for d in dirs:
            print(f"   Dir: {os.path.join(root, d)}")
    sys.exit(1)

print(f"   ✅ TeamTalkPy: {found_py}")
print(f"   ✅ TeamTalk_DLL: {found_dll}")

# 4. Copiar para o diretório implementation
if os.path.exists(IMPLEMENTATION_DIR):
    shutil.rmtree(IMPLEMENTATION_DIR)
shutil.copytree(found_py, os.path.join(IMPLEMENTATION_DIR, "TeamTalkPy"))
shutil.copytree(found_dll, os.path.join(IMPLEMENTATION_DIR, "TeamTalk_DLL"))

# 5. Criar __init__.py
init_file = os.path.join(IMPLEMENTATION_DIR, "__init__.py")
with open(init_file, "w") as f:
    f.write("")
print(f"   ✅ implementation/ pronto!")

# 6. Remover pasta de testes
test_dir = os.path.join(IMPLEMENTATION_DIR, "TeamTalkPy", "test")
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)

print(f"\n🎉 Setup completo! SDK v5.22a instalado!")
print(f"   📍 {IMPLEMENTATION_DIR}")