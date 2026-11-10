import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {Intro, Outro} from './scenes/Bookends';
import {Led} from './scenes/Led';
import {Flat} from './scenes/Flat';
import {Collage, TEAR} from './scenes/Collage';
import {Timeline} from './scenes/Timeline';
import {Journey} from './scenes/Journey';
import {UiDemo} from './scenes/UiDemo';
import {DataStory} from './scenes/DataStory';
import {Paper} from './scenes/Paper';
import {Editorial} from './scenes/Editorial';
import {Future3D} from './scenes/Future3D';
import {Hype} from './scenes/Hype';
import {C} from './theme';
import {SCENE, T} from './timeline';

/*
 Beat sheet — 120 BPM, 30 fps (1 beat = 15 frames, 1 compasso = 60 frames). Seções em src/timeline.ts.
   0     Abertura ("Onze formatos…")
   60    F1 LED — teaser de hipótese (cartões em 60/120/180/240; converge 282–299)
   300   F2 flat — explicador de pesquisa
   525   F3 colagem — diário de campo (rasgo 780–800 revela a F4 por baixo)
   780   F4 linha do tempo (selo em +165; mergulho no selo +200–240)
   1020  F5 jornada do experimento (pousos +24/+72/+120/+168; recuo +180–205)
   1260  F6 demo de protótipo (clique +48; ✓ +100; cartão +118; expande +204)
   1500  F7 data story (barras +30; destaque vira linha +200–232)
   1740  F8 paper explicado (estilo 03; contorno vira quadro 16:9 +206–240)
   1980  F9 entrevista editorial (clipe inteiro de 41,3 s a partir de +15; íris fecha no fim)
   3270  F10 visão de futuro (3D; laranja inunda +214–240)
   3510  F11 anúncio (palavras em +6/+66/+126; recolhe +196–236)
   3750  Fechamento (pergunta +14; logos +44/+52)
*/
export const DURATION = T.end;

export const HubFormatos: React.FC = () => {
	const f = useCurrentFrame();
	return (
		<AbsoluteFill style={{background: C.stage}}>
			{f < T.led && <Intro />}
			{f >= T.led && f < T.flat && <Led />}
			{f >= T.flat && f < T.collage && <Flat />}
			<Sequence from={T.timeline} durationInFrames={SCENE}><Timeline /></Sequence>
			{f >= T.collage && f < TEAR[1] && <Collage />}
			<Sequence from={T.journey} durationInFrames={SCENE}><Journey /></Sequence>
			<Sequence from={T.ui} durationInFrames={SCENE}><UiDemo /></Sequence>
			<Sequence from={T.data} durationInFrames={SCENE}><DataStory /></Sequence>
			<Sequence from={T.paper} durationInFrames={SCENE}><Paper /></Sequence>
			<Sequence from={T.editorial} durationInFrames={T.three - T.editorial}><Editorial /></Sequence>
			<Sequence from={T.three} durationInFrames={SCENE}><Future3D /></Sequence>
			<Sequence from={T.hype} durationInFrames={SCENE}><Hype /></Sequence>
			{f >= T.outro && <Outro from={T.outro} />}
			<Audio src={staticFile('audio/score.wav')} />
		</AbsoluteFill>
	);
};
