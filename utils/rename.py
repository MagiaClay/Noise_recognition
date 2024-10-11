import json
import os
import re
import sys

# 此脚本用于更改Label数据集中label书写错误的问题
def add_prefix_files(path):  # 定义函数名称
    mark = 're'  # 准备添加的前缀内容
    old_names = os.listdir(path)  # 取路径下的文件名，生成列表
    for old_name in old_names:  # 遍历列表下的文件名
        if old_name != sys.argv[0]:  # 代码本身文件路径，防止脚本文件放在path路径下时，被一起重命名
            if old_name.endswith('.jpg'):  # 当文件名以.txt后缀结尾时
                os.rename(os.path.join(path, old_name), os.path.join(path, mark + old_name))  # 重命名文件
                print(old_name, "has been renamed successfully! New name is: ", mark + old_name)  # 输出提示


def rewrite_json(path=r'D:\AI_fileCollected\Datasets\Helmet_ver1\Annotations'):
    dirs = os.listdir(path)

    num_flag = 0
    for file in dirs:  # 循环读取路径下的文件并筛选输出
        if os.path.splitext(file)[1] == ".json":  # 筛选Json文件
            num_flag = num_flag + 1
            print("path ===== ", file)
            # print(os.path.join(path,file))
            with open(os.path.join(path, file), 'r') as load_f:
                load_dict = json.load(load_f)
                # print(load_f)
            n = len(load_dict['shapes'])  # 获取字典load_dict中list值（因为每个list都有一个folder）
            # print(n)
            load_dict['imagePath'] = 're'+load_dict['imagePath']
            load_dict['imageData'] = ''
            for i in range(0, n):
                if re.findall('Without_Uniform', load_dict['shapes'][i]['label']):  # 模糊匹配，在folder中含有/export/guanghan/时
                    load_dict['shapes'][i]['label'] = 'Without_U'
                    # 路径更改，其中os.path.splitext(file)[0]是将文件名分为名字[0]+类型[1]
                elif re.findall('Uniform', load_dict['shapes'][i]['label']):  # 模糊匹配，在folder中含有/export/guanghan/时
                    load_dict['shapes'][i]['label'] = 'Uniform_Y'
                    # 路径更改，其中os.path.splitext(file)[0]是将文件名分为名字[0]+类型[1]

                # if load_dict['shapes'][i]['label'] == 'interstice':
                #   load_dict['shapes'][i]['label'] = 'cleft'
                with open(os.path.join(path, 're' + file), 'w') as dump_f:
                    json.dump(load_dict, dump_f)

    if num_flag == 0:
        print('所选文件夹不存在json文件，请重新确认要选择的文件夹')
    else:
        print('共{}个json文件'.format(num_flag))


if __name__ == '__main__':
    # add_prefix_files(r'D:\AI_fileCollected\Datasets\Helmet_ver1\JPEGImages')
    rewrite_json()
