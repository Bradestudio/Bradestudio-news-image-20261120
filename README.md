# Bradestudio-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Bradestudio/Bradestudio-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Bradestudio/Bradestudio-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One 1024×1024 picture that sums up Friday 20 November 2026 in world news: 48 verified stories from six continents, led by the first Trump–Xi–Putin three-way summit and a deferred Iran decision, plus the day's key numbers on a world map.

## Run it

```sh
python3 main.py
```

This copies the finished `entry.png` into `./output/entry.png`. It needs no network and writes the same bytes on every run.

## How the image is made

`gen_image.py` draws `entry.png` from scratch with Pillow and DejaVu fonts — a navy masthead carrying the date, a gold UTC timeline, two lead stories, ten illustrated briefs, a BY THE NUMBERS strip, a world map with numbered pins, and a numbered list of 36 further stories. `main.py` is the shipped program: it only copies the finished image to the grader's output folder, using the standard library alone.

## Sources

Every fact was checked against reporting dated 20 November 2026, including Reuters, AP, AFP, BBC, Al Jazeera, NASA, IMD, ICJ, The Hindu and Times of India. The wording is my own and the pictograms are hand-drawn originals.

## License

MIT — see LICENSE.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qjs4e9sj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
