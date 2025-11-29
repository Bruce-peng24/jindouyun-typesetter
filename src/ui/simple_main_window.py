"""
简化的主窗口类
实现三步操作界面：HTML输入 -> 排版方案选择 -> 导出文档
"""

import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QComboBox, QTextEdit, QMessageBox, 
    QApplication, QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QTextOption

# 添加当前目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入核心模块
from core.enhanced_pandoc_converter import EnhancedPandocConverter

# 导入版本检查模块
from core.version_checker import get_expiration_message, get_test_version_message


class SimpleMainWindow(QMainWindow):
    """简化的主窗口类 - 三步操作界面"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('金斗云排版工具 - 简化版')
        self.setGeometry(100, 100, 900, 700)
        
        # 获取项目根目录
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 获取pandoc路径
        self._init_pandoc_path()
        
        # 初始化转换器
        self.converter = EnhancedPandocConverter(self.pandoc_path)
        
        # 预设排版方案
        self.layout_templates = {
            'academic': {
                'name': '学术论文风格',
                'description': '适合论文、学术报告，包含标准的标题层级和引用格式',
                'template': None  # 可以后续添加具体模板
            },
            'business': {
                'name': '商务报告风格', 
                'description': '企业报告、方案文档，专业简洁的商务风格',
                'template': None
            },
            'technical': {
                'name': '技术文档风格',
                'description': 'API文档、技术手册，适合技术内容展示',
                'template': None
            },
            'simple': {
                'name': '简洁通用风格',
                'description': '日常办公文档，清晰简洁的通用格式',
                'template': None
            }
        }
        
        self.selected_template = 'simple'  # 默认选择
        self.html_content = ''
        
        self.init_ui()
        
    def _init_pandoc_path(self):
        """初始化pandoc路径"""
        if getattr(sys, 'frozen', False):
            # 在打包后的exe中
            if hasattr(sys, '_MEIPASS'):
                self.pandoc_path = os.path.join(sys._MEIPASS, 'pandoc', 'pandoc.exe')
            else:
                self.pandoc_path = os.path.join(os.path.dirname(sys.executable), 'pandoc', 'pandoc.exe')
        else:
            # 在开发环境中
            self.pandoc_path = os.path.join(self.root_dir, 'pandoc', 'pandoc.exe')
            
        # 检查路径是否存在
        if not os.path.exists(self.pandoc_path):
            print(f"Warning: Pandoc not found at {self.pandoc_path}")
            
    def init_ui(self):
        """初始化UI界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局（垂直）
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # 创建三个主要区域
        self._create_header_area(main_layout)
        self._create_main_content_area(main_layout)
        self._create_bottom_area(main_layout)
        
        # 设置样式
        self._set_styles()
        
        # 设置默认选择（在所有UI组件创建后）
        self.template_combo.setCurrentIndex(0)  # 默认选择第一个选项（简洁通用）
        
    def _create_header_area(self, parent_layout):
        """创建顶部标题区域"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        
        # 主标题
        title_label = QLabel('金斗云排版工具')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        
        # 副标题说明
        subtitle_label = QLabel('三步完成专业文档排版：粘贴HTML → 选择样式 → 导出Word')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 5px;
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_frame)
        
    def _create_main_content_area(self, parent_layout):
        """创建中部核心操作区域"""
        # 主内容框架
        content_frame = QFrame()
        content_frame.setFrameStyle(QFrame.Box)
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        
        # 步骤1：HTML输入区域
        self._create_html_input_area(content_layout)
        
        # 步骤2：排版方案选择区域
        self._create_template_selection_area(content_layout)
        
        parent_layout.addWidget(content_frame)
        
    def _create_html_input_area(self, parent_layout):
        """创建HTML输入区域"""
        # 步骤标题
        step_title = QLabel('步骤 1：粘贴HTML内容')
        step_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #495057;
            margin-bottom: 10px;
        """)
        
        # 文本输入框
        self.html_input = QTextEdit()
        self.html_input.setPlaceholderText('请在此处粘贴HTML内容...\n\n支持的内容格式：\n• HTML格式的文章、报告内容\n• 包含标题、段落、列表、表格等标准HTML标签\n• AI生成的HTML文档内容')
        self.html_input.setMinimumHeight(200)
        self.html_input.setMaximumHeight(250)
        
        # 设置文本框样式
        self.html_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                background-color: #fafafa;
            }
            QTextEdit:focus {
                border-color: #007bff;
                background-color: white;
            }
        """)
        
        parent_layout.addWidget(step_title)
        parent_layout.addWidget(self.html_input)
        
    def _create_template_selection_area(self, parent_layout):
        """创建排版方案选择区域"""
        # 步骤标题
        step_title = QLabel('步骤 2：选择文档样式')
        step_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #495057;
            margin-bottom: 15px;
        """)
        
        # 下拉菜单容器
        template_container = QWidget()
        template_layout = QVBoxLayout(template_container)
        template_layout.setSpacing(12)
        
        # 创建下拉菜单
        self.template_combo = QComboBox()
        self.template_combo.setMinimumHeight(40)
        
        # 设置下拉菜单样式
        self.template_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #007bff;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                selection-background-color: #007bff;
                selection-color: white;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item {
                height: 35px;
                padding: 8px 12px;
                font-size: 14px;
            }
        """)
        
        # 添加选项到下拉菜单
        self.template_combo.addItem('简洁通用：日常办公文档', 'simple')
        self.template_combo.addItem('学术论文：适合论文、报告格式', 'academic')
        self.template_combo.addItem('商务文档：企业报告、方案文档', 'business')
        self.template_combo.addItem('技术文档：API文档、技术手册', 'technical')
        
        # 创建描述标签
        self.template_desc_label = QLabel(self.layout_templates['simple']['description'])
        self.template_desc_label.setStyleSheet("""
            font-size: 12px;
            color: #6c757d;
            margin-top: 8px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
            border-left: 3px solid #007bff;
        """)
        self.template_desc_label.setWordWrap(True)
        self.template_desc_label.setMinimumHeight(50)
        
        # 连接信号
        self.template_combo.currentIndexChanged.connect(self._on_template_selected)
        
        # 添加到布局
        template_layout.addWidget(self.template_combo)
        template_layout.addWidget(self.template_desc_label)
        
        parent_layout.addWidget(step_title)
        parent_layout.addWidget(template_container)
        
    def _create_bottom_area(self, parent_layout):
        """创建底部操作和状态区域"""
        bottom_frame = QFrame()
        bottom_frame.setFrameStyle(QFrame.Box)
        bottom_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setSpacing(15)
        
        # 操作按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # 生成Word文档按钮
        self.generate_button = QPushButton('生成Word文档')
        self.generate_button.setMinimumHeight(45)
        self.generate_button.clicked.connect(self._generate_document)
        
        # 清空内容按钮
        self.clear_button = QPushButton('清空内容')
        self.clear_button.setMinimumHeight(45)
        self.clear_button.clicked.connect(self._clear_content)
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        # 状态显示区域
        status_container = QWidget()
        status_layout = QVBoxLayout(status_container)
        status_layout.setSpacing(8)
        
        # 状态标签
        self.status_label = QLabel('状态：等待用户输入...')
        self.status_label.setStyleSheet("""
            font-size: 14px;
            color: #495057;
            font-weight: bold;
        """)
        
        # 文件保存位置说明
        save_location = QLabel('文档将保存到：桌面/AI文档_时间戳.docx')
        save_location.setStyleSheet("""
            font-size: 12px;
            color: #6c757d;
        """)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(save_location)
        
        # 版本信息标签
        self.expiration_label = QLabel()
        self.expiration_label.setAlignment(Qt.AlignCenter)
        self.expiration_label.setStyleSheet("color: #d9534f; font-weight: bold;")
        self.expiration_label.setText(get_expiration_message())
        
        self.test_version_label = QLabel()
        self.test_version_label.setAlignment(Qt.AlignCenter)
        self.test_version_label.setStyleSheet("color: black; font-style: italic; padding: 5px;")
        self.test_version_label.setWordWrap(True)
        self.test_version_label.setText(get_test_version_message())
        
        # 添加所有组件到底部布局
        bottom_layout.addLayout(button_layout)
        bottom_layout.addWidget(status_container)
        bottom_layout.addWidget(self.expiration_label)
        bottom_layout.addWidget(self.test_version_label)
        
        parent_layout.addWidget(bottom_frame)
        
    def _set_styles(self):
        """设置整体样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QPushButton#clearButton {
                background-color: #6c757d;
            }
            QPushButton#clearButton:hover {
                background-color: #545b62;
            }
        """)
        
        # 设置清空按钮的样式
        self.clear_button.setObjectName("clearButton")
        
    def _on_template_selected(self, index):
        """处理模板选择事件"""
        if index >= 0:
            template_key = self.template_combo.itemData(index)
            if template_key and template_key in self.layout_templates:
                self.selected_template = template_key
                template_name = self.layout_templates[template_key]['name']
                template_desc = self.layout_templates[template_key]['description']
                
                # 更新状态标签
                self.status_label.setText(f"状态：已选择{template_name}")
                
                # 更新描述标签
                self.template_desc_label.setText(template_desc)
                
    def _generate_document(self):
        """生成Word文档"""
        # 获取HTML内容
        html_content = self.html_input.toPlainText().strip()
        
        if not html_content:
            QMessageBox.warning(self, '提示', '请先输入HTML内容')
            return
            
        try:
            self.status_label.setText('状态：正在生成文档...')
            QApplication.processEvents()
            
            # 生成输出文件名
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            if not os.path.exists(desktop_path):
                desktop_path = os.path.expanduser('~')  # 如果桌面不存在，使用用户目录
                
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'AI文档_{timestamp}.docx'
            output_path = os.path.join(desktop_path, output_filename)
            
            # 使用增强转换器直接转换HTML内容
            success, message = self.converter.convert_html_to_docx(
                html_content, output_path, self.selected_template
            )
            
            if success:
                self.status_label.setText(f'状态：文档生成成功 - {output_filename}')
                QMessageBox.information(
                    self, 
                    '成功', 
                    f'文档已成功生成！\n\n保存位置：{output_path}\n\n文件名：{output_filename}\n\n使用样式：{self.layout_templates[self.selected_template]["name"]}'
                )
            else:
                self.status_label.setText('状态：文档生成失败')
                QMessageBox.critical(self, '错误', f'文档生成失败：\n{message}')
                
        except Exception as e:
            self.status_label.setText('状态：文档生成失败')
            QMessageBox.critical(self, '错误', f'发生错误：\n{str(e)}')
            
    def _clear_content(self):
        """清空内容"""
        self.html_input.clear()
        self.status_label.setText('状态：等待用户输入...')
        
        # 重置为默认选择
        self.template_combo.setCurrentIndex(0)  # 重置为第一个选项（简洁通用）