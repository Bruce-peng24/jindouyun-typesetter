# jindouyun-typesetter (金豆云排版工具)

一个基于 PyQt5 和 Pandoc 的文档排版工具，专为 AI 生成内容优化，提供简洁易用的界面和多种专业排版方案。

## 项目概述

此项目在原 [Pandoc-GUI](README-old.md) 的基础上进行了简化和重构，专注于解决 AI 生成内容的排版问题。通过三步操作流程，用户可以快速将 HTML 内容转换为格式精美的 Word 文档。

### 主要特性

- **简洁三步操作**：粘贴 HTML → 选择方案 → 导出文档
- **AI 内容友好**：专为 AI 生成内容优化，自动清理杂乱标签
- **四种预设方案**：简洁通用、学术论文、商务文档、技术文档
- **开箱即用**：已集成 Python 环境和 Pandoc，无需额外安装
- **轻量高效**：基于成熟 Pandoc 引擎，转换速度快，质量高

### 界面设计（三步操作）

1. **粘贴HTML区域** - 大文本框，支持粘贴HTML内容
2. **排版方案选择** - 预设4种常用的美观的排版模板
3. **导出按钮** - 一键生成docx文档

### 预设排版方案

- **简洁通用**：日常办公文档
- **学术论文**：适合论文、报告格式
- **商务文档**：企业报告、方案文档
- **技术文档**：API文档、技术手册

## 系统要求

- Windows 10/11 (64位)
- 无需安装Python或Pandoc，所有依赖已集成在应用程序中

## 安装与使用

### 直接运行可执行文件

1. 下载并解压 jindouyun-typesetter 应用程序包
2. 双击运行 `dist/jindouyun-typesetter.exe` 即可启动应用程序

### 从源代码运行

如果您有源代码并希望自行运行：

```bash
# 克隆或下载项目到本地
cd /path/to/jindouyun-typesetter

# 安装依赖
pip install -r requirements.txt

# 运行源代码
python app_minimal_fixed.py
```

### 基本工作流程

1. **打开应用程序**：运行 jindouyun-typesetter 程序
2. **粘贴HTML内容**：将AI生成或编辑好的HTML内容粘贴到文本区域
3. **选择排版方案**：根据文档用途选择合适的预设排版方案
4. **导出文档**：点击导出按钮，生成格式精美的Word文档

## 项目结构

```
jindouyun-typesetter/
├── app_minimal_fixed.py     # 应用程序入口点
├── src/                     # 源代码目录
│   ├── core/                # 核心功能模块
│   │   ├── enhanced_pandoc_converter.py  # 增强的Pandoc转换功能
│   │   ├── pandoc_converter.py           # 基础Pandoc转换功能
│   │   └── template_manager.py           # 模板管理功能
│   ├── ui/                  # 用户界面模块
│   │   ├── main_window.py   # 主窗口
│   │   ├── format_config.py # 排版配置对话框
│   │   └── ...
│   └── utils/               # 工具模块
├── resource/                # 资源文件
├── pandoc/                  # Pandoc相关文件
├── dist/                    # 打包输出目录
├── build/                   # PyInstaller构建文件
├── requirements.txt         # 项目依赖
├── README.md               # 本文件
├── README-old.md           # 原项目概述
├── BUILD_GUIDE.md          # 综合构建指南
└── rebuild_app.bat         # 重新打包脚本
```

## 更新日志

### 版本 0.1.0 (2025-11-30)
- 初始版本发布
- 实现基本的HTML到Word文档转换功能
- 提供4种预设排版方案
- 优化用户界面，简化操作流程



## 技术栈

- **GUI框架**: PyQt5 5.15.11
- **核心引擎**: Pandoc 3.8.1 (已集成)
- **部署工具**: PyInstaller 6.4.0
- **运行环境**: Python 3.12.10 (64位，已集成)
- **其他依赖**: ntplib 0.4.0 (已集成)

## 开发指南

### 重新打包应用程序

如需修改代码后重新打包应用程序，请参考 `BUILD_GUIDE.md` 中的详细说明，或使用以下快捷命令：

```bash
# 使用预设脚本打包（推荐，包含自动依赖优化）
rebuild_app.bat
```

### 手动打包

如需手动打包，可使用以下命令：

```bash
pyinstaller --onefile --windowed --name="jindouyun-typesetter" --add-data "src;src" --collect-all PyQt5 --collect-all ntplib app_minimal_fixed.py
```

## 常见问题

### Q: 程序启动时提示"无法找到Pandoc"
A: 应用程序已内置Pandoc，此提示可能是由于文件损坏或路径错误。请尝试重新下载完整的应用程序包。

### Q: 排版后的文档格式不正确
A: 确保您粘贴的是有效的HTML内容，而不是纯文本或其他格式。AI生成的内容可能需要简单清理以确保HTML标签正确。

### Q: 如何提高文档排版质量
A: 尝试使用更结构化的HTML输入，确保正确使用标题、列表、段落等标签。第二阶段将提供HTML自动清理功能。

### Q: 需要安装Python或Pandoc吗？
A: 不需要。jindouyun-typesetter是独立应用程序，已内置运行所需的所有组件，包括Python环境和Pandoc工具。

## 许可证

本项目的许可证信息请查看 `LICENSE` 文件。有关项目使用的第三方库的许可证信息，请查看 `ThirdPartyLicenses.md` 文件。

## 贡献

欢迎提交问题报告和功能请求。如果您想为项目做出贡献，请遵循以下步骤：

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request