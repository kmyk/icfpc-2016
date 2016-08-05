#!/usr/bin/env python3
from fractions import Fraction

def write_to_png(fh, callback):
    import cairo
    WIDTH  = 512
    HEIGHT = 512

    # init
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(WIDTH, HEIGHT)

    # invert the coordinates
    ctx.scale(1, -1)
    ctx.translate(0, -1)

    # write background
    ctx.set_source_rgba(0, 0, 0, 0) # transparent
    ctx.rectangle(0, 0, 1, 1) # entire of the surface
    ctx.fill()

    # make margin
    ctx.translate(0.1, 0.1)
    ctx.scale(0.8, 0.8)

    # write border
    ctx.set_source_rgb(0, 0, 0) # black
    ctx.set_line_width(0.01) # thin
    ctx.rectangle(0, 0, 1, 1)
    ctx.stroke()

    # callback
    callback(ctx)

    # fin
    surface.write_to_png(fh.buffer)


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

    def output_to(self, fh):
        def cont(ctx):
            # write polygons
            ctx.set_source_rgba(0.8, 0.4, 0.4, 0.6) # red
            ctx.set_line_width(0.01) # thin
            for polygon in self.polygons:
                x, y = polygon[-1]
                ctx.move_to(float(x - self.left), float(y - self.bottom))
                for x, y in polygon:
                    ctx.line_to(float(x - self.left), float(y - self.bottom))
                ctx.fill()

            # write skeltons
            ctx.set_source_rgba(0.5, 0, 0, 1) # red
            for skelton in self.skeltons:
                x, y = skelton[0]
                ctx.move_to(float(x - self.left), float(y - self.bottom))
                x, y = skelton[1]
                ctx.line_to(float(x - self.left), float(y - self.bottom))
                ctx.stroke()

        write_to_png(fh, cont)


class solution(object):

    def __init__(self, sources, facets, destinations):
        # shallow copy
        self.sources      = sources
        self.facets       = facets
        self.destinations = destinations

        self.left = float('inf')
        self.bottom = float('inf')
        self.top = 0
        self.right = 0
        for x, y in self.sources:
            self.left   = min(self.left,   x)
            self.right  = max(self.right,  x)
            self.bottom = min(self.bottom, y)
            self.top    = max(self.top,    y)

    @classmethod
    def input_from(cls, fh):
        # read source positions
        sources = []
        source_num = int(fh.readline().strip())
        for _ in range(source_num):
            x, y = map(Fraction, fh.readline().strip().split(','))
            sources += [(x, y)]
        # read facets
        facets = []
        facet_num = int(fh.readline().strip())
        for _ in range(facet_num):
            facet = list(map(int, fh.readline().split()))[1:]
            facets += [facet]
        # read destination positions
        destinations = []
        for _ in range(source_num):
            x, y = map(Fraction, fh.readline().strip().split(','))
            destinations += [(x, y)]
        # return
        return solution(sources, facets, destinations)

    def output_to(self, fh, typ):
        # decide points
        if typ == 's':
            points = self.sources
        elif typ == 'd':
            points = self.destinations
        else:
            raise ValueError

        def cont(ctx):
            # write points
            ctx.set_line_width(0.01) # thin
            for facet in self.facets:
                x, y = points[facet[-1]]
                ctx.move_to(float(x - self.left), float(y - self.bottom))
                for i in facet:
                    x, y = points[i]
                    ctx.line_to(float(x - self.left), float(y - self.bottom))
                ctx.set_source_rgba(0.8, 0.4, 0.4, 0.6) # red
                ctx.fill_preserve()
                ctx.set_source_rgba(0.5, 0, 0, 1) # red
                ctx.stroke()

        write_to_png(fh, cont)

if __name__ == '__main__':
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--problem', action='store_true')
    group.add_argument('-s', '--solution', choices=[ 's', 'sources', 'd', 'destinations' ])
    parser.add_argument('input', nargs='?')
    parser.add_argument('output', nargs='?')
    args = parser.parse_args()

    if args.input:
        inf = open(args.input)
    else:
        inf = sys.stdin
    if args.output:
        outf = open(args.output)
    else:
        outf = sys.stdout
    if args.problem:
        problem.input_from(inf).output_to(outf)
    elif args.solution:
        solution.input_from(inf).output_to(outf, args.solution[0])
