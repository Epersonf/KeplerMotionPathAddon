import bpy
import math
import mathutils

class Polygon:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.clear_area()
        self.area = 0
    
    def clear_area(self):
        self.area = 0
        self.points = []
        self.add_point(self.x, self.z)
    
    def add_point(self, x, z):
        self.points.append(mathutils.Vector((x, z)))
        if len(self.points) > 2:
            newTriangle = self.points[-2:]
            newTriangle.append(self.points[0])
            self.area += self.calculate_area(newTriangle)
    
    def calculate_area(self, points):
        sum = 0
        for i in range(len(points)):
            point1 = points[i]
            point2 = points[(i + 1) % len(points)]
            sum += point1[0] * point2[1] - point1[1] * point2[0]
        return sum / 2

    def get_area(self):    
        return self.area