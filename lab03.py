from PIL import Image, ImageColor
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import rcParams


def load_image(path):
    img = Image.open(path)
    return img



def convert_to_grayscale(image):
    gray_img = image.convert('L')
    return gray_img



def convert_to_binary_matrix(gray_img):
    gray_matrix = np.array(gray_img)
    bin_matrix = np.where(gray_matrix > 100, 1, 0)
    return bin_matrix



dirs = \
[
    [-1,-1], [-1, 0], [-1,1],
    [0, -1], [0,  1],
    [1, -1], [1,  0], [1, 1]
]



def fill_label(bin_matrix, label_matrix, pos, label):
    h, w = bin_matrix.shape
    val = bin_matrix[pos[0], pos[1]]
    
    queue = deque([pos])

    while queue:
        [r,c] = queue.popleft()
        # print(r,c, len(queue))
        label_matrix[r, c] = label
        
        for d in dirs:
            [r1, c1] = np.add([r,c], d)
            # print(r1, c1)
            # if next position is out of the matrix
            if r1 < 0 or r1 >= h:
                continue
            if c1 < 0 or c1 >= w:
                continue

            # if next position already has a label
            if label_matrix[r1, c1] != 0:
                continue

            # if next cell in different component
            if bin_matrix[r1,c1] != val:
                continue
            
            # mark that r1,c1 is added to queue
            label_matrix[r1, c1] = -1
            queue.append([r1,c1])



def convert_to_label_matrix(binary_matrix):
    h, w = binary_matrix.shape
    label_matrix = np.full((h, w), 0)
    n_color = 1
    
    for i in range(h):
        for j in range(w):
            if label_matrix[i,j] != 0:
                continue
            fill_label(binary_matrix, 
                label_matrix, [i,j], n_color)
            n_color += 1
    
    return label_matrix, n_color



def convert_to_color_matrix(label_matrix, n_color):
    h, w = label_matrix.shape

    color_matrix = np.zeros((h, w, 3), dtype=np.uint8)

    rand_colors = np.random.randint(0, 256, size=(n_color, 3))
    color_matrix[:, :, :] = rand_colors[0]

    for i in range(h):
        for j in range(w):
            label = label_matrix[i][j]
            color_matrix[i][j] = rand_colors[label]

    return color_matrix



def convert_to_color_image(color_matrix):
    colored_img = Image.fromarray(color_matrix, 'RGB')
    return colored_img



def show_side_by_side(img_a, img_b):
    # img_a.thumbnail((512, 512))
    # img_a.thumbnail((512, 512))
    
    fig, ax = plt.subplots(1,2)
    
    ax[0].imshow(img_a)
    ax[1].imshow(img_b)

