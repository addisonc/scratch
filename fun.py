import operator

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

    def __str__(self):
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
         
    def derivs(self, symbol):
        return cos(self.arg)*self.arg.derivs(symbol)
       
    def __str__(self):
        return "sin(" + self.arg.__str__() + ")"
       
class cos(Expr):

    def __init__(self, arg):
        self.arg = arg
       
    def derivs(self, symbol):
        return sin(self.arg)*-1*self.arg.derivs(symbol)

    def __str__(self):
        return "cos(" + self.arg.__str__() + ")"
        
"""

Mul and Add are the objects that hold two bits of data that are multiplied or added respectively.
 
"""

class Mul(Expr):

    __demulargs__ = []
    
    def __init__(self, *args):
        for it in args:
            if isinstance(it,Mul):
                it.demul()
            else:
                __demulargs__.append(it)
        self.args = __demulargs__



    def demul(self):
        for arg in self.args:
        
            if isinstance(arg, Mul):
                demul(arg)
                
            else:
                __demulargs__.append(arg)

    def __str__(self):
        if isinstance(self.args[0], int):
            str1 = str(self.args[0])
        else:
            str1 = self.args[0].__str__()
            
        if isinstance(self.args[1], int):
            str2 = str(self.args[1])
        else:
            str2 = self.args[1].__str__()
        
        return str1 + "*" + str2

    def derivs(self):
        arg1int = isinstance(self.args[0], int)
        arg2int = isinstance(self.args[1], int)
        
        if arg1int:
            return Mul(self.args[1].derivs(),self.args[0])
        elif arg2int:
            return Mul(self.args[0].derivs(),self.args[1])
                
        return Add(Mul(self.args[0].derivs(),self.args[1]), Mul(self.args[0], self.args[1].derivs()))

class Add(Expr):

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        if isinstance(self.args[0], int):
            str1 = str(self.args[0])
        else:
            str1 = self.args[0].__str__()
            
        if isinstance(self.args[1], int):
            str2 = str(self.args[1])
        else:
            str2 = self.args[1].__str__()  
              
        return str1 + " + " + str2

    def derivs(self):
        arg1int = isinstance(self.args[0], int)
        arg2int = isinstance(self.args[1],int)
        
        if arg1int:
            return self.args[1].derivs()
        elif arg2int:
            return self.args[0].derivs()
            
        return Add(self.args[0].derivs(),self.args[1].derivs())
        
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

    def derivs(self):
        if self.args[1] == int(1):
            return int(1)
        else:
            return Mul(int(self.args[1]), Pow(self.args[0], int(self.args[1]-1)))

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

u = sin(x)
v = cos(y)

r = u*v*z
s = u+v+z
t = x**2*y**3*z**4
p = x**2+y**3+z**4

a = r+s
b = r*s
c = t+s*r
