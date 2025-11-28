"""
版本检查模块
处理软件过期检查和网络时间查询功能
"""

import sys
from datetime import datetime, timezone, timedelta
try:
    import ntplib
except ImportError:
    ntplib = None

from PyQt5.QtWidgets import QMessageBox

# 北京时间时区 (UTC+8)
BEIJING_TZ = timezone(timedelta(hours=8))

# 过期时间常量 (北京时间)
EXPIRATION_DATE = datetime(2025, 12, 5, 0, 0, 0, tzinfo=BEIJING_TZ)


def check_network_time():
    """查询网络时间
    
    Returns:
        datetime: 北京时间对象，如果失败则返回None
    """
    if ntplib is None:
        return None
        
    try:
        # 查询网络时间
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', version=3)
        # 获取UTC时间并转换为北京时间
        utc_time = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
        return utc_time.astimezone(BEIJING_TZ)
    except (ntplib.NTPException, OSError, Exception):
        return None


def is_expired(current_time=None):
    """检查软件是否已过期
    
    Args:
        current_time (datetime, optional): 当前时间，如果为None则查询网络时间
        
    Returns:
        tuple: (bool, datetime) - (是否过期, 当前时间)
    """
    if current_time is None:
        current_time = check_network_time()
    
    if current_time is None:
        # 无法获取网络时间，假设已过期以强制用户联网
        return True, None
    
    print(f"Current Time (Beijing): {current_time}")
    print(f"Expiration Time (Beijing): {EXPIRATION_DATE}")
    
    return current_time >= EXPIRATION_DATE, current_time


def show_version_expired_dialog():
    """显示版本过期对话框"""
    QMessageBox.critical(
        None,
        "版本过期",
        "当前版本已过期，请联系开发者获取最新版。",
        QMessageBox.Ok
    )


def show_network_error_dialog():
    """显示网络连接错误对话框"""
    QMessageBox.critical(
        None,
        "网络连接失败",
        "请连接网络以检查版本状态。",
        QMessageBox.Ok
    )


def check_expiration():
    """检查软件是否过期，并显示相应的对话框
    
    Returns:
        bool: True表示未过期可继续使用，False表示已过期或网络错误
    """
    expired, current_time = is_expired()
    
    if current_time is None:
        # 网络连接失败
        show_network_error_dialog()
        return False
    
    if expired:
        # 已过期
        show_version_expired_dialog()
        return False
    
    # 未过期，可以正常使用
    return True


def is_expired_with_local_time():
    """使用本地时间检查软件是否已过期（用于调试）
    
    Returns:
        tuple: (bool, datetime) - (是否过期, 当前北京时间)
    """
    # 获取当前本地时间并转换为北京时间
    local_time = datetime.now(BEIJING_TZ)
    return local_time >= EXPIRATION_DATE, local_time


def get_expiration_message():
    """获取过期提示信息
    
    Returns:
        str: 过期提示信息
    """
    expiration_str = EXPIRATION_DATE.strftime("%Y.%m.%d %H:%M (北京时间)")
    return f"当前版本将在 {expiration_str} 过期"


def get_test_version_message():
    """获取测试版本提示信息
    
    Returns:
        str: 测试版本提示信息
    """
    return "当前使用的程序版本为测试版本，可能会有各种各样不可言明的 Bug，遇到问题请理性反馈，谢谢。"