import bpy
import time
from bpy.utils import register_class, unregister_class
from bpy.types import (Operator)
from bpy.props import (StringProperty)
from . import utils

# ------------------------------------------------------------------------
#     Viewport Operators
# ------------------------------------------------------------------------
class KRANIO_OT_Set_View_Dir_Ortho_Operation(Operator):
    bl_idname = "kranio.set_view_dir_ortho_operation"
    bl_label = "Set Viewport to Direction and Orthographic"

    view: StringProperty(default="")

    def execute(self, context):
        if (self.view == ""):
            self.view = "LEFT"

        time.sleep(0.5) # Wait for a bit
        utils.ViewportViewChanger.set_viewport_view(self.view, True) # Switch viewport view to selected view and Orthographic
        time.sleep(0.5) # Wait some more
        return {'FINISHED'}
    
class KRANIO_OT_Set_View_Dir_Perspective_Operation(Operator):
    bl_idname = "kranio.set_view_dir_perspective_operation"
    bl_label = "Set Viewport to Direction and Perspective"

    view: StringProperty(default="")

    def execute(self, context):
        if (self.view == ""):
            self.view = "LEFT"

        time.sleep(0.5) # Wait for a bit
        utils.ViewportViewChanger.set_viewport_view(self.view, False) # Switch viewport view to selected view and Perspective
        time.sleep(0.5) # Wait some more
        return {'FINISHED'}

# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------

classes = (
    KRANIO_OT_Set_View_Dir_Ortho_Operation,
    KRANIO_OT_Set_View_Dir_Perspective_Operation,
)
# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    # Register classes
    for cls in classes:
        register_class(cls)

def unregister():
    # Unregister classes
    for cls in reversed(classes):
        unregister_class(cls)