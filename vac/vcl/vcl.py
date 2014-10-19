from __future__ import generators
import random


class Backend(object):

    __props = {}

    def __init__(self, *args):
        assert (len(args) == 3)
        self.__props['name'] = args[0]
        self.__props['host'] = args[1]
        self.__props['port'] = args[2]

    def do_backend(self):
        backend = "backend %s {\n.%s = %s;\n.%s = %s;\n}" \
            % (self.__props['name'],
               'host',
               self.__props['host'],
               'port',
               self.__props['port'])
        print backend
        return backend


class Acl(object):

    __acls = []

    def __init__(self, name, *acls):
        assert (len(acls) != 0)
        self.__name = name
        self.__acls = acls

    def do_acl(self):
        domains = ''.join("%s;\n" % a for a in self.__acls)
        acl = "acl %s {\n%s}" % (self.__name, domains)
        print acl
        return acl


class VclFunction(object):

    _actions = []

    def accept(self, visitor):
        visitor.visit(self)

    def operate(self):
        print "%s:%s" % (self.__class__.__name__, self._actions)


class VclRecv(VclFunction):

    def __init__(self):
        self._actions = ['pipe', 'lookup']


class VclHash(VclFunction):

    def __init__(self):
        self._actions = ['hash']


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

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def visit(self, vcl_func):
        vcl_func.operate()


def vcl_func_gen(n):
    funcs = VclFunction.__subclasses__()
    for i in range(n):
        yield random.choice(funcs)()

if __name__ == '__main__':
    v = Visitor()
    for f in vcl_func_gen(5):
        f.accept(v)
