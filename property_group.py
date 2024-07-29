import bpy
from bpy.utils import register_class, unregister_class
from bpy.props import (FloatProperty, StringProperty, BoolProperty, 
                       EnumProperty, PointerProperty, IntProperty, CollectionProperty)
from bpy.types import (PropertyGroup, Object)

# Variables that we want to hold onto and NOT be refreshed every time the panel is updated
class KRANIO_prop_group(PropertyGroup):
    des = "Toggles between the main panel and the 'Assigning Teeth' confirmation panel"
    currently_assigning_teeth: BoolProperty(name="Currently Assigning Teeth Toggle", default = False, description = des, subtype = 'NONE')

    des = "Toggles between the main panel and the 'Assigning Cerebellum' confirmation panel"
    currently_assigning_cerebellum: BoolProperty(name="Currently Assigning Cerebellum Toggle", default = False, description = des, subtype = 'NONE')

    des = "Toggles between the main panel and the 'Assigning Brain Stem' confirmation panel"
    currently_assigning_brain_stem: BoolProperty(name="Currently Assigning Brain Stem Toggle", default = False, description = des, subtype = 'NONE')
    
    des = "The name of the skull object, so we can reference it later when assigning the teeth material"
    skull_ob_name: StringProperty(name = "Skull Object for Assigning Teeth", default = "", description = des, subtype = 'NONE')

    des = "The name of the brain object, so we can reference it later when assigning the cerebellum and/or brain stem materials"
    brain_ob_name: StringProperty(name = "Brain Object for Assigning Teeth", default = "", description = des, subtype = 'NONE')

    des = "Define the export folder for the baked textures"
    bake_export_path: StringProperty(name = "Textures Export Path", default = "//", description = des, subtype = 'DIR_PATH')

    des = "Whether or not to show some more options for baking operations with SimpleBake"
    sb_options_show: BoolProperty(name = "Show SimpleBake Options", default = False, description = des, subtype = 'NONE')

    # des = "Whether or not the SimpleBake addon has been succesfully loaded and found by KRANIO"
    # simplebake_init: BoolProperty(name = "SimpleBake has been initialized", default = False, description = des, subtype = 'NONE')

# Access it e.g. like
#bpy.context.scene.KRANIO_Props.currently_assigning_teeth
#bpy.context.scene.KRANIO_Props.skull_ob_name

classes = (
    KRANIO_prop_group,
)

def register():
    # Register classes
    for cls in classes:
        register_class(cls)

    #Register property group
    bpy.types.Scene.KRANIO_Props = PointerProperty(type=KRANIO_prop_group)

def unregister():
    # prefs = bpy.context.preferences.addons["KRANIO"].preferences
    # prefs.property_unset("simplebake_initialized")
    # bpy.context.scene.KRANIO_Props.simplebake_init = False
    # print(f"Goodbye, SimpleBake")

    # Unregister classes
    for cls in reversed(classes):
        unregister_class(cls)