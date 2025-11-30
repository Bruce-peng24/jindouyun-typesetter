# Pandoc-GUI 构建指南

本指南介绍如何构建Pandoc-GUI应用程序，包括基本构建步骤和使用自动检测系统优化打包体积的方法。

## 项目路径可移植性

本项目设计为可以在任何位置运行，无需依赖特定绝对路径。所有构建脚本和配置文件都使用相对路径，这意味着：

1. 您可以将项目放在任何目录下（如 `D:\Projects\jindouyun-typesetter` 或 `C:\MyApps\jindouyun-typesetter`）
2. 任何人拉取代码后，无需修改任何路径即可直接构建
3. 唯一需要确认的是确保在项目根目录下运行 `rebuild_app.bat`

### 注意事项
- 如果从不同位置运行 `rebuild_app.bat`，建议先导航到项目根目录
- 批处理文件中的 `cd /d "c:\Practice-code\jindouyun-typesetter"` 命令是为了确保在正确的目录下运行，但您也可以删除此行并直接在项目根目录下运行批处理文件

## 基本构建步骤

### 准备工作

1. 确保 pandoc.exe 文件位于 pandoc 文件夹中
   - 如果文件缺失，可以从 pandoc.zip 解压恢复

2. 确保已安装所有必要的Python依赖（参见requirements.txt）

### 构建方法

#### 方法1：使用rebuild_app.bat（推荐，已集成自动检测）

直接运行 `rebuild_app.bat`，它会让您选择是否启用自动检测：

1. 选择"Y"启用自动检测（推荐），会自动执行以下步骤：
   - 运行自动检测脚本，优化依赖项
   - 更新Pandoc-GUI.spec文件
   - 执行PyInstaller打包

2. 选择"N"跳过检测，直接使用现有配置打包

```bash
rebuild_app.bat
```

#### 方法2：手动构建

如果您想完全控制构建过程：

1. 运行自动检测脚本（可选）：
```bash
python auto_detect_deps.py
```

2. 执行打包：
```bash
pyinstaller Pandoc-GUI.spec
```

#### 方法3：测试自动检测功能

如果您想测试自动检测功能，查看将要生成的配置而不修改spec文件：

```bash
python auto_detect_deps.py --test
```

#### 方法4：只预览自动检测结果而不修改文件

如果您想查看将要生成的配置而不修改spec文件：

```bash
python auto_detect_deps.py --print-only
```

## 打包结果

- 打包后的 exe 文件将位于 `dist` 文件夹中
- 默认文件名为 `Pandoc-GUI.exe`

## PyQt5和Python标准库自动检测系统

### 概述

`auto_detect_deps.py` 脚本可以：
1. 自动检测项目中实际使用的PyQt5组件
2. 自动检测项目中实际使用的Python标准库模块
3. 生成相应的PyInstaller配置，只包含必要的依赖

这样可以显著减小打包后的exe文件体积，并确保您不会因为添加新的Qt组件而忘记更新spec文件。

### 工作原理

#### PyQt5组件检测

脚本会扫描`src`目录中的所有Python文件，查找以下导入模式：
```python
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
import PyQt5.QtGui
```

然后只收集实际使用的组件（QtWidgets、QtCore、QtGui等），而不是整个PyQt5库。

#### Python标准库检测

同样，脚本会检测Python标准库的使用情况，然后生成排除列表，只包含项目中未使用的标准库模块。这样可以排除大量不必要的标准库，减小打包体积。

### 高级用法

#### 指定不同的源代码目录

默认情况下，脚本会扫描`src`目录。如果您有不同的目录结构：

```bash
python auto_detect_deps.py --src my_source_dir
```

#### 指定不同的spec文件

默认情况下，脚本会更新`Pandoc-GUI.spec`。如果您使用不同的文件名：

```bash
python auto_detect_deps.py --spec my_app.spec
```

## 注意事项

1. **不要使用其他打包脚本**：它们可能会缺少必要的配置
2. **备份spec文件**：在首次使用自动检测前，建议备份原始的`Pandoc-GUI.spec`文件
3. **测试打包结果**：使用自动检测后，请务必测试生成的exe文件是否能正常运行
4. **PyQt5组件**：脚本会确保始终包含核心的PyQt5组件（Qt、QtCore、QtGui、QtWidgets），即使代码中没有显式导入

## 故障排除

### 打包后缺少模块

如果打包后出现"ModuleNotFoundError"错误：

1. 检查错误信息中提到的模块
2. 在`Pandoc-GUI.spec`文件中，从排除列表中移除该模块（如果存在）
3. 或者手动添加该模块到`hiddenimports`列表

### PyQt5相关错误

如果出现PyQt5相关的错误：

1. 检查是否使用了未检测到的PyQt5组件
2. 在spec文件中手动添加缺少的组件：
```python
datas += collect_data_files('PyQt5.QtPrintSupport')
binaries += collect_dynamic_libs('PyQt5.QtPrintSupport')
hiddenimports += collect_submodules('PyQt5.QtPrintSupport')
```

### 找不到pandoc.exe

如果打包后的exe提示找不到pandoc.exe：

1. 确认打包前pandoc文件夹中有pandoc.exe
2. 确认没有使用错误的打包脚本
3. 删除build和dist文件夹后重新打包

## 自定义

如果您需要修改检测逻辑，可以编辑`auto_detect_deps.py`文件：

- `get_stdlib_modules()`: 修改标准库模块列表
- `extract_pyqt5_imports()`: 修改PyQt5组件检测逻辑
- `extract_stdlib_imports()`: 修改标准库检测逻辑

## 手动构建（高级）

如果自动构建脚本无法使用，或者您需要更多控制，可以手动执行以下命令：

1. 打开命令提示符（不是PowerShell）

2. 导航到项目目录：
   ```bash
   cd /d C:\Practice-code\Pandoc-GUI
   ```

3. 执行打包命令：
   ```bash
   pyinstaller --onefile --windowed --name="Pandoc-GUI" --add-data "src;src" --add-data "pandoc;pandoc" --collect-all PyQt5 --collect-all ntplib app_minimal_fixed.py
   ```

4. 测试结果：
   ```bash
   dist\Pandoc-GUI.exe
   ```

### 关键配置说明

以下是对打包命令中各参数的解释：

- `--onefile`: 将应用程序打包为单个可执行文件
- `--windowed`: 创建GUI应用程序（无控制台窗口）
- `--name="Pandoc-GUI"`: 指定输出文件名
- `--add-data "src;src"`: 包含src目录中的所有文件
- `--add-data "pandoc;pandoc"`: 包含pandoc目录中的所有文件
- `--collect-all PyQt5`: 包含PyQt5及其所有子模块

- `--collect-all ntplib`: 包含网络时间库
- `app_minimal_fixed.py`: 使用修复后的入口点

### 入口点选择

项目中包含多个入口点文件，各自用途：

- `app_minimal_fixed.py`: **推荐使用** - 成功打包的版本，使用简化的网络检查
- `app_minimal.py`: 原始最小化版本
- `app_robust.py`: 包含更多错误处理的版本

建议始终使用 `app_minimal_fixed.py` 作为入口点，因为它是已验证可以成功打包和运行的版本。

### 依赖项列表

Pandoc-GUI 需要以下Python包：

```
PyQt5
ntplib
```

如果需要重新安装这些依赖，可以使用：

```bash
pip install PyQt5 ntplib pyinstaller
```

### 虚拟环境使用

为避免依赖冲突，建议使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install PyQt5 ntplib pyinstaller

# 打包应用程序
pyinstaller --onefile --windowed --name="Pandoc-GUI" --add-data "src;src" --add-data "pandoc;pandoc" --collect-all PyQt5 --collect-all ntplib app_minimal_fixed.py
```

### 批处理文件编码问题

如果遇到批处理文件编码问题：

1. 使用命令提示符而不是PowerShell
2. 手动执行PyInstaller命令
3. 确保批处理文件使用UTF-8编码保存

## 贡献

欢迎提交改进建议和bug报告！