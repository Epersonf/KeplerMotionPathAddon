import bpy
import math
import mathutils
from .polygon import Polygon
from .object import Object

class Ellipse(Object):
    def __init__(self, name, x, y, z, a, b, precision=.1, alternate_focus=True, divisions=12, drawArea=True):
        self.name = name
        self.alternate_focus = alternate_focus
        self.precision = precision
        self.pos = (x, y, z)
        self.a = a
        self.b = b
        self.divisions = divisions
        self.drawArea = drawArea
        self.create_mesh()
        self.create_object()
        self.add_to_scene()
    
    def get_area(self):
        return math.pi * self.a * self.b
    
    def get_focus(self):
        squareC = math.pow(self.a, 2) - math.pow(self.b, 2)
        c = math.sqrt(abs(squareC))
        vec = [0, 0]
        if self.alternate_focus:
            c *= -1
        if self.a > self.b:
            vec[0] = c
        else:
            vec[1] = c
        return vec
    
    def generate_geometry(self):
        areaSingle = self.get_area() / self.divisions
        
        self.areaPoints = []

        dots = []
        edges = []
        
        focus = self.get_focus()
        polygon = Polygon(focus[0], focus[1])
        
        i = 0
        h = 1
        dots.append((focus[0], 0, focus[1]))
        while True:
            
            actualPos = (self.a*math.cos(i), 0, self.b*math.sin(i))
            dots.append(actualPos)
            
            i += self.precision
            
            if i < 2*math.pi:
                edges.append((h, h + 1))
            else:
                break

            polygon.add_point(actualPos[0], actualPos[2])
            if polygon.calculate_area() >= areaSingle:
                polygon.clear_area()
                if self.drawArea:
                    edges.append((0, h))
                self.areaPoints.append(i/(2*math.pi))
                print(i/(2*math.pi))
            
            h += 1
        
        if self.drawArea:
            edges.append((len(dots) - 1, 0))
        self.areaPoints.append(1)
        edges.append((len(dots) - 1, 1))
        
        return {
            "dots": dots,
            "edges": edges
        }
    
    def create_mesh(self):
        self.mesh = bpy.data.meshes.new(self.name + "Mesh")
        geometry = self.generate_geometry()
        self.mesh.from_pydata(geometry["dots"], geometry["edges"], [])
        return self.mesh
    
    def create_object(self):
        self.object = bpy.data.objects.new(self.name, self.mesh)
        self.object.location = self.pos
        self.object.show_name = True
        self.mesh.update()
        return self.object
    
    def add_to_scene(self):
        bpy.context.collection.objects.link(self.object)
