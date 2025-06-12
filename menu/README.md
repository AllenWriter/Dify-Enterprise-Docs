# Dify文档菜单管理工具

这是一个简化的菜单管理工具，用于管理Dify企业版文档的多版本菜单配置。

## 特性

- 🚀 **一键操作**: 单个脚本完成所有功能
- 📋 **交互式界面**: 友好的命令行交互
- 🔧 **命令行支持**: 支持自动化脚本调用
- 💾 **自动备份**: 重要操作前自动备份
- ✅ **智能验证**: 完整的菜单文件验证

## 快速开始

### 基本使用

```bash
# 进入交互模式（推荐）
python3 menu_manager.py

# 合并现有的菜单文件（你当前的需求）
python3 menu_manager.py merge

# 列出所有版本
python3 menu_manager.py list

# 验证菜单文件
python3 menu_manager.py validate
```

### 添加新版本

```bash
# 一键创建新版本的所有语言模板
python3 menu_manager.py add 2.9.x

# 只创建特定语言
python3 menu_manager.py add 2.9.x --languages en cn

# 创建单个模板
python3 menu_manager.py template 2.9.x en
```

### 提取和合并

```bash
# 从主配置提取菜单到独立文件
python3 menu_manager.py extract

# 将独立菜单文件合并回主配置
python3 menu_manager.py merge
```

## 目录结构

```
Dify-Enterprise-Docs/
├── docs.json                    # 主文档配置文件
├── menu/                        # 菜单管理目录
│   ├── menu_manager.py          # 菜单管理工具（新版本）
│   ├── README.md                # 本文档
│   ├── 2.5.x/                   # 版本目录
│   │   ├── menu-en.json         # 英文菜单
│   │   ├── menu-cn.json         # 中文菜单
│   │   └── menu-ja.json         # 日文菜单
│   ├── 2.6.x/
│   ├── 2.7.x/
│   └── 2.8.x/
└── docs.json.backup             # 自动备份文件
```

## 菜单文件格式

每个菜单文件包含以下结构：

```json
{
  "version": "2.8.x",
  "language": "cn",
  "href": "/zh-cn/introduction",
  "groups": [
    {
      "group": "简介",
      "pages": ["zh-cn/introduction"]
    },
    {
      "group": "部署手册",
      "pages": [
        "zh-cn/deployment/checklist",
        {
          "group": "安装指引",
          "pages": ["zh-cn/deployment/prerequisites/kubernetes"]
        }
      ]
    }
  ]
}
```

## 交互式界面

运行 `python3 menu_manager.py` 进入交互模式：

```
🎯 Dify 菜单管理工具
========================================

请选择操作:
1. 📤 提取菜单
2. 📥 合并菜单
3. 📋 列出版本
4. 🔍 验证菜单
5. 🆕 添加版本
6. 💾 备份配置
0. 🚪 退出
```

## 常用工作流程

### 首次使用
```bash
# 1. 备份并提取现有菜单
python3 menu_manager.py extract

# 2. 检查提取结果
python3 menu_manager.py list
```

### 日常维护
```bash
# 1. 编辑 menu/ 目录下的菜单文件
# 2. 验证修改
python3 menu_manager.py validate

# 3. 合并到主配置
python3 menu_manager.py merge
```

### 添加新版本
```bash
# 1. 创建新版本模板
python3 menu_manager.py add 2.9.x

# 2. 编辑生成的菜单文件
# 3. 合并到主配置
python3 menu_manager.py merge
```

## 命令参考

| 命令 | 描述 | 示例 |
|------|------|------|
| `extract` | 提取菜单到独立文件 | `python3 menu_manager.py extract` |
| `merge` | 合并菜单到主配置 | `python3 menu_manager.py merge` |
| `list` | 列出所有版本 | `python3 menu_manager.py list` |
| `validate` | 验证菜单文件 | `python3 menu_manager.py validate` |
| `add VERSION` | 添加新版本 | `python3 menu_manager.py add 2.9.x` |
| `template VERSION LANG` | 创建单个模板 | `python3 menu_manager.py template 2.9.x en` |
| `backup` | 备份主配置 | `python3 menu_manager.py backup` |

## 选项参数

- `--root PATH`: 指定文档根目录（默认：当前目录）
- `--quiet, -q`: 静默模式，减少输出信息
- `--languages LANG...`: 指定语言列表（用于 add 命令）

## 故障排除

### 常见问题

1. **JSON格式错误**
   ```bash
   python3 menu_manager.py validate
   ```

2. **文件权限问题**
   ```bash
   chmod +x menu_manager.py
   ```

3. **恢复备份**
   ```bash
   cp docs.json.backup docs.json
   ```

### 错误代码

- `0`: 成功
- `1`: 执行错误或验证失败

## 升级说明

### 从旧版本升级

如果你之前使用多个脚本文件：

1. 备份现有配置：`cp docs.json docs.json.backup`
2. 使用新工具：`python3 menu_manager.py`
3. 旧脚本文件已重命名为 `.old` 后缀，可以安全删除

### 兼容性

- Python 3.6+
- 与现有菜单文件格式完全兼容
- 保持与 Mintlify 文档系统的兼容性

## 技术说明

- **编码**: 所有文件使用 UTF-8 编码
- **格式**: 严格的 JSON 格式验证
- **备份**: 自动创建时间戳备份
- **错误处理**: 完善的异常处理和用户反馈

---

如有问题或建议，请联系文档维护团队。
