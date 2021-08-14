import os
import time


def getDirAndFileName(path):
    paths = path.split("/")
    l = len(paths)
    dir = ""
    for i in range(l - 1):
        t = paths[i].strip()
        if len(t) != 0:
            dir += "/" + t
    filename = paths[l - 1]

    print(dir)
    print(filename)

    return dir, filename


def getFilenameAndExtension(filename):
    filenames = filename.strip().split(".")
    l = len(filenames)
    if l == 1:
        return filename.strip(), ""
    else:
        name = filenames[0]
        for i in range(1, l - 1):
            name += "." + filenames[i]

        extension = filenames[l - 1]

        return name, extension


def isHideFile(filename):
    FilenameAndExtension = getFilenameAndExtension(filename)
    return len(FilenameAndExtension[0]) == 0 or FilenameAndExtension[0].find(".") == 0


def toUnixPath(path):
    return path.replace("\\", "/")


def SaveConf(filename, content):
    if os.path.exists(filename):
        filename = toUnixPath(filename)
        # isAbsolutePath = filename.find("/") != -1
        mtime = os.stat(filename).st_mtime
        file_modify_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(mtime))
        DirAndFileName = getDirAndFileName(filename)
        FilenameAndExtension = getFilenameAndExtension(DirAndFileName[1])
        new_str = "(" + file_modify_time + ")"
        if len(FilenameAndExtension[1]) == 0:
            new_name = FilenameAndExtension[0] + new_str
        else:
            new_name = FilenameAndExtension[0] + new_str + "." + FilenameAndExtension[1]
        new_name = DirAndFileName[0] + new_name
        print(filename + "文件已经存在,修改时间是: {0}".format(file_modify_time))
        print("已经将原文件重命名为 {0}".format(new_name))

        try:
            os.rename(filename, new_name)
        except Exception as e:
            print(e)

    fh = open(filename, 'w', encoding='utf-8')
    fh.write(str(content))
    fh.close()
    print("保存{0}成功！".format(filename))


def isFileExist(path):
    return os.path.exists(path)
