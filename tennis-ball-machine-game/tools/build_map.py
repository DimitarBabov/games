import sys, csv, json, os
GAME = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
out = [dict(n=int(r["level"]), w=int(r["world"]), name=r["name"], t=r["target"], b=int(r["balls"]),
            s=[int(r["star1"]), int(r["star2"]), int(r["star3"])], pos=r["pos"], stand=r["stand"], notes=r["notes"], side=r["side"], stage=r["stage"], cue=r["cue"])
       for r in csv.DictReader(open(os.path.join(GAME, "levels.csv")))]
html = open(os.path.join(HERE, "map_template.html")).read()
open(os.path.join(GAME, "quest-map.html"), "w").write(html.replace("/*__DATA__*/", json.dumps(out, separators=(",", ":"), ensure_ascii=False).replace("<", "\\u003c")))
print(len(out))
