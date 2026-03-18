import bpy
import os
import sys

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

try:
    import addon_utils
    addon_utils.enable("io_import_images_as_planes")
except Exception as e:
    print("Addon failed to enable:", e)

argv = sys.argv
if "--" not in argv:
    argv = []
else:
    argv = argv[argv.index("--") + 1:]

if len(argv) < 2:
    print("Usage: blender -b -P script.py -- <image_path> <output_path>")
    sys.exit(1)

image_path = argv[0]
output_path = argv[1]

filename = os.path.basename(image_path)
directory = os.path.dirname(image_path)

try:
    bpy.ops.import_image.to_plane(files=[{"name": filename, "name": filename}], directory=directory, align_axis='Z+', height=2.0)
    obj = bpy.context.active_object
    if obj:
        mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        mod.thickness = 0.1
        bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
        print("Successfully exported:", output_path)
    else:
        print("Failed to import image as plane.")
except Exception as e:
    print("Error during import/export:", e)
