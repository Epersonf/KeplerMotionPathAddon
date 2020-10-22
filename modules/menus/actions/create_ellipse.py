import bpy
from ...ellipse import Ellipse

class CreateEllipse(bpy.types.Operator):
    """Ellipse Creation Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.create_ellipse"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Create an Ellipse"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    #Parameters
    a: bpy.props.FloatProperty(name="Semi axis A", default=12, min=.1)
    b: bpy.props.FloatProperty(name="Semi axis B", default=12, min=.1)

    #Inclination
    ascending_node: bpy.props.FloatProperty(name="Longitude of the ascending node", default=0)
    inclination: bpy.props.FloatProperty(name="Inclination", default=0)
    periapsis: bpy.props.FloatProperty(name="Argument of periapsis", default=0)

    #Other
    alternate_focus: bpy.props.BoolProperty(name="Alternate focus", default=True)
    imprecision: bpy.props.FloatProperty(name="Imprecision", default=10, min=.01, max=100)
    divisions: bpy.props.IntProperty(name="Divisions", default=2000, min=1, max=100000)
    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Ellipse Options")
        row = layout.row()
        row.prop(self, "a")
        row.prop(self, "b")

        layout.separator()

        row = layout.row()
        row.label(text="Orientation Options")
        row = layout.row()
        row.prop(self, "ascending_node")
        row = layout.row()
        row.prop(self, "inclination")
        row = layout.row()
        row.prop(self, "periapsis")

        layout.separator()

        row = layout.row()
        row.label(text="Other options")
        row = layout.row()
        row.prop(self, "alternate_focus")
        row = layout.row()
        row.prop(self, "imprecision")
        row = layout.row()
        row.prop(self, "divisions")

    def execute(self, context):
        #Unselect all
        bpy.ops.object.select_all(action='DESELECT')
        #Get Position of Cursor
        pos = bpy.context.scene.cursor.location
        #Create Ellipse
        ellipse = Ellipse("Ellipse", pos[0], pos[1], pos[2], self.a, self.b, self.imprecision/1000, self.alternate_focus, self.divisions)
        #Adjust ellipse orientation
        ellipse.adjust_inclination(self.ascending_node, self.inclination, self.periapsis)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(CreateEllipse)

def unregister():
    bpy.utils.unregister_class(CreateEllipse)