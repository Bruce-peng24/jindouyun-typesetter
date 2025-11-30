"""
底部信息Tab控件
包含免责声明、服务协议、隐私政策等内容
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QTextEdit, QPushButton, QFrame, QSizePolicy, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class InfoTabWidget(QFrame):
    """低调的Tab式信息展示区域（不折叠）"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setObjectName("infoTabWidget")
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 设置固定高度和大小策略
        self.setFixedHeight(450)  # 增加高度以适应更大的字体
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(5)
        
        # 标题区域
        title_label = QLabel("Copyright © 2025 BrucePeng")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: 600; color: #4b5563;")
        
        # Tab控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("infoTabs")
        
        # 创建各个标签页
        self.create_about_tab()
        self.create_disclaimer_tab()
        self.create_service_agreement_tab()
        self.create_privacy_policy_tab()
        
        # 添加到主布局
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.tab_widget)
        
        # 设置样式
        self.set_styles()
        
    def create_disclaimer_tab(self):
        """创建免责声明标签页"""
        disclaimer_widget = QWidget()
        disclaimer_layout = QVBoxLayout(disclaimer_widget)
        
        disclaimer_text = QTextEdit()
        disclaimer_text.setReadOnly(True)
        disclaimer_text.setStyleSheet("font-size: 20px; line-height: 1.5;")
        disclaimer_text.setPlainText(
            "免责声明\n\n"
            "本软件（筋斗云排版）仅用于文档格式转换，不对用户提供的内容负责。\n\n"
            "用户使用本软件处理的内容应遵守相关法律法规，不得包含违法信息。\n\n"
            "开发者不对因使用本软件而产生的任何直接或间接损失承担责任。\n\n"
            "本软件按\"现状\"提供，不提供任何明示或暗示的担保。\n\n"
            "用户使用本软件即表示同意上述免责条款。"
        )
        
        disclaimer_layout.addWidget(disclaimer_text)
        self.tab_widget.addTab(disclaimer_widget, "免责声明")
        
    def create_service_agreement_tab(self):
        """创建服务协议标签页"""
        service_widget = QWidget()
        service_layout = QVBoxLayout(service_widget)
        
        service_text = QTextEdit()
        service_text.setReadOnly(True)
        service_text.setStyleSheet("font-size: 20px; line-height: 1.5;")
        service_text.setPlainText(
            "服务协议\n\n"
            "1. 服务内容\n"
            "筋斗云排版提供HTML到Word文档的格式转换服务。\n\n"
            "2. 用户责任\n"
            "用户应确保提供的内容不侵犯他人知识产权，不包含违法信息。\n\n"
            "3. 使用限制\n"
            "用户不得将本软件用于商业用途或大规模文档处理，除非获得明确授权。\n\n"
            "4. 知识产权\n"
            "本软件的知识产权归开发者所有，用户仅获得使用权。\n\n"
            "5. 协议修改\n"
            "开发者保留随时修改本协议的权利，更新后的协议将在软件中公布。\n\n"
            "6. 争议解决\n"
            "因使用本软件产生的争议，应通过友好协商解决。"
        )
        
        service_layout.addWidget(service_text)
        self.tab_widget.addTab(service_widget, "服务协议")
        
    def create_privacy_policy_tab(self):
        """创建隐私政策标签页"""
        privacy_widget = QWidget()
        privacy_layout = QVBoxLayout(privacy_widget)
        
        privacy_text = QTextEdit()
        privacy_text.setReadOnly(True)
        privacy_text.setStyleSheet("font-size: 20px; line-height: 1.5;")
        privacy_text.setPlainText(
            "隐私政策\n\n"
            "1. 信息收集\n"
            "筋斗云排版不会主动收集、存储或传输用户的任何个人数据。\n\n"
            "2. 数据处理\n"
            "用户提供的文档内容仅在本地进行处理，不会上传到任何服务器。\n\n"
            "3. 数据存储\n"
            "本软件不存储用户的文档内容，处理完成后生成的文件保存在用户指定的位置。\n\n"
            "4. 第三方服务\n"
            "本软件使用Pandoc进行文档转换，可能涉及第三方组件的数据处理。\n\n"
            "5. Cookies和追踪技术\n"
            "本软件不使用Cookies或任何网络追踪技术。\n\n"
            "6. 政策更新\n"
            "我们可能会不时更新本隐私政策，更新后的政策将在软件中公布。"
        )
        
        privacy_layout.addWidget(privacy_text)
        self.tab_widget.addTab(privacy_widget, "隐私政策")
        
    def set_styles(self):
        """设置样式 - 使用更低调的颜色和样式"""
        self.setStyleSheet("""
            QFrame#infoTabWidget {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                margin: 5px 0px;
            }
            
            QLabel#titleLabel {
                color: #6b7280;
                font-size: 14px;
                font-weight: 500;
                padding: 5px 0px;
                border-bottom: 1px solid #e5e7eb;
                margin-bottom: 5px;
            }
            
            QTabWidget#infoTabs::pane {
                border: 1px solid #e5e7eb;
                background-color: #ffffff;
                border-radius: 4px;
                top: -1px;
            }
            
            QTabBar::tab {
                background-color: #f3f4f6;
                border: 1px solid #e5e7eb;
                padding: 8px 16px;
                margin-right: 2px;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 20px;
                font-weight: 600;
                color: #6b7280;
                min-width: 140px;
                max-width: 140px;
            }
            
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 1px solid #ffffff;
                color: #4b5563;
                font-weight: 500;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #e5e7eb;
                color: #4b5563;
            }
            
            QTextEdit {
                border: none;
                background-color: #ffffff;
                color: #4b5563;
                font-size: 20px;
                line-height: 1.5;
                padding: 12px;
            }
        """)
    
    def create_about_tab(self):
        """创建关于与鸣谢标签页"""
        about_widget = QWidget()
        about_layout = QVBoxLayout(about_widget)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setStyleSheet("font-size: 20px; line-height: 1.5;")
        about_text.setHtml("""
            <h3>关于与鸣谢</h3>
            <p><b>筋斗云排版</b>是一款专为AI生成内容设计的智能排版工具，一键即可将AI内容转换为多种精美排版的Word文档，让您告别繁琐的手动调整。</p>
            
            <h4>版本信息</h4>
            <p>当前版本: 0.1.0 (首个版本)</p>
            
            <h4>核心特色</h4>
            <ul>
                <li>🚀 三步完成：复制指令 → 获取HTML → 生成文档</li>
                <li>🎨 四种模板：简洁通用、学术论文、商务文档、技术文档</li>
                <li>🤖 AI友好：内置专业提示词，让AI生成标准HTML内容</li>
                <li>💡 开箱即用：无需安装Python或Pandoc，所有依赖已集成</li>
            </ul>
            
            <h4>技术栈</h4>
            <ul>
                <li><b>PyQt5</b> - 图形界面框架 (GPL v3)</li>
                <li><b>Pandoc</b> - 核心文档转换引擎 (GPL v2+)</li>
                <li><b>PyInstaller</b> - 应用程序打包工具</li>
                <li><b>Python 3.12.10</b> - 运行环境 (已集成)</li>
            </ul>
            
            <h4>开源项目</h4>
            <p>本项目已开源在GitHub上，欢迎访问、Fork和贡献代码：</p>
            <p><a href="https://github.com/Bruce-peng24/Pandoc-GUI">https://github.com/Bruce-peng24/Pandoc-GUI</a></p>
            
            <h4>鸣谢</h4>
            <p>感谢所有为开源社区做出贡献的开发者，特别是Pandoc和PyQt5项目的维护者。</p>
            <p>本软件采用GPL v3许可证发布，详情请查看LICENSE文件。</p>
        """)
        
        about_layout.addWidget(about_text)
        self.tab_widget.addTab(about_widget, "关于与鸣谢")
    
