import os
import traceback
import shutil
import bpy
from bpy.utils import register_class, unregister_class
import addon_utils
from pathlib import Path
from . import ui

# Relative path to This addon
KRANIO_filepath = ""
for mod in addon_utils.modules():
	if __package__['name'] == "KRANIO":
		KRANIO_filepath = mod.__file__.replace('__init__.py', '')

sb_addon_name = 'SimpleBake'

def is_blend_saved():
    path = bpy.data.filepath
    if(path=="/" or path==""):
        return False
    else:
        return True
	
def get_kranio_path():
	return KRANIO_filepath
		
def get_kranio_mat_library_filename():
	return "KRANIO-Material-Library.blend"

def get_kranio_mat_library_path():
	return f"{get_kranio_path()}KranioMaterialLibrary/{get_kranio_mat_library_filename()}"
	
class ViewportViewChanger:
	def redraw_3d_viewport():
		s = bpy.context.screen
		viewport_areas = []
		for a in s.areas:
			if a.type == "VIEW_3D":
				viewport_areas.append(a)

		for a in viewport_areas:
			a.tag_redraw()

	@classmethod
	def set_viewport_view(self, view, ortho):
		for area in (a for a in bpy.context.screen.areas if a.type == 'VIEW_3D'):
			for region in (r for r in area.regions if r.type == 'WINDOW'):
				override = {'area': area, 'region': region}
				bpy.ops.view3d.view_axis(type = view)
				if ortho:
					if area.spaces.active.region_3d.is_perspective:
						bpy.ops.view3d.view_persportho()
						area.spaces.active.region_3d.update()
						self.redraw_3d_viewport()
				else:
					if area.spaces.active.region_3d.is_orthographic_side_view:
						bpy.ops.view3d.view_persportho()
						area.spaces.active.region_3d.update()
						self.redraw_3d_viewport()

class FileMover:

	@classmethod
	def movefiles(self, fromDir, toDir, filename):
		print("---")
		print(f"K: Copying file: '{filename}'")

		if not os.path.exists(fromDir):
			return self.error('- Original directory does not exist')
		if not os.path.exists(toDir):
			return self.error('- Target directory does not exist')
		
		print("- Both the target and original directory exists. Continuing file transfer...")

		filesin_From = os.listdir(fromDir)
		if len(filesin_From) == 0:
			return self.error('- no files found in original directory')
		elif os.path.isfile(f"{fromDir}\{filename}"):
			print(f"- Found the chosen file '{filename}' in the original directory. Continuing file transfer...")
					
		if os.path.isfile(f"{toDir}\{filename}"):
			return self.error('- File already exists in target directory')
		
		print("- No file with this name exists in the target directory. Checks done, attempting file transfer...")

		for file in filesin_From:
			if os.path.splitext(file)[1] == '':
				print("- File has no file extension. Good...")
				shutil.copy(os.path.join(fromDir, file), os.path.join(toDir, file))
				print(f"- Moved '{str(file)}' from {fromDir} to {toDir}")

	def error(message):
		'''dummy method to merge print and return into one-liner'''
		print(message)

class SimpleBakeHook:
	def load_kranio_simplebakepreset():
		fromPath = f"{get_kranio_path()}KranioSimpleBakeSettings"
		print("---")
		print(f"K: Looking for our SimpleBake preset in {fromPath}")

		targetPath = Path(bpy.utils.script_path_user())
		targetPath = targetPath.parents[1]
		targetPath = targetPath /  "data" / "SimpleBake"
		
		print(f"K: Attempting to move Kranio SimpleBake Settings from {fromPath} to {targetPath}")
		
		FileMover.movefiles(fromPath, targetPath, "KRANIO")

	def fetch_simplebake_props(context):
		sbp = None
		try:
			sbp = context.scene.SimpleBake_Props
			return sbp
		except Exception as err:
			print(f"SimpleBake Properties couldn't be accessed. SimpleBake is likely not installed properly. Error: {err}")
			ui.simplebake_initialized = False
			ui.simplebake_init_failed = True
			ui.simplebake_please_enable = False
			return None

	@classmethod
	def findsimplebake(self):
		print("K: Looking for SimpleBake...")
		try:
			if sb_addon_name not in addon_utils.addons_fake_modules:
				print(f"K: {sb_addon_name} is not installed.")
				ui.simplebake_initialized = False
				ui.simplebake_init_failed = True
			else:
				default, enabled = addon_utils.check(sb_addon_name)
				if enabled:
					print("K: SimpleBake is installed and enabled")
					ui.simplebake_initialized = True
					ui.simplebake_init_failed = False
					ui.simplebake_please_enable = False
					SimpleBakeHook.load_kranio_simplebakepreset()
				else:
					print("K: SimpleBake is installed but not enabled. Please enable in 'Edit -> Preferences -> Add-ons' to proceed.")
					ui.simplebake_please_enable = True

		except Exception as err:
			print(f"!!! - K: Error attempting to link KRANIO and {sb_addon_name} (details below): {err} - !!!")
			print(traceback.format_exc())
			ui.simplebake_initialized = False
			ui.simplebake_init_failed = True
    
classes = ([
        ])

def register():
    global classes
    for cls in classes:
        register_class(cls)
    

def unregister():
    global classes
    for cls in classes:
        unregister_class(cls)