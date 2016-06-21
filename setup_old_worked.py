import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["paramiko_expect", "paramiko", "os", "glob"], "excludes": [""]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = 'Console'
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(  name = "my-app",
        version = "0.0.1",
        description = "Copyright 2016",
        options = {"build_exe": build_exe_options},
        executables = [Executable("cp_new_with_commands_hardcoded.py", base=base)])

