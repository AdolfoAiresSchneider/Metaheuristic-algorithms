from copy import deepcopy as copy
from random import randint as rand
import math
import sys
from matplotlib import pyplot

# Solution definition ------------------------------------------------------------------------------------

class Solution:
  
  def update_cost(self, Graph):
    self.cost = 0
    for i in range(self.N):
      self.cost += Graph[self.tour[i]][self.tour[i+1]]
      
  def __init__(self, n = 0, source = 0, Graph = []):
    if n == 0: return
    self.tour, self.N, self.cost = [], n, 0
    cur_node = source
    
    while cur_node not in self.tour and len(self.tour) < self.N-1:
      aux = [math.inf, -1]
      for i in range(self.N):
        if i != cur_node and i not in self.tour:
          if Graph[cur_node][i] < aux[0]:
            aux = [Graph[cur_node][i], i]
      self.tour.append(cur_node)
      cur_node = aux[1]
      
    self.tour.extend([cur_node, source])
    self.update_cost(Graph)
  
  # Generate the neighborhood of this solution by randomly swapping two citys
  def gen_neighbors(self, Graph):
    neighbors = []
    for x in [(i, rand(i+1, self.N-1)) for i in range(1, self.N-1)]:
      viz = self.copy()
      viz.tour[x[0]], viz.tour[x[1]] = viz.tour[x[1]], viz.tour[x[0]]
      viz.update_cost(Graph)
      neighbors.append((viz, x))
    neighbors.sort(key = lambda x : x[0].cost)
    return neighbors
  
  def copy(self):
    cp = Solution(0)
    cp.tour,cp.N,cp.cost=self.tour.copy(),self.N,self.cost
    return cp
  pass

# Build the graph-----------------------------------------------------------------------------------------
def dist(pt1, pt2):
  return math.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])
  
def build_graph(arq): # Points
  n = int(arq.readline())
  Graph, points = [], []
  for line in arq:
    l,x,y = map(float, line.split())
    points.append((x,y))
  for i in range(n):
    Graph.append([dist(points[i], points[j]) for j in range(n)])
  return Graph, points
  
# Ploting the solution ----------------------------------------------------------------------------------

def plot(bestTour):
    x = [points[v][0] for v in bestTour]
    x.append(x[0])
    y = [points[v][1] for v in bestTour]
    y.append(y[0])
    pyplot.plot(x, y, linewidth = 0.3)
    pyplot.scatter(x, y, s = 10, color = 'b')
    pyplot.scatter(points[0][0], points[0][1], s = 10, color = 'r')
    for v in bestTour: pyplot.annotate(v + 1, points[v])
    pyplot.show()

# Tabu search method-------------------------------------------------------------------------------------

def tabu_search(cur_sol, Graph, it, tabu_list_size):

  tabu_list = list()
  best_sol = cur_sol.copy()
    
  while it > 0:
    it -= 1
    neighborhood = cur_sol.gen_neighbors(Graph)
    for X in neighborhood:
      move, neighbor = X[1], X[0]
      if move in tabu_list or move[::-1] in tabu_list:
        # Aspiration
        if neighbor.cost < best_sol.cost:
          cur_sol = neighbor
          bets_sol = neighbor.copy()
          tabu_list.append(move)
          break
      else:
        cur_sol = neighbor
        tabu_list.append(move)
        if cur_sol.cost < best_sol.cost: best_sol = neighbor.copy()
        break
        
    if len(tabu_list) > tabu_list_size: tabu_list.pop(0)
    
  return best_sol
  
def run_tabu_search(source, Graph, max_iterations, tabu_list_size):
  
  grid_sol = Solution(len(Graph), source, Graph) 
  return tabu_search(grid_sol, Graph, max_iterations, tabu_list_size)
  
#Execution of the Tabu search method for all possible sources---------------------------------------------

arq = open('Dantzing42')
max_it, tabu_list_size = map(int, arq.readline().split())
Graph, points = build_graph(arq)
solutions = []

for i in range(len(Graph)):
  x = run_tabu_search(i, Graph, max_it, tabu_list_size)
  print("Source = " + str(i)+ ", Cost = " + str(x.cost))
  solutions.append(x)
  
solutions.sort(key = lambda x : x.cost)
print("\nBest Cost = " + str(solutions[0].cost))
print("Tour = ", solutions[0].tour)
plot(solutions[0].tour)
arq.close()
