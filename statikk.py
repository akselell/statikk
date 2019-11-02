import math
import re
import numpy as np

class Beam:
    """
    A beam can take loads
    """
    def __init__(self, start, end, E, A, u1, u2, u3, u4, u5, u6):
        self.start = start
        self.end = end
        self.E = E
        self.A = A
        self.degrees = [u1, u2, u3, u4, u5, u6]
        self.length = self.get_length()
        self.l = self.get_l()
        self.m = self.get_m()
        self.n = self.get_n()
        self.matrix = self.get_local_matrix()

    def get_length(self):
        x1 = self.start[0]
        x2 = self.end[0]
        y1 = self.start[1]
        y2 = self.end[1]
        z1 = self.start[2]
        z2 = self.end[2]
        x = x2 - x1
        y = y2 - y1
        z = z2 - z1
        return math.sqrt(x**2 + y**2 + z**2)

    def get_l(self):
        x1 = self.start[0]
        x2 = self.end[0]
        return (x2-x1)/self.get_length()

    def get_m(self):    
        y1 = self.start[1]
        y2 = self.end[1]
        return (y2-y1)/self.get_length()
    
    def get_n(self):    
        z1 = self.start[2]
        z2 = self.end[2]
        return (z2-z1)/self.get_length()

    def get_local_matrix(self):

        matrix = np.array([
                     [self.l**2, self.l*self.m, self.l*self.n, -self.l**2, -self.l*self.m, -self.l*self.n],
                     [self.l*self.m, self.m**2, self.m*self.n, -self.l*self.m, -self.m**2, -self.m*self.n],
                     [self.l*self.n, self.m*self.n, self.n**2, -self.l*self.n, -self.m*self.n, -self.n**2],
                     [-self.l**2, -self.l*self.m, -self.l*self.n, self.l**2, self.l*self.m, self.l*self.n],
                     [-self.l*self.m, -self.m**2, -self.m*self.n, self.l*self.m, self.m**2, self.m*self.n],
                     [-self.l*self.n, -self.m*self.n, -self.n**2, self.l*self.n, self.m*self.n, self.n**2]
        ])
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] *= (self.E * self.A)/self.length
        return matrix

    def __repr__(self):
        return f"\n start:{self.start}, end:{self.end} matrix: \n{np.round(self.matrix)}" 

def get_displacements(Keff, force):
    return np.dot(np.linalg.inv(Keff), force)

def get_elements(line):
    print(repr(line))
    match = re.match(
        r"\((\d+), (\d+), (\d+)\)"
        r", "
        r"\((\d+), (\d+), (\d+)\)"
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
    start1, start2, start3, end1, end2, end3, E, A, u1, u2, u3, u4, u5, u6 = match.groups()
    start = (float(start1), float(start2), float(start3))
    end = (float(end1), float(end2), float(end3))
    E = float(E)
    A = float(A)
    u1 = int(u1)
    u2 = int(u2)
    u3 = int(u3)
    u4 = int(u4)
    u5 = int(u5)
    u6 = int(u6)
    return start, end, E, A, u1, u2, u3, u4, u5, u6


def main():
    trusses = []
    with open("example1.txt") as f:
        for line in f:
            line = line.rstrip()
            if re.search(r"^#", line):
                pass
            elif re.search(r"^Force", line):
                x = re.split(r"\s", line)
                us = len(x) - 1
                force =  np.zeros( (len(x)-1,1) )
                for i in range(len(x)-1):
                    force[i][0] += float(x[i+1])
                print(f"\n Force vektor:\n{force}")
            else:
                start, end, E, A, u1, u2, u3, u4, u5, u6 = get_elements(line)
                trusses.append(Beam(start, end, E, A, u1, u2, u3, u4, u5, u6))
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


if __name__ == "__main__":
    main()
