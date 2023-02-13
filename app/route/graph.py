
from math import inf

graph = {'A': {'C': 5, 'D': 1,  'E': 2},
         'B': {'H': 1, 'G': 3},
         'C': {'I': 2, 'D': 3, 'A': 5},
         'D': {'C': 3, 'A': 1, 'H': 2},
         'E': {'A': 2, 'F': 3},
         'F': {'E': 3, 'G': 1},
         'G': {'F': 1, 'B': 3, 'H': 2},
         'H': {'I': 2, 'D': 2,'B': 1, 'G': 2},
         'I': {'C': 2, 'H': 2}
         }

costs = {'A': 0,
         'B': inf,
         'C': inf,
         'D': inf,
         'E': inf,
         'F': inf,
         'G': inf,
         'H': inf,
         'I': inf}

parents = {}


class Graph:
    def __init__(self):
        self.graph = {}
        self.cost = {}
        self.parents = {}
        
    def add_node(self, parent_node, node=None):
        if node is None:
            self.graph[parent_node.fix()] = {}
            self.cost[parent_node.fix()] = inf
        else:
            self.graph[parent_node.fix()][node.fix()] = node

    def set_origin(self, node):
        self.cost[node.fix()] = 0

    def search(self, origin_node, destination_node):

        nextNode = origin_node
        self.set_origin( origin_node )
        
        while nextNode != destination_node:
            for k in self.graph[nextNode.fix()].keys():
                neighbor = self.graph[nextNode.fix()][k]
                if self.graph[nextNode.fix()][neighbor.fix()].dis() + \
                   self.cost[nextNode.fix()] < self.cost[neighbor.fix()]:
                    self.cost[neighbor.fix()] = \
                        self.graph[nextNode.fix()][neighbor.fix()].dis() + \
                    self.cost[nextNode.fix()]
                    self.parents[neighbor.fix()] = nextNode
                del self.graph[neighbor.fix()][nextNode.fix()]
            del self.cost[nextNode.fix()]
            nextNode = min(self.cost, key=self.cost.get)
            print(self.cost)
            
        return self.parents

    def get_graph(self):
        return self.graph
            
class Node:
    
    def __init__(self, fix, route_id=None, distance=0):

        self._route_id = route_id
        self._fix = fix
        self._distance = distance

    def __str__(self):
        return 'Node: ' + self._fix

    def __repr__(self):
        return f'Node(\'{self._route_id}\',{self._fix},{self._distance})'

    def dis(self):
        return self._distance

    def fix(self):
        return self._fix

    def route(self):
        return self._route_id
    
    def __ne__(self, other):
        return self._fix != other.fix()
    
    
def search(source, target, graph, costs, parents):
    nextNode = source
    while nextNode != target:
        for neighbor in graph[nextNode]:
            if graph[nextNode][neighbor] + costs[nextNode] < costs[neighbor]:
                costs[neighbor] = graph[nextNode][neighbor] + costs[nextNode]
                parents[neighbor] = nextNode
            del graph[neighbor][nextNode]
        del costs[nextNode]
        nextNode = min(costs, key=costs.get)
    return parents

def backpedal(source, target, searchResult):
    node = target
    backpath = [target]
    path = []
    while node != source:
        backpath.append(searchResult[node])
        node = searchResult[node]
    for i in range(len(backpath)):
        path.append(backpath[-i - 1])
    return path


node_a=Node( 'A' )
node_b=Node( 'B' )
node_c=Node( 'C' )
node_d=Node( 'D' )
node_e=Node( 'E' )
node_f=Node( 'F' )
node_g=Node( 'G' )
node_h=Node( 'H' )
node_i=Node( 'I' )

graph_n = Graph()
graph_n.add_node( node_a )
graph_n.add_node( node_b )
graph_n.add_node( node_c )
graph_n.add_node( node_d )
graph_n.add_node( node_e )
graph_n.add_node( node_f )
graph_n.add_node( node_g )
graph_n.add_node( node_h )
graph_n.add_node( node_i )

graph_n.add_node( node_a , Node('C','AC',5))
graph_n.add_node( node_a , Node('D','AD',1))
graph_n.add_node( node_a , Node('E','AE',2))

graph_n.add_node( node_b , Node('H','AD',1))
graph_n.add_node( node_b , Node('G','BG',3))

graph_n.add_node( node_c , Node('I','AC',2))
graph_n.add_node( node_c , Node('D','CD',3))
graph_n.add_node( node_c , Node('A','AC',5))

graph_n.add_node( node_d , Node('C','CD',3))
graph_n.add_node( node_d , Node('A','AD',1))
graph_n.add_node( node_d , Node('H','AD',2))

graph_n.add_node( node_e , Node('A','AE',2))
graph_n.add_node( node_e , Node('F','EF',3))

graph_n.add_node( node_f , Node('E','EF',3))
graph_n.add_node( node_f , Node('G','EF',1))

graph_n.add_node( node_g , Node('F','EF',1))
graph_n.add_node( node_g , Node('B','EF',3))
graph_n.add_node( node_g , Node('H','GH',2))

graph_n.add_node( node_h , Node('I','GH',2))
graph_n.add_node( node_h , Node('D','AD',2))
graph_n.add_node( node_h , Node('B','AD',1))
graph_n.add_node( node_h , Node('G','GH',2))

graph_n.add_node( node_i , Node('C','AC',2))
graph_n.add_node( node_i , Node('H','GH',2))


graph_n.search(node_a, node_b)


result = search('A', 'B', graph, costs, parents)

print('parent dictionary={}'.format(result))
print('shortest path={}'.format(backpedal('A', 'G', result)))


'''
graph = {'A': {'C': 5, 'D': 1,  'E': 2},
         'B': {'H': 1, 'G': 3},
         'C': {'I': 2, 'D': 3, 'A': 5},
         'D': {'C': 3, 'A': 1, 'H': 2},
         'E': {'A': 2, 'F': 3},
         'F': {'E': 3, 'G': 1},
         'G': {'F': 1, 'B': 3, 'H': 2},
         'H': {'I': 2, 'D': 2,'B': 1, 'G': 2},
         'I': {'C': 2, 'H': 2}
         }
'''
