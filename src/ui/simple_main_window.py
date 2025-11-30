"""
简化的主窗口类
实现三步操作界面：HTML输入 -> 排版方案选择 -> 导出文档
"""

import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit, QMessageBox, 
    QApplication, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QTimer

# 添加当前目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入核心模块
from core.enhanced_pandoc_converter import EnhancedPandocConverter

# 导入版本检查模块
from core.version_checker import get_expiration_message, get_test_version_message

# 导入底部tab组件
from ui.bottom_tab_widget import InfoTabWidget


class SimpleMainWindow(QMainWindow):
    """简化的主窗口类 - 三步操作界面"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('筋斗云排版')
        # 调整为更适合1920×1198大屏幕的尺寸
        self.setGeometry(200, 100, 1420, 900)
        # 设置最小宽度
        self.setMinimumWidth(1420)
        # 设置窗口启动时默认全屏
        self.showMaximized()
        
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
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 允许水平滚动
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)
        
        # 创建滚动内容容器
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        
        # 主布局（垂直）
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        
        # 滚动内容布局
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(25)
        scroll_layout.setContentsMargins(35, 35, 35, 25)
        
        # 创建头部区域
        self._create_header_area(scroll_layout)
        
        # 创建步骤区域容器（水平布局）
        steps_container = QWidget()
        steps_layout = QHBoxLayout(steps_container)
        steps_layout.setSpacing(20)
        steps_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建步骤1区域（左侧，占2/3宽度）
        step1_widget = QWidget()
        step1_layout = QVBoxLayout(step1_widget)
        step1_layout.setSpacing(20)
        step1_layout.setContentsMargins(0, 0, 0, 0)
        self._create_step1_area(step1_layout)
        
        # 创建右侧区域（占1/3宽度）
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建步骤2区域（右侧上方）
        self._create_step2_area(right_layout)
        
        # 创建步骤3区域（右侧下方）
        self._create_step3_area(right_layout)
        
        # 添加到水平布局
        steps_layout.addWidget(step1_widget, 2)  # 占2/3宽度
        steps_layout.addWidget(right_widget, 1)   # 占1/3宽度
        
        # 添加步骤容器到滚动布局
        scroll_layout.addWidget(steps_container)
        
        # 创建底部区域
        self._create_bottom_area(scroll_layout)
        
        # 设置样式
        self._set_styles()
        
        # 设置默认描述（在所有UI组件创建后）
        self.template_desc_label.setText(self.layout_templates['simple']['description'])
        
    def _create_header_area(self, parent_layout):
        """创建顶部标题区域"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                padding: 25px 20px;
                margin-bottom: 10px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(8)
        
        # 主标题 - 使用科技蓝突出"筋斗云"
        title_label = QLabel('<span style="color: #ffffff; font-size: 64px; font-weight: 800;">筋斗云</span><span style="color: #f0f9ff; font-size: 64px; font-weight: 600;">排版</span>')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setTextFormat(Qt.RichText)
        
        # 副标题说明
        subtitle_label = QLabel('三步完成专业文档排版：粘贴HTML → 选择样式 → 导出Word')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            font-size: 32px;
            color: #e0f2fe;
            font-weight: 500;
            margin-top: 5px;
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_frame)
        
    def _create_step1_area(self, parent_layout):
        """创建步骤1区域：AI工具使用说明和HTML输入"""
        step1_frame = QFrame()
        step1_frame.setObjectName("step1Frame")
        step1_frame.setStyleSheet("""
            QFrame#step1Frame {
                background-color: #d7e8ff;
                border: 2px solid #93c5fd;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        
        step1_layout = QVBoxLayout(step1_frame)
        step1_layout.setSpacing(20)
        step1_layout.setContentsMargins(25, 20, 25, 20)
        
        # 步骤1标题
        step1_title = QLabel('步骤 1：准备HTML内容')
        step1_title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 5px;
        """)
                
        # AI工具使用说明
        ai_instruction_title = QLabel('使用AI工具生成HTML内容：')
        ai_instruction_title.setStyleSheet("""
            font-size: 28px;
            font-weight: 600;
            color: #0369a1;
            margin-bottom: 8px;
        """)
        
        ai_instruction_text = QLabel(
            '1. 打开任意AI对话工具（如ChatGPT、文心一言等）\n'
            '2. 复制以下指令并发送给AI：\n'
            '3. 将AI返回的HTML内容粘贴到下方文本框'
        )
        ai_instruction_text.setStyleSheet("""
            font-size: 26px;
            color: #0c4a6e;
            line-height: 1.4;
        """)
        
        # AI指令标题和复制按钮行
        ai_command_row_layout = QHBoxLayout()
               
        # 一键复制按钮
        self.copy_button = QPushButton("📋 一键复制")
        self.copy_button.setObjectName("copyButton")
        self.copy_button.setMinimumHeight(40)
        self.copy_button.clicked.connect(self._copy_ai_command)
        
        ai_command_row_layout.addWidget(self.copy_button)
        ai_command_row_layout.addStretch()
        
        self.ai_command_input = QTextEdit()
        self.ai_command_input.setPlainText('你是一个专业的HTML语义化标记专家。请根据以下规则，将提供的文档内容转换为结构良好的HTML代码：\n### 角色与任务\n- **角色**：你是一个经验丰富的Web开发者，擅长使用HTML5进行语义化标记。\n- **主要任务**：使用以下指定的HTML标签集合，对文档内容进行智能格式化，确保输出代码具有良好的可访问性和结构清晰性。\n- **可用标签列表**：html, body, head, title, meta, h1, h2, h3, h4, h5, h6, p, br, hr, strong, b, em, i, ul, ol, li, dl, dt, dd, a, img, table, thead, tbody, tr, th, td, code, pre, blockquote。\n### 具体规则\n1. **文档结构**：\n   - 若内容包含标题层级，使用`h1`-`h6`表示标题等级（如主标题用`h1`，子标题用`h2`等）。\n   - 段落用`p`标签，换行用`br`，水平分割线用`hr`。\n   - 列表内容：无序列表用`ul` > `li`，有序列表用`ol` > `li`，定义列表用`dl` > `dt`（术语）和`dd`（描述）。\n2. **文本强调**：加粗用`strong`（重要）或`b`（纯样式），斜体用`em`（强调）或`i`（技术术语）。\n3. **媒体与表格**：图片链接用`img`（需补全alt属性），表格数据用`table` > `thead`/`tbody` > `tr` > `th`/`td`。\n4. **代码与引用**：内联代码用`code`，代码块用`pre` > `code`，引用块用`blockquote`。\n### 输出要求\n- 生成完整的HTML文档结构（包括`html`、`head`、`body`等必要标签）。\n- 将最终HTML代码包裹在Markdown代码块中（即使用三重反引号格式）。\n- 示例输出格式：\n```\n<!DOCTYPE html>\n<html>\n<head><title>文档标题</title></head>\n<body>......</body>\n</html>\n```')
        self.ai_command_input.setFixedHeight(240)
        self.ai_command_input.setReadOnly(True)  # 设置为只读模式
        self.ai_command_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #93c5fd;
                border-radius: 6px;
                padding: 12px;
                font-size: 22px;
                font-family: 'Consolas', 'Monaco', monospace;
                background-color: white;
                selection-background-color: #3b82f6;
                color: #475569;
            }
            QTextEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)
        
        # HTML输入区域
        html_input_label = QLabel('粘贴HTML内容：')
        html_input_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 10px;
        """)
        
        self.html_input = QTextEdit()
        self.html_input.setPlaceholderText('请在此处粘贴HTML内容...')
        self.html_input.setMinimumHeight(400)
        self.html_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 26px;
                background-color: white;
            }
            QTextEdit:focus {
                border: 2px solid #3b82f6;
                background-color: white;
            }
        """)
        
        # 添加到布局
        step1_layout.addWidget(step1_title)
        step1_layout.addWidget(ai_instruction_title)
        step1_layout.addWidget(ai_instruction_text)
        step1_layout.addLayout(ai_command_row_layout)
        step1_layout.addWidget(self.ai_command_input)
        step1_layout.addWidget(html_input_label)
        step1_layout.addWidget(self.html_input)
        
        parent_layout.addWidget(step1_frame)
        
    def _create_step2_area(self, parent_layout):
        """创建步骤2区域：样式选择"""
        step2_frame = QFrame()
        step2_frame.setObjectName("step2Frame")
        step2_frame.setStyleSheet("""
            QFrame#step2Frame {
                background-color: #d7e8ff;
                border: 2px solid #93c5fd;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        
        step2_layout = QVBoxLayout(step2_frame)
        step2_layout.setSpacing(20)
        step2_layout.setContentsMargins(25, 20, 25, 20)
        
        # 步骤2标题
        step2_title = QLabel('步骤 2：选择文档样式')
        step2_title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 5px;
        """)
                
        # 创建纵向按钮布局
        self.template_buttons_layout = QVBoxLayout()
        self.template_buttons_layout.setSpacing(10)
        
        # 创建按钮组
        self.template_buttons = []
        templates = [
            {'id': 'simple', 'name': '简洁通用', 'desc': '日常办公文档'},
            {'id': 'academic', 'name': '学术论文', 'desc': '适合论文、报告格式'},
            {'id': 'business', 'name': '商务文档', 'desc': '企业报告、方案文档'},
            {'id': 'technical', 'name': '技术文档', 'desc': 'API文档、技术手册'}
        ]
        
        for i, template in enumerate(templates):
            button = QPushButton(template['name'])
            button.setMinimumHeight(60)
            button.setMinimumWidth(240)  # 增加宽度以适应纵向布局
            button.setProperty("template_id", template['id'])
            button.setProperty("template_desc", template['desc'])
            button.clicked.connect(lambda checked, t=template: self._on_template_button_clicked(t))
            
            # 第一个按钮默认选中
            if i == 0:
                button.setObjectName("selectedTemplate")
                self.selected_template = template['id']
            
            self.template_buttons.append(button)
            self.template_buttons_layout.addWidget(button)
        
        # 样式描述
        desc_label = QLabel('样式描述：')
        desc_label.setStyleSheet("""
            font-size: 28px;
            font-weight: 600;
            color: #475569;
            margin-bottom: 0px;
        """)
        
        self.template_desc_label = QLabel(self.layout_templates['simple']['description'])
        self.template_desc_label.setStyleSheet("""
            font-size: 26px;
            color: #64748b;
            line-height: 1.5;
            padding: 0px;
            margin-top: 0px;
        """)
        self.template_desc_label.setWordWrap(True)
        self.template_desc_label.setMinimumHeight(80)
        
        # 添加到布局
        step2_layout.addWidget(step2_title)
        step2_layout.addLayout(self.template_buttons_layout)
        step2_layout.addWidget(desc_label)
        step2_layout.addWidget(self.template_desc_label)
        
        parent_layout.addWidget(step2_frame)
        
    def _create_step3_area(self, parent_layout):
        """创建步骤3区域：生成文档"""
        step3_frame = QFrame()
        step3_frame.setObjectName("step3Frame")
        step3_frame.setStyleSheet("""
            QFrame#step3Frame {
                background-color: #d7e8ff;
                border: 2px solid #6ee7b7;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        
        step3_layout = QVBoxLayout(step3_frame)
        step3_layout.setSpacing(20)
        step3_layout.setContentsMargins(25, 20, 25, 20)
        
        # 步骤3标题
        step3_title = QLabel('步骤 3：生成文档')
        step3_title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 5px;
        """)        
       
        # 操作按钮区域（纵向布局）
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)
        
        # 生成Word文档按钮
        self.generate_button = QPushButton('📄 生成Word文档')
        self.generate_button.setMinimumHeight(80)
        self.generate_button.clicked.connect(self._generate_document)
        self.generate_button.setObjectName("generateButton")
        
        # 清空内容按钮
        self.clear_button = QPushButton('🗑️ 清空内容')
        self.clear_button.setMinimumHeight(80)
        self.clear_button.clicked.connect(self._clear_content)
        self.clear_button.setObjectName("clearButton")
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.clear_button)
        
        # 状态标签
        self.status_label = QLabel('状态：等待用户输入...')
        self.status_label.setStyleSheet("""
            font-size: 30px;
            color: #475569;
            font-weight: 600;
        """)
        
        # 文件保存位置说明
        save_location = QLabel('📁 文档将保存到：桌面/筋斗云_timestamp.docx')
        save_location.setStyleSheet("""
            font-size: 26px;
            color: #64748b;
            font-weight: 500;
        """)
        
        # 添加到布局
        step3_layout.addWidget(step3_title)
        step3_layout.addLayout(button_layout)
        step3_layout.addWidget(self.status_label)
        step3_layout.addWidget(save_location)
        
        parent_layout.addWidget(step3_frame)

    def _create_bottom_area(self, parent_layout):
        """创建底部信息区域"""
        # 创建底部信息区域（版本信息）
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_frame.setStyleSheet("""
            QFrame#infoFrame {
                background-color: #f8fafc;
                border-top: 1px solid #e2e8f0;
                border-radius: 0px;
                padding: 15px 0px 5px 0px;
                margin: 10px 0px 0px 0px;
            }
        """)
        
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(5)
        info_layout.setContentsMargins(25, 15, 25, 5)
        
        # 版本过期时间
        self.expiration_label = QLabel()
        self.expiration_label.setStyleSheet("""
            font-size: 24px;
            color: #dc2626;
            font-weight: 600;
        """)
        self.expiration_label.setAlignment(Qt.AlignCenter)
        self.expiration_label.setText(get_expiration_message())
        
        # 测试版本说明
        self.test_version_label = QLabel()
        self.test_version_label.setStyleSheet("""
            font-size: 22px;
            color: #991b1b;
            font-style: italic;
            line-height: 1.4;
        """)
        self.test_version_label.setAlignment(Qt.AlignCenter)
        self.test_version_label.setWordWrap(True)
        self.test_version_label.setText(get_test_version_message())
        
        info_layout.addWidget(self.expiration_label)
        info_layout.addWidget(self.test_version_label)
        
        parent_layout.addWidget(info_frame)
        
        # 创建底部反馈链接区域
        feedback_frame = QFrame()
        feedback_layout = QHBoxLayout(feedback_frame)
        feedback_layout.setContentsMargins(0, 2, 0, 5)
        
        # 添加弹簧使链接居中
        feedback_layout.addStretch()
        
        # 创建反馈与建议链接
        feedback_label = QLabel('<a href="https://wj.qq.com/s2/25048545/zf1s/">反馈与建议_点击此处</a>')
        feedback_label.setOpenExternalLinks(True)
        feedback_label.setStyleSheet("""
            font-size: 25px;
            color: #3b82f6;
            text-decoration: underline;
            padding: 10px;
        """)
        feedback_layout.addWidget(feedback_label)
        
        # 添加右侧弹簧
        feedback_layout.addStretch()
        
        # 将反馈区域添加到父布局（在tab区域之前）
        parent_layout.addWidget(feedback_frame)
        
        # 添加信息展示区域
        self.bottom_tabs = InfoTabWidget()
        parent_layout.addWidget(self.bottom_tabs)
                
    def _set_styles(self):
        """设置整体样式"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8fafc, stop:1 #f1f5f9);
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
            
            /* 添加QLabel全局样式，确保没有边框 */
            QLabel {
                border: none;
                background: transparent;
            }
            
            /* 主按钮样式 - 绿色 */
            QPushButton#generateButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #22c55e, stop:1 #16a34a);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 30px;
                font-weight: 600;
                min-height: 100px;
            }
            QPushButton#generateButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #16a34a, stop:1 #15803d);
            }
            QPushButton#generateButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #15803d, stop:1 #166534);
                padding: 13px 23px 11px 25px;
            }
            
            /* 次按钮样式 */
            QPushButton#clearButton {
                background: transparent;
                color: #617087;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 30px;
                font-weight: 500;
                min-height: 100px;
            }
            QPushButton#clearButton:hover {
                background: #ff7171;
                color: #1b1b1b;
            }
            QPushButton#clearButton:pressed {
                background: #a20000;
                color: #ffffff;
                padding: 13px 23px 11px 25px;
            }
            
            /* 复制按钮样式 */
            QPushButton#copyButton {
                background-color: #f8fafc;
                color: #475569;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 20px;
                font-weight: 500;
                min-height: 40px;
                min-width: 120px;
            }
            QPushButton#copyButton:hover {
                background-color: #f1f5f9;
                color: #334155;
                border-color: #cbd5e1;
            }
            QPushButton#copyButton:pressed {
                background-color: #e2e8f0;
                color: #1e293b;
            }
            
            /* 模板选择按钮样式 */
            QPushButton {
                background-color: #f8fafc;
                color: #475569;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 28px;
                font-weight: 600;
                min-height: 60px;
                min-width: 240px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #334155;
                border-color: #cbd5e1;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
                color: #1e293b;
            }
            QPushButton#selectedTemplate {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: 2px solid #2563eb;
            }
            QPushButton#selectedTemplate:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2563eb, stop:1 #1d4ed8);
            }
            QPushButton#selectedTemplate:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1d4ed8, stop:1 #1e40af);
            }
            
            /* 滚动条样式 */
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
    def _on_template_button_clicked(self, template):
        """处理模板按钮点击事件"""
        self.selected_template = template['id']
        template_name = self.layout_templates[template['id']]['name']
        template_desc = self.layout_templates[template['id']]['description']
        
        # 更新状态标签
        self.status_label.setText(f"状态：已选择{template_name}")
        
        # 更新描述标签
        self.template_desc_label.setText(template_desc)
        
        # 更新按钮样式
        for button in self.template_buttons:
            if button.property("template_id") == template['id']:
                button.setObjectName("selectedTemplate")
            else:
                button.setObjectName("")
        
        # 强制刷新样式
        self.setStyleSheet(self.styleSheet())
                
    def _copy_ai_command(self):
        """复制AI指令到剪贴板"""
        command_text = self.ai_command_input.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(command_text)
        
        # 显示复制成功提示
        self.copy_button.setText("✓ 已复制")
        # 1秒后恢复按钮文本
        QTimer.singleShot(1000, lambda: self.copy_button.setText("📋 一键复制"))
                
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
            output_filename = f'筋斗云_{timestamp}.docx'
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
        # 重置第一个按钮为选中状态
        for button in self.template_buttons:
            if button.property("template_id") == 'simple':
                button.setObjectName("selectedTemplate")
            else:
                button.setObjectName("")
        
        # 重置选择的模板为默认值
        self.selected_template = 'simple'
        
        # 重置描述为默认值
        self.template_desc_label.setText(self.layout_templates['simple']['description'])
        
        # 强制刷新样式
        self.setStyleSheet(self.styleSheet())