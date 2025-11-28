"""
主窗口
包含应用程序的主界面和主要功能
"""

import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QComboBox, QMessageBox,
    QApplication
)
from PyQt5.QtCore import Qt

# 添加当前目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入自定义组件
from ui.format_config import FormatConfigDialog
from ui.about_dialog import AboutDialog

# 导入核心模块
from core.pandoc_converter import PandocConverter

# 导入工具模块
from utils.file_utils import (
    get_file_path, get_file_name, generate_output_path, get_project_root_dir
)

# 导入版本检查模块
from core.version_checker import get_expiration_message, get_test_version_message


class PandocGUI(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pandoc GUI')
        self.setGeometry(100, 100, 800, 600)
        
        # 获取项目根目录 - 需要向上两级目录（从 src/ui/ 到项目根目录）
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 获取正确的pandoc路径
        if getattr(sys, 'frozen', False):
            # 在打包后的exe中
            if hasattr(sys, '_MEIPASS'):
                # 在单文件exe中，使用临时目录
                self.pandoc_path = os.path.join(sys._MEIPASS, 'pandoc', 'pandoc.exe')
            else:
                # 在多文件exe中，使用exe所在目录
                self.pandoc_path = os.path.join(os.path.dirname(sys.executable), 'pandoc', 'pandoc.exe')
        else:
            # 在开发环境中，使用项目根目录
            self.pandoc_path = os.path.join(self.root_dir, 'pandoc', 'pandoc.exe')
            
        # 确保路径存在，如果不存在则尝试其他可能的路径
        if not os.path.exists(self.pandoc_path):
            print(f"Warning: Pandoc not found at {self.pandoc_path}")
            # 尝试从当前exe目录获取
            if getattr(sys, 'frozen', False):
                exe_dir = os.path.dirname(sys.executable)
                alt_path = os.path.join(exe_dir, 'pandoc', 'pandoc.exe')
                if os.path.exists(alt_path):
                    self.pandoc_path = alt_path
                    print(f"Found Pandoc at alternative path: {self.pandoc_path}")
                else:
                    print(f"Error: Pandoc not found at {alt_path} either")
        
        # 初始化转换器
        self.converter = PandocConverter(self.pandoc_path)
        
        # 支持的文件格式
        self.supported_formats = [
            'markdown', 'docx', 'pdf', 'html', 'epub', 'odt', 
            'txt', 'rst', 'json', 'latex', 'xml', 'pptx'
        ]
        
        self.input_file = None
        self.template_file = None
        
        self.init_ui()
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具')
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        # 关于与鸣谢
        about_action = help_menu.addAction('关于与鸣谢')
        about_action.triggered.connect(self.show_about_dialog)
            
    def init_ui(self):
        """初始化UI"""
        # 创建菜单栏
        self.create_menu_bar()
        
        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        
        # 文件选择部分
        file_layout = QVBoxLayout()
        
        # 输入文件选择
        input_layout = QHBoxLayout()
        self.input_label = QLabel('未选择文件')
        self.input_label.setFixedWidth(300)
        input_button = QPushButton('选择输入文件')
        input_button.clicked.connect(self.select_input_file)
        
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(input_button)
        file_layout.addLayout(input_layout)
        
        # 模板文件选择
        template_layout = QHBoxLayout()
        self.template_label = QLabel('未选择模板文件')
        self.template_label.setFixedWidth(300)
        template_button = QPushButton('选择docx模板文件(可选)')
        template_button.clicked.connect(self.select_template_file)
        
        template_layout.addWidget(self.template_label)
        template_layout.addWidget(template_button)
        file_layout.addLayout(template_layout)
        
        # 格式选择部分
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel('输出格式：'))
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(self.supported_formats)
        self.format_combo.setCurrentText('docx')
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # 转换按钮
        self.convert_button = QPushButton('转换文件')
        self.convert_button.clicked.connect(self.convert_file)
        self.convert_button.setFixedHeight(40)
        self.convert_button.setEnabled(False)
        
        # 创建模板文件按钮
        self.create_template_button = QPushButton('创建模板文件')
        self.create_template_button.clicked.connect(self.open_format_config_dialog)
        self.create_template_button.setFixedHeight(40)
        
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.create_template_button)
        
        # 状态显示
        self.status_label = QLabel('就绪')
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # 过期提示标签
        self.expiration_label = QLabel()
        self.expiration_label.setAlignment(Qt.AlignCenter)
        self.expiration_label.setStyleSheet("color: #d9534f; font-weight: bold;")
        self.expiration_label.setText(get_expiration_message())
        
        # 测试版本提示标签
        self.test_version_label = QLabel()
        self.test_version_label.setAlignment(Qt.AlignCenter)
        self.test_version_label.setStyleSheet("color: black; font-style: italic; padding: 5px;")
        self.test_version_label.setWordWrap(True)
        self.test_version_label.setText(get_test_version_message())
        
        # 添加所有布局到主布局
        main_layout.addLayout(file_layout)
        main_layout.addLayout(format_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.expiration_label)
        main_layout.addWidget(self.test_version_label)
        main_layout.addStretch()
        
        # 版权声明
        copyright_label = QLabel('Copyright © 2024 BrucePeng')
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: #666666; font-size: 15px; margin: 5px;")
        main_layout.addWidget(copyright_label)
    
    def select_input_file(self):
        """选择输入文件"""
        file_path = get_file_path(self, '选择输入文件', '所有文件 (*.*)')
        if file_path:
            self.input_file = file_path
            self.input_label.setText(get_file_name(file_path))
            self.convert_button.setEnabled(True)
            self.status_label.setText(f'已选择输入文件：{get_file_name(file_path)}')
    
    def select_template_file(self):
        """选择模板文件"""
        file_path = get_file_path(self, '选择模板文件', 'Word文档 (*.docx)')
        if file_path:
            self.template_file = file_path
            self.template_label.setText(get_file_name(file_path))
            self.status_label.setText(f'已选择模板文件：{get_file_name(file_path)}')
    
    def convert_file(self):
        """转换文件"""
        if not self.input_file:
            QMessageBox.warning(self, '警告', '请先选择输入文件')
            return
        
        output_format = self.format_combo.currentText()
        
        # 生成输出文件名
        output_file = generate_output_path(self.input_file, output_format)
        
        try:
            self.status_label.setText('正在转换...')
            QApplication.processEvents()
            
            # 执行转换
            success, message = self.converter.convert_file(
                self.input_file, output_file, self.template_file
            )
            
            if success:
                self.status_label.setText(message)
                QMessageBox.information(self, '成功', message)
            else:
                self.status_label.setText('转换失败')
                QMessageBox.critical(self, '错误', message)
                
        except Exception as e:
            self.status_label.setText('转换失败')
            QMessageBox.critical(self, '错误', f'发生错误：\n{str(e)}')
    
    def open_format_config_dialog(self):
        """打开排版配置对话框"""
        dialog = FormatConfigDialog(self)
        dialog.exec_()
    
    def show_about_dialog(self):
        """显示关于与鸣谢对话框"""
        dialog = AboutDialog(self)
        dialog.exec_()