"""
增强的Pandoc转换器模块
处理文档格式的转换功能，支持HTML直接转换
"""

import os
import sys
import subprocess
from PyQt5.QtWidgets import QMessageBox


class EnhancedPandocConverter:
    """增强的Pandoc转换器"""
    
    def __init__(self, pandoc_path=None):
        # 优先使用传入的路径，其次使用环境变量中的路径
        self.pandoc_path = pandoc_path or os.environ.get('PANDOC_PATH')
        self.supported_formats = [
            'markdown', 'docx', 'pdf', 'html', 'epub', 'odt', 
            'txt', 'rst', 'json', 'latex', 'xml', 'pptx'
        ]
    
    def set_pandoc_path(self, path):
        """设置Pandoc可执行文件路径"""
        self.pandoc_path = path
        # 检查路径是否存在，如果不存在则尝试其他可能的路径
        if self.pandoc_path and not os.path.exists(self.pandoc_path):
            # 尝试从临时目录获取
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                alt_path = os.path.join(sys._MEIPASS, 'pandoc', 'pandoc.exe')
                if os.path.exists(alt_path):
                    self.pandoc_path = alt_path
    
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
    
    def convert_html_to_docx(self, html_content, output_file, template_style='simple'):
        """
        直接将HTML内容转换为DOCX文件
        
        Args:
            html_content: HTML内容字符串
            output_file: 输出文件路径
            template_style: 模板样式类型
            
        Returns:
            tuple: (success, message)
        """
        if not self.pandoc_path:
            return False, "未设置Pandoc路径"
            
        if not os.path.exists(self.pandoc_path):
            return False, f"Pandoc可执行文件不存在: {self.pandoc_path}"
        
        try:
            import tempfile
            
            # 创建临时HTML文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
                # 确保HTML内容有完整的文档结构
                if not html_content.strip().startswith('<!DOCTYPE') and not html_content.strip().startswith('<html'):
                    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>文档</title>
</head>
<body>
{html_content}
</body>
</html>"""
                
                temp_file.write(html_content)
                temp_html_path = temp_file.name
            
            # 构建pandoc命令
            cmd = [self.pandoc_path, temp_html_path, '-o', output_file]
            
            # 根据样式类型添加相应的参数
            if template_style == 'academic':
                # 学术论文风格：使用更正式的格式
                cmd.extend(['--standalone', '--toc', '--number-sections'])
            elif template_style == 'business':
                # 商务报告风格：简洁专业
                cmd.extend(['--standalone'])
            elif template_style == 'technical':
                # 技术文档风格：保留代码格式
                cmd.extend(['--standalone', '--highlight-style', 'pygments'])
            else:
                # 简洁通用风格：标准格式
                cmd.extend(['--standalone'])
            
            # 执行转换
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            
            # 清理临时文件
            try:
                os.unlink(temp_html_path)
            except:
                pass
            
            return True, f"转换成功：{os.path.basename(output_file)}"
            
        except subprocess.CalledProcessError as e:
            return False, f"转换失败：\n{e.stderr if e.stderr else str(e)}"
            
        except Exception as e:
            return False, f"发生错误：\n{str(e)}"