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
    SAVE_DIR = os.path.join(DATASET_DIR, 'boxed_images')

    os.chdir(CURRENT_DIR)

    # 모듈 초기화
    dm = DatasetManager(DATASET_DIR)
    # vis = Visualizer(resize_shape=(256, 256))
    vis = Visualizer(resize_shape=(512, 512))
    ctrl = Controller(dm, vis)

    def run_loop(class_idx=None, idx=None, defect=True, random_select=True):
        """
        키 입력에 따른 반복 시각화 루프:
        - q: 종료
        - s: 저장
        - 기타: 다음 이미지
        """
        if class_idx is None and idx is None:
            random_select = True
            
        while True:
            info = None
            if random_select:
                info = dm.get_random_image_info(defect_only=defect)
            elif class_idx is not None and idx is not None:
                info = dm.get_image_info(class_idx, idx, defect)
            else:
                print("⚠️ class_idx와 idx를 모두 지정하거나 random_select=True 여야 합니다.")
                break

            action = vis.show_image(info, save_dir=SAVE_DIR)
            if action == 'quit':
                print("👋 종료합니다.")
                break
        
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

     # CLI 모드
    if any([args.class_id, args.idx, args.random]):
        if args.random:
            run_loop(defect=args.defect, random_select=True)
        elif args.class_id is not None and args.idx is not None:
            run_loop(class_idx=args.class_id, idx=args.idx, defect=args.defect, random_select=False)
        else:
            print("❗ --class와 --idx를 함께 지정하거나 --random 플래그를 사용하세요.")
    else:
        # 코드 직접 실행 모드
        run_loop(class_idx, idx, defect, random_select)