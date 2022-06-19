from collections import defaultdict
from data_structures.graph import Graph
from data_structures.max_heap import MaxHeap, Node
from copy import deepcopy

class StoerWagner:
  def algorithm(self, G: Graph):

    """
backupG: Graph = deep copy of the starting graph for calculating the weights of the arcs
    res: tuple = tuple containing the results of the algorithm execution
    """
    backupG = deepcopy(G)
    res = self.globalMinCut(backupG)
    return res[1][0][1]
    

  def stMinCut(self, G: Graph):

    """
    Q: MaxHeap = maxheap containing the graph nodes
    key: defaultdict (list) = key map. A value is in the form key [node] = node_weight
    """
    Q = MaxHeap()
    key = defaultdict(list)

    """
    Initialization
    * For each node node of G, key [node] = 0
    * Q <- V
    * s = null, t = null: initialization of nodes s and t that the function must return
    """
    for node in G.V:
      key[node] = 0
      Q.insert(Node(node, key[node]))
    s = t = None

    """
    Calculation of nodes s and t to be returned
    As long as the Q heap is not empty
        pull out the heavyweight knot
        s <- t obtained from the previous iteration
        t <- u
        For each node v with weight w adjacent to u
          If the node is present in Q
            key [v] + = w
            update Q with the new node of index v and weight key [v]
    """
    while Q.currentSize != 0:
      u = (Q.extractMax()).toTuple()
      s = t
      t = u
      for (v, w) in G.graph[u[0]]:
        if Q.search(v):
          key[v] = key[v] + w
          Q.increaseKey(v, key[v])

    """
    Removal of t from G.V
    Each node other than t is inserted into an auxiliary node list
    """
    V_diff = []
    for x in G.V:
        if(x != t[0]):
          V_diff.append(x)

    """
    Return of function
    The function returns:
    * An s-t mincut consisting of (V_diff, [t]) with V_diff = G.V - {t}
    * The two nodes s and t
    """
    return (V_diff, [t]), s[0], t[0]


  def globalMinCut(self, G: Graph):

    """
    Base case
    If the list of nodes contains only two nodes, they are returned.
    In particular, a tuple is returned
    ([v1], [(v2, G.totalWeightCost (v1, v2))]), where
        * v1 and v2 are the two nodes corresponding to the two partitions of G.V
        * totalWeightCost (v1, v2) is the weight of the arc between v1 and v2
    """
    if len(G.V) == 2:
      v1 = G.V.pop()
      v2 = G.V.pop()
      G.V.add(v2)
      G.V.add(v1)
      return ([v1], [(v2, G.totalWeightCost(v1, v2))])

    else:

      """
      Recursive step
      StMinCut is invoked on G
      The graph is contracted with respect to s and t using the contractGraph function
      GlobalMinCut is called on the contract graph
      At full recursion, comparisons are made between C1 and C2
      """
      (C1, s, t) = self.stMinCut(G)
      contractedG = self.contractGraph(G, s, t)
      C2 = self.globalMinCut(contractedG)
      if self.weightMinCut(C1) <= self.weightMinCut(C2):
        return C1
      else:
        return C2

# Returns the weight of the minCut
  def weightMinCut(self, C: any):
    V, t = C
    return t[0][1]


  def contractGraph(self, G: Graph, s, t):
    """
    Contraction of the graph with respect to s and t
    Each side adjacent to both nodes s and t is eliminated
    Each side adjacent to t is "shifted" to s
    The node t is eliminated and the contracted graph is returned
    """
    for (u,w) in G.graph[t]:
      if u == s:
        G.remove_edge(t, u, w)
    for (u, w) in G.graph[t]:
      if u != s:
        G.add_edge(s, u, w)
    G.remove_node(t)
    return G
