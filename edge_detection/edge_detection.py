import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import PIL.Image as Image
from glob import glob

def load_image(image_path):
    """Load an image from the specified file path."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    return image

def image_cropper(image, top, bottom, left, right, compress_ratio=1):
    """Crop the image to the specified dimensions."""
    return np.ascontiguousarray(image[top:bottom:compress_ratio, left:right:compress_ratio, :])

def draw_line(img, theta, rho):
    h, w = img.shape[:2]
    # 直線が垂直のとき
    if np.isclose(np.sin(theta), 0):
        x1, y1 = rho, 0
        x2, y2 = rho, h
    # 直線が垂直じゃないとき
    else:
        # 直線の式を式変形すればcalc_yの式がもとまる(解説を後述します)．
        calc_y = lambda x: rho / np.sin(theta) - x * np.cos(theta) / np.sin(theta)
        x1, y1 = 0, calc_y(0)
        x2, y2 = w, calc_y(w)
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
    # 直線を描画
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

def corssing_point(rho1, theta1, rho2, theta2):
    """Calculate the crossing point of two lines given in polar coordinates."""
    A = np.array([[np.cos(theta1), np.sin(theta1)],
                  [np.cos(theta2), np.sin(theta2)]])
    b = np.array([[rho1],
                  [rho2]])
    if np.linalg.det(A) == 0:
        return None  # Lines are parallel
    x0, y0 = np.linalg.solve(A, b)
    return (int(np.round(x0)), int(np.round(y0)))

if __name__ == "__main__":
    files = glob(os.path.join("images", "*"))
    # files = glob(os.path.join("images", "curve.jpg"))
    for file in files:
        # image_path = "images/small_curve.jpeg"
        image_path = file
        image = load_image(image_path)
        cropped_image = np.zeros(image.shape)
        if cropped_image.shape[1] > 1500:
            cropped_image = image_cropper(image, int(image.shape[0]//2), image.shape[0], 0, image.shape[1], 3)  # crop bottom half
        else:
            cropped_image = image_cropper(image, int(image.shape[0]//2), image.shape[0], 0, image.shape[1], 1)  # crop bottom half
        
        blurred_image = cv2.GaussianBlur(cropped_image, (5, 5), 0)
        print(f"Image shape: {cropped_image.shape}")
        
        # edge detection using Canny
        edges = cv2.Canny(blurred_image, 50, 150)
        im_lines = cv2.HoughLines(edges, rho=1.5, theta=np.pi/360, threshold=100)
        positive_lines = []
        negative_lines = []
        for line in im_lines:
            rho, theta = line[0]
            if np.sin(theta) < 0.99:
                if theta < np.pi / 2:
                    positive_lines.append(line)
                else:
                    negative_lines.append(line)
            
        if len(positive_lines) > 0:
            # for line in positive_lines:
            line = positive_lines[0]
            rho, theta = line[0]
            # print(line)
            # print(f"rho: {rho}, theta: {theta}")
            # print(f"sin(theta): {np.sin(theta)}, cos(theta): {np.cos(theta)}")
            # if np.sin(theta) < 0.99:  # vertical lines
            draw_line(cropped_image, theta, rho)
            # cv2.imshow("Canny Edges", cropped_image)
            # cv2.waitKey(0)
        
        if len(negative_lines) > 0:
            # for line in negative_lines:
            line = negative_lines[0]
            rho, theta = line[0]
            print(line)
            print(f"rho: {rho}, theta: {theta}")
            print(f"sin(theta): {np.sin(theta)}, cos(theta): {np.cos(theta)}")
            # if np.sin(theta) < 0.99:  # vertical lines
            draw_line(cropped_image, theta, rho)
        
        if len(positive_lines) > 0 and len(negative_lines) > 0:
            rho1, theta1 = positive_lines[0][0]
            rho2, theta2 = negative_lines[0][0]
            point = corssing_point(rho1, theta1, rho2, theta2)
            if point is not None:
                cv2.circle(cropped_image, point, 10, (255, 0, 0), -1)
        cv2.imshow("Canny Edges", cropped_image)
        cv2.waitKey(0)
        cv2.imshow("Canny Edges", edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()