import bpy
from ..polygon import Polygon
from ..ellipse import Ellipse

class CreateEllipse(bpy.types.Operator):
    """Ellipse Creation Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.create_ellipse"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Create an Ellipse"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    a: bpy.props.FloatProperty(name="Semi axis A", default=12)
    b: bpy.props.FloatProperty(name="Semi axis B", default=12)
    alternate_focus: bpy.props.BoolProperty(name="Alternate focus", default=True)
    imprecision: bpy.props.FloatProperty(name="Imprecision", default=10, min=1, max=10)
    divisions: bpy.props.IntProperty(name="Divisions", default=12, min=1, max=100000)
    
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
