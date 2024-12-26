#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
uiautomator2环境配置脚本
安装和配置uiautomator2及其依赖，支持Jenkins集成
"""

import subprocess
import sys
import os
import time
import json
from typing import List, Dict, Tuple
import importlib

def print_chinese(message: str) -> None:
    """确保中文消息在Windows控制台正确显示"""
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode('gbk', 'ignore').decode('gbk'))

def check_python_version() -> bool:
    """检查Python版本"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 6:
        print_chinese(f"Python版本兼容 (当前版本: {version.major}.{version.minor}.{version.micro})")
        return True
    else:
        print_chinese(f"Python版本不兼容 (需要3.6+, 当前版本: {version.major}.{version.minor}.{version.micro})")
        return False

def install_requirements() -> Tuple[bool, List[str]]:
    """安装必要的Python包"""
    requirements = [
        'uiautomator2',
        'adbutils>=0.10.0',
        'weditor',  # UI检查工具
        'pillow',   # 图像处理
        'opencv-python',  # 图像识别
        'requests', # 网络请求
        'allure-pytest',  # 测试报告
        'pytest'    # 测试框架
    ]

    failed_packages = []
    print_chinese("\n正在安装必要的Python包...")

    for package in requirements:
        try:
            print_chinese(f"正在安装 {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', package], check=True)
        except subprocess.CalledProcessError as e:
            print_chinese(f"安装包时出错: {str(e)}")
            failed_packages.append(package)

    return len(failed_packages) == 0, failed_packages

def verify_installation() -> Dict[str, bool]:
    """验证安装是否成功"""
    packages_to_check = {
        'uiautomator2': 'uiautomator2',
        'adbutils': 'adbutils',
        'weditor': 'weditor',
        'PIL': 'pillow',
        'cv2': 'opencv-python',
        'requests': 'requests',
        'pytest': 'pytest',
        'allure_pytest': 'allure-pytest'
    }

    installed = {}
    print_chinese("\n验证安装...")

    for module_name, package_name in packages_to_check.items():
        try:
            importlib.import_module(module_name)
            installed[package_name] = True
            print_chinese(f"✓ {package_name} 已安装")
        except ImportError:
            installed[package_name] = False
            print_chinese(f"✗ {package_name} 未安装")

    return installed

def setup_uiautomator2() -> bool:
    """配置uiautomator2"""
    try:
        print_chinese("\n初始化uiautomator2...")
        subprocess.run([sys.executable, '-m', 'uiautomator2', 'init'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_chinese(f"初始化uiautomator2失败: {str(e)}")
        return False

def create_requirements_file() -> None:
    """创建requirements.txt文件"""
    requirements = [
        'uiautomator2>=2.16.0',
        'adbutils>=0.10.0',
        'weditor>=0.6.0',
        'pillow>=8.0.0',
        'opencv-python>=4.5.0',
        'requests>=2.25.0',
        'pytest>=7.0.0',
        'allure-pytest>=2.9.0'
    ]

    try:
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(requirements))
        print_chinese("\n已创建requirements.txt文件")
    except Exception as e:
        print_chinese(f"\n创建requirements.txt失败: {str(e)}")

def create_status_report(success: bool, details: Dict) -> None:
    """创建状态报告用于Jenkins集成"""
    status = {
        'success': success,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'details': details
    }

    try:
        with open('setup_status.json', 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        print_chinese("\n已创建状态报告文件")
    except Exception as e:
        print_chinese(f"\n创建状态报告失败: {str(e)}")

def main():
    """主函数"""
    print_chinese("\n=== uiautomator2环境配置工具 ===\n")
    setup_success = True
    status_details = {}

    # 检查Python版本
    if not check_python_version():
        status_details['python_version'] = False
        setup_success = False
        create_status_report(False, status_details)
        return

    status_details['python_version'] = True

    # 安装依赖
    install_success, failed_packages = install_requirements()
    status_details['package_installation'] = {
        'success': install_success,
        'failed_packages': failed_packages
    }

    if not install_success:
        setup_success = False
        create_status_report(False, status_details)
        return

    # 验证安装
    installed_packages = verify_installation()
    all_installed = all(installed_packages.values())
    status_details['package_verification'] = installed_packages

    if all_installed:
        print_chinese("\n所有依赖包安装成功!")
    else:
        print_chinese("\n部分依赖包安装失败:")
        for package, installed in installed_packages.items():
            if not installed:
                print_chinese(f"- {package}: 未安装")
        print_chinese("\n请尝试手动安装失败的包")
        setup_success = False

    # 创建requirements.txt
    create_requirements_file()

    # 配置uiautomator2
    uiautomator2_success = setup_uiautomator2()
    status_details['uiautomator2_setup'] = uiautomator2_success

    if not uiautomator2_success:
        setup_success = False
        create_status_report(False, status_details)
        return

    create_status_report(setup_success, status_details)

    if setup_success:
        print_chinese("\n环境配置完成!")
        print_chinese("\n使用说明:")
        print_chinese("1. 确保Android设备已连接")
        print_chinese("2. 确保已启用USB调试")
        print_chinese("3. 运行自动化测试前先初始化设备:")
        print_chinese("   python3 -m uiautomator2 init")
    else:
        print_chinese("\n环境配置未完全成功，请查看setup_status.json了解详情")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()

    # 配置uiautomator2
    if not setup_uiautomator2():
        print_chinese("配置uiautomator2失败")
        return

    # 创建requirements.txt
    create_requirements_file()

    print_chinese("\n环境配置完成!")
    print_chinese("\n使用说明:")
    print_chinese("1. 确保Android设备已连接")
    print_chinese("2. 确保已启用USB调试")
    print_chinese("3. 运行自动化测试前先初始化设备:")
    print_chinese("   python3 -m uiautomator2 init")

if __name__ == "__main__":
    main()
