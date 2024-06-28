<h1>A Guide to the KRANIO Blender Addon</h1>

<h2>Installation</h2>

![Kranio_Addon Installation](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/9223d135-12e6-4c46-a8da-2c46d704bdd9)

<ol>
  <li>Download the .zip file to any location. (DO NOT extract the zip file)</li>
  <li>In Blender, navigate to Edit -> Preferences. Then the Addons tab.</li>
  <li>Hit the install button, locate the zip, and install the zip file.</li>
  <li>Make sure the addon is displayed in the list and enabled (search for "KRANIO" if needed)</li>
  <li>In the 3D viewport, press ‘N’ to open the side panel in the viewport</li>
  <li>Click on the KRANIO Addon tab.</li>
</ol>

<h3>Uninstall</h3>

If you have an installation issue, you may need to cleanly remove the addon before trying again. See the following steps:

<ol>
  <li>In Blender, go to Edit > Preferences, and search for “KRANIO”</li>
  <li>Expand the KRANIO Addon item, and press the "Remove" button</li>
  <ul>
    <li>Alternatively, you can simply uncheck the box next to the addon name. This will only disable the addon, not uninstall it, making it easier to start using again later.</li>
    <li>If you are troubleshooting, however, you should try and fully remove the addon, and ensure all versions of Blender are restarted before attempting to install it again.</li>
  </ul>
</ol>

<br>
<hr>
<br>

<h2>Dependencies - SimpleBake</h2>

Part of the functionality of KRANIO is to “bake” and export textures and 3D models by tapping into another addon called “SimpleBake”.
Purchase Simplebake here: https://blendermarket.com/products/simplebake---simple-pbr-and-other-baking-in-blender-2 
(Make sure you purchase the correct license/number of seats)

Install it alongside KRANIO, following the same steps as in the Installation section.

![Kranio_SimpleBake Intergration](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/c0a316b4-683f-4296-a994-efb281218b54)

<br>
<hr>
<br>

<h2>How to use the addon</h2>

The KRANIO addon panel is separated into sections. At the top, you can see some general information about the currently selected object.

![Kranio_Addon Panel_sections](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/61fe29b0-e58a-473a-8211-fb7b92848729)

<h3>General Fixes</h3>

![Kranio_Addon Panel_section01_generalFixes](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/719b8479-0ef0-4f36-895e-4c7b77d2fc04)

<ul>
  <li><b>Fix Position</b></li>
  The Fix Position button will move all currently selected objects to the center of the scene, and move their respective “origin points” to their center.
  <br><br><b>Tip:</b> Select all the objects and then click this button, to keep their current relative position to each other.
</ul>

<ul>
  <li><b>Decimate/Reduce Polygons</b></li>
  This button applies the “Decimate” modifier to the selected object and reduces the polygon count by 50%.
  <br><br><b>Tip:</b> Click on the wrench icon in the Properties panel to see the modifier. Here you can tweak the settings as needed.
</ul>

![Kranio_Modifiers Tab](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/e0f2ba0e-9015-4857-9283-76f734eb8e52)

<h3>Apply Materials</h3>

![Kranio_Addon Panel_section02_applyMaterials](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/54d70f26-cce0-4227-b5f2-7b5db8f32e97)

<ul>
  <li><b>Material Buttons</b></li>
  Each button corresponds to a Material that will be applied to all objects you currently have selected. Materials contain all the textures and other information for the shading.
  <br><br><b>Tip:</b> The Universal Material can be used to create many detailed looks for an object, with various patterns and shading settings.
</ul>

![Kranio_Addon Panel_section03_applyMaterials](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/6c7f5e32-1768-4540-adf4-9294dd704e18)

<ul>
  <li><b>Assign Teeth, Cerebellum, and Brain Stem</b></li>
  These buttons allow you to designate areas of the object that will have a different material. When clicked, a base material is applied, and a new panel will appear along with a new object in the scene.
  <br><br>Follow the instructions on the panel. When you click “Complete” a series of operations will happen, ending with your viewport snapping to a different view. This is expected, because the UV map needs to be "unwrapped" from this view.
  <br><br>

  ![Kranio_Addon Panel_section05_assignTeeth](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/0c56a581-a129-4539-a5eb-51fbbab1f19e)

</ul>

<h3>Objects Bake State & Bake Textures</h3>

<em>This section requires the SimpleBake addon</em>

These two panels help you keep track of your objects in the baking process, and quickly bake and export your textures and 3D files.

![Kranio_Addon Panel_section04_baking2](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/44594b88-b00d-45f1-9637-e5abc17c7847)

<ul>
  <li><b>Objects Bake State</b></li>
  This is a panel to keep track of all your objects and where they are in the baking process. There are four different states:
  <ul>
    <li><b>“Not added to SimpleBake”</b> symbolized by the ‘X’ icon</li>
    <li><b>“Added”</b> symbolized by the dot with a ring</li>
    <li><b>“Ready”</b> symbolized by the dot with two rings</li>
    <li><b>“Baked”</b> symbolized by the checkmark icon</li>
  </ul>
  <br>
  
  ![Kranio_Addon Panel_section04_baking-state](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/cb6d7a8a-3789-4b72-8ca7-cfc35cef094e)

</ul>
<br>
<ul>
  <li><b>Bake Textures</b></li>
  This is where you bake and export your object and its textures. Once a material is applied to an object, you will get access to this panel and its buttons. Simply click each button in succession to prepare the object, bake, and export:
  <br>
  
  ![Kranio_SimpleBake Process](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/77e49323-b06e-440f-9486-16abb186a39b)

</ul>
<br>
<ul>
  <li><b>Options</b></li>
  On the final panel, with the “Bake” button, there is a dropdown panel called “Options”:
  <ul>
    <li><b>Path:</b> Choose a folder you want the textures and 3D files exported to.</li>
    <li><b>“Add” & “Remove” buttons:</b> Below these is a list of objects that are currently set to bake. You can add or remove an object from this list by selecting it in the 3D scene and clicking the button <em>(you may need to click the remove button twice)</em>.</li>
    <li><b>“Clear” button:</b> This will clear the list of all objects, so no objects will be baked.</li>
  </ul>
</ul>

<br>
<hr>
<br>

<h2>Warnings and Errors</h2>

<b>In the connection with SimpleBake the potential for warnings and errors is highest, since it is a separately developed addon that KRANIO is interfacing with.</b>
<br>Here are some of the warning messages you could encounter, and how to fix the issue.

<br>

> [!WARNING]
> <b>SimpleBake couldn’t be loaded</b>
> <br>Make sure you have the SimpleBake addon installed
>
> ![Kranio_Addon Panel_warning01_sb-couldnt-load](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/15248f95-c920-4af7-b113-ea1a61378c9b)
>
> If you encounter this warning message it means that the SimpleBake addon is not installed on this version of Blender. Follow the instructions in the Dependencies - SimpleBake and Installation sections to get and install SimpleBake.
> Once SimpleBake is installed and enabled, you can either restart Blender or press the “Initialize SimpleBake” button.
> The “Get SimpleBake” button on this panel will take you to the same blendermarket.com page as linked in the Dependencies section, where you can purchase the SimpleBake addon.

<hr>

> [!WARNING]
> SimpleBake is installed but not enabled
> <br>Follow the instructions above to enable
>
> ![Kranio_Addon Panel_warning02_sb-installed-but-not-enabled](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/cc545ba4-7a9c-4cb7-9a90-e8113cf29faf)
>
> This means that you have correctly installed the SimpleBake addon, but it is simply not “enabled”. To enable it, open the same menu you did when installing KRANIO and SimpleBake, search for SimpleBake, and ensure the checkbox is checked:
>
> ![Kranio_SimpleBake Enable](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/8d4dc17e-0cce-4ea0-95c6-41eff84537f2)

<hr>

> [!WARNING]
> <b>Cannot bake an object that has no material</b>
> 
> ![Kranio_Addon Panel_warning02_sb-no-material](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/888aaa74-a570-4992-a323-64569e524fc8)
>
> This means that the object you have selected does not currently have a material applied.
> The selected objects are usually marked by an orange outline. You might not see any outlines if you have clicked somewhere else in the interface, but you can always see which object(s) Blender and KRANIO are considering as selected at the top of the panel.
> You can add a material from the KRANIO panel. Click on the red checkered sphere icon in the Properties panel to see which materials are currently on the object.
>
> ![Kranio_Selected Object with Material](https://github.com/CasparStanley/KRANIO-Addon/assets/14052888/54510158-fe41-4b92-bf51-f0d380ae2bf4)




