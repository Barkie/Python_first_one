import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "rulebases_to_excel",
        version = "0.1",
        description = "no description, soryan-boryan_v2",
        options = {"build_exe": build_exe_options},
        executables = [Executable("full_cpinfo_cpinfo_rule_search_xlsx_append_def_init_inside.py", base=base)])
