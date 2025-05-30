#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dify文档菜单管理工具
用于分离和管理不同版本的文档菜单配置
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List
import argparse


class MenuManager:
    def __init__(self, docs_root: str):
        self.docs_root = Path(docs_root)
        self.menu_dir = self.docs_root / "menu"
        self.main_docs_file = self.docs_root / "docs.json"
        
        # 确保菜单目录存在
        self.menu_dir.mkdir(exist_ok=True)
        
    def load_main_docs(self) -> Dict[str, Any]:
        """加载主文档配置文件"""
        if not self.main_docs_file.exists():
            raise FileNotFoundError(f"找不到主文档文件: {self.main_docs_file}")
        
        with open(self.main_docs_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_main_docs(self, docs_config: Dict[str, Any]):
        """保存主文档配置文件"""
        with open(self.main_docs_file, 'w', encoding='utf-8') as f:
            json.dump(docs_config, f, ensure_ascii=False, indent=2)
    
    def extract_menus(self):
        """提取各版本菜单到单独文件"""
        print("正在提取各版本菜单...")
        
        docs_config = self.load_main_docs()
        versions = docs_config.get('navigation', {}).get('versions', [])
        
        if not versions:
            print("警告: 未找到版本信息")
            return
        
        for version_info in versions:
            version = version_info.get('version')
            if not version:
                continue
                
            print(f"处理版本: {version}")
            
            # 创建版本目录
            version_dir = self.menu_dir / version
            version_dir.mkdir(exist_ok=True)
            
            # 为每个语言创建菜单文件
            languages = version_info.get('languages', [])
            for lang_info in languages:
                language = lang_info.get('language')
                if not language:
                    continue
                    
                print(f"  处理语言: {language}")
                
                # 创建菜单文件
                menu_file = version_dir / f"menu-{language}.json"
                menu_data = {
                    "version": version,
                    "language": language,
                    "href": lang_info.get('href', ''),
                    "groups": lang_info.get('groups', [])
                }
                
                with open(menu_file, 'w', encoding='utf-8') as f:
                    json.dump(menu_data, f, ensure_ascii=False, indent=2)
                    
                print(f"    已保存: {menu_file}")
        
        print("菜单提取完成!")
    
    def merge_menus(self):
        """将分离的菜单文件合并回主文档"""
        print("正在合并菜单文件...")
        
        docs_config = self.load_main_docs()
        
        # 重建versions数组
        versions = []
        
        # 遍历菜单目录中的版本文件夹
        for version_dir in sorted(self.menu_dir.iterdir()):
            if not version_dir.is_dir():
                continue
                
            version = version_dir.name
            print(f"处理版本: {version}")
            
            languages = []
            
            # 遍历版本目录中的菜单文件
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
                    
                except Exception as e:
                    print(f"    错误: 无法加载 {menu_file}: {e}")
            
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
        
        self.save_main_docs(docs_config)
        print("菜单合并完成!")
    
    def create_template_menu(self, version: str, language: str):
        """创建新的菜单模板"""
        print(f"创建新菜单模板: {version}-{language}")
        
        version_dir = self.menu_dir / version
        version_dir.mkdir(exist_ok=True)
        
        menu_file = version_dir / f"menu-{language}.json"
        
        template_data = {
            "version": version,
            "language": language,
            "href": f"/{language}/introduction",
            "groups": [
                {
                    "group": "Introduction" if language == "en" else "简介" if language == "cn" else "はじめに",
                    "pages": [
                        f"{language}/introduction"
                    ]
                },
                {
                    "group": "Deployment" if language == "en" else "部署手册" if language == "cn" else "デプロイメントマニュアル",
                    "pages": [
                        f"{language}/deployment/checklist"
                    ]
                }
            ]
        }
        
        with open(menu_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)
        
        print(f"模板已创建: {menu_file}")
    
    def list_versions(self):
        """列出所有版本和语言"""
        print("当前文档版本和语言:")
        print("-" * 40)
        
        for version_dir in sorted(self.menu_dir.iterdir()):
            if not version_dir.is_dir():
                continue
                
            version = version_dir.name
            print(f"版本: {version}")
            
            for menu_file in sorted(version_dir.glob("menu-*.json")):
                language = menu_file.stem.replace("menu-", "")
                print(f"  语言: {language}")
        
        print("-" * 40)
    
    def validate_menus(self):
        """验证菜单文件的完整性"""
        print("验证菜单文件...")
        
        issues = []
        
        for version_dir in self.menu_dir.iterdir():
            if not version_dir.is_dir():
                continue
                
            version = version_dir.name
            
            for menu_file in version_dir.glob("menu-*.json"):
                language = menu_file.stem.replace("menu-", "")
                
                try:
                    with open(menu_file, 'r', encoding='utf-8') as f:
                        menu_data = json.load(f)
                    
                    # 检查必需字段
                    required_fields = ['version', 'language', 'href', 'groups']
                    for field in required_fields:
                        if field not in menu_data:
                            issues.append(f"{menu_file}: 缺少字段 '{field}'")
                    
                    # 检查groups是否为数组
                    if not isinstance(menu_data.get('groups', []), list):
                        issues.append(f"{menu_file}: 'groups' 应该是数组")
                        
                except json.JSONDecodeError as e:
                    issues.append(f"{menu_file}: JSON格式错误 - {e}")
                except Exception as e:
                    issues.append(f"{menu_file}: 读取错误 - {e}")
        
        if issues:
            print("发现以下问题:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("所有菜单文件验证通过!")
    
    def backup_main_docs(self):
        """备份主文档配置文件"""
        backup_file = self.docs_root / "docs.json.backup"
        
        if self.main_docs_file.exists():
            import shutil
            shutil.copy2(self.main_docs_file, backup_file)
            print(f"已备份主文档配置到: {backup_file}")
        else:
            print("主文档配置文件不存在，无需备份")


def main():
    parser = argparse.ArgumentParser(description='Dify文档菜单管理工具')
    parser.add_argument('--root', default='.', help='文档根目录路径 (默认: 当前目录)')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 提取菜单命令
    subparsers.add_parser('extract', help='从主文档提取各版本菜单到单独文件')
    
    # 合并菜单命令
    subparsers.add_parser('merge', help='将分离的菜单文件合并回主文档')
    
    # 创建模板命令
    template_parser = subparsers.add_parser('template', help='创建新的菜单模板')
    template_parser.add_argument('version', help='版本号 (如: 2.8.x)')
    template_parser.add_argument('language', help='语言代码 (如: en, cn, ja)')
    
    # 列出版本命令
    subparsers.add_parser('list', help='列出所有版本和语言')
    
    # 验证菜单命令
    subparsers.add_parser('validate', help='验证菜单文件的完整性')
    
    # 备份命令
    subparsers.add_parser('backup', help='备份主文档配置文件')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        manager = MenuManager(args.root)
        
        if args.command == 'extract':
            manager.backup_main_docs()
            manager.extract_menus()
        elif args.command == 'merge':
            manager.merge_menus()
        elif args.command == 'template':
            manager.create_template_menu(args.version, args.language)
        elif args.command == 'list':
            manager.list_versions()
        elif args.command == 'validate':
            manager.validate_menus()
        elif args.command == 'backup':
            manager.backup_main_docs()
            
    except Exception as e:
        print(f"错误: {e}")
        return 1


if __name__ == '__main__':
    main()
