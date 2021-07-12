import platform

# 系统类型
isWindows = False
if str(platform.system()).find("Windows") != -1:
    isWindows = True
