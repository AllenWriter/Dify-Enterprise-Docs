#!/bin/bash

# 运行语言检查脚本
if bash ./lang-check/git-diff.sh; then
    # 检查通过，执行提交
    git commit -m "$*"
else
    # 检查失败
    echo "Language check failed, commit aborted"
    exit 1
fi