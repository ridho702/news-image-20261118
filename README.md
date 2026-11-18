# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/ridho702/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/ridho702/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Sum up 18 November's world news in one image. Built by an AI agent for make.fun's “Sum up 18 November's world news in one image” bounty, $250 in USDC.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the infographic from scratch (needs Pillow and the Liberation fonts):

```sh
python3 generate_entry.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=pxdmc197&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>

## The image

One 1024×1024 infographic, “Wednesday, 18 November 2026 — The world in one day”,
summarising the day's world news as reported on 18 November 2026:

1. **Lead — U.S. sinks five Iranian tankers as Iran hits back.** Washington says
   it sank five Iranian oil tankers in the Gulf of Oman after Iran's
   Revolutionary Guards twice targeted a U.S. warship; Tehran says it hit
   10 ships near the Strait of Hormuz and fired missiles at a U.S. base
   in Jordan.
2. **Europe — Ukraine hits Kerch Bridge for a second night.** Kyiv strikes the
   bridge to occupied Crimea again; Russia hits Ukrainian bridges in reply.
3. **Gaza — U.N. warns of more cold deaths in Gaza.** Winter sets in for
   1.7 million displaced people; Australia, Canada, Italy and the U.K. urge
   Israel to open aid access as flooding worsens conditions.
4. **Asia-Pacific — North Korea fires missile into the sea.** Pyongyang launches
   a ballistic missile towards the Sea of Japan, hours after U.S.–South
   Korea–Japan drills ended.
5. **Climate — COP31 climate talks enter final stretch.** Negotiators in Antalya
   work through a draft agreement with 144 disputed items ahead of the
   summit's scheduled close on Friday, 20 November.
6. **Russia — 19 dead as Russian military plane crashes.** An An-12 transport
   aircraft goes down in western Siberia, killing all 19 aboard, Russia's
   Defence Ministry says.

Also today: Israel's president asks ex-army chief Gadi Eisenkot to form a
government, bypassing caretaker PM Netanyahu; a 5.3-magnitude earthquake
strikes near Buzau, Romania, with no casualties reported; a cyber-attack
disables supermarket freezers across seven European countries.

The image is drawn programmatically with Pillow (`generate_entry.py`) from
flat vector-style shapes — no photographs, no copied artwork. `main.py`
(stdlib only) copies the committed `entry.png` to the output directory, so
both graded runs write byte-identical output.

## Sources

All stories were first reported on Wednesday 18 November 2026, checked
against same-day reporting from:

- News Trend Today, “Morning Headlines Roundup” (18 November 2026) —
  <http://newstrendtodaypk.blogspot.com/2026/11/morning-headlines-roundup-petrol-cut-by_0736199897.html>
- Nexus Europa, top news 18 Nov 2026 02:00 UTC (citing BBC News, France 24,
  The Guardian, Politico Europe, Bloomberg) —
  <https://nexuseuropa.eu/en/top-news/2026-11-18-0200>
- The Paris Eye, breaking news (18 November 2026) —
  <https://thepariseye.com/breaking-news>
- The Munich Eye, breaking news (18 November 2026) —
  <https://themunicheye.com/breaking-news>
- Daily Baku, world news (18 November 2026) —
  <https://dailybaku.az/en/category/dunya>
- Jagran Josh, school assembly news headlines (18 November 2026) —
  <https://www.jagranjosh.com/lite/news/school-assembly-news-headlines-november-18-2026-top-national-world-education-business-news-189094>

## Files

- `entry.png` — the submitted infographic (1024×1024 PNG, under 1 MiB)
- `generate_entry.py` — the Pillow script that draws `entry.png`
- `main.py` — the entry point: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
- `LICENSE` — MIT
