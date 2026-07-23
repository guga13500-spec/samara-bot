#!/usr/bin/env python3
"""
Setup Jarvis - Baixa o SDK do TeamTalk 5 e instala junto do pacote teamtalk
"""
import os, sys, shutil, urllib.request, platform

SDK_URL = "https://www.bearware.dk/teamtalksdk/v5.22a/tt5sdk_v5.22a_ubuntu22_x86_64.7z"

print("=" * 50)
print("SETUP JARVIS - SDK do TeamTalk 5")
print("=" * 50)

# 1. Encontrar onde o teamtalk.py está instalado
import teamtalk
teamtalk_dir = os.path.dirname(teamtalk.__file__)
impl_dir = os.path.join(teamtalk_dir, "implementation")
print(f"📁 TeamTalk instalado em: {teamtalk_dir}")
print(f"📁 Implementation: {impl_dir}")

# 2. Verificar se já tem SDK
dll_path = os.path.join(impl_dir, "TeamTalk_DLL", "libTeamTalk5.so")
if os.path.exists(dll_path):
    print(f"✅ SDK já instalado: {dll_path}")
    sys.exit(0)

# 3. Baixar SDK
sdk_path = "/tmp/ttsdk.7z"
print(f"\n📥 Baixando SDK v5.22a...")
if not os.path.exists(sdk_path):
    urllib.request.urlretrieve(SDK_URL, sdk_path)
    size_mb = os.path.getsize(sdk_path) / 1024 / 1024
    print(f"   ✅ SDK baixado ({size_mb:.1f} MB)")
else:
    print(f"   ✅ SDK já existe")

# 4. Extrair
extract_dir = "/tmp/ttsdk_extracted"
print(f"\n📦 Extraindo SDK...")
os.makedirs(extract_dir, exist_ok=True)
ret = os.system(f"7z x -y {sdk_path} -o{extract_dir} > /dev/null 2>&1")
if ret != 0:
    print(f"   ❌ Erro na extração (código {ret})")
    sys.exit(1)

# 5. Encontrar TeamTalkPy e TeamTalk_DLL
found_py = None
found_dll = None
for root, dirs, files in os.walk(extract_dir):
    for d in dirs:
        if d == "TeamTalkPy":
            found_py = os.path.join(root, d)
        if d == "TeamTalk_DLL":
            found_dll = os.path.join(root, d)

if not found_py or not found_dll:
    print(f"   ❌ Não encontrou TeamTalkPy ou TeamTalk_DLL")
    for root, dirs, files in os.walk(extract_dir):
        for d in dirs:
            print(f"   Dir: {os.path.join(root, d)}")
    sys.exit(1)

print(f"   ✅ TeamTalkPy: {found_py}")
print(f"   ✅ TeamTalk_DLL: {found_dll}")

# 6. Copiar para o diretório implementation do teamtalk
print(f"\n📋 Copiando para {impl_dir}...")
if os.path.exists(impl_dir):
    shutil.rmtree(impl_dir)

os.makedirs(impl_dir, exist_ok=True)
shutil.copytree(found_py, os.path.join(impl_dir, "TeamTalkPy"))
shutil.copytree(found_dll, os.path.join(impl_dir, "TeamTalk_DLL"))

# 7. Criar __init__.py vazio
init_file = os.path.join(impl_dir, "__init__.py")
with open(init_file, "w") as f:
    f.write("")

# 8. Remover testes
test_dir = os.path.join(impl_dir, "TeamTalkPy", "test")
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)

# 9. Verificar
dll_path = os.path.join(impl_dir, "TeamTalk_DLL", "libTeamTalk5.so")
if os.path.exists(dll_path):
    print(f"\n🎉 SDK instalado com sucesso em {impl_dir}!")
    print(f"   ✅ libTeamTalk5.so encontrado!")
else:
    print(f"\n❌ libTeamTalk5.so não encontrado!")
    for root, dirs, files in os.walk(impl_dir):
        for f in files:
            print(f"   {os.path.join(root, f)}")
    sys.exit(1)