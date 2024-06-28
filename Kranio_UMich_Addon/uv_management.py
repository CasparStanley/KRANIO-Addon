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
        [ob.select_set(False) for ob in bpy.data.objects if ob.type != "MESH"]

        # Set active object if none is set already
        if bpy.context.active_object == None:
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

    @classmethod
    def pack_islands(self, to_rotate, to_scale, the_margin):
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM', rotate=to_rotate, rotate_method='ANY', scale=to_scale, merge_overlap=False, margin_method='SCALED', margin=the_margin, pin=False, pin_method='LOCKED', shape_method='CONCAVE')


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
                active = [bpy.data.objects[self.override_active_name]]
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

            match self.u_method:
                case "CUBE":
                    bpy.ops.uv.cube_project(cube_size=ob_size, correct_aspect=True, clip_to_bounds=False, scale_to_bounds=False)
                case "SMART":
                    bpy.ops.uv.smart_project(angle_limit=1.15192, margin_method='SCALED', rotate_method='AXIS_ALIGNED_Y', island_margin=0.001, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
                case "SimpleBake":
                    bpy.ops.uv.smart_project(angle_limit=1.15192, margin_method='SCALED', rotate_method='AXIS_ALIGNED_Y', island_margin=0.001, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
                case "FRONT":
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, scale_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(False, True, 0.001)
                case "BACK":
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, scale_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(False, True, 0.001)
                case "LEFT":
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, scale_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(False, True, 0.001)
                case "RIGHT":
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, scale_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(False, True, 0.001)
                case "TOP":
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, scale_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(False, True, 0.001)
                case "BOTTOM":
                    bpy.ops.uv.project_from_view(orthographic=True, camera_bounds=True, correct_aspect=False, clip_to_bounds=False, scale_to_bounds=False)
                    KRANIO_UV_Support_Methods.pack_islands(False, True, 0.001)
                case _:
                    print("UV unwrap couldn't be done. The unwrapping method was not expected.")

            if self.pack_separate:
                KRANIO_UV_Support_Methods.pack_islands(True, True, 0.001)

            bpy.ops.object.editmode_toggle()
            ob.select_set(False)

        if self.pack_together:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT') # for all faces
            KRANIO_UV_Support_Methods.pack_islands(True, True, 0.001)
            bpy.ops.object.editmode_toggle()

        # Deselect objects that might still be selected from past selections...
        [ob.select_set(False) for ob in bpy.context.selected_objects]
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