bl_info = {
    "name": "KRANIO",
    "author": "Stanley Creative",
    "version": (0, 1, 0, 0),
    "blender": (4, 1, 0),
    "location": "3D View",
    "description": "Quick fixing and set-up of models, for improved visual fidelity",
    "category": "3D View",
}

import bpy
from bpy.utils import register_class, unregister_class

from .KranioScripts import material_operators
from .KranioScripts import viewport_operators
from .KranioScripts import general_fixes
from .KranioScripts import kranio_x_simplebake
from .KranioScripts import material_assignment
from .KranioScripts import property_group
from .KranioScripts import ui
from .KranioScripts import utils
from .KranioScripts import uv_management

classes = ([
        ])

def register():
    global classes
    for cls in classes:
        register_class(cls)

    material_operators.register()
    viewport_operators.register()
    general_fixes.register()
    kranio_x_simplebake.register()
    property_group.register()
    material_assignment.register()
    utils.register()
    ui.register()
    uv_management.register()
    

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    material_operators.unregister()
    viewport_operators.unregister()
    general_fixes.unregister()
    kranio_x_simplebake.unregister()
    property_group.unregister()
    material_assignment.unregister()
    utils.unregister()
    ui.unregister()
    uv_management.unregister()