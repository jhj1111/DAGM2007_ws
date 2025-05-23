# 코드 실행 세션이 초기화되었으므로 전체 기능을 통합한 완성 코드 실행
import os
import shutil
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import yaml
from glob import glob

# 기본 경로
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_BASE_DIR = os.path.basename(CURRENT_DIR)
BASE_DIR = CURRENT_DIR.replace(f'\\{CURRENT_BASE_DIR}', '')          # ~/DAGM2007
DAGM_DATASET_DIR = os.path.join(BASE_DIR, 'DAGM_dataset')
OUTPUT_BASE_DIR = os.path.join(BASE_DIR, "yoloseg_datasets")
# OUTPUT_BASE_DIR = CURRENT_DIR

# 타원 → polygon 변환
def ellipse_to_polygon(cx, cy, rx, ry, img_w, img_h, num_points=20):
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x_points = cx + rx * np.cos(angles)
    y_points = cy + ry * np.sin(angles)
    x_points /= img_w
    y_points /= img_h
    return [coord for xy in zip(x_points, y_points) for coord in xy]

# 클래스별 YOLOv8 segmentation 데이터셋 생성
def generate_yoloseg_dataset(class_idx, csv_path, def_img_dir, normal_img_dir=None,
                              img_w=512, img_h=512, split_ratios=(0.8, 0.1, 0.1)):
    df = pd.read_csv(csv_path)
    output_dir = os.path.join(OUTPUT_BASE_DIR, f"yoloseg_dataset_class{class_idx}")
    images_dir = os.path.join(output_dir, "images")
    labels_dir = os.path.join(output_dir, "labels")

    for subset in ['train', 'val', 'test']:
        os.makedirs(os.path.join(images_dir, subset), exist_ok=True)
        os.makedirs(os.path.join(labels_dir, subset), exist_ok=True)

    def_data = [(row['filename'], ellipse_to_polygon(row['x'], row['y'], row['w']/2, row['h']/2, img_w, img_h))
                for _, row in df.iterrows()]
    normal_data = []
    if normal_img_dir and os.path.exists(normal_img_dir):
        for fname in sorted(os.listdir(normal_img_dir)):
            if fname.endswith(".png"):
                normal_data.append((fname, []))

    all_data = def_data + normal_data
    filenames = [x[0] for x in all_data]
    polygons = [x[1] for x in all_data]

    train_val_names, test_names, train_val_polys, test_polys = train_test_split(
        filenames, polygons, test_size=split_ratios[2], random_state=42)
    train_names, val_names, train_polys, val_polys = train_test_split(
        train_val_names, train_val_polys, test_size=split_ratios[1]/(split_ratios[0]+split_ratios[1]), random_state=42)

    subsets = {'train': zip(train_names, train_polys),
               'val': zip(val_names, val_polys),
               'test': zip(test_names, test_polys)}

    for subset, items in subsets.items():
        for fname, poly in items:
            src_path = os.path.join(def_img_dir if fname in df['filename'].values else normal_img_dir, fname)
            dst_img_path = os.path.join(images_dir, subset, fname)
            dst_lbl_path = os.path.join(labels_dir, subset, fname.replace(".png", ".txt"))
            if os.path.exists(src_path):
                shutil.copy(src_path, dst_img_path)
                with open(dst_lbl_path, "w") as f:
                    if poly:
                        f.write("0 " + " ".join(f"{p:.6f}" for p in poly))

    with open(os.path.join(output_dir, "data.yaml"), "w") as f:
        yaml.dump({
            'path': output_dir,
            'train': 'images/train',
            'val': 'images/val',
            'test': 'images/test',
            'names': {0: 'defect'}
        }, f)

    return output_dir

def main():
    # Class1~5에 대해 실행
    def_class_list = glob(os.path.join(DAGM_DATASET_DIR, 'Class?_def'))
    print(DAGM_DATASET_DIR)
    print(def_class_list)
    created_dirs = []
    for i in range(1, len(def_class_list)+1):
        csv_path = os.path.join(DAGM_DATASET_DIR, f"def_{i}.csv")
        def_img_dir = os.path.join(DAGM_DATASET_DIR, f"Class{i}_def")
        normal_img_dir = os.path.join(DAGM_DATASET_DIR, f"Class{i}")
        if os.path.exists(csv_path) and os.path.isdir(def_img_dir):
            out_dir = generate_yoloseg_dataset(i, csv_path, def_img_dir, normal_img_dir)
            created_dirs.append(out_dir)

if __name__ == '__main__':
    main()