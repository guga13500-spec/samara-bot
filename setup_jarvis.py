#!/usr/bin/env python3
"""
Setup Jarvis - Baixa o SDK do TeamTalk 5 e instala junto do pacote teamtalk
"""
import os, sys, shutil, urllib.request, glob

SDK_URL = "https://www.bearware.dk/teamtalksdk/v5.22a/tt5sdk_v5.22a_ubuntu22_x86_64.7z"

print("=" * 50)
print("SETUP JARVIS - SDK do TeamTalk 5")
print("=" * 50)

# 1. Encontrar onde o teamtalk.py está instalado sem importar
# Procurar no site-packages
import site
for sp in site.getsitepackages():
    tt_dir = os.path.join(sp, "teamtalk")
    if os.path.exists(tt_dir):
        teamtalk_dir = tt_dir
        break
else:
    # Try pip show
    import subprocess
    result = subprocess.run(["pip", "show", "teamtalk.py"], capture_output=True, text=True)
    for line in result.stdout.split("\n"):
        if line.startswith("Location:"):
            loc = line.split(":")[1].strip()
            teamtalk_dir = os.path.join(loc, "teamtalk")
            break

impl_dir = os.path.join(teamtalk_dir, "implementation")
print(f"📁 TeamTalk em: {teamtalk_dir}")
print(f"📁 Implementation: {impl_dir}")

# 2. Verificar se já tem SDK
dll_path = os.path.join(impl_dir, "TeamTalk_DLL", "libTeamTalk5.so")
if os.path.exists(dll_path):
    print(f"✅ SDK já instalado!")
    sys.exit(0)

# 3. Baixar SDK
sdk_path = "/tmp/ttsdk.7z"
print(f"\n📥 Baixando SDK v5.22a...")
urllib.request.urlretrieve(SDK_URL, sdk_path)
size_mb = os.path.getsize(sdk_path) / 1024 / 1024
print(f"   ✅ Baixado ({size_mb:.1f} MB)")

# 4. Extrair
extract_dir = "/tmp/ttsdk_extracted"
print(f"\n📦 Extraindo...")
os.makedirs(extract_dir, exist_ok=True)
ret = os.system(f"7z x -y {sdk_path} -o{extract_dir} > /dev/null 2>&1")
if ret != 0:
    print(f"   ❌ Erro na extração")
    sys.exit(1)

# 5. Encontrar os diretórios
found_py = found_dll = None
for root, dirs, files in os.walk(extract_dir):
    for d in dirs:
        if d == "TeamTalkPy":
            found_py = os.path.join(root, d)
        if d == "TeamTalk_DLL":
            found_dll = os.path.join(root, d)

if not found_py or not found_dll:
    print(f"❌ Não encontrou SDK")
    for root, dirs, files in os.walk(extract_dir):
        for d in dirs:
            print(f"   Dir: {os.path.join(root, d)}")
    sys.exit(1)

# 6. Copiar
print(f"\n📋 Copiando SDK...")
if os.path.exists(impl_dir):
    shutil.rmtree(impl_dir)
os.makedirs(impl_dir, exist_ok=True)
shutil.copytree(found_py, os.path.join(impl_dir, "TeamTalkPy"))
shutil.copytree(found_dll, os.path.join(impl_dir, "TeamTalk_DLL"))
with open(os.path.join(impl_dir, "__init__.py"), "w") as f:
    f.write("")

# 7. Remover testes
test_dir = os.path.join(impl_dir, "TeamTalkPy", "test")
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)

# 8. Verificar
if os.path.exists(dll_path):
    print(f"\n🎉 SDK instalado! ✅")
else:
    print(f"\n❌ Falhou")
    sys.exit(1)