import math
import numpy as np
import re
import math

matrisen = np.linalg.inv([[1, 3, 3],
                          [1, 4, 3],
                          [1, 3, 4]])

matrise2 = np.linalg.inv([[97280, -23040], [-23040, 30720]])

class Truss:
    """
    a truss can take loads
    """
    def __init__(self, line):
        print(repr(line))
        #match = re.match(r"\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)", line)
        match = re.match(
            r"\((\d+), (\d+)\)"
            r", "
            r"\(([0-9]+), (\d+)\)"
            r", "
            r"(\d+e-?\d+)"
            r", "
            r"(\d+e-?\d+)", line)
        start1, start2, end1, end2, E, A = match.groups()
        start = (float(start1), float(start2))
        end = (float(end1), float(end2))
        E = float(E)
        A = float(A)

        self.start = start
        self.end = end
        self.E = E
        self.A = A
        self.length = self.get_length()

    def get_length(self):
        x1 = self.start[0]
        x2 = self.end[0]
        y1 = self.start[1]
        y2 = self.end[1]
        x = x2 - x1
        y = y2 - y1
        return math.sqrt(x**2 + y**2)

    def __repr__(self):
        return f"\nstart:{self.start}, end:{self.end}"

#for node in nodes:

trusses = []
with open("example1.txt") as f:
    for line in f:
        line = line.rstrip()
        if re.search(r"^ ", line):
            pass
        else:
            trusses.append(Truss(line))



print(trusses)
#print(matrise2)