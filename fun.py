import operator
"""
This function object is to be inherited by functions
It defines operators which are used in place of certain commands

Thus:
object1*object2 -> object1.__mul__(object2) 

"""
class function(object):
    def __call__(self):
        print self.whoami()

    def __add__(self, other):
        return Add(self, other)

    def __mul__(self,other):
        return mul(self, other)

    def derivs(self):
        raise NotImplementedError("derivs is not implmented")

"""
These define sine and cosine functions with the ability to print themselves and take a derivative of themself

"""
class sin(function):

    def __init__(self, arg):
        self.arg = arg
         
    def derivs(self):
        return cos(self.arg)
       
    def whoami(self):
        return "sin(" + self.arg + ")"
       
class cos(function):

    def __init__(self, arg):
        self.arg = arg
       
    def derivs(self):
        return mul(-1, sin(self.arg))

    def whoami(self):
        return "cos(" + self.arg + ")"
"""
mul and add are the objects that hold two bits of data that are multipliedn or added

"""
class mul(function):

    def __init__(self, *args):
        self.args = args

    def whoami(self):
        if isinstance(self.arg1, int):
            str1 = str(self.arg1)
        else:
            str1 = self.arg1.whoami()
            
        if isinstance(self.arg2, int):
            str2 = str(self.arg2)
        else:
            str2 = self.arg2.whoami()
        
        return str1 + "*" + str2

    def derivs(self):
        arg1int = isinstance(self.arg1, int)
        arg2int = isinstance(self.arg1,int)
        
        if arg1int:
            return mul(self.arg2.derivs(),self.arg1) 
        elif arg2int:
            return mul(self.arg1.derivs(),self.arg2)
                
        return Add(mul(self.arg1.derivs(),self.arg2), mul(self.arg1, self.arg2.derivs()))

class Add(function):

    def __init__(self, *arg):
        self.arg1 = arg[0]
        self.arg2 = arg[1]

    def whoami(self):
        if isinstance(self.arg1, int):
            str1 = str(self.arg1)
        else:
            str1 = self.arg1.whoami()
            
        if isinstance(self.arg2, int):
            str2 = str(self.arg2)
        else:
            str2 = self.arg2.whoami()  
              
        return str1 + " + " + str2

    def derivs(self):
        arg1int = isinstance(self.arg1, int)
        arg2int = isinstance(self.arg1,int)
        
        if arg1int:
            return self.arg2.derivs()
        elif arg2int:
            return self.arg1.derivs()
            
        return Add(self.arg1.derivs(),self.arg2.derivs())
        
"""
Not working yet ; would represent a power
Also need to add a symbols class so we can take derivative with respect to different variables

"""
class Pow(function):

    def __init__(self,arg,power):
        self.power = power
        self.arg = arg

    def whoami(self):
        return "(" + self.arg + ")" + "**" + str(self.power)

    def derivs(self):
        self.power -= 1
        return mul(self.power+1, self)

"""
a wave function; pretty basic right now
"""        
class psi(function):
    def __init__(self, wave):
        self.wave = wave
        
    def whoami(self):
        return self.wave.whoami()
        
    def derivs(self):
        return self.wave.derivs()
        
x = "x"
y = sin(x)
q = cos(x)
z = y*q    
