import os
import re

def modify_image_references(directory):
    # 使用更宽松的正则表达式
    pattern = re.compile(r'<figure>.*?<img.*?src="([^"]+)".*?</figure>', re.DOTALL)

    for filename in os.listdir(directory):
        if filename.endswith('.mdx'):
            filepath = os.path.join(directory, filename)
            print(f"正在处理文件: {filepath}")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                print(f"文件内容长度: {len(content)} 字符")
                print(f"文件内容前200字符: {content[:200]}")  # 打印文件开头的内容
                
                matches = pattern.findall(content)
                print(f"在 {filename} 中找到 {len(matches)} 个匹配项")
                for match in matches:
                    print(f"  匹配到的图片路径: {match}")

                modified_content = pattern.sub(lambda m: f'![]({m.group(1)})', content)

                if modified_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(modified_content)
                    print(f"已修改文件: {filename}")
                else:
                    print(f"文件未变更: {filename}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")

directory_path = '/Users/allen/Desktop/dify-enterprise/user-guide/build-app/flow-app/nodes'
modify_image_references(directory_path)
print("所有文件处理完毕")