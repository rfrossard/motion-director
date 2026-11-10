import React from 'react';
import {Composition} from 'remotion';
import {DURATION, HubFormatos} from './HubFormatos';
import {FPS} from './lib';
import './fonts';

export const Root: React.FC = () => (
	<Composition id="HubFormatos" component={HubFormatos} durationInFrames={DURATION} fps={FPS} width={1920} height={1080} />
);
