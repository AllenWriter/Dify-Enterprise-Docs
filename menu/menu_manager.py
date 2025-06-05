#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dify文档菜单管理工具 - 优化版本
整合了原来三个脚本的功能，提供简洁高效的菜单管理
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List


class DifyMenuManager:
    """Dify文档菜单管理器"""
    
    def __init__(self, docs_root: str = "."):
        self.docs_root = Path(docs_root).resolve()
        self.menu_dir = self.docs_root / "menu"
        self.main_docs_file = self.docs_root / "docs.json"
        
        # 确保菜单目录存在
        self.menu_dir.mkdir(exist_ok=True)
    
    def load_docs_config(self) -> Dict[str, Any]:
        """加载主文档配置"""
        if not self.main_docs_file.exists():
            raise FileNotFoundError(f"找不到文档配置文件: {self.main_docs_file}")
        
        with open(self.main_docs_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_docs_config(self, config: Dict[str, Any]) -> None:
        """保存文档配置"""
        with open(self.main_docs_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def version_sort_key(self, version_str: str) -> tuple:
        """生成版本排序键，新版本在前"""
        try:
            # 提取版本号，如 "2.8.x" -> (2, 8)
            parts = version_str.replace('.x', '').split('.')
            # 返回负数以实现降序排列（新版本在前）
            return tuple(-int(part) for part in parts)
        except (ValueError, AttributeError):
            # 如果解析失败，返回一个很大的负数，使其排在最后
            return (-999, -999)
    
    def sort_versions_desc(self, version_dirs: List[Path]) -> List[Path]:
        """按版本号降序排列目录（新版本在前）"""
        return sorted(version_dirs, key=lambda x: self.version_sort_key(x.name))
    
    def backup_docs(self) -> Path:
        """创建文档配置备份"""
        backup_file = self.docs_root / f"docs.json.backup"
        if self.main_docs_file.exists():
            import shutil
            shutil.copy2(self.main_docs_file, backup_file)
            return backup_file
        return None
    
    def extract_menus(self, verbose: bool = True) -> None:
        """提取各版本菜单到独立文件"""
        if verbose:
            print("🔄 正在提取菜单配置...")
        
        config = self.load_docs_config()
        versions = config.get('navigation', {}).get('versions', [])
        
        if not versions:
            print("⚠️  未找到版本配置")
            return
        
        extracted_count = 0
        for version_info in versions:
            version = version_info.get('version')
            if not version:
                continue
            
            version_dir = self.menu_dir / version
            version_dir.mkdir(exist_ok=True)
            
            languages = version_info.get('languages', [])
            for lang_info in languages:
                language = lang_info.get('language')
                if not language:
                    continue
                
                menu_data = {
                    "version": version,
                    "language": language,
                    "href": lang_info.get('href', ''),
                    "groups": lang_info.get('groups', [])
                }
                
                menu_file = version_dir / f"menu-{language}.json"
                with open(menu_file, 'w', encoding='utf-8') as f:
                    json.dump(menu_data, f, ensure_ascii=False, indent=2)
                
                extracted_count += 1
                if verbose:
                    print(f"  ✅ {version}/{language}")
        
        if verbose:
            print(f"✨ 成功提取 {extracted_count} 个菜单文件")
    
    def merge_menus(self, verbose: bool = True) -> None:
        """合并菜单文件到主配置"""
        if verbose:
            print("🔄 正在合并菜单配置...")
        
        config = self.load_docs_config()
        versions = []
        merged_count = 0
        
        # 获取所有版本目录并按版本号降序排列（新版本在前）
        version_dirs = [d for d in self.menu_dir.iterdir() if d.is_dir()]
        sorted_version_dirs = self.sort_versions_desc(version_dirs)
        
        for version_dir in sorted_version_dirs:
            
            version = version_dir.name
            languages = []
            
            for menu_file in sorted(version_dir.glob("menu-*.json")):
                language = menu_file.stem.replace("menu-", "")
                
                try:
                    with open(menu_file, 'r', encoding='utf-8') as f:
                        menu_data = json.load(f)
                    
                    languages.append({
                        "language": language,
                        "href": menu_data.get('href', ''),
                        "groups": menu_data.get('groups', [])
                    })
                    
                    merged_count += 1
                    if verbose:
                        print(f"  ✅ {version}/{language}")
                
                except Exception as e:
                    if verbose:
                        print(f"  ❌ {version}/{language}: {e}")
            
            if languages:
                versions.append({
                    "version": version,
                    "languages": languages
                })
        
        # 更新配置
        if 'navigation' not in config:
            config['navigation'] = {}
        config['navigation']['versions'] = versions
        
        self.save_docs_config(config)
        
        if verbose:
            print(f"✨ 成功合并 {merged_count} 个菜单文件")
    
    def validate_menus(self, verbose: bool = True) -> List[str]:
        """验证菜单文件"""
        if verbose:
            print("🔍 正在验证菜单文件...")
        
        issues = []
        checked_count = 0
        
        for version_dir in self.menu_dir.iterdir():
            if not version_dir.is_dir():
                continue
            
            for menu_file in version_dir.glob("menu-*.json"):
                checked_count += 1
                version = version_dir.name
                language = menu_file.stem.replace("menu-", "")
                
                try:
                    with open(menu_file, 'r', encoding='utf-8') as f:
                        menu_data = json.load(f)
                    
                    # 检查必需字段
                    required_fields = ['version', 'language', 'href', 'groups']
                    for field in required_fields:
                        if field not in menu_data:
                            issues.append(f"{version}/{language}: 缺少字段 '{field}'")
                    
                    # 检查一致性
                    if menu_data.get('version') != version:
                        issues.append(f"{version}/{language}: 版本不一致")
                    
                    if menu_data.get('language') != language:
                        issues.append(f"{version}/{language}: 语言不一致")
                    
                    if not isinstance(menu_data.get('groups', []), list):
                        issues.append(f"{version}/{language}: groups 应为数组")
                    
                    if len(menu_data.get('groups', [])) == 0:
                        issues.append(f"{version}/{language}: groups 不应为空")
                
                except json.JSONDecodeError as e:
                    issues.append(f"{version}/{language}: JSON格式错误 - {e}")
                except Exception as e:
                    issues.append(f"{version}/{language}: 读取错误 - {e}")
        
        if verbose:
            if issues:
                print(f"❌ 发现 {len(issues)} 个问题:")
                for issue in issues[:10]:  # 只显示前10个问题
                    print(f"   • {issue}")
                if len(issues) > 10:
                    print(f"   ... 还有 {len(issues) - 10} 个问题")
            else:
                print(f"✅ 所有 {checked_count} 个菜单文件验证通过")
        
        return issues
    
    def list_versions(self, verbose: bool = True) -> List[Dict]:
        """列出所有版本"""
        versions = []
        
        # 获取所有版本目录并按版本号降序排列（新版本在前）
        version_dirs = [d for d in self.menu_dir.iterdir() if d.is_dir()]
        sorted_version_dirs = self.sort_versions_desc(version_dirs)
        
        for version_dir in sorted_version_dirs:
            
            version = version_dir.name
            languages = []
            
            for menu_file in sorted(version_dir.glob("menu-*.json")):
                language = menu_file.stem.replace("menu-", "")
                
                try:
                    with open(menu_file, 'r', encoding='utf-8') as f:
                        menu_data = json.load(f)
                    languages.append({
                        'language': language,
                        'groups_count': len(menu_data.get('groups', [])),
                        'status': '✅'
                    })
                except:
                    languages.append({
                        'language': language,
                        'groups_count': 0,
                        'status': '❌'
                    })
            
            versions.append({
                'version': version,
                'languages': languages
            })
        
        if verbose:
            print("📋 当前版本列表:")
            print("-" * 50)
            for v in versions:
                print(f"📁 {v['version']}")
                for lang in v['languages']:
                    print(f"   {lang['status']} {lang['language']}: {lang['groups_count']} 个菜单组")
            print("-" * 50)
        
        return versions
    
    def create_template(self, version: str, language: str) -> None:
        """创建新版本模板"""
        print(f"🆕 创建模板: {version}/{language}")
        
        version_dir = self.menu_dir / version
        version_dir.mkdir(exist_ok=True)
        
        # 语言映射
        lang_map = {
            'en': {'group1': 'Introduction', 'group2': 'Deployment', 'href': f'/{language}/introduction'},
            'cn': {'group1': '简介', 'group2': '部署手册', 'href': f'/zh-cn/introduction'},
            'ja': {'group1': 'はじめに', 'group2': 'デプロイメントマニュアル', 'href': f'/ja-jp/introduction'}
        }
        
        lang_config = lang_map.get(language, lang_map['en'])
        
        template_data = {
            "version": version,
            "language": language,
            "href": lang_config['href'],
            "groups": [
                {
                    "group": lang_config['group1'],
                    "pages": [f"{language}/introduction"]
                },
                {
                    "group": lang_config['group2'],
                    "pages": [f"{language}/deployment/checklist"]
                }
            ]
        }
        
        menu_file = version_dir / f"menu-{language}.json"
        with open(menu_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 模板已创建: {menu_file}")
    
    def add_version(self, version: str, languages: List[str] = None) -> None:
        """添加新版本（自动创建所有语言的模板）"""
        if languages is None:
            languages = ['en', 'cn', 'ja']
        
        print(f"🚀 添加新版本: {version}")
        
        for language in languages:
            self.create_template(version, language)
        
        print(f"✨ 版本 {version} 创建完成，包含 {len(languages)} 种语言")
    
    def interactive_mode(self) -> None:
        """交互式模式"""
        print("🎯 Dify 菜单管理工具")
        print("=" * 40)
        
        while True:
            print("\n请选择操作:")
            print("1. 📤 提取菜单")
            print("2. 📥 合并菜单") 
            print("3. 📋 列出版本")
            print("4. 🔍 验证菜单")
            print("5. 🆕 添加版本")
            print("6. 💾 备份配置")
            print("0. 🚪 退出")
            
            try:
                choice = input("\n请输入选择 (0-6): ").strip()
                
                if choice == '0':
                    print("👋 再见!")
                    break
                elif choice == '1':
                    self.backup_docs()
                    self.extract_menus()
                elif choice == '2':
                    self.merge_menus()
                elif choice == '3':
                    self.list_versions()
                elif choice == '4':
                    self.validate_menus()
                elif choice == '5':
                    version = input("请输入版本号 (如: 2.9.x): ").strip()
                    if version:
                        self.add_version(version)
                elif choice == '6':
                    backup_file = self.backup_docs()
                    if backup_file:
                        print(f"✅ 备份已创建: {backup_file}")
                else:
                    print("❌ 无效选择")
                    
            except KeyboardInterrupt:
                print("\n\n👋 用户取消操作")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Dify文档菜单管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s                           # 进入交互模式
  %(prog)s extract                   # 提取菜单
  %(prog)s merge                     # 合并菜单
  %(prog)s add 2.9.x                 # 添加新版本
  %(prog)s template 2.9.x en         # 创建单个模板
  %(prog)s list                      # 列出版本
  %(prog)s validate                  # 验证菜单
        """)
    
    parser.add_argument('--root', default='.', help='文档根目录 (默认: 当前目录)')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 各种命令
    subparsers.add_parser('extract', help='提取菜单到独立文件')
    subparsers.add_parser('merge', help='合并菜单到主配置')
    subparsers.add_parser('list', help='列出所有版本')
    subparsers.add_parser('validate', help='验证菜单文件')
    subparsers.add_parser('backup', help='备份主配置')
    
    add_parser = subparsers.add_parser('add', help='添加新版本')
    add_parser.add_argument('version', help='版本号 (如: 2.9.x)')
    add_parser.add_argument('--languages', nargs='+', default=['en', 'cn', 'ja'], 
                           help='语言列表 (默认: en cn ja)')
    
    template_parser = subparsers.add_parser('template', help='创建单个模板')
    template_parser.add_argument('version', help='版本号')
    template_parser.add_argument('language', help='语言代码')
    
    args = parser.parse_args()
    
    try:
        manager = DifyMenuManager(args.root)
        verbose = not args.quiet
        
        # 如果没有指定命令，进入交互模式
        if not args.command:
            manager.interactive_mode()
            return
        
        # 执行指定命令
        if args.command == 'extract':
            manager.backup_docs()
            manager.extract_menus(verbose)
        elif args.command == 'merge':
            manager.merge_menus(verbose)
        elif args.command == 'list':
            manager.list_versions(verbose)
        elif args.command == 'validate':
            issues = manager.validate_menus(verbose)
            if issues and not verbose:
                sys.exit(1)
        elif args.command == 'backup':
            backup_file = manager.backup_docs()
            if backup_file and verbose:
                print(f"✅ 备份已创建: {backup_file}")
        elif args.command == 'add':
            manager.add_version(args.version, args.languages)
        elif args.command == 'template':
            manager.create_template(args.version, args.language)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
