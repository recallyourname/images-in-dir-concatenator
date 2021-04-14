from PIL import Image
from os import listdir, makedirs
from os.path import isfile, join, isdir
import errno
import pathlib
from math import sqrt, ceil
from tqdm import tqdm

current_path = pathlib.Path(__file__).parent.absolute()

def create_result_image(images_list, prop1, prop2):
    directory_name = str(current_path).replace("\\", "/")+'/results/'
    try:
        makedirs(directory_name)
    except OSError as exc: 
        if exc.errno == errno.EEXIST and isdir(directory_name):
            pass
    result_img_height = 0
    result_img_width = 0
    for row in images_list:
        if row: 
            print(row)
            widths, heights = zip(*(img.size for img in row))
            result_img_height += max(heights)
            if result_img_width < sum(widths):
                result_img_width = sum(widths)
    result_img = Image.new('RGBA', (result_img_width, result_img_height))
    y_offset = 0
    for row in tqdm(images_list):
        x_offset = 0
        if row:
            y_increment = max([img.size[1] for img in row])
            for img in row:
                result_img.paste(img, (x_offset, y_offset))
                x_offset += img.size[0]
        y_offset += y_increment
    
    result_img.save(directory_name+'Result_{}x{}.png'.format(prop1, prop2))

def define_images_position(pictures, numH, numV):
    images_list = []
    temp_list = []

    for k in range(1, numV):
        for j in range((k-1)*numH, k*numH):
            if j > pictures.__len__() - 1:
                break
            temp_list.append(pictures[j])
      
        images_list.append([Image.open(item) for item in temp_list])
        temp_list *= 0

    return images_list

def count_allocation(pictures, prop1, prop2):
    scale = sqrt(pictures / prop1*prop2)
    scale_limit = 0
    while 1:
        scale_limit += 1
        if scale/prop2 <= scale_limit <= scale/prop1:
            break
        
    scaled_proportions = [(prop1*i, prop2*i) for i in range(1, scale_limit+1)]
    return scaled_proportions[-1] 


def iterate_pngs(pic):
    return(int(pic.removeprefix('file_').removesuffix('.png')))

def get_pngs():
    mypath = current_path
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    pngs = [f for f in onlyfiles if ('.png' in f)]
    pngs.sort(key=iterate_pngs)
    return pngs

def main():
    prop1, prop2 = input('enter proportions> ').split('x')
    pictures = get_pngs()
    numH, numV = count_allocation(pictures.__len__(), int(prop1), int(prop2))
    images_list = define_images_position(pictures, numH, numV)
    create_result_image(images_list, prop1, prop2)


if __name__ == "__main__":
    main()
