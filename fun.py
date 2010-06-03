import operator
import math

"""

This Expr (expression) object is to be inherited by functions and other relevant objects.
It defines operators which are used in place of certain commands.

Thus:
object1*object2 -> object1.__mul__(object2)

"""

class Expr(object):

    def __call__(self):
        return self

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return Add(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __pow__(self, other):
        return Pow(self, other)

    def derivs(self, symbol):
        raise NotImplementedError("derivs is not implemented")

class Symbol(Expr):

    """

Input argument as an English letter.

"""

    def __init__(self, arg):
        self.arg = str(arg)

    def __str__(self):
        return self.arg

    def derivs(self, symbol):
        if str(symbol) == self.arg:
            return int(1)
        else:
            return int(0)

"""

These define sine and cosine functions with the ability to print themselves and take derivatives of themselves.

"""

class sin(Expr):

    def __init__(self, arg):
        self.arg = arg

    def __call__(self, num):
        return math.sin(float(num))

    def derivs(self, symbol):
        return cos(self.arg)*self.arg.derivs(symbol)

    def __str__(self):
        return "sin(" + str(self.arg) + ")"

class cos(Expr):

    def __init__(self, arg):
        self.arg = arg

    def __call__(self, num):
        return math.sin(float(num))

    def derivs(self, symbol):
        return sin(self.arg)*-1*self.arg.derivs(symbol)

    def __str__(self):
        return "cos(" + str(self.arg) + ")"

"""

Mul and Add are the objects that hold two bits of data that are multiplied or added respectively.

"""

class Mul(Expr):

    def __init__(self, *args):
        self.args = self.flatten_args(args)

    def flatten_args(self, args):
        flat_args = []
        for arg in args:
            if isinstance(arg, Mul):
                flat_args.extend(arg.args)
            else:
                flat_args.append(arg)
        return flat_args

    def __str__(self):
        arg_string = ''
        for arg in self.args:
            if len(arg_string) == 0:
                arg_string = arg_string + str(arg)
            else:
                arg_string = arg_string + "*" + str(arg)
        return arg_string

    def derivs(self, symbol):
        derivs = []
        for arg in self.args:
            if isinstance(arg, (int,float)):
                derivs.append(0)
            else:
                derivs.append(arg.derivs(symbol))
        muls = []
        for i in range(len(self.args)):
            mul_args = self.args[:i] + [derivs[i]] + self.args[i+1:]
            muls.append(Mul(*mul_args))
        return Add(*muls)

class Add(Expr):

    def __init__(self, *args):
        self.args = self.flatten_args(args)

    def flatten_args(self, args):
        flat_args = []
        for arg in args:
            if isinstance(arg, Add):
                flat_args.extend(arg.args)
            else:
                flat_args.append(arg)
        return flat_args

    def __str__(self):
        arg_string = ''
        for arg in self.args:
            if len(arg_string) == 0:
                arg_string = arg_string + str(arg)
            else:
                arg_string = arg_string + "+" + str(arg)
        return arg_string

    def derivs(self, symbol):
        deriv_args = Add()
        for arg in self.args:
            if isinstance(arg, (int,float)):
                deriv_args = Add(deriv_args,0)
            else:
                deriv_args = Add(deriv_args, arg.derivs(symbol))
        return deriv_args

"""

Pow raises arguments to a power.

"""

class Pow(Expr):

    """

Only raise arguments to integers!

"""

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        if isinstance(self.args[0], int):
            return "[" + str(self.args[0]) + "]" + "**" + str(self.args[1])
        else:
            return "[" + self.args[0].__str__() + "]" + "**" + str(self.args[1])

    def derivs(self, symbol):
        if str(self.args[0]) == str(symbol):
            if self.args[1] == int(1):
                return int(1)
            else:
                return Mul(int(self.args[1]), Pow(self.args[0], int(self.args[1]-1)))
        else:
            return 0

"""

a wave function; pretty basic right now

"""
class psi(Expr):
    def __init__(self, wave):
        self.wave = wave

    def __str__(self):
        return self.wave.__str__()

    def derivs(self):
        return self.wave.derivs()

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
f = Symbol('f')
g = Symbol('g')

u = sin(x)
v = cos(y)

r = u*v*z
s = u+v+z
t = x**2*y**3*z**4*f*g
p = x**2+y**3+z**4

a = r+s
b = r*s
c = t+s*r
