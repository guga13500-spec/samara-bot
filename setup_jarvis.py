#!/usr/bin/env python3
"""
Setup Jarvis - Baixa e instala o SDK do TeamTalk 5 no pacote teamtalk
"""
import os, sys, shutil, urllib.request, subprocess, glob, platform

SDK_URL = "https://www.bearware.dk/teamtalksdk/v5.22a/tt5sdk_v5.22a_ubuntu22_x86_64.7z"

print("=" * 50)
print("SETUP JARVIS - SDK do TeamTalk 5")
print("=" * 50)

# Encontrar diretório do teamtalk sem importar
result = subprocess.run(["pip", "show", "teamtalk.py"], capture_output=True, text=True)
teamtalk_dir = None
for line in result.stdout.split("\n"):
    if line.startswith("Location:"):
        teamtalk_dir = os.path.join(line.split(":")[1].strip(), "teamtalk")
        break

if not teamtalk_dir or not os.path.exists(teamtalk_dir):
    print("❌ teamtalk.py não encontrado!")
    # Tentar achar no site-packages
    import site
    for sp in site.getsitepackages():
        d = os.path.join(sp, "teamtalk")
        if os.path.exists(d):
            teamtalk_dir = d
            break

print(f"📁 TeamTalk em: {teamtalk_dir}")

impl_dir = os.path.join(teamtalk_dir, "implementation")

# Verificar se já instalou
dll = os.path.join(impl_dir, "TeamTalk_DLL", "libTeamTalk5.so")
if os.path.exists(dll):
    print(f"✅ SDK já instalado!")
    sys.exit(0)

# Baixar SDK
sdk_7z = "/tmp/ttsdk.7z"
if not os.path.exists(sdk_7z):
    print(f"\n📥 Baixando SDK v5.22a...")
    urllib.request.urlretrieve(SDK_URL, sdk_7z)
    mb = os.path.getsize(sdk_7z) / 1024 / 1024
    print(f"   ✅ {mb:.1f} MB")

# Extrair
extract_dir = "/tmp/ttsdk_extracted"
print(f"\n📦 Extraindo...")
os.makedirs(extract_dir, exist_ok=True)
ret = os.system(f"7z x -y {sdk_7z} -o{extract_dir} > /dev/null 2>&1")
if ret != 0:
    print(f"❌ Erro extraindo, tentando patool...")
    import patoolib
    patoolib.extract_archive(sdk_7z, outdir=extract_dir)

# Encontrar os diretórios
found_py = found_dll = None
for root, dirs, files in os.walk(extract_dir):
    for d in dirs:
        if d == "TeamTalkPy":
            found_py = os.path.join(root, d)
        if d == "TeamTalk_DLL":
            found_dll = os.path.join(root, d)

if not found_py or not found_dll:
    print(f"❌ Não encontrou SDK!")
    for root, dirs, _ in os.walk(extract_dir):
        for d in dirs:
            print(f"   {os.path.join(root, d)}")
    sys.exit(1)

print(f"✅ TeamTalkPy: {found_py}")
print(f"✅ TeamTalk_DLL: {found_dll}")

# Copiar
print(f"\n📋 Instalando SDK...")
if os.path.exists(impl_dir):
    shutil.rmtree(impl_dir)
os.makedirs(impl_dir)
shutil.copytree(found_py, os.path.join(impl_dir, "TeamTalkPy"))
shutil.copytree(found_dll, os.path.join(impl_dir, "TeamTalk_DLL"))
with open(os.path.join(impl_dir, "__init__.py"), "w") as f:
    f.write("")

# Remover testes
test_dir = os.path.join(impl_dir, "TeamTalkPy", "test")
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)

# Verificar
if os.path.exists(dll):
    print(f"\n🎉 SDK instalado com sucesso!")
else:
    print(f"\n❌ Falhou!")
    sys.exit(1)