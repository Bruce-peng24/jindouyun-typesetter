"""
页面设置配置组件
包含页面尺寸、页边距和页眉页脚的配置
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout,
    QComboBox, QButtonGroup, QRadioButton, QDoubleSpinBox,
    QFontComboBox, QSpinBox, QLineEdit
)
from PyQt5.QtCore import Qt


class PageWidget(QWidget):
    """页面设置配置组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
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
        
        # 页眉页脚
        header_footer_group = QGroupBox("页眉页脚")
        header_footer_layout = QFormLayout()
        
        self.header_font_combo = QFontComboBox()
        self.header_font_combo.setFontFilters(QFontComboBox.AllFonts)
        header_footer_layout.addRow("页眉字体:", self.header_font_combo)
        
        self.header_font_size_spin = QSpinBox()
        self.header_font_size_spin.setRange(8, 48)
        self.header_font_size_spin.setValue(9)
        header_footer_layout.addRow("页眉字体大小:", self.header_font_size_spin)
        
        self.footer_font_combo = QFontComboBox()
        self.footer_font_combo.setFontFilters(QFontComboBox.AllFonts)
        header_footer_layout.addRow("页脚字体:", self.footer_font_combo)
        
        self.footer_font_size_spin = QSpinBox()
        self.footer_font_size_spin.setRange(8, 48)
        self.footer_font_size_spin.setValue(9)
        header_footer_layout.addRow("页脚字体大小:", self.footer_font_size_spin)
        
        self.header_text_edit = QLineEdit()
        self.header_text_edit.setPlaceholderText("页眉文本")
        header_footer_layout.addRow("页眉文本:", self.header_text_edit)
        
        self.footer_text_edit = QLineEdit()
        self.footer_text_edit.setPlaceholderText("页脚文本")
        header_footer_layout.addRow("页脚文本:", self.footer_text_edit)
        
        header_footer_group.setLayout(header_footer_layout)
        layout.addWidget(header_footer_group)
        
        layout.addStretch()
    
    def get_config(self):
        """获取当前配置"""
        return {
            'size': self.page_size_combo.currentText(),
            'orientation': self.orientation_group.checkedId(),
            'margins': {
                'top': self.margin_top_spin.value(),
                'bottom': self.margin_bottom_spin.value(),
                'left': self.margin_left_spin.value(),
                'right': self.margin_right_spin.value()
            },
            'header_footer': {
                'header_font': self.header_font_combo.currentFont().family(),
                'header_size': self.header_font_size_spin.value(),
                'header_text': self.header_text_edit.text(),
                'footer_font': self.footer_font_combo.currentFont().family(),
                'footer_size': self.footer_font_size_spin.value(),
                'footer_text': self.footer_text_edit.text()
            }
        }
    
    def load_config(self, config):
        """加载配置"""
        # 加载页面尺寸
        self.page_size_combo.setCurrentText(config.get('size', 'A4'))
        
        # 加载页面方向
        orientation = config.get('orientation', 0)
        if orientation == 1:
            self.landscape_radio.setChecked(True)
        else:
            self.portrait_radio.setChecked(True)
        
        # 加载页边距
        if 'margins' in config:
            margins = config['margins']
            self.margin_top_spin.setValue(margins.get('top', 2.54))
            self.margin_bottom_spin.setValue(margins.get('bottom', 2.54))
            self.margin_left_spin.setValue(margins.get('left', 3.17))
            self.margin_right_spin.setValue(margins.get('right', 3.17))
        
        # 加载页眉页脚
        if 'header_footer' in config:
            header_footer = config['header_footer']
            self.header_font_combo.setCurrentText(header_footer.get('header_font', '宋体'))
            self.header_font_size_spin.setValue(header_footer.get('header_size', 9))
            self.header_text_edit.setText(header_footer.get('header_text', ''))
            self.footer_font_combo.setCurrentText(header_footer.get('footer_font', '宋体'))
            self.footer_font_size_spin.setValue(header_footer.get('footer_size', 9))
            self.footer_text_edit.setText(header_footer.get('footer_text', ''))