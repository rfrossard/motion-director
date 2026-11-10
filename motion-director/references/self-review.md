# Autoavaliação da biblioteca (09/11/2026)

Leia antes de prometer qualidade. Atualize ao fim de cada vídeo grande: o que falhou, o que a régua não pegou, o que mudou.

## Notas da biblioteca (1–5)
| área | nota | por quê |
|---|---|---|
| cobertura de estilos | 4,5 | 27 estilos com código testado, de pixel a Blender, mais 9 de reserva |
| qualidade das cenas de ouro | 4 | 25 de 27 estilos ≥ 4 depois de 3 rodadas de refação; `broll` e `pixel` ainda abaixo |
| processo (portão) | 4 | régua, regras duras e auditoria automática; ainda depende de notas dadas pelo modelo |
| auditoria | 4 | cenas, passagens e movimento; não vê ritmo real (só frames) nem ouve |
| áudio | 2,5 | volume medido e nivelado, mas a trilha sintetizada é básica e o modelo não ouve |
| reutilização | 3,5 | as cenas de ouro estão escritas para o vídeo "Biblioteca"; adaptar exige retrabalho e nova crítica |
| portabilidade | 4 | ferramentas globais em `~/.local/share/motion-director`; o kit roda fora do projeto (testado: frames idênticos) |

## O que deu errado e virou regra
1. **A 1ª versão "funciona", mas é fraca:** 13 de 27 cenas ficaram ≤ 3 contra referências. → Cena de ouro + portão (`quality.md`).
2. **Notas generosas do próprio autor:** cenas aprovadas a 3,5–4 eram 2–3. → Defeitos antes das notas, nota 5 só com "nenhum", revisor independente.
3. **Pessoas desenhadas em SVG ficam amadoras:** palitinho, bonecos de HQ e de anime. → Footage real, Open Peeps ou abstração.
4. **Matemática em fonte mono:** a cena de equações parecia terminal. → MathJax → SVG obrigatório.
5. **Composição rala** (poucas formas num fundo vazio): flat, stroke, journey, demo, broll. → Câmera perto e elementos ≥ 60 % do quadro.
6. **A auditoria de stills não via passagens nem movimento.** A v2 do `audit.py` achou hype → creator e journey → manim com "depois" vazio. → Folhas `trans_` e `motion_` no portão.
7. **Ferramentas presas a uma pasta de projeto.** → Casa global e kit autossuficiente (fontes OFL, scripts, motores).

## Pendências (backlog, em ordem)
1. Refazer as cenas de ouro de `broll` (forma única ocupando o quadro, morph contínuo) e `pixel` (sprite animado, parallax, ação no beat). Ver as fichas.
2. Corrigir as passagens hype → creator e journey → manim no kit (a cena que entra deve começar desenhada).
3. Parametrizar as cenas de ouro: textos e dados por props (hoje estão fixos no componente).
4. Trilha: integrar música licenciada (ou geração paga, com OK) como padrão de entrega final; `score2.py` só para rascunho.
5. Cartão `Invoke`: rótulos auxiliares em 20 px, abaixo do mínimo de 22. Subir no `core.tsx` quando for re-renderizar.
