import os

def rename_md_to_mdx(directory):
    print(f"正在搜索目录: {os.path.abspath(directory)}")
    files = os.listdir(directory)
    print(f"找到的文件: {files}")
    
    md_files = [f for f in files if f.endswith('.md')]
    print(f"找到的 .md 文件: {md_files}")
    
    for filename in md_files:
        new_filename = filename[:-3] + '.mdx'
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)
        
        try:
            os.rename(old_file, new_file)
            print(f'已将 {filename} 重命名为 {new_filename}')
        except Exception as e:
            print(f"重命名 {filename} 时出错: {str(e)}")

# 获取脚本所在目录的路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 执行函数，使用脚本所在目录作为参数
rename_md_to_mdx(script_dir)

print("脚本执行完毕")