import os, random
import pandas as pd
# import pandas
from glob import glob

class DatasetManager:
    """
    DAGM2007 데이터셋을 관리하는 클래스
    - 정상/결함 이미지 리스트 관리
    - 결함 여부 및 위치 정보(csv) 로딩 및 매핑
    """

    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.class_dirs = self._get_class_dirs()
        self.defect_info = self._load_defect_csv()

    def _get_class_dirs(self):
        """
        Class 폴더와 *_def 폴더를 구분해서 리스트화
        """
        dirs = glob(os.path.join(self.dataset_dir, "*"))
        class_dirs = {'normal': {}, 'defect': {}}

        for d in dirs:
            if not os.path.isdir(d):
                continue  # 폴더가 아닌 경우 스킵

            base = os.path.basename(d)
            if "def" in base:
                class_idx = int(base.replace("Class", "").replace("_def", ""))
                class_dirs['defect'][class_idx] = d
            elif "Class" in base:
                class_idx = int(base.replace("Class", ""))
                class_dirs['normal'][class_idx] = d

        return class_dirs

    def _load_defect_csv(self):
        """
        def_?.csv 파일을 불러와서 결함 위치 정보를 저장
        """
        defect_info = {}
        csv_files = glob(os.path.join(self.dataset_dir, "def_?.csv"))

        for csv_path in csv_files:
            class_idx = int(os.path.basename(csv_path).split("_")[1].split(".")[0])
            df = pd.read_csv(csv_path, sep=',', header=0)  # CSV는 쉼표 기준
            defect_info[class_idx] = {
                row['filename']: {
                    'x': row['x'],
                    'y': row['y'],
                    'angle': row['angle'],
                    'major': row['w'],
                    'minor': row['h']
                }
                for _, row in df.iterrows()
            }

        return defect_info

    def get_image_info(self, class_idx, idx, defect=False):
        """
        이미지 경로와 결함 여부, 결함 위치 정보를 반환
        """
        folder = self.class_dirs['defect' if defect else 'normal'][class_idx]
        filename = f"{idx:03d}.png"
        img_path = os.path.join(folder, filename)

        defect_data = None
        if defect:
            defect_data = self.defect_info.get(class_idx, {}).get(filename, None)
            print('defect_data =', defect_data)

        return {
            'path': img_path,
            'class': class_idx,
            'img_num': idx,
            'defect': defect and defect_data is not None,
            'ellipse': defect_data
        }

    def get_random_image_info(self, defect_only=False):
        """
        랜덤으로 이미지 정보를 반환
        """
        defect = random.choice([True, False]) if not defect_only else True
        class_idx = random.choice(list(self.class_dirs['defect'].keys() if defect else self.class_dirs['normal'].keys()))

        max_idx = 149 if defect else 999
        idx = random.randint(0, max_idx)+1

        return self.get_image_info(class_idx, idx, defect)
