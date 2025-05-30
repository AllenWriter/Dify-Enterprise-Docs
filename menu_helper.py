#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的菜单管理脚本
用于快速操作文档菜单
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd):
    """运行命令并显示输出"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    script_dir = Path(__file__).parent
    manager_script = script_dir / "menu_manager.py"
    
    if not manager_script.exists():
        print("错误: 找不到 menu_manager.py 文件")
        return 1
    
    print("Dify文档菜单管理工具")
    print("=" * 40)
    print("1. 提取菜单 (从主文档提取各版本菜单)")
    print("2. 合并菜单 (将分离的菜单合并回主文档)")
    print("3. 列出版本 (查看所有版本和语言)")
    print("4. 验证菜单 (检查菜单文件完整性)")
    print("5. 创建模板 (创建新版本菜单模板)")
    print("6. 备份配置 (备份主文档配置)")
    print("0. 退出")
    print("=" * 40)
    
    while True:
        try:
            choice = input("\n请选择操作 (0-6): ").strip()
            
            if choice == '0':
                print("再见!")
                break
            elif choice == '1':
                print("\n正在提取菜单...")
                run_command(f"python3 {manager_script} extract")
            elif choice == '2':
                print("\n正在合并菜单...")
                run_command(f"python3 {manager_script} merge")
            elif choice == '3':
                print("\n版本列表:")
                run_command(f"python3 {manager_script} list")
            elif choice == '4':
                print("\n验证菜单文件:")
                run_command(f"python3 {manager_script} validate")
            elif choice == '5':
                version = input("请输入版本号 (如: 2.8.x): ").strip()
                language = input("请输入语言代码 (如: en, cn, ja): ").strip()
                if version and language:
                    print(f"\n创建模板: {version}-{language}")
                    run_command(f"python3 {manager_script} template {version} {language}")
                else:
                    print("版本号和语言代码不能为空")
            elif choice == '6':
                print("\n备份配置文件:")
                run_command(f"python3 {manager_script} backup")
            else:
                print("无效选择，请输入 0-6")
                
        except KeyboardInterrupt:
            print("\n\n用户取消操作")
            break
        except Exception as e:
            print(f"错误: {e}")

if __name__ == '__main__':
    main()
