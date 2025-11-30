"""
关于与鸣谢对话框
包含应用程序信息、版本和开源协议声明
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QTabWidget, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon

# 添加当前目录到路径，以便导入模块
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AboutDialog(QDialog):
    """关于与鸣谢对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于与鸣谢")
        self.setModal(True)
        self.resize(1000, 700)
        
        # 获取项目根目录
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 创建选项卡
        tabs = QTabWidget()
        
        # 关于选项卡
        about_tab = self.create_about_tab()
        tabs.addTab(about_tab, "关于")
        
        # 功能优势选项卡
        features_tab = self.create_features_tab()
        tabs.addTab(features_tab, "功能优势")
        
        # 鸣谢选项卡
        credits_tab = self.create_credits_tab()
        tabs.addTab(credits_tab, "鸣谢")
        
        # 常见问题选项卡
        faq_tab = self.create_faq_tab()
        tabs.addTab(faq_tab, "常见问题")
        
        # 免责声明选项卡
        disclaimer_tab = self.create_disclaimer_tab()
        tabs.addTab(disclaimer_tab, "免责声明")
        
        # 服务协议选项卡
        service_terms_tab = self.create_service_terms_tab()
        tabs.addTab(service_terms_tab, "服务协议")
        
        # 隐私政策选项卡
        privacy_policy_tab = self.create_privacy_policy_tab()
        tabs.addTab(privacy_policy_tab, "隐私政策")
        
        # 许可协议选项卡
        license_tab = self.create_license_tab()
        tabs.addTab(license_tab, "许可协议")
        
        layout.addWidget(tabs)
        
        # 添加反馈链接区域
        feedback_layout = QHBoxLayout()
        feedback_label = QLabel("反馈与建议: ")
        feedback_link = QLabel("<a href='https://wj.qq.com/s2/25048545/zf1s/'>点击此处提供反馈</a>")
        feedback_link.setOpenExternalLinks(True)  # 启用外部链接点击
        feedback_layout.addWidget(feedback_label)
        feedback_layout.addWidget(feedback_link)
        feedback_layout.addStretch()
        
        layout.addLayout(feedback_layout)
        
        # 添加关闭按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
    def create_about_tab(self):
        """创建关于选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 应用图标和名称
        header_layout = QHBoxLayout()
        
        # 尝试加载应用图标（如果有的话）
        icon_path = os.path.join(self.root_dir, "assets", "icon.png")
        if os.path.exists(icon_path):
            icon_label = QLabel()
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
            header_layout.addWidget(icon_label)
        else:
            # 如果没有图标，添加一个占位符
            icon_label = QLabel("📄")
            icon_label.setStyleSheet("font-size: 48px;")
            header_layout.addWidget(icon_label)
        
        # 应用名称和版本信息
        info_layout = QVBoxLayout()
        
        app_name = QLabel("Pandoc GUI")
        app_name.setFont(QFont("Arial", 16, QFont.Bold))
        info_layout.addWidget(app_name)
        
        version = QLabel("版本: 0.1.1")
        info_layout.addWidget(version)
        
        description = QLabel("一个简单易用的Pandoc图形界面工具")
        description.setWordWrap(True)
        info_layout.addWidget(description)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # 应用说明
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml("""
            <h3>应用简介</h3>
            <p>Pandoc GUI 是一个基于 Pandoc 的文档转换工具的图形用户界面。</p>
            <p>它提供了一个简单易用的界面，让用户无需记忆复杂的命令行参数即可轻松地转换文档格式。</p>
            
            <h3>主要功能</h3>
            <ul>
                <li>支持多种文档格式之间的转换，包括 Markdown、Word、PDF、HTML 等</li>
                <li>提供直观的图形用户界面</li>
                <li>支持自定义模板</li>
                <li>支持文档排版配置</li>
            </ul>
            
            <h3>技术支持</h3>
            <p>如需技术支持或有任何问题，请参考文档或联系开发者。</p>
            
            <h3>开源项目</h3>
            <p>本项目已开源在GitHub上，欢迎访问、Fork和贡献代码：</p>
            <p><a href="https://github.com/Bruce-peng24/Pandoc-GUI">https://github.com/Bruce-peng24/Pandoc-GUI</a></p>

        """)
        
        layout.addWidget(about_text)
        
        return widget
    
    def create_credits_tab(self):
        """创建鸣谢选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        credits_text = QTextEdit()
        credits_text.setReadOnly(True)
        
        # 尝试读取第三方开源协议文件
        third_party_licenses_path = os.path.join(self.root_dir, "dist", "第三方开源协议.txt")
        if os.path.exists(third_party_licenses_path):
            with open(third_party_licenses_path, 'r', encoding='utf-8') as f:
                content = f.read()
                credits_text.setPlainText(content)
        else:
            # 如果文件不存在，使用默认内容
            credits_text.setHtml("""
                <h2>第三方开源组件协议声明</h2>
                <p>本软件使用了以下开源组件，特此声明其版权及许可信息：</p>
                
                <h3>1. Pandoc (核心组件)</h3>
                <p>授权协议：GPL v2+</p>
                <p>版权所有者：John MacFarlane</p>
                <p>官方网址：<a href="https://pandoc.org/">https://pandoc.org/</a></p>
                <p>要求：必须保留版权声明和授权信息</p>
                
                <h3>2. PyQt5</h3>
                <p>授权协议：GPL v3</p>
                <p>版权所有者：Riverbank Computing Limited</p>
                <p>官方网址：<a href="https://www.riverbankcomputing.com/software/pyqt/">https://www.riverbankcomputing.com/software/pyqt/</a></p>
                
                <h3>版权声明</h3>
                <p>本软件是依据上述开源组件的许可协议分发的。</p>
                <p>这些组件的版权和许可协议的完整文本可以在各自的官方网站上找到。</p>
            """)
        
        layout.addWidget(credits_text)
        
        return widget
    
    def create_features_tab(self):
        """创建功能优势选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        features_text = QTextEdit()
        features_text.setReadOnly(True)
        features_text.setHtml("""
            <h2>功能优势</h2>
            <p>Pandoc GUI 提供了许多优势，让您能够轻松高效地进行文档格式转换：</p>
            
            <h3>直观的用户界面</h3>
            <ul>
                <li>简洁现代的界面设计，无需记忆复杂的命令行参数</li>
                <li>可视化的操作流程，一目了然的功能布局</li>
                <li>支持拖放文件，操作更加便捷</li>
            </ul>
            
            <h3>强大的转换能力</h3>
            <ul>
                <li>支持多种常见文档格式之间的相互转换</li>
                <li>基于 Pandoc 强大的转换引擎，保证转换质量</li>
                <li>支持批量转换，提高工作效率</li>
            </ul>
            
            <h3>自定义配置</h3>
            <ul>
                <li>提供丰富的转换选项，满足不同需求</li>
                <li>支持自定义模板，个性化输出样式</li>
                <li>可保存常用配置，一键应用预设</li>
            </ul>
            
            <h3>实用功能</h3>
            <ul>
                <li>实时预览转换结果，减少试错成本</li>
                <li>转换历史记录，方便追溯和重复使用</li>
                <li>支持元数据编辑，增强文档信息管理</li>
            </ul>
            
            <h3>性能优化</h3>
            <ul>
                <li>优化的转换流程，提高转换速度</li>
                <li>低内存占用，适合各种配置的计算机</li>
                <li>后台处理，不影响其他操作</li>
            </ul>
            
            <h3>跨平台兼容</h3>
            <ul>
                <li>支持 Windows、macOS 和 Linux 系统</li>
                <li>统一的用户体验，不同系统下操作一致</li>
                <li>适配不同分辨率和屏幕尺寸</li>
            </ul>
            
            <h3>开放生态</h3>
            <ul>
                <li>开源软件，代码透明，安全性高</li>
                <li>支持插件扩展，功能可持续增强</li>
                <li>活跃的社区支持，问题及时解决</li>
            </ul>
        """)
        
        layout.addWidget(features_text)
        return widget
    
    def create_faq_tab(self):
        """创建常见问题选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        faq_text = QTextEdit()
        faq_text.setReadOnly(True)
        faq_text.setHtml("""
            <h2>常见问题</h2>
            <p>以下是用户在使用 Pandoc GUI 过程中可能遇到的一些常见问题及其解答：</p>
            
            <h3>Q: Pandoc GUI 是否需要单独安装 Pandoc？</h3>
            <p>A: Pandoc GUI 内置了 Pandoc 工具，通常不需要额外安装。但如果遇到转换问题，可能需要从官方网站安装最新版本的 Pandoc。</p>
            
            <h3>Q: 支持哪些文档格式的转换？</h3>
            <p>A: Pandoc GUI 支持多种常见格式，包括但不限于：Markdown、HTML、Word(docx)、PDF、LaTeX、RTF、EPUB 等。您可以在软件的格式选择下拉菜单中查看所有支持的格式。</p>
            
            <h3>Q: 转换大型文件时程序没有响应怎么办？</h3>
            <p>A: 大型文件转换可能需要较长时间，请耐心等待。如果长时间无响应，可以尝试：1) 检查文件是否损坏；2) 将大文件拆分成小文件；3) 关闭其他占用系统资源的程序。</p>
            
            <h3>Q: 如何自定义输出的文档样式？</h3>
            <p>A: 您可以通过"高级选项"中的模板设置来自定义输出样式，或者使用自定义CSS文件。也可以保存常用的模板配置，方便下次使用。</p>
            
            <h3>Q: 转换后的中文内容显示异常怎么办？</h3>
            <p>A: 请确保：1) 源文件的编码格式正确；2) 在转换选项中指定了正确的字体和编码；3) 目标格式支持所使用的中文字体。</p>
            
            <h3>Q: 如何批量转换多个文件？</h3>
            <p>A: 您可以使用"批量转换"功能，选择多个文件或整个文件夹，设置统一的转换选项后一次性完成所有文件的转换。</p>
            
            <h3>Q: 转换 PDF 时出现错误怎么办？</h3>
            <p>A: PDF 转换依赖于 LaTeX 引擎。请确保系统已安装完整的 LaTeX 环境（如 MiKTeX、TeX Live 等）。对于中文 PDF，可能需要安装 CTeX 宏包。</p>
            
            <h3>Q: 软件是否支持命令行调用？</h3>
            <p>A: 当前版本主要提供图形界面功能，但可以在高级设置中查看对应的 Pandoc 命令，以便在其他环境中使用。</p>
            
            <h3>Q: 如何报告软件缺陷或提出功能建议？</h3>
            <p>A: 您可以通过"反馈与建议"链接提交问题报告或功能请求，我们会尽快处理并回复。</p>
            
            <h3>Q: 软件是否收费？</h3>
            <p>A: Pandoc GUI 是开源软件，基于 GNU GPL v3 协议发布，完全免费使用。您可以根据协议自由使用、修改和分发。</p>
        """)
        
        layout.addWidget(faq_text)
        return widget
    
    def create_disclaimer_tab(self):
        """创建免责声明选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        disclaimer_text = QTextEdit()
        disclaimer_text.setReadOnly(True)
        disclaimer_text.setHtml("""
            <h2>免责声明</h2>
            <p>欢迎使用 Pandoc GUI 软件。在使用本软件前，请仔细阅读以下免责声明：</p>
            
            <h3>软件使用风险</h3>
            <p>本软件按"现状"提供，不提供任何明示或暗示的保证。用户使用本软件的风险由用户自行承担。</p>
            
            <h3>功能限制</h3>
            <p>本软件基于 Pandoc 工具开发，其功能受限于 Pandoc 本身的特性。对于文档转换结果的准确性和完整性，开发者不承担任何责任。</p>
            
            <h3>数据安全</h3>
            <p>本软件不会主动收集、上传或传输用户文档内容，但不对因用户计算机环境、第三方软件等原因导致的数据泄露承担责任。</p>
            
            <h3>法律责任</h3>
            <p>因使用本软件而导致的任何直接或间接损失，开发者不承担法律责任。用户在使用本软件处理重要文档前，建议先备份原始文件。</p>
            
            <h3>第三方服务</h3>
            <p>本软件可能包含指向第三方网站或服务的链接。这些链接仅为方便用户而提供，不代表开发者对其内容或服务的认可。使用第三方服务的风险由用户自行承担。</p>
            
            <h3>免责声明的变更</h3>
            <p>开发者保留随时修改本免责声明的权利，恕不另行通知。继续使用本软件即表示您接受修改后的声明。</p>
        """)
        
        layout.addWidget(disclaimer_text)
        return widget
    
    def create_service_terms_tab(self):
        """创建服务协议选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        service_text = QTextEdit()
        service_text.setReadOnly(True)
        service_text.setHtml("""
            <h2>服务协议</h2>
            <p>欢迎使用 Pandoc GUI 软件。本协议是您与开发者之间关于使用本软件的法律协议。</p>
            
            <h3>协议接受</h3>
            <p>一旦您下载、安装或使用本软件，即表示您已阅读、理解并同意接受本协议的所有条款。</p>
            
            <h3>软件授权</h3>
            <p>本软件基于 GNU GPL v3 许可协议发布，您可以自由使用、修改和分发，但需遵守 GPL 协议的相关规定。</p>
            
            <h3>使用限制</h3>
            <p>您不得对本软件进行逆向工程、反编译或试图获取源代码（除非 GPL 协议明确允许）。</p>
            <p>您不得将本软件用于任何非法目的，或违反任何适用的法律法规。</p>
            
            <h3>知识产权</h3>
            <p>本软件及其所有内容的知识产权归开发者或原始权利人所有。</p>
            <p>本软件使用的第三方组件的知识产权归其各自权利人所有。</p>
            
            <h3>更新与维护</h3>
            <p>开发者可能不定期提供软件更新。您有权选择是否安装这些更新。</p>
            <p>开发者不承诺提供持续的技术支持或维护服务。</p>
            
            <h3>协议终止</h3>
            <p>如果您违反本协议的任何条款，开发者有权立即终止您使用本软件的权利。</p>
            <p>终止使用后，您应立即卸载并销毁本软件的所有副本。</p>
            
            <h3>协议变更</h3>
            <p>开发者保留随时修改本协议的权利，恕不另行通知。继续使用本软件即表示您接受修改后的协议。</p>
        """)
        
        layout.addWidget(service_text)
        return widget
    
    def create_privacy_policy_tab(self):
        """创建隐私政策选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        privacy_text = QTextEdit()
        privacy_text.setReadOnly(True)
        privacy_text.setHtml("""
            <h2>隐私政策</h2>
            <p>我们非常重视您的隐私。本政策详细说明了 Pandoc GUI 软件如何收集、使用和保护您的信息。</p>
            
            <h3>信息收集</h3>
            <p>本软件为本地应用程序，不会主动收集、存储或传输您的个人信息。</p>
            <p>本软件不会访问您的文档内容，除非您明确选择打开文件进行转换。</p>
            
            <h3>本地存储</h3>
            <p>本软件可能需要在您的计算机上存储配置信息和最近使用的文件路径，以提升用户体验。</p>
            <p>这些信息仅保存在本地，不会被上传到任何服务器。</p>
            
            <h3>第三方服务</h3>
            <p>本软件本身不包含需要联网的功能，但可能使用系统默认浏览器打开外部链接（如本帮助文档）。</p>
            <p>对于您通过本软件访问的第三方网站或服务，其隐私保护政策适用于这些第三方服务。</p>
            
            <h3>数据安全</h3>
            <p>我们采取合理的技术措施保护存储在本地的软件配置信息，但不能保证绝对安全。</p>
            <p>建议您定期备份重要文档，并妥善保管您的计算机。</p>
            
            <h3>Cookie 和跟踪技术</h3>
            <p>本软件不使用 Cookie 或任何类似的跟踪技术。</p>
            
            <h3>儿童隐私</h3>
            <p>本软件不面向儿童设计，也不会故意收集儿童的个人信息。</p>
            
            <h3>隐私政策的变更</h3>
            <p>我们可能会不时更新本隐私政策。任何重大变更都会通过软件更新通知用户。</p>
            <p>继续使用本软件即表示您接受修改后的隐私政策。</p>
            
            <h3>联系方式</h3>
            <p>如果您对本隐私政策有任何疑问或建议，请通过"反馈与建议"链接联系我们。</p>
        """)
        
        layout.addWidget(privacy_text)
        return widget
    
    def create_license_tab(self):
        """创建许可协议选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 创建可滚动的文本区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        license_text = QTextEdit()
        license_text.setReadOnly(True)
        
        # 尝试读取LICENSE文件
        license_path = os.path.join(self.root_dir, "LICENSE")
        if os.path.exists(license_path):
            with open(license_path, 'r', encoding='utf-8') as f:
                content = f.read()
                license_text.setPlainText(content)
        else:
            # 如果文件不存在，使用默认内容
            license_text.setHtml("""
                <h2>GNU通用公共许可证</h2>
                <p>本程序是自由软件：您可以根据自由软件基金会发布的GNU通用公共许可证条款（第3版或更新版本）重新分发和/或修改它。</p>
                <p>分发本程序是希望它能发挥作用，但没有任何担保；甚至没有对适销性或特定用途适用性的暗示担保。有关详细信息，请参阅GNU通用公共许可证。</p>
                <p>您应该随本程序收到一份GNU通用公共许可证。如果没有，请参阅<a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses/</a>。</p>
            """)
        
        scroll_area.setWidget(license_text)
        layout.addWidget(scroll_area)
        
        return widget