import os
import time

def SaveConf(filename, content):
    if os.path.exists(filename):
        mtime = os.stat(filename).st_mtime
        file_modify_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(mtime))
        print(filename + "文件已经存在,修改时间是: {0}".format(file_modify_time))
        new_name = "(" + file_modify_time + ")" + filename
        print("已经将原文件重命名为 {0}".format(new_name))

        try:
            os.rename(filename, new_name)
        except Exception as e:
            print(e)

    fh = open(filename, 'w', encoding='utf-8')
    fh.write(content)
    fh.close()
    print("保存{0}成功！".format(filename))

def isFileExist(path):
    return os.path.exists(path)