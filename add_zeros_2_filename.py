import os, shutil
from glob import glob

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(CURRENT_DIR, 'DAGM_dataset')

def get_class_dirs():
    """
    Class 폴더와 *_def 폴더를 구분해서 리스트화
    """
    dirs = glob(os.path.join(DATASET_DIR, "*"))

    for d in dirs:
        if not os.path.isdir(d):
            continue  # 폴더가 아닌 경우 스킵
        os.chdir(d)
        images_list = glob('*')
        
        for img in images_list:
            if not img.endswith('.png'): 
                continue

            img_name = os.path.basename(img)
            img_name_with_zeros = f'{int(img_name.split('.')[0]):03d}.png'
            shutil.move(img_name, img_name_with_zeros)

if __name__ == '__main__':
    get_class_dirs()