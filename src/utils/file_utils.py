"""
文件操作工具模块
提供文件相关的辅助函数
"""

import os
from PyQt5.QtWidgets import QFileDialog


def get_file_path(parent, caption, file_filter="所有文件 (*.*)"):
    """获取文件路径对话框
    
    Args:
        parent: 父窗口
        caption: 对话框标题
        file_filter: 文件过滤器
        
    Returns:
        str: 文件路径，如果取消则返回None
    """
    file_path, _ = QFileDialog.getOpenFileName(
        parent, caption, '', file_filter
    )
    return file_path if file_path else None


def get_save_file_path(parent, caption, file_filter="所有文件 (*.*)", default_suffix=""):
    """获取保存文件路径对话框
    
    Args:
        parent: 父窗口
        caption: 对话框标题
        file_filter: 文件过滤器
        default_suffix: 默认文件后缀
        
    Returns:
        str: 文件路径，如果取消则返回None
    """
    file_path, _ = QFileDialog.getSaveFileName(
        parent, caption, '', file_filter
    )
    
    # 添加默认后缀（如果需要）
    if file_path and default_suffix and not os.path.splitext(file_path)[1]:
        file_path += default_suffix
        
    return file_path if file_path else None


def get_file_name(file_path):
    """获取文件名（不包含路径）
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件名
    """
    return os.path.basename(file_path)


def get_file_extension(file_path):
    """获取文件扩展名
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件扩展名（包含点号）
    """
    return os.path.splitext(file_path)[1].lower()


def get_file_name_without_extension(file_path):
    """获取不带扩展名的文件名
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 不带扩展名的文件名
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def get_directory_path(file_path):
    """获取文件所在目录路径
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 目录路径
    """
    return os.path.dirname(file_path)


def generate_output_path(input_path, output_format, suffix="_converted"):
    """生成输出文件路径
    
    Args:
        input_path: 输入文件路径
        output_format: 输出格式
        suffix: 文件名后缀
        
    Returns:
        str: 输出文件路径
    """
    input_dir = get_directory_path(input_path)
    input_name = get_file_name_without_extension(input_path)
    return os.path.join(input_dir, f"{input_name}{suffix}.{output_format}")


def ensure_directory_exists(directory_path):
    """确保目录存在，如果不存在则创建
    
    Args:
        directory_path: 目录路径
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def file_exists(file_path):
    """检查文件是否存在
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 文件是否存在
    """
    return os.path.exists(file_path)


def get_project_root_dir(current_file):
    """获取项目根目录
    
    Args:
        current_file: 当前文件路径（通常使用__file__变量）
        
    Returns:
        str: 项目根目录路径
    """
    # 获取当前文件所在目录的上一级目录
    return os.path.dirname(os.path.dirname(os.path.abspath(current_file)))