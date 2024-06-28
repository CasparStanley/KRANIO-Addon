import os
import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import (Panel)

simplebake_initialized = False
simplebake_init_failed = False
simplebake_please_enable = False
simplebake_bake_in_progress = False
object_add_bake_state = False

def simplebake_state_increment():
    global simplebake_state
    simplebake_state = simplebake_state + 1

def simplebake_state_reset():
    global simplebake_state
    simplebake_state = 0

placement = "npanel"

#Can be renderpanel or npanel
#FIXME: renderpanel broken - fix position is context dependent... For now we only show it in "View 3D" AKA the "N-Panel"
if placement == "renderpanel":
    space = 'PROPERTIES'
    region = 'WINDOW'
    context = "render"
    cat = ""
else:
    space = 'VIEW_3D'
    region = 'UI'
    context = ""
    cat = 'KRANIO'

class KRANIO_PT_main_panel(Panel):
    bl_label = "KRANIO"
    bl_idname = "KRANIO_PT_main_panel"
    bl_space_type = f"{space}"
    bl_region_type = f"{region}"
    bl_context = f"{context}"
    bl_category = f"{cat}"

    def drawBakeableObjectsState(self, context, box):
        row = box.row()
        row.label(text = "Objects Bake State", icon = 'FORCE_TEXTURE')

        # State of all bake-able objects
        for ob in bpy.data.objects:
            if (ob is not None):
                if (ob.type == "MESH" and ob.data.materials): # If the object is a mesh and has a material on it, consider it something we want to show
                    try:
                        if (ob['bake_state'] is not None):
                            match ob['bake_state']:
                                case 0:
                                    row = box.row()
                                    row.label(text = f"{ob.name}", icon = 'PROP_OFF')
                                case 1:
                                    row = box.row()
                                    row.label(text = f"{ob.name}", icon = 'PROP_ON')
                                case 2:
                                    row = box.row()
                                    row.label(text = f"{ob.name}", icon = 'CHECKMARK')
                        elif (ob['bake_state'] is None):
                            row = box.row()
                            row.label(text = f"{ob.name}", icon = 'CANCEL')

                    except:
                        row = box.row()
                        row.label(text = f"{ob.name}", icon = 'CANCEL')
                        pass

    def drawAddBakeState(self, context, box):
        row = box.row()
        row.scale_y = 1.5
        row.operator("kranio.object_state", icon='PLUS')
    
    def drawObjectInfo(self, context, layout):
        # Info about currently selected object
        try:
            ob = context.active_object
            
            # LIST OBJECT INFORMATION
            row = layout.row()
            row.label(text = "Selected: " + ob.name, icon = 'OBJECT_DATAMODE')
            row = layout.row()
            
            if (ob is not None):
                if (ob.type == 'MESH'):
                    row.label(text = "Polygons: " + str(len(ob.data.polygons)), icon = 'MESH_DATA')
                    
                else:
                    row.label(text = "Polygons: Not a Mesh", icon = 'MESH_DATA')
                
        except:
            # AN OBJECT NEEDS TO BE SELECTED
            row.label(text = "Please select an object", icon = 'OBJECT_DATAMODE')
            row = layout.row()
            row.label(text = "Polygons: -", icon = 'MESH_DATA')

    def drawGeneralFixes(self, context, box):
        row = box.row()
        row.label(text = "General Fixes", icon = 'TOOL_SETTINGS')
        row = box.row()
        row.scale_y = 1.5
        row.operator("kranio.fix_position", icon = 'PIVOT_CURSOR')
        row = box.row()
        row.scale_y = 1.5
        row.operator("kranio.decimate_modifier", icon = 'MODIFIER')

    def drawApplyMatterials(self, context, box):
        pcoll = preview_collections["main"]
        tooth_icon = pcoll["skull_tooth_icon"]
        cerebellum_icon = pcoll["brain_cereb_icon"]
        brain_stem_icon = pcoll["brain_bstem_icon"]

        #col = box.column()
        #col.prop(context.scene, 'mat_library_path')
        
        row = box.row()
        row.label(text = "Apply Materials", icon = 'MATERIAL')
        row = box.row()
        row.operator("kranio.universal_material_operation")
        row = box.row()
        row.operator("kranio.artery_operation")
        row = box.row()
        row.operator("kranio.brain_operation")
        row = box.row()
        row.operator("kranio.coil_operation")
        row = box.row()
        row.operator("kranio.metal_operation")
        row = box.row()
        row.operator("kranio.phlebolith_operation")
        row = box.row()
        row.operator("kranio.skull_operation")
        row = box.row()
        row.operator("kranio.stent_operation")
        row = box.row()
        row.operator("kranio.tumor_operation")
        row = box.row()
        row.operator("kranio.vein_operation")
        row = box.row()
        row.operator("kranio.venous_malformation_operation")
        row = box.row()
        row.scale_y = 1.5
        row = box.row()
        row.operator("kranio.teeth_operation", icon_value=tooth_icon.icon_id)
        row = box.row()
        row.operator("kranio.cerebellum_operation", icon_value=cerebellum_icon.icon_id)
        row = box.row()
        row.operator("kranio.brain_stem_operation", icon_value=brain_stem_icon.icon_id)

    def drawBakeInitialize(self, context, box):
        global simplebake_please_enable

        row = box.row()
        row.label(text = "Bake Textures", icon = 'TEXTURE')
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text = "Please go to")
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text = "Edit -> Preferences -> Add-ons")
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text = "and enable the SimpleBake add-on")
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 1
        row.label(text = "Once enabled, click the button", icon = 'SORT_ASC')

        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 1.5
        row.operator("kranio.initialize_simplebake", icon='FILE_REFRESH')
        if simplebake_please_enable:
            pcoll = preview_collections["main"]
            warning_yellow = pcoll["warning_icon_yellow"]

            row = box.row()
            row.alignment = 'CENTER'
            row.scale_y = 0.6
            row.label(text = "", icon_value=warning_yellow.icon_id)
            row = box.row()
            row.alignment = 'CENTER'
            row.scale_y = 0.6
            row.label(text = "SimpleBake is installed but not enabled")
            row = box.row()
            row.alignment = 'CENTER'
            row.scale_y = 0.6
            row.label(text = "Follow the instructions above to enable")
            row = box.row()

    def drawGetSimpleBake(self, context, box):
        pcoll = preview_collections["main"]
        warning_red = pcoll["warning_icon_red"]

        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text = "", icon_value=warning_red.icon_id)
        row = box.row()
        row.alert = True
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text="WARNING: SimpleBake couldn't be loaded")
        row = box.row()
        row.alert = True
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text="Make sure you have the SimpleBake addon installed")
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text="It can be found on BlenderMarket.com")
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text="If you have installed it but you are given an error")
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text="when attempting to enable the addon")
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(text="please restart Blender and try again")
        row = box.row()
        row.scale_y = 1.5
        row.operator("kranio.getsimplebake", icon='URL')
        row.operator("kranio.initialize_simplebake", icon='FILE_REFRESH')

    def drawBakePrepare_sub(self, context, box, ob):
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(icon = 'PROP_CON')
        row.label(icon = 'PROP_OFF')

        row = box.row()
        row.scale_y = 1.5
        row.operator("kranio.prep_operation", text = f"Prepare: {ob.name}")
    
    def drawBakeBake_sub(self, context, box, kranio_props, sbp):
        row = box.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.6
        row.label(icon = 'PROP_ON')
        row.label(icon = 'PROP_CON')

        # Bake button
        row = box.row()
        row.scale_y = 1.5
        row.operator("kranio.bake_pbr_simplebake", icon='RENDER_RESULT', text="Bake")
        
        options = box.box()
        row = options.row()
        row.prop(kranio_props, "sb_options_show", text="Options", icon="DOWNARROW_HLT" if kranio_props.sb_options_show else "RIGHTARROW", icon_only=False, emboss=False)

        if kranio_props.sb_options_show:
            # Choose export Path
            row = options.row()
            row.scale_y = 1
            col = row.column()
            col.prop(sbp, 'export_path', text="Path")
            col = row.column()
            col.operator("simplebake.export_path_to_blend_location", text="", icon="UV_SYNC_SELECT")

            # Add, Remove, or Clear List
            row = options.row()
            row.operator("kranio.add_simplebake_objects_list", icon='PRESET_NEW', text="Add")
            row.operator("kranio.remove_simplebake_objects_list", icon='CANCEL', text="Remove")
            row.operator("kranio.clear_simplebake_objects_list", icon='MESH_PLANE', text="Clear")

            # Show which objects we are baking
            row = options.row()
            row.alignment = 'LEFT'
            row.scale_y = 0.6
            row.label(text = "Baking: ")
            
            ob_list = ""
            list_length = len(sbp.objects_list) - 1

            for ob in sbp.objects_list:
                ob_list = ob_list + ob.name
                if ob.name != sbp.objects_list[list_length].name: # If not the last in the list, add a comma in between
                    ob_list = ob_list + ", "
            
            row.label(text = f"{ob_list}")

    def drawBakeWithSimpleBake(self, context, box):
        ob = context.active_object

        kranio_props = context.scene.KRANIO_Props
        global simplebake_initialized
        # UI might run before KRANIO and/or SimpleBake modules are fully enabled.
        if simplebake_initialized: # FIXME - If you enable KRANIO and SimpleBake, hit initialize, disable SimpleBake and then load another scene in Blender, clicking KRANIO will crash Blender
            try:
                from .utils import SimpleBakeHook
                sbp = SimpleBakeHook.fetch_simplebake_props(context)
            except:
                pass

        global object_add_bake_state
        try:
            test_state = ob['bake_state']
            object_add_bake_state = False
        except:
            object_add_bake_state = True
            pass

        row = box.row()
        row.label(text = "Bake Textures", icon = 'TEXTURE')
        row = box.row()

        if (ob is not None):
            if (ob.type == 'MESH'):
                if(len(ob.data.materials) > 0):
                    pass

                else:
                    pcoll = preview_collections["main"]
                    warning_yellow = pcoll["warning_icon_yellow"]
                    
                    row = box.row()
                    row.alignment = 'CENTER'
                    row.scale_y = 0.6
                    row.label(text = "", icon_value=warning_yellow.icon_id)
                    row = box.row()
                    row.alignment = 'CENTER'
                    row.scale_y = 0.6
                    row.label(text = "Cannot bake an object")
                    row = box.row()
                    row.alignment = 'CENTER'
                    row.scale_y = 0.6
                    row.label(text = "that has no material")
                    row = box.row()
                    return
            else:
                row = box.row()
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text = "", icon = 'ERROR')
                row = box.row()
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text = "Cannot bake an object")
                row = box.row()
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text = "that is not a mesh")
                row = box.row()
                return

        try:
            from SimpleBake import auto_update
            # SimpleBake was not able to check for updates. Still allows for baking.
            if auto_update.VersionControl.was_error:
                row.alert = True
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text="WARNING: Simplebake")
                row = box.row()
                row.alert = True
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text="wasn't able to check")
                row = box.row()
                row.alert = True
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text="for updates. Are you online?")
                
            # SimpleBake has an update available. Still allows for baking.
            elif not auto_update.VersionControl.at_current:
                row.alert=True
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text = "Newer version of SimpleBake available")
                row = box.row()
                row.alert=True
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text="Update automatically in addon preferences")
                row = box.row()
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                iv = auto_update.VersionControl.installed_version_str
                row.label(text=f"Installed version: {iv}")
                row = box.row()
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text=f"Available Version: {auto_update.VersionControl.current_version_str}")
            
            # SimpleBake is up-to-date. Allows for baking.
            else:
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text = "", icon = 'CHECKMARK')
                row = box.row()
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(text = "SimpleBake is up-to-date")

            if sbp:
                if (sbp.percent_complete == 0 or sbp.percent_complete == 100):
                    if object_add_bake_state is True:
                        self.drawAddBakeState(context, box)
                    else:
                        if (ob['bake_state'] is not None):
                            match ob['bake_state']:
                                # Prepare SimpleBake
                                case 0:
                                    self.drawBakePrepare_sub(context, box, ob)
                                # Bake!
                                case 1:
                                    self.drawBakeBake_sub(context, box, kranio_props, sbp)
                                # Object has been baked, but you can still bake again
                                case 2:
                                    self.drawBakeBake_sub(context, box, kranio_props, sbp)
                                case _:
                                    print ("what")
                
            else:
                row = box.row()
                row.alignment = 'CENTER'
                row.scale_y = 0.6
                row.label(icon = 'PROP_ON')
                row.label(icon = 'PROP_ON')
                row.label(icon = 'PROP_ON')
                row = box.row()
                row.scale_y = 1.5
                row.label(text = "Baking in progress...")
            
        # SimpleBake could not be loaded or found. Needs to be installed and enabled
        except Exception as err:
            print(f"K: SimpleBake Error: {err}")
            self.drawGetSimpleBake(context, box)

    def drawAssignTeethPanel(self, context, box):
        column = box.column()
        column.label(text = "ASSIGNING TEETH", icon = 'BONE_DATA')
        
        column = box.column()
        column.label(text = "Place the 'Teeth Area Mask' object")
        column.label(text = "in the mouth so it covers only the teeth")
        
        box.separator(factor=1.0)
        
        column = box.column()
        column.label(text = "You can scale and rotate to achieve this")
        column.label(text = "and edit the mesh if necessary")
        
        box.separator(factor=1.5)
        
        row = box.row()
        #row.operator("kranio.confirm_teeth_mask_placement", icon = 'CHECKMARK')
        row.operator("kranio.teeth_complete_operation", icon = 'CHECKMARK')
        row.operator("kranio.cancel_teeth_mask_placement", icon = 'CANCEL')

    def drawAssignCerebellumPanel(self, context, box):
        column = box.column()
        column.label(text = "ASSIGNING CEREBELLUM", icon = 'BONE_DATA')
        
        column = box.column()
        column.label(text = "Place the 'Cerebellum Area Mask' object")
        column.label(text = "behind the brain, so it cups the cerebellum")
        
        box.separator(factor=1.0)
        
        column = box.column()
        column.label(text = "You can scale and rotate to achieve this")
        column.label(text = "and edit the mesh if necessary")
        
        box.separator(factor=1.5)
        
        row = box.row()
        row.operator("kranio.cerebellum_complete_operation", icon = 'CHECKMARK')
        row.operator("kranio.cancel_cerebellum_mask_placement", icon = 'CANCEL')

    def drawAssignBrainStemPanel(self, context, box):
        column = box.column()
        column.label(text = "ASSIGNING BRAIN STEM", icon = 'BONE_DATA')
        
        column = box.column()
        column.label(text = "Place the 'Brain Stem Area Mask' object")
        column.label(text = "in front of the brain stem")
        
        box.separator(factor=1.0)
        
        column = box.column()
        column.label(text = "You can scale and rotate to achieve this")
        column.label(text = "and edit the mesh if necessary")
        
        box.separator(factor=1.5)
        
        row = box.row()
        row.operator("kranio.brain_stem_complete_operation", icon = 'CHECKMARK')
        row.operator("kranio.cancel_brain_stem_mask_placement", icon = 'CANCEL')
        
    # ------------------------------------------------------------------------
    #     MAIN UI DRAW FUNCTION
    # ------------------------------------------------------------------------
    def draw(self, context):
        layout = self.layout
        kranio_props = bpy.context.scene.KRANIO_Props

        global simplebake_initialized
        global simplebake_init_failed

        if kranio_props.currently_assigning_teeth: # IF WE ARE CURRENTLY WORKING ON ASSIGNING THE TEETH TO THE SKULL
            box = layout.box()
            self.drawAssignTeethPanel(context, box)
        
        elif kranio_props.currently_assigning_cerebellum: # IF WE ARE CURRENTLY WORKING ON ASSIGNING THE CEREBELLUM TO THE BRAIN
            box = layout.box()
            self.drawAssignCerebellumPanel(context, box)

        elif kranio_props.currently_assigning_brain_stem: # IF WE ARE CURRENTLY WORKING ON ASSIGNING THE BRAIN STEM TO THE BRAIN
            box = layout.box()
            self.drawAssignBrainStemPanel(context, box)
        
        else: # WE ARE NOT CURRENTLY ASSIGNING A MASK TO AN OBJECT
            # LIST OBJECT INFORMATION
            self.drawObjectInfo(context, layout)
            
            # GENERAL FIXES AND OBJECT INTERACTIONS
            box = layout.box()
            self.drawGeneralFixes(context, box)

            # Some spacing...
            layout.row()
            
            # APPLY MATERIALS
            box = layout.box()
            self.drawApplyMatterials(context, box)

            # Some spacing...
            layout.row()

            if simplebake_init_failed:
                # BUTTON TO GET SIMPLEBAKE ON BLENDERMARKET
                box = layout.box()
                self.drawGetSimpleBake(context, box)
            
            elif not simplebake_initialized:
                # BUTTON TO FIND AND INITIALIZE SIMPLEBAKE
                box = layout.box()
                self.drawBakeInitialize(context, box)

            else:
                # PREPARE OUR SIMPLEBAKE
                box = layout.box()
                self.drawBakeableObjectsState(context, box)
                box = layout.box()
                self.drawBakeWithSimpleBake(context, box)

# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------
preview_collections = {}

classes = ([
        KRANIO_PT_main_panel,
        ])

def register():
    global classes
    for cls in classes:
        register_class(cls)

    # Custom icons
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()

    # Path to the folder where the icon is
    # The path is calculated relative to this py file inside the addon folder
    kranio_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    # Load a preview thumbnail of a file and store in the previews collection
    pcoll.load("warning_icon_white", os.path.join(kranio_icons_dir, "KRANIO_icon_warning-white.png"), 'IMAGE')
    pcoll.load("warning_icon_yellow", os.path.join(kranio_icons_dir, "KRANIO_icon_warning-yellow.png"), 'IMAGE')
    pcoll.load("warning_icon_red", os.path.join(kranio_icons_dir, "KRANIO_icon_warning-red.png"), 'IMAGE')

    pcoll.load("skull_tooth_icon", os.path.join(kranio_icons_dir, "KRANIO_icon_tooth.png"), 'IMAGE')
    pcoll.load("brain_cereb_icon", os.path.join(kranio_icons_dir, "KRANIO_icon_brain_cerebellum.png"), 'IMAGE')
    pcoll.load("brain_bstem_icon", os.path.join(kranio_icons_dir, "KRANIO_icon_brain_brain-stem.png"), 'IMAGE')

    preview_collections["main"] = pcoll

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
