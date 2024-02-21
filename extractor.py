import cv2
import numpy as np
from ocr.OCR import detect_number


class KtpExtractor:
    def __init__(self, ktp_image: str):
        self.ktp_image = cv2.imread(ktp_image)

    def detect_ktp(self) -> np.ndarray | tuple:
        img_gray = cv2.cvtColor(self.ktp_image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

        # Contours
        detected_contours = img_gray.copy()
        contours, hierarchy = cv2.findContours(
            binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        detected_contours = cv2.drawContours(
            detected_contours, contours, -1, (0, 255, 0), cv2.FILLED
        )

        # get the first four big contours
        cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                screenCnt = approx
                break
        corners = screenCnt.reshape(-1, 2)
        corner_indexes = [0, 1, 2, 3]

        extracted_ktp = self.perspective_transforms(corners[corner_indexes])

        if extracted_ktp.shape[0] > extracted_ktp.shape[1]:
            corner_indexes = [1, 2, 3, 0]
            extracted_ktp = self.perspective_transforms(corners[corner_indexes])

        ktp_boxes = self.ktp_image.copy()
        cv2.polylines(ktp_boxes, [corners], True, (0, 0, 255), 5)
        for cor in corners:
            cv2.circle(ktp_boxes, tuple(cor), 15, (0, 255, 0), -1)

        return extracted_ktp, (
            self.ktp_image,
            img_gray,
            binary_image,
            detected_contours,
            ktp_boxes,
        )

    def perspective_transforms(self, corners: np.ndarray) -> np.ndarray:
        pt_A, pt_B, pt_C, pt_D = corners

        # Here, I have used L2 norm. You can use L1 also.
        width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
        width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
        maxWidth = max(int(width_AD), int(width_BC))

        height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
        height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
        maxHeight = max(int(height_AB), int(height_CD))

        input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
        output_pts = np.float32(
            [
                [0, 0],
                [0, maxHeight - 1],
                [maxWidth - 1, maxHeight - 1],
                [maxWidth - 1, 0],
            ]
        )

        transform = cv2.getPerspectiveTransform(input_pts, output_pts)
        out = cv2.warpPerspective(
            self.ktp_image, transform, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR
        )

        return out


class NikExtractor(KtpExtractor):
    def __init__(self, ktp_image: str):
        super().__init__(ktp_image)

    def get_nik_region(self) -> np.ndarray | tuple:
        detected_ktp, _ = self.detect_ktp()
        detected_ktp_copy = detected_ktp.copy()
        detected_ktp = cv2.cvtColor(detected_ktp, cv2.COLOR_BGR2GRAY)
        _, thresh_card = cv2.threshold(detected_ktp, 100, 255, cv2.THRESH_BINARY_INV)

        # Image Dilation to get the text region
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilate = cv2.dilate(thresh_card, kernel, iterations=7)
        dilate_copy = dilate.copy()

        img_list = []
        wide_list = []
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i, c in enumerate(cnts[0][::-1]):
            if i == 0:
                continue
            if i == 4:
                break

            x, y, w, h = cv2.boundingRect(c)
            img_list.append(thresh_card[y : y + h, x : x + w])
            wide_list.append(w)

            cv2.rectangle(dilate_copy, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.putText(
                dilate_copy,
                f"{i}",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                1,
                cv2.LINE_AA,
            )

            cv2.rectangle(detected_ktp_copy, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.putText(
                detected_ktp_copy,
                f"{i}",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                1,
                cv2.LINE_AA,
            )

        nik = img_list[wide_list.index(max(wide_list))]
        return nik, (thresh_card, dilate_copy, detected_ktp_copy)

    def get_nik_numbers(self) -> list | tuple:
        """
        Process:
        - Dilate to get the contours and boxes of numbers
        - Erode to do the OCR
        """

        extracted_nik_region, _ = self.get_nik_region()
        _, thresh_nik = cv2.threshold(extracted_nik_region, 120, 255, cv2.THRESH_BINARY)

        # Get contours from dilated image
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        dilate = cv2.dilate(thresh_nik, dilate_kernel, iterations=10)
        nik_contours = cv2.findContours(
            dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        eroded = cv2.erode(thresh_nik, erode_kernel, iterations=2)

        # Make copy of eroded NIK
        result = cv2.cvtColor(eroded.copy(), cv2.COLOR_GRAY2BGR)

        number_images = []
        number_boxes = sorted(nik_contours[0], key=lambda x: cv2.boundingRect(x)[0])
        for i, c in enumerate(number_boxes):
            x, y, w, h = cv2.boundingRect(c)
            number_images.append(eroded[y : y + h, x : x + w])
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(
                result,
                str(i),
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.3,
                (0, 0, 255),
                1,
                cv2.LINE_AA,
            )

        return number_images, (dilate, result)

    def extract_number_images(self) -> str:
        image_list, _ = self.get_nik_numbers()
        result = detect_number(image_list)
        return result


if __name__ == "__main__":
    tes = NikExtractor("assets/sample.jpg")
    result = tes.extract_number_images()
    print(result)
