bl_info = {
    "name": "Kepler Motion Path",
    "author": "Eperson and Francisco Meirelles",
    "description": "Generates an ellipse",
    "blender": (2, 83, 7)
}

from .modules.menus.menus import register as registerMenus, unregister as unregisterMenus

def register():
    registerMenus()

def unregister():
    unregisterMenus()

if __name__ == "__main__":
    register()

