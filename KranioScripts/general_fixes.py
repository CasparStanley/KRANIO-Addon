import os
import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import (Operator)

# ------------------------------------------------------------------------
#     GENERAL FIXES
# ------------------------------------------------------------------------
def fix_position(context):
    # Set Origin to center of geometry
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    # Set the cursor to the world origin
    bpy.ops.view3d.snap_cursor_to_center()
    # Reset the object position to center of the world
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
    # Focus the viewport on the object
    # bpy.ops.view3d.view_selected(use_all_regions=False)


class KRANIO_OT_position_fixer(Operator):
    """This will set the Object's origin to the center of its mass, and reset its position to the center of the world. Select all objects, then click this button, to move them together"""
    bl_idname = "kranio.fix_position"
    bl_label = "Fix Position"

    def execute(self, context):
        fix_position(context)
        return {'FINISHED'}
    
def decimate_modifier(context):
    # Add the Decimate modifier to the object
    bpy.ops.object.modifier_add(type='DECIMATE')
    ob = bpy.context.active_object
    ob.modifiers["Decimate"].ratio = 0.5


class KRANIO_OT_decimate_object(Operator):
    """This will add the 'Decimate' modifier to the object, and automatically reduce the quality by 50%. To adjust the settings, head to the Modifiers tab marked by the Wrench icon"""
    bl_idname = "kranio.decimate_modifier"
    bl_label = "Decimate / Reduce Polygons"

    def execute(self, context):
        decimate_modifier(context)
        return {'FINISHED'}
    
# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------

def menu_func(self, context):
    self.layout.operator(KRANIO_OT_position_fixer.bl_idname, text=KRANIO_OT_position_fixer.bl_label)
    self.layout.operator(KRANIO_OT_decimate_object.bl_idname, text=KRANIO_OT_decimate_object.bl_label)

classes = (
    KRANIO_OT_position_fixer,
    KRANIO_OT_decimate_object
)
# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    # Register classes
    for cls in classes:
        register_class(cls)
        
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    # Unregister classes
    for cls in reversed(classes):
        unregister_class(cls)
    
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    