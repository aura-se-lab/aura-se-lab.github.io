#!/usr/bin/env python3
"""Portrait pipeline for the People band — see docs/SPEC.html § 07.

Crops every portrait in src/assets/people/ to a 26:34 frame around the face,
and does nothing else. No exposure normalisation, no background separation, no
vignette, no sharpening: the photographs go out as they were taken.

Earlier versions graded them. Do not add that back — processed portraits of
real people look wrong, and the lab's own candid photographs are the point.
Crop and resize only.

Requires: opencv-python, pillow, numpy, and scripts/yunet.onnx
  (face_detection_yunet_2023mar.onnx from opencv/opencv_zoo).
"""
import io, math, os, sys
import cv2, numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "src", "assets", "people")
OUT  = os.path.join(SRC, "cropped")
MODEL = os.path.join(HERE, "yunet.onnx")
W, H = 560, 730
FACE_FRACTION = 0.285     # face height as a fraction of the crop height
FACE_FROM_TOP = 0.42      # where the face centre sits vertically


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
        im = im.resize((W, H), Image.LANCZOS)      # crop and resize only
        im.save(os.path.join(OUT, os.path.splitext(name)[0] + ".jpg"),
                quality=88, optimize=True, progressive=True)
        print(f"{name:34s} {'face' if box else 'NO FACE — centre crop'}")


if __name__ == "__main__":
    main()
