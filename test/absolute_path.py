# path = "/ad/ba/a.t"
path = "a.t"


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

        return name,extension

def isHideFile(filename):
    FilenameAndExtension=getFilenameAndExtension(filename)
    return len(FilenameAndExtension[0])==0 or FilenameAndExtension[0].find(".")==0

# DirAndFileName=getDirAndFileName(path)

# print(DirAndFileName[0])
# print(DirAndFileName[1])

print(getFilenameAndExtension("112"))
print(getFilenameAndExtension(".112"))
print(getFilenameAndExtension(".1321.231.3.112"))
# getFilenameAndExtension(DirAndFileName[1])
