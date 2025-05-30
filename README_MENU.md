# Dify文档菜单管理工具

这套工具用于管理Dify企业版文档的多版本菜单配置，帮助您将复杂的单一配置文件分离成易于维护的多个文件。

## 目录结构

```
Dify-Enterprise-Docs/
├── docs.json                 # 主文档配置文件
├── menu_manager.py          # 核心菜单管理脚本
├── menu_helper.py           # 简化操作脚本
├── README_MENU.md           # 本说明文件
└── menu/                    # 菜单文件目录
    ├── 2.7.x/              # 版本目录
    │   ├── menu-en.json     # 英文菜单
    │   ├── menu-cn.json     # 中文菜单
    │   └── menu-ja.json     # 日文菜单
    ├── 2.6.x/
    │   ├── menu-en.json
    │   ├── menu-cn.json
    │   └── menu-ja.json
    └── 2.5.x/
        ├── menu-en.json
        ├── menu-cn.json
        └── menu-ja.json
```

## 快速开始

### 1. 使用简化脚本（推荐）

```bash
python3 menu_helper.py
```

然后按照菜单提示选择操作：
- 1: 提取菜单（首次使用时）
- 2: 合并菜单（修改后合并回主文档）
- 3: 列出版本
- 4: 验证菜单
- 5: 创建模板
- 6: 备份配置

### 2. 使用完整脚本

```bash
# 首次提取菜单到单独文件
python3 menu_manager.py extract

# 编辑完菜单文件后，合并回主文档
python3 menu_manager.py merge

# 列出所有版本
python3 menu_manager.py list

# 验证菜单文件
python3 menu_manager.py validate

# 创建新版本模板
python3 menu_manager.py template 2.8.x en

# 备份主配置文件
python3 menu_manager.py backup
```

## 主要功能

### 1. 菜单提取 (Extract)
- 从 `docs.json` 中提取各版本的菜单配置
- 为每个版本创建独立目录
- 为每种语言创建单独的 JSON 文件
- 自动备份原始文件

### 2. 菜单合并 (Merge)
- 将分离的菜单文件合并回 `docs.json`
- 保持原有的文档结构和配置
- 只更新菜单部分的内容

### 3. 模板创建 (Template)
- 为新版本创建基础菜单模板
- 包含常用的菜单结构
- 支持多语言模板

### 4. 验证功能 (Validate)
- 检查菜单文件的 JSON 格式
- 验证必需字段的完整性
- 报告发现的问题

## 工作流程建议

### 首次使用
1. 备份原始 `docs.json` 文件
2. 运行 `extract` 命令提取菜单
3. 检查生成的菜单文件

### 日常维护
1. 直接编辑 `menu/` 目录下的菜单文件
2. 运行 `validate` 验证修改
3. 运行 `merge` 合并回主文档
4. 测试文档站点

### 添加新版本
1. 运行 `template` 创建新版本模板
2. 编辑新版本的菜单文件
3. 运行 `merge` 更新主文档

## 菜单文件格式

每个菜单文件包含以下结构：

```json
{
  "version": "2.7.x",
  "language": "en",
  "href": "/en-us/introduction",
  "groups": [
    {
      "group": "Introduction",
      "pages": [
        "introduction"
      ]
    },
    {
      "group": "Deployment",
      "pages": [
        "en-us/deployment/checklist",
        {
          "group": "Quick Start for POC",
          "pages": [
            "en-us/deployment/prerequisites/kubernetes"
          ]
        }
      ]
    }
  ]
}
```

## 注意事项

1. **备份重要性**: 首次使用前请备份 `docs.json` 文件
2. **文件编码**: 所有文件使用 UTF-8 编码，支持中文和日文
3. **JSON格式**: 编辑菜单文件时请保持正确的 JSON 格式
4. **路径一致性**: 确保页面路径与实际文档文件路径一致
5. **版本号格式**: 建议使用 "x.y.x" 格式的版本号

## 故障排除

### 常见问题

1. **JSON格式错误**
   - 使用 `validate` 命令检查格式
   - 确保所有括号和引号正确闭合

2. **文件找不到**
   - 检查文件路径是否正确
   - 确保在正确的目录下运行脚本

3. **权限问题**
   - 确保对文档目录有读写权限
   - 必要时使用 `chmod` 修改权限

### 恢复备份

如果出现问题，可以从备份恢复：

```bash
cp docs.json.backup docs.json
```

## 高级用法

### 批量操作

可以结合其他工具进行批量操作：

```bash
# 批量验证所有菜单文件
find menu/ -name "*.json" -exec python3 -m json.tool {} \;

# 查找包含特定内容的菜单文件
grep -r "某个页面名称" menu/
```

### 自动化集成

可以将这些脚本集成到 CI/CD 流程中：

```yaml
# GitHub Actions 示例
- name: Validate Menu Files
  run: python3 menu_manager.py validate

- name: Merge Menu Files
  run: python3 menu_manager.py merge
```

## 支持

如有问题或建议，请联系文档维护团队。
