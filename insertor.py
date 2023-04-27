


"""
这个模块负责插桩
功能：在每一个类后面加一条log语句
在目标文件夹下实现一个log类
在每个类后第一句和每个成员方法后第一句实现一句log
"""

import os
import re



def insert_log(filename):
    # 读取文件内容
    with open(filename, "r") as f:
        contents = f.read()

    # 插入log打印语句
    contents = re.sub(r'invoke-\w+ \{([^}]*)\}, ([^,}]+)', r'invoke-static {\\1}, Lcom/example/Logger;->log("\2")\n\0', contents)
    contents = re.sub(r'(invoke-direct \{[^}]*\}, L[^;]*;-><init>\([^)]*\)V\n)(return-void\n)', r'\1invoke-static {}, Lcom/example/Logger;->log("<init>")\n\2', contents)

    # 写回文件
    with open(filename, "w") as f:
        f.write(contents)

def insert_log_in_folder(folder):
    # 遍历目录下所有smali文件
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".smali"):
                filepath = os.path.join(root, file)
                insert_log(filepath)



def generate_smali_class(apk_dir, package_name, class_name):
    # 根据类名生成 smali 文件路径
    smali_file_path = os.path.join(apk_dir, 'smali', package_name.replace('.', '/'), 'Logger.smali')

    # 如果文件已存在，则直接返回
    if os.path.exists(smali_file_path):
        return

    # 否则，生成新的 smali 类
    smali_class = '.class public L%s;\n' % (package_name + '.' + class_name)
    smali_class += '.super Ljava/lang/Object;\n'
    smali_class += '\n'
    smali_class += '.method public static log(Ljava/lang/String;)V\n'
    smali_class += '\t.locals 1\n'
    smali_class += '\tconst-string v0, "MyLogTag"\n'
    smali_class += '\tinvoke-static {v0, p0}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I\n'
    smali_class += '\treturn-void\n'
    smali_class += '.end method\n'

    # 将 smali 类写入到对应的 smali 文件中
    os.makedirs(os.path.dirname(smali_file_path), exist_ok=True)
    with open(smali_file_path, 'w') as f:
        f.write(smali_class)

# 用法示例
apk_dir = '/path/to/apk/dir'
package_name = 'com.example.app'
class_name = 'MyLogger'
generate_smali_class(apk_dir, package_name, class_name)




if __name__ == "__main__":
    folder = "/path/to/folder"
    insert_log_in_folder(folder)
