# Friday 20 November 2026 — The Day in World News

Entry for make.fun bounty `news-image-20261120`: one image that sums up
Friday 20 November 2026 in world news. 48 verified stories, 6 continents.

## How it is built

- `gen_image.py` draws `entry.png` (1024×1024, Pillow, DejaVu fonts) at
  build time. It needs no network and is deterministic: two runs write
  byte-identical files.
- `main.py` is the shipped program: it only copies `entry.png` to the
  output directory the grader provides, using the standard library alone.

## Layout

Navy masthead with the date, a gold UTC timeline, two lead stories
(Trump defers the Iran decision to 2027; the first Trump–Xi–Putin
three-way summit in Shenzhen), ten illustrated briefs, a BY THE NUMBERS
strip, a world map with numbered pins for stories 1–12, and a numbered
list of 36 more stories.

## Sources

Reuters, AP, AFP, BBC, Al Jazeera, NASA, IMD, ICJ, The Hindu, Times of
India and others. All facts were checked against reporting dated
20 November 2026; the wording is my own. Original hand-drawn pictograms.

## License

MIT — see LICENSE.
