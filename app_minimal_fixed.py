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

# 导入版本检查模块
from core.version_checker import check_expiration
print("Version checker module loaded successfully")

try:
    # 尝试导入PyQt5
    from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QIcon, QPixmap
    print("PyQt5 import successful")
    
    # 尝试直接导入模块，不使用包结构
    import importlib.util
    
    # 加载simple_main_window.py
    main_window_path = os.path.join(os.path.dirname(__file__), 'src', 'ui', 'simple_main_window.py')
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        main_window_path = os.path.join(sys._MEIPASS, 'src', 'ui', 'simple_main_window.py')
    
    print(f"Loading simple_main_window from: {main_window_path}")
    
    spec = importlib.util.spec_from_file_location("simple_main_window", main_window_path)
    main_window_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_window_module)
    
    SimpleMainWindow = main_window_module.SimpleMainWindow
    print("SimpleMainWindow class loaded successfully")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    print("QApplication created")
    
    # 创建启动画面 - 使用QSplashScreen
    # 获取图片路径
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            splash_image_path = os.path.join(sys._MEIPASS, 'resource', 'loading.png')
        else:
            splash_image_path = os.path.join(application_path, 'resource', 'loading.png')
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        splash_image_path = os.path.join(current_dir, 'resource', 'loading.png')
    
    # 创建并显示启动画面
    try:
        splash = QSplashScreen(QPixmap(splash_image_path))
        splash.show()
        print("Splash screen created and shown")
    except Exception as e:
        print(f"无法加载启动画面: {e}")
        splash = None
    
    # 执行版本检查（使用网络时间）
    if not check_expiration():
        sys.exit(1)
    
    # 定义显示主窗口的函数
    def show_main_window():
        # 创建主窗口
        window = SimpleMainWindow()
        print("SimpleMainWindow window created")
        window.show()
        
        # 关闭启动画面
        if splash:
            splash.finish(window)
    
    # 设置2秒后显示主窗口并关闭启动画面
    QTimer.singleShot(2000, show_main_window)
    
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