"""Junta os tokens do whisper.cpp (work/transcript.json) em palavras com tempos: work/words.json = [[palavra, início_s, fim_s], ...]"""
import json
d = json.load(open('work/transcript.json'))
words = []
for seg in d['transcription']:
    for tk in seg['tokens']:
        tx = tk['text']
        if tx.startswith('[') and tx.endswith(']'):
            continue
        s, e = tk['offsets']['from'] / 1000, tk['offsets']['to'] / 1000
        if tx.startswith(' ') or not words:
            words.append([tx.strip(), s, e])
        else:
            words[-1][0] += tx; words[-1][2] = e
json.dump([w for w in words if w[0]], open('work/words.json', 'w'), ensure_ascii=False)
