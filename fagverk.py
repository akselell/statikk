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
            print(f"\n Element {counter} matrix:{truss}")
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

def main():
    trusses = []
    start = 0
    end = 12
    height = 4
    for i in range(3, 10):
        lower_nodes_x = np.linspace(start, end, i)
        higher_nodes_x = np.linspace(start, end, i) 
        print(lower_nodes_x)

    lower_nodes = []
    nodes = []
    u = 1
    for x in lower_nodes_x:
        if int(x) == start:
            nodes.append(Node(x, 0, 0, 0, 0))
        if int(x) == end:
            nodes.append(Node(x, 0, u, 0, 0))
            u += 1
        else:
            nodes.append(Node(x, 0, u, u+1, 0))
            u += 2
    higher_nodes = []
    for x in higher_nodes_x:
        higher_nodes.append((x,height))
        nodes.append(Node(x, height, u, u+1, 0))
        u += 2
    print(nodes)

    for nodes :
        trusses.append()

    number_us = [] 
    for truss in trusses:
        for u in truss.degrees:
            if u != 0:
                if u not in number_us:
                    number_us.append(u)
    us = len(number_us)


#    trusses.append(Beam())

main()
