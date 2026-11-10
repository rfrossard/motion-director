#!/usr/bin/env python3
"""Auditoria de qualidade do vídeo inteiro (portão obrigatório, references/quality.md §5).

1) Extrair:
     python scripts/audit.py extract out/video.mp4 [--plan src/b/plan.json] [--out work/audit]
   Gera em work/audit/:
     sheet_NN.png   3 frames por cena (22 %, 50 %, 78 %), com rótulo numa faixa própria
     trans_NN.png   cada passagem entre cenas: antes, meio da transição, depois
     motion_NN.png  movimento: 8 frames (a cada 3) em volta do meio de cada cena
     scores.md      tabelas a preencher (cenas e passagens), com coluna obrigatória de defeitos
2) Avaliar: de preferência um revisor independente (subagente que só vê as folhas, as referências e os traços obrigatórios).
   Liste os defeitos ANTES de dar as notas; nota 5 só com "nenhum".
3) Checar o portão:
     python scripts/audit.py check [--out work/audit]
   Código 1 se faltar nota ou defeito, se algum critério ficar < 4, ou se houver 5 com defeito listado.
Usa o ffmpeg completo do ambiente global (~/.local/share/motion-director/env) ou --ffmpeg.
"""
import argparse, json, os, re, shutil, subprocess, sys

CRIT = ['composição', 'ofício', 'movimento', 'legibilidade', 'fidelidade']
FONT = next((p for p in ['/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'] if os.path.exists(p)), None)


def timeline(plan):
    d = json.load(open(plan)); ov = d.get('overlap', {}); at = 0; out = []
    for s in d['scenes']:
        o = ov.get(s.get('out', ''), 0)
        out.append((s['id'], at, s['dur'], o)); at += s['dur'] - o
    return out


def ffbin(a):
    for c in [a, os.path.expanduser('~/.local/share/motion-director/env/bin/ffmpeg'), 'tools/env/bin/ffmpeg', shutil.which('ffmpeg')]:
        if c and os.path.exists(c): return c
    sys.exit('ffmpeg completo não encontrado; use --ffmpeg')


def lab(label, w=640, h=360):
    vf = f'scale={w}:{h},pad={w}:{h + 34}:0:34:color=black'
    if FONT: vf += f",drawtext=fontfile='{FONT}':text='{label}':x=10:y=8:fontsize=20:fontcolor=white"
    return vf


def run(*args): subprocess.run(list(args), check=True)


def sheets(ff, src_dir, prefix, n, per, grid, out):
    for k in range(0, n, per):
        run(ff, '-hide_banner', '-loglevel', 'error', '-y', '-framerate', '1', '-start_number', str(k), '-i', os.path.join(src_dir, 's_%04d.png'),
            '-frames:v', str(min(per, n - k)), '-vf', f'tile={grid}:padding=4:color=white', '-frames:v', '1', os.path.join(out, f'{prefix}_{k // per + 1:02d}.png'))


def extract(a):
    ff = ffbin(a.ffmpeg); fps = a.fps; tl = timeline(a.plan)
    os.makedirs(a.out, exist_ok=True)
    grab = lambda fr, vf, path: run(ff, '-hide_banner', '-loglevel', 'error', '-y', '-ss', f'{max(0, fr) / fps:.3f}', '-i', a.video, '-frames:v', '1', '-vf', vf, path)
    # cenas
    d = os.path.join(a.out, 'tiles'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d); i = 0
    for sid, st, dur, _ in tl:
        for p in (0.22, 0.5, 0.78):
            fr = st + int(dur * p); grab(fr, lab(f'{sid}  {int(p * 100)} pct  f{fr}'), os.path.join(d, f's_{i:04d}.png')); i += 1
    sheets(ff, d, 'sheet', i, 24, '3x8', a.out); ns = i
    # passagens: antes, meio da sobreposição, depois
    d = os.path.join(a.out, 'ttiles'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d); i = 0; trans = []
    for (s0, _, _, ov), (s1, st1, _, _) in zip(tl, tl[1:]):
        name = f'{s0} > {s1}'; trans.append(name)
        for tag, fr in (('antes', st1 - 6), ('meio', st1 + max(1, ov) // 2), ('depois', st1 + max(ov, 1) + 6)):
            grab(fr, lab(f'{name}  {tag}  f{fr}'), os.path.join(d, f's_{i:04d}.png')); i += 1
    sheets(ff, d, 'trans', i, 24, '3x8', a.out)
    # movimento: 8 frames, um a cada 3, em volta do meio
    d = os.path.join(a.out, 'mtiles'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d); i = 0
    for sid, st, dur, _ in tl:
        fr = st + dur // 2 - 12
        vf = "select='not(mod(n\\,3))',scale=240:135,tile=8x1,pad=iw:ih+30:0:30:color=black"
        if FONT: vf += f",drawtext=fontfile='{FONT}':text='{sid}  movimento f{fr}..{fr + 21}':x=8:y=6:fontsize=18:fontcolor=white"
        run(ff, '-hide_banner', '-loglevel', 'error', '-y', '-ss', f'{fr / fps:.3f}', '-i', a.video, '-vf', vf, '-frames:v', '1', os.path.join(d, f's_{i:04d}.png')); i += 1
    sheets(ff, d, 'motion', i, 10, '1x10', a.out)
    sc = os.path.join(a.out, 'scores.md')
    if not os.path.exists(sc) or a.force:
        with open(sc, 'w') as w:
            w.write('# Auditoria — portão: todos os critérios ≥ 4; defeitos listados antes das notas; 5 só com "nenhum"\n\n')
            w.write('revisor: <independente | autor>\n\n')
            w.write('| cena | defeitos (antes das notas) | ' + ' | '.join(CRIT) + ' |\n|' + '---|' * (len(CRIT) + 2) + '\n')
            for sid, *_ in tl: w.write(f'| {sid} | |' + ' |' * len(CRIT) + '\n')
            w.write('\n| passagem | defeitos (antes das notas) | nota |\n|---|---|---|\n')
            for t in trans: w.write(f'| {t} | | |\n')
    print(f'{ns} frames de cena, {len(trans)} passagens, {len(tl)} tiras de movimento em {a.out}; preencha {sc} e rode `audit.py check`.')


def num(v):
    m = re.match(r'^(\d+(?:[.,]\d)?)', v.strip())
    return float(m.group(1).replace(',', '.')) if m else None


def check(a):
    sc = os.path.join(a.out, 'scores.md'); bad = {}; n = 0; mode = None; rev = None
    for line in open(sc):
        if line.lower().startswith('revisor:'): rev = line.split(':', 1)[1].strip()
        if not line.strip().startswith('|'): continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if cells[0] in ('cena', 'passagem'): mode = cells[0]; continue
        if set(cells[0]) <= set('-: '): continue
        key, defects, notes = cells[0], cells[1], cells[2:]
        crit = CRIT if mode == 'cena' else ['nota']
        n += 1; prob = []
        if not defects: prob.append('defeitos não listados')
        for c, v in zip(crit, notes + [''] * len(crit)):
            x = num(v)
            if x is None: prob.append(f'sem nota em {c}')
            elif x < 4: prob.append(f'{c} = {v}')
            elif x >= 5 and defects and defects.lower() not in ('nenhum', 'nenhum.', '—', '-'): prob.append(f'{c} = 5 com defeito listado')
        if prob: bad[key] = prob
    if not n: sys.exit('scores.md sem linhas')
    if not rev or rev.startswith('<'): print('aviso: preencha "revisor:" (independente ou autor).')
    elif 'autor' in rev.lower(): print('aviso: revisão feita pelo próprio autor. Se puder, peça um revisor independente (subagente).')
    if bad:
        print(f'PORTÃO FECHADO — {len(bad)} item(ns) com problema:')
        for k, vs in bad.items():
            print(f' - {k}: ' + ('não avaliado' if all(v.startswith('sem nota') or v.startswith('defeitos') for v in vs) else '; '.join(vs)))
        sys.exit(1)
    print(f'PORTÃO ABERTO — {n} itens (cenas e passagens), todos ≥ 4.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    e = sp.add_parser('extract'); e.add_argument('video'); e.add_argument('--plan', default='src/b/plan.json'); e.add_argument('--out', default='work/audit'); e.add_argument('--fps', type=float, default=30); e.add_argument('--ffmpeg'); e.add_argument('--force', action='store_true')
    c = sp.add_parser('check'); c.add_argument('--out', default='work/audit')
    a = ap.parse_args(); extract(a) if a.cmd == 'extract' else check(a)
