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

## Final authorship — 20 Nov 2026, 07:45 WIB session

A second session rewrote `gen_image.py` and `main.py` from scratch
(own code, own wording and layout), rendering the same 48 verified
stories. What changed vs round 1, learned from our own round-1 result:

- Brief bodies now fit fully inside their cards (round 1's third lines
  sat on the card border); headline/body leading tightened and every
  block is asserted to fit at build time.
- The Riyadh tower art no longer crowds its kicker; the tower base was
  shortened and now sits clear of the text.
- Map pins no longer collide: Washington/New York/Miami and
  The Hague/Berlin and Tokyo/Seoul are nudged apart with thin leader
  lines to their true positions.
- Lead panels gained a source microline, filling dead space at the
  bottom of the text column.

Checks: `gen_image.py` run twice, byte-identical `entry.png`
(sha256 `191a6a7515fc6ad35b3fdaacf06ce23e0a9ff6ebb4f8a416644dd34c74c9cca0`,
165,872 bytes, 1024×1024). `main.py` run three times with
`MAKEFUN_OUTPUT_DIR`: identical output bytes. Kit check run on the
exact commit to submit (see check log).
