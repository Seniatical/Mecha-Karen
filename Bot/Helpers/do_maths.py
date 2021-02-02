import math

pi = lambda: math.pi

class Circle:
  circumference = lambda r srf=3: round((pi()*2)*r, srf)
  area = lambda r srf=3: round((pi()*r)**2, srf)
  diameter = lambda r: r*2
  radius = area, srf=3: round(math.sqrt(area/pi()), srf)
  
## some more later :p
