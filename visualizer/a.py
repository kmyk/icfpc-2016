#!/usr/bin/env python3
from fractions import Fraction

class problem(object):

    def __init__(self, polygons, skeltons):
        # shallow copy
        self.polygons = polygons
        self.skeltons = skeltons

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

    def output_to(self, fh, SIZE=256):
        import cairo
        WIDTH = 256
        HEIGHT = 256
        MARGIN = 28

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx = cairo.Context(surface)
        ctx.scale(WIDTH, HEIGHT)
        # invert the coordinates
        ctx.scale(1, -1)
        ctx.translate(0, -1)

        ctx.set_source_rgba(0, 0, 0, 0) # transparent
        ctx.rectangle(0, 0, 1, 1) # entire of the surface
        ctx.fill()

        ctx.set_source_rgba(0.8, 0.4, 0.4, 0.6) # red
        ctx.set_line_width(0.01) # thin
        for polygon in self.polygons:
            x, y = polygon[-1]
            ctx.move_to(float(x), float(y))
            for x, y in polygon:
                ctx.line_to(float(x), float(y))
            ctx.fill()

        ctx.set_source_rgba(0.5, 0, 0, 1) # red
        for skelton in self.skeltons:
            x, y = skelton[0]
            ctx.move_to(float(x), float(y))
            x, y = skelton[1]
            ctx.line_to(float(x), float(y))
            ctx.stroke()

        surface.write_to_png(fh.buffer)

import sys
problem.input_from(sys.stdin).output_to(sys.stdout)
