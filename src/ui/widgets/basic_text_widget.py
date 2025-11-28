"""
基础文本配置组件
包含段落、正文、字符样式和段落格式的配置
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QGroupBox,
    QFormLayout, QFontComboBox, QSpinBox, QCheckBox, QComboBox,
    QButtonGroup, QRadioButton, QDoubleSpinBox
)
from PyQt5.QtCore import Qt


class BasicTextWidget(QWidget):
    """基础文本与段落样式配置组件"""
    
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
        
        # 段落样式
        paragraph_group = QGroupBox("段落")
        paragraph_layout = QFormLayout()
        
        self.paragraph_font_combo = QFontComboBox()
        self.paragraph_font_combo.setFontFilters(QFontComboBox.AllFonts)
        paragraph_layout.addRow("字体:", self.paragraph_font_combo)
        
        self.paragraph_font_size_spin = QSpinBox()
        self.paragraph_font_size_spin.setRange(8, 72)
        self.paragraph_font_size_spin.setValue(12)
        paragraph_layout.addRow("字体大小:", self.paragraph_font_size_spin)
        
        self.paragraph_bold_check = QCheckBox("粗体")
        paragraph_layout.addRow("", self.paragraph_bold_check)
        
        self.paragraph_italic_check = QCheckBox("斜体")
        paragraph_layout.addRow("", self.paragraph_italic_check)
        
        paragraph_group.setLayout(paragraph_layout)
        scroll_layout.addWidget(paragraph_group)
        
        # 正文样式
        body_group = QGroupBox("正文")
        body_layout = QFormLayout()
        
        self.body_font_combo = QFontComboBox()
        self.body_font_combo.setFontFilters(QFontComboBox.AllFonts)
        body_layout.addRow("字体:", self.body_font_combo)
        
        self.body_font_size_spin = QSpinBox()
        self.body_font_size_spin.setRange(8, 72)
        self.body_font_size_spin.setValue(12)
        body_layout.addRow("字体大小:", self.body_font_size_spin)
        
        self.body_bold_check = QCheckBox("粗体")
        body_layout.addRow("", self.body_bold_check)
        
        self.body_italic_check = QCheckBox("斜体")
        body_layout.addRow("", self.body_italic_check)
        
        body_group.setLayout(body_layout)
        scroll_layout.addWidget(body_group)
        
        # 正文字符样式
        char_group = QGroupBox("正文字符（包含中文、英文、数字的字体）")
        char_layout = QFormLayout()
        
        # 中文字体
        self.chinese_font_combo = QFontComboBox()
        self.chinese_font_combo.setFontFilters(QFontComboBox.AllFonts)
        char_layout.addRow("中文字体:", self.chinese_font_combo)
        
        # 英文字体
        self.english_font_combo = QFontComboBox()
        self.english_font_combo.setFontFilters(QFontComboBox.AllFonts)
        char_layout.addRow("英文字体:", self.english_font_combo)
        
        # 数字字体
        self.number_font_combo = QFontComboBox()
        self.number_font_combo.setFontFilters(QFontComboBox.AllFonts)
        char_layout.addRow("数字字体:", self.number_font_combo)
        
        self.char_font_size_spin = QSpinBox()
        self.char_font_size_spin.setRange(8, 72)
        self.char_font_size_spin.setValue(12)
        char_layout.addRow("字体大小:", self.char_font_size_spin)
        
        char_group.setLayout(char_layout)
        scroll_layout.addWidget(char_group)
        
        # 段落格式
        format_group = QGroupBox("段落格式")
        format_layout = QFormLayout()
        
        self.first_line_indent_spin = QDoubleSpinBox()
        self.first_line_indent_spin.setRange(0, 10)
        self.first_line_indent_spin.setValue(2)
        self.first_line_indent_spin.setSuffix(" 字符")
        format_layout.addRow("首行缩进:", self.first_line_indent_spin)
        
        self.line_spacing_combo = QComboBox()
        self.line_spacing_combo.addItems(["1.0", "1.15", "1.5", "2.0"])
        self.line_spacing_combo.setCurrentText("1.5")
        format_layout.addRow("行间距:", self.line_spacing_combo)
        
        self.paragraph_spacing_spin = QDoubleSpinBox()
        self.paragraph_spacing_spin.setRange(0, 48)
        self.paragraph_spacing_spin.setValue(6)
        self.paragraph_spacing_spin.setSuffix(" 磅")
        format_layout.addRow("段前间距:", self.paragraph_spacing_spin)
        
        # 对齐方式
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
        
        align_layout = QHBoxLayout()
        align_layout.addWidget(self.left_radio)
        align_layout.addWidget(self.center_radio)
        align_layout.addWidget(self.right_radio)
        align_layout.addWidget(self.justify_radio)
        format_layout.addRow("对齐方式:", align_layout)
        
        format_group.setLayout(format_layout)
        scroll_layout.addWidget(format_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
    
    def get_config(self):
        """获取当前配置"""
        return {
            'paragraph': {
                'font': self.paragraph_font_combo.currentFont().family(),
                'size': self.paragraph_font_size_spin.value(),
                'bold': self.paragraph_bold_check.isChecked(),
                'italic': self.paragraph_italic_check.isChecked()
            },
            'body': {
                'font': self.body_font_combo.currentFont().family(),
                'size': self.body_font_size_spin.value(),
                'bold': self.body_bold_check.isChecked(),
                'italic': self.body_italic_check.isChecked()
            },
            'char': {
                'chinese_font': self.chinese_font_combo.currentFont().family(),
                'english_font': self.english_font_combo.currentFont().family(),
                'number_font': self.number_font_combo.currentFont().family(),
                'size': self.char_font_size_spin.value()
            },
            'format': {
                'first_line_indent': self.first_line_indent_spin.value(),
                'line_spacing': float(self.line_spacing_combo.currentText()),
                'paragraph_spacing': self.paragraph_spacing_spin.value(),
                'alignment': self.align_group.checkedId()
            }
        }
    
    def load_config(self, config):
        """加载配置"""
        # 加载段落样式
        if 'paragraph' in config:
            paragraph = config['paragraph']
            self.paragraph_font_combo.setCurrentText(paragraph.get('font', '宋体'))
            self.paragraph_font_size_spin.setValue(paragraph.get('size', 12))
            self.paragraph_bold_check.setChecked(paragraph.get('bold', False))
            self.paragraph_italic_check.setChecked(paragraph.get('italic', False))
        
        # 加载正文样式
        if 'body' in config:
            body = config['body']
            self.body_font_combo.setCurrentText(body.get('font', '宋体'))
            self.body_font_size_spin.setValue(body.get('size', 12))
            self.body_bold_check.setChecked(body.get('bold', False))
            self.body_italic_check.setChecked(body.get('italic', False))
        
        # 加载字符样式
        if 'char' in config:
            char = config['char']
            self.chinese_font_combo.setCurrentText(char.get('chinese_font', '宋体'))
            self.english_font_combo.setCurrentText(char.get('english_font', 'Times New Roman'))
            self.number_font_combo.setCurrentText(char.get('number_font', 'Times New Roman'))
            self.char_font_size_spin.setValue(char.get('size', 12))
        
        # 加载段落格式
        if 'format' in config:
            format_ = config['format']
            self.first_line_indent_spin.setValue(format_.get('first_line_indent', 2))
            self.line_spacing_combo.setCurrentText(str(format_.get('line_spacing', 1.5)))
            self.paragraph_spacing_spin.setValue(format_.get('paragraph_spacing', 6))
            
            alignment = format_.get('alignment', 3)
            if alignment == 0:
                self.left_radio.setChecked(True)
            elif alignment == 1:
                self.center_radio.setChecked(True)
            elif alignment == 2:
                self.right_radio.setChecked(True)
            else:
                self.justify_radio.setChecked(True)