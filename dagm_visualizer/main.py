import os
import argparse
from dataset_manager import DatasetManager
from visualizer import Visualizer
from controller import Controller

if __name__ == "__main__":
    # 현재 파일 위치 기준 경로 설정
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.basename(CURRENT_DIR)
    UPPER_DIR = CURRENT_DIR.replace(f'\\{BASE_DIR}', '')
    DATASET_DIR = os.path.join(UPPER_DIR, 'DAGM_dataset')
    # print(CURRENT_DIR)
    # print(DATASET_DIR)
    os.chdir(CURRENT_DIR)

    # 모듈 초기화
    dm = DatasetManager(DATASET_DIR)
    # vis = Visualizer(resize_shape=(256, 256))
    vis = Visualizer(resize_shape=(512, 512))
    ctrl = Controller(dm, vis)

    def select_params(class_idx, idx, defect, random_select):
        if class_idx and idx:
            if defect is None:
                ctrl.show_image(class_idx=class_idx, idx=idx)
            else:
                ctrl.show_image(class_idx=class_idx, idx=idx, defect=defect)
        else:
            random_select = True
            if defect or defect is None:
                ctrl.show_image(defect=defect, random_select=random_select)
            else:
                ctrl.show_image(random_select=random_select)
        
    # CLI 인자 파싱
    parser = argparse.ArgumentParser(description="DAGM2007 이미지 시각화 도구")
    parser.add_argument('--class', dest='class_id', type=int, help='클래스 번호 (1~5)')
    parser.add_argument('--idx', type=int, help='이미지 index 번호')
    parser.add_argument('--defect', action='store_true', help='결함 이미지 여부')
    parser.add_argument('--random', action='store_true', help='랜덤 이미지 표시')

    args = parser.parse_args()

    class_idx = None
    idx = None
    defect = True
    random_select = None

    # 실행
    if not (args.class_id and args.idx and args.defect and args.random):    # 파일 실행
        select_params(class_idx, idx, defect, random_select)
    else:
        if args.random :
            ctrl.show_image(defect=args.defect, random_select=True)
        else:
            if args.class_id is None or args.idx is None:
                print("랜덤 모드가 아니면 --class와 --idx를 모두 지정해야 합니다.")
            else:
                ctrl.show_image(class_idx=args.class_id, idx=args.idx, defect=args.defect)