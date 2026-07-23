#!/usr/bin/env python3
"""Jarvis - setup SDK + rodar bot"""
import os, sys, subprocess, urllib.request, shutil, ctypes

print("=== INSTALANDO DEPENDENCIAS ===")
subprocess.run("sudo apt-get update -qq", shell=True, check=True)
subprocess.run("sudo apt-get install -y -qq p7zip-full", shell=True, check=True)
subprocess.run("pip install -q requests teamtalk.py", shell=True, check=True)

print("=== LOCALIZANDO TEAMTALK ===")
import site
tt_dir = os.path.join(site.getsitepackages()[0], "teamtalk")
print(f"TT_DIR={tt_dir}")

print("=== BAIXANDO SDK ===")
url = "https://www.bearware.dk/teamtalksdk/v5.22a/tt5sdk_v5.22a_ubuntu22_x86_64.7z"
urllib.request.urlretrieve(url, "/tmp/s.7z")
print("  OK")

print("=== EXTRAINDO ===")
os.makedirs("/tmp/x", exist_ok=True)
subprocess.run("7z x -y /tmp/s.7z -o/tmp/x > /dev/null 2>&1", shell=True)

print("=== PROCURANDO SDK ===")
found_py = None
found_dll = None
for root, dirs, files in os.walk("/tmp/x"):
    for d in dirs:
        if d == "TeamTalkPy":
            found_py = os.path.join(root, d)
        if d == "TeamTalk_DLL":
            found_dll = os.path.join(root, d)
print(f"  TeamTalkPy={found_py}")
print(f"  TeamTalk_DLL={found_dll}")

print("=== COPIANDO SDK ===")
impl = os.path.join(tt_dir, "implementation")
if os.path.exists(impl):
    shutil.rmtree(impl)
os.makedirs(impl)
shutil.copytree(found_py, os.path.join(impl, "TeamTalkPy"))
shutil.copytree(found_dll, os.path.join(impl, "TeamTalk_DLL"))
with open(os.path.join(impl, "__init__.py"), "w") as f:
    f.write("")

sdk_path = os.path.join(impl, "TeamTalk_DLL")
print(f"SDK_PATH={sdk_path}")

print("=== TESTANDO IMPORT ===")
os.environ["LD_LIBRARY_PATH"] = sdk_path
lib = os.path.join(sdk_path, "libTeamTalk5.so")
print(f"  lib exists: {os.path.exists(lib)}")
ctypes.cdll.LoadLibrary(lib)
from teamtalk import TeamTalkBot
from teamtalk.enums import TeamTalkServerInfo
print("OK - IMPORT FUNCIONOU!")

print("=== RODANDO JARVIS ===")
os.environ["LD_LIBRARY_PATH"] = sdk_path
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
subprocess.run(["python3", "samara_bot.py"], env={**os.environ}, check=True)