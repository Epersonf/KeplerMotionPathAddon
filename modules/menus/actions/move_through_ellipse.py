import bpy
from ...ellipse import Ellipse
from ...planet import Planet

class MoveThroughEllipse(bpy.types.Operator):
    """Motion Through Ellipse"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.motion_through_ellipse"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move Through Ellipse"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    frame_step: bpy.props.IntProperty(name="Frames per area", default=24, min=1)
    a: bpy.props.FloatProperty(name="Semi axis A", default=12, min=.1)
    b: bpy.props.FloatProperty(name="Semi axis B", default=12, min=.1)
    alternate_focus: bpy.props.BoolProperty(name="Alternate focus", default=True)
    imprecision: bpy.props.FloatProperty(name="Imprecision", default=10, min=.01, max=100)
    divisions: bpy.props.IntProperty(name="Divisions", default=2000, min=1, max=100000)

    def execute(self, context):
        if bpy.context.object is None:
            self.report({"WARNING"}, "You must select an object.")
            return {"CANCELLED"}
        pos = bpy.context.object.location
        ellipse = Ellipse("Ellipse", pos[0], pos[1], pos[2], self.a, self.b, self.imprecision/1000, self.alternate_focus, self.divisions, False)
        planet = Planet(bpy.context.object)
        planet.set_pos((0, 0, 0))

        #unselect planet
        planet.unselect()

        #select ellipse
        ellipse.select(True)
        
        #convert ellipse to curve
        bpy.ops.object.convert(target='CURVE')

        #select planet and set as active
        planet.select(True)

        #add path constraint to current selected
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')

        #add Ellipse as target
        bpy.context.object.constraints["Follow Path"].target = ellipse.object

        #select ellipse and switch to edit mode to fix bug
        ellipse.select(True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        #generate animation
        planet.animate_through_ellipse(ellipse, self.frame_step)
        
        #make animation cyclic
        planet.select(True)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(MoveThroughEllipse)

def unregister():
    bpy.utils.unregister_class(MoveThroughEllipse)    