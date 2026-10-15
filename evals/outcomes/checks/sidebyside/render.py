"""Render two launch posts side by side with every factual claim highlighted.

Usage: python3 render.py annotations.json out.html
annotations.json: {"source": "...README text...",
                   "left":  {"title": "...", "subtitle": "...", "segments": [{"text": "...", "label": "invented|supported|plain", "note": "..."}]},
                   "right": {...}}
Segments are the post split in reading order; concatenated, they reproduce the post.
"""
import html
import json
import sys

COL = {"invented": ("#ff6b8b", "rgba(255,107,139,.22)"), "supported": ("#3ee08f", "rgba(62,224,143,.16)"), "plain": ("#d9dbe0", "transparent")}


def render_segments(segs):
    out = []
    for s in segs:
        fg, bg = COL[s["label"]]
        text = html.escape(s["text"]).replace("\n\n", "</p><p>").replace("\n", "<br>")
        if s["label"] == "plain":
            out.append(f"<span>{text}</span>")
        else:
            tip = html.escape(s.get("note", ""))
            out.append(f'<span class="{s["label"]}" title="{tip}" style="background:{bg};box-shadow:inset 0 -2px 0 {fg}">{text}</span>')
    return "<p>" + "".join(out) + "</p>"


def column(side):
    segs = side["segments"]
    inv = sum(1 for s in segs if s["label"] == "invented")
    sup = sum(1 for s in segs if s["label"] == "supported")
    return f"""<section>
  <h2>{html.escape(side['title'])}</h2>
  <div class="sub">{html.escape(side['subtitle'])}</div>
  <div class="counts"><span class="pill red">{inv} invented</span><span class="pill green">{sup} from the README</span></div>
  <article>{render_segments(segs)}</article>
</section>"""


def main():
    data = json.load(open(sys.argv[1]))
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Invented vs. sourced claims</title>
<style>
:root{{--bg:#0a0b0e;--panel:#15181f;--line:#262a33;--text:#f4f3ee;--dim:#8a909b}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px/1.6 -apple-system,"Inter",system-ui,sans-serif;padding:40px 48px}}
h1{{font-size:34px;margin:0 0 6px;letter-spacing:-.01em}} .lede{{color:var(--dim);margin:0 0 22px;max-width:1200px}}
.src{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 18px;font:14px/1.5 ui-monospace,Menlo,monospace;color:#cfd2d8;margin-bottom:24px;white-space:pre-wrap}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}
section{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px 26px}}
h2{{margin:0;font-size:22px}} .sub{{color:var(--dim);font-size:14px;margin:2px 0 10px}}
.counts{{display:flex;gap:10px;margin-bottom:12px}} .pill{{font:600 13px ui-monospace,Menlo,monospace;padding:4px 10px;border-radius:99px}}
.red{{background:rgba(255,107,139,.18);color:#ff6b8b}} .green{{background:rgba(62,224,143,.15);color:#3ee08f}}
article p{{margin:0 0 12px}} article span{{border-radius:3px}}
.legend{{color:var(--dim);font-size:14px;margin-top:18px}}
</style></head><body>
<h1>Same request, same model: “write the launch blog post for Tidepool v1.0”</h1>
<p class="lede">The only source was a 5-line README (below). Every factual claim in each post is highlighted:
<b style="color:#3ee08f">green</b> = stated in the README, <b style="color:#ff6b8b">red</b> = not in the README (made up).</p>
<div class="src">{html.escape(data['source'])}</div>
<div class="grid">{column(data['left'])}{column(data['right'])}</div>
<p class="legend">Claim labels come from an independent checker that compared each claim with the README; see examples/04-launch-post in github.com/jazzenchen/ambitious.</p>
</body></html>"""
    open(sys.argv[2], "w").write(page)


if __name__ == "__main__":
    main()
