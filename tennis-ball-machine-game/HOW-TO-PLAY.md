# Ball Machine Quest: How to Play

A 100-level tennis game for the Proton ball machine. There are **10 worlds with 10 levels each**, and every 10th level is a **BOSS**. George earns stars for balls that land in a target, unlocks levels and collects badges on the way to the **Champion** level (100).

| File | What it's for |
|---|---|
| `HOW-TO-PLAY.md` | This file: rules, court map, machine positions, scoring |
| `LEVELS.md` | All 100 levels with the Proton settings |
| `level-cards/` + `Level-Cards.pdf` | A picture card for every level, drawn like the Proton app |
| `quest-map.html` | George's game map: stars, gold levels, badges, unlocks |
| `simulator.html` | Animated simulator of every level |
| `coach-intro.html` | Two-minute intro for the coach |
| `coach-cues.csv` | One technique cue per world, from the coach (prints on the cards and the map) |
| `levels.csv` | The levels as a spreadsheet (handy while programming the machine) |
| `progress-tracker.csv` | One row per level: best score, stars, date passed |
| `session-log.csv` | One row per attempt: the practice diary |

---

## 1. How the game is built (and why)

**The worlds follow the order coaches use with juniors** and cover four of the five game situations: rallying, returning, net play and passing. The fifth, George's own serve, isn't in the game yet (he serves only in levels 91–92, and it isn't scored).

| World | Levels | Name | Focus |
|---|---|---|---|
| 1 | 1–10 | Rally Rookie | Consistency |
| 2 | 11–20 | Rally Builder | Consistency under pace |
| 3 | 21–30 | Deep Zone | Depth |
| 4 | 31–40 | Fast Feet | Movement and recovery |
| 5 | 41–50 | Aim Master | Direction (machine in the corners) |
| 6 | 51–60 | Spin Lab | Handling topspin and slice |
| 7 | 61–70 | Return of Serve | Returning (**Apex stand**) |
| 8 | 71–80 | Net Attack | Approach, volleys, overheads (machine on the service line for fast volleys) |
| 9 | 81–90 | Pass & Defend | Passing shots and lobs (machine at the net as the opponent) |
| 10 | 91–100 | Match Play | Serve +1, return +1, crosscourt battles, match pace |

**Worlds 1–9 have the same inside structure** (World 10 mixes everything, and level 76 is a same-ball overhead):

| Levels in a world | Stage | Why |
|---|---|---|
| 1–3 | **Same ball** every time | Builds the stroke |
| 4–6 | **Fixed pattern** (e.g. forehand, backhand) | Adds footwork and rhythm |
| 7–9 | **Random order** | Harder in practice, but carries over to matches |
| 10 | **Boss**: 20 balls, mixed | The test that opens the next world |

One-sided drills come in pairs: forehand then backhand, or deuce side then ad side. Where there's room for only one extra same-ball level (heavy topspin, the corner box, the wide serve), the backhand or ad side gets it, because that's usually the weaker side.

What this is based on:
- **Blocked first, random later.** One older, small tennis study found 8–9-year-olds learned forehands best from repeating the same ball, while 10–12-year-olds gained more from random practice (Farrow & Maschette). George is 10, so each world starts blocked and ends random.
- **Priorities for juniors:** consistency first, then depth, then direction, then spin and power (USPTA and coaching sources).
- **Five game situations:** junior tactics are taught around serving, returning, rallying, approaching and passing (Louis Cayer, ITF/Tennis Canada). The game covers four of them; serving is missing.
- **Serve +1 and return +1:** a study of elite juniors found these shots get the least practice time (13% and 18% of training). Worlds 7 and 10 include them.
- **Right difficulty:** practice works best when it's hard but doable (Challenge Point Framework). We pass a level at about 7 of 10 and adjust with the fast-track and drop-back rules below. The 7 of 10 mark is our own choice, not a number from research.
- **Targets, choices and success:** aiming at a target outside the body (external focus), letting the child choose some of the practice, and building on success all help kids learn (Wulf's OPTIMAL theory). The evidence for children is promising but still limited.
- **Did it stick?** How well someone does during practice is a poor guide to what they keep (Soderstrom & Bjork). Ten balls is also a small sample, so one pass can be luck. That's why a level only turns **gold** when he passes it again on a later day.

**What this game doesn't do**
- **A machine isn't an opponent.** The timing is fixed and there's no body to read. One small study found players time their return differently against a machine than against a real server (Carboch et al.). World 7 trains the return stroke, not reading a serve.
- **It checks where the ball lands, not how he hits it.** Technique belongs to his coach (see "Technique beats score" below).
- So this is extra practice next to lessons and real points, not a replacement for them.

---

## 2. The court map

The cards show the court **the same way the Proton app does**: machine at the bottom, George at the top.

### Shot spots (George's side): the 15 circles in the app

```
                 ======== NET ========
  S  front row   o    o    o    o    o     (just over the net)
  M  middle row  o    o    o    o    o
  D  back row    o    o    o    o    o     (near his baseline)
                 FW   F    C    B    BW    <- from the left of the app screen
```
- **D** = back row (top row of circles), **M** = middle row, **S** = front row (just over the net).
- The app view is from behind the machine, so the **left of the screen is a right-hander's forehand side**: FW = wide forehand, F = forehand, C = center, B = backhand, BW = wide backhand.
- On **Apex stand** levels the front row is where the serve lands: S-FW wide, S-F body, S-C T (deuce side); S-C T, S-B body, S-BW wide (ad side).
- `->` = Order in order. `RANDOM:` = Order random. `[V]` = volley it, `[O]` = overhead. `(lob)` = riser on.

### Target zones (machine's side): where his ball must land

| Target | Name | The ball counts if it lands... |
|---|---|---|
| **A** | Whole court | anywhere in the singles court |
| **B** | Deep zone | past the service line |
| **C** | Crosscourt | in the diagonal half of the court |
| **D** | Down the line | in the straight-ahead half of the court |
| **E** | Crosscourt box | in the diagonal corner box (3 m × 3 m, cones) |
| **F** | Down-the-line box | in the straight-ahead corner box |
| **G** | Middle box | in a 3 m wide box in the middle of zone B |

- `C / D`: odd-numbered balls go to C, even-numbered to D.
- `D|D|B`: one target per shot, in the order the shots are listed (e.g. pass, pass, lob).
- You need about **8–12 cones** or throw-down lines.

---

## 3. Machine positions and stands

Set these in each program's **Setup** (Machine Config) in the Proton app. The card shows them in the blue **MACHINE** strip.

| Position | Used for |
|---|---|
| **Baseline center** | Most levels |
| **Behind baseline** | Heavier, deeper balls (Deep Zone, Spin Lab, Heavy Match) |
| **Baseline corner** (left or right on screen) | Real crosscourt rallies (Aim Master, forehand and backhand battles) |
| **Service line center** | Fast volleys, less time to react |
| **Net center** | The machine is the net player: passing shots and lobs |

| Stand | Used for |
|---|---|
| **Stand Off** | Everything except returns |
| **Apex stand** | Return of Serve (World 7) and Return +1 (level 96) |

**Riser** is on only for overhead levels.

**Safety:** when the machine is at the service line or the net, George's shots come back toward it. The machine can take a hit, but nobody should stand next to it while he hits.

**Left-handed?** Tap **Mirror**. On corner levels, also put the machine in the other corner.

---

## 4. Machine settings

### Speed

| Step | Proton app speed |
|---|---|
| **S1** | 60 km/h (lowest) |
| **S2** | 70 km/h |
| **S3** | 80 km/h |
| **S4** | 90 km/h |

Shots closer to him (service line, net) feel much faster at the same km/h, so those levels use S1–S2. A shot written `S-FW (S4 Flat)` has its own speed and spin.

### Spin

| Name | Proton app spin |
|---|---|
| **Flat** | 0 rpm |
| **Top 1 / Top 2 / Top 3** | +500 / +1000 / +2000 rpm topspin |
| **Slice 1** | −500 rpm backspin |

### Delay

Seconds before each ball, the same as the app's Delay slider. Return levels use 7–8 s so he can reset between serves. Serve +1 levels use 8 s so he has time to serve first.

### Programming the machine

1. **Programs → Custom →** new program named like the card (`L007`).
2. **Setup:** machine position and stand from the MACHINE strip. Riser if the card says ON.
3. For each shot: **Add New Shot**, tap the circle on the card, set **Spin**, **Speed**, **Delay**, **Save Shot**.
4. Set **Loops** and **Order** from the card.

Program **one world at a time**.

---

## 5. Playing a level

1. Put out cones for the target. Set the machine position.
2. Run the program. **10 balls** (boss 20, final boss 30). The card says when to stop the machine early.
3. A parent counts balls that land **in the target on the first bounce**. Lines are in. Volleys must be hit before the bounce. On "recover" levels he must get back to the center mark before the next ball, or the shot is out.

### Technique beats score

- **Only real swings count.** A ball that's poked or pushed over just to get it in is out, even if it lands in the target. On volleys, a real swing means a firm punch.
- If he keeps poking, stop and start the level again. The stopped attempt doesn't count as a try.
- **Dad keeps score, the coach coaches.** Don't correct his technique during a level. Remind him of the coach's one cue for that world before he starts, and film 10 seconds now and then to show the coach.
- **Coach cues:** `coach-cues.csv` has one line per world for the coach's cue. Once it's filled in and the files are rebuilt (`tools/`), the cue prints on that world's cards and shows on the map.

### Stars

| Target | Balls | ★ | ★★ | ★★★ |
|---|---|---|---|---|
| Whole court (A) | 10 | 7 | 8 | 9+ |
| Half court or deep (B, C, D, and mixed targets) | 10 | 6 | 7 | 8+ |
| Small boxes (E, F, G) | 10 | 4 | 5 | 6+ |
| BOSS / FINAL BOSS | 20 / 30 | ×2 | ×2 | ×3 |

### Unlocking and adjusting difficulty

- **1 star passes a level** and unlocks the next one.
- **Fast track:** ★★★ on the first try lets him skip the next level, but only a two-sided one. Forehand-only, backhand-only, deuce-side and ad-side levels can never be skipped, and neither can the boss. So acing the forehand never skips the backhand.
- **Gold:** a level turns gold when he passes it again on a **later day**, on his **first try** that day. One pass shows he could do it once; gold shows it stuck. The map's 🥇 button picks one gold try for each session.
- **Drop back:** 3 tries max per level per session. After three misses, play the level before it once and try again another day.
- A **BOSS** unlocks with **15 stars** from levels 1–9 of that world. Beating it opens the next world.
- **His choice:** once per session he picks any unlocked level to play.

---

## 6. Badges

| Badge | How to earn it |
|---|---|
| ⭐ **First Star** | first star |
| 💯 **Perfect** | every ball in on any level |
| 🔥 **Hot Streak** | 7 in a row in the target |
| 💪 **Comeback Kid** | pass a level after failing it twice |
| 👑 **Boss Slayer** | beat a BOSS (10 to collect) |
| 🌟 **Three-Star World** | 3 stars on every level of one world |
| 🦵 **Iron Legs** | beat World 4 |
| 🎯 **Sniper** | 3 stars on any box level (E, F, G) |
| 🌀 **Spin Doctor** | beat World 6 |
| 🧱 **The Wall** | beat World 7 (Return of Serve) |
| 🥷 **Net Ninja** | beat World 8 |
| 🏹 **Passing Pro** | beat World 9 |
| 🥇 **Solid Gold** | turn 10 levels gold |
| 📅 **Iron Habit** | 3 sessions in one week |
| 🏆 **Champion** | beat level 100 |

### Rewards (agree on these with him first)

300 stars in total: for example 25 stars dinner choice, 50 new overgrip, 100 match trip, 150 weekend choice, 200 new shoes, 300 a camp or a new racket.

---

## 7. A good session (45–60 minutes)

1. **Warm-up (10 min):** jog, shuffles, arm circles, 20 easy balls with no scoring.
2. **Go for gold (10 min):** one level he passed on an earlier day. Only his first try counts for gold (the map's 🥇 button picks the level).
3. **New levels (20–30 min):** 2–4 levels, water between them.
4. **His choice (5 min):** any unlocked level.
5. **Write it down** in `session-log.csv` and `progress-tracker.csv`.

About **150–250 balls** per session, **2–3 sessions a week**. Stop if anything hurts. Overhead and return levels need a good shoulder and arm warm-up.

---

## Sources

- Farrow & Maschette (1997), via [PMC review on contextual interference in youth tennis](https://pmc.ncbi.nlm.nih.gov/articles/PMC5676081)
- [Singles tactics, Louis Cayer (Tennis Canada / ITF)](https://assets.tenniscanada.com/production/TPA/Resources/Singles-tactics-by-Louis-Cayer-2005.pdf)
- [USPTA: Six General Performance Components](https://www.uspta.com/Backup/Education/Resources/Six_General_Performance_Components.aspx)
- [ITF Coaching & Sport Science Review (third and fourth shot practice)](https://itfcoachingreview.com/index.php/journal/article/download/567/1573/2428)
- [Soderstrom & Bjork (2015), learning versus performance](https://pubmed.ncbi.nlm.nih.gov/25910388/)
- [Carboch et al. (2014), ball machine versus real server](https://pmc.ncbi.nlm.nih.gov/articles/PMC3990883)
- [Challenge Point Framework](https://en.wikipedia.org/wiki/Challenge_point_framework)
- [OPTIMAL theory in children, Scientific Reports 2024](https://link.springer.com/article/10.1038/s41598-024-63387-z)
- [ITF Tennis Play and Stay](https://www.itftennis.com/en/growing-the-game/itf-tennis-play-and-stay/)
