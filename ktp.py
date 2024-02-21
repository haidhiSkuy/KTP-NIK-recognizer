import cv2
import time
import argparse
import numpy as np
from utils import resize
from extractor import NikExtractor

start_time = time.time()

parser = argparse.ArgumentParser(description="Extrak Nomor NIK dari KTP")
parser.add_argument(
    "-i", "--image", type=str, help="path gambar ktp", default="assets/sample1.jpg"
)
parser.add_argument(
    "-p",
    "--proses",
    type=bool,
    help="tampilkan step by step image processing",
    default=False,
)
args = parser.parse_args()

path = args.image
detector = NikExtractor(path)
result = detector.extract_number_images()
print("+-----------------------+")
print(f"| NIK: {result} |")
print("+-----------------------+")

execution_time = time.time() - start_time
print(f"execution time: {execution_time:.2f}s")

if args.proses == True:
    extracted_ktp, (ktp_image, img_gray, binary_image, detected_contours, ktp_boxes) = (
        detector.detect_ktp()
    )
    nik, (thresh_card, dilate_copy, nik_region) = detector.get_nik_region()
    _, (dilate, result) = detector.get_nik_numbers()

    step1 = [ktp_image, img_gray, binary_image, detected_contours, ktp_boxes]
    step1 = [resize(img, scale_factor=0.17) for img in step1]
    step1 = np.concatenate(step1, axis=1)

    step2 = [extracted_ktp, thresh_card, dilate_copy, nik_region]
    step2 = [resize(img, scale_factor=0.4) for img in step2]
    step2 = np.concatenate(step2, axis=1)

    step3 = [dilate, result]
    step3 = [resize(img, scale_factor=0.9) for img in step3]
    step3 = np.concatenate(step3, axis=0)

    cv2.imshow("step 1", step1)
    cv2.imshow("step 2", step2)
    cv2.imshow("step 3", step3)

    cv2.waitKey(0)
