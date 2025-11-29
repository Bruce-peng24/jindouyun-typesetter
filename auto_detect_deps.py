#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5组件和Python标准库自动检测脚本
用于自动检测项目中实际使用的PyQt5组件和Python标准库模块，并生成相应的PyInstaller配置
"""

import os
import re
import ast
import sys
from typing import Set, List, Tuple, Dict

def find_python_files(directory: str) -> List[str]:
    """查找目录中的所有Python文件"""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_pyqt5_imports(file_path: str) -> Set[str]:
    """从Python文件中提取PyQt5相关的导入"""
    pyqt5_modules = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用AST解析导入语句
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith('PyQt5'):
                            parts = alias.name.split('.')
                            if len(parts) > 1:
                                pyqt5_modules.add(parts[1])  # 获取PyQt5后面的模块名
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith('PyQt5'):
                        parts = node.module.split('.')
                        if len(parts) > 1:
                            pyqt5_modules.add(parts[1])  # 获取PyQt5后面的模块名
        except SyntaxError:
            # 如果AST解析失败，使用正则表达式作为备选方案
            pattern = r'(?:from\s+PyQt5\.(\w+)|import\s+PyQt5\.(\w+))'
            matches = re.findall(pattern, content)
            for match in matches:
                module = match[0] if match[0] else match[1]
                if module:
                    pyqt5_modules.add(module)
    except (UnicodeDecodeError, IOError):
        pass
    
    return pyqt5_modules

def extract_stdlib_imports(file_path: str) -> Set[str]:
    """从Python文件中提取Python标准库相关的导入"""
    stdlib_modules = set()
    
    # 获取Python标准库模块列表
    stdlib_list = get_stdlib_modules()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用AST解析导入语句
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        # 获取顶级模块名
                        module_name = alias.name.split('.')[0]
                        if module_name in stdlib_list:
                            stdlib_modules.add(module_name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        # 获取顶级模块名
                        module_name = node.module.split('.')[0]
                        if module_name in stdlib_list:
                            stdlib_modules.add(module_name)
        except SyntaxError:
            # 如果AST解析失败，使用正则表达式作为备选方案
            pattern = r'(?:from\s+(\w+)|import\s+(\w+))'
            matches = re.findall(pattern, content)
            for match in matches:
                module_name = match[0] if match[0] else match[1]
                if module_name and module_name in stdlib_list:
                    stdlib_modules.add(module_name)
    except (UnicodeDecodeError, IOError):
        pass
    
    return stdlib_modules

def get_stdlib_modules() -> Set[str]:
    """获取Python标准库模块列表"""
    # 常见的Python标准库模块
    stdlib_modules = {
        'abc', 'argparse', 'array', 'asyncio', 'atexit', 'base64', 'bdb', 'binascii', 
        'bisect', 'builtins', 'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmd', 'code', 
        'codecs', 'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 
        'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 
        'ctypes', 'curses', 'dataclasses', 'datetime', 'decimal', 'difflib', 'dis', 
        'doctest', 'email', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 
        'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools', 
        'gc', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip', 'hashlib', 'heapq', 
        'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 
        'io', 'ipaddress', 'itertools', 'json', 'keyword', 'linecache', 'locale', 
        'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 
        'mmap', 'modulefinder', 'multiprocessing', 'netrc', 'nntplib', 'numbers', 
        'operator', 'optparse', 'os', 'ossaudiodev', 'pathlib', 'pdb', 'pickle', 
        'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix', 
        'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 
        'queue', 'quopri', 'random', 're', 'readline', 'reprlib', 'resource', 
        'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve', 
        'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 
        'socketserver', 'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 
        'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 
        'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'textwrap', 
        'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize', 'trace', 
        'traceback', 'tracemalloc', 'tty', 'turtle', 'types', 'typing', 'unicodedata', 
        'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 
        'webbrowser', 'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 
        'zipapp', 'zipfile', 'zipimport', 'zlib'
    }
    
    # 添加平台特定的标准库模块
    if sys.platform.startswith('win'):
        stdlib_modules.update(['msvcrt', 'win32api', 'win32con', 'win32file', 'win32gui'])
    elif sys.platform.startswith('linux'):
        stdlib_modules.update(['fcntl', 'grp', 'pwd', 'posix', 'pty', 'termios'])
    
    return stdlib_modules

def generate_pyqt5_config(project_dir: str = "src") -> str:
    """生成PyQt5相关的PyInstaller配置"""
    python_files = find_python_files(project_dir)
    all_pyqt5_modules = set()
    
    for file_path in python_files:
        modules = extract_pyqt5_imports(file_path)
        all_pyqt5_modules.update(modules)
    
    # 确保核心模块始终包含
    core_modules = {'Qt', 'QtCore', 'QtGui', 'QtWidgets'}
    all_pyqt5_modules.update(core_modules)
    
    # 生成配置字符串
    config_lines = [
        "# === 自动生成的PyQt5配置 ===",
        "# 以下配置由generate_pyqt5_config.py自动生成，请勿手动修改",
        "from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs",
        "",
        "# 自动检测到的PyQt5组件:",
        f"# 检测到的模块: {sorted(all_pyqt5_modules)}",
        "",
    ]
    
    # 为每个模块生成收集配置
    for module in sorted(all_pyqt5_modules):
        full_module_name = f"PyQt5.{module}"
        config_lines.extend([
            f"datas += collect_data_files('{full_module_name}')",
            f"binaries += collect_dynamic_libs('{full_module_name}')",
            f"hiddenimports += collect_submodules('{full_module_name}')",
        ])
    
    config_lines.extend([
        "",
        "# === 自动生成的Python标准库排除列表 ===",
        "# 以下是由generate_pyqt5_config.py自动生成的标准库排除列表",
        "",
    ])
    
    # 生成标准库排除列表
    all_stdlib_modules = set()
    for file_path in python_files:
        modules = extract_stdlib_imports(file_path)
        all_stdlib_modules.update(modules)
    
    # 获取所有标准库模块
    all_available_stdlib = get_stdlib_modules()
    
    # 计算未使用的标准库模块（这些将被排除）
    unused_stdlib = sorted(all_available_stdlib - all_stdlib_modules)
    
    # 过滤掉一些可能会引起问题的模块
    filtered_excludes = []
    for module in unused_stdlib:
        # 保留一些可能会被间接需要的模块
        if module not in ['sys', 'os', 'builtins', 'types', 'importlib', 'io']:
            filtered_excludes.append(f"'{module}'")
    
    if filtered_excludes:
        # 将排除项分成多行，每行8个
        excludes_lines = []
        for i in range(0, len(filtered_excludes), 8):
            chunk = filtered_excludes[i:i+8]
            if i == 0:
                excludes_lines.append("excludes=[\n    " + ", ".join(chunk) + ",")
            else:
                excludes_lines.append("    " + ", ".join(chunk) + ",")
        excludes_lines.append("],")
        
        # 不再添加中文注释，直接添加排除列表
        for line in excludes_lines:
            config_lines.append(line)
    
    config_lines.extend([
        "",
        "# === 以下为手动添加的其他依赖 ===",
        "",
    ])
    
    return "\n".join(config_lines)

def update_spec_file(spec_file: str, config: str):
    """更新spec文件中的PyQt5配置和标准库排除列表"""
    with open(spec_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找PyQt5配置部分的开始和结束
    start_marker = "# === 自动生成的PyQt5配置 ==="
    end_marker = "# === 以下为手动添加的其他依赖 ==="
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        # 替换现有的自动生成部分
        new_content = content[:start_idx] + config + content[end_idx:]
    else:
        # 如果没有找到标记，在import语句后插入
        import_end = content.find("\n\n", content.find("from PyInstaller.utils.hooks import"))
        if import_end != -1:
            new_content = content[:import_end] + "\n\n" + config + content[import_end:]
        else:
            raise ValueError("无法在spec文件中找到合适的位置插入配置")
    
    # 更新Analysis部分的excludes
    if "excludes=[" in new_content:
        # 找到excludes部分
        excludes_start = new_content.find("excludes=[")
        excludes_end = new_content.find("],", excludes_start)
        
        if excludes_end != -1:
            # 在配置中查找excludes列表
            excludes_start_in_config = config.find("excludes=[")
            excludes_end_in_config = config.find("],", excludes_start_in_config)
            
            if excludes_start_in_config != -1 and excludes_end_in_config != -1:
                # 提取排除列表内容
                excludes_content = config[excludes_start_in_config:excludes_end_in_config+2]
                
                # 替换原有的excludes
                new_content = (
                    new_content[:excludes_start] + 
                    excludes_content + 
                    new_content[excludes_end+2:]
                )
    
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已更新 {spec_file} 中的PyQt5配置和标准库排除列表")

def test_detection(src_dir="src"):
    """测试自动检测功能"""
    print("测试PyQt5和Python标准库自动检测系统")
    print("=" * 50)
    
    # 查找Python文件
    python_files = find_python_files(src_dir)
    print(f"找到 {len(python_files)} 个Python文件:")
    for file in python_files:
        print(f"  - {file}")
    
    print("\n生成的配置:")
    print("-" * 30)
    config = generate_pyqt5_config(src_dir)
    print(config)
    
    print("\n测试完成!")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="自动检测PyQt5组件并更新PyInstaller spec文件")
    parser.add_argument("--spec", default="Pandoc-GUI.spec", help="PyInstaller spec文件路径")
    parser.add_argument("--src", default="src", help="源代码目录路径")
    parser.add_argument("--print-only", action="store_true", help="只打印配置而不更新文件")
    parser.add_argument("--test", action="store_true", help="测试自动检测功能而不更新文件")
    
    args = parser.parse_args()
    
    if args.test:
        test_detection(args.src)
    else:
        config = generate_pyqt5_config(args.src)
        
        if args.print_only:
            print(config)
        else:
            update_spec_file(args.spec, config)
            print("PyQt5配置已更新!")