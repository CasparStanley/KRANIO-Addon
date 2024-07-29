import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import (Operator)
from .utils  import SimpleBakeHook

# ------------------------------------------------------------------------
#     TEXTURE BAKING
# ------------------------------------------------------------------------
def set_object_state(ob, state_name):
    match state_name:
        case "new":
            ob['bake_state'] = 0
        case "prepared":
            ob['bake_state'] = 1
        case "baked":
            ob['bake_state'] = 2
        case _:
            pass

class KRANIO_OT_Object_State_S(Operator):
    """Add the object to the list of objects that we want to bake"""
    bl_idname = "kranio.object_state"
    bl_label = "Add Object(s) to SimpleBake"

    def execute(self, context):
        # Get the currently selected objects,
        obs = context.selected_objects.copy()

        # Create a variable on the selected objects so we can keep track of where each of them are in the baking process
        for ob in obs:
            set_object_state(ob,"new")
        
        return {'FINISHED'}
    
class KRANIO_OT_Load_Preset_S(Operator):
    """Load the KRANIO preset onto SimpleBake. !! REQUIRES THE SIMPLEBAKE ADDON - It can be found on BlenderMarket.com"""
    bl_idname = "kranio.load_preset"
    bl_label = "Load Preset"        

    def execute(self, context):
        try:
            from SimpleBake.ui import objects_list as sb_ui_objects_list
            from SimpleBake import presets

            # Applying the preset will remove any objects currently in the bake list, so we want to keep whatever is currently there, there
            sbp = context.scene.SimpleBake_Props
            sb_bake_obs_list = sbp.objects_list

            # Get the currently selected objects,
            obs = context.selected_objects.copy()
            
            # Apply the KRANIO preset that we have now loaded
            bpy.ops.simplebake.preset_refresh()
            bpy.ops.simplebake.presets_list_index = 0
            # bpy.ops.simplebake.preset_load()
            presets.SimpleBake_OT_preset_load.execute(self, context)

            # Now that we have loaded the preset, add the objects back in, deselect them, and select whatever we had selected before
            [ob.select_set(True) for ob in sb_bake_obs_list]
            sb_ui_objects_list.SimpleBake_OT_Add_Bake_Object.execute(self, context)
            [ob.select_set(False) for ob in sb_bake_obs_list]
            [ob.select_set(True) for ob in obs]

        except Exception as err:
            print(f"K: Loading KRANIO preset on SimpleBake failed with error: {err}")
            return {'CANCELLED'}

        return {'FINISHED'}

class KRANIO_OT_Prepare_S(Operator):
    """Use the SimpleBake addon to bake out individual texture maps for all objects. !! REQUIRES THE SIMPLEBAKE ADDON - It can be found on BlenderMarket.com"""
    bl_idname = "kranio.prepare"
    bl_label = "Prepare SimpleBake"

    def execute(self, context):
        try:
            from SimpleBake.ui import objects_list as sb_ui_objects_list
            
            # Get the currently selected objects,
            obs = context.selected_objects.copy()
            # And get the active object
            active = bpy.context.view_layer.objects.active

            # Remove non-mesh objects from the selection
            [ob.select_set(False) for ob in obs if ob.type != "MESH"]

            # Create a variable on the selected objects so we can keep track of where each of them are in the baking process
            for ob in obs:
                set_object_state(ob,"new")

            # Load/Apply the KRANIO preset on SimpleBake
            bpy.ops.kranio.load_preset()

            # Access these internal methods from SimpleBake that won't work as a bpy.ops since it's the "wrong context"
            # Adds the selected objects to the bake list
            sb_ui_objects_list.SimpleBake_OT_Add_Bake_Object.execute(self, context)

            # The object(s) have now been prepared, so they enter "state 1" - Unwrapped and added to the SimpleBake list
            for ob in obs:
                set_object_state(ob,"prepared")

            obs.clear()
        
        except Exception as err:
            print(f"SimpleBake preparation for KRANIO object failed: {err}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
class KRANIO_OT_Bake_S(Operator):
    """Bake the texture files for this object"""
    bl_idname = "kranio.bake_pbr_simplebake"
    bl_label = "Bake"

    def execute(self, context):
        # Just in case remnants of a previous selection is still here, clear that
        try:
            obs.clear()
        except:
            pass
        
        # Get the currently selected objects,
        obs = context.selected_objects.copy()

        # Bake with the SimpleBake bake operation - Modal error happens here but we ignore it
        bpy.ops.simplebake.bake_operation_pbr()

        # The object(s) have now been baked, so they enter "state 3" - Done!
        for ob in obs:
            set_object_state(ob,"baked")
        
        return {'FINISHED'}
    
class KRANIO_OT_Add_S(Operator):
    """Add to the list of objects that are currently set to bake"""
    bl_idname = "kranio.add_simplebake_objects_list"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        state = False
        if len(bpy.context.selected_objects) > 0:
            state = True

        return state

    def execute(self, context):
        # Bake with the SimpleBake bake operation - Modal error happens here but we ignore it
        bpy.ops.simplebake.add_bake_object()
        return {'FINISHED'}

class KRANIO_OT_Remove_S(Operator):
    """Remove from the list of objects that are currently set to bake"""
    bl_idname = "kranio.remove_simplebake_objects_list"
    bl_label = "Remove"

    @classmethod
    def poll(cls, context):
        sbp = context.scene.SimpleBake_Props
        state = False
        if len(sbp.objects_list) > 0:
            state = True

        return state

    def execute(self, context):
        try:
            # Bake with the SimpleBake bake operation - Modal error happens here but we ignore it
            bpy.ops.simplebake.remove_bake_object()
        except Exception as err:
            print(f"KRANIO ERROR: Attempted 'bpy.ops.simplebake.remove_bake_object()' --- FAILED WITH: {err}")
        return {'FINISHED'}

class KRANIO_OT_Clear_S(Operator):
    """Clear the list of objects that are currently set to bake"""
    bl_idname = "kranio.clear_simplebake_objects_list"
    bl_label = "Clear"

    def execute(self, context):
        try:
            # Bake with the SimpleBake bake operation - Modal error happens here but we ignore it
            bpy.ops.simplebake.clear_bake_objects_list()
        except Exception as err:
            print(f"KRANIO ERROR: Attempted 'bpy.ops.simplebake.clear_bake_objects_list()' --- FAILED WITH: {err}")
        return {'FINISHED'}
    
class KRANIO_OT_Addon_Blendermarket_S(Operator):
    """If you do not have the SimpleBake addon, you cannot use this feature. To export your textures as simply as with a click of a button, please purchase the SimpleBake addon. Click here to be taken to BlenderMarket.com where you can do that"""
    bl_idname = "kranio.getsimplebake"
    bl_label = "Get SimpleBake"
    
    def execute(self, context):
        try:
            import webbrowser
            webbrowser.open('https://blendermarket.com/products/simplebake---simple-pbr-and-other-baking-in-blender-2', new=2)
        except Exception as err:
            print(f"KRANIO ERROR: Attempted 'import webbrowser' and 'webbrowser.open()' --- FAILED WITH: {err}")
        return {'FINISHED'}
    
class KRANIO_OT_SimpleBake_Initialize_S(Operator):
    """If SimpleBake has not been found yet by KRANIO, click here to locate it and get access to its features through this panel"""
    bl_idname = "kranio.initialize_simplebake"
    bl_label = "Initialize SimpleBake"
    
    def execute(self, context):
        # Create the "bake_state" property for all mesh objects
        for ob in bpy.data.objects:
            if (ob is not None):
                if (ob.type == "MESH"):
                    try:
                        # Attempt to read the bake_state of each object. If it throws an error, it's probably because the object doesn't have the property
                        print(ob['bake_state'])
                    except:
                        # Then we create the property and set it to 0
                        set_object_state(ob, "new")
                        pass
        
        try:
            # Locate simplebake
            SimpleBakeHook.findsimplebake()
            return {'FINISHED'}
        except Exception as err:
            print(f"KRANIO ERROR: Attempted 'SimpleBakeHook.findsimplebake()' --- FAILED WITH: {err}")
            return {'CANCELLED'}
        
        
    
# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------
classes = (
    KRANIO_OT_Object_State_S,
    KRANIO_OT_Load_Preset_S,
    KRANIO_OT_Prepare_S,
    KRANIO_OT_Bake_S,
    KRANIO_OT_Add_S,
    KRANIO_OT_Remove_S,
    KRANIO_OT_Clear_S,
    KRANIO_OT_Addon_Blendermarket_S,
    KRANIO_OT_SimpleBake_Initialize_S
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