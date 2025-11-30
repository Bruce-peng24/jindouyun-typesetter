# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('src', 'src'), ('pandoc', 'pandoc')]
binaries = []
hiddenimports = []

# === 自动生成的PyQt5配置 ===
# 以下配置由generate_pyqt5_config.py自动生成，请勿手动修改
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

# 自动检测到的PyQt5组件:
# 检测到的模块: ['Qt', 'QtCore', 'QtGui', 'QtWidgets']

datas += collect_data_files('PyQt5.Qt')
binaries += collect_dynamic_libs('PyQt5.Qt')
hiddenimports += collect_submodules('PyQt5.Qt')
datas += collect_data_files('PyQt5.QtCore')
binaries += collect_dynamic_libs('PyQt5.QtCore')
hiddenimports += collect_submodules('PyQt5.QtCore')
datas += collect_data_files('PyQt5.QtGui')
binaries += collect_dynamic_libs('PyQt5.QtGui')
hiddenimports += collect_submodules('PyQt5.QtGui')
datas += collect_data_files('PyQt5.QtWidgets')
binaries += collect_dynamic_libs('PyQt5.QtWidgets')
hiddenimports += collect_submodules('PyQt5.QtWidgets')

# === 自动生成的Python标准库排除列表 ===
# 以下是由generate_pyqt5_config.py自动生成的标准库排除列表

excludes=[
    'abc', 'argparse', 'array', 'asyncio', 'atexit', 'base64', 'bdb', 'binascii',
    'bisect', 'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmd', 'code',
    'codecs', 'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib',
    'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 'ctypes', 'curses', 'dataclasses',
    'decimal', 'difflib', 'dis', 'doctest', 'email', 'enum', 'errno', 'faulthandler',
    'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools',
    'gc', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip', 'hashlib',
    'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp', 'inspect',
    'ipaddress', 'itertools', 'json', 'keyword', 'linecache', 'locale', 'logging', 'lzma',
    'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'msvcrt',
    'multiprocessing', 'netrc', 'nntplib', 'numbers', 'operator', 'optparse', 'ossaudiodev', 'pathlib',
    'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib',
    'posix', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr',
    'pydoc', 'queue', 'quopri', 'random', 're', 'readline', 'reprlib', 'resource',
    'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex',
    'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver',
    'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'sunau',
    'symbol', 'symtable', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'termios',
    'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize', 'trace',
    'traceback', 'tracemalloc', 'tty', 'turtle', 'typing', 'unicodedata', 'unittest', 'urllib',
    'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'win32api',
    'win32con', 'win32file', 'win32gui', 'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml',
    'xmlrpc', 'zipapp', 'zipfile', 'zipimport', 'zlib',
],

# === 以下为手动添加的其他依赖 ===
# === 以下为手动添加的其他依赖 ===
tmp_ret = collect_all('ntplib')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['app_minimal_fixed.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='jindouyun-typesetter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        'vcruntime140.dll', 'msvcp140.dll', 'api-ms-win-*.dll',
        # 添加已知可能导致UPX压缩问题的Qt5 DLL
        'Qt5WebEngineCore.dll', 'Qt5WebEngineWidgets.dll',
        'Qt5Multimedia.dll', 'Qt5MultimediaWidgets.dll',
        # 添加其他已知可能有问题的DLL
        'Qt5NetworkAuth.dll', 'Qt5Quick.dll', 'Qt5QuickControls2.dll',
        'Qt5QuickWidgets.dll', 'Qt5Qml.dll'
    ],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
