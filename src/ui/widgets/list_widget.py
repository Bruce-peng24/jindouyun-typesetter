"""
列表配置组件
包含有序列表和无序列表的样式配置
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QGroupBox,
    QFormLayout, QFontComboBox, QSpinBox, QCheckBox, QComboBox
)
from PyQt5.QtCore import Qt


class ListWidget(QWidget):
    """列表样式配置组件"""
    
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
        
        # 有序列表样式
        ordered_group = QGroupBox("有序列表")
        ordered_layout = QFormLayout()
        
        self.ordered_font_combo = QFontComboBox()
        self.ordered_font_combo.setFontFilters(QFontComboBox.AllFonts)
        ordered_layout.addRow("字体:", self.ordered_font_combo)
        
        self.ordered_font_size_spin = QSpinBox()
        self.ordered_font_size_spin.setRange(8, 72)
        self.ordered_font_size_spin.setValue(12)
        ordered_layout.addRow("字体大小:", self.ordered_font_size_spin)
        
        self.ordered_bold_check = QCheckBox("粗体")
        ordered_layout.addRow("", self.ordered_bold_check)
        
        self.ordered_italic_check = QCheckBox("斜体")
        ordered_layout.addRow("", self.ordered_italic_check)
        
        # 编号格式
        self.ordered_format_combo = QComboBox()
        self.ordered_format_combo.addItems(["1, 2, 3...", "a, b, c...", "A, B, C...", "I, II, III..."])
        ordered_layout.addRow("编号格式:", self.ordered_format_combo)
        
        ordered_group.setLayout(ordered_layout)
        scroll_layout.addWidget(ordered_group)
        
        # 无序列表样式
        unordered_group = QGroupBox("无序列表")
        unordered_layout = QFormLayout()
        
        self.unordered_font_combo = QFontComboBox()
        self.unordered_font_combo.setFontFilters(QFontComboBox.AllFonts)
        unordered_layout.addRow("字体:", self.unordered_font_combo)
        
        self.unordered_font_size_spin = QSpinBox()
        self.unordered_font_size_spin.setRange(8, 72)
        self.unordered_font_size_spin.setValue(12)
        unordered_layout.addRow("字体大小:", self.unordered_font_size_spin)
        
        self.unordered_bold_check = QCheckBox("粗体")
        unordered_layout.addRow("", self.unordered_bold_check)
        
        self.unordered_italic_check = QCheckBox("斜体")
        unordered_layout.addRow("", self.unordered_italic_check)
        
        # 项目符号格式
        self.unordered_format_combo = QComboBox()
        self.unordered_format_combo.addItems(["●", "■", "○", "■", "►"])
        unordered_layout.addRow("项目符号:", self.unordered_format_combo)
        
        unordered_group.setLayout(unordered_layout)
        scroll_layout.addWidget(unordered_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
    
    def get_config(self):
        """获取当前配置"""
        return {
            'ordered': {
                'font': self.ordered_font_combo.currentFont().family(),
                'size': self.ordered_font_size_spin.value(),
                'bold': self.ordered_bold_check.isChecked(),
                'italic': self.ordered_italic_check.isChecked(),
                'format': self.ordered_format_combo.currentText()
            },
            'unordered': {
                'font': self.unordered_font_combo.currentFont().family(),
                'size': self.unordered_font_size_spin.value(),
                'bold': self.unordered_bold_check.isChecked(),
                'italic': self.unordered_italic_check.isChecked(),
                'format': self.unordered_format_combo.currentText()
            }
        }
    
    def load_config(self, config):
        """加载配置"""
        # 加载有序列表样式
        if 'ordered' in config:
            ordered = config['ordered']
            self.ordered_font_combo.setCurrentText(ordered.get('font', '宋体'))
            self.ordered_font_size_spin.setValue(ordered.get('size', 12))
            self.ordered_bold_check.setChecked(ordered.get('bold', False))
            self.ordered_italic_check.setChecked(ordered.get('italic', False))
            self.ordered_format_combo.setCurrentText(ordered.get('format', '1, 2, 3...'))
        
        # 加载无序列表样式
        if 'unordered' in config:
            unordered = config['unordered']
            self.unordered_font_combo.setCurrentText(unordered.get('font', '宋体'))
            self.unordered_font_size_spin.setValue(unordered.get('size', 12))
            self.unordered_bold_check.setChecked(unordered.get('bold', False))
            self.unordered_italic_check.setChecked(unordered.get('italic', False))
            self.unordered_format_combo.setCurrentText(unordered.get('format', '●'))
    
    def load_default_config(self):
        """加载默认配置"""
        self.ordered_font_combo.setCurrentText('宋体')
        self.unordered_font_combo.setCurrentText('宋体')