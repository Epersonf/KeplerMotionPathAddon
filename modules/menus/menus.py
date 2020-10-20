import bpy

from .actions.create_ellipse import register as registerCreateEllipse, unregister as unregisterCreateEllipse
from .actions.move_through_ellipse import register as registerMoveThroughEllipse, unregister as unregisterMoveThroughEllipse

def register():
    registerCreateEllipse()
    registerMoveThroughEllipse()

def unregister():
    unregisterCreateEllipse()
    unregisterMoveThroughEllipse()
