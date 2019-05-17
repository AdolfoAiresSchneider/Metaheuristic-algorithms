import copy
import random

class Solution:
  
	# Update the cost of the solution
  def update_fitness(self, Graph):
    self.fitness = 0
    for i in range(self.N):
      u = self.permutation[i]
      for edge in Graph[u]:
        v, cost = edge[1], edge[0]
        if v == self.permutation[i+1]:
          self.fitness += cost
          break
       
  # Generate a greed solutuion(not the best one)
  def __init__(self, n = 0, source = 0, Graph = []):
    if n == 0:
      return
    self.permutation = [] 		# Solution
    self.N = n     		# Number of vertices
    self.fitness = 0	# Quality of the solution
    
    cur_node, self.fitness = source, 0
    while cur_node not in self.permutation:
      for edge in Graph[cur_node]:
        v = edge[1]
        if v not in self.permutation:
          self.permutation.append(cur_node)
          cur_node = v
          break
      if len(self.permutation) == self.N-1:
        break
    
    self.permutation.append(cur_node), self.permutation.append(source)
    self.update_fitness(Graph)
  
  # Generate the neighborhood of this solution by randomly swapping two citys
  def gen_neighbors(self, Graph):
    neighbors = []
    for i in range(1, self.N-1):
      j = random.randint(i+1, self.N-1)
      y = copy.deepcopy(self)
      v1, v2 = self.permutation[i], self.permutation[j]
      y.permutation[i], y.permutation[j] = v2, v1
      y.update_fitness(Graph)
      neighbors.append((y, (v1, v2)))

    neighbors.sort(key = lambda x : x[0].fitness)
    return neighbors
  pass # End of class definition

# Build the graph of the TSP instance
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

# Tabu search method - Local search starting at the fisrt_sol maintain a Tabu list of size tbl_size
def tabu_search(cur_sol, Graph, max_it, tbl_size, tabu_list = list()):
  best_sol = copy.deepcopy(cur_sol)
  cnt = 1
  while cnt <= max_it:
    cnt += 1
    neighborhood = cur_sol.gen_neighbors(Graph)
    for new_sol in neighborhood:
      move, neighbor = new_sol[1], new_sol[0]
      if move in tabu_list or move[::-1] in tabu_list:
        if neighbor.fitness < cur_sol.fitness:
          cur_sol = copy.deepcopy(neighbor)
          tabu_list.append(move)
          break
      else:
        tabu_list.append(move)
        cur_sol = copy.deepcopy(neighbor)
        if cur_sol.fitness < best_sol.fitness:
          best_sol = copy.deepcopy(neighbor)
        break
    
    if len(tabu_list) > tbl_size:
      tabu_list.pop(0)
  
  return best_sol

# Run the Tabu search method with a start city called source.
# source = First and last city for the TSP tour 
def run_ts(source, Graph, max_iterations, tabu_list_siz):
  grid_sol = Solution(len(Graph)-1, source, Graph) 
  final_sol = tabu_search(grid_sol, Graph, max_iterations, tabu_list_siz)
  return final_sol
  
#Execution of the Tabu search method for all possible sources
arq = open('in')
Graph = build_graph(arq)
sols = []

for i in range(1, 52):
  x = run_ts(i, Graph, 100, 10)
  print([i, x.fitness, len(x.permutation)])
  sols.append(x)
  
sols.sort(key = lambda x : x.fitness)
print(sols[0].fitness, sols[0].permutation)
arq.close()
