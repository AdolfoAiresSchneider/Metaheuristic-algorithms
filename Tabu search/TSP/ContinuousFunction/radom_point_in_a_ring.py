from random import uniform
from math import sqrt, cos, sin, pi, hypot
from matplotlib import pyplot

def randomPoint(xc, yc, R1, R2):
  p = R2/R1
  a = uniform(p, 1)*2.*pi*R1
  x = uniform(p, 1)
  r = R1*x
  return (r*cos(a), r*sin(a))
  

def plot(points, R1, R2):
    c1 = pyplot.Circle((0,0), R1, color = 'r', fill = False)
    c2 = pyplot.Circle((0,0), R2, color = 'r', fill = False)
    x = [v[0] for v in points]
    print(points)
    y = [v[1] for v in points]
    pyplot.plot(x, y, linewidth = 0)
    pyplot.scatter(x, y, s = 10, color = 'b')
    pyplot.gcf().gca().add_artist(c1)
    pyplot.gcf().gca().add_artist(c2)
    pyplot.gca().set_xlim(-2*R1,2*R1);
    pyplot.gca().set_ylim(-2*R1,2*R1);
    pyplot.show()

pt = []
r1 = 3000
r2 = 1000
for i in range(500):
  pt.append(randomPoint(0,0,r1,r2))

plot(pt,r1,r2)
# ~ print(hypot(-166.0+170, -85+88))
  
  
