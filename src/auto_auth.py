# -*- coding: utf-8 -*-

import time

import config
import program_logs


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
    restartFilename = "restart.ysuauth"
    while True:
        execfile("main_auto_auth.py")
        if config.isFileExist(restartFilename):
            program_logs.print1("\t\t\t\t\tAfter 10 seconds will restart!")
            time.sleep(10)
            program_logs.print1("\t\t\t\t\trestart！！！！")
        else:
            break
