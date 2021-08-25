import YSUNetAuthTools

if __name__ == '__main__':
    ysuAuth = YSUNetAuthTools.YSUNetAuth()
    while True:
        if not ysuAuth.tst_net():
            print("!!!")
