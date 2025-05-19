#!/usr/bin/env python3
"""
compare_images.py

A script to decode two Base64-encoded images (possibly of different size, format, or compression)
and compare them using both perceptual hashing (pHash) and Structural Similarity Index (SSIM).

Dependencies:
  pip install pillow imagehash scikit-image numpy

Usage:
  python compare_images.py <base64_image1> <base64_image2>

Each argument should be the raw Base64 string, or prefixed data URI like:
"data:image/png;base64,iVBORw0KGgoAAAANS..."
"""

import io
import base64
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import imagehash

imgs = []
for i in range(9):
    imgs.append(Image.open(f"templates/media/fragments/{i + 1}.jpeg"))

def decode_image(b64_data: str) -> Image.Image:
    """
    Decode a Base64 string (with or without data URI header) into a PIL Image.
    """
    # Strip data URI header if present
    if ',' in b64_data and b64_data.startswith('data:'):
        b64_data = b64_data.split(',', 1)[1]
    try:
        raw = base64.b64decode(b64_data)
        return Image.open(io.BytesIO(raw))
    except Exception as e:
        raise ValueError(f"Failed to decode Base64 image: {e}")


def compare_hash(img1: Image.Image, img2: Image.Image, hash_size: int = 8) -> int:
    """
    Compute perceptual hash (pHash) difference between two images.
    Returns the Hamming distance between hashes.
    """
    h1 = imagehash.phash(img1, hash_size=hash_size)
    h2 = imagehash.phash(img2, hash_size=hash_size)
    return h1 - h2


def compare_ssim(img1: Image.Image, img2: Image.Image) -> float:
    """
    Compute Structural Similarity Index (SSIM) between two images.
    Converts to grayscale and resizes both to the smaller dimensions.
    Returns a score between -1.0 and 1.0 (1.0 = identical).
    """
    # Convert to grayscale
    gray1 = img1.convert('L')
    gray2 = img2.convert('L')

    # Resize to match using LANCZOS resampling
    new_size = (min(gray1.width, gray2.width), min(gray1.height, gray2.height))
    gray1 = gray1.resize(new_size, Image.Resampling.LANCZOS)
    gray2 = gray2.resize(new_size, Image.Resampling.LANCZOS)

    arr1 = np.array(gray1)
    arr2 = np.array(gray2)

    score, _ = ssim(arr1, arr2, full=True)
    return score


def chock(level_numbr, b64_2):
    img1 = imgs[level_numbr]
    img2 = decode_image(b64_2)

    # Compare via perceptual hash
    hamming_dist = compare_hash(img1, img2)
    # Compare via SSIM
    ssim_score = compare_ssim(img1, img2)

    return hamming_dist, ssim_score

    # print(f"Perceptual hash difference (Hamming distance): {hamming_dist}")
    # print(f"Structural Similarity Index (SSIM): {ssim_score * 100:.2f}%")



