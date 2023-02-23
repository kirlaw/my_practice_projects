#数据保存格式：
#文件名 \t label
#


import os

dirs=[""]

for label,dir in enumerate(dirs):
    files=os.listdir(dir)
    for file in files:
        with open("lego_train/train_list.txt",'a+') as f:
            f.write(file+'\t'+str(label)+'\n')
