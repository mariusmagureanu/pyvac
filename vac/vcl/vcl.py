from __future__ import generators
import random


class VclFunction(object):
    def accept(self, visitor):
        visitor.visit(self)

    def operate(self):
        print self.__class__.__name__


class VclRecv(VclFunction):
    pass


class VclHash(VclFunction):
    pass


class VclMiss(VclFunction):
    pass


class VclHit(VclFunction):
    pass


class VclFetch(VclFunction):
    pass


class VclDeliver(VclFunction):
    pass


class VclPipe(VclFunction):
    pass


class VclPass(VclFunction):
    pass


class Visitor:
    def __str__(self):
        return self.__class__.__name__

    def visit(self, vcl_func):
        vcl_func.operate()


def vcl_func_gen(n):
    funcs = VclFunction.__subclasses__()
    for i in range(n):
        yield random.choice(funcs)()

if __name__=='__main__':
    v = Visitor()
    for f in vcl_func_gen(5):
        f.accept(v)
    

