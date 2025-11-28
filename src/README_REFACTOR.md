# Pandoc GUI 重构说明

## 重构概述

原始的 `main.py` 文件超过68,000个字符，包含了所有功能，不利于维护和扩展。重构后，我们按照功能模块将代码拆分为多个文件，使代码更加模块化、可维护和可扩展。

## 重构后的目录结构

```
src/
├── main.py                 # 主程序入口，简化版
├── main_new.py             # 重构后的主程序入口
├── ui/                     # UI相关模块
│   ├── __init__.py
│   ├── main_window.py      # 主窗口UI
│   ├── format_config.py    # 排版配置对话框UI
│   └── widgets/            # 自定义UI组件
│       ├── __init__.py
│       ├── basic_text_widget.py    # 基础文本配置组件
│       ├── heading_widget.py       # 标题配置组件
│       ├── list_widget.py          # 列表配置组件
│       ├── reference_widget.py     # 引用配置组件
│       ├── layout_widget.py        # 布局配置组件
│       └── page_widget.py         # 页面配置组件
├── core/                   # 核心功能模块
│   ├── __init__.py
│   ├── pandoc_converter.py # Pandoc转换功能
│   ├── template_manager.py # 模板管理功能
│   └── config_manager.py   # 配置管理功能
├── utils/                  # 工具模块
│   ├── __init__.py
│   └── file_utils.py       # 文件操作工具
└── README_REFACTOR.md      # 本文件
```

## 重构的主要变化

### 1. 模块化拆分

- 将单一的 `FormatConfigDialog` 类拆分为多个独立的UI组件类
- 将核心业务逻辑移至 `core/` 目录下的专门模块
- 将通用工具函数移至 `utils/` 目录下的专门模块

### 2. 职责分离

- UI组件：只负责用户界面的创建和显示
- 核心模块：负责业务逻辑和数据处理
- 工具模块：提供通用的辅助函数

### 3. 简化主程序

- `main.py` 只保留应用程序入口和主窗口创建逻辑
- 原始 `main.py` 的大部分功能已移至其他模块

## 如何使用重构后的代码

1. 运行重构后的程序：
   ```bash
   cd src
   python main_new.py
   ```

2. 或者将 `main_new.py` 重命名为 `main.py` 替换原始文件：
   ```bash
   cd src
   mv main.py main_backup.py
   mv main_new.py main.py
   python main.py
   ```

## 重构的好处

1. **代码组织更清晰**：每个文件只负责特定功能
2. **更易维护**：修改特定功能只需关注相关文件
3. **提高代码复用性**：组件可以在不同地方复用
4. **便于测试**：小模块更容易进行单元测试
5. **团队协作更友好**：不同开发者可以专注于不同模块

## 兼容性说明

重构后的代码保持了与原始代码相同的用户界面和功能，用户不会感觉到明显的变化。主要的改进在于代码的组织和维护性。