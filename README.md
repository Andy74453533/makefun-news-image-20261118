[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Andy74453533/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Andy74453533/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Built for the [make.fun bounty: Sum up 18 November's world news in one image](https://make.fun/bounty/news-image-20261118).

# The World Today — 18 November 2026

Entry for `news-image-20261118`: a program that writes one 1024×1024 PNG
summarising the world's news of Wednesday 18 November 2026 to
`/output/entry.png`. Standard library plus Pillow for rendering (with a
pre-rendered fallback), offline, deterministic — two runs write
byte-identical files.

## The image

A newspaper front page, "THE WORLD TODAY", dated Wednesday, 18 November
2026. Everything is drawn programmatically — no downloaded photos, no
network at run time:

- **Lead story — Summit in Shenzhen:** Xi Jinping and Vladimir Putin meet
  a day before the first-ever three-way summit with Donald Trump; APEC
  opens, the Quad meets in Manila. Illustrated with the three flags
  (China, Russia, United States) drawn from code.
- **Iran strikes U.S. bases in Kuwait and Bahrain** — Tehran answers the
  U.S. strike on Qeshm Island; Houthi drones hit a Saudi pipeline.
- **Ukraine strike partly collapses the Crimea bridge** — drones injure
  six in Dnipro.
- **Democrats take the U.S. Senate, 56–44** — Peltola wins Alaska.
- **Nvidia beats forecasts: revenue $115.8bn** — sales up 103% in the
  first report since Jensen Huang's exit.
- **Also:** U.S. loses measles-free status; Ebola grips children in DRC;
  cold grips Gaza's displaced. Plus a markets strip (S&P 500 −1.03%,
  Nasdaq −0.74%, Brent $91.55, gold $3,775, VIX 25.46).

Story selection: the five most widely reported developments of the day
across the major briefings (see SOURCES.md), chosen to be recognisable
to a picture editor judging the image on its own — each story is
self-contained, with a headline and a one-line summary, so the image
needs no news feed to be understood.

## How to run

```sh
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # or any output directory
```

- `main.py` renders the page with Pillow from the fixed story data in
  the file, using the embedded DejaVu fonts in `assets/fonts/`.
- If Pillow is unavailable, it copies the pre-rendered
  `assets/entry.png` instead, so the output is identical either way.
- No network access, no randomness, no clock: the output is a fixed
  1024×1024 PNG (124,251 bytes, well under the 1 MiB limit).

## Layout

```
main.py                  program (render + fallback copy)
assets/entry.png         pre-rendered image (fallback + reference)
assets/fonts/            DejaVu Sans / Sans Bold / Serif Bold (embedded)
entry.png                test render of the program's output
SOURCES.md               news sources for the stories shown
LICENSE                  MIT
```

## License

MIT — see LICENSE.
