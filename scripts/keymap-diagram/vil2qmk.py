#!/usr/bin/env python3
"""Convert a Vial .vil export into the QMK keymap.json that keymap-drawer reads.

keymap-drawer only parses QMK keymap.json or ZMK devicetree, and a .vil is
neither. Vial stores [layer][matrix_row][matrix_col] with -1 for holes in the
matrix; QMK wants one flat list per layer in physical order. Two wrinkles make
this more than a flatten:

  * rows 0-3 are the left half and 4-7 the right, and the right half is wired
    outer-to-inner, so its rows read backwards relative to the desk.
  * rows 2 and 5 carry a 7th entry that is the encoder push, not a key. The
    physical layout in cornix_lp.json has no slot for those, so they are cut.

    ./vil2qmk.py ~/Desktop/cornix_lp_v1.vil cornix.json
"""
import argparse
import json
import sys

ENCODER_ROWS = {2, 5}
ENCODER_COL = 6
HALF_ROWS = 4
DEAD = ("KC_NO", "KC_TRNS")


def row_keys(layer, r):
    return [k for c, k in enumerate(layer[r])
            if k != -1 and not (r in ENCODER_ROWS and c == ENCODER_COL)]


def flatten(layer):
    out = []
    for r in range(HALF_ROWS):
        out += row_keys(layer, r)
        out += list(reversed(row_keys(layer, r + HALF_ROWS)))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vil", help="the .vil exported from Vial")
    ap.add_argument("out", help="where to write the QMK keymap.json")
    ap.add_argument("--keyboard", default="cornix_lp")
    args = ap.parse_args()

    vil = json.loads(open(args.vil, encoding="utf-8").read())
    layers = [flatten(l) for l in vil["layout"]]

    # Vial always pads to 10 layers; carry over only the ones with keys on them.
    used = [i for i, l in enumerate(layers) if any(k not in DEAD for k in l)]
    widths = {len(layers[i]) for i in used}
    if len(widths) != 1:
        sys.exit(f"vil2qmk: layers disagree on key count: {sorted(widths)}")

    json.dump({"keyboard": args.keyboard, "keymap": args.keyboard,
               "layout": "LAYOUT", "layers": [layers[i] for i in used]},
              open(args.out, "w", encoding="utf-8"), indent=1)

    combos = [c for c in vil.get("combo", []) if any(x not in ("KC_NO", "") for x in c)]
    print(f"{len(used)} layers ({', '.join(map(str, used))}), "
          f"{len(layers[used[0]])} keys each -> {args.out}", file=sys.stderr)
    for c in combos:
        print(f"  combo: {' + '.join(x for x in c[:4] if x != 'KC_NO')} -> {c[4]}",
              file=sys.stderr)
    print("\nnext:\n"
          f"  uvx --from keymap-drawer keymap parse -q {args.out} > keymap.yaml\n"
          "  uvx --from keymap-drawer keymap draw keymap.yaml \\\n"
          "      -j scripts/keymap-diagram/cornix_lp.json > out.svg", file=sys.stderr)


if __name__ == "__main__":
    main()
