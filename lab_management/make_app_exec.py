from cx_Freeze import setup, Executable

base = None    

executables = [Executable("run.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "<sunda_desktop_app>",
    options = options,
    version = "<Test_001>",
    description = '<not Sure and not So much>',
    executables = executables
)