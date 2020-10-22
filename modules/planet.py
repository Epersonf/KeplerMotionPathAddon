import bpy
from .object import Object

class Planet(Object):

    def __init__(self, obj):
        super().__init__(obj)
    
    def animate_through_ellipse(self, ellipse, frame_step, clockwise):

        #get current frame
        current_frame = bpy.context.scene.frame_current

        #set frame to current - 1 to avoid bugs on the first frame of the animation
        bpy.context.scene.frame_set(current_frame - 1)

        #for through all area points generating the animation
        for i in range(len(ellipse.areaPoints)):
            self.object.keyframe_insert(data_path='constraints["Follow Path"].offset', frame=current_frame + i * frame_step)
            h = i
            if !clockwise:
                h = len(ellipse.areaPoints) - 1 - i
            self.object.constraints["Follow Path"].offset = ellipse.areaPoints[h]


