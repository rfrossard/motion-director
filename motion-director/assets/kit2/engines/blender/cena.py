# Cena 18 — reconstrução realista "a cena do render". Uso: blender -b -P blender/cena.py -- <out_dir> <frames>
import bpy, math, sys, os
argv = sys.argv[sys.argv.index('--') + 1:]
OUT, NF = argv[0], int(argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
for eng in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'):
    try: sc.render.engine = eng; break
    except Exception: pass
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.fps = 30; sc.frame_start, sc.frame_end = 1, NF
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = os.path.join(OUT, 'f_')
try: sc.eevee.taa_render_samples = 48
except Exception: pass
try: sc.view_settings.view_transform = 'AgX'
except Exception: pass

def mat(name, color, rough=0.5, metal=0.0, emit=None, strength=0.0, img=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if img:
        t = m.node_tree.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(img)
        m.node_tree.links.new(t.outputs['Color'], b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value = strength
        m.node_tree.links.new(t.outputs['Color'], b.inputs['Base Color'])
    return m

def box(name, size, loc, m, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name
    o.scale = size; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        bv = o.modifiers.new('bv', 'BEVEL'); bv.width = bevel; bv.segments = 4
    o.data.materials.append(m); return o

# mesa de madeira (veio procedural)
wood = bpy.data.materials.new('wood'); wood.use_nodes = True; nt = wood.node_tree
bsdf = nt.nodes['Principled BSDF']; wave = nt.nodes.new('ShaderNodeTexWave'); wave.inputs['Scale'].default_value = 1.6; wave.inputs['Distortion'].default_value = 2.5; wave.inputs['Detail'].default_value = 6
ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = (0.16, 0.085, 0.045, 1); ramp.color_ramp.elements[1].color = (0.27, 0.15, 0.08, 1)
nt.links.new(wave.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color']); bsdf.inputs['Roughness'].default_value = 0.42
box('mesa', (3.2, 1.8, 0.06), (0, 0, -0.03), wood, 0.01)
# parede e chão de fundo
box('parede', (8, 0.1, 4), (0, 1.6, 1.5), mat('parede', (0.62, 0.6, 0.57), 0.9))
# notebook
alu = mat('alu', (0.55, 0.56, 0.58), 0.3, 0.9)
box('base', (1.2, 0.8, 0.03), (0, 0.05, 0.015), alu, 0.012)
box('teclado', (1.05, 0.38, 0.005), (0, 0.12, 0.032), mat('tecl', (0.05, 0.05, 0.06), 0.6))
tela_tampa = box('tampa', (1.2, 0.025, 0.78), (0, 0.46, 0.41), alu, 0.012)
tela_tampa.rotation_euler = (math.radians(-12), 0, 0)
bpy.ops.mesh.primitive_plane_add(size=1); tela = bpy.context.object; tela.name = 'tela'
tela.scale = (1.1, 0.69, 1); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
tela.data.materials.append(mat('tela', (1, 1, 1), 0.6, img=os.path.join(HERE, 'screen.png'), strength=3.0))
# a tela segue a matriz real da tampa: face da frente, em pé no espaço local da tampa
from mathutils import Matrix, Euler
bpy.context.view_layer.update()
tela.matrix_world = tela_tampa.matrix_world @ Matrix.Translation((0, -0.0135, 0)) @ Euler((math.radians(90), 0, 0)).to_matrix().to_4x4()
# caneca + café + vapor
bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.22, location=(0.92, -0.15, 0.11)); caneca = bpy.context.object
caneca.data.materials.append(mat('ceram', (0.93, 0.36, 0.08), 0.35))
bpy.ops.mesh.primitive_torus_add(major_radius=0.07, minor_radius=0.018, location=(1.04, -0.15, 0.12), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(mat('ceram2', (0.93, 0.36, 0.08), 0.35))
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.01, location=(0.92, -0.15, 0.2)); bpy.context.object.data.materials.append(mat('cafe', (0.08, 0.04, 0.02), 0.1))
# caderno e caneta
box('caderno', (0.42, 0.55, 0.02), (-0.95, -0.2, 0.01), mat('papel', (0.92, 0.9, 0.84), 0.85), 0.004).rotation_euler = (0, 0, math.radians(12))
bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.32, location=(-0.85, -0.2, 0.03), rotation=(0, math.radians(90), math.radians(30)))
bpy.context.object.data.materials.append(mat('caneta', (0.02, 0.02, 0.15), 0.3, 0.4))
# luzes: janela (área quente) + preenchimento frio + brilho da tela
bpy.ops.object.light_add(type='AREA', location=(-2.2, -1.2, 2.2)); k = bpy.context.object; k.data.energy = 420; k.data.size = 2.5; k.data.color = (1.0, 0.82, 0.62)
k.rotation_euler = (math.radians(50), math.radians(-35), 0)
bpy.ops.object.light_add(type='AREA', location=(2.5, -2.0, 1.5)); f = bpy.context.object; f.data.energy = 120; f.data.size = 3; f.data.color = (0.6, 0.7, 1.0)
f.rotation_euler = (math.radians(60), math.radians(40), 0)
bpy.ops.object.light_add(type='POINT', location=(0.9, -0.6, 0.9)); s = bpy.context.object; s.data.energy = 15; s.data.color = (1.0, 0.6, 0.3)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.03, 0.03, 0.04, 1)
# câmera: dolly lento até a tela preencher o quadro
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
cam.data.lens = 35; cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = 2.8
tgt = bpy.data.objects.new('alvo', None); sc.collection.objects.link(tgt); bpy.context.view_layer.update(); tgt.location = tela.matrix_world.translation
tc = cam.constraints.new('TRACK_TO'); tc.target = tgt; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
cam.data.dof.focus_object = tgt
def ease(x): return x * x * (3 - 2 * x)
for fr in range(1, NF + 1):
    k = ease((fr - 1) / max(1, NF - 1))
    a = math.radians(-38 + 34 * k)                     # gira do lado da caneca para frente
    r = 3.0 - 2.25 * (k ** 1.6)                         # aproxima
    cam.location = (math.sin(a) * r, -math.cos(a) * r + 0.44, 0.95 - 0.5 * k)
    cam.keyframe_insert('location', frame=fr)
bpy.ops.render.render(animation=True)
