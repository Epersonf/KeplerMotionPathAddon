import bpy
import math
import mathutils

class Polygon:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.clear_area()
    
    def clear_area(self):
        self.points = []
        self.add_point(self.x, self.z)
    
    def add_point(self, x, z):
        self.points.append((x, z))
    
    def calculate_area(self):    
        sum = 0
        for i in range(len(self.points)):
            point1 = self.points[i]
            point2 = self.points[(i + 1) % len(self.points)]
            sum += point1[0] * point2[1] - point1[1] * point2[0]
        return sum / 2