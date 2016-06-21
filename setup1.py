import sys
from cx_Freeze import setup, Executable

targetDir = 'c:/python/checkpoint/build_exe/'
mainScript = 'winpexpect_test.py'
targetName = 'first program'

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = []
excludes = []
packages = []
path = []

#buildOptions = {"build_exe": {"includes": includes,
#                              "excludes": excludes,
#                              "packages": packages,
#                              "path": path
#                              }
#                },

setup(
    name = targetName,
    version = '0.1',
    description = 'cawabanga',
#    options = dict(build_exe = buildOptions),
	options = {"build_exe": {"includes": includes}},
    executables = [Executable(
        mainScript,
        targetName='test.exe',
 #       targetDir=targetDir,
        base='Console',
        #appendScriptToExe=True
    ), Executable(
        'expectstub.py',
        targetName='expectStub.exe',
 #       targetDir=targetDir,
        base='Console',
#        appendScriptToExe=True
    )]
)