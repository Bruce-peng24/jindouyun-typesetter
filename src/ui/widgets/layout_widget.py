"""
非文本与布局样式块配置组件
包含块文本、水平线、表格和图片说明的样式配置
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QGroupBox,
    QFormLayout, QFontComboBox, QSpinBox, QCheckBox, QComboBox,
    QDoubleSpinBox, QPushButton
)
from PyQt5.QtCore import Qt


class LayoutWidget(QWidget):
    """非文本与布局样式块配置组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # 块文本样式
        block_group = QGroupBox("块文本")
        block_layout = QFormLayout()
        
        self.block_font_combo = QFontComboBox()
        self.block_font_combo.setFontFilters(QFontComboBox.AllFonts)
        block_layout.addRow("字体:", self.block_font_combo)
        
        self.block_font_size_spin = QSpinBox()
        self.block_font_size_spin.setRange(8, 72)
        self.block_font_size_spin.setValue(12)
        block_layout.addRow("字体大小:", self.block_font_size_spin)
        
        self.block_bold_check = QCheckBox("粗体")
        block_layout.addRow("", self.block_bold_check)
        
        self.block_italic_check = QCheckBox("斜体")
        block_layout.addRow("", self.block_italic_check)
        
        # 块文本缩进
        self.block_indent_spin = QDoubleSpinBox()
        self.block_indent_spin.setRange(0, 10)
        self.block_indent_spin.setValue(2)
        self.block_indent_spin.setSuffix(" 字符")
        block_layout.addRow("左右缩进:", self.block_indent_spin)
        
        block_group.setLayout(block_layout)
        scroll_layout.addWidget(block_group)
        
        # 水平线样式
        hr_group = QGroupBox("水平线")
        hr_layout = QFormLayout()
        
        self.hr_thickness_spin = QDoubleSpinBox()
        self.hr_thickness_spin.setRange(0.5, 5)
        self.hr_thickness_spin.setValue(1)
        self.hr_thickness_spin.setSuffix(" 磅")
        hr_layout.addRow("线条粗细:", self.hr_thickness_spin)
        
        self.hr_width_spin = QSpinBox()
        self.hr_width_spin.setRange(10, 100)
        self.hr_width_spin.setValue(100)
        self.hr_width_spin.setSuffix("%")
        hr_layout.addRow("线条宽度:", self.hr_width_spin)
        
        self.hr_color_button = QPushButton("选择颜色")
        hr_layout.addRow("线条颜色:", self.hr_color_button)
        
        hr_group.setLayout(hr_layout)
        scroll_layout.addWidget(hr_group)
        
        # 表标题样式
        table_caption_group = QGroupBox("表标题")
        table_caption_layout = QFormLayout()
        
        self.table_caption_font_combo = QFontComboBox()
        self.table_caption_font_combo.setFontFilters(QFontComboBox.AllFonts)
        table_caption_layout.addRow("字体:", self.table_caption_font_combo)
        
        self.table_caption_font_size_spin = QSpinBox()
        self.table_caption_font_size_spin.setRange(8, 48)
        self.table_caption_font_size_spin.setValue(12)
        table_caption_layout.addRow("字体大小:", self.table_caption_font_size_spin)
        
        self.table_caption_bold_check = QCheckBox("粗体")
        self.table_caption_bold_check.setChecked(True)
        table_caption_layout.addRow("", self.table_caption_bold_check)
        
        self.table_caption_italic_check = QCheckBox("斜体")
        table_caption_layout.addRow("", self.table_caption_italic_check)
        
        # 表标题位置
        self.table_caption_position_combo = QComboBox()
        self.table_caption_position_combo.addItems(["表格上方", "表格下方"])
        table_caption_layout.addRow("位置:", self.table_caption_position_combo)
        
        table_caption_group.setLayout(table_caption_layout)
        scroll_layout.addWidget(table_caption_group)
        
        # 表格样式
        table_group = QGroupBox("表格")
        table_layout = QFormLayout()
        
        self.table_font_combo = QFontComboBox()
        self.table_font_combo.setFontFilters(QFontComboBox.AllFonts)
        table_layout.addRow("字体:", self.table_font_combo)
        
        self.table_font_size_spin = QSpinBox()
        self.table_font_size_spin.setRange(8, 48)
        self.table_font_size_spin.setValue(10)
        table_layout.addRow("字体大小:", self.table_font_size_spin)
        
        self.table_header_bold_check = QCheckBox("表头粗体")
        self.table_header_bold_check.setChecked(True)
        table_layout.addRow("", self.table_header_bold_check)
        
        # 表格边框
        self.table_border_check = QCheckBox("显示边框")
        self.table_border_check.setChecked(True)
        table_layout.addRow("", self.table_border_check)
        
        table_group.setLayout(table_layout)
        scroll_layout.addWidget(table_group)
        
        # 图片说明样式
        figure_caption_group = QGroupBox("图片说明")
        figure_caption_layout = QFormLayout()
        
        self.figure_caption_font_combo = QFontComboBox()
        self.figure_caption_font_combo.setFontFilters(QFontComboBox.AllFonts)
        figure_caption_layout.addRow("字体:", self.figure_caption_font_combo)
        
        self.figure_caption_font_size_spin = QSpinBox()
        self.figure_caption_font_size_spin.setRange(8, 48)
        self.figure_caption_font_size_spin.setValue(10)
        figure_caption_layout.addRow("字体大小:", self.figure_caption_font_size_spin)
        
        self.figure_caption_bold_check = QCheckBox("粗体")
        figure_caption_layout.addRow("", self.figure_caption_bold_check)
        
        self.figure_caption_italic_check = QCheckBox("斜体")
        self.figure_caption_italic_check.setChecked(True)
        figure_caption_layout.addRow("", self.figure_caption_italic_check)
        
        # 图片说明位置
        self.figure_caption_position_combo = QComboBox()
        self.figure_caption_position_combo.addItems(["图片下方", "图片上方"])
        self.figure_caption_position_combo.setCurrentText("图片下方")
        figure_caption_layout.addRow("位置:", self.figure_caption_position_combo)
        
        figure_caption_group.setLayout(figure_caption_layout)
        scroll_layout.addWidget(figure_caption_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
    
    def set_color_chooser_callback(self, callback):
        """设置颜色选择回调函数"""
        self.hr_color_button.clicked.connect(
            lambda: callback(self.hr_color_button)
        )
    
    def get_config(self):
        """获取当前配置"""
        return {
            'block_text': {
                'font': self.block_font_combo.currentFont().family(),
                'size': self.block_font_size_spin.value(),
                'bold': self.block_bold_check.isChecked(),
                'italic': self.block_italic_check.isChecked(),
                'indent': self.block_indent_spin.value()
            },
            'horizontal_line': {
                'thickness': self.hr_thickness_spin.value(),
                'width': self.hr_width_spin.value(),
                'color': getattr(self.hr_color_button, 'property', lambda x: None)('color') or '#000000'
            },
            'table_caption': {
                'font': self.table_caption_font_combo.currentFont().family(),
                'size': self.table_caption_font_size_spin.value(),
                'bold': self.table_caption_bold_check.isChecked(),
                'italic': self.table_caption_italic_check.isChecked(),
                'position': self.table_caption_position_combo.currentText()
            },
            'table': {
                'font': self.table_font_combo.currentFont().family(),
                'size': self.table_font_size_spin.value(),
                'header_bold': self.table_header_bold_check.isChecked(),
                'border': self.table_border_check.isChecked()
            },
            'figure_caption': {
                'font': self.figure_caption_font_combo.currentFont().family(),
                'size': self.figure_caption_font_size_spin.value(),
                'bold': self.figure_caption_bold_check.isChecked(),
                'italic': self.figure_caption_italic_check.isChecked(),
                'position': self.figure_caption_position_combo.currentText()
            }
        }
    
    def load_config(self, config):
        """加载配置"""
        # 加载块文本样式
        if 'block_text' in config:
            block_text = config['block_text']
            self.block_font_combo.setCurrentText(block_text.get('font', '宋体'))
            self.block_font_size_spin.setValue(block_text.get('size', 12))
            self.block_bold_check.setChecked(block_text.get('bold', False))
            self.block_italic_check.setChecked(block_text.get('italic', False))
            self.block_indent_spin.setValue(block_text.get('indent', 2))
        
        # 加载水平线样式
        if 'horizontal_line' in config:
            hr = config['horizontal_line']
            self.hr_thickness_spin.setValue(hr.get('thickness', 1))
            self.hr_width_spin.setValue(hr.get('width', 100))
            
            color = hr.get('color', '#000000')
            self.hr_color_button.setStyleSheet(f"background-color: {color}")
            self.hr_color_button.setProperty('color', color)
        
        # 加载表标题样式
        if 'table_caption' in config:
            table_caption = config['table_caption']
            self.table_caption_font_combo.setCurrentText(table_caption.get('font', '宋体'))
            self.table_caption_font_size_spin.setValue(table_caption.get('size', 12))
            self.table_caption_bold_check.setChecked(table_caption.get('bold', True))
            self.table_caption_italic_check.setChecked(table_caption.get('italic', False))
            self.table_caption_position_combo.setCurrentText(table_caption.get('position', '表格上方'))
        
        # 加载表格样式
        if 'table' in config:
            table = config['table']
            self.table_font_combo.setCurrentText(table.get('font', '宋体'))
            self.table_font_size_spin.setValue(table.get('size', 10))
            self.table_header_bold_check.setChecked(table.get('header_bold', True))
            self.table_border_check.setChecked(table.get('border', True))
        
        # 加载图片说明样式
        if 'figure_caption' in config:
            figure_caption = config['figure_caption']
            self.figure_caption_font_combo.setCurrentText(figure_caption.get('font', '宋体'))
            self.figure_caption_font_size_spin.setValue(figure_caption.get('size', 10))
            self.figure_caption_bold_check.setChecked(figure_caption.get('bold', False))
            self.figure_caption_italic_check.setChecked(figure_caption.get('italic', True))
            self.figure_caption_position_combo.setCurrentText(figure_caption.get('position', '图片下方'))
    
    def load_default_config(self):
        """加载默认配置"""
        self.block_font_combo.setCurrentText('宋体')
        self.table_caption_font_combo.setCurrentText('宋体')
        self.table_caption_bold_check.setChecked(True)
        self.table_font_combo.setCurrentText('宋体')
        self.table_border_check.setChecked(True)
        self.figure_caption_font_combo.setCurrentText('宋体')
        self.figure_caption_italic_check.setChecked(True)
        self.figure_caption_position_combo.setCurrentText('图片下方')
        
        # 设置默认水平线颜色
        default_color = '#000000'
        self.hr_color_button.setStyleSheet(f"background-color: {default_color}")
        self.hr_color_button.setProperty('color', default_color)
    
    def apply_report_template(self):
        """应用报告模板"""
        self.table_caption_bold_check.setChecked(True)
        self.table_font_size_spin.setValue(11)