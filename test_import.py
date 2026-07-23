import os, sys, ctypes, subprocess

sdk_path = os.environ.get('SDK_PATH', '')
if not sdk_path:
    print("SDK_PATH not set!")
    sys.exit(1)

lib = os.path.join(sdk_path, 'libTeamTalk5.so')
print("lib:", lib, "exists:", os.path.exists(lib))

if not os.path.exists(lib):
    subprocess.run(['find', '/tmp/sdk', '-name', '*.so'], check=False)
    # Also check the teamtalk dir
    tt_dir = os.path.dirname(os.path.dirname(sdk_path))
    for root, dirs, files in os.walk(tt_dir):
        for f in files:
            print("  so:", os.path.join(root, f))
    sys.exit(1)

os.environ['LD_LIBRARY_PATH'] = sdk_path
ctypes.cdll.LoadLibrary(lib)
from teamtalk import TeamTalkBot
from teamtalk.enums import TeamTalkServerInfo
print("OK - IMPORT FUNCIONOU!")