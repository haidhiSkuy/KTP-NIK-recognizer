import cv2
import numpy as np
from skimage.metrics import structural_similarity

with open("ocr/ocr_number.npy", "rb") as f:
    ocr_image_array = np.load(f)


def detect_number(number_images: list):
    final_results = []
    for img in number_images:
        img = cv2.resize(img, (20, 30))

        ssi, label = [], []
        for i, ocr in enumerate(ocr_image_array):
            ssi_index, _ = structural_similarity(img, ocr, full=True)
            ssi.append(ssi_index)
            label.append(i)

        ssi_max = ssi.index(max(ssi))
        predicted = label[ssi_max]
        final_results.append(predicted)

    return "".join([str(i) for i in final_results])

if __name__ == "__main__":
    img1 = [cv2.cvtColor(i, cv2.COLOR_GRAY2BGR) for i in ocr_image_array[0:5]]
    img1 = np.concatenate(img1, axis=1)

    img2 = [cv2.cvtColor(i, cv2.COLOR_GRAY2BGR) for i in ocr_image_array[5:]]
    img2 = np.concatenate(img2, axis=1)

    cv2.imshow("", np.concatenate([img1,img2], axis=0))
    cv2.waitKey(0)
