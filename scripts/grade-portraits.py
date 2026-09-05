#!/usr/bin/env python3
"""Portrait pipeline for the People band — see docs/SPEC.html § 07.

Crops every portrait in src/assets/people/ to a 26:34 frame around the face,
normalises exposure across the set, and pushes the background back so eight
photographs taken in eight different places read as one contact sheet.
The subject keeps full colour and full sharpness — do not desaturate faces.

Requires: opencv-python, pillow, numpy, and scripts/yunet.onnx
  (face_detection_yunet_2023mar.onnx from opencv/opencv_zoo).
"""
import io, math, os, sys
import cv2, numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "src", "assets", "people")
OUT  = os.path.join(SRC, "graded")
MODEL = os.path.join(HERE, "yunet.onnx")
W, H = 560, 730
FACE_FRACTION = 0.285     # face height as a fraction of the crop height
FACE_FROM_TOP = 0.42      # where the face centre sits vertically
TARGET_LUMA   = 0.485     # every portrait is pulled to this mean brightness


def detect(im):
    bgr = np.array(im)[:, :, ::-1].copy()
    d = cv2.FaceDetectorYN.create(MODEL, "", (im.width, im.height), 0.5, 0.3, 5000)
    _, f = d.detect(bgr)
    if f is None or not len(f):
        return None
    return [float(v) for v in max(f, key=lambda r: r[2] * r[3])[:4]]


def crop(im, box):
    if box is None:
        cw = min(im.width, im.height * (W / H)); ch = cw * (H / W)
        x0, y0 = (im.width - cw) / 2, (im.height - ch) * 0.1
        return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))), None
    fx, fy, fw, fh = box
    ch = fh / FACE_FRACTION
    cw = ch * (W / H)
    sc = min(1.0, im.width / cw, im.height / ch)
    cw, ch = cw * sc, ch * sc
    x0 = max(0, min(fx + fw / 2 - cw / 2, im.width - cw))
    y0 = max(0, min(fy + fh / 2 - ch * FACE_FROM_TOP, im.height - ch))
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))), (fx - x0, fy - y0, fw, fh)


def grade(im, fb):
    fx, fy, fw, fh = fb
    LUMA = np.array([.2126, .7152, .0722], np.float32)
    a0 = np.asarray(im).astype(np.float32) / 255.
    lo, hi = np.percentile(a0 @ LUMA, [1.0, 99.0])
    a = np.clip((a0 - lo) / max(hi - lo, 1e-3), 0, 1)
    a = a0 * 0.45 + a * 0.55                 # gentle — a full stretch blows out plain walls
    a = a * a * (3 - 2 * a) * 0.24 + a * 0.76  # soft filmic S
    a = 0.015 + a * (1 - 0.030)                # lift blacks, hold whites off 1.0
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

    l = ((np.asarray(im).astype(np.float32) / 255.) @ LUMA).mean()
    g = min(max(math.log(TARGET_LUMA) / math.log(max(l, 1e-3)), 0.80), 1.30)
    im = Image.fromarray((np.power(np.asarray(im).astype(np.float32) / 255., g) * 255).astype(np.uint8))

    bg = ImageEnhance.Color(im).enhance(0.30)
    bg = ImageEnhance.Brightness(bg).enhance(0.82)
    bg = ImageEnhance.Contrast(bg).enhance(0.92)
    bg = bg.filter(ImageFilter.GaussianBlur(3.4))
    mask = Image.new("L", im.size, 0)
    cx, cy = fx + fw / 2, fy + fh / 2
    ImageDraw.Draw(mask).ellipse(
        [cx - fw * 1.35, cy - fh * 1.45, cx + fw * 1.35, cy + fh * 2.60], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(fw * 0.62))
    im = Image.composite(im, bg, mask)

    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.3, percent=48, threshold=3))

    v = Image.new("L", im.size, 0)
    ImageDraw.Draw(v).ellipse(
        [-im.width * .26, -im.height * .22, im.width * 1.26, im.height * 1.22], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(im.width * 0.24))
    return Image.composite(im, ImageEnhance.Brightness(im).enhance(0.88), v)


def main():
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(MODEL):
        sys.exit("missing scripts/yunet.onnx — fetch face_detection_yunet_2023mar.onnx "
                 "from https://github.com/opencv/opencv_zoo")
    for name in sorted(os.listdir(SRC)):
        if not name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        im = Image.open(os.path.join(SRC, name)).convert("RGB")
        box = detect(im)
        im, fb = crop(im, box)
        s = W / im.width
        fb = (fb[0] * s, fb[1] * s, fb[2] * s, fb[3] * s) if fb else \
             (W * .30, H * .18, W * .40, H * .30)
        im = grade(im.resize((W, H), Image.LANCZOS), fb)
        im.save(os.path.join(OUT, os.path.splitext(name)[0] + ".jpg"),
                quality=84, optimize=True, progressive=True)
        print(f"{name:34s} {'face' if box else 'NO FACE — centre crop'}")


if __name__ == "__main__":
    main()
