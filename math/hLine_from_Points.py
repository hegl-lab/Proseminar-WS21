# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 14:34:28 2021

@author: Simon Heidrich
"""
import math
from hyperbolic import util
from hyperbolic.euclid.shapes import Circle, Arc, Line as ELine
from hyperbolic.euclid import intersection
from hyperbolic.poincare.shapes import Hypercycle

def fromPoints( x1, y1, x2, y2, segment=False, **kwargs):
    if util.nearZero(x1-x2) and util.nearZero(y1-y2):
        raise ValueError('Start and end points are the same')
    if _pointsInlineWithOrigin(x1, y1, x2, y2):
        if segment:
            shape = ELine(x1, y1, x2, y2)
            return (shape,True)
        else:
            lineRad = math.atan2(y2-y1, x2-x1)
            sx, sy = math.cos(lineRad), math.sin(lineRad)
            shape = ELine(-sx, -sy, sx, sy)
            return (shape,False)
    r1 = math.hypot(x1, y1)
    r2 = math.hypot(x2, y2)
    if util.nearZero(r1-1) and util.nearZero(r2-1):
        # Both points are ideal points so circInv will not give a 3rd points
        a1 = math.atan2(y1, x1)
        a2 = math.atan2(y2, x2)
        swap = (a2 - a1) % (math.pi*2) > math.pi
        if swap:
            a1, a2 = a2, a1
        aDiff = (a2 - a1) % (math.pi*2)
        assert aDiff <= math.pi
        centerDist = 1/math.cos(aDiff/2)
        centerAng = a1 + aDiff/2
        cx = math.cos(centerAng) * centerDist
        cy = math.sin(centerAng) * centerDist
        r = centerDist * math.sin(aDiff/2)
        arcDeg = 180 - math.degrees(aDiff)
        arcStartDeg = math.degrees(a1) - 90
        arcEndDeg = arcStartDeg - arcDeg
        if swap:
            arcStartDeg, arcEndDeg = arcEndDeg, arcStartDeg
        arc = Arc(cx, cy, r, arcEndDeg, arcStartDeg, cw=swap)
        return (arc,False)
        # Even if segment is True, the given points span the
        # entire line so it isn't a segment
    else:
        exMid = True
        if util.nearZero(r1-1):
            x3, y3 = util.circInv(x2, y2)
            if r2 > 1:
                exMid = False
        else:
            x3, y3 = util.circInv(x1, y1)
            if r1 > 1:
                exMid = False
        arc = Arc.fromPoints(x1, y1, x2, y2, x3, y3, excludeMid=exMid)
        if segment:
            return (arc,True)
        else:
            x1, y1, x2, y2 = intersection.circleCircle(arc, Circle(0,0,1))
            if arc.cw:
                x1, y1, x2, y2 = x2, y2, x1, y1
            arcFull = Arc.fromPoints(x1, y1, x2, y2, x3, y3, excludeMid=exMid)
            assert arc.cw == arcFull.cw
            return (arcFull,False)
