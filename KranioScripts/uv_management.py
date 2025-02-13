import bpy, _bpy
from bpy.utils import register_class, unregister_class
from bpy.types import (Operator, Object)
from bpy.props import (BoolProperty, StringProperty, EnumProperty)
from  .  import utils

class KRANIO_UV_Support_Methods():
    @classmethod
    def get_uv_map(self, ob, map_name):
        uvmap = ob.data.uv_layers.get(map_name)
        if not uvmap:
            uvmap = ob.data.uv_layers.new(name = map_name)
        return uvmap

    @classmethod
    def remove_non_meshes_and_ensure_active(self):
        # Remove non-mesh objects from the selection
        [ob.select_set(False) for ob in bpy.context.scene.objects if ob.type != "MESH"]

        # Set active object if none is set already
        if bpy.context.active_object == None:
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

    @classmethod
    def pack_islands(self, to_rotate, the_margin):
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(rotate=to_rotate, margin=the_margin)


class KRANIO_OT_Process_UV_Maps(Operator):
    """Various Blender UV Unwrapping methods that we want to use"""
    bl_idname = "kranio.process_uv_maps"
    bl_label = "Prepare UVs"

    override_active_name: StringProperty(default="")
    
    u_method: StringProperty(default="")
    pack_separate: BoolProperty(default=True)
    pack_together: BoolProperty(default=False)
    uvmap_name: StringProperty(default="")

    # TODO - Since bools have to be Default True/False we are not curently packing any uv maps. Ensure that anything you want to pack didn't count on the default value from before
    
    def execute(self, context):
        # Default values can behave weirdly in python if we set them in the def, so instead we set them to None and do it like this
        if (self.u_method == ""):
            self.u_method = "SMART"
        if (self.uvmap_name == ""):
            self.uvmap_name = "UVMap"

        if (self.pack_separate and self.pack_together):
            self.pack_together = False # We can't pack together AND separate, so if both are True for some reason, pack separately

        obs = bpy.context.selected_objects.copy()
        active = None
        try:
            if self.override_active_name != "":
                active = [bpy.context.scene.objects[self.override_active_name]]
            else:
                try: # There might not be an active object... so we TRY!
                    active = bpy.context.view_layer.objects.active
                except Exception as err:
                    print(f"::::: K: Getting active object failed: {err}")
        except Exception as err:
            print(f"::::: K: Overriding active object failed: {err}")

        # TODO - Ensure that these two really do need to be different...
        if self.u_method != "SimpleBake":
            KRANIO_UV_Support_Methods.remove_non_meshes_and_ensure_active()
            # Deselect all objects now that we have a reference for them, so that we don't unwrap and pack them together
            [ob.select_set(False) for ob in obs]

        else:
            # Deselect all objects now that we have a reference for them, so that we don't unwrap and pack them together
            [ob.select_set(False) for ob in obs]
            [ob.select_set(False) for ob in bpy.context.selected_objects]
        

        vl = context.view_layer

        for ob in obs:
            # Get object size, the larger of its x and y dimensions
            ob_size = max(ob.dimensions.x, ob.dimensions.y)

            vl.objects.active = ob
            ob.select_set(True)

            uvmap = KRANIO_UV_Support_Methods.get_uv_map(ob, self.uvmap_name)
            uvmap.active = True
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT') # for all faces

            try :
                if (self.u_method == "CUBE"):
                    print("KRANIO: UV Unwrap - Cube project")
                    bpy.ops.uv.cube_project(cube_size=ob_size, correct_aspect=True, clip_to_bounds=False, stretch_to_bounds=False)
                elif (self.u_method == "SMART"):
                    print("KRANIO: UV Unwrap - Smart UV project")
                    bpy.ops.uv.smart_project(angle_limit=1.15192, island_margin=0.001, user_area_weight=0.0, use_aspect=True, stretch_to_bounds=False)
                elif (self.u_method == "SimpleBake"):
                    print("KRANIO: UV Unwrap - SimpleBake map - Smart UV project")
                    bpy.ops.uv.smart_project(angle_limit=1.15192, island_margin=0.001, user_area_weight=0.0, use_aspect=True, stretch_to_bounds=False)
                elif (self.u_method == "FRONT"):
                    print("KRANIO: UV Unwrap - Project from view, front")
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, stretch_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(to_rotate=False, the_margin=0.001)
                elif (self.u_method == "BACK"):
                    print("KRANIO: UV Unwrap - Project from view, back")
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, stretch_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(to_rotate=False, the_margin=0.001)
                elif (self.u_method == "LEFT"):
                    print("KRANIO: UV Unwrap - Project from view, left")
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, stretch_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(to_rotate=False, the_margin=0.001)
                elif (self.u_method == "RIGHT"):
                    print("KRANIO: UV Unwrap - Project from view, right")
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, stretch_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(to_rotate=False, the_margin=0.001)
                elif (self.u_method == "TOP"):
                    print("KRANIO: UV Unwrap - Project from view, top")
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, stretch_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(to_rotate=False, the_margin=0.001)
                elif (self.u_method == "BOTTOM"):
                    print("KRANIO: UV Unwrap - Project from view, bottom")
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, stretch_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(to_rotate=False, the_margin=0.001)
                else :
                    print(f"UV unwrap couldn't be done. The unwrapping method '{self.u_method}' was not expected.")
            
            except Exception as err:
                print(f"KRANIO ERROR: Attempted UV unwrap --- FAILED WITH: {err}")

            print("UV unwrap successful")

            if self.pack_separate:
                print("Packing UVs separate")
                KRANIO_UV_Support_Methods.pack_islands(to_rotate=True, the_margin=0.001)

            print("Toggling edit mode back to object mode")

            bpy.ops.object.editmode_toggle()

            print("Deselecting object")
            
            ob.select_set(False)

        if self.pack_together:
            print("Packing UVs together with all selected objects")
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT') # for all faces
            KRANIO_UV_Support_Methods.pack_islands(to_rotate=True, the_margin=0.001)
            bpy.ops.object.editmode_toggle()

        print("Deselect objects that might still be selected from past selections...")
        # Deselect objects that might still be selected from past selections...
        [ob.select_set(False) for ob in bpy.context.selected_objects]

        print("Selecting all the objects again and set the one we had active before as active again")
        # Let's select all the objects again and set the one we had active before as active again
        [ob.select_set(True) for ob in obs]
        bpy.context.view_layer.objects.active = active
        obs.clear()

        return {'FINISHED'}

    #def unwrap_cube_project(context):
        # TODO - Run Unwrapping with these settings: u_method = "CUBE", everything else default
            
    #def unwrap_smart_uv_project(context, pack_with_other_objects = None):
        # TODO - Run Unwrapping with these settings: u_method = "SMART", and whether or not to pack separated or together

    #def unwrap_view_project(context, view, map_name):
        # TODO - Run Unwrapping with these settings: u_method = view (AKA "FRONT" or "LEFT" for example), uvmap_name = THE MAP NAME, FOR EXAMPLE TEETH, OR CEREBELLUM
            
    #def unwrap_smart_uv_project_for_simplebake(context, obs, active):        
        # TODO - Run Unwrapping with these settings: "SMART", Pack Separate TRUE, "SimpleBake")


# ------------------------------------------------------------------------
#     UV Unwrap From View // Project From View
# ------------------------------------------------------------------------

# Project From View needs a "Modal" to give the viewport time to switch view, and not lock up, so the projection can happen from the correct view.




# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------

classes = (
    KRANIO_OT_Process_UV_Maps,
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