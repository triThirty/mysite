__author__ = 'triThirty'

import hashlib

class MD5(object):
    def __init__(self):
        self.m=hashlib.md5()

    def getMD5(self,str):
        self.m.update(str)
        return self.m



if __name__ == '__main__':
    m=MD5()
    mm = m.getMD5('12222222'.encode())
    print(mm.hexdigest())