"""Ball Machine Quest v2: level data -> LEVELS.md, levels.csv, progress-tracker.csv, session-log.csv
usage: python3 gen.py <game_dir>

Shot notation
  D-F            depth (S/M/D) + lane (FW/F/C/B/BW) of the Proton circle
  M-F (Top 2)    per-shot spin
  S-FW (S4 Flat) per-shot speed and spin;  D-F (75 Top 1) = per-shot speed in km/h
  M-C (lob)      lob (riser ON for the whole program); (high) = high topspin ball
  S-F [V]        how George plays it: [V] volley, [O] overhead, default groundstroke
  a -> b         fixed order;  RANDOM: a, b   = Order random
Targets: "C" one target | "C / D" odd balls / even balls | "D|D|B" per shot in the list
Machine positions: BC baseline center, BB behind baseline, CL / CR baseline corner (left / right on the app screen),
                   SC service line center, NC net center.   Stands: Off, Mini, Apex.
"""
import csv, os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

POS = {"BC": "Baseline center", "BB": "Behind baseline", "CL": "Baseline corner (left on screen)",
       "CR": "Baseline corner (right on screen)", "SC": "Service line center", "NC": "Net center"}

WORLDS = {
    1: ("Rally Rookie", "Consistency", "Slow balls straight to you. Just keep it in the court."),
    2: ("Rally Builder", "Consistency under pace", "Faster balls, less time, longer rallies."),
    3: ("Deep Zone", "Depth", "Push the ball past the service line. Some levels put the machine behind the baseline for heavier balls."),
    4: ("Fast Feet", "Movement", "Wide and short balls. Recover to the center mark after every shot."),
    5: ("Aim Master", "Direction", "Crosscourt and down the line. The machine moves to a corner for real crosscourt rallies."),
    6: ("Spin Lab", "Handling spin", "Heavy topspin that kicks up and slice that stays low."),
    7: ("Return of Serve", "Returning", "Apex stand: the machine serves. Split step, short swing, and give every return a job."),
    8: ("Net Attack", "Approaching & net", "Approach shots, volleys and overheads. Fast volley levels put the machine on the service line."),
    9: ("Pass & Defend", "Passing & defending", "The machine stands at the net like an opponent. Pass it or lob it."),
    10: ("Match Play", "Patterns & match", "Serve +1, return +1, crosscourt battles and match pace."),
}

# (name, shots, speed, spin, delay_s, target, rule, pos, stand)
L = [
 # ---- World 1: Rally Rookie (consistency, target A) ----
 ("Forehand Start", "M-F", "S1", "Flat", 6, "A", "Forehands only", "BC", "Off"),
 ("Backhand Start", "M-B", "S1", "Flat", 6, "A", "Backhands only", "BC", "Off"),
 ("Backhand Spin-Up", "M-B", "S2", "Top 1", 5, "A", "", "BC", "Off"),
 ("Ping-Pong", "M-F -> M-B", "S1", "Flat", 6, "A", "Alternate forehand / backhand", "BC", "Off"),
 ("Ping-Pong 2", "M-F -> M-B", "S2", "Top 1", 5, "A", "", "BC", "Off"),
 ("Two and One", "M-F -> M-F -> M-B", "S2", "Top 1", 5, "A", "", "BC", "Off"),
 ("First Guess", "RANDOM: M-F, M-B", "S1", "Flat", 6, "A", "Order random: watch the ball leave the machine", "BC", "Off"),
 ("Guess It", "RANDOM: M-F, M-B", "S2", "Top 1", 5, "A", "", "BC", "Off"),
 ("Three-Way Guess", "RANDOM: M-F, M-C, M-B", "S2", "Top 1", 5, "A", "Ball at the body: step away", "BC", "Off"),
 ("BOSS: Rookie Rally", "RANDOM: M-F, M-B, D-F (75 Top 1), D-B (75 Top 1)", "S2", "Top 1", 5, "A", "20 balls", "BC", "Off"),
 # ---- World 2: Rally Builder (consistency under pace) ----
 ("Faster Forehand", "M-F", "S3", "Top 1", 5, "A", "", "BC", "Off"),
 ("Faster Backhand", "M-B", "S3", "Top 1", 5, "A", "", "BC", "Off"),
 ("Body Ball", "M-C", "S3", "Top 1", 5, "A", "Step away, pick forehand or backhand", "BC", "Off"),
 ("Fast Ping-Pong", "M-F -> M-B", "S3", "Top 1", 4.5, "A", "", "BC", "Off"),
 ("Two Backhands", "M-B -> M-B -> M-F", "S3", "Top 1", 4.5, "A", "", "BC", "Off"),
 ("Three Spots", "M-F -> M-C -> M-B", "S3", "Top 1", 4, "A", "", "BC", "Off"),
 ("Fast Guess", "RANDOM: M-F, M-B", "S3", "Top 1", 5, "A", "", "BC", "Off"),
 ("Three-Way Fast", "RANDOM: M-F, M-C, M-B", "S3", "Top 1", 4.5, "A", "", "BC", "Off"),
 ("Speed Step", "RANDOM: M-F, M-B", "S4", "Top 1", 5, "A", "", "BC", "Off"),
 ("BOSS: Rally Builder", "RANDOM: M-F, M-C, M-B, D-F, D-B", "S3", "Top 1", 4.5, "A", "20 balls", "BC", "Off"),
 # ---- World 3: Deep Zone (depth, B / G) ----
 ("Deep Forehand", "M-F", "S2", "Top 1", 5, "B", "Aim high over the net", "BC", "Off"),
 ("Deep Backhand", "M-B", "S2", "Top 1", 5, "B", "", "BC", "Off"),
 ("Heavy Deep Backhand", "D-B", "S3", "Top 2", 5, "B", "Machine behind the baseline: start 1 step back", "BB", "Off"),
 ("Deep Ping-Pong", "M-F -> M-B", "S3", "Top 1", 5, "B", "", "BC", "Off"),
 ("Heavy Ping-Pong", "D-F -> D-B", "S3", "Top 2", 5, "B", "", "BB", "Off"),
 ("Middle Box Rally", "M-F -> M-B", "S3", "Top 1", 5, "G", "", "BC", "Off"),
 ("Deep Guess", "RANDOM: M-F, M-B", "S3", "Top 1", 5, "B", "", "BC", "Off"),
 ("Heavy Guess", "RANDOM: D-F, D-C, D-B", "S3", "Top 2", 5, "B", "", "BB", "Off"),
 ("Middle Box Guess", "RANDOM: M-F, M-B", "S3", "Top 1", 4.5, "G", "", "BC", "Off"),
 ("BOSS: Deep Diver", "RANDOM: M-F, M-B, D-F, D-B", "S3", "Top 2", 4.5, "B", "20 balls", "BB", "Off"),
 # ---- World 4: Fast Feet (movement) ----
 ("Wide Forehand", "M-FW", "S2", "Top 1", 6, "A", "Recover to the center mark after every shot", "BC", "Off"),
 ("Wide Backhand", "M-BW", "S2", "Top 1", 6, "A", "Recover to the center mark", "BC", "Off"),
 ("Short Forehand", "S-F", "S2", "Top 1", 6, "A", "Run in, hit, backpedal to the baseline", "BC", "Off"),
 ("Side to Side", "M-FW -> M-BW", "S2", "Top 1", 6, "A", "Recover to the center mark", "BC", "Off"),
 ("In and Out", "S-B -> D-B", "S2", "Top 1", 6, "A", "Backhand side: run in for the short ball, back for the deep one", "BC", "Off"),
 ("Four Corners", "M-FW -> S-C -> M-BW -> D-C", "S3", "Top 1", 5.5, "A", "Recover to the center mark", "BC", "Off"),
 ("Wide Guess", "RANDOM: M-FW, M-BW", "S3", "Top 1", 5.5, "A", "Recover to the center mark", "BC", "Off"),
 ("Short or Deep", "RANDOM: S-F, S-B, D-F, D-B", "S3", "Top 1", 5.5, "A", "", "BC", "Off"),
 ("Five-Way Run", "RANDOM: M-FW, M-F, M-C, M-B, M-BW", "S3", "Top 1", 5, "B", "Recover to the center mark", "BC", "Off"),
 ("BOSS: Iron Legs", "RANDOM: M-FW, M-BW, S-C, D-F, D-B", "S3", "Top 1", 5, "B", "20 balls. Recover to the center mark", "BC", "Off"),
 # ---- World 5: Aim Master (direction) ----
 ("Forehand Crosscourt", "M-F", "S3", "Top 1", 5, "C", "Machine in the corner: a real crosscourt rally", "CR", "Off"),
 ("Backhand Crosscourt", "M-B", "S3", "Top 1", 5, "C", "Machine in the corner", "CL", "Off"),
 ("Backhand Corner Box", "M-B", "S3", "Top 1", 5, "E", "Machine in the corner", "CL", "Off"),
 ("Crosscourt Ping-Pong", "M-F -> M-B", "S3", "Top 1", 5, "C", "Both sides crosscourt", "BC", "Off"),
 ("Switch It", "M-F", "S3", "Top 1", 5, "C / D", "Odd balls crosscourt, even balls down the line", "BC", "Off"),
 ("Cross and Line", "M-F -> M-B", "S3", "Top 1", 5, "C / D", "Forehand crosscourt, backhand down the line", "BC", "Off"),
 ("Crosscourt Guess", "RANDOM: M-F, M-B", "S3", "Top 1", 5, "C", "Every ball crosscourt", "BC", "Off"),
 ("Line Guess", "RANDOM: M-F, M-B", "S3", "Top 1", 5, "D", "Every ball down the line", "BC", "Off"),
 ("Box Guess", "RANDOM: M-F, M-B", "S3", "Top 1", 5, "E", "Every ball into the crosscourt box", "BC", "Off"),
 ("BOSS: Sniper", "M-F -> M-B", "S3", "Top 2", 4.5, "E / D", "20 balls. Odd balls crosscourt box, even balls down the line", "BC", "Off"),
 # ---- World 6: Spin Lab ----
 ("Topspin Forehand", "M-F", "S3", "Top 2", 5, "A", "Ball kicks up: move back, hit at waist height", "BC", "Off"),
 ("Slice Backhand", "M-B", "S3", "Slice 1", 5, "A", "Ball stays low: bend your knees", "BC", "Off"),
 ("Heavy Backhand", "D-B", "S3", "Top 3", 5, "A", "High bouncer to the backhand: step back or take it early", "BB", "Off"),
 ("Topspin Ping-Pong", "M-F -> M-B", "S3", "Top 2", 5, "B", "", "BC", "Off"),
 ("Slice Ping-Pong", "M-F -> M-B", "S3", "Slice 1", 5, "A", "", "BC", "Off"),
 ("Spin Switch", "M-F (Top 2) -> M-B (Slice 1) -> M-F (Slice 1) -> M-B (Top 2)", "S3", "Mixed (per shot)", 5, "B", "", "BC", "Off"),
 ("Forehand Spin Guess", "RANDOM: M-F (Top 1), M-F (Top 3), M-F (Slice 1)", "S3", "Mixed (per shot)", 5, "B", "Forehands only", "BC", "Off"),
 ("Backhand Spin Guess", "RANDOM: M-B (Top 1), M-B (Top 3), M-B (Slice 1)", "S3", "Mixed (per shot)", 5, "B", "Backhands only", "BC", "Off"),
 ("Full Spin Guess", "RANDOM: M-F (Top 1), M-F (Top 3), M-F (Slice 1), M-B (Top 1), M-B (Top 3), M-B (Slice 1)", "S3", "Mixed (per shot)", 5, "B", "", "BC", "Off"),
 ("BOSS: Spin Doctor", "RANDOM: M-F (Top 3), M-B (Slice 1), D-F (Slice 1), D-B (Top 3), M-C (Top 2)", "S3", "Mixed (per shot)", 5, "B", "20 balls", "BB", "Off"),
 # ---- World 7: Return of Serve (Apex stand) ----
 ("Deuce Body Serve", "S-F", "S2", "Flat", 7, "A", "Stand on the deuce side. Split step as the machine fires", "BC", "Apex"),
 ("Ad Body Serve", "S-B", "S2", "Flat", 7, "A", "Stand on the ad side", "BC", "Apex"),
 ("Ad Wide Serve", "S-BW", "S2", "Flat", 7, "A", "Stand on the ad side. Short swing, block it back", "BC", "Apex"),
 ("Deuce T and Wide", "S-C -> S-FW", "S2", "Flat", 7, "A", "Deuce side", "BC", "Apex"),
 ("Ad T and Wide", "S-C -> S-BW", "S2", "Flat", 7, "A", "Ad side", "BC", "Apex"),
 ("Deuce, Ad, Deuce", "S-F -> S-B", "S3", "Flat", 8, "B", "Switch sides after every return, like a match", "BC", "Apex"),
 ("Read the Deuce Serve", "RANDOM: S-FW, S-F, S-C", "S3", "Flat", 7, "B", "Deuce side", "BC", "Apex"),
 ("Read the Ad Serve", "RANDOM: S-C, S-B, S-BW", "S3", "Flat", 7, "B", "Ad side", "BC", "Apex"),
 ("First or Second Serve", "RANDOM: S-FW (S4 Flat), S-C (S4 Flat), S-F (S2 Top 2)", "S3", "Mixed (per shot)", 7, "C", "Deuce side. Big serve: block crosscourt. Slow serve: step in", "BC", "Apex"),
 ("BOSS: Return +1", "S-F (S3 Flat) -> M-B (S3 Top 1)", "S3", "Mixed (per shot)", 6, "B", "20 balls. Return, recover to the middle, then hit the next ball", "BC", "Apex"),
 # ---- World 8: Net Attack ----
 ("Forehand Volley", "S-F [V]", "S2", "Flat", 6, "A", "Stand 2 m from the net. Catch the ball in the air", "BC", "Off"),
 ("Backhand Volley", "S-B [V]", "S2", "Flat", 6, "A", "Stand 2 m from the net", "BC", "Off"),
 ("Quick Hands", "S-F [V]", "S1", "Flat", 5, "A", "Machine on the service line: less time to react", "SC", "Off"),
 ("Volley Ping-Pong", "S-F [V] -> S-B [V]", "S2", "Flat", 5, "B", "", "BC", "Off"),
 ("Approach + Volley", "S-C -> S-B [V]", "S2", "Top 1", 6, "B|A", "Start at the baseline: approach, then volley", "BC", "Off"),
 ("First Overhead", "M-C (lob) [O]", "S2", "Flat", 8, "A", "Riser on. Point at the ball with your free hand", "BC", "Off"),
 ("Quick Hands Guess", "RANDOM: S-F [V], S-B [V]", "S1", "Flat", 5, "A", "Machine on the service line", "SC", "Off"),
 ("Volley Guess", "RANDOM: S-FW [V], S-F [V], S-B [V], S-BW [V]", "S2", "Flat", 5, "B", "", "BC", "Off"),
 ("Overhead Guess", "RANDOM: M-F (lob) [O], M-C (lob) [O], M-B (lob) [O]", "S2", "Flat", 8, "A", "Riser on. Turn sideways and shuffle", "BC", "Off"),
 ("BOSS: Net Ninja", "S-C -> S-F [V] -> S-B [V]", "S2", "Flat", 6, "B|A|A", "20 balls. Approach, then 2 volleys. Start each pattern at the baseline", "BC", "Off"),
 # ---- World 9: Pass & Defend (machine at the net) ----
 ("Forehand Pass", "D-F", "S1", "Top 1", 5, "D", "Machine at the net is the opponent: pass it down the line", "NC", "Off"),
 ("Backhand Pass", "D-B", "S1", "Top 1", 5, "D", "Pass down the line", "NC", "Off"),
 ("First Lob", "D-C", "S1", "Top 1", 5, "B", "Lob over the machine, land it deep", "NC", "Off"),
 ("Pass Ping-Pong", "D-F -> D-B", "S2", "Top 1", 5, "D", "", "NC", "Off"),
 ("Cross and Line Pass", "D-F -> D-B", "S2", "Top 1", 5, "C / D", "Odd balls crosscourt, even balls down the line", "NC", "Off"),
 ("Pass, Pass, Lob", "D-F -> D-B -> D-C", "S2", "Top 1", 5, "D|D|B", "", "NC", "Off"),
 ("Pass Guess", "RANDOM: D-F, D-B", "S2", "Top 1", 5, "D", "", "NC", "Off"),
 ("Defend!", "RANDOM: D-FW, D-BW", "S3", "Top 2", 5, "B", "Machine back on the baseline. Hit high and deep to get back in the point", "BC", "Off"),
 ("Pass or Lob", "RANDOM: D-F, D-B, D-C", "S2", "Top 1", 5, "D|D|B", "Wide ball: pass. Middle ball: lob", "NC", "Off"),
 ("BOSS: Passing Pro", "RANDOM: D-FW, D-F, D-C, D-B, D-BW", "S2", "Top 1", 4.5, "D|D|B|D|D", "20 balls. Pass the wide balls, lob the middle one", "NC", "Off"),
 # ---- World 10: Match Play ----
 ("Serve +1", "M-F", "S3", "Top 1", 8, "B", "Serve first (any box), then hit the machine's ball deep. Only the machine ball counts", "BC", "Off"),
 ("Serve +1 Attack", "S-C", "S3", "Top 1", 8, "E / F", "Serve, then attack the short ball into either corner box", "BC", "Off"),
 ("Forehand Battle", "RANDOM: M-F, M-FW", "S4", "Top 2", 4.5, "C", "Machine in the corner: crosscourt forehand rally", "CR", "Off"),
 ("Backhand Battle", "RANDOM: M-B, M-BW", "S4", "Top 2", 4.5, "C", "Machine in the corner: crosscourt backhand rally", "CL", "Off"),
 ("Point Builder", "M-F -> S-C -> S-B [V]", "S3", "Top 1", 5, "B|B|A", "Rally, attack the short ball, finish with a volley", "BC", "Off"),
 ("Return +1 Ad", "S-BW (S3 Flat) -> M-F (S3 Top 1)", "S3", "Mixed (per shot)", 6, "B", "Apex stand. Return from the ad side, then the next ball", "BC", "Apex"),
 ("Defend and Turn", "D-FW -> D-BW -> S-C", "S4", "Top 2", 5, "B", "Two defensive balls, then attack the short one", "BC", "Off"),
 ("Match Chaos", "RANDOM: M-FW, M-F, M-C, M-B, M-BW, D-C", "S4", "Top 2", 4.5, "B", "", "BC", "Off"),
 ("Heavy Match", "RANDOM: D-F (Top 3), D-B (Top 3), M-F (Slice 1), M-B (Slice 1)", "S4", "Mixed (per shot)", 5, "B", "", "BB", "Off"),
 ("FINAL BOSS: Champion", "RANDOM: M-FW (Top 1), M-F (Top 2), M-C (80 Slice 1), M-B (Top 3), M-BW (Top 1), D-F (Top 2), D-B (80 Slice 1), S-C (Top 2)", "S4", "Mixed (per shot)", 4.5, "B", "30 balls", "BC", "Off"),
]
assert len(L) == 100, len(L)

# 60 km/h (the app's lowest) cannot carry a flat ball to the middle row from the baseline, so S1 is 65.
SPEED = {"S1": 65, "S2": 70, "S3": 80, "S4": 90}
SPINV = {"Flat": "0", "Top 1": "+500", "Top 2": "+1000", "Top 3": "+2000", "Slice 1": "-500"}


def marks(n, target):
    balls = 30 if n == 100 else (20 if n % 10 == 0 else 10)
    t = target.replace(" ", "").replace("|", "").replace("/", "")
    if any(x in t for x in "EFG"):
        base = (4, 5, 6)
    elif t and set(t) == {"A"}:
        base = (7, 8, 9)
    else:
        base = (6, 7, 8)
    k = balls // 10
    return balls, tuple(b * k for b in base)


import re
# Which side a level trains. Fast track only ever skips two-sided levels (side == "both").
SIDE = {61: "deuce", 62: "ad", 63: "ad", 64: "deuce", 65: "ad", 67: "deuce", 68: "ad", 69: "deuce", 96: "ad"}


def side_of(n, shots):
    if n in SIDE:
        return SIDE[n]
    lanes = set(re.findall(r"[SMD]-(BW|FW|B|F|C)", shots))
    if lanes <= {"F", "FW"}:
        return "FH"
    if lanes <= {"B", "BW"}:
        return "BH"
    return "both"


def check_of(shots, pos, stand, riser):
    """'ok' = inside the machine's reach by the flight model fitted to app readings (tools/reach/).
    'unchecked' = the model can't judge it yet: front-row targets, service-line or net position, Apex stand, riser."""
    if stand != "Off" or riser == "ON" or pos in ("SC", "NC") or re.search(r"\bS-(BW|FW|B|F|C)", shots):
        return "unchecked"
    return "ok"


def stage_of(n, shots, target):
    if n % 10 == 0:
        return "boss"
    if shots.startswith("RANDOM"):
        return "random"
    alt = "/" in target and {p.strip() for p in target.split("/")} != {"E", "F"}
    return "pattern" if ("->" in shots or alt) else "same ball"


# One technique cue per world, from the coach. Edit coach-cues.csv and re-run; cues print on the cards and the map.
CUE_FILE = os.path.join(OUT, "coach-cues.csv")
if not os.path.exists(CUE_FILE):
    with open(CUE_FILE, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["world", "world_name", "focus", "cue"])
        for k, (wn, focus, _) in WORLDS.items():
            w.writerow([k, wn, focus, ""])
CUES = {int(r["world"]): r["cue"].strip() for r in csv.DictReader(open(CUE_FILE))}

rows = []
for i, (name, shots, speed, spin, delay, target, rule, pos, stand) in enumerate(L, 1):
    world = (i - 1) // 10 + 1
    balls, (s1, s2, s3) = marks(i, target)
    riser = "ON" if ("(lob" in shots or "(high" in shots) else "Off"
    rows.append(dict(level=i, world=world, world_name=WORLDS[world][0], name=name, proton_name=f"L{i:03d}",
                     shots=shots, speed=speed, spin=spin, interval=delay, speed_kmh=SPEED[speed],
                     spin_rpm=SPINV.get(spin, "per shot"), target=target, balls=balls,
                     star1=s1, star2=s2, star3=s3, notes=rule, pos=pos, pos_name=POS[pos], stand=stand, riser=riser,
                     side=side_of(i, shots), stage=stage_of(i, shots, target), cue=CUES.get(world, ""),
                     check=check_of(shots, pos, stand, riser)))

md = ["# All 100 Levels", "",
      "See **HOW-TO-PLAY.md** for the court map, target zones and machine positions.", "",
      "- **Save as**: the program name in the Proton app (L001 … L100).",
      "- **Machine**: where to put the Proton and which stand (set in the program's **Setup**).",
      "- **Shots**: `->` play in this order; `RANDOM:` set Order to random. `[V]` volley, `[O]` overhead. `(lob)` = riser on.",
      "- **Target**: `C / D` = odd balls C, even balls D. `D|D|B` = one target per shot, in the order listed.",
      "- **Card**: a picture of the level drawn like the Proton app (all cards are also in `Level-Cards.pdf`).",
      "- **Stage**: worlds 1–9 go from the **same ball**, to fixed **patterns**, to **random** order, then the **boss**. World 10 mixes everything.",
      "- One-sided drills come in forehand / backhand (or deuce / ad) pairs. Fast track never skips a one-sided level.",
      "- **⚠ unchecked**: these settings have not been checked against the app's reach limits yet (front-row targets, service-line and net positions, Apex stand, riser). If the app says *cannot hit target*, change the speed one notch at a time.", ""]
for w in range(1, 11):
    wn, focus, wd = WORLDS[w]
    md += [f"## World {w}: {wn} · {focus}", "", f"_{wd}_", "",
           "| Lvl | Save as | Name | Stage | Machine | Shots | Speed | Spin | Delay (s) | Target | Balls | ★ / ★★ / ★★★ | Notes | Card |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows[(w - 1) * 10: w * 10]:
        mach = r["pos_name"] + ("" if r["stand"] == "Off" else f" · **{r['stand']} stand**") + (" · riser ON" if r["riser"] == "ON" else "")
        nm = "**" + r["name"] + "**" if r["level"] % 10 == 0 else r["name"]
        sp = r["spin"] + ("" if r["spin_rpm"] == "per shot" else f" ({r['spin_rpm']} rpm)")
        md.append(f"| {r['level']} | {r['proton_name']} | {nm} | {r['stage']} | {mach} | {r['shots']} | {r['speed_kmh']} km/h | {sp} | {r['interval']} | {r['target']} | {r['balls']} | {r['star1']} / {r['star2']} / {r['star3']} | {'⚠ unchecked. ' if r['check'] == 'unchecked' else ''}{r['notes']} | [card](level-cards/{r['proton_name']}.png) |")
    md.append("")
open(os.path.join(OUT, "LEVELS.md"), "w").write("\n".join(md))

with open(os.path.join(OUT, "levels.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

with open(os.path.join(OUT, "progress-tracker.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Level", "World", "Name", "Machine", "Target", "Balls", "1 star", "2 stars", "3 stars",
                "Best score", "Best stars", "Attempts", "Date first passed", "Gold (date passed again, first try)", "Saved in Proton app (Y/N)"])
    for r in rows:
        w.writerow([r["level"], r["world"], r["name"], r["pos_name"] + ("" if r["stand"] == "Off" else f" + {r['stand']} stand"),
                    r["target"], r["balls"], r["star1"], r["star2"], r["star3"], "", "", "", "", "", ""])

with open(os.path.join(OUT, "session-log.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Level", "Attempt #", "Balls in target", "Balls played", "Stars", "Best streak", "Badges earned", "Notes (how it felt, what to fix)"])
    w.writerow(["2026-11-29", 1, 1, 8, 10, 2, 5, "First Star", "Example row - delete me"])
print("ok", len(rows))
