"""
标题配置组件
包含各级标题的样式配置
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QGroupBox,
    QFormLayout, QFontComboBox, QSpinBox, QCheckBox, QComboBox
)
from PyQt5.QtCore import Qt


class HeadingWidget(QWidget):
    """标题与层级样式配置组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.heading_configs = {}
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # 标题样式
        for level in range(1, 10):
            group = QGroupBox(f"标题{level}")
            group_layout = QFormLayout()
            
            # 字体选择
            font_combo = QFontComboBox()
            font_combo.setFontFilters(QFontComboBox.AllFonts)
            group_layout.addRow("字体:", font_combo)
            
            # 字体大小
            size_spin = QSpinBox()
            size_spin.setRange(6, 72)
            if level == 1:
                size_spin.setValue(16)
            elif level == 2:
                size_spin.setValue(14)
            elif level == 3:
                size_spin.setValue(13)
            else:
                size_spin.setValue(12)
            group_layout.addRow("字体大小:", size_spin)
            
            # 粗体
            bold_check = QCheckBox("粗体")
            bold_check.setChecked(True if level <= 3 else False)
            group_layout.addRow("", bold_check)
            
            # 斜体
            italic_check = QCheckBox("斜体")
            group_layout.addRow("", italic_check)
            
            # 下划线
            underline_check = QCheckBox("下划线")
            group_layout.addRow("", underline_check)
            
            # 对齐方式
            align_combo = QComboBox()
            align_combo.addItems(["左对齐", "居中对齐", "右对齐", "两端对齐"])
            if level == 1:
                align_combo.setCurrentText("居中对齐")
            else:
                align_combo.setCurrentText("左对齐")
            group_layout.addRow("对齐方式:", align_combo)
            
            # 保存控件引用
            self.heading_configs[f"标题{level}"] = {
                'font': font_combo,
                'size': size_spin,
                'bold': bold_check,
                'italic': italic_check,
                'underline': underline_check,
                'align': align_combo
            }
            
            group.setLayout(group_layout)
            scroll_layout.addWidget(group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
    
    def get_config(self):
        """获取当前配置"""
        config = {}
        for level, controls in self.heading_configs.items():
            config[level] = {
                'font': controls['font'].currentFont().family(),
                'size': controls['size'].value(),
                'bold': controls['bold'].isChecked(),
                'italic': controls['italic'].isChecked(),
                'underline': controls['underline'].isChecked(),
                'align': controls['align'].currentText()
            }
        return config
    
    def load_config(self, config):
        """加载配置"""
        for level, heading_config in config.items():
            if level in self.heading_configs:
                controls = self.heading_configs[level]
                controls['font'].setCurrentText(heading_config.get('font', '宋体'))
                controls['size'].setValue(heading_config.get('size', 12))
                controls['bold'].setChecked(heading_config.get('bold', False))
                controls['italic'].setChecked(heading_config.get('italic', False))
                controls['underline'].setChecked(heading_config.get('underline', False))
                controls['align'].setCurrentText(heading_config.get('align', '左对齐'))
    
    def apply_academic_template(self):
        """应用学术论文模板"""
        for level, controls in self.heading_configs.items():
            level_num = int(level.replace("标题", ""))
            if level_num == 1:
                controls['size'].setValue(16)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("居中对齐")
            elif level_num == 2:
                controls['size'].setValue(14)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("左对齐")
            elif level_num == 3:
                controls['size'].setValue(13)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("左对齐")
            else:
                controls['size'].setValue(12)
                controls['bold'].setChecked(False)
                controls['align'].setCurrentText("左对齐")
    
    def apply_report_template(self):
        """应用报告模板"""
        for level, controls in self.heading_configs.items():
            level_num = int(level.replace("标题", ""))
            if level_num == 1:
                controls['size'].setValue(18)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("居中对齐")
            elif level_num == 2:
                controls['size'].setValue(16)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("居中对齐")
            else:
                controls['size'].setValue(14)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("左对齐")
    
    def apply_novel_template(self):
        """应用小说模板"""
        for level, controls in self.heading_configs.items():
            level_num = int(level.replace("标题", ""))
            if level_num == 1:
                controls['size'].setValue(20)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("居中对齐")
            elif level_num == 2:
                controls['size'].setValue(16)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("居中对齐")
            else:
                controls['size'].setValue(14)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("左对齐")
    
    def apply_resume_template(self):
        """应用简历模板"""
        for level, controls in self.heading_configs.items():
            level_num = int(level.replace("标题", ""))
            if level_num == 1:
                controls['size'].setValue(18)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("居中对齐")
            else:
                controls['size'].setValue(14)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("左对齐")
    
    def apply_letter_template(self):
        """应用信函模板"""
        for level, controls in self.heading_configs.items():
            level_num = int(level.replace("标题", ""))
            if level_num == 1:
                controls['size'].setValue(16)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("左对齐")
            else:
                controls['size'].setValue(14)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("左对齐")
    
    def load_default_config(self):
        """加载默认配置"""
        for level, controls in self.heading_configs.items():
            level_num = int(level.replace("标题", ""))
            if level_num == 1:
                controls['size'].setValue(16)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("居中对齐")
            elif level_num == 2:
                controls['size'].setValue(14)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("左对齐")
            elif level_num == 3:
                controls['size'].setValue(13)
                controls['bold'].setChecked(True)
                controls['align'].setCurrentText("左对齐")
            else:
                controls['size'].setValue(12)
                controls['bold'].setChecked(False)
                controls['align'].setCurrentText("左对齐")