# Diver26 OSINT CTF — read_qr Write-up

## Challenge Summary

The challenge provides an image (`qrcode.png`) containing an embedded QR code.
The goal is to extract the URL encoded inside it **without scanning it with a
mobile phone camera** — the point of the exercise is to practice with OSINT tools rather than relying on a phone app that might auto-open the link to a wrong url(which can be risky if the QR points to something malicious, and defeats the purpose of the exercise).

## Why not scan with a phone?

- Phone QR scanners often auto-follow the link, which is bad practice for OSINT/security work — you should inspect a URL before visiting it.
- The challenge is testing familiarity with scriptable, repeatable tools (useful when you need to process many QR codes, or extract one from a  low-quality/partial image that phone scanners choke on).

## Prerequisites
Install the essential libraries
```bash
pip install -r requirements.txt --break-system-packages
```

Place `qrcode.png` in your working directory before running the script.

## Method 1 — OpenCV (as given in the challenge)

```python
import cv2

# Read the image file
image = cv2.imread("qrcode.png")

# Initialize the OpenCV QR code detector
detector = cv2.QRCodeDetector()

# Detect and decode the data
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

if data:
    print(f"Decoded Data: {data}")
else:
    print("QR Code not detected")
```

Run it with:

```bash
python3 decode_qr.py
```

or interactively:

```bash
python3
>>> import cv2
>>> image = cv2.imread("qrcode.png")
>>> detector = cv2.QRCodeDetector()
>>> data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
>>> print(data)
```

### If OpenCV fails to detect the code

OpenCV's built-in detector can struggle with low-resolution, rotated, or
noisy QR images. If `data` comes back empty, try preprocessing the image
first:

```python
import cv2

image = cv2.imread("qrcode.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Upscale small images — QR detectors often fail on tiny codes
gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

# Threshold to clean up noise/compression artifacts
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

detector = cv2.QRCodeDetector()
data, points, _ = detector.detectAndDecode(thresh)
print(f"Decoded Data: {data}" if data else "Still not detected — try Method 2")
```

## Notes

- This write-up assumes `qrcode.png` is a clean, single QR code image. If the
  challenge image contains the QR code embedded within a larger photo
  (e.g., a photo of a real-world sign or receipt), crop/isolate the QR
  region first for more reliable detection.
- Always keep decoding tools offline/local for CTF images — no need to upload
  challenge assets to third-party "QR decoder" websites, which is both
  unnecessary and could leak challenge data.
