import numpy as np
import cv2
from cv2.typing import MatLike


class ImageHandler:
    def __init__(self, path: str):

        self.image_matrix: MatLike | None = cv2.imread(path)

        if self.image_matrix is None:
            self.image: MatLike = np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            self.image: MatLike = self.image_matrix

    def makeBlur(
        self, image: MatLike | None, ksize: tuple[int, int], show: bool = True
    ) -> MatLike:
        if image is None:
            image = self.image
        blurred_image = cv2.blur(image, ksize=ksize)
        if show:
            cv2.imshow("blurred_image", blurred_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return blurred_image

    def makeGaussianBlur(
        self,
        image: MatLike | None,
        ksize: tuple[int, int],
        sigmaX: int | float,
        show: bool = True,
    ) -> MatLike:
        if image is None:
            image = self.image
        gaussian_blurred = cv2.GaussianBlur(image, ksize=ksize, sigmaX=sigmaX)
        if show:
            cv2.imshow("gaussian_blurred", gaussian_blurred)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return gaussian_blurred

    def makeMedianBlur(
        self, image: MatLike | None, ksize: int, show: bool = True
    ) -> MatLike:
        if image is None:
            image = self.image
        median_blurred = cv2.medianBlur(image, ksize=ksize)
        if show:
            cv2.imshow("median_blurred", median_blurred)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return median_blurred

    def makeBilateralFilter(
        self,
        image: MatLike | None,
        diam: int,
        sigmaColor: int,
        sigmaSpace: int,
        show: bool = True,
    ) -> MatLike:
        if image is None:
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
        image: MatLike | None,
        kernel: MatLike,
        iterations: int = 1,
        show: bool = True,
    ):
        if image is None:
            image = self.image
        eroded_image = cv2.erode(image, kernel, iterations=iterations)

        if show:
            cv2.imshow("eroded_image", eroded_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return eroded_image

    def makeDilate(
        self,
        image: MatLike | None,
        kernel: MatLike,
        iterations: int = 1,
        show: bool = True,
    ) -> MatLike:

        if image is None:
            image = self.image

        dilated_image = cv2.dilate(image, kernel, iterations=iterations)

        if show:
            cv2.imshow("dilated_image", dilated_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return dilated_image

    def del_noise_binary(
        self, image: MatLike | None, kernel, iterations: int = 1, show: bool = True
    ) -> MatLike:

        if image is None:
            image = self.image

        binary_image = cv2.dilate(
            cv2.erode(image, kernel, iterations=iterations),
            kernel,
            iterations=iterations,
        )
        if show:
            cv2.imshow("binary_image", binary_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return binary_image

    def apply_clahe(
        self,
        image: MatLike | None,
        clip_limit: float | int,
        grid_size: tuple[int, int],
        show: bool = True,
    ) -> MatLike:
        """
        Применяет CLAHE (Contrast Limited Adaptive Histogram Equalization) к изображению.

        Параметры:
        - image: входное изображение
        - clip_limit: порог ограничения контраста (больше значение = больше контраст)
        - grid_size: размер сетки для адаптивного выравнивания (x, y)
        """

        if image is None:
            image = self.image

        # Создаем объект CLAHE с заданными параметрами
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)

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
