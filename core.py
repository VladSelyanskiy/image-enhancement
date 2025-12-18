import numpy as np
import cv2
from cv2.typing import MatLike


class ImageHandler:
    def __init__(
        self,
        path: str,
        height,
        weight,
        reduction_common,
        reduction_binary,
        opening,
        global_equ,
        contrast,
    ):
        self.height = height
        self.weight = weight
        self.reduction_common = reduction_common
        self.reduction_binary = reduction_binary
        self.opening = opening
        self.global_equ = global_equ
        self.contrast = contrast

        self.image_matrix: MatLike | None = cv2.imread(path)

        if self.image_matrix is None:
            self.image: MatLike = np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            self.image: MatLike = self.image_matrix

    def makeMedianBlur(self, show: bool = True) -> MatLike:

        image = self.image
        ksize = self.reduction_common

        median_blurred = cv2.medianBlur(image, ksize)

        if show:
            cv2.imshow("median_blurred", median_blurred)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return median_blurred

    def makeBilateralFilter(
        self,
        diam: int,
        sigmaColor: int,
        sigmaSpace: int,
        show: bool = True,
    ) -> MatLike:
        image = self.image
        filtered_image = cv2.bilateralFilter(
            image, d=diam, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace
        )
        if show:
            cv2.imshow("filtered_image", filtered_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return filtered_image

    def makeErode(
        self,
        show: bool = True,
    ):
        image = self.image
        kernel = np.ones((self.reduction_binary, self.reduction_binary), np.uint8)

        eroded_image = cv2.erode(image, kernel)

        if show:
            cv2.imshow("eroded_image", eroded_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return eroded_image

    def makeDilate(
        self,
        show: bool = True,
    ) -> MatLike:

        image = self.image
        kernel = np.ones((self.reduction_binary, self.reduction_binary), np.uint8)

        dilated_image = cv2.dilate(image, kernel)

        if show:
            cv2.imshow("dilated_image", dilated_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return dilated_image

    def delNoiseBinary(
        self,
        show: bool = True,
    ) -> MatLike:

        image = self.image
        kernel = np.ones((self.reduction_binary, self.reduction_binary), np.uint8)

        if self.opening:
            binary_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        else:
            binary_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

        if show:
            cv2.imshow(f"binary_image {self.opening}", binary_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return binary_image

    def applyClahe(
        self,
        show: bool = True,
    ) -> MatLike:
        """
        Применяет CLAHE (Contrast Limited Adaptive Histogram Equalization) к изображению.

        Параметры:
        - clip_limit: порог ограничения контраста (больше значение = больше контраст)
        - grid_size: размер сетки для адаптивного выравнивания (x, y)
        """

        image = self.image

        # Создаем объект CLAHE с заданными параметрами
        clahe = cv2.createCLAHE(clipLimit=self.contrast)

        # LAB лучше сохраняет цветовую информацию при изменении яркости
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        # Разделяем каналы: L - яркость, A и B - цветовые компоненты
        l_channel, a_channel, b_channel = cv2.split(lab)

        # Применяем CLAHE только к каналу яркости (L)
        l_channel_clahe = clahe.apply(l_channel)

        # Объединяем обработанный канал яркости с исходными цветовыми каналами
        lab_clahe = cv2.merge([l_channel_clahe, a_channel, b_channel])

        # Преобразуем обратно в BGR
        clahe_image = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

        if show:
            cv2.imshow("clahe_image", clahe_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return clahe_image

    def makeEqualization(self, show: bool = True) -> MatLike:
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        if self.global_equ:
            equalized_image = cv2.equalizeHist(image)
        else:
            clahe = cv2.createCLAHE()
            equalized_image = clahe.apply(image)

        if show:
            cv2.imshow("equalized_image", equalized_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return equalized_image
