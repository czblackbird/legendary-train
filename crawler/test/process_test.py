from multiprocessing import Process, Pool
import os
import string
from random import Random


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('function f')
    print('hello', name)


def test1():
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()


def pool():
    with Pool(5) as p:
        p.map(f, [''.join(Random().choices(string.ascii_letters, k=5))
              for i in range(100)])


def l():
    print([(''.join(Random().choices(string.ascii_letters, k=5))[0:4], '000')
           for i in range(100)])


if __name__ == '__main__':
    # test1()
    l()
    # pool()
