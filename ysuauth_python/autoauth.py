import time
import program_logs
import config


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


if __name__ == '__main__':
    # pass
    # runfile()
    while True:
        execfile("./autoauth1.py")
        if config.isFileExist("restart.ysuauth"):
            program_logs.print1("\t\t\t\t\t10秒后重新启动程序")
            time.sleep(10)
            program_logs.print1("\t\t\t\t\t重新启动程序！！！！")
        else:
            break
