from cx_Freeze import setup, Executable
import sys

sys.setrecursionlimit(2000)

build_exe_options = {
    "packages": ["selenium", "bs4", "tkinter", "webdriver_manager", "threading", "openpyxl", "requests"],
    "excludes": [],
    "include_files": [],  # If you have other files like icons, add them here
}

bdist_msi_options = {
    'upgrade_code': '{5E505EAA-23AA-4517-A1A3-2F99408C5A60}',  # A unique UUID for your application
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % ("CarData", "CarDataScraper"),  # Change 'YourCompany' to your actual company's name
    'data': {
        'Shortcut': [
            ("DesktopShortcut",        # Shortcut
             "DesktopFolder",          # Directory_
             "CarDataScraper",         # Name
             "TARGETDIR",              # Component_
             "[TARGETDIR]main.exe",    # Target
             None,                     # Arguments
             None,                     # Description
             None,                     # Hotkey
             None,                     # Icon
             None,                     # IconIndex
             None,                     # ShowCmd
             'TARGETDIR'               # WkDir
             )
        ]
    }
}

base = None

setup(
    name="CarDataScraper",
    version="3.0",
    description="Car Data Scraper application",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[Executable("main.py", base=base, icon="car-data.ico")]
)
