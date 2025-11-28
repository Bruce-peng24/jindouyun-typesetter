"""
排版配置对话框
包含所有排版配置相关的UI和逻辑
"""

import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QComboBox, QMessageBox, 
    QDialog, QTabWidget, QGroupBox, QGridLayout, QLineEdit,
    QSpinBox, QFontComboBox, QCheckBox, QColorDialog, QFormLayout,
    QTextEdit, QSplitter, QListWidget, QStackedWidget, QButtonGroup,
    QRadioButton, QScrollArea, QMenuBar, QMenu, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

# 添加当前目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入自定义组件
from ui.widgets.basic_text_widget import BasicTextWidget
from ui.widgets.heading_widget import HeadingWidget
from ui.widgets.list_widget import ListWidget
from ui.widgets.reference_widget import ReferenceWidget
from ui.widgets.layout_widget import LayoutWidget
from ui.widgets.page_widget import PageWidget

# 导入核心模块
from core.config_manager import ConfigManager
from core.template_manager import TemplateManager

# 导入工具模块
from utils.file_utils import get_save_file_path


class FormatConfigDialog(QDialog):
    """排版配置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("排版配置")
        self.setMinimumSize(800, 600)
        self.config = {}
        
        # 初始化管理器
        self.config_manager = ConfigManager()
        self.template_manager = TemplateManager()
        
        # 初始化组件
        self.widgets = {}
        
        self.init_ui()
        self.load_default_config()
        
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout(self)  # 改为垂直布局，以便将预设模板区域放在顶部
        
        # 预设模板区域 - 移到顶部
        template_container = QWidget()
        template_layout = QVBoxLayout(template_container)
        
        # 预设模板标题和选择区域
        template_select_layout = QHBoxLayout()
        template_select_layout.addWidget(QLabel("预设模板："))
        
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "默认模板", "学术论文模板", "报告模板", "小说模板", "简历模板", "信函模板"
        ])
        self.template_combo.setCurrentText("默认模板")
        self.template_combo.currentTextChanged.connect(self.load_template_preview)
        template_select_layout.addWidget(self.template_combo)
        
        apply_template_button = QPushButton("应用模板")
        apply_template_button.clicked.connect(self.apply_preset_template)
        template_select_layout.addWidget(apply_template_button)
        
        # 导出模板按钮也放在这里
        export_template_button = QPushButton("导出模板")
        export_template_button.clicked.connect(self.export_template)
        template_select_layout.addWidget(export_template_button)
        
        template_layout.addLayout(template_select_layout)
        
        # 模板预览文本
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(120)
        self.preview_text.setPlainText("默认模板预览")
        template_layout.addWidget(self.preview_text)
        
        # 添加模板容器到主布局
        main_layout.addWidget(template_container)
        
        # 创建导航列表和配置区域的水平布局
        nav_config_layout = QHBoxLayout()
        
        # 创建导航列表和配置区域的分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 创建导航列表
        self.nav_list = QListWidget()
        self.nav_list.setMaximumWidth(200)
        
        # 添加导航项
        nav_items = [
            "基础文本与段落样式",
            "标题与层级样式", 
            "列表样式",
            "引用与交互元素样式",
            "非文本与布局样式块",
            "页面设置"
        ]
        
        for item in nav_items:
            self.nav_list.addItem(item)
        
        # 连接导航点击事件
        self.nav_list.currentRowChanged.connect(self.show_config_section)
        
        # 创建配置区域
        self.config_stack = QStackedWidget()
        
        # 创建各配置区域
        self.widgets['basic_text'] = BasicTextWidget()
        self.widgets['heading'] = HeadingWidget()
        self.widgets['list'] = ListWidget()
        self.widgets['reference'] = ReferenceWidget()
        self.widgets['layout'] = LayoutWidget()
        self.widgets['page'] = PageWidget()
        
        # 设置颜色选择回调
        self.widgets['reference'].set_color_chooser_callback(self.choose_color)
        self.widgets['layout'].set_color_chooser_callback(self.choose_color)
        
        # 添加配置区域到堆栈
        self.config_stack.addWidget(self.widgets['basic_text'])
        self.config_stack.addWidget(self.widgets['heading'])
        self.config_stack.addWidget(self.widgets['list'])
        self.config_stack.addWidget(self.widgets['reference'])
        self.config_stack.addWidget(self.widgets['layout'])
        self.config_stack.addWidget(self.widgets['page'])
        
        # 设置默认选中第一项
        self.nav_list.setCurrentRow(0)
        
        # 添加到分割器
        splitter.addWidget(self.nav_list)
        splitter.addWidget(self.config_stack)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        # 添加分割器到导航配置布局
        nav_config_layout.addWidget(splitter)
        
        # 添加导航配置布局到主布局
        main_layout.addLayout(nav_config_layout)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        
        # 添加按钮布局到主布局
        main_layout.addLayout(button_layout)
    
    def show_config_section(self, index):
        """根据选择的导航项显示对应的配置区域"""
        self.config_stack.setCurrentIndex(index)
    
    def choose_color(self, button):
        """选择颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()}")
            button.setProperty("color", color.name())
    
    def load_template_preview(self, template_name):
        """加载模板预览"""
        preview_text = self.template_manager.get_template_preview(template_name)
        self.preview_text.setPlainText(preview_text)
    
    def apply_preset_template(self):
        """应用预设模板"""
        template_name = self.template_combo.currentText()
        self.template_manager.apply_template(template_name, self.widgets)
    
    def load_default_config(self):
        """加载默认配置"""
        self.template_manager.load_default_config(self.widgets)
        
        # 加载默认模板预览
        self.load_template_preview("默认模板")
    
    def export_template(self):
        """导出模板文件"""
        # 先收集当前配置
        self.config = self.config_manager.collect_config(self.widgets)
        
        # 创建模板文档
        doc = self.config_manager.create_template_file()
        
        # 选择保存位置
        file_path = get_save_file_path(
            self, '保存模板文件', 'Word文档 (*.docx)', '.docx'
        )
        
        if file_path:
            try:
                doc.save(file_path)
                QMessageBox.information(self, '成功', f'模板文件已保存到：{file_path}')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'保存模板文件失败：\n{str(e)}')