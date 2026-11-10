import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import * as THREE from 'three';
import {SVGLoader} from 'three/examples/jsm/loaders/SVGLoader.js';
import parts from '../brand-parts.json';
import {C, F} from '../theme';
import {easeIn, easeInOut, lerp, seg, softIn, spring01} from '../lib';
import {FormatLabel} from '../Label';

// Formato 10: logo do International Hub extrudado em 3D (tratamento 07) — peças com os paths oficiais
// Convenção: `z` é a face da frente da peça; a extrusão vai `depth` para trás.
type Part = {d: string; role: 'primary' | 'text' | 'cut'; z: number; depth: number; delay?: number};
type Brand = {id: string; vb: number[]; cutDark: string; parts: Part[]};
const HUB = (parts as Brand[]).find((b) => b.id === 'hub')!;
const [, , VW, VH] = HUB.vb;

const color = (p: Part) => (p.role === 'primary' ? C.orange : p.role === 'text' ? '#ffffff' : HUB.cutDark);

const Logo3D: React.FC<{f: number}> = ({f}) => {
	const geos = useMemo(() => {
		const loader = new SVGLoader();
		return HUB.parts.map((p) => {
			const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${VW} ${VH}"><path fill-rule="evenodd" d="${p.d}"/></svg>`;
			const data = loader.parse(svg);
			const shapes = data.paths.flatMap((path) => SVGLoader.createShapes(path));
			const g = new THREE.ExtrudeGeometry(shapes, {depth: p.depth, bevelEnabled: true, bevelThickness: 1.2, bevelSize: 0.8, bevelSegments: 2, curveSegments: 10});
			g.translate(-VW / 2, -VH / 2, -p.depth);
			return g;
		});
	}, []);
	const t = f / 30;
	const sep = spring01((f - 40) / 30, 7, 0.78); // as peças se separam em Z
	const enter = spring01((f - 4) / 30, 9, 0.8);
	const rotY = lerp(-0.55, 0.42, easeInOut(seg(f, 0, 240))) + Math.sin(t * 1.3) * 0.04;
	const rotX = 0.16 + Math.sin(t * 0.9) * 0.03;
	const s = 0.0105 * enter;
	return (
		<group rotation={[rotX, rotY, 0]} scale={[s, -s, s]}>
			{HUB.parts.map((p, i) => (
				<mesh key={i} geometry={geos[i]} position={[0, 0, p.z * 2.2 * sep]}>
					<meshStandardMaterial color={color(p)} roughness={0.42} metalness={0.08} />
				</mesh>
			))}
		</group>
	);
};

export const Future3D: React.FC = () => {
	const f = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const head = softIn(f, 70, 12);
	const flood = easeIn(seg(f, 214, 240));
	return (
		<AbsoluteFill style={{background: C.stage}}>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, #0b0b3a 0%, #000 65%)'}} />
			<ThreeCanvas width={width} height={height} camera={{fov: 32, position: [0, 0.2, 11]}}>
				<ambientLight intensity={0.55} />
				<directionalLight position={[3, 4, 7]} intensity={2.4} />
				<pointLight position={[-5, -2, 4]} intensity={40} color={C.orange} />
				<pointLight position={[4, 2, -3]} intensity={25} color="#6f7bff" />
				<Logo3D f={f} />
			</ThreeCanvas>
			<div style={{position: 'absolute', top: 870, width: 1920, textAlign: 'center', fontFamily: F.itau, fontWeight: 300, fontSize: 64, color: C.ink, opacity: head.opacity * (1 - flood), transform: `translateY(${head.y}px)`, filter: `blur(${head.blur}px)`}}>
				Para onde isso pode ir
			</div>
			{/* saída: o laranja inunda a tela a partir do centro */}
			<svg width={1920} height={1080} style={{position: 'absolute'}}>
				<circle cx={960} cy={500} r={lerp(0, 1150, flood)} fill={C.orange} />
			</svg>
			{f < 214 && <FormatLabel frame={f} f0={10} n={10} name="VISÃO DE FUTURO" traits="3D extrudado · profundidade · acento" />}
		</AbsoluteFill>
	);
};
