"""
Pandoc转换器模块
处理文档格式的转换功能
"""

import os
import subprocess
from PyQt5.QtWidgets import QMessageBox


class PandocConverter:
    """Pandoc转换器"""
    
    def __init__(self, pandoc_path=None):
        self.pandoc_path = pandoc_path
        self.supported_formats = [
            'markdown', 'docx', 'pdf', 'html', 'epub', 'odt', 
            'txt', 'rst', 'json', 'latex', 'xml', 'pptx'
        ]
    
    def set_pandoc_path(self, path):
        """设置Pandoc可执行文件路径"""
        self.pandoc_path = path
    
    def convert_file(self, input_file, output_file, template_file=None):
        """
        转换文件格式
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            template_file: 模板文件路径（可选）
            
        Returns:
            tuple: (success, message)
        """
        if not self.pandoc_path:
            return False, "未设置Pandoc路径"
            
        if not os.path.exists(self.pandoc_path):
            return False, f"Pandoc可执行文件不存在: {self.pandoc_path}"
            
        if not os.path.exists(input_file):
            return False, f"输入文件不存在: {input_file}"
        
        # 构建pandoc命令
        cmd = [self.pandoc_path, input_file, '-o', output_file]
        
        # 如果有模板文件，添加模板参数（仅对docx格式有效）
        if template_file and output_file.lower().endswith('.docx'):
            cmd.extend(['--reference-doc', template_file])
        
        try:
            # 执行pandoc命令
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            
            return True, f"转换成功：{os.path.basename(output_file)}"
            
        except subprocess.CalledProcessError as e:
            return False, f"转换失败：\n{e.stderr if e.stderr else str(e)}"
            
        except Exception as e:
            return False, f"发生错误：\n{str(e)}"