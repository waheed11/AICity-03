import bpy
import sys
import os
import subprocess

# Ensure opencv is installed
try:
    import cv2
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "opencv-python", "numpy"])
    import cv2
    import numpy as np

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

argv = sys.argv
if "--" not in argv:
    argv = []
else:
    argv = argv[argv.index("--") + 1:]

image_path = argv[0]
output_path = argv[1]

# Load image with OpenCV
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
if img is None:
    print("Could not load image:", image_path)
    sys.exit(1)

# Check if image has alpha channel
if len(img.shape) == 3 and img.shape[2] == 4:
    alpha = img[:, :, 3]
else:
    # Convert to grayscale and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(alpha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if not contours:
    print("No contours found.")
    sys.exit(1)

# Find largest contour
contour = max(contours, key=cv2.contourArea)

# Scale contour points to Blender space
height, width = img.shape[:2]
scale = 2.0 / max(height, width)

# Create a curve object
curveData = bpy.data.curves.new('MyCurve', type='CURVE')
curveData.dimensions = '2D'
curveData.extrude = 0.1 # This gives the 3D thickness!
curveData.resolution_u = 2

# Add splines
polyline = curveData.splines.new('POLY')
polyline.points.add(len(contour) - 1)
polyline.use_cyclic_u = True

for i, point in enumerate(contour):
    x, y = point[0]
    # Normalize and center
    bx = (x - width/2) * scale
    by = -(y - height/2) * scale # Invert Y for Blender
    polyline.points[i].co = (bx, by, 0.0, 1.0)

curveObj = bpy.data.objects.new('ExtrudedShape', curveData)
bpy.context.collection.objects.link(curveObj)
bpy.context.view_layer.objects.active = curveObj
curveObj.select_set(True)

# Convert curve to mesh
bpy.ops.object.convert(target='MESH')
meshObj = bpy.context.active_object

# Export
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
print("Successfully generated true 3D contour model:", output_path)
