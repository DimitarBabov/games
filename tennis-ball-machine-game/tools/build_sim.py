import sys, csv, json, os
GAME = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "render.py")).read()
src = src[:src.index("# ---------- card")]
sys.argv = ["x", GAME]
ns = {}; exec(src, ns)
out = []
for r in csv.DictReader(open(os.path.join(GAME, "levels.csv"))):
    rnd, shots = ns["parse"](r)
    js = [dict(d=s["depth"], l=s["lane"], kmh=s["speed"], rpm=ns["SPIN"][s["spin"]], delay=s["interval"],
               riser=s["riser"], hit=s["hit"]) for s in shots]
    out.append(dict(n=int(r["level"]), world=int(r["world"]), name=r["name"], save=r["proton_name"], shots=js, random=rnd,
                    target=r["target"], balls=int(r["balls"]), stars=[int(r["star1"]), int(r["star2"]), int(r["star3"])],
                    notes=r["notes"], pos=r["pos"], posName=r["pos_name"], stand=r["stand"], riser=r["riser"] == "ON"))
html = open(os.path.join(HERE, "sim_template.html")).read()
open(os.path.join(GAME, "simulator.html"), "w").write(html.replace("/*__DATA__*/", json.dumps(out, separators=(",", ":"), ensure_ascii=False)))
print(len(out))
