# Reconstrução 3D realista — Blender Python (`blender3d`)

**Look**: cena fotorrealista (luz física, materiais PBR, profundidade de campo, névoa atmosférica) com câmera de cinema: travelling lento, grua, dolly.
**Usos**: "como era" (lugares e épocas), arquitetura, produto 3D, maquetes, recriações históricas.
**Exemplos**: "1906 San Francisco Market Street in Blender" (@alexalbert__, 418 salvos), "Hindenburg disaster recreated in Blender" (@aimanhasnoname), seção Blender do showreel de @shneural.

## Método (do exemplo de Market Street)
1. **Arquivo de fontes antes de modelar**: cada objeto com dimensões, material, fonte e grau de confiança (mapas, fotos, plantas, dados públicos).
2. **Geradores reutilizáveis** em Python (`bpy`): fachada, telhado, janelas, postes, veículos — a cena é montada **a partir dos dados**, não à mão.
3. Sem meshes/texturas/HDRIs baixados, salvo licença clara; materiais procedurais (Principled BSDF + noise).
4. Câmera: 1–3 movimentos longos com easing; lente 24–50 mm; DOF suave.
5. Render: Eevee para rascunho; Cycles (64–256 amostras + denoise) para final; 1920×1080, mesmo fps do projeto.

## Técnica
```bash
blender -b -P scene.py -- --out renders/frame_#### --frames 1-300   # headless
ffmpeg -framerate 30 -i renders/frame_%04d.png -c:v libx264 -pix_fmt yuv420p clip.mp4
```
```python
import bpy, math
def facade(x, y, w, h, floors, material): ...   # gera geometria a partir de parâmetros
cam = bpy.data.objects['Camera']
for f, (loc, rot) in enumerate(path):           # path calculado com easing
    cam.location, cam.rotation_euler = loc, rot
    cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f)
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'  # confira o nome na versão instalada
```

## Armadilhas
- Verifique a versão (`blender --version`) e os nomes de API antes de usar; mudam entre versões.
- Render final é lento: faça stills primeiro, depois um trecho de 2 s, depois tudo.
- Pessoas fotorrealistas: evite ou use silhuetas — erram fácil e caem no vale da estranheza.
- Fatos históricos: cite fontes no `CREDITS.md`; marque reconstruções incertas.

## Bastões
Câmera atravessa uma janela/porta e o próximo estilo está "do outro lado"; ou a cena congela e vira foto (passagem para `collage`/`archival`).

## Prompt-semente
"Reconstrua <lugar/objeto, data> no Blender via Python. Primeiro monte um arquivo de fontes (dimensões, materiais, referências, confiança). Escreva geradores reutilizáveis e monte a cena a partir dos dados. Sem assets baixados. Um movimento de câmera de <N> s, 1080p30."

**Status**: testado no vídeo "Biblioteca de estilos" (08/11/2026). Código: `assets/kit2/engines/blender/cena.py → clipe` · cena `BlenderS`.

**Lições do teste**: Blender 5.2 Eevee ≈0,45 s/frame. Armadilhas resolvidas: `transform_apply` aplica location/rotation por padrão (use `location=False, rotation=False, scale=True`); cubo não mapeia textura numa face (use plano); posicione peças pela `matrix_world` da peça-mãe; evite divisão por (NF−1) com 1 frame.

**Auditoria (09/11/2026)** (composição / ofício / movimento / legibilidade / fidelidade): 4,5 / 4,5 / 4 / 4 / 4,5. Passa.
