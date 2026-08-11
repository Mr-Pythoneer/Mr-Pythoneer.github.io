# Brand

Circular seal. Centre device generated with an image model, ring and
lettering composed deterministically by `seal.py` (Pillow + Georgia Bold),
so the Latin is guaranteed correct and stays crisp at any size.

Motto: **NIL NISI OPTIMUM** — "nothing unless the best."

| File | Use |
|---|---|
| `seal-avatar-*.png` | **The one to upload.** Linework dilated so it survives being shrunk to 40px in GitHub comment threads. |
| `seal-b-*.png` | Same layout, original hairline weight. Better at large sizes, mushy below ~64px. |
| `seal-a-*.png` | No handle on the bottom arc — three stars instead. |

Regenerate with `python3 seal.py`. Gold is `#FFBF00`, matched to the source
artwork; background is pure black so the device composites seamlessly.
