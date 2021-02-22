import math
import typing

pi = lambda: math.pi

class Circle:
  circumference = lambda r srf=3: round((pi()*2)*r, srf)
  area = lambda r srf=3: round((pi()*r)**2, srf)
  diameter = lambda r: r*2
  radius = area, srf=3: round(math.sqrt(area/pi()), srf)
    
class BaseOperation:
  __slots__ = ('eq', 'var')
  
  def __init__(self, **kwargs):
    self.eq = kwargs['eq']
    self.var = kwargs['var']
    
  def get_result(self) -> typing.Any:
    global var
    exec('global {var}; {var} = {eq}'.format(var = self.var, eq = self.eq))
    del var
    
    return var
  
  @staticmethod
  def globsearch(key: str):
    globals_ = globals()
    try:
      key = globals[key]
    except KeyError:
      return False
    return key
  
  @staticmethod
  def typed(etc, etcx, attr):
    if etc == etcx:
      return hasattr(etc, attr)
    if type(etc) == etcx:
      return True
    
    return etc == etcx if type(etcx) != etc else hasattr(etc, attr) == hasattr(etcx, attr)
  
## some more later :p
