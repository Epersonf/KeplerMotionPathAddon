import bpy
from .object import Object

class Planet(Object):

    def __init__(self, obj):
        super().__init__(obj)
    
    def animate_through_ellipse(self, ellipse, frame_step):
        current_frame = bpy.context.scene.frame_current
        for i in range(len(ellipse.areaPoints)):
            self.object.keyframe_insert(data_path='constraints["Follow Path"].offset', frame=current_frame + i * frame_step)
            self.object.constraints["Follow Path"].offset = ellipse.areaPoints[i]

