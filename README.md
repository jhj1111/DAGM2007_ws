# [DAGM2007 Datasets](.\DAGM_dataset/)

> DAGM2007 데이터셋 저장소

# [DAGM2007 Defect Visualizer](.\dagm_visualizer/)

> DAGM2007 데이터셋 기반으로 클래스/결합 유무/결합 위치를 시각화하는 Python 도구

# [DAGM2007 YOLO-segment Datasets](.\yoloseg_datasets/)

> DAGM2007 YOLO-segment 학습용 데이터셋 저장소

---

## 프로젝트 구조

```
DAGM2007/
├── dagm_visualizer/
│   ├── dataset_manager.py      # 데이터 로딩 및 결합 위치 매핑
│   ├── visualizer.py           # 이미지 시각화 (ellipse 표시)
│   ├── controller.py           # 사용자 입력 처리
│   ├── main.py                 # CLI 진입점
│   └── README.md               # 설명 파일 (현재 문서)
├── DAGM_dataset/               # 이미지 및 라벨 데이터 폴더
│   ├── Class1/
│   ├── Class1_def/
│   ├── Class2/
│   ├── Class2_def/
│   ├── Class3/
│   ├── Class3_def/
│   ├── Class4/
│   ├── Class5/
│   ├── Class5_def/
│   ├── def_1.csv  # Class1 결합 위치 정보
│   ├── def_2.csv
│   ├── def_3.csv
│   ├── def_4.csv
│   ├── def_5.csv
├── add_zeros_2_filename.py     # 이미지 이름을 3자리로 일괄 변경
└── cut_data.py                 # labels.txt → def_?.csv 변환 스크립트
```
**파일 트리 준수**
---

## Train 파일

- google colab 환경 실행 추천

### [DAGM2007_train.ipny](./DAGM2007_train.ipny)

> 이미지 분류 모델 학습 파일(resnet)

### [DAGM2007_YOLO_train.ipny](./DAGM2007_YOLO_train.ipny)

> YOLO segmentation 모델 학습 파일(YOLOv8_segment)

---

## 기타 파일

### `add_zeros_2_filename.py`

* `DAGM_dataset/Class*_def/*.png`의 이름을 `001.png ~ 150.png` 형식으로 일괄화

### `cut_data.py`

* `Class*_def/labels.txt` 파일을 파싱해 `def_?.csv` 형식으로 변환
* 사용 포맷: `filename,class,label,x,y,angle,w,h`

---

## 필수 라이브러리 설치

```bash
pip install opencv-python pandas
```

---

## 참고 링크

* [DAGM 2007 Dataset](https://conferences.mpi-inf.mpg.de/dagm/2007/prizes.html)
* [Ultralatics Docs-segmnet](https://docs.ultralytics.com/ko/tasks/segment/#predict)

---
