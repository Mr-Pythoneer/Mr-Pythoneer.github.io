# Brand

Circular seal. The centre device was generated with an image model; the rings,
lettering and sparkles are composed deterministically by `seal.py`
(Pillow + Georgia Bold), so the Latin is guaranteed correct and the type stays
crisp at every size.

Layout follows the traditional pattern — Latin motto on the top arc, the same
line in English on the bottom, handle small on the inner curve:

- **NIL NISI OPTIMUM** — "nothing unless the best"
- **ONLY THE BEST**
- **MR-PYTHONEER**

| File | Use |
|---|---|
| `seal-1024.png` | **Upload this one** as the GitHub avatar. |
| `seal-2048.png` | Master. |
| `seal-460/128/64/40.png` | Size checks. |

The source linework is dilated before compositing (`dilate=7`): the hairline
sunburst rays otherwise vanish completely when the seal is shrunk to the 40px
GitHub renders in comment threads, leaving an unreadable smudge. The side
effect is a glow around the crystal at full size, which is deliberate.

Regenerate with `python3 seal.py`. Gold is `#FFBF00`, sampled from the source
artwork; background is pure black so the device composites seamlessly.
