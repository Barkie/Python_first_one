import sys
import cx_Freeze
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
#buildOptions = {"packages": [], "excludes": [""]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

mainScript = 'winpexpect_test.py'
targetDir = 'c:/python/git/build_new'
setup(
    name = 'test',
    version = '0.1',
    description = 'test',
    #options = dict(build_exe = buildOptions),
    executables = [Executable(
        mainScript,
        targetName='test.exe',
        #base="Console",
#        appendScriptToExe=True
    ), Executable(
        'expectstub.py',
        targetName='expectStub.exe',
        #base="Console",
#        appendScriptToExe=True
    )]
)