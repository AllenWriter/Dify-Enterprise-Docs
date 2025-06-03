#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
菜单管理工具演示脚本
"""

import json
import os
from pathlib import Path

# 设置工作目录
DOCS_ROOT = Path("/Users/allen/Documents/Dify-Enterprise-Docs")
MENU_DIR = DOCS_ROOT / "menu"

def demo_extract():
    """演示菜单提取功能"""
    print("=== 菜单提取演示 ===")
    
    # 读取原始文档配置
    docs_file = DOCS_ROOT / "docs.json"
    if not docs_file.exists():
        print(f"错误: 找不到文档文件 {docs_file}")
        return
    
    with open(docs_file, 'r', encoding='utf-8') as f:
        docs_config = json.load(f)
    
    versions = docs_config.get('navigation', {}).get('versions', [])
    print(f"找到 {len(versions)} 个版本")
    
    # 创建菜单目录结构
    for version_info in versions:
        version = version_info.get('version')
        print(f"\n处理版本: {version}")
        
        # 创建版本目录
        version_dir = MENU_DIR / version
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # 处理每种语言
        languages = version_info.get('languages', [])
        for lang_info in languages:
            language = lang_info.get('language')
            print(f"  处理语言: {language}")
            
            # 创建菜单数据
            menu_data = {
                "version": version,
                "language": language,
                "href": lang_info.get('href', ''),
                "groups": lang_info.get('groups', [])
            }
            
            # 保存菜单文件
            menu_file = version_dir / f"menu-{language}.json"
            with open(menu_file, 'w', encoding='utf-8') as f:
                json.dump(menu_data, f, ensure_ascii=False, indent=2)
            
            print(f"    已创建: {menu_file}")
            print(f"    包含 {len(menu_data['groups'])} 个菜单组")
    
    print("\n菜单提取完成! 🎉")

def demo_list():
    """演示列出版本功能"""
    print("\n=== 版本列表演示 ===")
    
    if not MENU_DIR.exists():
        print("菜单目录不存在，请先运行提取功能")
        return
    
    print("当前文档版本和语言:")
    print("-" * 50)
    
    for version_dir in sorted(MENU_DIR.iterdir()):
        if not version_dir.is_dir():
            continue
            
        version = version_dir.name
        print(f"📁 版本: {version}")
        
        menu_files = list(version_dir.glob("menu-*.json"))
        if not menu_files:
            print("    ⚠️  无菜单文件")
            continue
            
        for menu_file in sorted(menu_files):
            language = menu_file.stem.replace("menu-", "")
            
            try:
                with open(menu_file, 'r', encoding='utf-8') as f:
                    menu_data = json.load(f)
                groups_count = len(menu_data.get('groups', []))
                print(f"    🌐 {language}: {groups_count} 个菜单组")
            except Exception as e:
                print(f"    ❌ {language}: 读取错误 - {e}")
    
    print("-" * 50)

def demo_validate():
    """演示验证功能"""
    print("\n=== 菜单验证演示 ===")
    
    if not MENU_DIR.exists():
        print("菜单目录不存在，请先运行提取功能")
        return
    
    issues = []
    checked_files = 0
    
    for version_dir in MENU_DIR.iterdir():
        if not version_dir.is_dir():
            continue
            
        version = version_dir.name
        
        for menu_file in version_dir.glob("menu-*.json"):
            checked_files += 1
            language = menu_file.stem.replace("menu-", "")
            
            try:
                with open(menu_file, 'r', encoding='utf-8') as f:
                    menu_data = json.load(f)
                
                # 检查必需字段
                required_fields = ['version', 'language', 'href', 'groups']
                for field in required_fields:
                    if field not in menu_data:
                        issues.append(f"{menu_file.name}: 缺少字段 '{field}'")
                
                # 检查版本一致性
                if menu_data.get('version') != version:
                    issues.append(f"{menu_file.name}: 版本不匹配 (文件:{menu_data.get('version')} vs 目录:{version})")
                
                # 检查语言一致性
                if menu_data.get('language') != language:
                    issues.append(f"{menu_file.name}: 语言不匹配 (文件:{menu_data.get('language')} vs 文件名:{language})")
                
                # 检查groups是否为数组
                if not isinstance(menu_data.get('groups', []), list):
                    issues.append(f"{menu_file.name}: 'groups' 应该是数组")
                
                # 检查groups是否为空
                if len(menu_data.get('groups', [])) == 0:
                    issues.append(f"{menu_file.name}: 'groups' 不应为空")
                    
            except json.JSONDecodeError as e:
                issues.append(f"{menu_file.name}: JSON格式错误 - {e}")
            except Exception as e:
                issues.append(f"{menu_file.name}: 读取错误 - {e}")
    
    print(f"检查了 {checked_files} 个菜单文件")
    
    if issues:
        print(f"\n发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"  ❌ {issue}")
    else:
        print("\n✅ 所有菜单文件验证通过!")

def demo_merge():
    """演示合并功能"""
    print("\n=== 菜单合并演示 ===")
    
    if not MENU_DIR.exists():
        print("菜单目录不存在，请先运行提取功能")
        return
    
    # 读取原始配置（用于保持其他配置不变）
    docs_file = DOCS_ROOT / "docs.json"
    with open(docs_file, 'r', encoding='utf-8') as f:
        docs_config = json.load(f)
    
    # 重建versions数组
    versions = []
    
    for version_dir in sorted(MENU_DIR.iterdir()):
        if not version_dir.is_dir():
            continue
            
        version = version_dir.name
        print(f"处理版本: {version}")
        
        languages = []
        
        for menu_file in sorted(version_dir.glob("menu-*.json")):
            language = menu_file.stem.replace("menu-", "")
            print(f"  加载语言: {language}")
            
            try:
                with open(menu_file, 'r', encoding='utf-8') as f:
                    menu_data = json.load(f)
                
                language_info = {
                    "language": language,
                    "href": menu_data.get('href', ''),
                    "groups": menu_data.get('groups', [])
                }
                
                languages.append(language_info)
                print(f"    ✅ 包含 {len(menu_data.get('groups', []))} 个菜单组")
                
            except Exception as e:
                print(f"    ❌ 错误: 无法加载 {menu_file}: {e}")
        
        if languages:
            version_info = {
                "version": version,
                "languages": languages
            }
            versions.append(version_info)
    
    # 更新主配置文件
    if 'navigation' not in docs_config:
        docs_config['navigation'] = {}
    docs_config['navigation']['versions'] = versions
    
    # 创建备份
    backup_file = DOCS_ROOT / "docs.json.backup"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(docs_config, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 合并完成! 备份已保存到: {backup_file}")
    print(f"总共处理了 {len(versions)} 个版本")

def main():
    """主函数"""
    print("🚀 Dify文档菜单管理工具演示")
    print("=" * 60)
    
    # 确保目录存在
    MENU_DIR.mkdir(exist_ok=True)
    
    while True:
        print("\n请选择演示功能:")
        print("1. 📤 提取菜单 (从主文档提取各版本菜单)")
        print("2. 📋 列出版本 (查看所有版本和语言)")
        print("3. 🔍 验证菜单 (检查菜单文件完整性)")
        print("4. 📥 合并菜单 (将分离的菜单合并回主文档)")
        print("5. 📁 查看目录结构")
        print("0. 🚪 退出")
        
        try:
            choice = input("\n请输入选择 (0-5): ").strip()
            
            if choice == '0':
                print("\n👋 再见!")
                break
            elif choice == '1':
                demo_extract()
            elif choice == '2':
                demo_list()
            elif choice == '3':
                demo_validate()
            elif choice == '4':
                demo_merge()
            elif choice == '5':
                show_directory_structure()
            else:
                print("❌ 无效选择，请输入 0-5")
                
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作，再见!")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

def show_directory_structure():
    """显示目录结构"""
    print("\n=== 目录结构 ===")
    
    def print_tree(path, prefix="", is_last=True):
        """递归打印目录树"""
        if not path.exists():
            print(f"{prefix}❌ {path.name} (不存在)")
            return
            
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{path.name}")
        
        if path.is_dir():
            children = list(path.iterdir())
            children.sort(key=lambda x: (x.is_file(), x.name))
            
            for i, child in enumerate(children):
                is_last_child = i == len(children) - 1
                extension = "    " if is_last else "│   "
                print_tree(child, prefix + extension, is_last_child)
    
    print(f"📁 {DOCS_ROOT.name}/")
    
    # 显示主要文件
    main_files = ['docs.json', 'menu_manager.py', 'menu_helper.py', 'README_MENU.md']
    for i, filename in enumerate(main_files):
        file_path = DOCS_ROOT / filename
        is_last = i == len(main_files) - 1 and not MENU_DIR.exists()
        status = "✅" if file_path.exists() else "❌"
        current_prefix = "└── " if is_last else "├── "
        print(f"{current_prefix}{status} {filename}")
    
    # 显示菜单目录
    if MENU_DIR.exists():
        print_tree(MENU_DIR, "", True)
    else:
        print("└── ❌ menu/ (目录不存在)")

if __name__ == '__main__':
    main()
