#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Android设备连接验证脚本
验证ADB设备连接状态并测试基本功能
"""

import subprocess
import sys
import time
from typing import Optional, Dict, List
import json

def print_chinese(message: str) -> None:
    """确保中文消息在Windows控制台正确显示"""
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode('gbk', 'ignore').decode('gbk'))

def get_device_info(serial: str) -> Dict[str, str]:
    """获取设备详细信息"""
    try:
        # 获取设备型号
        model = subprocess.run(
            ['adb', '-s', serial, 'shell', 'getprop', 'ro.product.model'],
            capture_output=True, text=True
        ).stdout.strip()

        # 获取Android版本
        version = subprocess.run(
            ['adb', '-s', serial, 'shell', 'getprop', 'ro.build.version.release'],
            capture_output=True, text=True
        ).stdout.strip()

        # 获取设备制造商
        manufacturer = subprocess.run(
            ['adb', '-s', serial, 'shell', 'getprop', 'ro.product.manufacturer'],
            capture_output=True, text=True
        ).stdout.strip()

        return {
            'serial': serial,
            'model': model,
            'android_version': version,
            'manufacturer': manufacturer
        }
    except subprocess.CalledProcessError:
        return {
            'serial': serial,
            'model': 'Unknown',
            'android_version': 'Unknown',
            'manufacturer': 'Unknown'
        }

def verify_device_connection(device_ip: Optional[str] = None) -> List[Dict[str, str]]:
    """验证设备连接状态"""
    connected_devices = []

    try:
        if device_ip:
            # 尝试连接指定IP的设备
            print_chinese(f"\n正在连接设备: {device_ip}...")
            result = subprocess.run(
                ['adb', 'connect', f'{device_ip}:5555'],
                capture_output=True,
                text=True
            )
            if 'connected' not in result.stdout.lower():
                print_chinese("设备连接失败")
                return []

        # 获取所有已连接设备
        devices_output = subprocess.run(
            ['adb', 'devices'],
            capture_output=True,
            text=True
        ).stdout.strip()

        # 解析设备列表
        for line in devices_output.split('\n')[1:]:  # 跳过第一行 "List of devices attached"
            if line.strip():
                serial = line.split()[0]
                if 'device' in line:
                    device_info = get_device_info(serial)
                    connected_devices.append(device_info)

    except subprocess.CalledProcessError as e:
        print_chinese(f"执行ADB命令时出错: {str(e)}")
        return []

    return connected_devices

def test_device_connection(device_info: Dict[str, str]) -> bool:
    """测试设备连接的稳定性"""
    serial = device_info['serial']
    try:
        # 测试基本shell命令
        print_chinese(f"\n正在测试设备 {device_info['model']} ({serial}) 的连接...")

        # 测试ping
        subprocess.run(
            ['adb', '-s', serial, 'shell', 'ping', '-c', '1', '127.0.0.1'],
            check=True, capture_output=True
        )
        print_chinese("网络连接测试成功")

        # 测试文件系统访问
        subprocess.run(
            ['adb', '-s', serial, 'shell', 'ls', '/data/local/tmp'],
            check=True, capture_output=True
        )
        print_chinese("文件系统访问测试成功")

        return True
    except subprocess.CalledProcessError as e:
        print_chinese(f"连接测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print_chinese("\n=== Android设备连接验证工具 ===\n")

    # 获取命令行参数中的设备IP（如果有）
    device_ip = sys.argv[1] if len(sys.argv) > 1 else None

    # 验证设备连接
    connected_devices = verify_device_connection(device_ip)

    if not connected_devices:
        print_chinese("\n未找到已连接的设备")
        print_chinese("请确保:")
        print_chinese("1. 设备已通过USB连接或在同一网络中")
        print_chinese("2. 已在设备上启用开发者选项")
        print_chinese("3. 已启用USB调试")
        print_chinese("4. 已在设备上允许USB调试")
        return

    print_chinese(f"\n找到 {len(connected_devices)} 个已连接设备:")
    for device in connected_devices:
        print_chinese(f"\n设备信息:")
        print_chinese(f"- 序列号: {device['serial']}")
        print_chinese(f"- 型号: {device['model']}")
        print_chinese(f"- 制造商: {device['manufacturer']}")
        print_chinese(f"- Android版本: {device['android_version']}")

        # 测试设备连接
        if test_device_connection(device):
            print_chinese("设备连接验证成功")
        else:
            print_chinese("设备连接验证失败")

if __name__ == "__main__":
    main()
