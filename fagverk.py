from statikk import Beam
import numpy as np
import random

class Bridge:
    """
    Bridge
    """
    def __init__(self, start, end, trusses, us):
        self.start = start
        self.end = end
        self.trusses = trusses
        self.us = us
        self.keff = self.get_keff()

    def get_keff(self):
        counter = 1
        for truss in self.trusses:
            #print(f"\n Element {counter} matrix:{truss}")
            counter += 1
        keff = np.zeros( (self.us,self.us) )
        for truss in self.trusses:
            i = 0
            for u in truss.degrees:
                if u != 0:
                    j = 0
                    for u2 in truss.degrees:
                        if u2 != 0:
                            keff[u-1][u2-1] += truss.matrix[i][j]
                        j += 1
                i += 1
        return keff
    def __repr__(self):
        return f"{self.keff}"


class Node:
    """
    A node has placements and degrees of freedom
    """
    def __init__(self, x, y, u1, u2, u3):
        self.x = x
        self.y = y
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3

    def __repr__(self):
        return "\n x={} y={} u1={} u2={} u3={}" .format(self.x, self.y, self.u1, self.u2, self.u3)

def get_deflections(force, bridge):
    return np.dot(np.linalg.inv(bridge.Keff), force)

def main():
    trusses = []
    start = 0.0
    end = 12.0
    height = 4.0
    force = -200
    y = 1
#    for i in range(3, 10):
    for i in range(3, 4):
        lower_nodes_x = np.linspace(start, end, i)
        higher_nodes_x = np.linspace(start, end, i) 
        lower_nodes = []
        nodes = []
        u = 1
        for x in lower_nodes_x:
            if int(x) == start:
                nodes.append(Node(x, 0, 0, 0, 0))
            elif int(x) == end:
                nodes.append(Node(x, 0, u, 0, 0))
                u += 1
            else:
                nodes.append(Node(x, 0, u, u+1, 0))
                u += 2
        higher_nodes = []
        for x in higher_nodes_x:
            higher_nodes.append((x, height))
            nodes.append(Node(x, height, u, u+1, 0))
            u += 2
        u -= 2
        #print(nodes)
        nodes1 = nodes[:]
        for node1 in nodes:
            for node2 in nodes:
#                if ((node2.x, node2.y), (node1.x, node1.y), 200e6, 12e-4, 0e1, node2.u1, node2.u2, node2.u3, node1.u1, node1.u2, node1.u3) in trusses:
#                    continue
                if node1 != node2:
                    trusses.append(Beam((node1.x, node1.y), (node2.x, node2.y), 200e6, 12e-4, 0e1, node1.u1, node1.u2, node1.u3, node2.u1, node2.u2, node2.u3))
            nodes.remove(node1)
        #print(trusses)
        number_us = [] 
        for truss in trusses:
            for u in truss.degrees:
                if u != 0:
                    if u not in number_us:
                        number_us.append(u)
        us = len(number_us)
        print("fwerg", number_us)
        print("hei", us)
        
        force_per_node = force/len(higher_nodes_x)
        force_vector = np.zeros( (us,1) )
        print("he", nodes1)
        for node in nodes1:
            if node.y != 0:
                force_vector[node.u2-1][0] += force_per_node
            print(force_vector, node)
            
        #print(us)
        bridge = Bridge(start, end, trusses, us)
        #print(y ,bridge, "\n")
        y += 1
        deflections = get_deflections(force_vector, bridge)
        print(deflections)

#    trusses.append(Beam())

if __name__ == "__main__":
    main()
