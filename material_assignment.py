import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import (Operator)
from bpy.props import (StringProperty)
from  .  import utils

kranioPath = utils.get_kranio_path()
matLib = utils.get_kranio_mat_library_filename()
matLibPath = utils.get_kranio_mat_library_path()

# ------------------------------------------------------------------------
#     GENERAL METHODS
# ------------------------------------------------------------------------
class KRANIO_OT_Assign_Material(Operator):
    """Apply the Artery material to this object. This will automatically create a new UV Map to make sure the material looks as intended"""
    bl_idname = "kranio.assign_mat"
    bl_label = "Artery"

    mat_name: StringProperty(default="")

    def load_material(self):
        print(f"K: Material Library Path is located at: {matLibPath}")
        # Load Material Library .blend file to access materials
        with bpy.data.libraries.load(matLibPath) as (data_from, data_to):
            data_to.materials = [name for name in data_from.materials if name == self.mat_name]
            
        # Create a variable called material_library that we can reference in the rest of the script
        material_library = data_to.materials

        # Sanity check
        for mat in material_library:
            if mat is not None:
                print("K: KRANIO materials loaded successfully:")
                print(mat.name)
            else:
                print("K: ERROR: Materials could not be loaded!")

    def execute(self, context):
        if bpy.data.materials.get(self.mat_name) is None:
            self.load_material() # Get material from Materials Library
        
        material = bpy.data.materials.get(self.mat_name)

        # Remove non-mesh objects from the selection
        [obj.select_set(False) for obj in bpy.data.objects if obj.type != "MESH"]

        # Set active object if none is set already
        if bpy.context.active_object == None:
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        
        # Create a reference for all our currently selected objects
        obs = bpy.context.selected_objects.copy()

        for ob in obs:
            # Assign it to object
            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = material
            else:
                # no slots
                ob.data.materials.append(material)

        # Let's select all the objects again
        [obj.select_set(True) for obj in obs]
        return {'FINISHED'}

# ------------------------------------------------------------------------
#     COMPLEX MATERIALS
# ------------------------------------------------------------------------
# Shared Methods
def load_mask(context, mask_name):
    """Load the mask object that we use to show where this area is located on the object and apply the material there"""
    print(f"K: Material Library Path is located at: {matLibPath}")
    # Load Material Library .blend file to access the mask
    with bpy.data.libraries.load(matLibPath) as (data_from, data_to):
        data_to.collections = [name for name in data_from.collections if name == mask_name]
        
    # Create a variable called mask_collection that we can xreference in the rest of the script
    mask_collection = data_to.collections[0]

    vl = context.view_layer

    # Sanity check
    if mask_collection.all_objects[0] is not None:
        mask_ob = mask_collection.all_objects[0]
        context.scene.collection.children.link(mask_collection)
        
        vl.objects.active = mask_ob
        mask_ob.select_set(True)
        print("K: KRANIO material mask loaded successfully:")
        print(mask_ob.name)
        return mask_ob
    else:
        print("K: ERROR: Material Area Mask could not be loaded!")

def masking_cleanup(mask_name, ob_name):
    """Removes the mask object and deletes any remnants of its existence so if it's imported again there won't be any duplicate data"""
    kranio_props = bpy.context.scene.KRANIO_Props

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    # Get the area mask object
    mask_ob = bpy.context.scene.objects[mask_name]
    
    try:
        mask_ob.select_set(True)
        bpy.ops.object.delete()
        
        # Delete the mesh data
        mesh = bpy.data.meshes[mask_name]
        # This check is essential to preventing crashes. (never remove a mesh without a user count check for zero) 
        if mesh.users == 0:
            r = removeMeshFromMemory(mask_name)
            
        # Delete the collection
        collection = bpy.data.collections.get(mask_name)
        bpy.data.collections.remove(collection)
    
    except:
        pass
    
    # Go back to main panel
    match mask_name:
        case "Teeth Area Mask":
            kranio_props.currently_assigning_teeth = False
        case "Cerebellum Area Mask":
            kranio_props.currently_assigning_cerebellum = False
            pass
        case "Brain Stem Area Mask":
            kranio_props.currently_assigning_brain_stem = False
            pass
        case _:
            pass
    
    # Select the main object again
    ob = bpy.context.scene.objects[ob_name]
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    # Set as the active object
    bpy.context.view_layer.objects.active = ob
    # Select the object
    ob.select_set(True)

def confirm_mask_placement(context, mask_type, ob_name):
    """Once the mask object is placed, this runs through the list of operations that converts the placement of the object to a usable vertex color mask"""
    mask_name = f"{mask_type} Area Mask"
    
    mask_name_without_spaces = mask_type.replace(" ", "")
    vg_name = f"{mask_name_without_spaces}Mask"
    cm_name = f"{mask_name_without_spaces}ColorMask"

    # Get the main object and the area mask object
    main_ob = bpy.context.scene.objects[ob_name]
    mask_ob = bpy.context.scene.objects[mask_name]
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    # Make the main object the active object
    bpy.context.view_layer.objects.active = main_ob
    # Select the main object
    main_ob.select_set(True)
    
    # Create a new vertex group to assign to, or select the existing one, and assign all vertices to '1'
    try:
        mask_vertex_group = main_ob.vertex_groups[vg_name]
    except:
        mask_vertex_group = main_ob.vertex_groups.new(name = vg_name)
        
    mask_vertex_group.add(list(range(len(main_ob.data.vertices))), 1.0, 'REPLACE')

    #TODO - sanity debugging
    print(f"::::::::: K: Vertex Groups on object:")
    for vg in main_ob.vertex_groups:
        print(f":: {vg.name}")

    print(f"::::::::: K: Active vertex group before selecting '{vg_name}': '{main_ob.vertex_groups.active.name}'")
    # Important! Select the Vertex Group that we want to use, just in case another one was selected or created.
    main_ob.vertex_groups.active = mask_vertex_group
    #sanity
    print(f"::::::::: K: Active vertex group now: '{main_ob.vertex_groups.active.name}'")

    # Add the Vertex Weight Proximity modifier to the main object
    vertex_weight_prox_mod = main_ob.modifiers.new(type='VERTEX_WEIGHT_PROXIMITY', name="VertexWeightProximity")
    # Set the vertex group for the modifier to the Vertex Group mask
    vertex_weight_prox_mod.vertex_group = vg_name
    # Set the target for the modifier to the Area Mask object
    vertex_weight_prox_mod.target = mask_ob
    # Set the other modifier settings
    vertex_weight_prox_mod.proximity_mode = 'GEOMETRY'
    vertex_weight_prox_mod.min_dist = 5
    vertex_weight_prox_mod.max_dist = 10
    vertex_weight_prox_mod.falloff_type = 'SMOOTH'
    
    # Apply the VertexWeightProximity modifier and convert the Vertex Group mask to Vertex Colors
    bpy.ops.object.modifier_apply(modifier="VertexWeightProximity")
    
    try:
        color_mask = main_ob.data.color_attributes[cm_name]
    except:
        color_mask = main_ob.data.color_attributes.new(name=cm_name, type='BYTE_COLOR', domain='POINT')

    # Important! Like with the Vertex Group, select the Color Mask that we want to use, just in case another one was selected or created.
    main_ob.data.color_attributes.active_color = color_mask
    
    bpy.ops.paint.vertex_paint_toggle() # Perhaps 'bpy.ops.object.mode_set(mode='VERTEX_PAINT')' could be a safer way to ensure we enter vertex paint mode, and back to object mode
    bpy.ops.paint.vertex_color_from_weight()
    bpy.ops.paint.vertex_color_invert()
    bpy.ops.paint.vertex_paint_toggle()
    
    bpy.ops.paint.vertex_paint_toggle()
    bpy.ops.paint.vertex_paint_toggle()

    # Run the cleanup method after we are done with the masking
    masking_cleanup(mask_name, ob_name)

# TEETH MATERIAL
class KRANIO_OT_Confirm_Teeth_Placement(Operator):
    """Confirm the placement of the Teeth Area Mask. This will apply the Teeth material to this area, gradually transitioning to the Skull material"""
    bl_idname = "kranio.confirm_teeth_mask_placement"
    bl_label = "Confirm"

    def execute(self, context):
        kranio_props = bpy.context.scene.KRANIO_Props
        confirm_mask_placement(context, "Teeth", kranio_props.skull_ob_name)
        return {'FINISHED'}

class KRANIO_OT_Cancel_Teeth_Placement(Operator):
    """Cancel the placement of the Teeth Area Mask. This will delete the Teeth Area Mask object and return to the standard menu"""
    bl_idname = "kranio.cancel_teeth_mask_placement"
    bl_label = "Cancel"

    def execute(self, context):
        kranio_props = bpy.context.scene.KRANIO_Props
        masking_cleanup("Teeth Area Mask", kranio_props.skull_ob_name) # Simply run the cleanup method without doing any of the masking
        return {'FINISHED'}

class KRANIO_OT_Material_Set_Teeth(Operator):
    """Assign teeth to the Skull object. This will create an object, generally shaped like the combined area of the teeth. Place this object so it just overlaps all of the teeth, and as little of the skull as possible. You can scale and rotate the object to get it right, and modify the mesh itself if necessary. Once this step is completed, press the 'Confirm' button"""
    bl_idname = "kranio.set_mat_teeth"
    bl_label = "Assign Teeth"

    def execute(self, context):
        kranio_props = bpy.context.scene.KRANIO_Props
        kranio_props.currently_assigning_teeth = True # Switch to the "Assigning Teeth" panel
        
        ob = bpy.context.active_object #Get selected object
        kranio_props.skull_ob_name = ob.name # Save the name of selected object, the skull, so we can reference this later when applying modifiers to it
        
        print(f"K: Saved '{ob.name}' as skull object name")
        ob.select_set(False)

        load_mask(context, "Teeth Area Mask")
        return {'FINISHED'}

class KRANIO_OT_Confirm_Cerebellum_Placement(Operator):
    """Confirm the placement of the Cerebellum Area Mask. This will apply the Cerebellum material to this area, gradually transitioning to the Brain material"""
    bl_idname = "kranio.confirm_cerebellum_mask_placement"
    bl_label = "Confirm"

    def execute(self, context):
        kranio_props = bpy.context.scene.KRANIO_Props
        confirm_mask_placement(context, "Cerebellum", kranio_props.brain_ob_name)
        return {'FINISHED'}

class KRANIO_OT_Cancel_Cerebellum_Placement(Operator):
    """Cancel the placement of the Cerebellum Area Mask. This will delete the Cerebellum Area Mask object and return to the standard menu"""
    bl_idname = "kranio.cancel_cerebellum_mask_placement"
    bl_label = "Cancel"

    def execute(self, context):
        kranio_props = bpy.context.scene.KRANIO_Props
        masking_cleanup("Cerebellum Area Mask", kranio_props.brain_ob_name) # Simply run the cleanup method without doing any of the masking
        return {'FINISHED'}
            
class KRANIO_OT_Material_Set_Cerebellum(Operator):
    """Assign Cerebellum to the Brain object. This will create an object, generally shaped like the cerebellum. Place this object so it cups the cerebellum, and touches as little of the rest of the brain as possible. You can scale and rotate the object to get it right, and modify the mesh itself if necessary. Once this step is completed, press the 'Confirm' button"""
    bl_idname = "kranio.set_mat_cerebellum"
    bl_label = "Assign Cerebellum"

    def execute(self, context):
        kranio_props = bpy.context.scene.KRANIO_Props
        kranio_props.currently_assigning_cerebellum = True # Switch to the "Assigning Cerebellum" panel
        
        ob = bpy.context.active_object #Get selected object
        kranio_props.brain_ob_name = ob.name # Save the name of selected object, the brain, so we can reference this later when applying modifiers to it
        
        print(f"K: Saved '{ob.name}' as brain object name")
        ob.select_set(False)

        load_mask(context, "Cerebellum Area Mask")
        return {'FINISHED'}

class KRANIO_OT_Confirm_Brain_Stem_Placement(Operator):
    """Confirm the placement of the Brain Stem Area Mask. This will apply the Brain Stem material to this area, gradually transitioning to the Brain material"""
    bl_idname = "kranio.confirm_brain_stem_mask_placement"
    bl_label = "Confirm"

    def execute(self, context):
        kranio_props = bpy.context.scene.KRANIO_Props
        confirm_mask_placement(context, "Brain Stem", kranio_props.brain_ob_name)
        return {'FINISHED'}

class KRANIO_OT_Cancel_Brain_Stem_Placement(Operator):
    """Cancel the placement of the Brain Stem Area Mask. This will delete the Brain Stem Area Mask object and return to the standard menu"""
    bl_idname = "kranio.cancel_brain_stem_mask_placement"
    bl_label = "Cancel"

    def execute(self, context):
        kranio_props = bpy.context.scene.KRANIO_Props
        masking_cleanup("Brain Stem Area Mask", kranio_props.brain_ob_name) # Simply run the cleanup method without doing any of the masking
        return {'FINISHED'}
            
class KRANIO_OT_Material_Set_Brain_Stem(Operator):
    """Assign Brain Stem to the Brain object. This will create an object, generally shaped like the brain stem. Place this object so it sits just in front of the brain stem, and touches as little of the rest of the brain as possible. You can scale and rotate the object to get it right, and modify the mesh itself if necessary. Once this step is completed, press the 'Confirm' button"""
    bl_idname = "kranio.set_mat_brain_stem"
    bl_label = "Assign Brain Stem"

    def execute(self, context):
        kranio_props = bpy.context.scene.KRANIO_Props
        kranio_props.currently_assigning_brain_stem = True # Switch to the "Assigning Brain Stem" panel
        
        ob = bpy.context.active_object #Get selected object
        kranio_props.brain_ob_name = ob.name # Save the name of selected object, the brain, so we can reference this later when applying modifiers to it
        
        print(f"K: Saved '{ob.name}' as brain object name")
        ob.select_set(False)

        load_mask(context, "Brain Stem Area Mask")
        return {'FINISHED'}

# ------------------------------------------------------------------------
#     OTHER FUNCTIONS
# ------------------------------------------------------------------------
def removeMeshFromMemory (passedMeshName):
    # Extra test because this can crash Blender.
    mesh = bpy.data.meshes[passedMeshName]
    try:
        mesh.user_clear()
        can_continue = True
    except:
        can_continue = False
    
    if can_continue == True:
        try:
            bpy.data.meshes.remove(mesh)
            result = True
        except:
            result = False
    else:
        result = False
        
    return result
    
# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------

def menu_func(self, context):
    self.layout.operator(KRANIO_OT_Material_Set_Teeth.bl_idname, text=KRANIO_OT_Material_Set_Teeth.bl_label)
    self.layout.operator(KRANIO_OT_Material_Set_Cerebellum.bl_idname, text=KRANIO_OT_Material_Set_Cerebellum.bl_label)
    self.layout.operator(KRANIO_OT_Material_Set_Brain_Stem.bl_idname, text=KRANIO_OT_Material_Set_Brain_Stem.bl_label)

classes = (
    KRANIO_OT_Assign_Material,
    KRANIO_OT_Material_Set_Teeth,
    KRANIO_OT_Confirm_Teeth_Placement,
    KRANIO_OT_Cancel_Teeth_Placement,
    KRANIO_OT_Material_Set_Cerebellum,
    KRANIO_OT_Confirm_Cerebellum_Placement,
    KRANIO_OT_Cancel_Cerebellum_Placement,
    KRANIO_OT_Material_Set_Brain_Stem,
    KRANIO_OT_Confirm_Brain_Stem_Placement,
    KRANIO_OT_Cancel_Brain_Stem_Placement
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