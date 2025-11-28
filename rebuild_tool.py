#!/usr/bin/env python3
"""
Pandoc GUI 应用程序打包工具（已弃用）
这个文件仅作为参考，实际打包请使用 rebuild_app.bat
"""

import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                            QWidget, QLabel, QMessageBox)

class RebuildTool(QMainWindow):
    """重新打包工具主窗口（已弃用）"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pandoc-GUI 打包工具（已弃用）")
        self.setGeometry(100, 100, 500, 200)
        
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 标题
        title_label = QLabel("此工具已弃用")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 说明
        info_text = """此打包工具已被弃用，请使用 rebuild_app.bat 进行打包。

rebuild_app.bat 使用 Pandoc-GUI.spec 配置文件，包含了所有必要的依赖和资源文件。

运行方法：
1. 确保 pandoc.exe 在 pandoc 文件夹中
2. 运行 rebuild_app.bat
3. 打包后的 exe 文件将位于 dist 文件夹中"""
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 按钮
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        self.close_button.setMinimumHeight(40)
        layout.addWidget(self.close_button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RebuildTool()
    window.show()
    sys.exit(app.exec_())