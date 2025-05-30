# 快速使用指南

## 🚀 快速开始

您现在有了一套完整的文档菜单管理工具！

### 📁 创建的文件

1. **menu_manager.py** - 核心管理脚本
2. **menu_helper.py** - 简化操作脚本  
3. **demo.py** - 演示和测试脚本
4. **README_MENU.md** - 详细说明文档
5. **menu/** - 菜单文件存储目录

### 🎯 立即体验

**方式一：使用演示脚本（推荐新手）**
```bash
cd /Users/allen/Documents/Dify-Enterprise-Docs
python3 demo.py
```

**方式二：使用简化脚本**
```bash
python3 menu_helper.py
```

**方式三：直接使用核心脚本**
```bash
# 提取菜单
python3 menu_manager.py extract

# 列出版本
python3 menu_manager.py list

# 验证菜单
python3 menu_manager.py validate

# 合并菜单
python3 menu_manager.py merge
```

### 📋 建议的工作流程

1. **首次设置**
   ```bash
   python3 demo.py
   # 选择 1 - 提取菜单
   ```

2. **查看提取结果**
   ```bash
   python3 demo.py
   # 选择 2 - 列出版本
   # 选择 5 - 查看目录结构
   ```

3. **验证提取的菜单**
   ```bash
   python3 demo.py
   # 选择 3 - 验证菜单
   ```

4. **编辑菜单文件**
   - 直接编辑 `menu/` 目录下的JSON文件
   - 每个版本一个文件夹，每种语言一个文件

5. **合并回主文档**
   ```bash
   python3 demo.py
   # 选择 4 - 合并菜单
   ```

### 🎨 目录结构预览

```
Dify-Enterprise-Docs/
├── docs.json                    # 主文档配置
├── docs.json.backup            # 自动备份
├── menu_manager.py             # 核心脚本
├── menu_helper.py              # 简化脚本
├── demo.py                     # 演示脚本
├── README_MENU.md              # 详细文档
└── menu/                       # 菜单文件目录
    ├── 2.7.x/
    │   ├── menu-en.json        # 英文菜单
    │   ├── menu-cn.json        # 中文菜单
    │   └── menu-ja.json        # 日文菜单
    ├── 2.6.x/
    │   ├── menu-en.json
    │   ├── menu-cn.json
    │   └── menu-ja.json
    └── 2.5.x/
        ├── menu-en.json
        ├── menu-cn.json
        └── menu-ja.json
```

### 💡 核心优势

- **🔄 版本分离**: 每个版本独立管理，互不干扰
- **🌍 多语言支持**: 英文、中文、日文分别维护
- **✅ 自动验证**: 检查JSON格式和字段完整性
- **📦 自动备份**: 每次操作前自动备份原文件
- **🎛️ 简单操作**: 多种使用方式，适合不同需求

### 🔧 下一步

1. 运行 `python3 demo.py` 体验所有功能
2. 查看 `README_MENU.md` 了解详细用法
3. 开始编辑分离后的菜单文件
4. 享受更高效的文档维护体验！

---

**需要帮助？** 随时查看 README_MENU.md 或运行演示脚本！
