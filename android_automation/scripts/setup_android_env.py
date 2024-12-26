#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Android UI自动化测试环境配置脚本
用于Windows环境下的自动化环境配置和设备连接验证
"""

import os
import sys
import subprocess
import time
from typing import Optional, List, Dict
import platform

def print_chinese(message: str) -> None:
    """确保中文消息在Windows控制台正确显示"""
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode('gbk', 'ignore').decode('gbk'))

def check_python_version() -> bool:
    """检查Python版本是否满足要求"""
    version = sys.version_info
    if version.major != 3 or version.minor < 6:
        print_chinese("错误: 需要Python 3.6或更高版本")
        return False
    return True

def install_package(package: str) -> bool:
    """安装Python包"""
    try:
        print_chinese(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
        return True
    except subprocess.CalledProcessError:
        print_chinese(f"安装 {package} 失败")
        return False

def check_dependencies() -> bool:
    """检查并安装必要的依赖"""
    required_packages = ["uiautomator2", "adbutils"]

    for package in required_packages:
        try:
            __import__(package)
            print_chinese(f"{package} 已安装")
        except ImportError:
            if not install_package(package):
                return False
    return True

def verify_adb_installation() -> bool:
    """验证ADB是否正确安装"""
    try:
        import adbutils
        adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        version = adb.server_version()
        print_chinese(f"ADB 服务器版本: {version}")
        return True
    except Exception as e:
        print_chinese(f"ADB 验证失败: {str(e)}")
        print_chinese("请确保Android SDK平台工具已安装，并且ADB在系统PATH中")
        return False

def list_devices() -> List[Dict[str, str]]:
    """列出所有连接的设备"""
    try:
        import adbutils
        adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        devices = []
        for device in adb.device_list():
            info = {
                "serial": device.serial,
                "state": "connected",
                "model": device.prop.model
            }
            devices.append(info)
        return devices
    except Exception as e:
        print_chinese(f"获取设备列表失败: {str(e)}")
        return []

def verify_uiautomator2() -> bool:
    """验证uiautomator2是否正常工作"""
    try:
        import uiautomator2 as u2
        print_chinese("uiautomator2 验证成功")
        return True
    except Exception as e:
        print_chinese(f"uiautomator2 验证失败: {str(e)}")
        return False

def main():
    """主函数"""
    print_chinese("\n=== Android UI自动化测试环境配置 ===\n")

    # 检查操作系统
    if platform.system() != "Windows":
        print_chinese("警告: 此脚本设计用于Windows系统")

    # 检查Python版本
    if not check_python_version():
        return

    # 检查依赖
    print_chinese("\n正在检查依赖...")
    if not check_dependencies():
        return

    # 验证ADB
    print_chinese("\n正在验证ADB...")
    if not verify_adb_installation():
        return

    # 验证uiautomator2
    print_chinese("\n正在验证uiautomator2...")
    if not verify_uiautomator2():
        return

    # 列出设备
    print_chinese("\n正在查找已连接设备...")
    devices = list_devices()
    if devices:
        print_chinese("\n找到以下设备:")
        for device in devices:
            print_chinese(f"设备: {device['model']} ({device['serial']})")
    else:
        print_chinese("\n未找到已连接的设备。请确保:")
        print_chinese("1. 设备已通过USB连接或在同一网络中")
        print_chinese("2. 已在设备上启用开发者选项")
        print_chinese("3. 已启用USB调试或无线调试")

    print_chinese("\n环境配置检查完成")


if __name__ == "__main__":
    main()
