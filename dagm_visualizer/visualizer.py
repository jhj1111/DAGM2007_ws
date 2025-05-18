import cv2, os

class Visualizer:
    """
    이미지에 클래스, 결함 여부, 결함 위치를 시각화하는 클래스
    """

    def __init__(self, resize_shape=(256, 256)):
        self.resize_shape = resize_shape

    def show_image(self, info, save_dir=None):
        """
        이미지 로드 후 결함 위치 표시 및 출력
        이미지 시각화 및 키 입력 처리:
        - q: 종료
        - s: 저장
        - 기타: 계속
        """
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.basename(CURRENT_DIR)
        UPPER_DIR = CURRENT_DIR.replace(f'\\{BASE_DIR}', '')
        DATASET_DIR = os.path.join(UPPER_DIR, 'DAGM_dataset')
        SAVE_DIR = os.path.join(DATASET_DIR, 'Boxed')
        save_dir = SAVE_DIR if save_dir is None else save_dir

        img = cv2.imread(info['path'], cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(f"Image not found: {info['path']}")

        scale_x = self.resize_shape[0] / img.shape[1]
        scale_y = self.resize_shape[1] / img.shape[0]

        img_resized = cv2.resize(img, self.resize_shape)

        if info['defect'] and info['ellipse'] is not None:
            params = info['ellipse']
            center = (int(params['x'] * scale_x), int(params['y'] * scale_y))
            axes = (int(params['major'] * scale_x / 2), int(params['minor'] * scale_y / 2))
            angle = params['angle']

            cv2.ellipse(img_resized, center, axes, angle*180/3.14, 0, 360, (0, 0, 255), 2)

        label = f"Class: {info['class']} | ImageNum: {info['img_num']} | Defect: {'Yes' if info['defect'] else 'No'}"
        annotation = "press 'q' to quick, 's' to save"
        cv2.putText(img_resized, label, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img_resized, annotation, (10, self.resize_shape[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("DAGM2007 Visualizer", img_resized)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()

        if key == ord('q'):
            return 'quit'
        elif key == ord('s'):
            if save_dir:
                os.makedirs(save_dir, exist_ok=True)
                filename = os.path.basename(info['path'])
                save_path = os.path.join(save_dir, f"saved_{filename}")
                cv2.imwrite(save_path, img_resized)
                print(f"✅ 저장됨: {save_path}")
            return 'save'
        else:
            return 'next'
