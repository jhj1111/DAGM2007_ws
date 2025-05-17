class Controller:
    """
    DatasetManager와 Visualizer를 연결하는 인터페이스 클래스
    """

    def __init__(self, dataset_manager, visualizer):
        self.dataset_manager = dataset_manager
        self.visualizer = visualizer

    def show_image(self, class_idx=None, idx=None, defect=True, random_select=True):
        """
        랜덤 혹은 특정 이미지를 시각화
        """
        if random_select:
            info = self.dataset_manager.get_random_image_info(defect_only=defect)
        else:
            if class_idx is None or idx is None:
                raise ValueError("class_idx와 idx를 모두 지정해야 합니다.")
            info = self.dataset_manager.get_image_info(class_idx, idx, defect)

        self.visualizer.show_image(info)
