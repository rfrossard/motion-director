# Biblioteca de skills de vídeo (Claude Code)

> **Repositório privado.** Contém logos oficiais do Itaú/Hub/ICTi (`motion-director/assets/kit-src/brand-parts.json`), dados de exemplo derivados de reportagem da TV Globo (`motion-director/assets/kit2/src/b/words.json`) e um skill de terceiro sem licença de redistribuição (`paper-collage-film`). **Não torne público** sem removê-los.

Instalado em `~/.claude/skills`, fica disponível ao Claude Code em qualquer pasta.

## Skills
| skill | o que faz | origem |
|---|---|---|
| `motion-director` | **master**: escolhe o estilo de cada trecho entre 27, coordena os skills de estilo, aplica contratos (beat, passagens, legendas, áudio) e o **portão de qualidade**; kits Remotion testados | próprio |
| `flat-science-explainer` | explicadores flat científicos (Kurzgesagt-like) | próprio |
| `editorial-archival-edit` | edição editorial de arquivo P&B sobre vídeo real | próprio (estilo de @kaye_creatives) |
| `explainer-default` · `explainer-engaging` · `explainer-high-energy` | demo calmo · jornada em take único · anúncio no beat | Barty-Bart/motion-graphics (MIT) |
| `motion-broll` | B-roll em forma única cronometrado pela fala | Barty-Bart/motion-graphics (MIT) |
| `object-separation` | recorte de pessoa/objeto com SAM 2 local | Barty-Bart/motion-graphics (MIT) |
| `sound-effects` | passe de som medido (biblioteca CC0) | Barty-Bart/motion-graphics (MIT) |
| `paper-collage-film` | filme de colagem de papel rasgado | @kaye_creatives (uso pessoal, não redistribuir) |

Cada skill de terceiro tem `PROVENANCE.md` com origem, licença e modificações locais. Todos receberam ao fim do `SKILL.md` uma seção "Portão de qualidade" que aponta para o `motion-director`.

## Instalar numa máquina
```bash
git clone https://github.com/rfrossard/motion-director.git ~/.claude/skills
```
Ferramentas pesadas (fora do repositório) em `~/.local/share/motion-director`: ambiente micromamba com Manim + ffmpeg completo, whisper.cpp e fontes.
Instruções: `motion-director/assets/kit2/KIT2.md`, seção "Instalar o ambiente". Os kits Remotion instalam as dependências com `npm install` em cada projeto.

## Qualidade
- `motion-director/references/quality.md`: portão obrigatório (cena de ouro por estilo, crítica com notas ≥ 4, regras duras, auditoria do MP4 com `scripts/audit.py`).
- `motion-director/references/self-review.md`: autoavaliação e pendências.

## Atualizar
Depois de mudar um skill: `git -C ~/.claude/skills add -A && git -C ~/.claude/skills commit -m "..." && git -C ~/.claude/skills push`.
