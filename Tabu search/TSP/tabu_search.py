import copy
import random

class Solution:
  
  path = []
  fitness = 0
  N = 0
  
  def update_fitness(self, Graph):
    self.fitness = 0
    n = len(self.path)
    for i in range(n-1):
      u = self.path[i]
      for edge in Graph[u]:
        v, cost = edge[1], edge[0]
        if v == self.path[i+1]:
          self.fitness += cost
          break
       
  def copy(self, other):
    self.fitness = other.fitness
    self.path = copy.copy(other.path)
  
  # generate a greed solutuion(not the best one)
  def __init__(self, n = 0, source = 0, Graph = []):
    if n == 0:
      return
    self.path.clear()
    self.N = n
    cur_node, self.fitness = source, 0
    while cur_node not in self.path:
      for edge in Graph[cur_node]:
        v = edge[1]
        if v not in self.path:
          self.path.append(cur_node)
          cur_node = v
          break
      if len(self.path) == self.N-1:
        break
    
    self.path.append(cur_node)
    self.path.append(source)
    self.update_fitness(Graph)
      
  def gen_neighbors(self, Graph):
    neighbors = []
    n = len(Graph)-1
    for i in range(1, n-1):
      j = random.randint(i+1, n-1)
      new_sol = Solution()
      new_sol.copy(self)
      v1, v2 = self.path[i], self.path[j]
      new_sol.path[i], new_sol.path[j] = v2, v1
      new_sol.update_fitness(Graph)
            
      if new_sol not in neighbors:
        neighbors.append((new_sol, (v1, v2)))

    neighbors.sort(key=lambda x : x[0].fitness)
    return neighbors
  pass	
  
def build_graph(arq):
  n = int(arq.readline())
  Graph = [[] for i in range(n+1)]
  for line in arq:
    u,v,c = map(int, line.split())
    Graph[u].append((c,v))
    Graph[v].append((c,u))
  for u in range(n):
	  Graph[u].sort()
  return Graph

def tabu_search(first_sol, Graph, max_it, tbl_size):
  tabu_list = list()
  cur_sol = Solution()
  best_sol = Solution()
  cur_sol.copy(first_sol)
  best_sol.copy(cur_sol)
  
  cnt = 1
  while cnt <= max_it:
    cnt += 1
    neighborhood = cur_sol.gen_neighbors(Graph)
    for new_sol in neighborhood:
      move, neighbor = new_sol[1], new_sol[0]
      if move in tabu_list or move[::-1] in tabu_list:
        if neighbor.fitness < cur_sol.fitness:
          cur_sol.copy(neighbor)
          tabu_list.append(move)
          break # olhar isso 
      else:
        tabu_list.append(move)
        cur_sol.copy(neighbor)
        if cur_sol.fitness < best_sol.fitness:
          best_sol.copy(cur_sol)
        break # olhar isso 
    
    if len(tabu_list) > tbl_size:
      tabu_list.pop(0)
  
  return best_sol

def run_ts(source, Graph, max_it, sz_tabu_list):
  grid_sol = Solution(len(Graph)-1, source, Graph)
  final_sol = tabu_search(grid_sol, Graph, max_it, sz_tabu_list)
  return final_sol


####################################  Execution

arq = open('in')
Graph = build_graph(arq)
arq.close()

sols = []
for i in range(1, 52):
  x = run_ts(i, Graph, 100, 10)
  print([i, x.fitness, len(x.path)])
  sols.append(x)
  
sols.sort(key=lambda x : x.fitness)
print(sols[0].fitness, sols[0].path)
