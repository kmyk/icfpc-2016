#!/usr/bin/env python3
from fractions import Fraction

class problem(object):

    def __init__(self, polygons, skeltons):
        # shallow copy
        self.polygons = polygons
        self.skeltons = skeltons

        self.left = float('inf')
        self.bottom = float('inf')
        self.top = 0
        self.right = 0
        for polygon in self.polygons:
            for x, y in polygon:
                self.left   = min(self.left,   x)
                self.right  = max(self.right,  x)
                self.bottom = min(self.bottom, y)
                self.top    = max(self.top,    y)

    @classmethod
    def input_from(cls, fh):
        # read polygons
        polygons = []
        polygon_num = int(fh.readline().strip())
        for _ in range(polygon_num):
            vertices = []
            vertex_num = int(fh.readline().strip())
            for _ in range(vertex_num):
                x, y = map(Fraction, fh.readline().strip().split(','))
                vertices += [(x, y)]
            polygons += [vertices]
        # read skeltons
        skeltons = []
        skelton_num = int(fh.readline().strip())
        for _ in range(skelton_num):
            a, b = fh.readline().split()
            ax, ay = map(Fraction, a.split(','))
            bx, by = map(Fraction, b.split(','))
            skeltons += [((ax, ay), (bx, by))]
        # return
        return problem(polygons, skeltons)


class solution(object):

    def __init__(self):
        # shallow copy
        self.sources      = []
        self.facets       = []
        self.destinations = []

    def output_to(self, fh):
        print(len(self.sources), file=fh)
        for x, y in self.sources:
            print(x, y, file=fh)
        print(len(self.facets), file=fh)
        for facet in self.facets:
            print(len(facet), *facet, file=fh)
        for x, y in self.destinations:
            print(x, y, file=fh)

import sys
p = problem.input_from(sys.stdin)
s = solution()
s.sources += [ (0, 0), (1, 0), (1, 1), (0, 1) ]
s.facets += [ [ 0, 1, 2, 3 ] ]
s.destinations += [ (p.left + x, p.bottom + y) for x, y in s.sources ]
s.output_to(sys.stdout)
