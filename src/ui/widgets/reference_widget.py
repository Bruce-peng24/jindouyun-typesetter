"""
引用与交互元素配置组件
包含超链接、脚注等样式配置
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QGroupBox,
    QFormLayout, QFontComboBox, QSpinBox, QCheckBox, QPushButton
)
from PyQt5.QtCore import Qt


class ReferenceWidget(QWidget):
    """引用与交互元素样式配置组件"""
    
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
        
        # 超链接样式
        link_group = QGroupBox("超链接")
        link_layout = QFormLayout()
        
        self.link_font_combo = QFontComboBox()
        self.link_font_combo.setFontFilters(QFontComboBox.AllFonts)
        link_layout.addRow("字体:", self.link_font_combo)
        
        self.link_font_size_spin = QSpinBox()
        self.link_font_size_spin.setRange(8, 72)
        self.link_font_size_spin.setValue(12)
        link_layout.addRow("字体大小:", self.link_font_size_spin)
        
        self.link_bold_check = QCheckBox("粗体")
        link_layout.addRow("", self.link_bold_check)
        
        self.link_italic_check = QCheckBox("斜体")
        link_layout.addRow("", self.link_italic_check)
        
        self.link_underline_check = QCheckBox("下划线")
        self.link_underline_check.setChecked(True)
        link_layout.addRow("", self.link_underline_check)
        
        # 链接颜色
        self.link_color_button = QPushButton("选择颜色")
        link_layout.addRow("链接颜色:", self.link_color_button)
        
        link_group.setLayout(link_layout)
        scroll_layout.addWidget(link_group)
        
        # 脚注样式
        footnote_group = QGroupBox("脚注")
        footnote_layout = QFormLayout()
        
        self.footnote_font_combo = QFontComboBox()
        self.footnote_font_combo.setFontFilters(QFontComboBox.AllFonts)
        footnote_layout.addRow("字体:", self.footnote_font_combo)
        
        self.footnote_font_size_spin = QSpinBox()
        self.footnote_font_size_spin.setRange(6, 48)
        self.footnote_font_size_spin.setValue(9)
        footnote_layout.addRow("字体大小:", self.footnote_font_size_spin)
        
        self.footnote_bold_check = QCheckBox("粗体")
        footnote_layout.addRow("", self.footnote_bold_check)
        
        self.footnote_italic_check = QCheckBox("斜体")
        self.footnote_italic_check.setChecked(True)
        footnote_layout.addRow("", self.footnote_italic_check)
        
        self.footnote_underline_check = QCheckBox("下划线")
        footnote_layout.addRow("", self.footnote_underline_check)
        
        footnote_group.setLayout(footnote_layout)
        scroll_layout.addWidget(footnote_group)
        
        # 脚注引用文本样式
        footnote_ref_group = QGroupBox("脚注引用文本")
        footnote_ref_layout = QFormLayout()
        
        self.footnote_ref_font_size_spin = QSpinBox()
        self.footnote_ref_font_size_spin.setRange(6, 24)
        self.footnote_ref_font_size_spin.setValue(9)
        footnote_ref_layout.addRow("字体大小:", self.footnote_ref_font_size_spin)
        
        self.footnote_ref_superscript_check = QCheckBox("上标")
        self.footnote_ref_superscript_check.setChecked(True)
        footnote_ref_layout.addRow("", self.footnote_ref_superscript_check)
        
        self.footnote_ref_bold_check = QCheckBox("粗体")
        footnote_ref_layout.addRow("", self.footnote_ref_bold_check)
        
        self.footnote_ref_italic_check = QCheckBox("斜体")
        footnote_ref_layout.addRow("", self.footnote_ref_italic_check)
        
        footnote_ref_group.setLayout(footnote_ref_layout)
        scroll_layout.addWidget(footnote_ref_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
    
    def set_color_chooser_callback(self, callback):
        """设置颜色选择回调函数"""
        self.link_color_button.clicked.connect(
            lambda: callback(self.link_color_button)
        )
    
    def get_config(self):
        """获取当前配置"""
        return {
            'link': {
                'font': self.link_font_combo.currentFont().family(),
                'size': self.link_font_size_spin.value(),
                'bold': self.link_bold_check.isChecked(),
                'italic': self.link_italic_check.isChecked(),
                'underline': self.link_underline_check.isChecked(),
                'color': getattr(self.link_color_button, 'property', lambda x: None)('color') or '#0000FF'
            },
            'footnote': {
                'font': self.footnote_font_combo.currentFont().family(),
                'size': self.footnote_font_size_spin.value(),
                'bold': self.footnote_bold_check.isChecked(),
                'italic': self.footnote_italic_check.isChecked(),
                'underline': self.footnote_underline_check.isChecked()
            },
            'footnote_ref': {
                'size': self.footnote_ref_font_size_spin.value(),
                'superscript': self.footnote_ref_superscript_check.isChecked(),
                'bold': self.footnote_ref_bold_check.isChecked(),
                'italic': self.footnote_ref_italic_check.isChecked()
            }
        }
    
    def load_config(self, config):
        """加载配置"""
        # 加载超链接样式
        if 'link' in config:
            link = config['link']
            self.link_font_combo.setCurrentText(link.get('font', '宋体'))
            self.link_font_size_spin.setValue(link.get('size', 12))
            self.link_bold_check.setChecked(link.get('bold', False))
            self.link_italic_check.setChecked(link.get('italic', False))
            self.link_underline_check.setChecked(link.get('underline', True))
            
            color = link.get('color', '#0000FF')
            self.link_color_button.setStyleSheet(f"background-color: {color}")
            self.link_color_button.setProperty('color', color)
        
        # 加载脚注样式
        if 'footnote' in config:
            footnote = config['footnote']
            self.footnote_font_combo.setCurrentText(footnote.get('font', '宋体'))
            self.footnote_font_size_spin.setValue(footnote.get('size', 9))
            self.footnote_bold_check.setChecked(footnote.get('bold', False))
            self.footnote_italic_check.setChecked(footnote.get('italic', True))
            self.footnote_underline_check.setChecked(footnote.get('underline', False))
        
        # 加载脚注引用样式
        if 'footnote_ref' in config:
            footnote_ref = config['footnote_ref']
            self.footnote_ref_font_size_spin.setValue(footnote_ref.get('size', 9))
            self.footnote_ref_superscript_check.setChecked(footnote_ref.get('superscript', True))
            self.footnote_ref_bold_check.setChecked(footnote_ref.get('bold', False))
            self.footnote_ref_italic_check.setChecked(footnote_ref.get('italic', False))
    
    def load_default_config(self):
        """加载默认配置"""
        self.link_font_combo.setCurrentText('宋体')
        self.link_underline_check.setChecked(True)
        self.footnote_font_combo.setCurrentText('宋体')
        self.footnote_italic_check.setChecked(True)
        self.footnote_ref_superscript_check.setChecked(True)
        
        # 设置默认链接颜色
        default_color = '#0000FF'
        self.link_color_button.setStyleSheet(f"background-color: {default_color}")
        self.link_color_button.setProperty('color', default_color)