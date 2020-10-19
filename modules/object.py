import bpy

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