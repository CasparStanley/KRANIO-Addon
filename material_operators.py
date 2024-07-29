import bpy, _bpy
from bpy.utils import register_class, unregister_class
from bpy.types import (Operator, Macro)

class KRANIO_OT_Material_Macro(Macro):
    bl_idname = "kranio.material_macro"
    bl_label = "Set Material Now"
    bl_options = {'BLOCKING', 'INTERNAL'}

    @classmethod
    def clean(cls):
        try:
            unregister_class(cls)
        except:
            pass
        register_class(cls)

class KRANIO_OT_Set_Finished(Operator):
    bl_idname = "kranio.material_set_finished"
    bl_label = "Material Set Finished"
    bl_options = {'INTERNAL'}

    @classmethod
    def clean(cls):
        try:
            unregister_class(cls)
        except:
            pass
        register_class(cls)

    def execute(self, context):
        dns = bpy.app.driver_namespace
        dns['material_set_finished'] = True
        return {'FINISHED'}

# ------------------------------------------------------------------------
#     Main Material Operators
# ------------------------------------------------------------------------
class KRANIO_OT_Universal_Material_Operation(Operator):
    bl_idname = "kranio.universal_material_operation"
    bl_label = "Universal Material"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Universal Material")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "_Universal_KRANIO_Material" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Artery_Operation(Operator):
    bl_idname = "kranio.artery_operation"
    bl_label = "Artery"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Artery")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Artery_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Brain_Operation(Operator):
    bl_idname = "kranio.brain_operation"
    bl_label = "Brain"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Brain")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Brain_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Coil_Operation(Operator):
    bl_idname = "kranio.coil_operation"
    bl_label = "Coil"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Coil")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Coil_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Metal_Operation(Operator):
    bl_idname = "kranio.metal_operation"
    bl_label = "Metal"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Metal")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Metal_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Phlebolith_Operation(Operator):
    bl_idname = "kranio.phlebolith_operation"
    bl_label = "Phlebolith"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Phlebolith")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Phlebolith_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Skull_Operation(Operator):
    bl_idname = "kranio.skull_operation"
    bl_label = "Skull"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Skull")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Skull_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps").properties.u_method = "CUBE" # Unwrap with cube project
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Stent_Operation(Operator):
    bl_idname = "kranio.stent_operation"
    bl_label = "Stent"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Stent")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Stent_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Tumor_Operation(Operator):
    bl_idname = "kranio.tumor_operation"
    bl_label = "Tumor"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Tumor")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Tumor_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Vein_Operation(Operator):
    bl_idname = "kranio.vein_operation"
    bl_label = "Vein"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Vein")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Vein_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Venous_Malformation_Operation(Operator):
    bl_idname = "kranio.venous_malformation_operation"
    bl_label = "Venous Malformation"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Venous Malformation")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Venous-Malformation_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap with standard settings
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}

class KRANIO_OT_Teeth_Operation(Operator):
    bl_idname = "kranio.teeth_operation"
    bl_label = "Assign Teeth"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Beginning assigning Teeth")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Skull_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps").properties.u_method = "CUBE" # Unwrap the Skull with cube project
        MACRO.define("KRANIO_OT_set_mat_teeth")
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Cerebellum_Operation(Operator):
    bl_idname = "kranio.cerebellum_operation"
    bl_label = "Assign Cerebellum"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Beginning assigning Cerebellum")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Brain_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap the Brain with standard settings
        MACRO.define("KRANIO_OT_set_mat_cerebellum")
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Brain_Stem_Operation(Operator):
    bl_idname = "kranio.brain_stem_operation"
    bl_label = "Assign Brain Stem"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Beginning assigning Brain Stem")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns

        MACRO.define("KRANIO_OT_assign_mat").properties.mat_name = "Brain_textured" # Define a sub-op that tells the modal to assign this material
        MACRO.define("KRANIO_OT_process_uv_maps") # Unwrap the Brain with standard settings
        MACRO.define("KRANIO_OT_set_mat_brain_stem")
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
    
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}


# ------------------------------------------------------------------------
#     Complete Setup of Special Materials Operators
# ------------------------------------------------------------------------
class KRANIO_OT_Teeth_Complete_Operation(Operator):
    bl_idname = "kranio.teeth_complete_operation"
    bl_label = "Complete Assignment of Teeth"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Teeth")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns
        
        op = MACRO.define("KRANIO_OT_set_view_dir_ortho_operation") # Define a sub-op that changes the viewport view to the correct direction and also Orthohraphic, to ensure correct UV unwrapping
        op.properties.view = "FRONT"
        MACRO.define("KRANIO_OT_confirm_teeth_mask_placement") # Define a sub-op that tells the modal to run the unwrapping with certain settings
        op = MACRO.define("KRANIO_OT_process_uv_maps") # Now that everything mask-wise is done, it's time to create a custom UV map for this part of the material
        op.properties.u_method = "FRONT"
        op.properties.uvmap_name = "Teeth"
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done

        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        op = MACRO.define("KRANIO_OT_set_view_dir_perspective_operation") # Define a sub-op that changes the viewport view to the correct direction and also Orthohraphic, to ensure correct UV unwrapping
        op.properties.view = "FRONT"

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Cerebellum_Complete_Operation(Operator):
    bl_idname = "kranio.cerebellum_complete_operation"
    bl_label = "Complete Assignment of Cerebellum"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Cerebellum")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()

        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns
        
        op = MACRO.define("KRANIO_OT_set_view_dir_ortho_operation") # Define a sub-op that changes the viewport view to the correct direction and also Orthohraphic, to ensure correct UV unwrapping
        op.properties.view = "LEFT"
        MACRO.define("KRANIO_OT_confirm_cerebellum_mask_placement") # Define a sub-op that tells the modal to run the unwrapping with certain settings
        op = MACRO.define("KRANIO_OT_process_uv_maps") # Now that everything mask-wise is done, it's time to create a custom UV map for this part of the material
        op.properties.u_method = "LEFT"
        op.properties.uvmap_name = "Cerebellum"
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done
        
        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        # Define a sub-op that changes the viewport view to the correct direction and also Orthohraphic, to ensure correct UV unwrapping
        op = MACRO.define("KRANIO_OT_set_view_dir_perspective_operation")
        op.properties.view = "FRONT"

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
class KRANIO_OT_Brain_Stem_Complete_Operation(Operator):
    bl_idname = "kranio.brain_stem_complete_operation"
    bl_label = "Complete Assignment of Brain Stem"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished assigning Brain Stem")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()
        
        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns
        
        op = MACRO.define("KRANIO_OT_set_view_dir_ortho_operation") # Define a sub-op that changes the viewport view to the correct direction and also Orthohraphic, to ensure correct UV unwrapping
        op.properties.view = "FRONT"
        MACRO.define("KRANIO_OT_confirm_brain_stem_mask_placement") # Define a sub-op that tells the modal to run the unwrapping with certain settings
        op = MACRO.define("KRANIO_OT_process_uv_maps") # Now that everything mask-wise is done, it's time to create a custom UV map for this part of the material
        op.properties.u_method = "FRONT"
        op.properties.uvmap_name = "BrainStem"
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done

        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Material Operation Failed with error: {err}")

        op = MACRO.define("KRANIO_OT_set_view_dir_perspective_operation") # Define a sub-op that changes the viewport view to the correct direction and also Orthohraphic, to ensure correct UV unwrapping
        op.properties.view = "FRONT"

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}
    
# ------------------------------------------------------------------------
#     Baking Material Operators
# ------------------------------------------------------------------------
class KRANIO_OT_Prep_Operation(Operator):
    bl_idname = "kranio.prep_operation"
    bl_label = "Prepare Object for Baking"
    bl_options = {'UNDO'}

    _timer = None
    def modal(self, context, event):
        if self.dns.get('material_set_finished'):
            context.window_manager.event_timer_remove(self._timer)
            self.report({'INFO'}, "Finished preparing object")
            del bpy.app.driver_namespace['material_set_finished']
            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        MACRO = KRANIO_OT_Material_Macro
        MACRO.clean()
        KRANIO_OT_Set_Finished.clean()
        
        dns = bpy.app.driver_namespace # Store a flag in dns so the modal knows when to end
        dns['material_set_finished'] = False
        self.dns = dns
        
        MACRO.define("KRANIO_OT_prepare") # Define a sub-op that tells the modal to run the unwrapping with certain settings
        op = MACRO.define("KRANIO_OT_process_uv_maps") # Now that everything mask-wise is done, it's time to create a custom UV map for this part of the material
        op.properties.u_method = "SimpleBake"
        op.properties.uvmap_name = "SimpleBake"
        op.properties.pack_separate = True
        MACRO.define("KRANIO_OT_material_set_finished") # Define a last sub-op that tells the modal the unwraps are done

        try:
            bpy.ops.kranio.material_macro('INVOKE_DEFAULT') # 'INVOKE_DEFAULT' keeps the ui responsive. This is propagated onto the sub-ops
        except Exception as err:
            print(f"K: Baking Material Operation Failed with error: {err}")

        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1)
        return {'RUNNING_MODAL'}

# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------
classes = (
    KRANIO_OT_Universal_Material_Operation,
    KRANIO_OT_Artery_Operation,
    KRANIO_OT_Brain_Operation,
    KRANIO_OT_Coil_Operation,
    KRANIO_OT_Metal_Operation,
    KRANIO_OT_Phlebolith_Operation,
    KRANIO_OT_Skull_Operation,
    KRANIO_OT_Stent_Operation,
    KRANIO_OT_Tumor_Operation,
    KRANIO_OT_Vein_Operation,
    KRANIO_OT_Venous_Malformation_Operation,
    KRANIO_OT_Teeth_Operation,
    KRANIO_OT_Cerebellum_Operation,
    KRANIO_OT_Brain_Stem_Operation,
    KRANIO_OT_Teeth_Complete_Operation,
    KRANIO_OT_Cerebellum_Complete_Operation,
    KRANIO_OT_Brain_Stem_Complete_Operation,
    KRANIO_OT_Prep_Operation,
    KRANIO_OT_Material_Macro,
    KRANIO_OT_Set_Finished
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


# THIS CODE IS IN CASE WE WANT TO RUN A SUB OPERATION FOR A RANGE
# HOWEVER, FOR EXAMPLE FOR THE UV MAPS THE UNWRAPPING METHOD CONTROLS THE LOOPING
# num_unwraps = 2
# sub_op = 'KRANIO_OT_Process_UVs'
# define = _bpy.ops.macro_define

# for i in range(num_unwraps):
#     # Sub-operators can be stored on the macro itself
#     setattr(MACRO, f"unwrap_{i}", define(MACRO, sub_op))