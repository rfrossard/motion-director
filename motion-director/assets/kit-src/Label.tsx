import React from 'react';
import {C, F, SAFE} from './theme';
import {softIn} from './lib';

// Rótulo de formato no canto superior esquerdo + linha de características em mono
export const FormatLabel: React.FC<{
	frame: number;
	f0: number;
	n: number;
	name: string;
	traits: string;
	dark?: boolean;
	accent?: string;
	traitsColor?: string;
}> = ({frame, f0, n, name, traits, dark = true, accent = C.orange, traitsColor}) => {
	const a = softIn(frame, f0);
	const b = softIn(frame, f0 + 8);
	return (
		<div style={{position: 'absolute', left: SAFE, top: SAFE - 20}}>
			<div
				style={{
					fontFamily: F.display,
					fontWeight: 800,
					fontSize: 30,
					letterSpacing: '0.08em',
					color: dark ? C.ink : C.navy,
					opacity: a.opacity,
					transform: `translateY(${a.y}px)`,
					filter: `blur(${a.blur}px)`,
					whiteSpace: 'nowrap',
				}}
			>
				<span style={{color: accent}}>FORMATO {n}</span> · {name}
			</div>
			<div
				style={{
					fontFamily: F.mono,
					fontSize: 20,
					marginTop: 10,
					color: traitsColor ?? (dark ? C.muted : '#4f5566'),
					opacity: b.opacity,
					transform: `translateY(${b.y}px)`,
					whiteSpace: 'nowrap',
				}}
			>
				{traits}
			</div>
		</div>
	);
};
