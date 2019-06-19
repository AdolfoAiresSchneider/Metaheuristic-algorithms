from copy import deepcopy as cp
from random import uniform
import random
from math import sqrt, cos, sin, pi, exp
import sys
from matplotlib import pyplot

def F(x):
  return sin(10*pi*x[0])*x[0]+1
  # ~ return -cos(x[0])*cos(x[1])*exp(-(x[0]-pi)**2 - (x[1] - pi)**2)
  
def randomPoint(xc, yc, R1, R2):
  p = R2/R1
  a = uniform(p, 1)*2.*pi*R1
  r = R1*uniform(p, 1)
  return [xc+r*cos(a), yc+r*sin(a)]

def Dist(x, y): 
  dist = 0.0
  for i in range(len(x)):
    dist = dist + (x[i]-y[i])**2
  return sqrt(dist)

class Move:
  def __init__(self, x, R1, R2):
    self.x, self.R1, self.R2 = x , R1, R2
  def __eq__(self, pt):
    dist = Dist(self.x, pt)
    if (not (dist <= self.R1 and dist >= self.R2)):
      return False
    return True
  pass

class Solution:
  
  def update_fitness(self):
    self.fitness = F(self.x)
       
  def __init__(self, N, L, R):
    if N == 0:
      return
    self.L, self.R, self.N, self.fitness = L, R, N, 0
    self.x = [uniform(L, R) for i in range(N)]
  
  def gen_neighbors(self, k, n_ring):
    neighbors = []
    for i in range(1, k+1):
      for j in range(n_ring):
        cpt = cp(self.x)
        Sol = cp(self)
        if i == 1:
          Sol.x = randomPoint(self.x[0],self.x[1], k, 0)
          Sol.update_fitness()
          neighbors.append((Sol, Move(cpt, 0, k)))
        else:
          Sol.x = randomPoint(self.x[0],self.x[1], i*k, (i-1)*k)
          Sol.update_fitness()
          neighbors.append((Sol, Move(cpt, i*k, (i-1)*k)))
    neighbors.sort(key = lambda z : z[0].fitness)
    return neighbors
  pass # End of class definition


def tabu_search(cur_sol, max_it, tbl_size, k, n_ring, tabu_list = list()):
  best_sol = cp(cur_sol)
  cnt = 1
  while cnt <= max_it:
    cnt += 1
    neighborhood = cur_sol.gen_neighbors(k, n_ring)
    for new_sol in neighborhood:
      move, neighbor = new_sol[1], new_sol[0]
      #  ponto
      if move.x in tabu_list:
        if neighbor.fitness < cur_sol.fitness:
          cur_sol = cp(neighbor)
          tabu_list.append(move)
          if cur_sol.fitness < best_sol.fitness:
            best_sol = cp(neighbor)
          break
      else:
        tabu_list.append(move)
        cur_sol = cp(neighbor)
        if cur_sol.fitness < best_sol.fitness:
          best_sol = cp(neighbor)
        break
    
    if len(tabu_list) > tbl_size:
      tabu_list.pop (0)
  
  return best_sol


def run_ts(n, max_iterations, tabu_list_sz, L, R, k, n_ring):
  sol1 = Solution(n, L, R) # number of dimensions, range(L, R)
  final_sol = tabu_search(sol1, max_iterations, tabu_list_sz, k, n_ring)
  print(sol1.x, final_sol.fitness)
  return final_sol

sols = [run_ts(2, 100, 10, -100, 100, 10, 10) for i in range(10)]
sols.sort(key = lambda z : z.fitness)
print(["Best = ", sols[0].x, sols[0].fitness])
