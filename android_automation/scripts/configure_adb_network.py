#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ADB网络配置脚本
配置ADB服务器网络设置并启用TCP/IP模式
"""

import os
import subprocess
import sys
import time
from typing import Optional, Tuple
import platform
import socket

def print_chinese(message: str) -> None:
    """确保中文消息在Windows控制台正确显示"""
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode('gbk', 'ignore').decode('gbk'))

def restart_adb_server() -> bool:
    """重启ADB服务器"""
    try:
        print_chinese("正在重启ADB服务器...")
        # 停止现有服务器
        subprocess.run(['adb', 'kill-server'], check=True, capture_output=True)
        time.sleep(1)
        # 启动服务器并绑定到所有接口
        subprocess.run(['adb', 'start-server'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print_chinese(f"重启ADB服务器失败: {str(e)}")
        return False

def verify_port_listening(port: int) -> bool:
    """验证端口是否在监听"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0
    except:
        return False

def enable_tcpip_mode(port: int = 5555) -> bool:
    """启用TCP/IP模式"""
    try:
        # 检查是否有设备通过USB连接
        devices = subprocess.run(['adb', 'devices'],
                              capture_output=True,
                              text=True).stdout.strip()

        if 'device' not in devices:
            print_chinese("注意: 未检测到USB设备连接，TCP/IP模式可能无法启用")
            print_chinese("请确保至少有一个设备通过USB连接以启用TCP/IP模式")
            return False

        # 启用TCP/IP模式
        subprocess.run(['adb', 'tcpip', str(port)], check=True)
        print_chinese(f"TCP/IP模式已启用 (端口 {port})")
        return True
    except subprocess.CalledProcessError as e:
        print_chinese(f"启用TCP/IP模式失败: {str(e)}")
        return False

def verify_network_setup() -> Tuple[bool, str]:
    """验证网络设置"""
    try:
        # 检查ADB服务器端口
        if not verify_port_listening(5037):
            return False, "ADB服务器端口 (5037) 未在监听"

        # 获取网络接口信息
        if platform.system() == "Windows":
            cmd = ['ipconfig']
        else:
            cmd = ['ip', 'addr']

        net_info = subprocess.run(cmd, capture_output=True, text=True).stdout
        return True, net_info
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    print_chinese("\n=== ADB网络配置工具 ===\n")

    # 检查操作系统
    if platform.system() != "Windows":
        print_chinese("警告: 此脚本设计用于Windows系统")

    # 重启ADB服务器
    if not restart_adb_server():
        return

    # 启用TCP/IP模式
    if not enable_tcpip_mode():
        print_chinese("\n要启用TCP/IP模式，请:")
        print_chinese("1. 通过USB连接设备")
        print_chinese("2. 确保已启用USB调试")
        print_chinese("3. 在设备上允许USB调试")
        print_chinese("4. 重新运行此脚本")
        return

    # 验证网络设置
    success, net_info = verify_network_setup()
    if success:
        print_chinese("\n网络配置成功!")
        print_chinese("\n可用网络接口:")
        print(net_info)
        print_chinese("\n使用说明:")
        print_chinese("1. 记录设备的IP地址")
        print_chinese("2. 断开USB连接")
        print_chinese("3. 使用以下命令连接设备:")
        print_chinese("   adb connect <设备IP>:5555")
    else:
        print_chinese(f"\n网络配置验证失败: {net_info}")

if __name__ == "__main__":
    main()
