import bpy
from ...ellipse import Ellipse
from ...planet import Planet

class MoveThroughEllipse(bpy.types.Operator):
    """Motion Through Ellipse"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.motion_through_ellipse"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move Through Ellipse"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    #Animation
    frame_step: bpy.props.IntProperty(name="Frames per area", default=24, min=1)
    clockwise: bpy.props.BoolProperty(name="Clockwise", default=True)

    #Parameters
    a: bpy.props.FloatProperty(name="Semi axis A", default=12, min=.1)
    b: bpy.props.FloatProperty(name="Semi axis B", default=12, min=.1)

    #Inclination
    ascending_node: bpy.props.FloatProperty(name="Longitude of the ascending node", default=0)
    inclination: bpy.props.FloatProperty(name="Inclination", default=0)
    periapsis: bpy.props.FloatProperty(name="Argument of periapsis", default=0)
    true_anomaly: bpy.props.FloatProperty(name="True anomaly", default=0)

    #Other
    alternate_focus: bpy.props.BoolProperty(name="Alternate focus", default=True)
    imprecision: bpy.props.FloatProperty(name="Imprecision", default=10, min=.01, max=100)
    divisions: bpy.props.IntProperty(name="Divisions", default=2000, min=1, max=100000)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Animation Options")
        row = layout.row()
        row.prop(self, "frame_step")
        row.prop(self, "clockwise")

        layout.separator()

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
        row = layout.row()
        row.prop(self, "true_anomaly")

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
        if bpy.context.object is None:
            self.report({"WARNING"}, "You must select an object.")
            return {"CANCELLED"}
        bpy.ops.object.select_all(action='DESELECT')
        pos = bpy.context.object.location
        ellipse = Ellipse("Ellipse", pos[0], pos[1], pos[2], self.a, self.b, self.imprecision/1000, self.alternate_focus, self.divisions, False)
        planet = Planet(bpy.context.object)
        planet.set_pos((0, 0, 0))

        #Unselect planet
        planet.unselect()

        #Select ellipse
        ellipse.select(True)
        
        #Convert ellipse to curve
        bpy.ops.object.convert(target='CURVE')

        #Select planet and set as active
        planet.select(True)

        #Add path constraint to current selected
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')

        #Add Ellipse as target
        bpy.context.object.constraints["Follow Path"].target = ellipse.object

        #Select ellipse and switch to edit mode to fix bug
        ellipse.select(True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        #Generate animation
        planet.animate_through_ellipse(ellipse, self.frame_step, self.clockwise)
        
        #Make animation cyclic
        planet.select(True)

        #Adjust ellipse orientation
        planet.unselect()
        ellipse.adjust_inclination(self.ascending_node, self.inclination, self.periapsis, self.true_anomaly)

        #Reselection
        ellipse.unselect()
        planet.select(True)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(MoveThroughEllipse)

def unregister():
    bpy.utils.unregister_class(MoveThroughEllipse)    