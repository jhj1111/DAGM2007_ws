import os
import re
import pandas as pd

# BASE_PATH = "/home/jw22/Desktop/dagm_test/DAGM_dataset/extracted"
# 현재 파이썬 파일 위치 기준으로 상대 경로 설정
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(CURRENT_DIR)

def parse_labels_to_csv(class_num, extension='txt'):
    label_name = 'labels.txt'
    if extension=='txt':
        label_path = os.path.join(CURRENT_DIR, 'DAGM_dataset', f"Class{class_num}_def", "labels.txt")
    elif extension=='csv':
        label_name = f'def_{class_num}.csv'
        label_path = os.path.join(CURRENT_DIR, 'DAGM_dataset', f'def_{class_num}.csv')

    if not os.path.exists(label_path):
        print(f"❌ Class{class_num}_def: {label_name} 없음")
        return

    with open(label_path, "r") as f:
        lines = f.readlines()

    records = []
    for idx, line in enumerate(lines):
        parts = re.split(r"\s+", line.strip())
        if len(parts) > 7:
            print(f"⚠️ Class{class_num} line {idx + 1} → 파싱 실패: '{line.strip()}'")
            continue
        try:
            w, h, angle, x, y = map(float, parts[1:6])
        except ValueError:
            print(f"🚫 Class{class_num} line {idx + 1} → 숫자 변환 실패: '{parts}'")
            continue

        records.append(
            {
                "filename": f"{idx+1:03d}.png",
                "class": class_num,
                "label": 1,
                "x": x,
                "y": y,
                "angle": angle,
                "w": w,
                "h": h,
            }
        )

    # 저장
    df = pd.DataFrame(records)
    out_csv = os.path.join(CURRENT_DIR, 'DAGM_dataset', f"def_{class_num}.csv")
    df.to_csv(out_csv, index=False)
    print(f"✅ Class{class_num} → 저장 완료: {out_csv}")


# 실행: Class1_def ~ Class5_def
for c in range(1, 7):
    parse_labels_to_csv(c)
