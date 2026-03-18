import bpy
import os
import sys

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    import addon_utils
    addon_utils.enable("io_import_images_as_planes")
except Exception as e:
    print("Addon failed:", e)

argv = sys.argv
if "--" not in argv:
    argv = []
else:
    argv = argv[argv.index("--") + 1:]

image_path = argv[0]
output_path = argv[1]

filename = os.path.basename(image_path)
directory = os.path.dirname(image_path)

bpy.ops.import_image.to_plane(files=[{"name": filename, "name": filename}], directory=directory, align_axis='Z+', height=2.0)
obj = bpy.context.active_object

if obj:
    # Subdivide heavily for displacement
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=50)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create texture from image
    tex = bpy.data.textures.new("DisplaceTex", type='IMAGE')
    img = bpy.data.images.load(image_path)
    tex.image = img
    
    # Add displace modifier
    disp_mod = obj.modifiers.new(name="Displacement", type='DISPLACE')
    disp_mod.texture = tex
    disp_mod.strength = 0.3 # Adjust depth
    disp_mod.mid_level = 0.5
    
    # Add solidify to give it volume
    sol_mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    sol_mod.thickness = 0.2
    
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print("Exported 3D displaced model:", output_path)
