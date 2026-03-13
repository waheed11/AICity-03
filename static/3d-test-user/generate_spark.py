import bpy
import math

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Helper for materials
def create_mat(name, color, metallic=0.0, roughness=0.5, transmission=0.0, emission=None, emission_strength=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        if 'Transmission Weight' in bsdf.inputs: # Blender 4.0+
            bsdf.inputs['Transmission Weight'].default_value = transmission
        else:
            bsdf.inputs['Transmission'].default_value = transmission
            
        if emission:
            bsdf.inputs['Emission Color'].default_value = emission
            bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

# Materials
mat_skin = create_mat("Skin", (0.9, 0.7, 0.6, 1.0), roughness=0.4)
mat_suit = create_mat("Suit", (0.8, 0.8, 0.8, 1.0), metallic=0.2, roughness=0.3)
mat_glass = create_mat("Glass", (1.0, 1.0, 1.0, 1.0), roughness=0.0, transmission=1.0)
mat_glow_green = create_mat("GlowGreen", (0.0, 1.0, 0.0, 1.0), emission=(0.0, 1.0, 0.0, 1.0), emission_strength=5.0)
mat_glow_gold = create_mat("GlowGold", (1.0, 0.8, 0.1, 1.0), emission=(1.0, 0.8, 0.1, 1.0), emission_strength=5.0)
mat_dark = create_mat("Dark", (0.1, 0.1, 0.1, 1.0))
mat_cheek = create_mat("Cheek", (1.0, 0.4, 0.5, 1.0))

# Create Body
bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=1.5, location=(0, 0, 0.75))
body = bpy.context.active_object
body.data.materials.append(mat_suit)
bpy.ops.object.shade_smooth()

# Create Head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 2.0))
head = bpy.context.active_object
head.data.materials.append(mat_skin)
bpy.ops.object.shade_smooth()

# Create Cheeks
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(0.3, 0.7, 1.9))
cheek1 = bpy.context.active_object
cheek1.scale[1] = 0.3
cheek1.data.materials.append(mat_cheek)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(-0.3, 0.7, 1.9))
cheek2 = bpy.context.active_object
cheek2.scale[1] = 0.3
cheek2.data.materials.append(mat_cheek)

# Create Monocle
bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.1, location=(0.3, 0.75, 2.1))
monocle = bpy.context.active_object
monocle.rotation_euler = (math.pi/2, 0, 0)
monocle.data.materials.append(mat_glow_green)

# Create Eye (Other)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(-0.3, 0.75, 2.1))
eye2 = bpy.context.active_object
eye2.scale[1] = 0.2
eye2.data.materials.append(mat_dark)

# Create Helmet
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, location=(0, 0, 2.0))
helmet = bpy.context.active_object
helmet.data.materials.append(mat_glass)
bpy.ops.object.shade_smooth()

# Antennae
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.5, location=(1.25, 0, 2.0))
ant1 = bpy.context.active_object
ant1.rotation_euler = (0, math.pi/2, 0)
ant1.data.materials.append(mat_glow_gold)

bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.5, location=(-1.25, 0, 2.0))
ant2 = bpy.context.active_object
ant2.rotation_euler = (0, math.pi/2, 0)
ant2.data.materials.append(mat_glow_gold)

# Nameplate SPARK
bpy.ops.object.text_add(location=(-0.3, 0.65, 1.0))
txt_spark = bpy.context.active_object
txt_spark.data.body = "SPARK"
txt_spark.scale = (0.2, 0.2, 0.2)
txt_spark.rotation_euler = (math.pi/2, 0, 0)
txt_spark.data.materials.append(mat_dark)
bpy.ops.object.convert(target='MESH')

# ONLINE HUD
bpy.ops.object.text_add(location=(-0.3, 0.9, 2.8))
txt_online = bpy.context.active_object
txt_online.data.body = "ONLINE"
txt_online.scale = (0.2, 0.2, 0.2)
txt_online.rotation_euler = (math.pi/2, 0, 0)
txt_online.data.materials.append(mat_glow_green)
bpy.ops.object.convert(target='MESH')

# 3-Point Lighting
bpy.ops.object.light_add(type='AREA', radius=5, location=(3, -3, 4))
light_key = bpy.context.active_object
light_key.data.energy = 500
light_key.rotation_euler = (math.pi/4, 0, math.pi/4)

bpy.ops.object.light_add(type='AREA', radius=5, location=(-4, -1, 3))
light_fill = bpy.context.active_object
light_fill.data.energy = 200
light_fill.rotation_euler = (math.pi/4, 0, -math.pi/4)

bpy.ops.object.light_add(type='AREA', radius=3, location=(0, 4, 3))
light_rim = bpy.context.active_object
light_rim.data.energy = 800
light_rim.rotation_euler = (-math.pi/4, 0, math.pi)
light_rim.data.color = (0.5, 0.8, 1.0) # Bluish rim

# Create basic Rig (Armature)
bpy.ops.object.armature_add(location=(0, 0, 0))
rig = bpy.context.active_object
bpy.ops.object.mode_set(mode='EDIT')
bone_base = rig.data.edit_bones[0]
bone_base.tail = (0, 0, 1.5)
bone_head = rig.data.edit_bones.new("Head")
bone_head.head = (0, 0, 1.5)
bone_head.tail = (0, 0, 2.8)
bone_head.parent = bone_base
bpy.ops.object.mode_set(mode='OBJECT')

# Setup Render Settings (Cycles)
bpy.context.scene.render.engine = 'CYCLES'

# Export GLB
output_path = "/home/waheed/.openclaw/workspace/projects/AICity-03/static/3d-test-user/spark_agent.glb"
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
print("Spark agent exported successfully!")
