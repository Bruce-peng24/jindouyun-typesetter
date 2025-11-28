"""
Pandoc GUI 应用程序入口
重构后的主程序文件，仅包含应用程序入口
"""

import sys
import os
# 添加当前目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication

# 导入主窗口类
from ui.main_window import PandocGUI

# 导入版本检查模块
from core.version_checker import check_expiration


def main():
    """主函数"""
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 执行过期检查
    if not check_expiration():
        sys.exit(1)
    
    # 创建主窗口
    window = PandocGUI()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()