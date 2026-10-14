"""L:// Tumblr template generator · Instituto Luterano Latinoamericano · CC BY-NC-SA 4.0. 1280x1920 (Tumblr 2:3). Requires: pip install pillow
usage: python3 tumblr_template.py out.png "TITULO" "subtitulo" [tech|teo|ench|sede]
Empty title -> blank template with guide boxes."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
D = os.path.dirname(os.path.abspath(__file__)) + "/"
W, H = 1280, 1920
CREAM = (243, 237, 224); INK = (28, 26, 24); GRID = (200, 192, 176)
COL = {"tech": (242, 196, 0), "teo": (30, 99, 200), "ench": (34, 150, 80), "sede": (28, 26, 24)}
ART = {"tech": "art_ens.webp", "teo": "art_sede.webp", "ench": "art_ench.webp", "sede": "art_sede.webp"}
TAG = {"tech": "🟨 TECNOLOGÍA", "teo": "🟦 TEOLOGÍA", "ench": "🟩 ENCHIRIDION", "sede": "SEDE DE AGENTES"}

for _f in ("Oswald.ttf", "SpaceMono.ttf", "SpaceMono-Bold.ttf"):
    if not os.path.exists(D + _f):
        sys.exit("Falta " + _f + ": descárgala de fonts.google.com (Oswald, Space Mono) y ponla junto a este script.")

def osw(sz, w=700):
    f = ImageFont.truetype(D + "Oswald.ttf", sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
mono = lambda sz, b=False: ImageFont.truetype(D + ("SpaceMono-Bold.ttf" if b else "SpaceMono.ttf"), sz)

def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def make(out, title="", sub="", school="sede"):
    acc = COL[school]
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    for x in range(40, W, 40):
        for y in range(40, H, 40):
            d.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=GRID)
    M = 72
    # blueprint frame + corner ticks
    d.rectangle((M - 24, M - 24, W - M + 24, H - M + 24), outline=INK, width=2)
    for cx, cy in [(M - 24, M - 24), (W - M + 24, M - 24), (M - 24, H - M + 24), (W - M + 24, H - M + 24)]:
        d.line((cx - 18, cy, cx + 18, cy), fill=INK, width=2); d.line((cx, cy - 18, cx, cy + 18), fill=INK, width=2)
        d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), outline=INK, width=2)
    # header: seal + name
    seal = Image.open(D + "L_final.png").convert("L").resize((150, 150), Image.LANCZOS)
    sm = ImageOps.invert(seal).point(lambda v: 255 if v > 140 else (0 if v < 90 else (v - 90) * 5))
    im.paste(Image.new("RGB", seal.size, INK), (M, M), sm)
    d.text((M + 175, M + 22), "L://", font=osw(64), fill=INK)
    d.text((M + 175, M + 104), "INSTITUTO LUTERANO LATINOAMERICANO", font=mono(22, True), fill=INK)
    for i, c in enumerate([COL["tech"], COL["teo"], COL["ench"]]):
        x = W - M - 3 * 38 + i * 38; d.rectangle((x, M + 10, x + 30, M + 40), fill=c)
    d.text((W - M, M + 62), "#OPENCOURSEWARE", font=mono(18), fill=INK, anchor="ra")
    y = M + 190; d.line((M, y, W - M, y), fill=INK, width=2)
    # school tag chip
    tag = TAG[school].replace("🟨 ", "").replace("🟦 ", "").replace("🟩 ", "")
    f = mono(24, True); tw = d.textlength(tag, font=f)
    d.rectangle((M, y + 40, M + 44, y + 84), fill=acc)
    d.text((M + 62, y + 46), tag, font=f, fill=INK)
    d.text((W - M, y + 46), "æ:// >_", font=mono(24, True), fill=INK, anchor="ra")
    # title
    ty = y + 130
    if title:
        tf = osw(150); lines = wrap(d, title.upper(), tf, W - 2 * M)
        if len(lines) > 3: tf = osw(112); lines = wrap(d, title.upper(), tf, W - 2 * M)
        for ln in lines:
            d.text((M, ty), ln, font=tf, fill=INK); ty += int(tf.size * 1.3)
    else:
        for i in range(2):
            d.rectangle((M, ty, W - M, ty + 150), outline=GRID, width=3)
            d.text((M + 20, ty + 55), "TÍTULO · OSWALD BOLD 150" if i == 0 else "SEGUNDA LÍNEA", font=mono(26), fill=GRID); ty += 175
    ty += 10
    if sub:
        sf = mono(32)
        for ln in wrap(d, sub, sf, W - 2 * M):
            d.text((M, ty), ln, font=sf, fill=INK); ty += 48
    else:
        d.rectangle((M, ty, W - M, ty + 100), outline=GRID, width=3)
        d.text((M + 20, ty + 32), "subtítulo · Space Mono 32", font=mono(26), fill=GRID); ty += 100
    # line art (masked to ink / accent)
    art = Image.open(D + ART[school]).convert("RGBA")
    area_top, area_bot = ty + 40, H - M - 230
    s = min((W - 2 * M) / art.width, (area_bot - area_top) / art.height)
    art = art.resize((int(art.width * s), int(art.height * s)), Image.LANCZOS)
    ax = (W - art.width) // 2; ay = area_bot - art.height
    ink = acc if school != "tech" else INK
    im.paste(Image.new("RGB", art.size, ink), (ax, ay), art.split()[3])
    # dimension line under art (industrial detail)
    dy = area_bot + 30
    d.line((ax, dy, ax + art.width, dy), fill=INK, width=2)
    for xx in (ax, ax + art.width): d.line((xx, dy - 12, xx, dy + 12), fill=INK, width=2)
    d.text((W // 2, dy - 34), "el agente propone · tú compruebas · tú decides", font=mono(20), fill=INK, anchor="ma")
    # footer
    fy = H - M - 150; d.line((M, fy, W - M, fy), fill=INK, width=2)
    d.rectangle((M, fy + 28, M + 520, fy + 92), fill=INK)
    d.text((M + 260, fy + 60), "lutheraninstitute.github.io", font=mono(24, True), fill=CREAM, anchor="mm")
    d.text((W - M, fy + 34), "#elearnlatam #aprendelatam", font=mono(22), fill=INK, anchor="ra")
    d.text((W - M, fy + 66), "solo tu celular · gratis", font=mono(22), fill=INK, anchor="ra")
    im.save(out, optimize=True)

if __name__ == "__main__":
    a = sys.argv[1:] + ["", "", "sede"][len(sys.argv) - 2:]
    make(a[0], a[1], a[2], a[3] or "sede")
