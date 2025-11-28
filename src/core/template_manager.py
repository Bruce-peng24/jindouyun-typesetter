"""
模板管理模块
处理预设模板的加载和应用
"""

from PyQt5.QtGui import QFont


class TemplateManager:
    """模板管理器"""
    
    def __init__(self):
        self.templates = {
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
    
    def get_template_preview(self, template_name):
        """获取模板预览文本"""
        return self.templates.get(template_name, "模板预览不可用")
    
    def apply_template(self, template_name, widgets):
        """应用指定模板到各个配置组件"""
        if template_name == "学术论文模板":
            self.apply_academic_template(widgets)
        elif template_name == "报告模板":
            self.apply_report_template(widgets)
        elif template_name == "小说模板":
            self.apply_novel_template(widgets)
        elif template_name == "简历模板":
            self.apply_resume_template(widgets)
        elif template_name == "信函模板":
            self.apply_letter_template(widgets)
        elif template_name == "默认模板":
            self.load_default_config(widgets)
    
    def apply_academic_template(self, widgets):
        """应用学术论文模板"""
        # 基础文本与段落样式
        basic_text = widgets['basic_text']
        basic_text.chinese_font_combo.setCurrentFont(QFont("宋体"))
        basic_text.english_font_combo.setCurrentFont(QFont("Times New Roman"))
        basic_text.number_font_combo.setCurrentFont(QFont("Times New Roman"))
        basic_text.first_line_indent_spin.setValue(2.0)
        basic_text.line_spacing_combo.setCurrentText("1.5")
        basic_text.paragraph_spacing_spin.setValue(6)
        basic_text.justify_radio.setChecked(True)
        
        # 标题样式
        widgets['heading'].apply_academic_template()
        
        # 脚注样式
        reference = widgets['reference']
        reference.footnote_font_size_spin.setValue(9)
        reference.footnote_italic_check.setChecked(True)
        reference.footnote_ref_superscript_check.setChecked(True)
    
    def apply_report_template(self, widgets):
        """应用报告模板"""
        # 基础文本与段落样式
        basic_text = widgets['basic_text']
        basic_text.chinese_font_combo.setCurrentFont(QFont("宋体"))
        basic_text.english_font_combo.setCurrentFont(QFont("Arial"))
        basic_text.number_font_combo.setCurrentFont(QFont("Arial"))
        basic_text.first_line_indent_spin.setValue(2.0)
        basic_text.line_spacing_combo.setCurrentText("1.5")
        basic_text.paragraph_spacing_spin.setValue(6)
        basic_text.justify_radio.setChecked(True)
        
        # 标题样式
        widgets['heading'].apply_report_template()
        
        # 表格样式
        widgets['layout'].apply_report_template()
    
    def apply_novel_template(self, widgets):
        """应用小说模板"""
        # 基础文本与段落样式
        basic_text = widgets['basic_text']
        basic_text.chinese_font_combo.setCurrentFont(QFont("宋体"))
        basic_text.english_font_combo.setCurrentFont(QFont("Times New Roman"))
        basic_text.number_font_combo.setCurrentFont(QFont("Times New Roman"))
        basic_text.first_line_indent_spin.setValue(2.0)
        basic_text.line_spacing_combo.setCurrentText("1.5")
        basic_text.paragraph_spacing_spin.setValue(6)
        basic_text.justify_radio.setChecked(True)
        
        # 标题样式
        widgets['heading'].apply_novel_template()
    
    def apply_resume_template(self, widgets):
        """应用简历模板"""
        # 基础文本与段落样式
        basic_text = widgets['basic_text']
        basic_text.chinese_font_combo.setCurrentFont(QFont("宋体"))
        basic_text.english_font_combo.setCurrentFont(QFont("Arial"))
        basic_text.number_font_combo.setCurrentFont(QFont("Arial"))
        basic_text.first_line_indent_spin.setValue(0)  # 简历通常不首行缩进
        basic_text.line_spacing_combo.setCurrentText("1.15")
        basic_text.paragraph_spacing_spin.setValue(3)
        basic_text.left_radio.setChecked(True)  # 左对齐
        
        # 标题样式
        widgets['heading'].apply_resume_template()
    
    def apply_letter_template(self, widgets):
        """应用信函模板"""
        # 基础文本与段落样式
        basic_text = widgets['basic_text']
        basic_text.chinese_font_combo.setCurrentFont(QFont("宋体"))
        basic_text.english_font_combo.setCurrentFont(QFont("Times New Roman"))
        basic_text.number_font_combo.setCurrentFont(QFont("Times New Roman"))
        basic_text.first_line_indent_spin.setValue(2.0)
        basic_text.line_spacing_combo.setCurrentText("1.5")
        basic_text.paragraph_spacing_spin.setValue(6)
        basic_text.left_radio.setChecked(True)  # 左对齐
        
        # 标题样式
        widgets['heading'].apply_letter_template()
    
    def load_default_config(self, widgets):
        """加载默认配置"""
        # 基础文本与段落样式默认值
        basic_text = widgets['basic_text']
        basic_text.chinese_font_combo.setCurrentFont(QFont("宋体"))
        basic_text.english_font_combo.setCurrentFont(QFont("Times New Roman"))
        basic_text.number_font_combo.setCurrentFont(QFont("Times New Roman"))
        basic_text.paragraph_font_combo.setCurrentFont(QFont("宋体"))
        basic_text.body_font_combo.setCurrentFont(QFont("宋体"))
        basic_text.justify_radio.setChecked(True)
        
        # 标题样式默认值
        widgets['heading'].load_default_config()
        
        # 列表样式默认值
        widgets['list'].load_default_config()
        
        # 引用与交互元素样式默认值
        widgets['reference'].load_default_config()
        
        # 非文本与布局样式块默认值
        widgets['layout'].load_default_config()
        
        # 页面设置默认值使用组件的默认值
        # (因为页面设置通常不需要模板化)