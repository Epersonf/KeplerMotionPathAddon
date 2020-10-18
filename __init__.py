bl_info = {
    "name": "Kepler Motion Path",
    "author": "Eperson",
    "description": "Generates an ellipse",
    "blender": (2, 83, 7)
}

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

class Ellipse:
    def __init__(self, name, x, y, z, a, b, precision=.1, alternate_focus=True, divisions=12):
        self.name = name
        self.alternate_focus = alternate_focus
        self.precision = precision
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.divisions = divisions
    
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
                edges.append((0, h))
            
            h += 1
        
        edges.append((len(dots) - 1, 0))
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
        self.object.location = (self.x, self.y, self.z)
        self.object.show_name = True
        self.mesh.update()
        return self.object
    
    def add_to_scene(self):
        bpy.context.collection.objects.link(self.object)


class CreateEllipse(bpy.types.Operator):
    """Ellipse Creation Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.create_ellipse"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Create an Ellipse"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    a: bpy.props.FloatProperty(name="Semi axis A", default=12)
    b: bpy.props.FloatProperty(name="Semi axis B", default=12)
    alternate_focus: bpy.props.BoolProperty(name="Alternate focus", default=True)
    imprecision: bpy.props.FloatProperty(name="Imprecision", default=10, min=1, max=10)
    divisions: bpy.props.IntProperty(name="Divisions", default=12, min=1, max=1000)
    
    def execute(self, context):
        #Create Elipse
        pos = bpy.context.scene.cursor.location
        ellipse = Ellipse("Ellipse", pos[0], pos[1], pos[2], self.a, self.b, self.imprecision/1000, self.alternate_focus, self.divisions)
        ellipse.create_mesh()
        ellipse.create_object()
        ellipse.add_to_scene()
        return {"FINISHED"}

def register():
    bpy.utils.register_class(CreateEllipse)

def unregister():
    bpy.utils.unregister_class(CreateEllipse)

if __name__ == "__main__":
    register()

