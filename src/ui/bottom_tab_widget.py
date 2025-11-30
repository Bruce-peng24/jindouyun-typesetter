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
        self.create_features_tab()
        self.create_faq_tab()
        self.create_changelog_tab()
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
            <p><b>筋斗云排版</b>是一个基于Pandoc的文档转换工具的图形用户界面。</p>
            
            <h4>版本信息</h4>
            <p>当前版本: 0.1.0 (首个版本)</p>
            
            <h4>功能简介</h4>
            <p>提供简单易用的界面，让用户无需记忆复杂的命令行参数即可轻松地转换文档格式。</p>
            
            <h4>鸣谢</h4>
            <p>本软件使用了以下开源组件：</p>
            <ul>
                <li><b>Pandoc</b> - 核心文档转换引擎 (GPL v2+)</li>
                <li><b>PyQt5</b> - 图形界面框架 (GPL v3)</li>
            </ul>
            
            <h4>开源项目</h4>
            <p>本项目已开源在GitHub上，欢迎访问、Fork和贡献代码：</p>
            <p><a href="https://github.com/Bruce-peng24/Pandoc-GUI">https://github.com/Bruce-peng24/Pandoc-GUI</a></p>
        """)
        
        about_layout.addWidget(about_text)
        self.tab_widget.addTab(about_widget, "关于与鸣谢")
    
    def create_features_tab(self):
        """创建功能优势标签页"""
        features_widget = QWidget()
        features_layout = QVBoxLayout(features_widget)
        
        features_text = QTextEdit()
        features_text.setReadOnly(True)
        features_text.setStyleSheet("font-size: 20px; line-height: 1.5;")
        features_text.setHtml("""
            <h3>功能优势</h3>
            <p>筋斗云排版提供了许多优势，让您能够轻松高效地进行文档格式转换：</p>
            
            <h4>直观的用户界面</h4>
            <ul>
                <li>简洁现代的界面设计，无需记忆复杂的命令行参数</li>
                <li>可视化的操作流程，一目了然的功能布局</li>
                <li>支持拖放文件，操作更加便捷</li>
            </ul>
            
            <h4>强大的转换能力</h4>
            <ul>
                <li>支持多种常见文档格式之间的相互转换</li>
                <li>基于Pandoc强大的转换引擎，保证转换质量</li>
                <li>支持批量转换，提高工作效率</li>
            </ul>
            
            <h4>自定义配置</h4>
            <ul>
                <li>提供丰富的转换选项，满足不同需求</li>
                <li>支持自定义模板，个性化输出样式</li>
                <li>可保存常用配置，一键应用预设</li>
            </ul>
            
            <h4>实用功能</h4>
            <ul>
                <li>实时预览转换结果，减少试错成本</li>
                <li>转换历史记录，方便追溯和重复使用</li>
                <li>支持元数据编辑，增强文档信息管理</li>
            </ul>
            
            <h4>性能优化</h4>
            <ul>
                <li>优化的转换流程，提高转换速度</li>
                <li>低内存占用，适合各种配置的计算机</li>
                <li>后台处理，不影响其他操作</li>
            </ul>
            
            <h4>跨平台兼容</h4>
            <ul>
                <li>支持Windows、macOS和Linux系统</li>
                <li>统一的用户体验，不同系统下操作一致</li>
                <li>适配不同分辨率和屏幕尺寸</li>
            </ul>
        """)
        
        features_layout.addWidget(features_text)
        self.tab_widget.addTab(features_widget, "功能优势")
    
    def create_faq_tab(self):
        """创建常见问题标签页"""
        faq_widget = QWidget()
        faq_layout = QVBoxLayout(faq_widget)
        
        faq_text = QTextEdit()
        faq_text.setReadOnly(True)
        faq_text.setStyleSheet("font-size: 20px; line-height: 1.5;")
        faq_text.setHtml("""
            <h3>常见问题</h3>
            <p>以下是用户在使用筋斗云排版过程中可能遇到的一些常见问题及其解答：</p>
            
            <h4>Q: 软件是否需要单独安装Pandoc？</h4>
            <p>A: 筋斗云排版内置了Pandoc工具，通常不需要额外安装。但如果遇到转换问题，可能需要从官方网站安装最新版本的Pandoc。</p>
            
            <h4>Q: 支持哪些文档格式的转换？</h4>
            <p>A: 筋斗云排版支持多种常见格式，包括但不限于：Markdown、HTML、Word(docx)、PDF、LaTeX、RTF、EPUB等。您可以在软件的格式选择下拉菜单中查看所有支持的格式。</p>
            
            <h4>Q: 转换大型文件时程序没有响应怎么办？</h4>
            <p>A: 大型文件转换可能需要较长时间，请耐心等待。如果长时间无响应，可以尝试：1)检查文件是否损坏；2)将大文件拆分成小文件；3)关闭其他占用系统资源的程序。</p>
            
            <h4>Q: 如何自定义输出的文档样式？</h4>
            <p>A: 您可以通过"高级选项"中的模板设置来自定义输出样式，或者使用自定义CSS文件。也可以保存常用的模板配置，方便下次使用。</p>
            
            <h4>Q: 转换后的中文内容显示异常怎么办？</h4>
            <p>A: 请确保：1)源文件的编码格式正确；2)在转换选项中指定了正确的字体和编码；3)目标格式支持所使用的中文字体。</p>
            
            <h4>Q: 软件是否收费？</h4>
            <p>A: 筋斗云排版是开源软件，基于GNU GPL v3协议发布，完全免费使用。您可以根据协议自由使用、修改和分发。</p>
        """)
        
        faq_layout.addWidget(faq_text)
        self.tab_widget.addTab(faq_widget, "常见问题")
    
    def create_changelog_tab(self):
        """创建更新日志标签页"""
        changelog_widget = QWidget()
        changelog_layout = QVBoxLayout(changelog_widget)
        
        changelog_text = QTextEdit()
        changelog_text.setReadOnly(True)
        changelog_text.setStyleSheet("font-size: 20px; line-height: 1.5;")
        changelog_text.setHtml("""
            <h3>更新日志</h3>
            
            <h4>版本 0.1.0 (首次发布)</h4>
            <p><b>发布日期:</b> 2025-11-29</p>
            
            <h5>新功能</h5>
            <ul>
                <li>初始版本发布</li>
                <li>基于PyQt5的图形用户界面</li>
                <li>集成Pandoc文档转换引擎</li>
                <li>支持多种文档格式之间的转换</li>
                <li>直观的文件拖放操作</li>
                <li>转换进度显示</li>
                <li>自定义转换选项</li>
                <li>批量文件转换功能</li>
            </ul>
            
            <h5>用户界面</h5>
            <ul>
                <li>简洁现代的设计风格</li>
                <li>底部信息展示区域</li>
                <li>关于与鸣谢、功能优势、常见问题等帮助信息</li>
                <li>响应式布局设计</li>
            </ul>
            
            <h5>技术特性</h5>
            <ul>
                <li>跨平台支持(Windows、macOS、Linux)</li>
                <li>本地文档处理，无需网络连接</li>
                <li>版本检查机制</li>
                <li>错误处理和用户友好提示</li>
            </ul>
            
            <h5>未来计划</h5>
            <ul>
                <li>添加更多文档格式支持</li>
                <li>增强自定义模板功能</li>
                <li>添加转换历史记录</li>
                <li>改进用户界面交互体验</li>
                <li>添加插件系统支持</li>
            </ul>
        """)
        
        changelog_layout.addWidget(changelog_text)
        self.tab_widget.addTab(changelog_widget, "更新日志")