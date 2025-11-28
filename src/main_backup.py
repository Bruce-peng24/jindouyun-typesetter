import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QComboBox, QMessageBox, 
    QDialog, QTabWidget, QGroupBox, QGridLayout, QLineEdit,
    QSpinBox, QFontComboBox, QCheckBox, QColorDialog, QFormLayout,
    QTextEdit, QSplitter, QListWidget, QStackedWidget, QButtonGroup,
    QRadioButton, QScrollArea, QMenuBar, QMenu, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn


class FormatConfigDialog(QDialog):
    """排版配置对话框"""
    config_saved = pyqtSignal(dict)  # 配置保存信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("排版配置")
        self.setMinimumSize(800, 600)
        self.config = {}
        
        self.init_ui()
        self.load_default_config()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 添加各配置标签页
        self.font_tab = self.create_font_tab()
        self.paragraph_tab = self.create_paragraph_tab()
        self.page_tab = self.create_page_tab()
        self.style_tab = self.create_style_tab()
        self.template_tab = self.create_template_tab()
        
        self.tab_widget.addTab(self.font_tab, "字体设置")
        self.tab_widget.addTab(self.paragraph_tab, "段落设置")
        self.tab_widget.addTab(self.page_tab, "页面设置")
        self.tab_widget.addTab(self.style_tab, "样式配置")
        self.tab_widget.addTab(self.template_tab, "配置模板")
        
        # 按钮区域
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存配置")
        save_button.clicked.connect(self.save_config)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(button_layout)
    
    def create_font_tab(self):
        """创建字体设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 字体设置分组
        font_group = QGroupBox("默认字体设置")
        font_layout = QFormLayout()
        
        # 中文字体
        self.chinese_font_combo = QFontComboBox()
        self.chinese_font_combo.setFontFilters(QFontComboBox.SimplifiedChineseFonts)
        font_layout.addRow("中文字体:", self.chinese_font_combo)
        
        # 英文字体
        self.english_font_combo = QFontComboBox()
        self.english_font_combo.setFontFilters(QFontComboBox.LatinFonts)
        font_layout.addRow("英文字体:", self.english_font_combo)
        
        # 字体大小
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(12)
        font_layout.addRow("字体大小:", self.font_size_spin)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # 特殊元素字体设置
        special_group = QGroupBox("特殊元素字体")
        special_layout = QFormLayout()
        
        self.title_font_size_spin = QSpinBox()
        self.title_font_size_spin.setRange(10, 72)
        self.title_font_size_spin.setValue(16)
        special_layout.addRow("标题字体大小:", self.title_font_size_spin)
        
        self.body_font_size_spin = QSpinBox()
        self.body_font_size_spin.setRange(8, 48)
        self.body_font_size_spin.setValue(12)
        special_layout.addRow("正文字体大小:", self.body_font_size_spin)
        
        self.footnote_font_size_spin = QSpinBox()
        self.footnote_font_size_spin.setRange(6, 24)
        self.footnote_font_size_spin.setValue(9)
        special_layout.addRow("脚注字体大小:", self.footnote_font_size_spin)
        
        special_group.setLayout(special_layout)
        layout.addWidget(special_group)
        
        layout.addStretch()
        return tab
    
    def create_paragraph_tab(self):
        """创建段落设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 段落缩进和间距
        indent_group = QGroupBox("缩进和间距")
        indent_layout = QFormLayout()
        
        self.first_line_indent_spin = QDoubleSpinBox()
        self.first_line_indent_spin.setRange(0, 10)
        self.first_line_indent_spin.setValue(2)
        self.first_line_indent_spin.setSuffix(" 字符")
        indent_layout.addRow("首行缩进:", self.first_line_indent_spin)
        
        self.line_spacing_combo = QComboBox()
        self.line_spacing_combo.addItems(["1.0", "1.15", "1.5", "2.0"])
        self.line_spacing_combo.setCurrentText("1.5")
        indent_layout.addRow("行间距:", self.line_spacing_combo)
        
        self.paragraph_spacing_spin = QDoubleSpinBox()
        self.paragraph_spacing_spin.setRange(0, 48)
        self.paragraph_spacing_spin.setValue(6)
        self.paragraph_spacing_spin.setSuffix(" 磅")
        indent_layout.addRow("段前间距:", self.paragraph_spacing_spin)
        
        indent_group.setLayout(indent_layout)
        layout.addWidget(indent_group)
        
        # 对齐方式
        align_group = QGroupBox("对齐方式")
        align_layout = QVBoxLayout()
        
        self.align_group = QButtonGroup()
        self.left_radio = QRadioButton("左对齐")
        self.center_radio = QRadioButton("居中对齐")
        self.right_radio = QRadioButton("右对齐")
        self.justify_radio = QRadioButton("两端对齐")
        self.justify_radio.setChecked(True)
        
        self.align_group.addButton(self.left_radio, 0)
        self.align_group.addButton(self.center_radio, 1)
        self.align_group.addButton(self.right_radio, 2)
        self.align_group.addButton(self.justify_radio, 3)
        
        align_layout.addWidget(self.left_radio)
        align_layout.addWidget(self.center_radio)
        align_layout.addWidget(self.right_radio)
        align_layout.addWidget(self.justify_radio)
        
        align_group.setLayout(align_layout)
        layout.addWidget(align_group)
        
        layout.addStretch()
        return tab
    
    def create_page_tab(self):
        """创建页面设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 页面尺寸
        size_group = QGroupBox("页面尺寸")
        size_layout = QFormLayout()
        
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "A3", "A5", "B4", "B5", "Letter", "Legal"])
        self.page_size_combo.setCurrentText("A4")
        size_layout.addRow("纸张大小:", self.page_size_combo)
        
        self.orientation_group = QButtonGroup()
        self.portrait_radio = QRadioButton("纵向")
        self.landscape_radio = QRadioButton("横向")
        self.portrait_radio.setChecked(True)
        
        self.orientation_group.addButton(self.portrait_radio, 0)
        self.orientation_group.addButton(self.landscape_radio, 1)
        
        orientation_layout = QHBoxLayout()
        orientation_layout.addWidget(self.portrait_radio)
        orientation_layout.addWidget(self.landscape_radio)
        size_layout.addRow("页面方向:", orientation_layout)
        
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        # 页边距
        margin_group = QGroupBox("页边距")
        margin_layout = QFormLayout()
        
        self.margin_top_spin = QDoubleSpinBox()
        self.margin_top_spin.setRange(0, 10)
        self.margin_top_spin.setValue(2.54)
        self.margin_top_spin.setSuffix(" 厘米")
        margin_layout.addRow("上边距:", self.margin_top_spin)
        
        self.margin_bottom_spin = QDoubleSpinBox()
        self.margin_bottom_spin.setRange(0, 10)
        self.margin_bottom_spin.setValue(2.54)
        self.margin_bottom_spin.setSuffix(" 厘米")
        margin_layout.addRow("下边距:", self.margin_bottom_spin)
        
        self.margin_left_spin = QDoubleSpinBox()
        self.margin_left_spin.setRange(0, 10)
        self.margin_left_spin.setValue(3.17)
        self.margin_left_spin.setSuffix(" 厘米")
        margin_layout.addRow("左边距:", self.margin_left_spin)
        
        self.margin_right_spin = QDoubleSpinBox()
        self.margin_right_spin.setRange(0, 10)
        self.margin_right_spin.setValue(3.17)
        self.margin_right_spin.setSuffix(" 厘米")
        margin_layout.addRow("右边距:", self.margin_right_spin)
        
        margin_group.setLayout(margin_layout)
        layout.addWidget(margin_group)
        
        layout.addStretch()
        return tab
    
    def create_style_tab(self):
        """创建样式配置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # 样式列表
        styles_list = [
            "标题1", "标题2", "标题3", "标题4", "标题5", "标题6", "标题7", "标题8", "标题9",
            "段落", "正文", "正文字符（包含中文、英文、数字的字体）", "超链接", "脚注", "脚注引用文本",
            "有序列表", "无序列表", "水平线", "块文本", "表标题", "表格", "图片说明"
        ]
        
        self.style_configs = {}
        
        for style_name in styles_list:
            group = QGroupBox(style_name)
            group_layout = QFormLayout()
            
            # 字体选择
            font_combo = QFontComboBox()
            group_layout.addRow("字体:", font_combo)
            
            # 字体大小
            size_spin = QSpinBox()
            size_spin.setRange(6, 72)
            group_layout.addRow("字体大小:", size_spin)
            
            # 粗体
            bold_check = QCheckBox("粗体")
            group_layout.addRow("", bold_check)
            
            # 斜体
            italic_check = QCheckBox("斜体")
            group_layout.addRow("", italic_check)
            
            # 下划线
            underline_check = QCheckBox("下划线")
            group_layout.addRow("", underline_check)
            
            # 保存控件引用
            self.style_configs[style_name] = {
                'font': font_combo,
                'size': size_spin,
                'bold': bold_check,
                'italic': italic_check,
                'underline': underline_check
            }
            
            group.setLayout(group_layout)
            scroll_layout.addWidget(group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        return tab
    
    def create_template_tab(self):
        """创建配置模板标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 预设模板
        preset_group = QGroupBox("预设模板")
        preset_layout = QVBoxLayout()
        
        self.template_list = QListWidget()
        self.template_list.addItems([
            "学术论文模板", "报告模板", "小说模板", "简历模板", "信函模板", "默认模板"
        ])
        preset_layout.addWidget(self.template_list)
        
        load_template_button = QPushButton("加载模板")
        load_template_button.clicked.connect(self.load_preset_template)
        preset_layout.addWidget(load_template_button)
        
        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)
        
        # 模板预览
        preview_group = QGroupBox("模板预览")
        preview_layout = QVBoxLayout()
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(200)
        preview_layout.addWidget(self.preview_text)
        
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        layout.addStretch()
        return tab
    
    def load_default_config(self):
        """加载默认配置"""
        # 字体设置默认值
        self.chinese_font_combo.setCurrentFont(QFont("宋体"))
        self.english_font_combo.setCurrentFont(QFont("Times New Roman"))
        
        # 样式设置默认值
        style_defaults = {
            "标题1": {'size': 16, 'bold': True},
            "标题2": {'size': 14, 'bold': True},
            "标题3": {'size': 13, 'bold': True},
            "正文": {'size': 12},
            "脚注": {'size': 9},
            "表标题": {'size': 12, 'bold': True},
            "图片说明": {'size': 10, 'italic': True}
        }
        
        for style_name, defaults in style_defaults.items():
            if style_name in self.style_configs:
                if 'size' in defaults:
                    self.style_configs[style_name]['size'].setValue(defaults['size'])
                if 'bold' in defaults:
                    self.style_configs[style_name]['bold'].setChecked(defaults['bold'])
                if 'italic' in defaults:
                    self.style_configs[style_name]['italic'].setChecked(defaults['italic'])
        
        # 加载默认模板预览
        self.load_template_preview("默认模板")
    
    def load_preset_template(self):
        """加载预设模板"""
        selected = self.template_list.currentItem()
        if selected:
            template_name = selected.text()
            self.load_template_preview(template_name)
            self.apply_template_settings(template_name)
    
    def load_template_preview(self, template_name):
        """加载模板预览"""
        templates = {
            "学术论文模板": """
学术论文模板预览:
- 标题格式: 居中，加粗，16pt
- 作者信息: 居中，12pt
- 摘要: 段落首行缩进2字符，12pt
- 关键词: 段落首行缩进2字符，12pt
- 正文: 段落首行缩进2字符，12pt，1.5倍行距
- 一级标题: 居中，加粗，16pt
- 二级标题: 左对齐，加粗，14pt
- 三级标题: 左对齐，加粗，13pt
- 参考文献: 段落首行缩进2字符，10pt
            """,
            "报告模板": """
报告模板预览:
- 标题格式: 居中，加粗，18pt
- 章节标题: 居中，加粗，16pt
- 小节标题: 左对齐，加粗，14pt
- 正文: 段落首行缩进2字符，12pt，1.5倍行距
- 列表项: 12pt，左对齐
- 图表标题: 居中，12pt，加粗
- 表格内容: 11pt，居中
            """,
            "小说模板": """
小说模板预览:
- 书名: 居中，加粗，20pt
- 作者信息: 居中，14pt
- 章节标题: 居中，16pt
- 正文: 段落首行缩进2字符，12pt，1.5倍行距
- 对话: 与正文相同，可加引号标识
- 注释: 脚注格式，9pt
            """,
            "简历模板": """
简历模板预览:
- 姓名: 居中，加粗，18pt
- 联系方式: 居中，12pt
- 栏目标题: 左对齐，加粗，14pt
- 内容段落: 左对齐，11pt
- 项目列表: 11pt，左对齐，项目符号
- 日期: 右对齐，11pt
            """,
            "信函模板": """
信函模板预览:
- 发件人信息: 左对齐，12pt
- 日期: 右对齐，12pt
- 收件人信息: 左对齐，12pt
- 称呼: 左对齐，12pt
- 正文: 段落首行缩进2字符，12pt，1.5倍行距
- 结尾问候语: 左对齐，12pt
- 署名: 左对齐，12pt
            """,
            "默认模板": """
默认模板预览:
- 标题: 居中，加粗，16pt
- 副标题: 居中，14pt
- 正文: 段落首行缩进2字符，12pt，1.5倍行距
- 一级标题: 左对齐，加粗，16pt
- 二级标题: 左对齐，加粗，14pt
- 三级标题: 左对齐，加粗，13pt
- 列表项: 12pt，左对齐
- 表格: 12pt，居中
- 图片说明: 居中，10pt
            """
        }
        
        self.preview_text.setText(templates.get(template_name, "模板预览不可用"))
    
    def apply_template_settings(self, template_name):
        """应用模板设置"""
        # 根据模板名称设置不同的默认值
        if template_name == "学术论文模板":
            self.first_line_indent_spin.setValue(2.0)
            self.line_spacing_combo.setCurrentText("1.5")
            self.justify_radio.setChecked(True)
            
            # 设置各级标题大小
            if "标题1" in self.style_configs:
                self.style_configs["标题1"]['size'].setValue(16)
                self.style_configs["标题1"]['bold'].setChecked(True)
            
            if "标题2" in self.style_configs:
                self.style_configs["标题2"]['size'].setValue(14)
                self.style_configs["标题2"]['bold'].setChecked(True)
                
            # 设置正文
            if "正文" in self.style_configs:
                self.style_configs["正文"]['size'].setValue(12)
                
            # 设置脚注
            if "脚注" in self.style_configs:
                self.style_configs["脚注"]['size'].setValue(9)
                
        elif template_name == "报告模板":
            self.first_line_indent_spin.setValue(2.0)
            self.line_spacing_combo.setCurrentText("1.5")
            
            # 设置各级标题大小
            if "标题1" in self.style_configs:
                self.style_configs["标题1"]['size'].setValue(18)
                self.style_configs["标题1"]['bold'].setChecked(True)
            
            # 设置表标题
            if "表标题" in self.style_configs:
                self.style_configs["表标题"]['size'].setValue(12)
                self.style_configs["表标题"]['bold'].setChecked(True)
                
        # 可以继续添加其他模板的应用逻辑...
    
    def save_config(self):
        """保存配置"""
        # 收集字体设置
        self.config['chinese_font'] = self.chinese_font_combo.currentFont().family()
        self.config['english_font'] = self.english_font_combo.currentFont().family()
        self.config['font_size'] = self.font_size_spin.value()
        
        # 收集段落设置
        self.config['first_line_indent'] = self.first_line_indent_spin.value()
        self.config['line_spacing'] = float(self.line_spacing_combo.currentText())
        self.config['paragraph_spacing'] = self.paragraph_spacing_spin.value()
        self.config['alignment'] = self.align_group.checkedId()
        
        # 收集页面设置
        self.config['page_size'] = self.page_size_combo.currentText()
        self.config['orientation'] = self.orientation_group.checkedId()
        self.config['margin_top'] = self.margin_top_spin.value()
        self.config['margin_bottom'] = self.margin_bottom_spin.value()
        self.config['margin_left'] = self.margin_left_spin.value()
        self.config['margin_right'] = self.margin_right_spin.value()
        
        # 收集样式设置
        self.config['styles'] = {}
        for style_name, controls in self.style_configs.items():
            self.config['styles'][style_name] = {
                'font': controls['font'].currentFont().family(),
                'size': controls['size'].value(),
                'bold': controls['bold'].isChecked(),
                'italic': controls['italic'].isChecked(),
                'underline': controls['underline'].isChecked()
            }
        
        # 发送配置保存信号
        self.config_saved.emit(self.config)
        self.accept()


class PandocGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pandoc GUI')
        self.setGeometry(100, 100, 600, 400)
        
        # 获取项目根目录
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pandoc_path = os.path.join(self.root_dir, 'pandoc', 'pandoc.exe')
        
        # 支持的文件格式
        self.supported_formats = [
            'markdown', 'docx', 'pdf', 'html', 'epub', 'odt', 
            'txt', 'rst', 'json', 'latex', 'xml', 'pptx'
        ]
        
        self.input_file = None
        self.template_file = None
        self.format_config = None  # 存储排版配置
        
        self.init_ui()
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具')
        
    
    def init_ui(self):
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
        self.template_label = QLabel('未选择模板文件（可选）')
        self.template_label.setFixedWidth(300)
        template_button = QPushButton('选择模板文件')
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
        
        # 排版配置按钮
        config_button = QPushButton('排版配置')
        config_button.clicked.connect(self.open_format_config_dialog)
        config_button.setFixedWidth(120)
        format_layout.addWidget(config_button)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # 转换按钮
        self.convert_button = QPushButton('转换文件')
        self.convert_button.clicked.connect(self.convert_file)
        self.convert_button.setFixedHeight(40)
        self.convert_button.setEnabled(False)
        
        # 应用排版格式按钮
        self.apply_format_button = QPushButton('应用排版格式')
        self.apply_format_button.clicked.connect(self.apply_format_to_docx)
        self.apply_format_button.setFixedHeight(40)
        self.apply_format_button.setEnabled(False)
        
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.apply_format_button)
        
        # 状态显示
        self.status_label = QLabel('就绪')
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # 添加所有布局到主布局
        main_layout.addLayout(file_layout)
        main_layout.addLayout(format_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addStretch()
    
    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择输入文件', '', '所有文件 (*.*)'
        )
        if file_path:
            self.input_file = file_path
            self.input_label.setText(os.path.basename(file_path))
            self.convert_button.setEnabled(True)
            self.status_label.setText(f'已选择输入文件：{os.path.basename(file_path)}')
    
    def select_template_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择模板文件', '', 'Word文档 (*.docx)'
        )
        if file_path:
            self.template_file = file_path
            self.template_label.setText(os.path.basename(file_path))
            self.status_label.setText(f'已选择模板文件：{os.path.basename(file_path)}')
    
    def convert_file(self):
        if not self.input_file:
            QMessageBox.warning(self, '警告', '请先选择输入文件')
            return
        
        output_format = self.format_combo.currentText()
        
        # 生成输出文件名
        input_dir = os.path.dirname(self.input_file)
        input_name = os.path.splitext(os.path.basename(self.input_file))[0]
        output_file = os.path.join(input_dir, f'{input_name}_converted.{output_format}')
        
        # 构建pandoc命令
        cmd = [self.pandoc_path, self.input_file, '-o', output_file]
        
        # 如果有模板文件，添加模板参数
        if self.template_file and output_format == 'docx':
            cmd.extend(['--reference-doc', self.template_file])
        
        try:
            self.status_label.setText('正在转换...')
            QApplication.processEvents()
            
            # 执行pandoc命令
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            
            self.status_label.setText(f'转换成功：{os.path.basename(output_file)}')
            QMessageBox.information(self, '成功', f'文件已转换为：{output_file}')
            
        except subprocess.CalledProcessError as e:
            self.status_label.setText('转换失败')
            QMessageBox.critical(
                self, '错误', 
                f'转换失败：\n{e.stderr if e.stderr else str(e)}'
            )
        except Exception as e:
            self.status_label.setText('转换失败')
            QMessageBox.critical(self, '错误', f'发生错误：\n{str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PandocGUI()
    window.show()
    sys.exit(app.exec_())