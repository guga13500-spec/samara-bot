#!/bin/bash
set -e

echo "=== INSTALANDO DEPENDENCIAS ==="
sudo apt-get update -qq
sudo apt-get install -y -qq p7zip-full
pip install -q requests teamtalk.py

echo "=== LOCALIZANDO TEAMTALK ==="
TT_DIR=$(python3 -c "import site; print(site.getsitepackages()[0])")/teamtalk
echo "TT_DIR=$TT_DIR"

echo "=== BAIXANDO SDK ==="
curl -s -o /tmp/ttsdk.7z "https://www.bearware.dk/teamtalksdk/v5.22a/tt5sdk_v5.22a_ubuntu22_x86_64.7z"
ls -la /tmp/ttsdk.7z

echo "=== EXTRAINDO ==="
7z x -y /tmp/ttsdk.7z -o/tmp/sdk > /dev/null 2>&1
echo "OK"

echo "=== COPIANDO SDK ==="
FP=$(find /tmp/sdk -type d -name TeamTalkPy | head -1)
FD=$(find /tmp/sdk -type d -name TeamTalk_DLL | head -1)
rm -rf "$TT_DIR/implementation"
mkdir -p "$TT_DIR/implementation"
cp -r "$FP" "$TT_DIR/implementation/TeamTalkPy"
cp -r "$FD" "$TT_DIR/implementation/TeamTalk_DLL"
touch "$TT_DIR/implementation/__init__.py"

export SDK_PATH="$TT_DIR/implementation/TeamTalk_DLL"
export LD_LIBRARY_PATH="$SDK_PATH"

echo "=== TESTANDO IMPORT ==="
python3 -c "
import os, ctypes, sys
os.environ['LD_LIBRARY_PATH'] = '$SDK_PATH'
ctypes.cdll.LoadLibrary('$SDK_PATH/libTeamTalk5.so')
from teamtalk import TeamTalkBot
from teamtalk.enums import TeamTalkServerInfo
print('OK - IMPORT FUNCIONOU!')
"

echo "=== RODANDO JARVIS ==="
export OPENROUTER_API_KEY="$1"
python3 samara_bot.py