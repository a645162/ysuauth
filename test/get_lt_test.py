class testget_lt():
    a = 1

    def __init__(self):
        pass

    def __init__(self, a):
        self.a = a

    def __get__(self, other):
        return self.a > other.a

    def __lt__(self, other):
        return self.a < other.a

    def __ge__(self, other):
        return self.a >= other.a

    def __le__(self, other):
        return self.a <= other.a


# >    __get__
# <    __lt__
# >=    __ge__
# <=    __le__
if __name__ == '__main__':
    a = testget_lt(1)
    b = testget_lt(2)
    c = testget_lt(2)
    d = testget_lt(2)
    print(a > b)
    print(a < b)
    print(a >= b)
    print(a <= b)
    print()
    print(c >= d)
    print(c <= d)
