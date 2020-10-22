import bpy
import math
import mathutils
from .polygon import Polygon
from .object import Object

class Ellipse(Object):
    def __init__(self, name, x, y, z, a, b, imprecision=.1, alternate_focus=True, divisions=12, drawArea=True):
        self.name = name
        self.alternate_focus = alternate_focus
        self.imprecision = imprecision
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
        vec = mathutils.Vector((0, 0))
        if self.alternate_focus:
            c *= -1
        if self.a > self.b:
            vec[0] = c
        else:
            vec[1] = c
        return vec
    
    def generate_geometry(self):
        areaSingle = self.get_area() / self.divisions
        margin = 0 if (self.a > self.b) else 50
        dots, edges, self.areaPoints = [], [], []
        
        focus = self.get_focus()
        polygon = Polygon(0, 0)
        dots.append(mathutils.Vector((0, 0, 0)))

        i = 0
        h = 1
        while True:
            
            #get actual point position
            actualPos = mathutils.Vector((self.a*math.cos(i) + focus[0], self.b*math.sin(i) + focus[1], 0))

            #add actualPos vertice
            dots.append(actualPos)
            
            #check if i is greater than 2PI
            if i >= 2*math.pi:
                break

            #add ellipse edges
            edges.append((h, h + 1))

            #add a new point to the polygon
            polygon.add_point(actualPos[0], actualPos[1])

            #check if area is greater than single area size
            if polygon.get_area() >= areaSingle:
                #reset area
                polygon.clear_area()

                #draw edge from focus to area vertice
                if self.drawArea:
                    edges.append((0, h))
                
                #store area vertice percentage
                self.areaPoints.append(margin + ((i - self.imprecision) * 100)/(2 * math.pi))
            
            h += 1
            i += self.imprecision
        
        #create the last edge for the remaining area
        if self.drawArea:
            edges.append((1, 0))
        
        #store the last vertice percentage to follow path constraint
        self.areaPoints.append(margin + 100)

        #connects last vertice of the ellipse with the first one
        edges.append((len(dots)-1, 1))
        
        return {
            "dots": dots,
            "edges": edges
        }
    
    def adjust_inclination(self, ascending_node, inclination, periapsis, true_anomaly):
        self.select(True)
        self.rotate(periapsis + true_anomaly, 'Z', 'NORMAL')
        self.rotate(-inclination, 'X', 'NORMAL')
        self.rotate(ascending_node, 'Z', 'NORMAL')

    def create_mesh(self):
        self.mesh = bpy.data.meshes.new(self.name + "Mesh")
        geometry = self.generate_geometry()
        self.mesh.from_pydata(geometry["dots"], geometry["edges"], [])
        return self.mesh
    
    def create_object(self):
        self.object = bpy.data.objects.new(self.name, self.mesh)

        self.object.location = self.pos

        self.mesh.update()
        return self.object
    
    def add_to_scene(self):
        bpy.context.collection.objects.link(self.object)
