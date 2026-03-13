import bpy
import sys

# Clear existing objects
bpy.ops.wm.read_factory_settings(use_empty=True)

# Create material function
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
    return mat

# Create materials for stylized agent
mat_body = create_material("BodyMat", (0.1, 0.4, 0.8, 1.0)) # Blue suit
mat_head = create_material("HeadMat", (0.9, 0.75, 0.6, 1.0)) # Skin tone
mat_eye = create_material("EyeMat", (0.05, 0.05, 0.05, 1.0)) # Dark eyes
mat_tie = create_material("TieMat", (0.8, 0.1, 0.1, 1.0)) # Red tie

# Body
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 2.5))
body = bpy.context.active_object
body.scale = (0.7, 0.4, 0.9)
body.data.materials.append(mat_body)

# Head
bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0, 0, 4.0))
head = bpy.context.active_object
head.data.materials.append(mat_head)

# Eyes (funny big blocky eyes)
bpy.ops.mesh.primitive_cube_add(size=0.15, location=(0.25, 0.6, 4.1))
eye1 = bpy.context.active_object
eye1.data.materials.append(mat_eye)

bpy.ops.mesh.primitive_cube_add(size=0.15, location=(-0.25, 0.6, 4.1))
eye2 = bpy.context.active_object
eye2.data.materials.append(mat_eye)

# Tie
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0.42, 2.8))
tie = bpy.context.active_object
tie.scale = (0.8, 0.1, 4.0)
tie.data.materials.append(mat_tie)

# Arms
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.9, 0, 2.5))
arm1 = bpy.context.active_object
arm1.scale = (0.3, 0.3, 1.6)
arm1.data.materials.append(mat_body)

bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.9, 0, 2.5))
arm2 = bpy.context.active_object
arm2.scale = (0.3, 0.3, 1.6)
arm2.data.materials.append(mat_body)

# Legs
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.35, 0, 0.8))
leg1 = bpy.context.active_object
leg1.scale = (0.4, 0.35, 1.6)
leg1.data.materials.append(mat_body)

bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.35, 0, 0.8))
leg2 = bpy.context.active_object
leg2.scale = (0.4, 0.35, 1.6)
leg2.data.materials.append(mat_body)

# Export
output_path = "/home/waheed/.openclaw/workspace/projects/AICity-03/static/3d-test-user/agent_generated.glb"
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
print(f"Generated 3D stylized agent at: {output_path}")
