// Início de cada seção (frames a 30 fps; 1 beat = 15 frames, 1 compasso = 60)
export const T = {
	intro: 0,
	led: 60,
	flat: 300,
	collage: 525,
	timeline: 780, // revelada por baixo do rasgo da colagem (780–800)
	journey: 1020,
	ui: 1260,
	data: 1500,
	paper: 1740,
	editorial: 1980, // clipe inteiro (41,3 s) + entrada/saída: 1290 frames = 86 beats
	three: 3270,
	hype: 3510,
	outro: 3750,
	end: 4110, // fechamento de 12 s (lista de skills)
} as const;

export const SCENE = 240; // 8 s por formato novo
export const EDITORIAL_LEN = T.three - T.editorial;
export const CLIP_IN = 15; // o clipe começa 1 beat depois do início da seção editorial
