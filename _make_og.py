from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H), (10, 10, 22))
draw = ImageDraw.Draw(img)

# Diagonal gradient: deep purple -> magenta -> pink (brand colors)
top_left = (88, 28, 135)      # #581C87 purple-900
mid = (192, 38, 211)          # #C026D3 fuchsia-600
bottom_right = (236, 72, 153) # #EC4899 pink-500

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

for y in range(H):
    for x in range(W):
        t = (x + y) / (W + H)
        if t < 0.5:
            c = lerp(top_left, mid, t * 2)
        else:
            c = lerp(mid, bottom_right, (t - 0.5) * 2)
        draw.point((x, y), fill=c)

# Subtle dark vignette overlay for text contrast
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for i in range(120):
    alpha = int(70 * (i / 120))
    od.rectangle([(0, H - 380 + i * 2), (W, H)], fill=(10, 10, 22, alpha))
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img)

# Fonts - try Plus Jakarta if installed, fallback to system
def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\PlusJakartaSans-Bold.ttf" if bold else r"C:\Windows\Fonts\PlusJakartaSans-Regular.ttf",
        r"C:\Windows\Fonts\seguibl.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

f_brand = load_font(78, bold=True)
f_tag = load_font(44, bold=True)
f_sub = load_font(28, bold=False)
f_mark = load_font(72, bold=True)

# R mark - rounded square top-left
mark_x, mark_y, mark_size = 80, 80, 110
draw.rounded_rectangle(
    [(mark_x, mark_y), (mark_x + mark_size, mark_y + mark_size)],
    radius=24,
    fill=(255, 255, 255, 255)
)
# Center "R" in mark
mark_text = "R"
bbox = draw.textbbox((0, 0), mark_text, font=f_mark)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw.text(
    (mark_x + (mark_size - tw) / 2 - bbox[0], mark_y + (mark_size - th) / 2 - bbox[1] - 4),
    mark_text, fill=(168, 39, 219), font=f_mark
)

# "ReachPundit" wordmark next to mark
brand_x = mark_x + mark_size + 28
brand_y = mark_y + 20
draw.text((brand_x, brand_y), "ReachPundit", fill=(255, 255, 255), font=load_font(56, bold=True))

# Main headline (centered, bottom 1/3)
headline = "Websites, Apps & Marketing"
bbox = draw.textbbox((0, 0), headline, font=f_brand)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) / 2, 280), headline, fill=(255, 255, 255), font=f_brand)

# Sub headline
sub1 = "Built for small business owners"
bbox = draw.textbbox((0, 0), sub1, font=f_tag)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) / 2, 410), sub1, fill=(255, 255, 255), font=f_tag)

# Bottom line: pricing
sub2 = "From $497   ·   Shipped in 7 to 14 days   ·   Free 15-min consult"
bbox = draw.textbbox((0, 0), sub2, font=f_sub)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) / 2, 500), sub2, fill=(240, 230, 250), font=f_sub)

# Domain bottom-right
domain = "reachpundit.com"
bbox = draw.textbbox((0, 0), domain, font=f_sub)
tw = bbox[2] - bbox[0]
draw.text((W - tw - 60, H - 60), domain, fill=(255, 255, 255), font=f_sub)

out = r"C:\Users\nirma\growth-mantra\og-image.png"
img.save(out, "PNG", optimize=True)
print("WROTE:", out, "size:", os.path.getsize(out), "bytes")
