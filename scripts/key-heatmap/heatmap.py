#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

FINGER = [0, 1, 2, 3, 3, 4, 4, 5, 6, 7]
INNER_COLUMNS = {4, 5}

SHIFTED = {"<": ",", ">": ".", "?": "/", ":": ";", '"': "'"}

BUCKETS = 10
LIGHT = ["#f6f0e0", "#f0e4c8", "#e8d6ab", "#dec489", "#d2ad63",
         "#c09443", "#a67a2d", "#87601e", "#684713", "#48300c"]
DARK = ["#272521", "#332d20", "#453922", "#5b4926", "#745c2b",
        "#907432", "#ad8f3d", "#c9ab52", "#e0c67c", "#f2e0ae"]
INK_LIGHT = ["#3a3128"] * 6 + ["#faf6ec"] * 4
INK_DARK = ["#b5ad9b"] * 3 + ["#ded5be"] * 3 + ["#2a2416"] * 4

KEY, GAP, SPLIT = 48, 6, 24
PAD_X, PAD_TOP = 26, 24
TITLE_H, GUTTER, LEGEND_H = 28, 26, 50
PITCH = KEY + GAP
BOARD_W = 10 * PITCH - GAP + SPLIT
BOARD_H = TITLE_H + 3 * PITCH - GAP
WIDTH = BOARD_W + 2 * PAD_X


def strip_markdown(md):
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)      # front matter
    md = re.sub(r"```.*?```", " ", md, flags=re.S)             # fenced code
    md = re.sub(r"`[^`]*`", " ", md)                           # inline code
    md = re.sub(r"\{\{[<%].*?[>%]\}\}", " ", md, flags=re.S)   # hugo shortcodes
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", md)              # images
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)           # links -> link text
    md = re.sub(r"^\s*\|.*\|\s*$", " ", md, flags=re.M)        # tables
    md = re.sub(r"<[^>]+>", " ", md)                           # raw html
    md = re.sub(r"https?://\S+", " ", md)
    return md


def load_corpus(root, pattern, excludes):
    paths = sorted(p for p in root.glob(pattern) if p.is_file())
    kept = [p for p in paths if not any(p.match(x) for x in excludes)]
    if not kept:
        sys.exit(f"heatmap: no files matched {pattern!r} under {root}")
    return kept, " ".join(strip_markdown(p.read_text(encoding="utf-8")) for p in kept)


def analyse(rows, text):
    keymap = {ch: (r, c) for r, row in enumerate(rows) for c, ch in enumerate(row)}
    counts = dict.fromkeys(keymap, 0)
    total = same_finger = 0
    previous = None
    for raw in text:
        ch = SHIFTED.get(raw, raw).lower()
        if ch not in keymap:
            previous = None # a space or digit breaks the bigram chain
            continue
        counts[ch] += 1
        total += 1
        here = keymap[ch]
        if previous and FINGER[previous[1]] == FINGER[here[1]] and previous != here:
            same_finger += 1
        previous = here
    if not total:
        sys.exit("heatmap: corpus contains no scorable characters")
    on_row = lambda r: sum(v for k, v in counts.items() if keymap[k][0] == r)
    stretch = sum(v for k, v in counts.items() if keymap[k][1] in INNER_COLUMNS)
    return {
        "counts": counts,
        "total": total,
        "home": on_row(1) / total,
        "stretch": stretch / total,
        "same_finger": same_finger / total,
    }


def validate(key, layout):
    rows = layout.get("rows")
    if not isinstance(rows, list) or len(rows) != 3:
        sys.exit(f"heatmap: layout {key!r} needs exactly 3 rows")
    if any(len(r) != 10 for r in rows):
        sys.exit(f"heatmap: layout {key!r} needs 10 keys per row")
    flat = "".join(rows)
    if len(set(flat)) != len(flat):
        sys.exit(f"heatmap: layout {key!r} repeats a character")


def render_board(board, offset_y, vmax, grand_total):
    pct = lambda n: f"{n / grand_total * 100:.1f}" if n / grand_total * 100 >= 0.05 else "&lt;.1"
    subtitle = (f'home row {board["home"] * 100:.0f}%'
                f'  ·  stretch {board["stretch"] * 100:.0f}%'
                f'  ·  same-finger {board["same_finger"] * 100:.1f}%')
    out = [f'<g transform="translate(0,{offset_y})">',
           f'<text class="bt" x="{PAD_X}" y="13">{board["name"]}</text>',
           f'<text class="bs" x="{PAD_X + BOARD_W}" y="13" text-anchor="end">{subtitle}</text>']
    for r, row in enumerate(board["rows"]):
        for c, ch in enumerate(row):
            x = PAD_X + c * PITCH + (SPLIT if c >= 5 else 0)
            y = r * PITCH + TITLE_H
            n = board["counts"][ch]
            b = min(BUCKETS - 1, int(n / vmax * BUCKETS)) if vmax else 0
            label = "&amp;" if ch == "&" else ("&lt;" if ch == "<" else ch)
            out.append(f'<rect class="k b{b}" x="{x}" y="{y}" '
                       f'width="{KEY}" height="{KEY}" rx="7"/>')
            out.append(f'<text class="kl b{b}" x="{x + KEY / 2}" y="{y + 22}">{label}</text>')
            out.append(f'<text class="kp b{b}" x="{x + KEY / 2}" y="{y + 36}">{pct(n)}</text>')
    out.append("</g>")
    return "\n".join(out)


def render_svg(boards, label):
    height = PAD_TOP + len(boards) * BOARD_H + (len(boards) - 1) * GUTTER + LEGEND_H
    total = boards[0]["total"]
    vmax = max(max(b["counts"].values()) for b in boards)

    groups = "\n".join(
        render_board(b, PAD_TOP + i * (BOARD_H + GUTTER), vmax, total)
        for i, b in enumerate(boards)
    )

    swatch, legend_y = 24, height - 30
    legend = [f'<text class="bs" x="{PAD_X}" y="{legend_y - 6}">share of keypresses</text>']
    legend += [f'<rect class="b{i}" x="{PAD_X + i * swatch}" y="{legend_y}" '
               f'width="{swatch}" height="10" rx="2"/>' for i in range(BUCKETS)]
    legend += [
        f'<text class="lg" x="{PAD_X}" y="{legend_y + 25}">low</text>',
        f'<text class="lg" x="{PAD_X + BUCKETS * swatch}" y="{legend_y + 25}" '
        f'text-anchor="end">high</text>',
        f'<text class="bs" x="{PAD_X + BOARD_W}" y="{legend_y + 25}" text-anchor="end">'
        f'corpus size: {total:,} keypresses {label}</text>',
    ]

    fills = "".join(f".b{i}{{fill:{LIGHT[i]}}}text.b{i}{{fill:{INK_LIGHT[i]}}}"
                    for i in range(BUCKETS))
    dark_fills = "".join(f".b{i}{{fill:{DARK[i]}}}text.b{i}{{fill:{INK_DARK[i]}}}"
                         for i in range(BUCKETS))

    names = ", ".join(b["name"] for b in boards)
    desc = (f"Three-row, ten-column key grids for {names}, each shaded by how often the key "
            f"is pressed over the same body of text. " + " ".join(
                f'On {b["name"]}, {b["home"] * 100:.0f} percent of keypresses land on the home row, '
                f'{b["stretch"] * 100:.0f} percent in the two inner columns that an index finger '
                f'reaches by splaying sideways, and {b["same_finger"] * 100:.1f} percent are '
                f'same-finger bigrams.' for b in boards))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" \
width="{WIDTH}" height="{height}" role="img" aria-labelledby="ttl desc">
<title id="ttl">Keypress heatmap: {names}</title>
<desc id="desc">{desc}</desc>
<style>
  .srf{{fill:#fffdf8}}
  .bt{{font:600 13px/1 ui-serif,Iowan Old Style,Georgia,serif;fill:#2b2520}}
  .bs,.lg{{font:400 10.5px/1 ui-sans-serif,system-ui,sans-serif;fill:#6b6355}}
  .kl{{font:600 14px/1 ui-monospace,SFMono-Regular,Menlo,monospace;text-anchor:middle}}
  .kp{{font:400 8.5px/1 ui-sans-serif,system-ui,sans-serif;text-anchor:middle;opacity:.75}}
  .k{{stroke:#fffdf8;stroke-width:1.5}}
  {fills}
  @media (prefers-color-scheme: dark){{
    .srf{{fill:#141310}}
    .bt{{fill:#e8e1d3}}
    .bs,.lg{{fill:#8f8878}}
    .k{{stroke:#141310}}
    {dark_fills}
  }}
</style>
<rect class="srf" x="0" y="0" width="{WIDTH}" height="{height}" rx="10"/>
{groups}
{"".join(legend)}
</svg>
'''


def main():
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(
        description="Render a keypress heatmap comparing layouts over a Markdown corpus.")
    ap.add_argument("input", type=Path,
                    help="directory to read the corpus from")
    ap.add_argument("-o", "--output", type=Path, default=Path("-"),
                    help="SVG destination, or - for stdout (default: -)")
    ap.add_argument("--layouts", type=Path, default=here / "layouts.json",
                    help="layout definitions (default: layouts.json beside this script)")
    ap.add_argument("--only", metavar="KEY",
                    help="comma-separated layout keys to render, in the order given "
                         "(default: every layout, in file order)")
    ap.add_argument("--glob", default="**/*.md",
                    help="which files to read under INPUT (default: **/*.md)")
    ap.add_argument("--exclude", metavar="PATTERN", action="append", default=[],
                    help="skip files matching this glob; repeatable")
    ap.add_argument("--label", default="(kasader.dev)",
                    help="trailing words for the legend's corpus note")
    ap.add_argument("-q", "--quiet", action="store_true",
                    help="suppress the summary written to stderr")
    args = ap.parse_args()

    if not args.input.is_dir():
        sys.exit(f"heatmap: {args.input} is not a directory")

    definitions = json.loads(args.layouts.read_text(encoding="utf-8"))
    keys = [k.strip() for k in args.only.split(",")] if args.only else list(definitions)
    for key in keys:
        if key not in definitions:
            sys.exit(f"heatmap: unknown layout {key!r}; have {', '.join(definitions)}")
        validate(key, definitions[key])

    files, text = load_corpus(args.input, args.glob, args.exclude)
    boards = [{"name": definitions[k]["name"], "rows": definitions[k]["rows"],
               **analyse(definitions[k]["rows"], text)} for k in keys]

    svg = render_svg(boards, args.label)
    if str(args.output) == "-":
        sys.stdout.write(svg)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(svg, encoding="utf-8")

    if not args.quiet:
        w, h = WIDTH, PAD_TOP + len(boards) * BOARD_H + (len(boards) - 1) * GUTTER + LEGEND_H
        print(f"{len(files)} files, {boards[0]['total']:,} scored keypresses "
              f"-> {args.output} ({w}x{h})", file=sys.stderr)
        print(f"{'':<22}{'home':>8}{'stretch':>9}{'SFB':>8}", file=sys.stderr)
        for b in boards:
            print(f"{b['name']:<22}{b['home']:>7.1%}{b['stretch']:>9.1%}"
                  f"{b['same_finger']:>8.2%}", file=sys.stderr)


if __name__ == "__main__":
    main()
