from collections import defaultdict


class Graph:
    def __init__(self, count_vertices):
        self.graph = defaultdict(list)
        self.count_vertices = count_vertices

    def insert_node(self, top_node, edge_node):
        self.graph.setdefault(edge_node, [])
        self.graph[edge_node].append(top_node)

    def run_sort_topological(self, v, visited, stack): # run
        visited.append(v)
        for i in self.graph[v]:
            if i not in visited:
                self.run_sort_topological(i, visited, stack)
        stack.insert(0, v)

    def sort_topologial(self): #init
        visited = []
        stack = []
        for key in list(self.graph):
            if key not in visited:
                self.run_sort_topological(key, visited, stack)
        return stack
