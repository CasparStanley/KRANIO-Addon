bl_info = {
    "name": "KRANIO",
    "author": "Stanley Creative",
    "version": (0, 1, 0, 0),
    "blender": (4, 2, 0),
    "location": "3D View",
    "description": "Quick fixing and set-up of models, for improved visual fidelity!",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View",
}

import bpy
from bpy.utils import register_class, unregister_class

from . import material_operators
from . import viewport_operators
from . import umich_kranio_addon
from . import kranio_x_simplebake
from . import material_assignment
from . import property_group
from . import ui
from . import utils
from . import uv_management

classes = ([
        ])

def register():
    global classes
    for cls in classes:
        register_class(cls)

    material_operators.register()
    viewport_operators.register()
    umich_kranio_addon.register()
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
    umich_kranio_addon.unregister()
    kranio_x_simplebake.unregister()
    property_group.unregister()
    material_assignment.unregister()
    utils.unregister()
    ui.unregister()
    uv_management.unregister()