import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, random, staticFile, useCurrentFrame} from 'remotion';
import {C, F, SAFE} from '../theme';
import {clamp, easeIn, easeInOut, expo, lerp, seg} from '../lib';
import {FormatLabel} from '../Label';
import {CLIP_IN, EDITORIAL_LEN} from '../timeline';
import edl from '../editorial-edl.json';

// Formato 9: entrevista editorial — o clipe INTEIRO, com P&B claro, bloom, grão, palavras cinéticas,
// tela dividida que desliza junto com quem fala e legendas queimadas no estilo `caption` sobre `surface`.
type Word = {w: string; s: number; e: number}; // tempos em segundos do clipe
type Kinetic = {text: string; s: number; e: number; x: number; y: number; size: number; accent?: boolean; ink?: boolean};
type Split = {s: number; e: number; quote: string; faceX: number};
const EDL = edl as {captions: Word[][]; kinetic: Kinetic[]; splits: Split[]};

const SRC = staticFile('source/entrevista.mp4');
const LOWER_THIRD: [number, number] = [21.6, 26.0]; // crachá do JN no clipe (s)
const GRADE = 'grayscale(1) contrast(1.07) brightness(1.1)';

const Clip: React.FC<{objectPosition?: string; muted?: boolean; extraFilter?: string}> = ({objectPosition = '50% 50%', muted = true, extraFilter = ''}) => (
	<OffthreadVideo src={SRC} muted={muted} volume={muted ? 0 : 1.45} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition, filter: `${GRADE} ${extraFilter}`}} />
);

// imagem tratada: grade + bloom + pretos levantados
const Picture: React.FC<{objectPosition?: string; withAudio?: boolean}> = ({objectPosition, withAudio}) => (
	<AbsoluteFill>
		<Clip objectPosition={objectPosition} muted={!withAudio} />
		<AbsoluteFill style={{mixBlendMode: 'screen', opacity: 0.28}}>
			<Clip objectPosition={objectPosition} extraFilter="brightness(1.5) contrast(2.2) blur(16px)" />
		</AbsoluteFill>
		<AbsoluteFill style={{background: 'rgb(16,16,16)', mixBlendMode: 'lighten'}} />
	</AbsoluteFill>
);

const Grain: React.FC<{f: number}> = ({f}) => (
	<AbsoluteFill style={{mixBlendMode: 'overlay', opacity: 0.09, pointerEvents: 'none'}}>
		<svg width="100%" height="100%">
			<filter id="ed-grain">
				<feTurbulence type="fractalNoise" baseFrequency={0.95} numOctaves={2} seed={f} stitchTiles="stitch" />
				<feColorMatrix type="saturate" values="0" />
			</filter>
			<rect width="100%" height="100%" filter="url(#ed-grain)" />
		</svg>
	</AbsoluteFill>
);

export const Editorial: React.FC = () => {
	const f = useCurrentFrame();
	const t = (f - CLIP_IN) / 30; // tempo do clipe em segundos
	const weave = {x: (random(`wx${f}`) - 0.5) * 1.2, y: (random(`wy${f}`) - 0.5) * 1.2};
	// tela dividida ativa?
	const sp = EDL.splits.find((s) => t >= s.s - 0.1 && t <= s.e + 0.5);
	let insertW = 0;
	if (sp) {
		const pin = easeInOut(clamp((t - sp.s) / 0.4));
		const pout = easeInOut(clamp((t - sp.e) / 0.4));
		insertW = 760 * (pin - pout);
	}
	// legenda atual (grupo de palavras)
	const group = EDL.captions.find((g) => t >= g[0].s - 0.05 && t <= g[g.length - 1].e + 0.25);
	// saída: íris fecha até um ponto
	const iris = easeIn(seg(f, EDITORIAL_LEN - 35, EDITORIAL_LEN));
	const irisR = lerp(1200, 0, iris);
	return (
		<AbsoluteFill style={{background: C.stage}}>
			<AbsoluteFill style={{clipPath: `circle(${irisR}px at 50% 50%)`}}>
				<Sequence from={CLIP_IN} layout="none">
					{/* quem fala: painel à direita, recortado de novo (nunca espremido) */}
					<div style={{position: 'absolute', left: insertW, top: 0, width: 1920 - insertW, height: 1080, overflow: 'hidden', transform: `translate(${weave.x}px, ${weave.y}px)`}}>
						<div style={{position: 'absolute', left: 0, width: 1920 - insertW, height: 1080}}>
							<Picture withAudio objectPosition={sp ? `${sp.faceX * 100}% 50%` : '50% 50%'} />
						</div>
					</div>
				</Sequence>
				{/* painel de inserto: citação em tipografia editorial */}
				{sp && insertW > 1 && (
					<div style={{position: 'absolute', left: 0, top: 0, width: insertW, height: 1080, background: '#f2efe8', overflow: 'hidden'}}>
						<div style={{position: 'absolute', left: 70, top: 300, width: 620, opacity: clamp((t - sp.s - 0.3) / 0.3)}}>
							<div style={{fontFamily: F.mono, fontSize: 20, letterSpacing: '0.08em', color: '#4f5566'}}>EM PRIMEIRA PESSOA</div>
							<div style={{fontFamily: F.itau, fontWeight: 300, fontSize: 58, lineHeight: '68px', color: '#111114', marginTop: 26}}>“{sp.quote}”</div>
							<div style={{width: 80, height: 4, background: C.orange, marginTop: 34}} />
						</div>
					</div>
				)}
				{/* palavras cinéticas no tempo da fala */}
				{EDL.kinetic.map((k, i) => {
					if (t < k.s || t > k.e + 0.2) return null;
					const e = expo((t - k.s) / 0.32);
					const out = clamp((t - k.e) / 0.2);
					const drift = (t - k.s) * 0.03;
					return (
						<div key={i} style={{position: 'absolute', left: k.x, top: k.y, fontFamily: k.accent ? F.itau : F.display, fontWeight: k.accent ? 300 : 800, fontSize: k.size, lineHeight: 0.95, color: k.ink ? '#111114' : '#fff', whiteSpace: 'nowrap', textShadow: k.ink ? '0 0 30px rgba(255,255,255,0.5)' : '0 4px 26px rgba(0,0,0,0.45)', opacity: clamp((t - k.s) * 14) * (1 - out), transform: `translateY(${(1 - e) * 0.32 + drift}em)`, filter: `blur(${(1 - e) * 9 + out * 6}px)`}}>
							{k.text}
						</div>
					);
				})}
				<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.32) 100%)'}} />
				<Grain f={f} />
				{/* legendas queimadas: caption sobre surface */}
				{group && (
					<div style={{position: 'absolute', left: 0, width: 1920, top: t >= LOWER_THIRD[0] && t <= LOWER_THIRD[1] ? 790 : 905, display: 'flex', justifyContent: 'center'}}>
						<div style={{maxWidth: 1300, background: 'rgba(17,21,27,0.86)', borderRadius: 4, padding: '10px 22px', fontFamily: F.display, fontWeight: 700, fontSize: 40, lineHeight: '50px', color: C.ink, textAlign: 'center'}}>
							{group.map((w, i) => (
								<span key={i} style={{opacity: t >= w.s - 0.05 ? 1 : 0.35}}>{(i ? ' ' : '') + w.w}</span>
							))}
						</div>
					</div>
				)}
				<div style={{position: 'absolute', right: SAFE, top: 84, fontFamily: F.mono, fontSize: 18, color: 'rgba(243,244,247,0.75)'}}>Imagens: TV Globo / Jornal Nacional</div>
				{f < 270 && <FormatLabel frame={f} f0={20} n={9} name="ENTREVISTA EDITORIAL" traits="P&B claro · grão · tipografia cinética" />}
			</AbsoluteFill>
			{/* contorno que veio do "paper" */}
			{f < CLIP_IN + 4 && <div style={{position: 'absolute', inset: 0, border: `2.5px solid ${C.ink}`}} />}
		</AbsoluteFill>
	);
};
