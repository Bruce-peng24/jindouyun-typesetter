#!/usr/bin/env python3
"""
Pandoc GUI 最小化入口点（修复版本）
解决网络检查问题
"""

import sys
import os

# 获取应用程序路径
if getattr(sys, 'frozen', False):
    # 如果是打包后的可执行文件
    application_path = os.path.dirname(sys.executable)
    
    # 在单文件模式下，所有内容被解压到临时目录
    if hasattr(sys, '_MEIPASS'):
        temp_dir = sys._MEIPASS
        # 添加临时目录到路径
        sys.path.insert(0, temp_dir)
        
        # 尝试添加src目录到路径
        src_path = os.path.join(temp_dir, 'src')
        if os.path.exists(src_path):
            sys.path.insert(0, src_path)
    
    # 也添加应用程序目录到路径
    sys.path.insert(0, application_path)
    src_path = os.path.join(application_path, 'src')
    if os.path.exists(src_path):
        sys.path.insert(0, src_path)
    
    # 确保pandoc路径可用
    pandoc_path = os.path.join(temp_dir, 'pandoc', 'pandoc.exe') if hasattr(sys, '_MEIPASS') else os.path.join(application_path, 'pandoc', 'pandoc.exe')
    os.environ['PANDOC_PATH'] = pandoc_path
else:
    # 如果是开发环境
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(current_dir, 'src')
    sys.path.insert(0, src_path)

# 修复网络检查问题 - 创建一个简单的版本检查函数
def simple_check_expiration():
    """简单的过期检查，避免网络问题"""
    from datetime import datetime, timezone, timedelta
    
    # 北京时间时区 (UTC+8)
    BEIJING_TZ = timezone(timedelta(hours=8))
    
    # 过期时间常量 (北京时间)
    EXPIRATION_DATE = datetime(2025, 12, 5, 0, 0, 0, tzinfo=BEIJING_TZ)
    
    # 使用本地时间检查
    local_time = datetime.now(BEIJING_TZ)
    
    print(f"Current Time (Beijing): {local_time}")
    print(f"Expiration Time (Beijing): {EXPIRATION_DATE}")
    
    return local_time < EXPIRATION_DATE

try:
    # 尝试导入PyQt5
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QIcon
    print("PyQt5 import successful")
    
    # 尝试直接导入模块，不使用包结构
    import importlib.util
    
    # 加载main_window.py
    main_window_path = os.path.join(os.path.dirname(__file__), 'src', 'ui', 'main_window.py')
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        main_window_path = os.path.join(sys._MEIPASS, 'src', 'ui', 'main_window.py')
    
    print(f"Loading main_window from: {main_window_path}")
    
    spec = importlib.util.spec_from_file_location("main_window", main_window_path)
    main_window_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_window_module)
    
    PandocGUI = main_window_module.PandocGUI
    print("PandocGUI class loaded successfully")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    print("QApplication created")
    
    # 执行简单的过期检查（避免网络问题）
    if not simple_check_expiration():
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(None, "版本过期", "当前版本已过期，请联系开发者获取最新版。")
        sys.exit(1)
    
    # 创建主窗口
    window = PandocGUI()
    print("PandocGUI window created")
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())
    
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"sys.path: {sys.path}")
    
    try:
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Import Error", f"Failed to import required modules:\n{e}\n\nPlease ensure all dependencies are installed.")
    except:
        pass
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    
    try:
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Error", f"An error occurred:\n{e}")
    except:
        pass
    sys.exit(1)