import bpy
import math

class Object:

    def __init__(self, obj):
        self.object = obj
    
    def select(self, setActive=False):
        if self.object is None:
            return
        self.object.select_set(True)
        if setActive:
            bpy.context.view_layer.objects.active = self.object

    def unselect(self):
        if self.object is None:
            return
        self.object.select_set(False)
    
    def set_pos(self, pos):
        self.object.location = pos
    
    def rotate(self, degree, axis, orientation):
        val = math.radians(degree)
        bpy.ops.transform.rotate(value=val, orient_axis=axis, orient_type=orientation, orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type=orientation, constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)