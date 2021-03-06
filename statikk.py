import math
import re
import numpy as np
import time
import sys


class Beam:
    """
    A beam can take loads
    """
    def __init__(self, start, end, E, A, I, u1, u2, u3, u4, u5, u6):
        self.start = start
        self.end = end
        self.E = E
        self.A = A
        self.I = I
        self.degrees = [u1, u2, u3, u4, u5, u6]
        self.length = self.get_length()
        self.c = self.get_c()
        self.s = self.get_s()
        self.matrix = self.get_local_matrix()

    def get_length(self):
        x1 = self.start[0]
        x2 = self.end[0]
        y1 = self.start[1]
        y2 = self.end[1]
        x = x2 - x1
        y = y2 - y1
        return math.sqrt(x**2 + y**2)

    def get_c(self):
        x1 = self.start[0]
        x2 = self.end[0]
        return (x2-x1)/self.get_length()

    def get_s(self):    
        y1 = self.start[1]
        y2 = self.end[1]
        return (y2-y1)/self.get_length()

    def get_local_matrix(self):
        k = np.array([
                      [(self.E*self.A)/self.length, 0, 0, -(self.E*self.A)/self.length, 0, 0],
                      [0, (12*self.E*self.I)/self.length**3, (6*self.E*self.I)/self.length**2, 0, -(12*self.E*self.I)/self.length**3, (6*self.E*self.I)/self.length**2],
                      [0, (6*self.E*self.I)/self.length**2, (4*self.E*self.I)/self.length, 0, -(6*self.E*self.I)/self.length**2, (2*self.E*self.I)/self.length],
                      [-(self.E*self.A)/self.length, 0, 0, (self.E*self.A)/self.length, 0, 0],
                      [0, -(12*self.E*self.I)/self.length**3, -(6*self.E*self.I)/self.length**2, 0, (12*self.E*self.I)/self.length**3, -(6*self.E*self.I)/self.length**2],
                      [0, (6*self.E*self.I)/self.length**2, (2*self.E*self.I)/self.length, 0, -(6*self.E*self.I)/self.length**2, (4*self.E*self.I)/self.length]
                      ])
        t = np.array([
                      [self.c, self.s, 0, 0, 0, 0],
                      [-self.s, self.c, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, self.c, self.s, 0],
                      [0, 0, 0, -self.s, self.c, 0],
                      [0, 0, 0, 0, 0, 1]
                      ])
        tt = t.transpose()
        a = np.dot(tt, k)
        return np.dot(a, t)

    def __repr__(self):
        return f"\n start:{self.start}, end:{self.end}, dof:{self.degrees} matrix: \n {np.round(self.matrix)}"

def get_displacements(Keff, force):
    return np.dot(np.linalg.inv(Keff), force)

def get_elements(line):
    print(repr(line))
    match = re.match(
        r"\((\d+), (\d+)\)"
        r", "
        r"\(([0-9]+), (\d+)\)"
        r", "
        r"(\d+e-?\d+)"
        r", "
        r"(\d+e-?\d+)"
        r", "
        r"(\d+e-?\d+)"
        r", "
        r"(\d+)"
        r", "
        r"(\d+)"
        r", "
        r"(\d+)"
        r", "
        r"(\d+)"
        r", "
        r"(\d+)"
        r", "
        r"(\d+)", line)
    start1, start2, end1, end2, E, A, I, u1, u2, u3, u4, u5, u6 = match.groups()
    start = (float(start1), float(start2))
    end = (float(end1), float(end2))
    E = float(E)
    A = float(A)
    I = float(I)
    u1 = int(u1)
    u2 = int(u2)
    u3 = int(u3)
    u4 = int(u4)
    u5 = int(u5)
    u6 = int(u6)
    return start, end, E, A, I, u1, u2, u3, u4, u5, u6

def calculate_element_forces(trusses, displ):
    y = 1
    for truss in trusses:
        displa =  np.zeros( (6,1) )
        i = 0
        for u in truss.degrees:
            if u != 0:
                displa[i][0] += displ[u-1][0]
            i += 1
#        print("\n", displa, "gg")
        force = np.dot(truss.matrix, displa)
        print("\n ", y, "\n", force)
        y += 1    
#        return force


def main():
    starttime = time.time()
    trusses = []
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.rstrip()
            if re.search(r"^#", line):
                pass
            elif re.search(r"^Force", line):
                x = re.split(r"\s", line)
                us = len(x) - 1
                force =  np.zeros( (us,1) )
                for i in range(us):
                    force[i][0] += float(x[i+1])
                print(f"\n Force vektor:\n{force}")
            else:
                start, end, E, A, I, u1, u2, u3, u4, u5, u6 = get_elements(line)
                trusses.append(Beam(start, end, E, A, I, u1, u2, u3, u4, u5, u6))
    counter = 1
    for truss in trusses:
        print(f"\n Element {counter} matrix:{truss}")
        counter += 1
    Keff = np.zeros( (us,us) )
    for truss in trusses:
        i = 0
        for u in truss.degrees:
            if u != 0:
                j = 0
                for u2 in truss.degrees:
                    if u2 != 0:
                        Keff[u-1][u2-1] += truss.matrix[i][j]
                    j += 1
            i += 1
    print(f"\n Keff: \n{np.round(Keff, 2)}")
    displ = get_displacements(Keff, force)
    print(f"\n Displacements: \n{displ}")
    print(f"\n {round(time.time() - starttime, 4)} sec to complete")
    print(calculate_element_forces(trusses, displ))

if __name__ == "__main__":
    main()
