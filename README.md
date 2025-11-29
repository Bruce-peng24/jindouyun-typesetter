# Pandoc-GUI

一个基于PyQt5的Pandoc图形界面工具，提供直观的文档格式转换功能和自定义排版模板管理。

## 项目概述

Pandoc-GUI是一个为Pandoc文档转换工具设计的图形界面，允许用户通过简单的点击操作完成复杂的文档格式转换，并支持自定义Word模板的应用。

### 主要特性

- **开箱即用**：已集成Python环境和Pandoc，无需额外安装
- **直观的图形界面**：基于PyQt5构建的现代化GUI，提供友好的用户体验
- **多格式文档转换**：支持Markdown、HTML、Word、PDF等常见格式的相互转换
- **自定义排版模板**：可创建、编辑和应用自定义Word模板，实现专业排版效果
- **详细的排版控制**：支持文本样式、标题格式、列表样式、页面布局等基本的排版参数
- **便捷的模板管理**：可导出当前配置为Word模板，或选择已有模板文件应用

## 技术栈

- **GUI框架**: PyQt5 5.15.11
- **核心引擎**: Pandoc 3.8.1 (已集成)
- **部署工具**: PyInstaller 6.4.0
- **运行环境**: Python 3.12.10 (64位，已集成)
- **其他依赖**: python-docx 1.2.0, ntplib 0.4.0 (已集成)

## 系统要求

- Windows 10/11 (64位)
- 无需安装Python或Pandoc，所有依赖已集成在应用程序中

## 使用指南

### 直接运行可执行文件

1. 下载并解压Pandoc-GUI应用程序包
2. 双击运行 `dist\\Pandoc-GUI.exe` 即可启动应用程序

### 从源代码运行

如果您有源代码并希望自行运行：

```bash
# 克隆或下载项目到本地
cd /path/to/Pandoc-GUI

# 安装依赖
pip install -r requirements.txt

# 运行源代码
python app_minimal_fixed.py
# 或使用传统入口
python src/main.py
```

### 基本工作流程

1. **打开应用程序**：运行Pandoc-GUI程序
2. **选择输入文件**：点击"选择文件"按钮选择要转换的文档
3. **配置排版样式**：
   - 点击"排版配置"按钮或菜单项，打开排版配置对话框
   - 在对话框中配置各种排版参数（字体、段落、页面等）
   - 可以点击"导出模板"按钮，将当前配置导出为Word模板文件
4. **应用模板**：使用"选择模板文件"功能选择之前导出的模板文件
5. **转换文档**：选择输出格式，点击"转换"按钮完成文档转换

### 未来计划功能

- **批量转换**：支持多个文件的批量处理
- **实时预览**：部分格式支持实时预览功能
- **版本检查**：自动记录使用的Pandoc版本，确保兼容性

### 排版配置选项

#### 基础文本与段落样式
- 段落格式（首行缩进、段前段后间距等）
- 正文样式（字体、大小、颜色等）
- 正文字符（中文、英文、数字的字体分别设置）
- 文本对齐方式

#### 标题与层级样式
- 标题1至标题9的格式设置
- 不同层级标题的字体、大小、间距等
- 标题编号样式
- 标题对齐方式

#### 列表样式
- 有序列表格式（编号样式、缩进等）
- 无序列表格式（项目符号样式、缩进等）
- 嵌套列表的缩进控制

#### 引用与交互元素样式
- 超链接样式（颜色、下划线等）
- 脚注格式（字体、大小等）
- 脚注引用文本样式

#### 布局与页面样式
- 页面设置（页边距、纸张大小、方向等）
- 页眉页脚设置
- 块文本样式
- 水平线格式

#### 表格与图片样式
- 表标题格式
- 表格样式（边框、对齐等）
- 图片说明格式

#### 高级排版选项
- 自定义样式应用
- 模板导入导出
- 样式预览功能

## 项目结构

```
Pandoc-GUI/
├── app_minimal_fixed.py  # 应用程序最小入口点（修复版本）
├── src/                  # 源代码目录
│   ├── main.py          # 应用程序入口
│   ├── README_REFACTOR.md # 模块化重构说明
│   ├── ui/              # 用户界面模块
│   │   ├── main_window.py    # 主窗口
│   │   ├── format_config.py  # 排版配置对话框
│   │   ├── about_dialog.py   # 关于对话框
│   │   └── widgets/          # 自定义UI组件
│   │       ├── basic_text_widget.py  # 基础文本与段落样式组件
│   │       ├── heading_widget.py     # 标题与层级样式组件
│   │       ├── layout_widget.py      # 布局样式组件
│   │       ├── list_widget.py        # 列表样式组件
│   │       ├── page_widget.py        # 页面设置组件
│   │       └── reference_widget.py   # 引用与交互元素样式组件
│   ├── core/             # 核心功能模块
│   │   ├── pandoc_converter.py # Pandoc转换功能
│   │   ├── template_manager.py  # 模板管理功能
│   │   ├── config_manager.py    # 配置管理功能
│   │   └── version_checker.py   # 版本检查功能
│   └── utils/            # 工具模块
│       └── file_utils.py  # 文件操作工具
├── assets/               # 资源文件
├── pandoc/               # Pandoc相关文件
├── dist/                 # 打包输出目录
├── build/                # PyInstaller构建文件
├── venv/                 # 虚拟环境
├── requirements.txt      # 项目依赖
├── README.md            # 本文件
├── BUILD_GUIDE.md       # 综合构建指南
├── auto_detect_deps.py  # 自动依赖检测脚本
├── rebuild_app.bat      # 重新打包脚本（包含自动优化）
├── Pandoc-GUI.spec      # PyInstaller配置文件
└── UPX_OPTIMIZATION.md  # UPX压缩优化说明
```

## 开发指南

### 重新打包应用程序

如需修改代码后重新打包应用程序，请参考 `BUILD_GUIDE.md` 中的详细说明，或使用以下快捷命令：

```bash
# 使用预设脚本打包（推荐，包含自动依赖优化）
rebuild_app.bat
```

#### 自动依赖优化

项目包含自动检测和优化系统，可以：
- 自动检测项目实际使用的PyQt5组件，只包含必要的部分
- 自动检测并排除未使用的Python标准库模块
- 应用优化的UPX压缩设置，减小最终exe文件体积

#### 手动打包（不推荐）

如需手动打包，可使用以下命令：

```bash
pyinstaller --onefile --windowed --name="Pandoc-GUI" --add-data "src;src" --collect-all PyQt5 --collect-all docx --collect-all python-docx --collect-all ntplib app_minimal_fixed.py
```

注意：手动打包不会应用依赖优化，生成的exe文件可能会较大。

### 模块化架构

项目采用模块化设计，将代码组织为以下主要部分：

- **核心模块 (core/)**：处理Pandoc转换、模板管理、配置管理等功能
- **UI模块 (ui/)**：负责用户界面，包括主窗口、对话框和各种配置组件
- **工具模块 (utils/)**：提供文件操作等辅助功能
- **UI组件 (ui/widgets/)**：模块化的UI组件，每个组件负责特定的排版配置

### 内置依赖说明

Pandoc-GUI应用程序已将以下组件内置，用户无需单独安装：

- **Python 3.12.10 运行环境**：通过PyInstaller打包，用户无需安装Python
- **Pandoc 3.8.1**：已集成在应用程序的pandoc目录中，自动识别并使用
- **所有Python依赖**：PyQt5、python-docx、ntplib等依赖包已打包到可执行文件中

### 部署说明

打包后的应用程序是一个独立的可执行文件，包含运行所需的所有组件：

```
dist/
└── Pandoc-GUI.exe         # 主可执行文件（内置所有依赖）
```

用户只需下载并运行Pandoc-GUI.exe即可使用全部功能，无需任何额外安装。

## 版本历史

### v0.1.1 (当前版本)
- 添加自动依赖检测和优化系统
- 优化UPX压缩设置，减小exe文件体积
- 合并文档，简化项目结构
- 修复批处理文件编码问题

### v0.1.0
- 初始版本发布
- 基本的文档格式转换功能
- 基于PyQt5的GUI界面
- 支持多种文档格式间的转换
- 提供基本的排版配置选项

## 常见问题

### Q: 程序启动时提示"无法找到Pandoc"
A: 应用程序已内置Pandoc，此提示可能是由于文件损坏或路径错误。请尝试重新下载完整的应用程序包。

### Q: 打包后的exe文件无法正常运行
A: 请参考 `BUILD_GUIDE.md` 中的常见问题解决方案，或尝试使用 `rebuild_app.bat` 脚本重新打包。

### Q: 打包后的exe文件太大？
A: 使用 `rebuild_app.bat` 脚本并选择"Y"启用自动依赖优化，这可以显著减小exe文件体积。更多优化细节请参考 `UPX_OPTIMIZATION.md`。

### Q: 排版配置未生效
A: 确保已正确选择模板文件，并且模板文件与目标输出格式兼容。

### Q: 需要安装Python或Pandoc吗？
A: 不需要。Pandoc-GUI是独立应用程序，已内置运行所需的所有组件，包括Python环境和Pandoc工具。

### Q: 如何确认程序使用的是内置的Pandoc？
A: 程序会自动在应用程序目录的pandoc子目录中查找pandoc.exe。您可以在"帮助"菜单中查看当前使用的Pandoc版本信息。

### Q: 如何从源代码运行最新版本？
A: 请使用 `app_minimal_fixed.py` 作为入口点，而不是 `src/main.py`，前者解决了路径检查和网络检查问题。

## 许可证

本项目的许可证信息请查看 `LICENSE` 文件。有关项目使用的第三方库的许可证信息，请查看 `ThirdPartyLicenses.md` 文件。

## 贡献

欢迎提交问题报告和功能请求。如果您想为项目做出贡献，请遵循以下步骤：

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request