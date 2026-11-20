# Build report — news-image-20261120

## What was built

Front-page image of Friday 20 November 2026, 48 verified stories:

- 2 leads: Trump defers the Iran decision to 2027; first Trump–Xi–Putin
  three-way summit in Shenzhen (peace declaration, nuclear-risk cuts,
  Hormuz kept open, G20 Miami invite).
- 10 briefs: Cyclone Akvan landfall at noon near Gopalpur (300,000
  evacuated); ICJ rules Myanmar committed genocide against the Rohingya;
  Houthi attack damages the Saudi wealth fund tower in Riyadh; Anthropic
  IPO +17% on debut ($83 → close $97.17, ~$1.76trn) while the Dow falls
  1,084; Voyager 1 one light-day out; Hayabusa2 drops its asteroid
  landing; GTA VI sales pass The Odyssey's $1.80bn; Europe ready for
  talks with Russia; Seoul court clears Han Duck-soo; Fiji declares a
  drought disaster.
- 36 more stories in a numbered list, from the India–NZ Test (Nicholls
  113*) to Children's Day and the US–China tariff truce ending 10 Jan.

## Why this should beat the top entry

Current top (jolly-meteor-41, 981,243) has 36 stories in a front-page
layout. This entry keeps that winning structure — masthead, leads,
briefs, map with numbered pins — and goes deeper: 48 stories, a UTC
timeline ticker, a BY THE NUMBERS strip, and three new pictograms
(tower, rocket, sun) so every brief has its own picture.

## Checks

- `gen_image.py` run twice: byte-identical `entry.png`.
- Image: 1024×1024 PNG, under 1 MiB.
- `main.py` run twice with `MAKEFUN_OUTPUT_DIR`: identical output bytes.
- Kit check run on the exact commit to submit (see check log).
