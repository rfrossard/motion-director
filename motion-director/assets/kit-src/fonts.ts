import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

export const fontsReady = Promise.all([
	loadFont({family: 'Itau Display Pro', url: staticFile('fonts/ItauDisplayPro-Light.ttf'), weight: '300'}),
	loadFont({family: 'Archivo', url: staticFile('fonts/archivo-latin-700-normal.woff2'), weight: '700'}),
	loadFont({family: 'Archivo', url: staticFile('fonts/archivo-latin-800-normal.woff2'), weight: '800'}),
	loadFont({family: 'IBM Plex Mono', url: staticFile('fonts/ibm-plex-mono-latin-400-normal.woff2'), weight: '400'}),
	loadFont({family: 'IBM Plex Mono', url: staticFile('fonts/ibm-plex-mono-latin-500-normal.woff2'), weight: '500'}),
]);
